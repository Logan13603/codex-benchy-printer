"""Align 9-hole X rails, two shims and blind M2 pilots in the base.

Each rail has nine holes on 15 mm pitch with 5 mm ends. An M2×12 candidate
passes through 4.8 mm rail plus 2 mm shim into 4 mm of base thread.
The Ø1.6 base pilots indicate tapping, not modeled threads. Hardware length,
rail screw-head height and torque remain procurement/assembly checks.
Read common.py before running.
"""


def _single_hole(comp, sketch_name, model_point, diameter_name,
                 depth_expr, top_y=None):
    if any(sk.name == sketch_name for sk in comp.sketches):
        return
    if top_y is None:
        sketch = comp.sketches.add(comp.xZConstructionPlane)
        q = adsk.core.Point3D.create(model_point[0], model_point[2], 0)
    else:
        face = next(f for f in comp.bRepBodies.item(0).faces
                    if abs(f.pointOnFace.y - top_y) < 0.000001
                    and f.area > 100)
        sketch = comp.sketches.add(face)
        q = sketch.modelToSketchSpace(adsk.core.Point3D.create(*model_point))
    sketch.name = sketch_name
    circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
        q, 0.08 if diameter_name == 'base_m2_tap_pilot_d' else 0.115)
    center = circle.centerSketchPoint
    orient = adsk.fusion.DimensionOrientations
    x_mm = round(q.x * 10, 4)
    y_mm = round(q.y * 10, 4)
    if x_mm == 0 and y_mm == 0:
        sketch.geometricConstraints.addCoincident(center, sketch.originPoint)
    else:
        if x_mm == 0:
            sketch.geometricConstraints.addVerticalPoints(
                sketch.originPoint, center)
        else:
            sketch.sketchDimensions.addDistanceDimension(
                sketch.originPoint, center,
                orient.HorizontalDimensionOrientation,
                adsk.core.Point3D.create(q.x / 2, q.y + 0.5, 0),
            ).parameter.expression = str(abs(x_mm)) + ' mm'
        if y_mm == 0:
            sketch.geometricConstraints.addHorizontalPoints(
                sketch.originPoint, center)
        else:
            sketch.sketchDimensions.addDistanceDimension(
                sketch.originPoint, center,
                orient.VerticalDimensionOrientation,
                adsk.core.Point3D.create(q.x + 0.5, q.y / 2, 0),
            ).parameter.expression = str(abs(y_mm)) + ' mm'
    sketch.sketchDimensions.addDiameterDimension(
        circle, adsk.core.Point3D.create(q.x + 0.5, q.y + 0.5, 0)
    ).parameter.expression = diameter_name
    assert sketch.isFullyConstrained, sketch_name
    target_area = 0.0201 if diameter_name == 'base_m2_tap_pilot_d' else 0.04155
    profiles = adsk.core.ObjectCollection.create()
    for j in range(sketch.profiles.count):
        p = sketch.profiles.item(j)
        props = p.areaProperties()
        if (abs(props.area - target_area) < 0.002
                and abs(props.centroid.x - q.x) < 0.005
                and abs(props.centroid.y - q.y) < 0.005):
            profiles.add(p)
    assert profiles.count == 1, (sketch_name, profiles.count)
    feat = comp.features.extrudeFeatures.addSimple(
        profiles, adsk.core.ValueInput.createByString(depth_expr),
        adsk.fusion.FeatureOperations.CutFeatureOperation)
    feat.name = 'CUT-' + sketch_name


def run(_context: str):
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    dimension(d, 'base_m2_tap_pilot_d', '1.6 mm',
              'Pilot for M2 rail screw tapped into aluminum base')
    dimension(d, 'base_m2_tap_depth', '4 mm',
              'Blind M2 rail screw thread depth in base')
    frame = find_child(d.rootComponent, '10_FRAME').component
    shim = find_child(frame, 'CBP-1300_X_RAIL_ALIGNMENT_SHIM').component
    base = find_child(frame, 'CBP-1100_BASE_PLATE').component
    for i, x_mm in enumerate(range(-60, 61, 15), 1):
        _single_hole(shim, 'SK-1300-02_RAIL_CLEAR_' + str(i).zfill(2),
                     (x_mm / 10, 0, 0), 'mgn7_rail_hole_d',
                     'x_shim_t')
        for side, suffix in [(-1, 'A'), (1, 'B')]:
            _single_hole(
                base,
                'SK-1100-04_M2_RAIL_TAP_' + suffix + str(i).zfill(2),
                (x_mm / 10, 1.2, side * 6),
                'base_m2_tap_pilot_d',
                '-base_m2_tap_depth', top_y=1.2)
    print('shim cm3', shim.bRepBodies.item(0).volume,
          'base cm3', base.bRepBodies.item(0).volume)
