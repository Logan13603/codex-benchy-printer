"""Fusion MCP CAD milestone 002: frame envelopes and lightweight stage.

Coordinates: Fusion X = machine X; Fusion -Z = machine Y; Fusion Y = machine Z.
Lengths passed to Fusion geometry are centimeters. Names and dimensions are
development geometry, not a manufacturing release.
"""

import adsk.core
import adsk.fusion


def moved(x_cm, y_cm, z_cm):
    matrix = adsk.core.Matrix3D.create()
    matrix.translation = adsk.core.Vector3D.create(x_cm, y_cm, z_cm)
    return matrix


def find_child(parent, name):
    for occurrence in parent.occurrences:
        if occurrence.component.name == name:
            return occurrence
    return None


def child(parent, name, location=(0, 0, 0)):
    existing = find_child(parent, name)
    if existing:
        return existing
    occurrence = parent.occurrences.addNewComponent(moved(*location))
    assert occurrence
    occurrence.component.name = name
    return occurrence


def constrained_box(component, sketch_name, body_name, width, depth, height):
    """Create a centered, dimensioned XZ sketch and extrude in Fusion +Y."""
    if component.bRepBodies.count:
        return component.bRepBodies.item(0)
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    half_width = design.userParameters.itemByName(width).value / 2
    half_depth = design.userParameters.itemByName(depth).value / 2
    sketch = component.sketches.add(component.xZConstructionPlane)
    sketch.name = sketch_name
    lines = sketch.sketchCurves.sketchLines.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(half_width, half_depth, 0),
    )
    orient = adsk.fusion.DimensionOrientations
    origin = sketch.originPoint
    corner = lines.item(0).startSketchPoint
    sketch.sketchDimensions.addDistanceDimension(
        lines.item(0).startSketchPoint, lines.item(0).endSketchPoint,
        orient.HorizontalDimensionOrientation,
        adsk.core.Point3D.create(0, half_depth + 1, 0),
    ).parameter.expression = width
    sketch.sketchDimensions.addDistanceDimension(
        lines.item(1).startSketchPoint, lines.item(1).endSketchPoint,
        orient.VerticalDimensionOrientation,
        adsk.core.Point3D.create(-half_width - 1, 0, 0),
    ).parameter.expression = depth
    sketch.sketchDimensions.addDistanceDimension(
        origin, corner, orient.HorizontalDimensionOrientation,
        adsk.core.Point3D.create(half_width / 2, half_depth + 1, 0),
    ).parameter.expression = width + '/2'
    sketch.sketchDimensions.addDistanceDimension(
        origin, corner, orient.VerticalDimensionOrientation,
        adsk.core.Point3D.create(half_width + 1, half_depth / 2, 0),
    ).parameter.expression = depth + '/2'
    constraints = sketch.geometricConstraints
    constraints.addHorizontal(lines.item(0))
    constraints.addVertical(lines.item(1))
    constraints.addHorizontal(lines.item(2))
    constraints.addVertical(lines.item(3))
    assert sketch.isFullyConstrained, sketch_name
    feature = component.features.extrudeFeatures.addSimple(
        sketch.profiles.item(0), adsk.core.ValueInput.createByString(height),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    assert feature, body_name
    feature.name = 'EX-' + body_name
    body = component.bRepBodies.item(0)
    body.name = body_name
    return body


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root = design.rootComponent
    frame = find_child(root, '10_FRAME').component

    # Structural envelopes: purchased 40 mm profile interfaces remain to be
    # measured; the solids provide station geometry and editable stock sizes.
    left = child(frame, 'CBP-1200_40MM_Z_COLUMN', (-16.0, 1.2, -15.0))
    constrained_box(left.component, 'SK-1200-01_COLUMN_SECTION',
                    'CBP-1200_COLUMN_ENVELOPE',
                    'tower_section', 'tower_section', 'tower_h')
    column_instances = [o for o in frame.occurrences
                        if o.component == left.component]
    if len(column_instances) == 1:
        frame.occurrences.addExistingComponent(
            left.component, moved(16.0, 1.2, -15.0))

    bridge = child(frame, 'CBP-1210_Z_CROSSBEAM_ENVELOPE',
                   (0, 25.2, -15.0))
    constrained_box(bridge.component, 'SK-1210-01_BEAM_SECTION',
                    'CBP-1210_CROSSBEAM_ENVELOPE',
                    'tower_span', 'tower_section', 'tower_section')

    motion = child(root, '20_XY_MOTION').component
    bed = child(root, '30_BED').component
    child(root, '40_Z_AXIS')
    child(root, '50_TOOLHEAD')
    child(root, '60_CPAP_COOLING')
    child(root, '70_ELECTRONICS')
    child(root, '80_HARNESS')

    stage = child(motion, 'CBP-2100_CARBON_XY_STAGE', (0, 8.0, 0))
    constrained_box(stage.component, 'SK-2100-01_STAGE_OUTLINE',
                    'CBP-2100_2MM_STAGE_STOCK',
                    'stage_x', 'stage_y', 'stage_t')
    substrate = child(bed, 'CBP-3100_BED_SUBSTRATE', (0, 8.2, 0))
    constrained_box(substrate.component, 'SK-3100-01_BED_OUTLINE',
                    'CBP-3100_BED_SUBSTRATE_STOCK',
                    'bed_x', 'bed_y', 'bed_t')
    surface = child(bed, 'CBP-3110_BUILD_SURFACE', (0, 8.5, 0))
    constrained_box(surface.component, 'SK-3110-01_SURFACE_OUTLINE',
                    'CBP-3110_BUILD_SURFACE_FILM',
                    'bed_x', 'bed_y', 'bed_surface_t')

    print('groups', [o.component.name for o in root.occurrences])
    print('frame members', [(o.component.name, o.transform2.translation.x,
                              o.transform2.translation.y,
                              o.transform2.translation.z)
                             for o in frame.occurrences])
    print('stage_mm', design.userParameters.itemByName('stage_x').value * 10,
          design.userParameters.itemByName('stage_y').value * 10,
          design.userParameters.itemByName('stage_t').value * 10)
