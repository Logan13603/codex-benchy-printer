"""Native Fusion replacement of ONLY the obsolete RevF 190/180 gantry.

Load common.py, then the tested helper definitions from04_toolhead.py, then
this source. Merely loading this file does not execute Fusion operations.
Explicit execution after a saved/exported checkpoint is:
    run('REPLACE_OLD_190_180_GANTRY_AFTER_CHECKPOINT')

This is deliberately not a generic updater. It requires the exact document,
old subtree names, old190/180 parameters, frozen CQ source hash, and unchanged
fixed-Y subtree. It builds a staging subtree first and checks every body
volume/bound and sketch before deleting the guarded old22 occurrence. Do not
rerun it over a completed R2 subtree. It never builds05/06 mount components.

All dimensions are mm; native Fusion physical-property volumes are cm^3.
Purchased rail/block raceways are simplified exactly as01_frame_xy_cq.py.
Thread pilots represent M2/M3 tapped interfaces, not modeled helical threads.
Published purchased masses override simplified solid volumes.
"""
import collections
import hashlib
import math
from pathlib import Path


_M2_DOCUMENT = 'Codex Benchy Printer RevF Detailed Bowden'
_M2_ACK = 'REPLACE_OLD_190_180_GANTRY_AFTER_CHECKPOINT'
_M2_STAGE = '22_Y_GANTRY_R2_STAGING'
_M2_SOURCE = Path(r'C:\Users\logan\Documents\Codex\2026-09-20\this-will-take-multiple-trys-because-3\outputs\codex-benchy-printer\cad\revf\01_frame_xy_cq.py')
_M2_SOURCE_SHA256 = 'ca96f5a8c68f1ecc88ab372e5f045fb85980d3829cd5c846886b9fd997de3de7'
_M2_OLD_CHILDREN = collections.Counter({
    'CBP-P202_MGN9H_MOUNT_CAP': 2,
    'CBP-M202_CARBON_X_TUBE_190': 1,
    'CBP-M203R_Y_END_SOCKET': 1,
    'CBP-M203L_Y_END_SOCKET': 1,
    'CBP-P203_MGN7_X_RAIL_180': 1,
    'CBP-M204_X_RAIL_THREAD_STRIP': 1,
    '23_X_CARRIAGE': 1,
})
_M2_FIXED_CHILDREN = collections.Counter({
    'CBP-M201_Y_RAIL_ADAPTER_AL4': 2,
    'CBP-P201_MGN9_RAIL_200': 2,
})


def source_selfcheck():
    """Pure-Python analytic geometry contract; no Fusion import or mutation.

    The rail has throughØ2.3 and additional annularØ4.2×2.4 counterbores.
    Relief tools run entirely along block length, hence the removed groove
    uses actual block length, not the slightly longer cutter length.
    """
    disk = lambda dia: math.pi * (dia / 2.0) ** 2
    beam_v = 150 * (20 * 20 - 17 * 17) - 9 * disk(2.3) * 1.5
    strip_v = 140 * 8 * 2 - 9 * disk(1.6) * 2
    rail_v = 140 * 7 * 4.8 - 9 * (disk(2.3) * 4.8 +
                                                   (disk(4.2) - disk(2.3)) * 2.4)
    yblock_v = 10 * 39.9 * 20 - 6.6 * 39.9 * 9.3 - 4 * disk(2.5) * 3
    xblock_v = 30.8 * 8 * 17 - 30.8 * 5 * 7.3 - 4 * disk(1.6) * 2.5
    rows = {
        'CBP-P202_MGN9H_Y_BLOCK_L': (yblock_v, ((-116, -19.95, 270), (-106, 19.95, 290))),
        'CBP-P202_MGN9H_Y_BLOCK_R': (yblock_v, ((106, -19.95, 270), (116, 19.95, 290))),
        'CBP-M202_CARBON_X_TUBE_150': (beam_v, ((-75, -10, 270), (75, 10, 290))),
        'CBP-M204_BONDED_M2_STRIP': (strip_v, ((-70, -8.5, 276), (70, -6.5, 284))),
        'CBP-P203_MGN7_X_RAIL_140': (rail_v, ((-70, -14.8, 276.5), (70, -10, 283.5))),
        'CBP-P204_MGN7H_X_BLOCK': (xblock_v, ((-15.4, -18, 271.5), (15.4, -10, 288.5))),
    }
    assert list(range(-60, 61, 15)) == [-60, -45, -30, -15, 0, 15, 30, 45, 60]
    assert (140 - 8 * 15) / 2 == 10, 'Nine rail holes must have10mm end margins'
    assert (150 - 140) / 2 == 5, 'Rail length must remain inside beam ends'
    assert abs((-10 - 4.8) - (-14.8)) < 1e-12, 'Rail extrusion direction must be negativeY'
    assert abs((-12.4 - 2.4) - (-14.8)) < 1e-12, 'Counterbore must open at negativeY front face'
    assert all(v > 0 for v, _ in rows.values())
    return {n: {'volume_mm3': v, 'bbox_mm': b} for n, (v, b) in rows.items()}


def _m2_occ(parent, name):
    matches = [o for o in parent.occurrences if o.component.name == name]
    assert len(matches) == 1, (name, 'expected exactly one occurrence', len(matches))
    return matches[0]


def _m2_names(c):
    return collections.Counter(o.component.name for o in c.occurrences)


def _m2_matrix(o):
    return tuple(float(q) for q in o.transform2.asArray())


def _m2_identity(o):
    target = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
    assert all(abs(a - b) < 1e-8 for a, b in zip(_m2_matrix(o), target)), \
        'Return occurrence to frozen zero pose before replacement: ' + o.name


def _m2_fixed_snapshot(c):
    """Geometry/placement fingerprint independent of token-string stability."""
    return sorted((o.name, o.component.name, _m2_matrix(o),
                   tuple(round(b.physicalProperties.volume, 10) for b in o.component.bRepBodies),
                   tuple((s.name, s.isFullyConstrained) for s in o.component.sketches))
                  for o in c.occurrences)


def _m2_guard_old(d):
    assert d and d.designType == adsk.fusion.DesignTypes.ParametricDesignType
    assert d.parentDocument.name == _M2_DOCUMENT, \
        'Wrong document; expected exactly: ' + _M2_DOCUMENT
    assert _M2_SOURCE.is_file(), 'Frozen CQ source is not available: ' + str(_M2_SOURCE)
    actual_hash = hashlib.sha256(_M2_SOURCE.read_bytes()).hexdigest()
    assert actual_hash == _M2_SOURCE_SHA256, 'Frozen01_frame_xy_cq.py changed; review R2 contract first'
    motion_o = _m2_occ(d.rootComponent, '20_XY_MOTION')
    _m2_identity(motion_o)
    fixed_o = _m2_occ(motion_o.component, '21_Y_RAILS_FIXED')
    old_o = _m2_occ(motion_o.component, '22_Y_GANTRY')
    _m2_identity(fixed_o)
    _m2_identity(old_o)
    assert _m2_names(fixed_o.component) == _M2_FIXED_CHILDREN, \
        'Fixed Y rail subtree differs from reviewed source'
    assert _m2_names(old_o.component) == _M2_OLD_CHILDREN, \
        'Old22 has unexpected/new components; no replacement authorized by this builder'
    old_x = _m2_occ(old_o.component, '23_X_CARRIAGE').component
    assert _m2_names(old_x) == collections.Counter({'CBP-P204_MGN7H_MOUNT_CAP': 1})
    assert old_o.component.bRepBodies.count == 0 and old_x.bRepBodies.count == 0
    for name, mm in [('x_beam_l', 190), ('x_rail_l', 180)]:
        p = d.userParameters.itemByName(name)
        assert p and abs(p.value * 10 - mm) < 1e-6, (name, 'not the obsolete190/180 source')
    old_beam = _m2_occ(old_o.component, 'CBP-M202_CARBON_X_TUBE_190').component
    assert old_beam.bRepBodies.count == 1
    body=old_beam.bRepBodies.item(0)
    volume=body.physicalProperties.volume*1000
    if abs(volume-21090)>=.05:
        # Inspected native v5: old unscoped socket cuts also trimmed20mm
        # from each tube end. Recognize only that exact reviewed variant.
        assert abs(volume-16650)<.05,'Unreviewed old tube geometry'
        assert [f.name for f in old_beam.features]==['EX-CBP-M202','CUT-HOLLOW','CUT-CARBON-SOCKET','CUT-CARBON-SOCKET (1)']
        actual=[p.asArray() for p in [body.boundingBox.minPoint,body.boundingBox.maxPoint]]
        assert all(abs(a-b)<1e-7 for row,expected in zip(actual,[(-1,-1,2),(1,1,17)]) for a,b in zip(row,expected))
    return motion_o.component, fixed_o, old_o


def _m2_parameters(d):
    entries = [
        ('rf_m2_beam_l', '150 mm', 'Frozen closed carbon tube length; former190mm model superseded'),
        ('rf_m2_beam_side', '20 mm', 'Stock square carbon tube outside side'),
        ('rf_m2_beam_wall', '1.5 mm', 'Nominal stock wall; actual supplier tolerance remains a hold'),
        ('rf_m2_rail_l', '140 mm', 'MGN7 X rail custom cut;9 holes with10mm end margins'),
        ('rf_m2_rail_w', '7 mm', 'MGN7 rail section width along globalZ'),
        ('rf_m2_rail_h', '4.8 mm', 'MGN7 rail depth along globalY'),
        ('rf_m2_rail_pitch', '15 mm', 'Nine rail and backing-strip hole stations'),
        ('rf_m2_rail_clear', '2.3 mm', 'M2 clearance hole in carbon and rail'),
        ('rf_m2_rail_cbore', '4.2 mm', 'Purchased rail screw-head counterbore'),
        ('rf_m2_rail_cbdepth', '2.4 mm', 'Purchased rail counterbore depth from front face'),
        ('rf_m2_m2_pilot', '1.6 mm', 'M2 tapping pilot; helical threads not modeled'),
        ('rf_m2_m3_pilot', '2.5 mm', 'M3 tapping pilot; helical threads not modeled'),
        ('rf_m2_strip_h', '8 mm', 'Backing strip height along globalZ'),
        ('rf_m2_strip_t', '2 mm', '6061 strip thickness; bonded to tube front inner wall'),
        ('rf_m2_strip_y', '-7.5 mm', 'Strip center; outer faceY-8.5 touches carbon inner wall'),
        ('rf_m2_rail_y', '-12.4 mm', 'Rail center; rearY-10 meets tube outer wall'),
        ('rf_m2_z', '280 mm', 'Frozen gantry/rail common vertical datum'),
        ('rf_m2_yblock_x', '111 mm', 'MGN9H envelope center magnitude; front facesX+/-106'),
        ('rf_m2_yblock_l', '39.9 mm', 'HIWIN nominal MGN9H block length'),
        ('rf_m2_yblock_w', '20 mm', 'MGN9H block width along globalZ'),
        ('rf_m2_yblock_h', '10 mm', 'Complete MGN9H assembly depth; rail relief included'),
        ('rf_m2_yrelief_x', '112.7 mm', 'Center magnitude of MGN9 rail relief proxy'),
        ('rf_m2_yrelief_d', '6.6 mm', 'Rail relief depth; simplified raceway not manufacturing geometry'),
        ('rf_m2_yrelief_w', '9.3 mm', 'Rail relief width along globalZ'),
        ('rf_m2_yblock_mount_y', '8 mm', 'Half16mm longitudinal mounting pitch'),
        ('rf_m2_yblock_mount_z', '7.5 mm', 'Half15mm transverse mounting pitch'),
        ('rf_m2_yblock_tap', '3 mm', 'Blind M3 mounting-pilot depth fromX+/-106'),
        ('rf_m2_xblock_l', '30.8 mm', 'MGN7H nominal length alongX'),
        ('rf_m2_xblock_w', '17 mm', 'MGN7H width alongZ'),
        ('rf_m2_xblock_h', '8 mm', 'Complete MGN7H assembly depth alongY'),
        ('rf_m2_xblock_y', '-14 mm', 'Full block center; front mounting faceY-18'),
        ('rf_m2_xblock_mount_x', '6.5 mm', 'Half13mm mounting pitch'),
        ('rf_m2_xblock_mount_z', '6 mm', 'Half12mm mounting pitch'),
        ('rf_m2_xblock_tap', '2.5 mm', 'Blind M2 mounting-pilot depth fromY-18'),
    ]
    # Never silently reuse an already edited R2 parameter or alter legacy
    # parameters referenced by the preserved fixed rails and old geometry.
    for name, expr, note in entries:
        p = d.userParameters.itemByName(name)
        if p:
            assert abs(p.value - d.unitsManager.evaluateExpression(expr, 'mm')) < 1e-8, \
                'Existing R2 parameter differs: ' + name
        else:
            param(d, name, expr, note)


def _m2_new(parent, name, notes):
    assert not any(o.component.name == name for o in parent.occurrences), 'Already built ' + name
    c = part(parent, name).component
    c.partNumber = name
    c.description = notes
    return c


def _m2_yblock(parent, side, hand):
    op = adsk.fusion.FeatureOperations
    c = _m2_new(parent, 'CBP-P202_MGN9H_Y_BLOCK_' + hand,
        'PURCHASED MGN9H full envelope with open rail relief; nominal39.9Lx20Wx10assembly depth. M3x3blind,16Yx15Z pattern. Catalog26g overrides proxy volume; raceways/seals simplified.')
    x = str(side) + '*rf_m2_yblock_x'
    _box(c, 'MGN9H-FULL-ENVELOPE', 'rf_m2_yblock_h', 'rf_m2_yblock_l', 'rf_m2_yblock_w',
         (x, 0, 'rf_m2_z'), op.NewBodyFeatureOperation)
    _box(c, 'MGN9-RAIL-RELIEF', 'rf_m2_yrelief_d', 'rf_m2_yblock_l + .1 mm', 'rf_m2_yrelief_w',
         (str(side) + '*rf_m2_yrelief_x', 0, 'rf_m2_z'), op.CutFeatureOperation)
    for sy in (-1, 1):
        for sz in (-1, 1):
            _cyl(c, 'M3-BLIND-' + str(sy) + '-' + str(sz), 'rf_m2_m3_pilot', 'rf_m2_yblock_tap',
                 (str(side) + '*(rf_m2_yblock_x-rf_m2_yblock_h/2)',
                  str(sy) + '*rf_m2_yblock_mount_y',
                  'rf_m2_z+' + str(sz) + '*rf_m2_yblock_mount_z'),
                 (side, 0, 0), op.CutFeatureOperation)
    return c


def _m2_beam(parent):
    op = adsk.fusion.FeatureOperations
    c = _m2_new(parent, 'CBP-M202_CARBON_X_TUBE_150',
        '150x20x20x1.5 closed stock carbon tube; nineØ2.3 holes penetrate FRONT wall only fromY-10. No transverse belt ports. Stock tolerance, laminate stiffness, density and bond coupon remain validation holds.')
    _box(c, 'CF-OUTER', 'rf_m2_beam_l', 'rf_m2_beam_side', 'rf_m2_beam_side',
         (0, 0, 'rf_m2_z'), op.NewBodyFeatureOperation)
    _box(c, 'CF-OPEN-ENDED-BORE', 'rf_m2_beam_l+.2 mm', 'rf_m2_beam_side-2*rf_m2_beam_wall',
         'rf_m2_beam_side-2*rf_m2_beam_wall', (0, 0, 'rf_m2_z'), op.CutFeatureOperation)
    for k in range(-4, 5):
        _cyl(c, 'FRONT-WALL-M2-' + str(k+5), 'rf_m2_rail_clear', 'rf_m2_beam_wall',
             (str(k) + '*rf_m2_rail_pitch', '-rf_m2_beam_side/2', 'rf_m2_z'),
             (0, 1, 0), op.CutFeatureOperation)
    return c


def _m2_strip(parent):
    op = adsk.fusion.FeatureOperations
    c = _m2_new(parent, 'CBP-M204_BONDED_M2_STRIP',
        '140x8x2 6061 aluminum backing strip; nineM2through taps at15pitch,10mm end margins. Inner surface bond interfaceY-8.5. Bond preparation/coupon and fastener lengths must be verified.')
    _box(c, 'STRIP', 'rf_m2_rail_l', 'rf_m2_strip_t', 'rf_m2_strip_h',
         (0, 'rf_m2_strip_y', 'rf_m2_z'), op.NewBodyFeatureOperation)
    for k in range(-4, 5):
        _cyl(c, 'M2-THROUGH-TAP-' + str(k+5), 'rf_m2_m2_pilot', 'rf_m2_strip_t',
             (str(k) + '*rf_m2_rail_pitch', 'rf_m2_strip_y-rf_m2_strip_t/2', 'rf_m2_z'),
             (0, 1, 0), op.CutFeatureOperation)
    return c


def _m2_xrail(parent):
    op = adsk.fusion.FeatureOperations
    c = _m2_new(parent, 'CBP-P203_MGN7_X_RAIL_140',
        'PURCHASED MGN7 mounting proxy140x7x4.8; nineØ2.3through/Ø4.2x2.4counterbore fromFRONT.15pitch,10mm end margins custom-cut order. Catalog30.8g mass. Raceways omitted.')
    _box(c, 'MGN7-RAIL', 'rf_m2_rail_l', 'rf_m2_rail_h', 'rf_m2_rail_w',
         (0, 'rf_m2_rail_y', 'rf_m2_z'), op.NewBodyFeatureOperation)
    for k in range(-4, 5):
        x = str(k) + '*rf_m2_rail_pitch'
        _cyl(c, 'M2-THROUGH-' + str(k+5), 'rf_m2_rail_clear', 'rf_m2_rail_h',
             (x, 'rf_m2_rail_y+rf_m2_rail_h/2', 'rf_m2_z'), (0, -1, 0), op.CutFeatureOperation)
        _cyl(c, 'M2-COUNTERBORE-' + str(k+5), 'rf_m2_rail_cbore', 'rf_m2_rail_cbdepth',
             (x, 'rf_m2_rail_y', 'rf_m2_z'), (0, -1, 0), op.CutFeatureOperation)
    return c


def _m2_xblock(parent):
    op = adsk.fusion.FeatureOperations
    c = _m2_new(parent, 'CBP-P204_MGN7H_X_BLOCK',
        'PURCHASED MGN7H full envelope30.8x17x8 with open rail relief. FourM2x2.5blind mounting pilots at13Xx12Z fromfrontY-18. Catalog15g; raceways/seals simplified. Child of23_X_CARRIAGE.')
    _box(c, 'MGN7H-FULL-ENVELOPE', 'rf_m2_xblock_l', 'rf_m2_xblock_h', 'rf_m2_xblock_w',
         (0, 'rf_m2_xblock_y', 'rf_m2_z'), op.NewBodyFeatureOperation)
    _box(c, 'MGN7-RAIL-RELIEF', 'rf_m2_xblock_l+.2 mm', '5 mm', '7.3 mm',
         (0, '-12.5 mm', 'rf_m2_z'), op.CutFeatureOperation)
    for sx in (-1, 1):
        for sz in (-1, 1):
            _cyl(c, 'M2-BLIND-' + str(sx) + '-' + str(sz), 'rf_m2_m2_pilot', 'rf_m2_xblock_tap',
                 (str(sx) + '*rf_m2_xblock_mount_x', 'rf_m2_xblock_y-rf_m2_xblock_h/2',
                  'rf_m2_z+' + str(sz) + '*rf_m2_xblock_mount_z'),
                 (0, 1, 0), op.CutFeatureOperation)
    return c


def _m2_validate(c, contract):
    assert c.bRepBodies.count == 1, (c.name, 'expected one solid', c.bRepBodies.count)
    body = c.bRepBodies.item(0)
    assert body.isSolid, c.name
    body.name = c.name
    volume = body.physicalProperties.volume * 1000
    assert abs(volume - contract['volume_mm3']) < .05, (c.name, 'volume mismatch', volume, contract)
    bounds = body.boundingBox
    actual = [(p.x * 10, p.y * 10, p.z * 10) for p in (bounds.minPoint, bounds.maxPoint)]
    assert all(abs(a - b) < 1e-3 for q, r in zip(actual, contract['bbox_mm']) for a, b in zip(q, r)), \
        (c.name, 'bounds mismatch', actual, contract['bbox_mm'])
    assert all(s.isFullyConstrained for s in c.sketches), (c.name, 'unconstrained sketch')
    return {'name': c.name, 'volume_mm3': volume, 'bbox_mm': actual, 'sketches': c.sketches.count}


def run(_context: str):
    """Explicit guarded replacement; root operator must checkpoint first."""
    assert _context == _M2_ACK, 'Explicit checkpoint acknowledgement required: run(' + repr(_M2_ACK) + ')'
    assert all(callable(globals().get(n)) for n in ('param', 'part', '_box', '_cyl', 'audit')), \
        'Load common.py and tested04 helper definitions first; do not execute04.run'
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    motion, fixed_o, old_o = _m2_guard_old(d)
    assert not any(o.component.name == _M2_STAGE for o in motion.occurrences), \
        'Existing staging subtree requires manual inspection before retry'
    fixed_before = _m2_fixed_snapshot(fixed_o.component)
    _m2_parameters(d)
    staging = part(motion, _M2_STAGE)
    committed = False
    try:
        moving = staging.component
        moving.description = 'R2 native150/140 gantry; matches frozen01_frame_xy_cq.py. Purchased proxies have complete rail clearances;05/06 end supports built separately.'
        built = [_m2_yblock(moving, -1, 'L'), _m2_yblock(moving, 1, 'R'),
                 _m2_beam(moving), _m2_strip(moving), _m2_xrail(moving)]
        head = _m2_new(moving, '23_X_CARRIAGE', 'Separate X-moving group; full MGN7H block only at this stage.')
        built.append(_m2_xblock(head))
        d.computeAll()
        contract = source_selfcheck()
        results = [_m2_validate(c, contract[c.name]) for c in built]
        assert _m2_fixed_snapshot(fixed_o.component) == fixed_before, 'Fixed Y rails changed; abort before deleting old22'
        # Recheck the exact original subtree at the final mutation boundary.
        current_motion, current_fixed, current_old = _m2_guard_old(d)
        assert current_old.isValid and old_o.isValid
        assert _m2_fixed_snapshot(current_fixed.component) == fixed_before
        assert current_old.deleteMe(), 'Could not remove guarded obsolete22 occurrence'
        committed = True
        moving.name = '22_Y_GANTRY'
        d.computeAll()
        assert _m2_fixed_snapshot(fixed_o.component) == fixed_before, 'Fixed Y preservation check failed'
        audit(d)
        print('R2 NATIVE GEOMETRY CHECKS:', results)
        print('Replaced only guarded old22:150mm closed carbon tube,140mm rail, full relieved MGN9H/MGN7H blocks.21 preserved. Save/export/checkpoint before05/06 mounts; manufacturing and travel validation remain pending.')
    except Exception:
        # Construction failure preserves old22. If commit already occurred,
        # retain the validated R2 subtree for inspection/recovery instead.
        if not committed and staging.isValid:
            assert staging.deleteMe(), 'Staging cleanup failed; inspect before retry'
        raise
