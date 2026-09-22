"""Bridge-pattern correction trial with unchanged shell density and flow.
Not a physically validated bridge speed profile.
Analysis only. Wall count, shell layers, original mesh, scale, widths and infill
percentage remain fixed. Direct travel needs physical string/collision checks.
"""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
from path_model import ROOT,parse,summarize
from audit_cura import audit
from extrusion_dynamics import plan,summary


def run(args):
 base=ROOT/'slicing/cura-4.13.1-simplified'
 settings=json.loads((base/'settings.json').read_text(encoding='utf-8'))
 meta=json.loads((base/'provenance.json').read_text(encoding='utf-8'))
 assert hashlib.sha256(args.engine.read_bytes()).hexdigest()==meta['binary_sha256']
 defs=ROOT/'slicing/third_party/cura-4.13.1'
 for f,sha in meta['definition_sha256'].items():assert hashlib.sha256((defs/f).read_bytes()).hexdigest()==sha
 common={'retraction_combing':'off','optimize_wall_printing_order':True}
 cases=[('concentric-bridges',{'top_bottom_pattern':'concentric','infill_angles':'[0]',
        'bridge_settings_enabled':True,'bridge_wall_coast':0,'bridge_wall_material_flow':100,
        'bridge_skin_material_flow':100,'bridge_skin_material_flow_2':100,'bridge_skin_material_flow_3':100,
        'bridge_skin_density':100,'bridge_skin_density_2':100,'bridge_skin_density_3':100,
        'bridge_wall_speed':1500,'bridge_skin_speed':1500,'bridge_skin_speed_2':1500,'bridge_skin_speed_3':1500})]
 result={'status':'Unvalidated slicer optimizations; not ready to print','trials':[]}
 for name,change in cases:
  folder=ROOT/'slicing/cura-travel-study'/name;folder.mkdir(parents=True,exist_ok=False)
  change={**common,**change};trial={**settings,**change};flags=[]
  for k,v in trial.items():flags+=['-s',k+'='+(str(v).lower() if isinstance(v,bool) else str(v))]
  output=folder/'analysis.gcode'
  cmd=[str(args.engine.resolve()),'slice','-j',str(defs/'fdmprinter.def.json')]+flags
  cmd+=['-e0','-j',str(defs/'fdmextruder.def.json')]+flags
  cmd+=['-l',str(ROOT/'slicing/models/3DBenchy.stl'),'-o',str(output)]
  env=os.environ.copy();env['CURA_ENGINE_SEARCH_PATH']=str(defs)
  p=subprocess.run(cmd,capture_output=True,text=True,env=env)
  (folder/'slice-log.txt').write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0,name
  (folder/'settings.json').write_text(json.dumps(trial,indent=2)+'\n',encoding='utf-8')
  (folder/'provenance.json').write_text(json.dumps({**meta,'parent_trial':'cura-4.13.1-simplified',
      'changed_settings':change,'gcode_sha256':hashlib.sha256(output.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
  moves=parse(output);row={'name':name,'changed_settings':change,'summary':summarize(moves),'audit':audit(output),'timing':[]}
  for q,a,scv,icv in [(300,2000000,500,1),(300,2000000,500,10),(300,1000000,100,1),(200,2000000,500,1),(150,500000,50,1)]:
   pm=plan(moves,instant=icv,flow=q,accel=a,scv=scv)
   row['timing'].append({'q_mm3_s':q,'a_mm_s2':a,'scv_mm_s':scv,'e_corner_mm_s':icv,**summary(pm)})
  result['trials'].append(row)
  print(name,'volume',row['summary']['volume_mm3'],'travel',row['summary']['travel_path_mm'],
        'violations',len(row['audit']['certain_width_violations']),'times',[round(x['seconds'],4) for x in row['timing']],flush=True)
 (ROOT/'engineering/bridge-trial-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--engine',required=True,type=Path);run(ap.parse_args())
