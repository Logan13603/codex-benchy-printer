"""Re-check the most promising checkpoint-008 slice under motion smoothing.
This is the prior hypothetical four-motor Cartesian fixture, not a real design.
"""
import argparse,json,sys,hashlib
from path_model import ROOT,parse
from extrusion_dynamics import plan
import smoothed_motion as sm
import spatial_study as sp


def run(args):
 source=ROOT/'slicing/cura-travel-study/concentric-skin/analysis.gcode';raw=parse(source)
 planned=plan(raw,1.,0.);t,p,mask,layers,total=sm.sample(planned,args.dt)
 groups=sp.strokes(planned,raw);defs,meta=sm.load_smoothers()
 result={'status':'Unvalidated geometry/drive screen for new concentric-skin candidate',
         'gcode_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'time_s':total,'dt_s':args.dt,
         'fixture':'Two Nanotec SCB5618L4204-B motors per independent Cartesian axis; 60g axis load; 30mm-radius 7.5g drum. No transmission elasticity or electrical dynamics.',
         'runs':[]}
 for freq in (200,400,800):
  shaped,v,a,T,mu=sm.smooth(p,t,args.dt,defs.get_zv_smoother,freq)
  spatial,_=sp.spatial_metrics(groups,t,shaped,.04)
  result['runs'].append({'frequency_Hz':freq,'smoother_duration_ms':T*1000,
                        'dynamics':sm.metrics(p,mask,shaped,v,a),'spatial':spatial})
  out=spatial['by_role']['WALL-OUTER'];torque=result['runs'][-1]['dynamics']['max_abs_inertial_torque_Nm_per_motor']
  print(freq,'outer bounds',out['ref_to_smoothed_lower_mm'],out['ref_to_smoothed_upper_mm'],'torque',torque,flush=True)
 (ROOT/'engineering/concentric-motion-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--numpy-dir');ap.add_argument('--dt',type=float,default=.000025);args=ap.parse_args()
 if args.numpy_dir:sys.path.insert(0,args.numpy_dir)
 import numpy as np
 from scipy.spatial import cKDTree
 sm.np=np;sp.np=np;sp.cKDTree=cKDTree
 run(args)
