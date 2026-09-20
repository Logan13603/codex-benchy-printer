"""Read-only summary of relative-E Orca toolpaths; not a print-time simulator."""
from pathlib import Path
import re, math, json, hashlib
root=Path(__file__).resolve().parents[1]
p=root/'slicing/analysis.gcode'
text=p.read_text()
assert 'use_relative_e_distances = 1' in text
pos=dict(X=0.,Y=0.,Z=0.); e_print=0.; length=0.; travel=0.; moves=0
for line in text.splitlines():
    code=line.split(';')[0].strip()
    if not re.match(r'^G[01]\s',code): continue
    fields={k:float(v) for k,v in re.findall(r'([XYZEF])(-?\d*\.?\d+)',code)}
    nxt={k:fields.get(k,pos[k]) for k in pos}
    d=math.dist(list(pos.values()),list(nxt.values()))
    if d>0 and fields.get('E',0)>0:
        e_print+=fields['E']; length+=d; moves+=1
    else: travel+=d
    pos=nxt
volume=e_print*math.pi*1.75**2/4
result={'status':'preliminary toolpath arithmetic; settings audit and dynamic simulation pending',
 'gcode_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'deposition_filament_mm':e_print,
 'deposition_volume_mm3':volume,'PLA_mass_g_at_1_24':volume*0.00124,
 'extruding_path_mm':length,'nonextruding_path_mm':travel,'extruding_segments':moves,
 'minimum_mean_flow_for_55s_mm3_s':volume/55,'minimum_mean_flow_for_60s_mm3_s':volume/60,
 'ideal_flow_only_time_at_75mm3_s':volume/75,
 'limitations':['Excludes stationary priming/unretraction from deposition volume.',
 'Flow-only time assumes continuous deposition, infinite acceleration and zero travel time.',
 '75 mm3/s is a hypothetical cap, not validated capability with a 0.5-mm nozzle.',
 'Not proof of global impossibility or a final feasibility decision.']}
(root/'engineering/preliminary_toolpath_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
