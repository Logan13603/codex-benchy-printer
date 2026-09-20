"""One deliberately optimistic sensitivity trial; width audit still required."""
import json,subprocess,zipfile
from pathlib import Path
from reslice import S, ORCA
out=S/'variants/combined-no-retraction';out.mkdir(parents=True,exist_ok=True)
p=json.loads((S/'variants/width-0.50/process.json').read_text())
p.update(infill_combination='1',infill_combination_max_layer_height='0.5',
         thick_internal_bridges='0',thick_bridges='0',resolution='0.025')
m=json.loads((S/'machine.json').read_text())
m.update(retraction_length=['0'],wipe=['0'],retract_when_changing_layer=['0'])
for n,d in [('process',p),('machine',m)]: (out/(n+'.json')).write_text(json.dumps(d,indent=2)+'\n')
cmd=[str(ORCA),'--debug','2','--slice','0','--load-settings',f'{out/"machine.json"};{out/"process.json"}',
     '--load-filaments',str(S/'filament.json'),'--outputdir',str(out),'--export-3mf','analysis.3mf',str(S/'models/3DBenchy.stl')]
r=subprocess.run(cmd,capture_output=True,text=True)
(out/'slice-log.txt').write_text(r.stdout+r.stderr)
if r.returncode: raise RuntimeError(r.stderr)
with zipfile.ZipFile(out/'analysis.3mf') as z:data=z.read('Metadata/plate_1.gcode')
(out/'analysis.gcode').write_bytes(data)
if (out/'plate_1.gcode').read_bytes()==data:(out/'plate_1.gcode').unlink()
print('Optimistic trial complete; no retraction is an unvalidated extrusion assumption.')
