"""Pinned Klipper extruder-junction and pressure-advance screening.
No firmware deployment or physical process validation. Units mm, seconds.
"""
import ast, json, math, hashlib, logging, argparse, sys
from types import SimpleNamespace
from path_model import ROOT, parse, AF, Move as StudyMove
from validate_klipper_planner import load_planner


def extruder(instant=1.):
    folder=ROOT/'validation/third_party/klipper'
    meta=json.loads((folder/'PROVENANCE.json').read_text(encoding='utf-8'))
    entry=next(x for x in meta['files'] if x.get('file')=='extruder.py')
    code=(folder/'extruder.py').read_bytes()
    assert hashlib.sha256(code).hexdigest()==entry['sha256']
    tree=ast.parse(code); cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='PrinterExtruder')
    ns={'math':math,'logging':logging}
    exec(compile(ast.Module(body=[cls],type_ignores=[]),'pinned_klipper_extruder','exec'),ns)
    e=ns['PrinterExtruder'].__new__(ns['PrinterExtruder'])
    e.heater=SimpleNamespace(can_extrude=True);e.printer=SimpleNamespace(command_error=ValueError)
    e.filament_area=AF;e.nozzle_diameter=.5;e.max_extrude_ratio=1./AF
    e.max_e_velocity=150.;e.max_e_accel=5000.;e.max_e_dist=50.;e.instant_corner_v=instant
    return e


def plan(moves, instant=1., mcr=0., finite=True, flow=300., vmax=2400., accel=2000000., scv=500., first=300.):
    KMove,Queue,_=load_planner();ext=extruder(instant) if instant is not None else None
    th=SimpleNamespace(max_accel=accel,max_velocity=vmax,junction_deviation=scv**2*(math.sqrt(2)-1)/accel,
                       mcr_pseudo_accel=accel*(1-mcr),extra_axes=[] if ext is None else [ext])
    queue=Queue();queue.set_flush_time(1.);pos=[0.,0.,0.,0.];done=[]
    for sm in moves:
        end=[pos[k]+sm.u[k]*sm.d for k in range(3)]+[pos[3]+sm.e]
        v=vmax;a=accel
        if not sm.xyz:v=min(40.,sm.feed);a=5000.
        else:
            if sm.e>0:
                v=min(v,flow*sm.d/(sm.e*AF),150.*sm.d/sm.e)
                if sm.z<=.251:v=min(v,first)
            if abs(sm.u[2])>1e-9:v=min(v,30/abs(sm.u[2]));a=min(a,1000/abs(sm.u[2]))
        km=KMove(th,pos,end,v);km.limit_speed(v,a)
        if ext is not None and km.axes_d[3]:ext.check_move(km,3)
        km.cbp_deposit=sm.xyz and sm.e>0;km.cbp_layer_z=sm.z;km.cbp_role=sm.role if km.cbp_deposit else 'travel'
        flush=queue.add_move(km)
        if finite and flush:done.extend(queue.flush(lazy=True))
        pos=end
    done.extend(queue.flush())
    return done


def summary(planned):
    layers={};roles={};seconds=0.;deposition=0.
    for m in planned:
        t=m.accel_t+m.cruise_t+m.decel_t;seconds+=t
        layers[m.cbp_layer_z]=layers.get(m.cbp_layer_z,0.)+t
        roles[m.cbp_role]=roles.get(m.cbp_role,0.)+t
        if m.cbp_deposit:deposition+=t
    return {'seconds':seconds,'deposition_seconds':deposition,'by_role_seconds':roles,
            'cooling_floor_s':[{'floor_s':f,'seconds':sum(max(t,f) for t in layers.values())} for f in (.1,.15,.2,.24)]}


def phases(planned):
    starts=[];ends=[];ep=[];ev=[];ea=[];roles=[];dep=[];clock=0.
    for m in planned:
        e=m.start_pos[3];r=m.axes_r[3]
        for t,v,a in [(m.accel_t,m.start_v,m.accel),(m.cruise_t,m.cruise_v,0.),(m.decel_t,m.cruise_v,-m.accel)]:
            if t>1e-12:
                starts.append(clock);ends.append(clock+t);ep.append(e);ev.append(r*v);ea.append(r*a)
                roles.append(m.cbp_role);dep.append(m.cbp_deposit)
                e+=r*(v*t+.5*a*t*t);clock+=t
    return [np.array(x) for x in (starts,ends,ep,ev,ea,roles,dep)]


def triangular_kernel(smooth_time,dt):
    half=smooth_time/2;n=math.ceil(half/dt);offset=np.arange(-n,n+1)*dt
    def primitive(x):
        # Integral from zero, of (half-|x|)/half^2 on supported interval.
        x=np.clip(x,-half,half);return (half*x-.5*x*np.abs(x))/half**2
    k=primitive(offset+dt/2)-primitive(offset-dt/2)
    assert abs(k.sum()-1)<1e-12
    return k


def convolve(values,k):
    n=(len(k)-1)//2
    return np.convolve(np.pad(values,(n,n),mode='edge'),k,mode='valid')


def pressure_screen(planned,dt,smooth_times=(.04,.01,.004,.001),pa_values=(.01,.04)):
    starts,ends,ep,ev,ea,roles,dep=phases(planned);total=ends[-1]
    # Padding includes full smoothing tail. No material is silently truncated.
    t=np.arange(-.05,total+.05,dt);ix=np.clip(np.searchsorted(ends,t,side='right'),0,len(ends)-1)
    tau=t-starts[ix];e=ep[ix]+ev[ix]*tau+.5*ea[ix]*tau*tau;v=ev[ix]+ea[ix]*tau
    e[t<0]=ep[0];e[t>total]=planned[-1].end_pos[3];v[(t<0)|(t>total)]=0.
    deposit=dep[ix]&(t>=0)&(t<=total);q=v*AF
    rows=[]
    for st in smooth_times:
        k=triangular_kernel(st,dt)
        # For linear pressure plant tau*q_out_dot+q_out=q_feed, and perfectly
        # matched PA=tau, the ideal output is triangular-filtered nominal Q.
        # This follows algebraically; it is NOT a model fitted to this hotend.
        qout=convolve(q,k);volume=q.sum()*dt
        output_total=qout.sum()*dt;travel_output=qout[~deposit].sum()*dt
        by_role={}
        for role in np.unique(roles):
            mask=(roles[ix]==role)&deposit
            if not mask.any():continue
            nom=q[mask].sum()*dt;out=qout[mask].sum()*dt
            by_role[str(role)]={'nominal_volume_mm3':float(nom),'matched_model_output_mm3':float(out),'ratio':float(out/nom)}
        for pa in pa_values:
            raw=e+pa*v*dep[ix]
            position=convolve(raw,k);velocity=np.gradient(position,dt);acceleration=np.gradient(velocity,dt)
            rows.append({'pa_s':pa,'smooth_time_s':st,'time_step_s':dt,
                'input_total_volume_mm3':float(volume),'output_total_volume_mm3':float(output_total),
                'matched_model_output_during_travel_fraction':float(travel_output/output_total),
                'by_role':by_role,'peak_abs_feed_mm_s':float(np.max(np.abs(velocity))),
                'min_feed_mm_s':float(velocity.min()),'max_feed_mm_s':float(velocity.max()),
                'peak_abs_feed_accel_mm_s2':float(np.max(np.abs(acceleration))),
                'four_equal_inputs_peak_abs_feed_mm_s_each':float(np.max(np.abs(velocity))/4),
                'four_equal_inputs_peak_abs_feed_accel_mm_s2_each':float(np.max(np.abs(acceleration))/4)})
    return rows


def tests():
    KMove,_,_=load_planner();e=extruder(1.)
    th=SimpleNamespace(max_accel=1e5,max_velocity=2000,junction_deviation=1.,mcr_pseudo_accel=1e5,extra_axes=[e])
    m1=KMove(th,[0,0,0,0],[10,0,0,.5],1000)
    m2=KMove(th,[10,0,0,.5],[20,0,0,1.5],1000)
    assert abs(e.calc_junction(m1,m2,3)-400)<1e-9
    pure=KMove(th,[0,0,0,0],[0,0,0,10],1000);e.check_move(pure,3)
    assert pure.max_cruise_v2==150**2 and pure.accel==5000
    over=KMove(th,[0,0,0,0],[10,0,0,10],1000)
    try:e.check_move(over,3)
    except ValueError:pass
    else:raise AssertionError('Overextrusion not rejected')
    dt=1e-5;t=np.arange(0,.1,dt);k=triangular_kernel(.01,dt);v=2*t+1
    assert np.max(np.abs(convolve(v,k)[1000:-1000]-v[1000:-1000]))<1e-10
    return ['Unmodified extrusion junction gives 20 mm/s for ratio jump .05 at E-corner 1.',
            'Extrude-only speed/acceleration limits applied; overextrusion rejected.',
            'Triangular kernel has unit area and preserves an interior linear ramp.']


def run(args):
    source=ROOT/args.source;moves=parse(source)
    result={'status':'Pinned extrusion checks and uncalibrated linear-pressure sensitivity, not printer validation',
            'gcode_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'tests':tests(),
            'caps':{'v_mm_s':2400,'a_mm_s2':2000000,'scv_mm_s':500,'q_mm3_s':300,'first_mm_s':300},'timing':[]}
    for instant in (None,1.,5.,10.,25.,100.):
        for mcr in (0.,.5):
            planned=plan(moves,instant,mcr)
            row={'extruder_instantaneous_corner_velocity_mm_s':instant,'mcr':mcr,'finite_queue':True,**summary(planned)}
            result['timing'].append(row);print('junction',instant,'mcr',mcr,'s',row['seconds'],flush=True)
    selected=plan(moves,1.,0.)
    result['pressure_case']='Default E instantaneous corner=1, MCR0; PA values are sensitivities, not settings.'
    result['pressure_advance']=pressure_screen(selected,args.dt)
    # Numerical integration agrees with exact commanded E to within sampling error.
    exact=sum(m.e for m in moves if m.e>0)*AF
    for r in result['pressure_advance']:
        assert abs(r['input_total_volume_mm3']-exact)/exact<2e-4
        assert abs(r['output_total_volume_mm3']-r['input_total_volume_mm3'])<1e-7
        print('PA',r['pa_s'],'smooth',r['smooth_time_s'],'Emax',r['peak_abs_feed_mm_s'],
              'EAmax',r['peak_abs_feed_accel_mm_s2'],'travel_fraction',r['matched_model_output_during_travel_fraction'],flush=True)
    (ROOT/'engineering'/args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--numpy-dir');ap.add_argument('--dt',type=float,default=.000025)
    ap.add_argument('--output',default='extrusion-dynamics-results.json')
    ap.add_argument('--source',default='slicing/cura-4.13.1-simplified/analysis.gcode');args=ap.parse_args()
    if args.numpy_dir:sys.path.insert(0,args.numpy_dir)
    import numpy as np
    run(args)
