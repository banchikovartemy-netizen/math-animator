"""Copy an exact, SHA-verified segment cache hit without pulling the Manim image."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
from rendering.planner import segments_for,fingerprint


def probe(job,segment_id,mode,smoke=False,cache=Path('.cache/math-animator'),outputs=Path('outputs')):
    started=time.monotonic()
    segment=next(s for s in segments_for(job,smoke) if s['id']==segment_id)
    key=fingerprint(job,segment,mode,smoke)
    stage='smoke' if smoke else mode
    source=cache/'segments'/job/stage/segment_id/key
    video=source/'video.mp4';meta=source/'segment.json'
    if not video.is_file() or not meta.is_file():return False
    try:
        report=json.loads(meta.read_text())
        if report['status']!='passed' or report['fingerprint']!=key or report['sha256']!=hashlib.sha256(video.read_bytes()).hexdigest():return False
    except (ValueError,KeyError):return False
    target=outputs/job/stage/'segments'/segment_id;target.mkdir(parents=True,exist_ok=True)
    shutil.copy2(video,target/f'{segment_id}.mp4')
    report.update(cache_hit=True,cache_source='actions-without-container',seconds=time.monotonic()-started)
    (target/'segment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return True

if __name__=='__main__':
    hit=probe(os.environ['JOB'],os.environ['SEGMENT'],os.environ['MODE'],os.environ['SMOKE']=='true')
    with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write('hit='+str(hit).lower()+'\n')
    print('Verified segment cache hit; Manim image pull skipped.' if hit else 'Segment needs rendering.')
