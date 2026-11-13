"""Select affected jobs and their independent scene segments."""
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]

def safe_name(value):
    if not re.fullmatch(r'[a-z][a-z0-9_]{0,63}',value):
        raise ValueError('Invalid artifact name')
    return value

def load_manifest(job,root=ROOT):
    safe_name(job)
    data=json.loads((root/'examples'/f'{job}.json').read_text())
    for segment in data.get('segments',[]) + data.get('preview_segments',[]):
        safe_name(segment['id'])
    return data

def segments_for(job,smoke=False,root=ROOT):
    m=load_manifest(job,root)
    if smoke and m.get('preview_segments'):return m['preview_segments']
    if m.get('segments'):return m['segments'][:1] if smoke else m['segments']
    return [dict(id='main',scene=m['scene'],**{'class':m['class']},dependencies=m.get('dependencies',[]),**({'range':[0,4]} if smoke else {}))]

def dependencies(job,segment,root=ROOT):
    m=load_manifest(job,root)
    paths=[segment['scene'],m['solution'],*segment.get('dependencies',[]),*m.get('dependencies',[])]
    for path in paths:
        resolved=(root/path).resolve()
        if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
            raise ValueError(f'Invalid dependency: {path}')
    return sorted(set(paths))

def fingerprint(job,segment,mode,smoke=False,root=ROOT):
    h=hashlib.sha256(json.dumps([job,segment,mode,smoke,'segment-cache-v1'],sort_keys=True).encode())
    paths=dependencies(job,segment,root)
    paths += ['Dockerfile','requirements.lock']
    paths += [str(p.relative_to(root)) for directory in ['src/animation','src/rendering'] for p in (root/directory).rglob('*.py')]
    for name in sorted(set(paths)):
        h.update(name.encode());h.update((root/name).read_bytes())
    return h.hexdigest()

def affected_jobs(changed,root=ROOT):
    jobs=sorted(p.stem for p in (root/'examples').glob('*.json'))
    if any(p.startswith(('src/','tests/')) or p in {'Dockerfile','requirements.lock','pyproject.toml'} for p in changed):return jobs
    selected=[]
    for job in jobs:
        m=load_manifest(job,root)
        deps={f'examples/{job}.json',m['solution'],*m.get('dependencies',[])}
        for segment in segments_for(job,root=root)+m.get('preview_segments',[]):
            deps.update(dependencies(job,segment,root))
        if deps.intersection(changed):selected.append(job)
    return selected

def runtime_key(root=ROOT):
    return hashlib.sha256((root/'Dockerfile').read_bytes()+(root/'requirements.lock').read_bytes()).hexdigest()[:16]
