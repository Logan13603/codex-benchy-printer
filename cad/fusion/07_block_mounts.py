"""Dimensioned MGN7H block mounting pilots in the two shared proxy models.

HIWIN MGN7H: four M2×2.5 blind holes on B=12 mm transverse and C=13 mm
longitudinal centers. These Ø1.6 pilots show the tap interface but do not
model threads or block raceways. Read common.py before running.
"""


def _block_pilots(component, positions, sketch_name):
    if any(s.name == sketch_name + '_01' for s in component.sketches):
        return
    orient = adsk.fusion.DimensionOrientations
    for index, (x_mm, z_mm) in enumerate(positions, 1):
        face = next(f for f in component.bRepBodies.item(0).faces
                    if abs(f.pointOnFace.y - 0.32) < 0.000001
                    and f.area > 4)
        sketch = component.sketches.add(face)
        sketch.name = sketch_name + '_' + str(index).zfill(2)
        q = sketch.modelToSketchSpace(adsk.core.Point3D.create(
            x_mm / 10, 0.32, z_mm / 10))
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            q, 0.08)
        center = circle.centerSketchPoint
        sketch.sketchDimensions.addDistanceDimension(
            sketch.originPoint, center,
            orient.HorizontalDimensionOrientation,
            adsk.core.Point3D.create(q.x / 2, q.y + 0.3, 0),
        ).parameter.expression = str(round(abs(q.x * 10), 4)) + ' mm'
        sketch.sketchDimensions.addDistanceDimension(
            sketch.originPoint, center,
            orient.VerticalDimensionOrientation,
            adsk.core.Point3D.create(q.x + 0.3, q.y / 2, 0),
        ).parameter.expression = str(round(abs(q.y * 10), 4)) + ' mm'
        sketch.sketchDimensions.addDiameterDimension(
            circle, adsk.core.Point3D.create(q.x + 0.3, q.y + 0.3, 0)
        ).parameter.expression = 'mgn7h_tap_pilot_d'
        assert sketch.isFullyConstrained, sketch.name
        profiles = adsk.core.ObjectCollection.create()
        for i in range(sketch.profiles.count):
            p = sketch.profiles.item(i)
            props = p.areaProperties()
            if (0.018 < props.area < 0.022
                    and abs(props.centroid.x - q.x) < 0.005
                    and abs(props.centroid.y - q.y) < 0.005):
                profiles.add(p)
        assert profiles.count == 1, [
            (round(sketch.profiles.item(i).areaProperties().area, 5),
             round(sketch.profiles.item(i).areaProperties().centroid.x, 3),
             round(sketch.profiles.item(i).areaProperties().centroid.y, 3),
             round(sketch.profiles.item(i).areaProperties().centroid.z, 3))
            for i in range(sketch.profiles.count)]
        cut = component.features.extrudeFeatures.addSimple(
            profiles, adsk.core.ValueInput.createByString(
                '-mgn7h_mount_thread_depth'),
            adsk.fusion.FeatureOperations.CutFeatureOperation)
        cut.name = 'CUT-MGN7H-M2-TAP-PILOT-' + str(index).zfill(2)
    print(component.name, 'four mounting pilots',
          'volume_cm3', component.bRepBodies.item(0).volume)


def run(_context: str):
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    dimension(d, 'mgn7h_tap_pilot_d', '1.6 mm',
              'Pilot for nominal M2 tap, simplified')
    dimension(d, 'mgn7h_mount_thread_depth', '2.5 mm',
              'HIWIN MGN7H block M2 thread depth')
    dimension(d, 'mgn7h_mount_B', '12 mm',
              'HIWIN MGN7H mounting transverse spacing')
    dimension(d, 'mgn7h_mount_C', '13 mm',
              'HIWIN MGN7H mounting longitudinal spacing')
    motion = find_child(d.rootComponent, '20_XY_MOTION').component
    x = find_child(motion, 'CBP-P202_MGN7H_X_BLOCK_PROXY').component
    y = find_child(motion, 'CBP-P204_MGN7H_Y_BLOCK_PROXY').component
    _block_pilots(x, [(sx*6.5, sz*6) for sx in [-1, 1]
                      for sz in [-1, 1]],
                  'SK-P202-02_FOUR_M2_PILOTS')
    _block_pilots(y, [(sx*6, sz*6.5) for sx in [-1, 1]
                      for sz in [-1, 1]],
                  'SK-P204-02_FOUR_M2_PILOTS')
