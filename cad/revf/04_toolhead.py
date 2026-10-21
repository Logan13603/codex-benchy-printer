"""Native Fusion feature builder for the RevF Bowden toolhead.

Load common.py first, then this file.  No custom sketch is fixed.  Coordinate
dimensioned points are used for the nonorthogonal split masks and hex pockets.
This builder has NOT been executed in the current locked desktop session.
The CadQuery counterpart is executed and audited independently; that does not
verify Fusion loft correspondence or sketch solving.  Purchased component and
fastener STEP files are imported as individual named components after custom
features; their native interfaces are deliberately not replaced with a solid
monolithic toolhead import.
"""
import os
import json


def _exp(x):
    return str(x) if isinstance(x, str) else str(float(x)) + ' mm'


def _abs_exp(e):
    return '-(' + e + ')' if val(e) < 0 else e


def _pin(s, p, x, y):
    """Drive a point in sketch coordinates, without fixing geometry."""
    ori = adsk.fusion.DimensionOrientations
    a, b = val(x), val(y)
    if abs(a) < 1e-8 and abs(b) < 1e-8:
        s.geometricConstraints.addCoincident(p, s.originPoint)
        return
    if abs(a)>1e-8 and abs(b)>1e-8:
        # Fusion's solver can reject two origin-distance dimensions on a
        # freestanding polygon vertex. A constrained coordinate datum gives
        # the same two driving coordinates without fixing any geometry.
        reference=next((q for q in s.sketchPoints if q!=p and q.isFullyConstrained
                        and abs(q.geometry.y-b)<1e-7),None)
        if reference is None:
            reference=s.sketchPoints.add(adsk.core.Point3D.create(0,b,0))
            s.geometricConstraints.addVerticalPoints(s.originPoint,reference)
            s.sketchDimensions.addDistanceDimension(s.originPoint,reference,
                ori.VerticalDimensionOrientation,
                adsk.core.Point3D.create(.5,b/2,0)).parameter.expression=_abs_exp(y)
        s.geometricConstraints.addHorizontalPoints(reference,p)
        s.sketchDimensions.addDistanceDimension(s.originPoint,p,
            ori.HorizontalDimensionOrientation,
            adsk.core.Point3D.create(a/2,b+.5,0)).parameter.expression=_abs_exp(x)
        return
    if abs(a) < 1e-8:
        s.geometricConstraints.addVerticalPoints(s.originPoint, p)
    else:
        s.sketchDimensions.addDistanceDimension(s.originPoint, p,
            ori.HorizontalDimensionOrientation,
            adsk.core.Point3D.create(a / 2, b + .5, 0)).parameter.expression = _abs_exp(x)
    if abs(b) < 1e-8:
        s.geometricConstraints.addHorizontalPoints(s.originPoint, p)
    else:
        s.sketchDimensions.addDistanceDimension(s.originPoint, p,
            ori.VerticalDimensionOrientation,
            adsk.core.Point3D.create(a + .5, b / 2, 0)).parameter.expression = _abs_exp(y)


def _projection(direction, xyz):
    return ' + '.join('(' + format(k, '.12g') + ')*(' + _exp(e) + ')'
                      for k, e in zip((direction.x, direction.y, direction.z), xyz)
                      if abs(k) > 1e-10) or '0 mm'


def _plane(c, name, xyz, normal=(0, 0, 1)):
    """Parametric rotated + offset plane for XZ-normal or Y-normal profiles."""
    nx, ny, nz = normal
    if abs(ny) < 1e-7:
        angle = math.degrees(math.atan2(nx, nz))
        axis = c.yConstructionAxis
    else:
        assert abs(nx) < 1e-7 and abs(nz) < 1e-7
        angle = -90 if ny > 0 else 90
        axis = c.xConstructionAxis
    if abs(angle) < 1e-9:
        base = c.xYConstructionPlane
    else:
        i = c.constructionPlanes.createInput()
        assert i.setByAngle(axis, vi(str(angle) + ' deg'), c.xYConstructionPlane)
        base = c.constructionPlanes.add(i)
        base.name = 'PL-' + name + '-ANGLE'
        base.isLightBulbOn = False
    n = base.geometry.normal
    offset = _projection(n, xyz)
    i = c.constructionPlanes.createInput()
    assert i.setByOffset(base, vi(offset))
    p = c.constructionPlanes.add(i)
    p.name = 'PL-' + name
    p.isLightBulbOn = False
    return p


def _profile(c, name, xyz, normal, wy, hx):
    """Rectangular loft section with local X chosen by actual plane orientation."""
    p = _plane(c, name, xyz, normal)
    probe = c.sketches.add(p)
    xd, yd = probe.xDirection, probe.yDirection
    cx, cy = _projection(xd, xyz), _projection(yd, xyz)
    # If the sketch X axis is along Y, width is wy; otherwise it is hx.
    w, h = (wy, hx) if abs(xd.y) > .9 else (hx, wy)
    assert probe.deleteMe()
    return rect_sketch(c, 'SK-' + name, _exp(w), _exp(h), cx, cy, p)


def _circle_profile(c, name, xyz, normal, diameter):
    p = _plane(c, name, xyz, normal)
    s = c.sketches.add(p)
    s.name = 'SK-' + name
    cx, cy = _projection(s.xDirection, xyz), _projection(s.yDirection, xyz)
    cir = s.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(val(cx), val(cy), 0), val(_exp(diameter)) / 2)
    _pin(s, cir.centerSketchPoint, cx, cy)
    s.sketchDimensions.addDiameterDimension(cir,
        adsk.core.Point3D.create(val(cx) + .5, val(cy) + .5, 0)).parameter.expression = _exp(diameter)
    assert s.isFullyConstrained, name
    return s


def _poly(c, name, xyz, normal, world_points):
    p = _plane(c, name, xyz, normal)
    s = c.sketches.add(p)
    s.name = 'SK-' + name
    pts = []
    for v in world_points:
        # Plane origin is on its normal through the component origin, so its
        # in-plane dot product is zero. Dimensions therefore remain expressions.
        ux, uy = _projection(s.xDirection, v), _projection(s.yDirection, v)
        if abs(val(ux)) < 1e-8 and abs(val(uy)) < 1e-8:
            pt = s.originPoint
        else:
            pt = s.sketchPoints.add(adsk.core.Point3D.create(val(ux), val(uy), 0))
        pts.append((pt,ux,uy))
    for i, (pt,ux,uy) in enumerate(pts):
        s.sketchCurves.sketchLines.addByTwoPoints(pt, pts[(i + 1) % len(pts)][0])
    for pt,ux,uy in pts:
        if pt!=s.originPoint:_pin(s,pt,ux,uy)
    assert s.isFullyConstrained, name
    return s


def _box(c, name, dx, dy, dz, xyz, op):
    x, y, z = [_exp(q) for q in xyz]
    p = _plane(c, name, (x, y, '(' + z + ')-(' + _exp(dz) + ')/2'))
    s = rect_sketch(c, 'SK-' + name, _exp(dx), _exp(dy), x, y, p)
    return extrude(c, s, _exp(dz), op, 'EX-' + name)


def _cyl(c, name, diameter, length, xyz, axis, op):
    s = _circle_profile(c, name, xyz, axis, diameter)
    return extrude(c, s, _exp(length), op, 'EX-' + name)


def _loft(c, name, sections, op, wall=0):
    profiles = [_profile(c, name + '-' + str(i), xyz, normal,
                         '(' + _exp(wy) + ')+2*(' + _exp(wall) + ')',
                         '(' + _exp(hx) + ')+2*(' + _exp(wall) + ')')
                for i, (xyz, normal, wy, hx) in enumerate(sections)]
    # Consecutive two-section lofts reproduce the piecewise ruled construction
    # and avoid the overshoot possible with a multi-section interpolating loft.
    f = None
    for k in range(len(profiles) - 1):
        operation = op
        if k > 0 and op == adsk.fusion.FeatureOperations.NewBodyFeatureOperation:
            operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
        i = c.features.loftFeatures.createInput(operation)
        i.isSolid = True
        i.loftSections.add(profiles[k].profiles.item(0))
        i.loftSections.add(profiles[k + 1].profiles.item(0))
        if operation in (adsk.fusion.FeatureOperations.CutFeatureOperation,adsk.fusion.FeatureOperations.IntersectFeatureOperation):
            assert c.bRepBodies.count,'No owned loft target: '+name
            i.participantBodies=list(c.bRepBodies)
        f = c.features.loftFeatures.add(i)
        assert f, name
        assert all(b.parentComponent==c for b in f.bodies),'Loft escaped owning component: '+name
        f.name = 'LOFT-' + name + '-SEG-' + str(k)
    for s in profiles:
        s.isVisible = False
    return f


def _hexcut(c, name, af, length, xyz, axis):
    p = _plane(c, name, xyz, axis)
    s = c.sketches.add(p)
    s.name = 'SK-' + name
    cx, cy = _projection(s.xDirection, xyz), _projection(s.yDirection, xyz)
    r = val(_exp(af)) / math.sqrt(3)
    pts = []
    for k in range(6):
        a = k * math.pi / 3
        ux = '(' + cx + ') + ' + str(r * math.cos(a) * 10) + ' mm'
        uy = '(' + cy + ') + ' + str(r * math.sin(a) * 10) + ' mm'
        pt = s.sketchPoints.add(adsk.core.Point3D.create(val(ux), val(uy), 0))
        _pin(s, pt, ux, uy)
        pts.append(pt)
    for k, pt in enumerate(pts):
        s.sketchCurves.sketchLines.addByTwoPoints(pt, pts[(k + 1) % 6])
    assert s.isFullyConstrained, name
    return extrude(c, s, _exp(length), adsk.fusion.FeatureOperations.CutFeatureOperation, 'CUT-' + name)


def _sections(side):
    r = math.sqrt(.5)
    a = math.radians(17)
    return [
        ((side * 8, -14, 331), (0, 0, -1), 10, 12),
        ((side * 24, -38, 315), (side * r, 0, -r), 10, 12),
        ((side * 42, -62, 301), (0, 0, -1), 10, 12),
        ((side * 42, -62, 247), (0, 0, -1), 10, 12),
        ((side * 38, -55, 237), (-side * .5, 0, -math.sqrt(.75)), 14, 8),
        ((side * 27, -40, 231), (-side * math.sqrt(.75), 0, -.5), 16, 5),
        ((side * 12, -38, 228.8), (-side * math.cos(a), 0, -math.sin(a)), 16, 3),
    ]


def _new(parent, name):
    assert not any(o.component.name == name for o in parent.occurrences), 'Already built ' + name
    return part(parent, name).component


def _carrier(parent):
    op = adsk.fusion.FeatureOperations
    cut, new, join = op.CutFeatureOperation, op.NewBodyFeatureOperation, op.JoinFeatureOperation
    c = _new(parent, 'CBP-P401_R1_AL_CARRIAGE_SPINE')
    _box(c, 'SPINE', 36, 3, 54, (0, -19.5, 283), new)
    for x in (-6.5, 6.5):
        for z in (274, 286):
            _cyl(c, 'MGN7-' + str(x) + '-' + str(z), 2.2, 4, (x, -17.5, z), (0, -1, 0), cut)
    for x in (-10, 10):
        _cyl(c, 'PLATFORM-' + str(x), 3.3, 4, (x, -17.5, 297.26), (0, -1, 0), cut)
        _cyl(c, 'GUARD-TAP-M2-' + str(x), 1.6, 4, (x, -17.5, 260), (0, -1, 0), cut)
    for x in (-11, 11):
        _cyl(c, 'BRIDGE-TAP-M3-' + str(x), 2.5, 4, (x, -17.5, 306), (0, -1, 0), cut)
    for x in (-15, 15):
        _cyl(c, 'WIRE-TAP-M2-' + str(x), 1.6, 4, (x, -17.5, 294), (0, -1, 0), cut)
    c = _new(parent, 'CBP-P402_R1_AL_HOTEND_PLATFORM')
    _box(c, 'PLATFORM', 32, 30, 6, (0, -36, 'rf_hotend_mount_z + 3 mm'), new)
    for x in (-5.657, 5.657):
        for dy in (-5.657, 5.657):
            _cyl(c, 'HOTEND-' + str(x) + '-' + str(dy), 2.7, 7,
                 (x, -38 + dy, 'rf_hotend_mount_z - .5 mm'), (0, 0, 1), cut)
    _cyl(c, 'PC4-M6-TAP', 5, 7, (0, -38, 'rf_hotend_mount_z - .5 mm'), (0, 0, 1), cut)
    for x in (-10, 10):
        _cyl(c, 'EDGE-TAP-M3-' + str(x), 2.5, 10, (x, -21, 297.26), (0, -1, 0), cut)
    for x in (-12, 12):
        _cyl(c, 'FAN-TAP-M3-' + str(x), 2.5, 4.5, (x, -48, 300.26), (0, 0, -1), cut)
    for x in (-11, 11):
        _cyl(c, 'BRIDGE-HEAD-RELIEF-' + str(x), 6.4, 1, (x, -29.8, 'rf_hotend_mount_z'), (0, 0, 1), cut)
    c = _new(parent, 'CBP-P403_R1_DUCT_SUPPORT_BRIDGE')
    _box(c, 'BRIDGE-CROSSBAR', 114, 6.8, 8, (0, -24.4, 306), new)
    for x in (-11, 11):
        _cyl(c, 'SPINE-M3-' + str(x), 3.3, 8, (x, -28.4, 306), (0, 1, 0), cut)
    for side in (-1, 1):
        _box(c, 'FORWARD-ARM-' + str(side), 8, 28.5, 7, (side * 52, -35.25, 306), join)
        _box(c, 'FRONT-LEG-' + str(side), 8, 6.8, 18, (side * 52, -46.1, 300.5), join)
        _box(c, 'BOSS-FOOT-' + str(side), 18, 9.1, 7, (side * 47, -47.25, 295), join)
        _cyl(c, 'DUCT-M3-' + str(side), 3.3, 10, (side * 42, -52.4, 295), (0, 1, 0), cut)
    for x in (-25, 25):
        _box(c, 'LIGHTEN-' + str(x), 18, 8, 4, (x, -24.4, 306), cut)
    c = _new(parent, 'CBP-P405_R1_REAR_THERMAL_WIRE_GUARD')
    _box(c, 'GUARD', 24, .5, 20, (0, -22.75, 253), new)
    for x in (-10, 10):
        _cyl(c, 'M2-' + str(x), 2.2, 1, (x, -23.2, 260), (0, 1, 0), cut)
    for cover in (False, True):
        c = _new(parent, 'CBP-P407_R1_WIRE_SADDLE_COVER' if cover else 'CBP-P406_R1_WIRE_SADDLE')
        _box(c, 'WIRE-CLAMP', 36, 2 if cover else 7, 8, (0, -10 if cover else -14.5, 295), new)
        for x in (-3, 3):
            _cyl(c, 'WIRE-GROOVE-' + str(x), 3.5, 9, (x, -11, 290.5), (0, 0, 1), cut)
        for x in (-15, 15):
            _cyl(c, 'WIRE-M2-' + str(x), 2.2, 3 if cover else 8,
                 (x, -8.5 if cover else -10.5, 294), (0, -1, 0), cut)
        for x in (-10, 10):
            _cyl(c, 'PLATFORM-HEAD-ACCESS-' + str(x), 7, 11,
                 (x, -18.5, 297.26), (0, 1, 0), cut)


def _flange(c, side, z, name):
    op = adsk.fusion.FeatureOperations
    _box(c, name, 41, 20.2, 2, (side * 42, -62, z), op.JoinFeatureOperation)
    _box(c, name + '-FLOW', 12, 10, 4, (side * 42, -62, z), op.CutFeatureOperation)
    for x in (-17.5, 17.5):
        for y in (-7.1, 7.1):
            _cyl(c, name + '-M2p5-' + str(x) + '-' + str(y), 2.7, 4,
                 (side * 42 + x, -62 + y, z - 2), (0, 0, 1), op.CutFeatureOperation)


def _fork(parent, front):
    op = adsk.fusion.FeatureOperations
    name = 'CBP-P411_R1_CPAP_FORK_FRONT' if front else 'CBP-P412_R1_CPAP_FORK_REAR'
    c = _new(parent, name)
    _cyl(c, 'INLET-OD', 25, 24, (0, -14, 326), (0, 0, 1), op.NewBodyFeatureOperation)
    for side in (-1, 1):
        sec = _sections(side)[:3]
        _loft(c, 'FORK-OUTER-' + str(side), sec, op.JoinFeatureOperation, 'rf_cpap_wall')
    _cyl(c, 'INLET-ID', 22, 26, (0, -14, 325), (0, 0, 1), op.CutFeatureOperation)
    for side in (-1, 1):
        sec = _sections(side)[:3]
        _loft(c, 'FORK-FLOW-' + str(side), sec, op.CutFeatureOperation)
        _flange(c, side, 302, 'FLANGE-' + str(side))
    for x in (-16, 16):
        _box(c, 'INLET-SEAM-PAD-' + str(x), 10, 6, 8, (x, -14, 339), op.JoinFeatureOperation)
        _cyl(c, 'INLET-SEAM-M2p5-' + str(x), 2.7, 8, (x, -18, 339), (0, 1, 0), op.CutFeatureOperation)
        _hexcut(c, 'INLET-NUT-' + str(x), 5, 2, (x, -11, 339), (0, -1, 0))
    for side in (-1, 1):
        x = side * 39
        _box(c, 'ARM-SEAM-PAD-' + str(side), 22, 6, 8, (x, -38, 315), op.JoinFeatureOperation)
        _cyl(c, 'ARM-SEAM-M2p5-' + str(side), 2.7, 8, (x, -42, 315), (0, 1, 0), op.CutFeatureOperation)
        _hexcut(c, 'ARM-NUT-' + str(side), 5, 2, (x, -35, 315), (0, -1, 0))
    yz = ([(-62, 190), (150, 190), (150, 400), (-14, 400), (-14, 331), (-38, 315), (-62, 301)]
          if front else [(-150, 190), (-62, 190), (-62, 301), (-38, 315), (-14, 331), (-14, 400), (-150, 400)])
    s = _poly(c, 'MEDIAN-SPLIT', (-110, 0, 0), (1, 0, 0), [(-110, y, z) for y, z in yz])
    extrude(c, s, '220 mm', op.CutFeatureOperation, 'CUT-MEDIAN-SPLIT')
    return c


def _lower(parent, side, front):
    op = adsk.fusion.FeatureOperations
    number = ('413' if front else '414') if side < 0 else ('415' if front else '416')
    c = _new(parent, 'CBP-P' + number + '_R1_' + ('LEFT' if side < 0 else 'RIGHT') + '_DUCT_' + ('FRONT' if front else 'REAR'))
    sec = _sections(side)[2:]
    _loft(c, 'DUCT-OUTER', sec, op.NewBodyFeatureOperation, 'rf_cpap_wall')
    inner = list(sec)
    p, n, w, h = inner[-1]
    inner[-1] = (tuple(p[i] + n[i] * .25 for i in range(3)), n, w, h)
    _loft(c, 'DUCT-FLOW', inner, op.CutFeatureOperation)
    _flange(c, side, 300, 'FLANGE')
    for z in (248, 271, 289):
        _box(c, 'SEAM-PAD-' + str(z), 8, 5, 6, (side * 52.4, -62, z), op.JoinFeatureOperation)
        _cyl(c, 'SEAM-M2p5-' + str(z), 2.7, 7, (side * 52.4, -65.5, z), (0, 1, 0), op.CutFeatureOperation)
        _hexcut(c, 'SEAM-NUT-' + str(z), 5, 2, (side * 52.4, -59.5, z), (0, -1, 0))
    _box(c, 'SUPPORT-BOSS', 10, 4, 10, (side * 42, -53.8, 295), op.JoinFeatureOperation)
    _cyl(c, 'SUPPORT-M3', 3.3, 3.7, (side * 42, -51.8, 295), (0, -1, 0), op.CutFeatureOperation)
    _hexcut(c, 'SUPPORT-NUT', 5.5, 2.4, (side * 42, -51.8, 295), (0, -1, 0))
    yz = ([(-38, 180), (150, 180), (150, 330), (-62, 330), (-62, 247), (-55, 237), (-40, 231), (-38, 228.8)]
          if front else [(-160, 180), (-38, 180), (-38, 228.8), (-40, 231), (-55, 237), (-62, 247), (-62, 330), (-160, 330)])
    s = _poly(c, 'MEDIAN-SPLIT', (-110, 0, 0), (1, 0, 0), [(-110, y, z) for y, z in yz])
    extrude(c, s, '220 mm', op.CutFeatureOperation, 'CUT-MEDIAN-SPLIT')
    return c


def _fan(parent):
    op = adsk.fusion.FeatureOperations
    c = _new(parent, 'CBP-P404_R1_COLDEND_FAN_CRADLE')
    _box(c, 'FAN-FRAME', 30, 3, 30, (0, -66.5, 272), op.NewBodyFeatureOperation)
    _cyl(c, 'FAN-OPENING', 22, 4, (0, -68.5, 272), (0, 1, 0), op.CutFeatureOperation)
    # Generic profile helper expects normals in XZ; Y-normal profiles use the
    # same method and detects width orientation via plane.xDirection.
    _loft(c, 'COLDEND-SHROUD-OUTER', [((0, -65, 272), (0, 1, 0), 22.4, 22.4),
                                    ((0, -52, 272), (0, 1, 0), 26.4, 26.4)], op.JoinFeatureOperation)
    _loft(c, 'COLDEND-SHROUD-FLOW', [((0, -65.2, 272), (0, 1, 0), 20, 20),
                                   ((0, -51.8, 272), (0, 1, 0), 24, 24)], op.CutFeatureOperation)
    for x in (-10, 10):
        for z in (262, 282):
            _cyl(c, 'FAN-M2-' + str(x) + '-' + str(z), 2.2, 4, (x, -68.5, z), (0, 1, 0), op.CutFeatureOperation)
            _cyl(c, 'FAN-NUT-TOOL-CLEARANCE-' + str(x) + '-' + str(z), 5.4, 8, (x, -65, z), (0, 1, 0), op.CutFeatureOperation)
    for x in (-12, 12):
        _box(c, 'FAN-COLUMN-' + str(x), 4, 3, 17.26, (x, -66.5, 294.63), op.JoinFeatureOperation)
        _box(c, 'FAN-FOOT-' + str(x), 8, 18.5, 3, (x, -57.25, 301.76), op.JoinFeatureOperation)
        _cyl(c, 'FAN-FOOT-M3-' + str(x), 3.3, 4, (x, -48, 299.76), (0, 0, 1), op.CutFeatureOperation)


def _import_hardware(parent, export_folder):
    app = adsk.core.Application.get()
    prefix = ('CBP-H', 'CBP-C401', 'CBP-C402', 'CBP-C403')
    assert os.path.isdir(export_folder), 'Run 04_toolhead_cq.py standalone export first'
    manifest_path = os.path.join(export_folder, 'toolhead-components.json')
    with open(manifest_path, 'r', encoding='utf-8') as handle:
        current_files = [row['name'] + '.step' for row in json.load(handle)]
    for filename in sorted(current_files):
        if filename.lower().endswith('.step') and filename.startswith(prefix):
            name = filename[:-5]
            if any(o.component.name == name for o in parent.occurrences):
                continue
            o = part(parent, name)
            options = app.importManager.createSTEPImportOptions(os.path.join(export_folder, filename))
            assert app.importManager.importToTarget(options, o.component)


def run(_context: str):
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    assert d and d.designType == adsk.fusion.DesignTypes.ParametricDesignType
    param(d, 'rf_hotend_mount_z', '294.26 mm', 'Goliath maker mounting top, 69.26 mm above nozzle datum')
    param(d, 'rf_cpap_wall', '1.2 mm', 'Nominal manufactured duct wall at loft sections')
    toolhead = group(d.rootComponent, '40_TOOLHEAD').component
    cooling = group(d.rootComponent, '50_CPAP_COOLING').component
    _carrier(toolhead)
    _fork(cooling, True)
    _fork(cooling, False)
    for side in (-1, 1):
        _lower(cooling, side, True)
        _lower(cooling, side, False)
    _fan(toolhead)
    # Set this absolute path to the verified local standalone export folder.
    folder = r'C:\Users\logan\Documents\Codex\2026-09-20\this-will-take-multiple-trys-because-3\outputs\codex-benchy-printer\cad\revf\generated\toolhead'
    _import_hardware(toolhead, folder)
    d.computeAll()
    audit(d)
    print('Native RevF Bowden custom toolhead built. Verify loft correspondence, interference, materials and fully constrained sketches before release.')

