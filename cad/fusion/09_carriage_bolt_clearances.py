"""Drill bridge and stage for the MGN7H four-hole interface.

Ø2.2 mm simplified M2 clearance. Eight bridge holes attach two X blocks;
four stage holes attach the Y block. Sketches are individually dimensioned
because Fusion auto-infers redundant relations across symmetric circles.
Read common.py before running.
"""


def _through(component, positions, prefix, depth_expr):
    orient = adsk.fusion.DimensionOrientations
    for i, (x_mm, z_mm) in enumerate(positions, 1):
        name = prefix + '_' + str(i).zfill(2)
        if any(sk.name == name for sk in component.sketches):
            continue
        sketch = component.sketches.add(component.xZConstructionPlane)
        sketch.name = name
        x = x_mm / 10
        z = z_mm / 10
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(x, z, 0), 0.11)
        center = circle.centerSketchPoint
        if x_mm == 0 and z_mm == 0:
            sketch.geometricConstraints.addCoincident(center, sketch.originPoint)
        elif x_mm == 0:
            sketch.geometricConstraints.addVerticalPoints(
                sketch.originPoint, center)
            sketch.sketchDimensions.addDistanceDimension(
                sketch.originPoint, center,
                orient.VerticalDimensionOrientation,
                adsk.core.Point3D.create(0.5, z / 2, 0),
            ).parameter.expression = str(abs(z_mm)) + ' mm'
        else:
            sketch.sketchDimensions.addDistanceDimension(
                sketch.originPoint, center,
                orient.HorizontalDimensionOrientation,
                adsk.core.Point3D.create(x / 2, z + 0.5, 0),
            ).parameter.expression = str(abs(x_mm)) + ' mm'
            if z_mm == 0:
                sketch.geometricConstraints.addHorizontalPoints(
                    sketch.originPoint, center)
            else:
                sketch.sketchDimensions.addDistanceDimension(
                    sketch.originPoint, center,
                    orient.VerticalDimensionOrientation,
                    adsk.core.Point3D.create(x + 0.5, z / 2, 0),
                ).parameter.expression = str(abs(z_mm)) + ' mm'
        sketch.sketchDimensions.addDiameterDimension(
            circle, adsk.core.Point3D.create(x + 0.5, z + 0.5, 0)
        ).parameter.expression = 'm2_carriage_clearance_d'
        assert sketch.isFullyConstrained, name
        profiles = adsk.core.ObjectCollection.create()
        for j in range(sketch.profiles.count):
            p = sketch.profiles.item(j)
            props = p.areaProperties()
            if (0.036 < props.area < 0.040
                    and abs(props.centroid.x - x) < 0.005
                    and abs(props.centroid.y - z) < 0.005):
                profiles.add(p)
        assert profiles.count == 1, (name, profiles.count)
        cut = component.features.extrudeFeatures.addSimple(
            profiles, adsk.core.ValueInput.createByString(depth_expr),
            adsk.fusion.FeatureOperations.CutFeatureOperation)
        cut.name = 'CUT-M2-CARRIAGE-CLEAR-' + str(i).zfill(2)
    print(component.name, 'clearance holes', len(positions),
          'volume_cm3', component.bRepBodies.item(0).volume)


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    dimension(design, 'm2_carriage_clearance_d', '2.2 mm',
              'M2 clearance in bridge and stage')
    motion = find_child(design.rootComponent, '20_XY_MOTION').component
    bridge = find_child(motion, 'CBP-2200_CARBON_X_BRIDGE').component
    stage = find_child(motion, 'CBP-2100_CARBON_XY_STAGE').component
    bridge_pos = [(sx * 6.5, side * 60 + sz * 6)
                  for side in [-1, 1]
                  for sx in [-1, 1]
                  for sz in [-1, 1]]
    stage_pos = [(sx * 6, sz * 6.5)
                 for sx in [-1, 1] for sz in [-1, 1]]
    _through(bridge, bridge_pos, 'SK-2200-03_M2_XBLOCK_CLEAR',
             'bridge_h')
    _through(stage, stage_pos, 'SK-2100-02_M2_YBLOCK_CLEAR',
             'stage_t')
    _through(bridge, [(0, z) for z in range(-45, 46, 15)],
             'SK-2200-04_M2_YRAIL_CLEAR', 'bridge_h')

