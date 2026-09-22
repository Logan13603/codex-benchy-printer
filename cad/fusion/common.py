"""Shared Fusion CAD helpers. All geometry inputs use centimeters internally."""

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
    """Centered XZ sketch with four driving dimensions, then +Y extrusion."""
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
        sketch.originPoint, corner, orient.HorizontalDimensionOrientation,
        adsk.core.Point3D.create(half_width / 2, half_depth + 1, 0),
    ).parameter.expression = width + '/2'
    sketch.sketchDimensions.addDistanceDimension(
        sketch.originPoint, corner, orient.VerticalDimensionOrientation,
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


def dimension(design, name, expression, comment):
    existing = design.userParameters.itemByName(name)
    if existing:
        return existing
    return design.userParameters.add(
        name, adsk.core.ValueInput.createByString(expression), 'mm', comment)

