"""Reproduce the independent Cura 4.13.1 study. Analysis G-code: DO NOT PRINT.

Supply the archived release's extracted CuraEngine.exe with --engine.
No downloading, installation or printer connection is performed by this script.
"""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--engine',type=Path,required=True)
    ap.add_argument('--trial',choices=['cura-4.13.1','cura-4.13.1-no-gap','cura-4.13.1-simplified'],default='cura-4.13.1-no-gap')
    ap.add_argument('--out',type=Path,required=True,help='Fresh output directory, outside archived trial')
    a=ap.parse_args();trial=ROOT/'slicing'/a.trial;meta=json.loads((trial/'provenance.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(a.engine.read_bytes()).hexdigest()==meta['binary_sha256'],'Wrong engine binary'
    defs=ROOT/'slicing/third_party/cura-4.13.1'
    for name,sha in meta['definition_sha256'].items():assert hashlib.sha256((defs/name).read_bytes()).hexdigest()==sha
    a.out.mkdir(parents=True,exist_ok=False)
    settings=json.loads((trial/'settings.json').read_text(encoding='utf-8'))
    flags=[]
    for k,v in settings.items():flags+=['-s',k+'='+(str(v).lower() if isinstance(v,bool) else str(v))]
    cmd=[str(a.engine.resolve()),'slice','-j',str(defs/'fdmprinter.def.json')]+flags
    cmd+=['-e0','-j',str(defs/'fdmextruder.def.json')]+flags
    cmd+=['-l',str(ROOT/'slicing/models/3DBenchy.stl'),'-o',str(a.out/'analysis.gcode')]
    env=os.environ.copy();env['CURA_ENGINE_SEARCH_PATH']=str(defs)
    p=subprocess.run(cmd,capture_output=True,text=True,env=env)
    (a.out/'slice-log.txt').write_text(p.stdout+p.stderr,encoding='utf-8')
    if p.returncode:raise RuntimeError('Slicer failed; see log')
    print('Analysis slice completed. Header time, bounds and filament totals are placeholders; use the independent audit.')

if __name__=='__main__':main()
