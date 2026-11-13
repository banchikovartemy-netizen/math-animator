"""Independent, content-addressed segments; persistent Manim assets; lossless join."""
from dataclasses import asdict
import configparser
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from math_engine.checks import require_passed
from rendering.planner import ROOT,load_manifest,segments_for,fingerprint,safe_name
from validation.video import PROFILES,validate_video

def checked_solution(job):
    from rendering.cli import artifact_module
    m=load_manifest(job)
    path=(ROOT/m['solution']).resolve()
    if not path.is_relative_to(ROOT/'examples'):raise ValueError('Untrusted solution path')
    solution=artifact_module(path).build_solution()
    require_passed(solution.checks)
    if not solution.checks:raise ValueError('Mathematical checks required')
    return asdict(solution)

def cache_root():
    return Path(os.environ.get('MATH_ANIMATOR_CACHE',str(ROOT/'.cache/math-animator'))).resolve()

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def render_segment(job,mode,segment_id,smoke=False):
    started=time.monotonic();solution=checked_solution(job)
    segment=next((s for s in segments_for(job,smoke) if s['id']==segment_id),None)
    if segment is None:raise ValueError('Unknown scene segment')
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',segment['class']):raise ValueError('Invalid scene class')
    key=fingerprint(job,segment,mode,smoke)
    stage='smoke' if smoke else mode
    output=ROOT/'outputs'/job/stage/'segments'/segment_id
    output.mkdir(parents=True,exist_ok=True)
    target=output/f'{segment_id}.mp4'
    cached=cache_root()/'segments'/job/stage/segment_id/key
    report={'job':job,'mode':mode,'segment':segment_id,'fingerprint':key,'status':'failed','solution':solution}
    try:
        meta=cached/'segment.json';video=cached/'video.mp4'
        if meta.is_file() and video.is_file():
            saved=json.loads(meta.read_text())
            if saved['fingerprint']==key and saved['sha256']==digest(video):
                shutil.copy2(video,target)
                report.update(saved,cache_hit=True)
                report['seconds']=time.monotonic()-started
                return target
        assets=cache_root()/'assets'/job/segment_id
        media=cache_root()/'manim'/job/stage/segment_id
        assets.mkdir(parents=True,exist_ok=True);media.mkdir(parents=True,exist_ok=True)
        w,h,fps=PROFILES[mode]
        cfg=configparser.ConfigParser()
        cfg['CLI']={'media_dir':str(media),'tex_dir':str(assets/'Tex'),'text_dir':str(assets/'texts'),
                    'max_files_cached':'2000','disable_caching':'False','background_color':'#000000'}
        config_path=output/'manim.cfg'
        with config_path.open('w') as f:cfg.write(f)
        env=dict(os.environ);env['PYTHONPATH']=os.pathsep.join([str(ROOT/'src'),str(ROOT),env.get('PYTHONPATH','')])
        cmd=[sys.executable,'-m','manim',str(ROOT/segment['scene']),segment['class'],
             '--config_file',str(config_path),'--renderer','cairo','--resolution',f'{w},{h}',
             '--fps',str(fps),'--format','mp4','--output_file',segment_id]
        if 'range' in segment:cmd+=['-n',','.join(map(str,segment['range']))]
        with (output/'render.log').open('w') as log:
            subprocess.run(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1800)
        candidates=list((media/'videos').rglob(f'{segment_id}.mp4'))
        if len(candidates)!=1:raise ValueError('Expected one completed segment')
        shutil.copy2(candidates[0],target)
        report.update(video=validate_video(target,mode),status='passed',cache_hit=False,sha256=digest(target))
        layout=media/'layout.json'
        if layout.exists():report['layout']=json.loads(layout.read_text())
        cached.mkdir(parents=True,exist_ok=True)
        shutil.copy2(target,cached/'video.mp4')
        (cached/'segment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        return target
    except Exception as error:
        report['error']=str(error);raise
    finally:
        report['seconds']=time.monotonic()-started
        (output/'segment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        print(json.dumps({'segment':segment_id,'status':report['status'],'cache_hit':report.get('cache_hit',False),'seconds':report['seconds']}))

def assemble(job,mode,directory=None,smoke=False):
    started=time.monotonic();solution=checked_solution(job)
    stage='smoke' if smoke else mode
    output=ROOT/'outputs'/job/stage;output.mkdir(parents=True,exist_ok=True)
    source=Path(directory) if directory else output
    files=[];reports=[]
    for segment in segments_for(job,smoke):
        sid=segment['id']
        candidates=list(source.rglob(f'{sid}/segment.json'))
        if len(candidates)!=1:raise ValueError(f'Missing/duplicate segment {sid}')
        report=json.loads(candidates[0].read_text());video=candidates[0].parent/f'{sid}.mp4'
        if report['status']!='passed' or report['fingerprint']!=fingerprint(job,segment,mode,smoke):raise ValueError('Stale or failed segment')
        if report['solution']!=solution or report['sha256']!=digest(video):raise ValueError('Mathematics or segment content changed')
        files.append(video.resolve());reports.append(report)
    concat=output/'concat.txt'
    # Paths originate from checked artifacts; quote for the FFmpeg concat demuxer.
    concat.write_text(''.join("file '"+str(p).replace("'","'\\''")+"'\n" for p in files))
    target=output/f'{job}.mp4'
    command=['ffmpeg','-y','-v','warning','-f','concat','-safe','0','-i',str(concat),'-map','0:v:0','-c','copy','-movflags','+faststart',str(target)]
    with (output/'assembly.log').open('w') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    report={'job':job,'mode':mode,'smoke':smoke,'status':'passed','solution':solution,
            'video':validate_video(target,mode),'segments':reports,'assembly_seconds':time.monotonic()-started}
    (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    (output/'solution.json').write_text(json.dumps(solution,ensure_ascii=False,indent=2))
    print(target);return target

def render_job(job,mode='preview',segment=None,smoke=False,assemble_from=None,workers=3):
    safe_name(job)
    if smoke and mode!='preview':raise ValueError('Smoke uses preview profile')
    if assemble_from is not None:return assemble(job,mode,assemble_from,smoke)
    if segment:return render_segment(job,mode,segment,smoke)
    from concurrent.futures import ThreadPoolExecutor
    if not 1 <= workers <= 8:raise ValueError('workers must be 1..8')
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(render_segment,job,mode,item['id'],smoke) for item in segments_for(job,smoke)]
        for future in futures:future.result()
    return assemble(job,mode,smoke=smoke)
