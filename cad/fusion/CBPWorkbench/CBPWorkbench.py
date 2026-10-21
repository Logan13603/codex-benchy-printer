"""Project-local Fusion API runner, explicitly started from Scripts and Add-ins.

This is not a UI automation helper. Fusion's supported CustomEvent API runs
the project's CAD operations on its main thread. No startup setting is changed.
Each queued script must reside inside this project's cad directory. A STOP
file cleanly ends the worker; the saved CAD is never closed or discarded.
"""
from pathlib import Path
import contextlib
import io
import json
import threading
import traceback
import time
import adsk.core
import adsk.fusion

CAD=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parents[5]/'work'/'fusion_jobs'
EVENT='CBP_Project_CAD_Workbench_20261021'
HANDLERS=[]
STOP=threading.Event()
APP=None
LAST=None


def write(name,data):
    WORK.mkdir(parents=True,exist_ok=True)
    p=WORK/name;tmp=p.with_suffix('.tmp')
    tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8');tmp.replace(p)


class JobHandler(adsk.core.CustomEventHandler):
    def notify(self,args):
        global LAST
        if (WORK/'STOP').exists():
            STOP.set();APP.unregisterCustomEvent(EVENT)
            write('runner.json',{'state':'stopped','time':time.time()})
            adsk.terminate();return
        job=json.loads((WORK/'job.json').read_text(encoding='utf-8-sig'))
        if job['id']==LAST:return
        LAST=job['id'];out=io.StringIO();result={'id':LAST,'state':'running'}
        write('result.json',result)
        try:
            path=(CAD/job['script']).resolve()
            if not path.is_relative_to(CAD):raise ValueError('Only project CAD scripts can run')
            namespace={'__name__':'cbp_queued_job','__file__':str(path)}
            with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):
                exec(compile(path.read_text(encoding='utf-8-sig'),str(path),'exec'),namespace)
                namespace['run']('')
            result.update(state='complete',ok=True)
        except Exception:
            result.update(state='failed',ok=False,error=traceback.format_exc())
        result['output']=out.getvalue()
        result['document']=APP.activeDocument.name if APP.activeDocument else None
        result['modified']=APP.activeDocument.isModified if APP.activeDocument else None
        result['finished_at']=time.time();write('result.json',result)


def worker():
    submitted=None
    while not STOP.wait(.5):
        try:
            if (WORK/'STOP').exists():APP.fireCustomEvent(EVENT);return
            p=WORK/'job.json'
            if p.exists():
                job=json.loads(p.read_text(encoding='utf-8-sig'))
                if job['id']!=submitted:
                    submitted=job['id'];APP.fireCustomEvent(EVENT)
        except Exception as e:write('worker-error.json',{'error':str(e)})


def run(context):
    global APP
    APP=adsk.core.Application.get()
    WORK.mkdir(parents=True,exist_ok=True)
    STOP.clear()
    ev=APP.registerCustomEvent(EVENT)
    if not ev:raise RuntimeError('Workbench already running')
    h=JobHandler();ev.add(h);HANDLERS.append(h)
    threading.Thread(target=worker,daemon=True).start()
    write('runner.json',{'state':'ready','cad_root':str(CAD),'fusion_version':APP.version,'time':time.time()})
    adsk.autoTerminate(False)


def stop(context):
    STOP.set()
    if APP:
        try:APP.unregisterCustomEvent(EVENT)
        except Exception:pass
    write('runner.json',{'state':'stopped','time':time.time()})
