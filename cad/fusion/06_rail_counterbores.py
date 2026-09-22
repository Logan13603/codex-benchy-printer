"""Machine the MGN7 Ø4.2 × 2.4 mm counterbores from each rail top face.

Use after 05_rail_through_holes.py. The bought rails may have a supplier-specific
end-hole pattern; this model represents ordered/custom-cut lengths.
Read common.py before running.
"""


def _counterbores(component, positions, along_x, sketch_name):
    if any(sk.name == sketch_name for sk in component.sketches):
        return
    top = next(face for face in component.bRepBodies.item(0).faces
               if abs(face.pointOnFace.y - 0.48) < 0.000001
               and face.area > 5)
    sketch = component.sketches.add(top)
    sketch.name = sketch_name
    orient = adsk.fusion.DimensionOrientations
    for mm in positions:
        point = adsk.core.Point3D.create(
            mm / 10 if along_x else 0, 0.48,
            0 if along_x else mm / 10)
        q = sketch.modelToSketchSpace(point)
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            q, 0.21)
        center = circle.centerSketchPoint
        if mm == 0:
            sketch.geometricConstraints.addCoincident(center, sketch.originPoint)
        elif abs(q.x) > abs(q.y):
            sketch.geometricConstraints.addHorizontalPoints(sketch.originPoint,
                                                             center)
            sketch.sketchDimensions.addDistanceDimension(
                sketch.originPoint, center,
                orient.HorizontalDimensionOrientation,
                adsk.core.Point3D.create(q.x / 2, 0.5, 0),
            ).parameter.expression = str(abs(mm)) + ' mm'
        else:
            sketch.geometricConstraints.addVerticalPoints(sketch.originPoint,
                                                           center)
            sketch.sketchDimensions.addDistanceDimension(
                sketch.originPoint, center,
                orient.VerticalDimensionOrientation,
                adsk.core.Point3D.create(0.5, q.y / 2, 0),
            ).parameter.expression = str(abs(mm)) + ' mm'
        sketch.sketchDimensions.addDiameterDimension(
            circle, adsk.core.Point3D.create(q.x + 0.5, q.y + 0.5, 0)
        ).parameter.expression = 'mgn7_counterbore_d'
    assert sketch.isFullyConstrained, sketch_name
    profiles = adsk.core.ObjectCollection.create()
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        if 0.08 < profile.areaProperties().area < 0.11:
            profiles.add(profile)
    assert profiles.count == len(positions)
    cut = component.features.extrudeFeatures.addSimple(
        profiles, adsk.core.ValueInput.createByString('-mgn7_counterbore_depth'),
        adsk.fusion.FeatureOperations.CutFeatureOperation)
    cut.name = 'CUT-MGN7-COUNTERBORES'
    print(component.name, 'counterbores', len(positions),
          'profiles', profiles.count,
          'fully constrained', sketch.isFullyConstrained,
          'volume_cm3', component.bRepBodies.item(0).volume)


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    dimension(design, 'mgn7_counterbore_d', '4.2 mm',
              'HIWIN MGN7 rail counterbore diameter')
    dimension(design, 'mgn7_counterbore_depth', '2.4 mm',
              'HIWIN MGN7 rail counterbore depth from top')
    motion = find_child(design.rootComponent, '20_XY_MOTION').component
    x = find_child(motion, 'CBP-P201_MGN7_X_RAIL_130_PROXY').component
    y = find_child(motion, 'CBP-P203_MGN7_Y_RAIL_110_PROXY').component
    _counterbores(x, list(range(-60, 61, 15)), True,
                  'SK-P201-03_NINE_MGN7_COUNTERBORES')
    _counterbores(y, list(range(-45, 46, 15)), False,
                  'SK-P203-03_SEVEN_MGN7_COUNTERBORES')

