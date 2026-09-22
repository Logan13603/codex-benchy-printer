"""Replace overbroad first counterbore cut with annular-profile-only cut.

The first 06 script collected every sketch profile, including the outer rail
profile, and consequently removed the upper half of each rail. This repair
preserves the dimensioned sketches but cuts only the nine/seven annuli.
"""


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    motion = find_child(design.rootComponent, '20_XY_MOTION').component
    for name in ['CBP-P201_MGN7_X_RAIL_130_PROXY',
                 'CBP-P203_MGN7_Y_RAIL_110_PROXY']:
        comp = find_child(motion, name).component
        feature = comp.features.extrudeFeatures.itemByName(
            'CUT-MGN7-COUNTERBORES')
        assert feature
        assert feature.deleteMe()
        sketch = next(sk for sk in comp.sketches
                      if 'COUNTERBORES' in sk.name)
        profiles = adsk.core.ObjectCollection.create()
        for i in range(sketch.profiles.count):
            profile = sketch.profiles.item(i)
            if 0.08 < profile.areaProperties().area < 0.11:
                profiles.add(profile)
        expected = 9 if 'P201' in name else 7
        assert profiles.count == expected, profiles.count
        cut = comp.features.extrudeFeatures.addSimple(
            profiles,
            adsk.core.ValueInput.createByString('-mgn7_counterbore_depth'),
            adsk.fusion.FeatureOperations.CutFeatureOperation)
        cut.name = 'CUT-MGN7-COUNTERBORES'
        assert sketch.isFullyConstrained
        print(name, 'annular counterbores', profiles.count,
              'volume_cm3', comp.bRepBodies.item(0).volume)

