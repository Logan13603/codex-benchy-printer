"""Re-slice fixed-width wall candidates, retaining two walls and solid layers.

Analysis G-code only. Reproducible pinned Cura binary; no printer connection.
The result does not certify local feature coverage or physical extrusion width.
"""
import argparse, json, hashlib, subprocess, os
from pathlib import Path
from path_model import ROOT, parse, summarize, duration
from audit_cura import audit


def run(args):
    base = ROOT/'slicing/cura-4.13.1-simplified'
    settings = json.loads((base/'settings.json').read_text())
    meta = json.loads((base/'provenance.json').read_text())
    assert hashlib.sha256(args.engine.read_bytes()).hexdigest() == meta['binary_sha256']
    defs = ROOT/'slicing/third_party/cura-4.13.1'
    for f, sha in meta['definition_sha256'].items():
        assert hashlib.sha256((defs/f).read_bytes()).hexdigest() == sha
    result = {'status': 'Slicer optimization study, not a print-ready profile', 'trials': []}
    for name, outer, inner in [('walls-040', .4, .4), ('walls-045', .45, .45), ('outer-040-inner-050', .4, .5)]:
        folder = ROOT/'slicing/cura-width-study'/name
        folder.mkdir(parents=True, exist_ok=False)
        changes = {'wall_line_width': (outer+inner)/2, 'wall_line_width_0': outer,
                   'wall_line_width_x': inner, 'wall_thickness': outer+inner}
        trial = {**settings, **changes}
        flags = []
        for k, v in trial.items(): flags += ['-s', k+'='+(str(v).lower() if isinstance(v, bool) else str(v))]
        output = folder/'analysis.gcode'
        cmd = [str(args.engine.resolve()), 'slice', '-j', str(defs/'fdmprinter.def.json')] + flags
        cmd += ['-e0', '-j', str(defs/'fdmextruder.def.json')] + flags
        cmd += ['-l', str(ROOT/'slicing/models/3DBenchy.stl'), '-o', str(output)]
        env = os.environ.copy(); env['CURA_ENGINE_SEARCH_PATH'] = str(defs)
        p = subprocess.run(cmd, capture_output=True, text=True, env=env)
        (folder/'slice-log.txt').write_text(p.stdout+p.stderr, encoding='utf-8')
        assert p.returncode == 0, name
        (folder/'settings.json').write_text(json.dumps(trial, indent=2)+'\n', encoding='utf-8')
        (folder/'provenance.json').write_text(json.dumps({**meta, 'parent_trial':'cura-4.13.1-simplified',
            'changed_settings':changes, 'gcode_sha256':hashlib.sha256(output.read_bytes()).hexdigest()}, indent=2)+'\n', encoding='utf-8')
        moves = parse(output)
        row = {'name':name, 'changed_settings':changes, 'summary':summarize(moves), 'audit':audit(output),
               'timing': [duration(moves, q, 2400, a, scv, first_layer_cap=300)
                          for q in (200, 250, 300) for a in (500000, 1000000, 2000000) for scv in (50, 100, 500)]}
        result['trials'].append(row)
        print(name, 'mass', row['summary']['mass_g'], 'violations', len(row['audit']['certain_width_violations']),
              'fastest', min(x['seconds'] for x in row['timing']), flush=True)
    (ROOT/'engineering/width-study-results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--engine', required=True, type=Path)
    run(ap.parse_args())
