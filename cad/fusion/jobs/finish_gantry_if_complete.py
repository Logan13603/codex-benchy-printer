"""One-shot guarded recovery save. No CAD construction, retries or event pumping.

Run only after the native02R2 attempt. A delayed MCP response is not success:
inspect the persisted result and archive manifest before reporting completion.
Document.save reference:
https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/core_Document_save.htm
"""
import adsk.core, adsk.fusion
import datetime, hashlib, json
from pathlib import Path


def run(_context: str):
    base = Path(__file__).resolve().parents[2]
    result_path = base / 'native' / 'gantry-recovery-save-result.json'
    report = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'INSPECTING_NOT_YET_SAVED'}
    def record():
        result_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    record()
    app = adsk.core.Application.get()
    doc = app.activeDocument
    assert doc.name == 'Codex Benchy Printer RevF Detailed Bowden', doc.name
    assert doc.isSaved
    assert doc.dataFile.id == 'urn:adsk.wipprod:dm.lineage:KBbymbG_SICh0kr8e2I17A'
    d = adsk.fusion.Design.cast(app.activeProduct)
    source = base / 'revf' / '02_motion_r2.py'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == '053d49251b6461574097cbdba4e62b5531e6fcea44ed66e8863c2dd376fbffc0'
    ns = {'__file__': str(source)}
    exec(compile(source.read_text(encoding='utf-8'), str(source), 'exec'), ns)
    contract = ns['source_selfcheck']()
    all_components = list(d.allComponents)
    if any(c.name == '22_Y_GANTRY_R2_STAGING' for c in all_components):
        report['status'] = 'INCOMPLETE_STAGING_PRESENT_NO_SAVE'
        record(); print(json.dumps(report)); return
    old_names = ('CBP-M202_CARBON_X_TUBE_190', 'CBP-P203_MGN7_X_RAIL_180')
    if any(c.name in old_names for c in all_components):
        report['status'] = 'OLD_GANTRY_PRESENT_NO_SAVE'
        record(); print(json.dumps(report)); return
    checks = []
    for name, expected in contract.items():
        matches = [c for c in all_components if c.name == name]
        assert len(matches) == 1, (name, len(matches))
        c = matches[0]
        assert c.bRepBodies.count == 1 and c.bRepBodies.item(0).isSolid, name
        b = c.bRepBodies.item(0)
        volume = b.volume * 1000
        assert abs(volume - expected['volume_mm3']) < .05, (name, volume)
        bounds = [[p.x*10, p.y*10, p.z*10] for p in (b.boundingBox.minPoint, b.boundingBox.maxPoint)]
        assert all(abs(a-b) < .001 for p,q in zip(bounds, expected['bbox_mm']) for a,b in zip(p,q)), (name, bounds)
        assert all(s.isFullyConstrained for s in c.sketches), name
        assert all(f.healthState == adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState for f in c.features), name
        checks.append({'component':name, 'volume_mm3':volume, 'bbox_mm':bounds})
    # The original replacement also checks a complete before/after fingerprint.
    # Independently compare fixed rail volumes to the saved013 reference here.
    prior = json.loads((base/'native'/'CBP-RevF-013-Complete-Bracing-Display-manifest.json').read_text(encoding='utf-8'))
    fixed_names = ('CBP-M201_Y_RAIL_ADAPTER_AL4', 'CBP-P201_MGN9_RAIL_200')
    for name in fixed_names:
        expected = sorted(r['volume_mm3'] for r in prior['components'] if r['name'] == name)
        current = sorted(sum(b.volume*1000 for b in c.bRepBodies) for c in all_components if c.name == name)
        # Two occurrences reuse each unique component definition in013.
        assert len(current) == len(expected) == 1, (name, current, expected)
        assert all(abs(a-b) < .05 for a,b in zip(current, expected)), (name, current, expected)
    report.update(status='GEOMETRY_CHECKS_PASSED_SAVE_REQUESTED', checks=checks)
    record()
    assert doc.save('Guarded150/140mm native gantry recovery checkpoint; development CAD'), 'Native save failed'
    report.update(status='SAVE_RETURNED_TRUE', fusion_version=doc.dataFile.versionNumber, modified=doc.isModified)
    record()
    if doc.isModified:
        report['status'] = 'SAVE_RETURNED_TRUE_EXPORT_DEFERRED_STILL_MODIFIED'
        record(); print(json.dumps(report)); return
    snapshot_source = base/'fusion'/'jobs'/'snapshot_saved.py'
    snapshot_ns = {'__file__':str(snapshot_source)}
    exec(compile(snapshot_source.read_text(encoding='utf-8'), str(snapshot_source), 'exec'), snapshot_ns)
    snapshot_ns['snapshot']('CBP-RevF-014-Native-Gantry-Recovery')
    report['status'] = 'SAVED_AND_EXPORTED_014_NOT_REOPENED_OR_UPLOADED'
    record(); print(json.dumps(report))
