"""Add real MGN7 through-hole interfaces to the three rail proxy bodies.

Source: HIWIN Linear Guideway catalog, MGN7 rail: Ø2.3 mm through,
15 mm pitch, 7 × 4.8 mm rail section. The X rail has 5 mm end margins;
the custom 110 mm Y length uses 10 mm margins. Counterbores are next.
Read common.py before running this script.
"""


def _rail_holes(design, component, along_x, positions, sketch_name):
    if any(sk.name == sketch_name for sk in component.sketches):
        return
    sketch = component.sketches.add(component.xZConstructionPlane)
    sketch.name = sketch_name
    orient = adsk.fusion.DimensionOrientations
    for mm in positions:
        x = mm / 10 if along_x else 0
        z = 0 if along_x else mm / 10
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(x, z, 0), 0.115)
        center = circle.centerSketchPoint
        if mm == 0:
            sketch.geometricConstraints.addCoincident(center, sketch.originPoint)
        elif along_x:
            sketch.geometricConstraints.addHorizontalPoints(sketch.originPoint, center)
            sketch.sketchDimensions.addDistanceDimension(
                sketch.originPoint, center,
                orient.HorizontalDimensionOrientation,
                adsk.core.Point3D.create(x / 2, 0.5, 0),
            ).parameter.expression = str(abs(mm)) + ' mm'
        else:
            sketch.geometricConstraints.addVerticalPoints(sketch.originPoint, center)
            sketch.sketchDimensions.addDistanceDimension(
                sketch.originPoint, center,
                orient.VerticalDimensionOrientation,
                adsk.core.Point3D.create(0.5, z / 2, 0),
            ).parameter.expression = str(abs(mm)) + ' mm'
        sketch.sketchDimensions.addDiameterDimension(
            circle, adsk.core.Point3D.create(x + 0.5, z + 0.5, 0)
        ).parameter.expression = 'mgn7_rail_hole_d'
    assert sketch.isFullyConstrained, sketch_name
    assert sketch.profiles.count >= len(positions)
    profiles = adsk.core.ObjectCollection.create()
    for i in range(sketch.profiles.count):
        profiles.add(sketch.profiles.item(i))
    cut = component.features.extrudeFeatures.addSimple(
        profiles, adsk.core.ValueInput.createByString('mgn7_rail_h'),
        adsk.fusion.FeatureOperations.CutFeatureOperation)
    cut.name = 'CUT-MGN7-THROUGH-HOLES'
    print(component.name, 'holes', len(positions),
          'fully constrained', sketch.isFullyConstrained,
          'volume_cm3', component.bRepBodies.item(0).volume)


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    dimension(design, 'mgn7_rail_hole_d', '2.3 mm',
              'HIWIN MGN7 rail mounting through hole diameter')
    dimension(design, 'mgn7_rail_pitch', '15 mm',
              'HIWIN MGN7 rail mounting hole pitch')
    motion = find_child(design.rootComponent, '20_XY_MOTION').component
    x = find_child(motion, 'CBP-P201_MGN7_X_RAIL_130_PROXY').component
    y = find_child(motion, 'CBP-P203_MGN7_Y_RAIL_110_PROXY').component
    _rail_holes(design, x, True, list(range(-60, 61, 15)),
                'SK-P201-02_NINE_MGN7_MOUNT_HOLES')
    _rail_holes(design, y, False, list(range(-45, 46, 15)),
                'SK-P203-02_SEVEN_MGN7_MOUNT_HOLES')
