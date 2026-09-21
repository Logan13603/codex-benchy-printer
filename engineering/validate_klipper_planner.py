"""Cross-check the numerical study against unmodified, pinned Klipper planner classes.

No printer, MCU or hardware is contacted. Only Move/LookAheadQueue are loaded
from the archived GPLv3 upstream source. Artificial speed/flow/axis caps mirror
the screening model. This tests planner arithmetic, not full firmware behavior.
"""
import ast,math,json,hashlib
from types import SimpleNamespace
from path_model import ROOT,parse,duration,Move as StudyMove,AF

def load_planner():
    folder=ROOT/'validation/third_party/klipper'
    meta=json.loads((folder/'PROVENANCE.json').read_text(encoding='utf-8'))
    source=(folder/'toolhead.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==meta['files'][0]['sha256']
    parsed=ast.parse(source)
    selected=[n for n in parsed.body if isinstance(n,ast.ClassDef) and n.name in ('Move','LookAheadQueue')]
    namespace={'math':math,'LOOKAHEAD_FLUSH_TIME':.150}
    exec(compile(ast.Module(body=selected,type_ignores=[]),'pinned_klipper_planner','exec'),namespace)
    return namespace['Move'],namespace['LookAheadQueue'],meta

def klipper_duration(moves,flow=200,vmax=2000,accel=100000,scv=100,mcr=0.,finite_queue=False):
    KMove,Queue,meta=load_planner()
    toolhead=SimpleNamespace(max_accel=accel,max_velocity=vmax,
            junction_deviation=scv**2*(math.sqrt(2)-1)/accel,
            mcr_pseudo_accel=accel*(1-mcr),extra_axes=[])
    queue=Queue();queue.set_flush_time(1.)
    pos=[0.,0.,0.,0.];done=[];roles=[]
    for sm in moves:
        end=[pos[k]+sm.u[k]*sm.d for k in range(3)]+[pos[3]+sm.e]
        velocity=vmax; a=accel
        if not sm.xyz: velocity=min(40.,sm.feed);a=5000.
        else:
            if sm.e>0:velocity=min(velocity,flow*sm.d/(sm.e*AF),150.*sm.d/sm.e)
            if abs(sm.u[2])>1e-9:
                velocity=min(velocity,30/abs(sm.u[2]));a=min(a,1000/abs(sm.u[2]))
        km=KMove(toolhead,pos,end,velocity);km.limit_speed(velocity,a)
        km.cbp_role=sm.role if sm.xyz and sm.e>0 else ('travel' if sm.xyz else 'pure-E')
        flush=queue.add_move(km)
        if finite_queue and flush:done.extend(queue.flush(lazy=True))
        pos=end
    done.extend(queue.flush())
    times=[m.accel_t+m.cruise_t+m.decel_t for m in done]
    by_role={}
    for m,t in zip(done,times):by_role[m.cbp_role]=by_role.get(m.cbp_role,0.)+t
    return {'seconds':sum(times),'move_count':len(done),'by_role_seconds':by_role,
            'minimum_cruise_ratio':mcr,'finite_queue':finite_queue,'upstream_commit':meta['commit']}

def run():
    cases=[('triangle',[StudyMove(10,(1.,0.,0.),0,1,1000,'test',.5)],1000,100,20),
           ('trapezoid',[StudyMove(100,(1.,0.,0.),0,1,1000,'test',.5)],10,100,20),
           ('reversal',[StudyMove(10,(1.,0.,0.),0,1,1000,'test',.5),StudyMove(10,(-1.,0.,0.),0,1,1000,'test',.5)],1000,100,20)]
    result={'analytical_tests':[],'trials':{}}
    for name,moves,v,a,sc in cases:
        old=duration(moves,200,v,a,sc)['seconds'];actual=klipper_duration(moves,200,v,a,sc)['seconds']
        assert abs(actual-old)<1e-7,(name,actual,old)
        result['analytical_tests'].append({'name':name,'study_seconds':old,'klipper_seconds':actual,'passed':True})
    paths=[ROOT/'slicing/variants'/name/'analysis.gcode' for name in ['combined-no-retraction','width-0.50']]
    paths.append(ROOT/'slicing/cura-4.13.1-no-gap/analysis.gcode')
    for path in paths:
        name=path.parent.name; moves=parse(path)
        old=duration(moves,200,2000,100000,100)['seconds']
        variants=[klipper_duration(moves,mcr=mcr,finite_queue=finite) for mcr,finite in [(0,False),(0,True),(.5,True)]]
        result['trials'][name]={'gcode_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                               'study_seconds':old,'planner_runs':variants,
                               'difference_s_unlimited_queue':variants[0]['seconds']-old}
        print(name,json.dumps(result['trials'][name]),flush=True)
    (ROOT/'validation/klipper-planner-comparison.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':run()
