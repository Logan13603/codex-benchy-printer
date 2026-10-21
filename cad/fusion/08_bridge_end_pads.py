"""Thicken only the moving X-bridge ends to catch all MGN7H mount holes.

The previous constant 10 mm bridge was too narrow for the official 13 mm
longitudinal hole spacing. A monolithic 22 × 24 × 10 mm enlargement at each
end adds about 9 g at 1.6 g/cm³ while preserving the central 10 mm web.
These still need matching through holes and structural validation.
Read common.py before running.
"""


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    dimension(design, 'bridge_pad_w', '22 mm',
              'Monolithic bridge end pad width along X')
    dimension(design, 'bridge_pad_l', '24 mm',
              'Monolithic bridge end pad length along Y')
    motion = find_child(design.rootComponent, '20_XY_MOTION').component
    bridge = find_child(motion, 'CBP-2200_CARBON_X_BRIDGE').component
    orient = adsk.fusion.DimensionOrientations
    for side, suffix in [(-1, 'A'), (1, 'B')]:
        name = 'SK-2200-02_END_PAD_' + suffix
        if any(sk.name == name for sk in bridge.sketches):
            continue
        sketch = bridge.sketches.add(bridge.xZConstructionPlane)
        sketch.name = name
        lines = sketch.sketchCurves.sketchLines.addCenterPointRectangle(
            adsk.core.Point3D.create(0, side * 6.0, 0),
            adsk.core.Point3D.create(1.1, side * 7.2, 0))
        corner = lines.item(0).startSketchPoint
        sketch.sketchDimensions.addDistanceDimension(
            lines.item(0).startSketchPoint,
            lines.item(0).endSketchPoint,
            orient.HorizontalDimensionOrientation,
            adsk.core.Point3D.create(0, side * 8, 0),
        ).parameter.expression = 'bridge_pad_w'
        sketch.sketchDimensions.addDistanceDimension(
            lines.item(1).startSketchPoint,
            lines.item(1).endSketchPoint,
            orient.VerticalDimensionOrientation,
            adsk.core.Point3D.create(1.5, side * 6, 0),
        ).parameter.expression = 'bridge_pad_l'
        sketch.sketchDimensions.addDistanceDimension(
            sketch.originPoint, corner,
            orient.HorizontalDimensionOrientation,
            adsk.core.Point3D.create(0.5, side * 8, 0),
        ).parameter.expression = 'bridge_pad_w/2'
        sketch.sketchDimensions.addDistanceDimension(
            sketch.originPoint, corner,
            orient.VerticalDimensionOrientation,
            adsk.core.Point3D.create(1.5, side * 4, 0),
        ).parameter.expression = 'x_rail_sep/2+bridge_pad_l/2'
        constraints = sketch.geometricConstraints
        constraints.addHorizontal(lines.item(0))
        constraints.addVertical(lines.item(1))
        constraints.addHorizontal(lines.item(2))
        constraints.addVertical(lines.item(3))
        assert sketch.isFullyConstrained, name
        feat = bridge.features.extrudeFeatures.addSimple(
            sketch.profiles.item(0),
            adsk.core.ValueInput.createByString('bridge_h'),
            adsk.fusion.FeatureOperations.JoinFeatureOperation)
        feat.name = 'JOIN-BRIDGE-END-PAD-' + suffix
    print('bridge body cm3', bridge.bRepBodies.item(0).volume,
          'sketches', bridge.sketches.count)
