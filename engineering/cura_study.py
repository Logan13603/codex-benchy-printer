"""Reproduce the controlled Cura simplification comparison and extreme-cap sweep."""
import json,hashlib
from path_model import ROOT,parse,summarize,duration
from validate_klipper_planner import klipper_duration

def run():
    result={}
    for name in ['cura-4.13.1-no-gap','cura-4.13.1-simplified']:
        path=ROOT/'slicing'/name/'analysis.gcode';moves=parse(path)
        result[name]={'gcode_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
          'summary':summarize(moves),'optimistic':duration(moves,200,2000,100000,100),
          'planner':klipper_duration(moves)}
        if name.endswith('simplified'):
            result[name]['sensitivity']=[duration(moves,q,3000,a,100) for q in [200,400] for a in [100000,200000,500000,1000000]]
        print(name,result[name]['optimistic']['seconds'],flush=True)
    (ROOT/'engineering/cura-path-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':run()
