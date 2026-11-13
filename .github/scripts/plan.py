import json
import os
import subprocess
from rendering.planner import ROOT,affected_jobs,segments_for,fingerprint,runtime_key,load_manifest
requested=os.environ.get('REQUESTED_JOB','changed')
mode=os.environ.get('MODE','preview')
smoke=os.environ.get('SMOKE','true')=='true'
if smoke:mode='preview'
if requested=='all':jobs=sorted(p.stem for p in (ROOT/'examples').glob('*.json'))
elif requested=='changed':
    before=os.environ.get('BEFORE','')
    if not before or set(before)=={'0'}:before='HEAD^'
    changed=subprocess.check_output(['git','diff','--name-only',before,'HEAD'],text=True).splitlines()
    jobs=affected_jobs(changed)
else:
    load_manifest(requested);jobs=[requested]
items=[dict(job=job,segment=s['id'],mode=mode,smoke=smoke,key=fingerprint(job,s,mode,smoke)[:24],runtime=runtime_key()) for job in jobs for s in segments_for(job,smoke)]
with open(os.environ['GITHUB_OUTPUT'],'a') as f:
    f.write('matrix='+json.dumps({'include':items})+'\n')
    f.write('jobs='+json.dumps(jobs)+'\n')
    f.write('count='+str(len(items))+'\n')
    f.write('mode='+mode+'\n')
    f.write('smoke='+str(smoke).lower()+'\n')
print(json.dumps({'jobs':jobs,'segments':len(items),'mode':mode,'smoke':smoke}))
