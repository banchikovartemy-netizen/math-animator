from dataclasses import asdict
import json
from pathlib import Path
import shutil
import subprocess
import pytest
from rendering.planner import ROOT,affected_jobs,segments_for,fingerprint
from rendering.pipeline import assemble,digest,checked_solution


def test_push_selects_only_affected_problem():
    assert affected_jobs(['scenes/integral_graph/extrema.py']) == ['integral_graph']
    assert affected_jobs(['examples/matrix5_solution.py']) == ['matrix5']
    assert affected_jobs(['README.md']) == []
    assert set(affected_jobs(['examples/solutions.py'])) == {'integration','derivative','geometry','matrix','graph'}


def test_smoke_is_representative_sample_not_full_video():
    assert [s['id'] for s in segments_for('integral_graph',True)] == ['sample']
    assert len(segments_for('integral_graph')) == 6
    assert len(segments_for('matrix5')) == 7
    assert segments_for('integration',True)[0]['range'] == [0,4]


def test_conclusion_edit_invalidates_only_its_segment(tmp_path):
    for name in ['src','examples','scenes']:
        shutil.copytree(ROOT/name,tmp_path/name,ignore=shutil.ignore_patterns('__pycache__','*.egg-info'))
    for name in ['Dockerfile','requirements.lock']:shutil.copy(ROOT/name,tmp_path/name)
    parts=segments_for('matrix5',root=tmp_path)
    before={s['id']:fingerprint('matrix5',s,'final',root=tmp_path) for s in parts}
    path=tmp_path/'scenes/matrix5_parts/outro.py'
    path.write_text(path.read_text()+'\n# changed conclusion\n')
    after={s['id']:fingerprint('matrix5',s,'final',root=tmp_path) for s in parts}
    assert [name for name in before if before[name]!=after[name]] == ['outro']
    assert before['row1'] != fingerprint('matrix5',parts[1],'preview',root=tmp_path)


def test_assembly_rejects_stale_or_corrupted_parts(tmp_path,monkeypatch):
    import rendering.pipeline as pipeline
    # Exercise real MP4 concatenation with all six integral segments in order.
    solution=checked_solution('integral_graph')
    original_root=pipeline.ROOT
    output_root=tmp_path/'project';output_root.mkdir()
    monkeypatch.setattr(pipeline,'ROOT',output_root)
    # trusted mathematical loader uses repository ROOT from planner, not this output location
    monkeypatch.setattr(pipeline,'checked_solution',lambda job:solution)
    colors=['red','green','blue','yellow','magenta','cyan']
    metadata=[]
    for s,color in zip(segments_for('integral_graph'),colors):
        d=tmp_path/'parts'/s['id'];d.mkdir(parents=True)
        video=d/f'{s["id"]}.mp4'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f'color=c={color}:s=1280x720:r=24','-t','0.25','-c:v','libx264','-pix_fmt','yuv420p',str(video)],check=True)
        report={'job':'integral_graph','mode':'preview','segment':s['id'],'status':'passed',
                'fingerprint':fingerprint('integral_graph',s,'preview'),'sha256':digest(video),'solution':solution}
        path=d/'segment.json';path.write_text(json.dumps(report));metadata.append(path)
    target=assemble('integral_graph','preview',tmp_path/'parts')
    report=json.loads((target.parent/'report.json').read_text())
    assert report['video']['decoded'] and abs(report['video']['duration']-1.5)<.01
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(target),'-vf','fps=4,scale=1:1','-pix_fmt','rgb24','-f','rawvideo','-'])
    pixels=[tuple(raw[i:i+3]) for i in range(0,len(raw),3)]
    assert len(pixels)==6
    assert pixels[0][0]>200 and pixels[0][1]<30  # first red
    assert pixels[2][2]>200 and pixels[2][0]<30  # third blue
    assert pixels[-1][1]>200 and pixels[-1][2]>200  # last cyan
    modified=json.loads(metadata[0].read_text());modified['fingerprint']='stale';metadata[0].write_text(json.dumps(modified))
    with pytest.raises(ValueError,match='Stale'):assemble('integral_graph','preview',tmp_path/'parts')
    modified['fingerprint']=fingerprint('integral_graph',segments_for('integral_graph')[0],'preview')
    modified['sha256']='invalid';metadata[0].write_text(json.dumps(modified))
    with pytest.raises(ValueError,match='content changed'):assemble('integral_graph','preview',tmp_path/'parts')
