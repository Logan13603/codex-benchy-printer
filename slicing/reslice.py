"""Reproduce analysis slices with installed OrcaSlicer 2.3.2. Never a print profile."""
import json, subprocess, zipfile, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'slicing'
ORCA = Path(r'C:\Program Files\OrcaSlicer\orca-slicer.exe')

def run():
    # Existing flattened profiles are the versioned inputs, avoiding mutable inheritance.
    records = []
    for width in (0.4, 0.45, 0.5):
        name = f'width-{width:.2f}'
        out = S / 'variants' / name
        out.mkdir(parents=True, exist_ok=True)
        profile = json.loads((S/'process.json').read_text())
        for k in list(profile):
            if k == 'line_width' or k.endswith('_line_width'):
                profile[k] = str(width)
        profile['detect_thin_wall'] = '1'
        (out/'process.json').write_text(json.dumps(profile, indent=2)+'\n')
        machine = json.loads((S/'machine.json').read_text())
        machine['nozzle_diameter'] = [str(min(width, 0.5))]
        (out/'machine.json').write_text(json.dumps(machine, indent=2)+'\n')
        cmd = [str(ORCA), '--debug', '2', '--slice', '0', '--load-settings',
               f'{out/"machine.json"};{out/"process.json"}', '--load-filaments',
               str(S/'filament.json'), '--outputdir', str(out), '--export-3mf',
               'analysis.3mf', str(S/'models/3DBenchy.stl')]
        p = subprocess.run(cmd, capture_output=True, text=True)
        (out/'slice-log.txt').write_text(p.stdout+p.stderr)
        if p.returncode: raise RuntimeError((name,p.returncode,p.stderr))
        with zipfile.ZipFile(out/'analysis.3mf') as z:
            data = z.read('Metadata/plate_1.gcode')
        (out/'analysis.gcode').write_bytes(data)
        duplicate = out/'plate_1.gcode'
        if duplicate.exists() and duplicate.read_bytes() == data: duplicate.unlink()
        records.append({'variant':name,'sha256':hashlib.sha256(data).hexdigest(),
                        'nozzle_mm':min(width,0.5),'nominal_width_mm':width,
                        'thin_wall_detection':True,'returncode':p.returncode})
        print(name, 'completed', flush=True)
    (S/'variants/manifest.json').write_text(json.dumps(records,indent=2)+'\n')

if __name__ == '__main__': run()
