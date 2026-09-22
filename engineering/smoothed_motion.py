"""Sample pinned Klipper moves and convolve pinned Kalico smoothers.

Reference calculation only, not firmware simulation or calibrated settings.
Requires numpy. Specify --numpy-dir if using the local bundled dependency path.
The reported geometry error compares time-aligned paths; it is not a surface
Hausdorff distance, dimensional inspection, or a physical motor response.
"""
import argparse,math,json,hashlib,importlib.util,sys
from types import SimpleNamespace
from pathlib import Path
from path_model import ROOT,parse,AF
from validate_klipper_planner import load_planner


def planned_moves(moves,vmax,accel,scv,flow,first=300):
    KMove,Queue,_=load_planner()
    th=SimpleNamespace(max_accel=accel,max_velocity=vmax,
        junction_deviation=scv**2*(math.sqrt(2)-1)/accel,
        mcr_pseudo_accel=accel,extra_axes=[])
    queue=Queue();queue.set_flush_time(1.)
    pos=[0.,0.,0.,0.];done=[]
    for sm in moves:
        end=[pos[k]+sm.u[k]*sm.d for k in range(3)]+[pos[3]+sm.e]
        v=vmax;a=accel
        if not sm.xyz:v=min(40.,sm.feed);a=5000.
        else:
            if sm.e>0:
                v=min(v,flow*sm.d/(sm.e*AF),150.*sm.d/sm.e)
                if sm.z<=.251:v=min(v,first)
            if abs(sm.u[2])>1e-9:
                v=min(v,30/abs(sm.u[2]));a=min(a,1000/abs(sm.u[2]))
        km=KMove(th,pos,end,v);km.limit_speed(v,a)
        km.cbp_deposit=sm.xyz and sm.e>0
        km.cbp_layer_z=sm.z
        queue.add_move(km);pos=end
    done.extend(queue.flush())
    return done


def sample(moves,dt):
    # Break each exact trapezoid into constant-acceleration phases, then
    # evaluate positions analytically at uniform sample times.
    starts=[];ends=[];positions=[];velocities=[];accels=[];deposit=[]
    clock=0.;layers={}
    for m in moves:
        p=np.array(m.start_pos[:2]);u=np.array(m.axes_r[:2])
        total=m.accel_t+m.cruise_t+m.decel_t
        layers[m.cbp_layer_z]=layers.get(m.cbp_layer_z,0)+total
        for t,v,a in [(m.accel_t,m.start_v,m.accel),
                      (m.cruise_t,m.cruise_v,0.),
                      (m.decel_t,m.cruise_v,-m.accel)]:
            if t>1e-12:
                starts.append(clock);ends.append(clock+t);positions.append(p.copy())
                velocities.append(u*v);accels.append(u*a);deposit.append(m.cbp_deposit)
                p+=u*(v*t+.5*a*t*t);clock+=t
    times=np.arange(0,clock,dt)
    ix=np.minimum(np.searchsorted(ends,times,side='right'),len(ends)-1)
    tau=times-np.array(starts)[ix]
    p=np.array(positions)[ix]+np.array(velocities)[ix]*tau[:,None]+.5*np.array(accels)[ix]*tau[:,None]**2
    return times,p,np.array(deposit)[ix],layers,clock


def load_smoothers():
    root=ROOT/'validation/third_party/kalico'
    metadata=json.loads((root/'PROVENANCE.json').read_text())
    for f in metadata['files']:
        assert hashlib.sha256((root/f['file']).read_bytes()).hexdigest()==f['sha256']
    spec=importlib.util.spec_from_file_location('cbp_kalico_shaper_defs',root/'shaper_defs.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module,metadata


def smooth(p,times,dt,init,freq):
    coeff,T=init(freq)
    half=int(math.ceil(T/(2*dt)))
    offsets=np.arange(-half,half+1)*dt
    # Exact polynomial mass in each sampling bin; midpoint sampling poorly
    # resolves the narrow kernels at high frequencies.
    integral=[0.]+[c/(i+1) for i,c in enumerate(coeff)]
    lo=np.maximum(offsets-dt/2,-T/2);hi=np.minimum(offsets+dt/2,T/2)
    kernel=np.where(hi>lo,np.polynomial.polynomial.polyval(hi,integral)-np.polynomial.polynomial.polyval(lo,integral),0.)
    assert abs(kernel.sum()-1)<1e-7,(freq,kernel.sum())
    kernel/=kernel.sum()
    mu=float(np.dot(offsets,kernel))
    # Causal delay is removed for a like-for-like geometry comparison.
    # Runtime latency still exists; the planner must allocate the lookahead.
    # Keep the physical tail beyond the observation window while aligning.
    # Clamping the aligned result at the original end creates a false velocity
    # step and a timestep-dependent acceleration spike.
    shaped=np.column_stack([np.convolve(np.pad(p[:,k],(2*half,2*half),mode='edge'),kernel,mode='valid') for k in (0,1)])
    extended_times=np.arange(-half,len(p)+half)*dt+times[0]
    aligned=np.column_stack([np.interp(times+mu,extended_times,shaped[:,k]) for k in (0,1)])
    vel=np.gradient(aligned,dt,axis=0);a=np.gradient(vel,dt,axis=0)
    return aligned,vel,a,T,mu


def metrics(p,mask,shaped,v,a,radius=.03,axis_mass=.06,count=2):
    error=np.linalg.norm(shaped-p,axis=1)
    # Two independent motors per Cartesian axis is an assumed test fixture,
    # NOT a cable robot or a selected machine. Equal load sharing assumed.
    J=48e-6
    drum_mass=.0075;Jdrum=.5*drum_mass*radius**2
    torque=(axis_mass/count*radius+(J+Jdrum)/radius)*a/1000
    rpm=v/1000/radius*60/(2*math.pi)
    return {'max_xy_error_during_deposition_mm':float(error[mask].max()),
            'p95_xy_error_during_deposition_mm':float(np.percentile(error[mask],95)),
            'max_abs_axis_accel_mm_s2':np.max(np.abs(a),axis=0).tolist(),
            'max_abs_axis_speed_mm_s':np.max(np.abs(v),axis=0).tolist(),
            'max_abs_motor_rpm':np.max(np.abs(rpm),axis=0).tolist(),
            'max_abs_inertial_torque_Nm_per_motor':np.max(np.abs(torque),axis=0).tolist(),
            'time_fraction_above_2Nm_either_axis':float(np.mean(np.any(np.abs(torque)>2.,axis=1)))}


def run(args):
    defs,metadata=load_smoothers()
    source=ROOT/'slicing/cura-4.13.1-simplified/analysis.gcode';path=parse(source)
    planned=planned_moves(path,2400,2000000,500,300)
    t,p,mask,layers,total=sample(planned,args.dt)
    result={'status':'Uncalibrated smoothing sensitivity, not a machine prediction',
            'sample_interval_s':args.dt,'gcode_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'kalico_commit':metadata['commit'],'base_time_s':total,
            'caps':{'velocity_mm_s':2400,'accel_mm_s2':2000000,'scv_mm_s':500,'flow_mm3_s':300,'first_layer_mm_s':300},
            'cooling_floor_lower_bounds':[{'minimum_layer_s':floor,'time_s':sum(max(floor,v) for v in layers.values())} for floor in (.1,.15,.2,.24)],
            'fixture_assumptions':{'kinematics':'independent Cartesian','motors_per_axis':2,'moving_mass_per_axis_kg':.06,
                'rotor_inertia_kg_m2':48e-6,'drum_radius_m':.03,'drum_mass_kg':.0075,'drum_inertia_factor':.5,
                'excluded':'friction, belts, bearings, nonuniform sharing, compliance, motor electrical dynamics and torque-speed margin'},
            'runs':[]}
    for name,init in [('smooth_zv',defs.get_zv_smoother),('smooth_mzv',defs.get_mzv_smoother)]:
        for freq in (50,100,200,400,800):
            sp,v,a,T,mu=smooth(p,t,args.dt,init,freq)
            row={'smoother':name,'frequency_Hz':freq,'duration_ms':T*1000,'centroid_ms':mu*1000,**metrics(p,mask,sp,v,a)}
            result['runs'].append(row)
            print(name,freq,'error',round(row['max_xy_error_during_deposition_mm'],3),'torque',[round(x,3) for x in row['max_abs_inertial_torque_Nm_per_motor']],flush=True)
    # Uniform straight motion should pass with unity gain and centroid shift.
    st=np.arange(0,.1,args.dt);line=np.column_stack([st*100,np.zeros_like(st)])
    sp,_,_,_,_=smooth(line,st,args.dt,defs.get_mzv_smoother,100)
    mid=(st>.02)&(st<.08)
    assert float(np.abs(sp[mid]-line[mid]).max())<1e-7
    out=ROOT/'engineering'/args.output
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('base',total,'cooling',result['cooling_floor_lower_bounds'])


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--numpy-dir');ap.add_argument('--dt',type=float,default=.0001)
    ap.add_argument('--output',default='smoothed-motion-results.json');args=ap.parse_args()
    if args.numpy_dir:sys.path.insert(0,args.numpy_dir)
    import numpy as np
    run(args)
