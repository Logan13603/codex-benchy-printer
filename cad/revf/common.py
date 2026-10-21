"""RevF Fusion API helpers. Local geometry in mm; Fusion internal cm.

All planar manufactured profiles use driving dimensions, never sketch fixing.
Purchased profile simplifications retain mounting interfaces; masses are
recorded separately from simplified geometric volumes.
"""
import adsk.core
import adsk.fusion
import math


def vi(expr):
    return adsk.core.ValueInput.createByString(str(expr))


def param(d, name, expression, note='', unit='mm'):
    p = d.userParameters.itemByName(name)
    if p:
        return p
    return d.userParameters.add(name, vi(expression), unit, note)


def val(expr):
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    return d.unitsManager.evaluateExpression(str(expr), 'mm')


def transform(x=0, y=0, z=0, axis='Z'):
    m = adsk.core.Matrix3D.create()
    origin = adsk.core.Point3D.create(x/10, y/10, z/10)
    if axis == 'X':
        axes = [(0,1,0),(0,0,1),(1,0,0)]
    elif axis == 'Y':
        axes = [(1,0,0),(0,0,1),(0,-1,0)]
    else:
        axes = [(1,0,0),(0,1,0),(0,0,1)]
    m.setWithCoordinateSystem(origin,*[adsk.core.Vector3D.create(*a) for a in axes])
    return m


def group(root, name):
    for o in root.occurrences:
        if o.component.name == name:
            return o
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = name
    return o


def part(parent, name, matrix=None):
    for o in parent.occurrences:
        if o.component.name == name:
            return o
    o = parent.occurrences.addNewComponent(matrix or adsk.core.Matrix3D.create())
    o.component.name = name
    o.component.partNumber = name.split('_')[0]
    return o


def rect_sketch(c, name, width, depth, cx='0 mm', cy='0 mm', plane=None):
    s = c.sketches.add(plane or c.xYConstructionPlane)
    s.name = name
    w,h,x,y = [val(e) for e in [width,depth,cx,cy]]
    sx = -1 if x < 0 else 1
    sy = -1 if y < 0 else 1
    ls = s.sketchCurves.sketchLines.addCenterPointRectangle(
        adsk.core.Point3D.create(x,y,0),
        adsk.core.Point3D.create(x+sx*w/2,y+sy*h/2,0))
    orient = adsk.fusion.DimensionOrientations
    corner = ls.item(0).startSketchPoint
    dims = s.sketchDimensions
    dims.addDistanceDimension(ls.item(0).startSketchPoint,ls.item(0).endSketchPoint,
        orient.HorizontalDimensionOrientation,adsk.core.Point3D.create(x,y+sy*(h/2+0.5),0)).parameter.expression = width
    dims.addDistanceDimension(ls.item(1).startSketchPoint,ls.item(1).endSketchPoint,
        orient.VerticalDimensionOrientation,adsk.core.Point3D.create(x+sx*(w/2+0.5),y,0)).parameter.expression = depth
    dims.addDistanceDimension(s.originPoint,corner,orient.HorizontalDimensionOrientation,
        adsk.core.Point3D.create(x/2,y+sy*(h/2+1),0)).parameter.expression = '('+width+')/2'+(' + ('+cx+')' if sx>0 else ' - ('+cx+')')
    dims.addDistanceDimension(s.originPoint,corner,orient.VerticalDimensionOrientation,
        adsk.core.Point3D.create(x+sx*(w/2+1),y/2,0)).parameter.expression = '('+depth+')/2'+(' + ('+cy+')' if sy>0 else ' - ('+cy+')')
    s.geometricConstraints.addHorizontal(ls.item(0))
    s.geometricConstraints.addVertical(ls.item(1))
    s.geometricConstraints.addHorizontal(ls.item(2))
    s.geometricConstraints.addVertical(ls.item(3))
    assert s.isFullyConstrained, name
    return s


def extrude(c,s,distance,op,name,profile=None):
    selected=profile or s.profiles.item(0)
    scoped=(adsk.fusion.FeatureOperations.CutFeatureOperation,adsk.fusion.FeatureOperations.IntersectFeatureOperation)
    if op in scoped:
        assert c.bRepBodies.count,'No owned target bodies for '+name
        inp=c.features.extrudeFeatures.createInput(selected,op)
        negative=val(distance)<0
        extent=adsk.fusion.DistanceExtentDefinition.create(vi('-('+str(distance)+')' if negative else distance))
        direction=adsk.fusion.ExtentDirections.NegativeExtentDirection if negative else adsk.fusion.ExtentDirections.PositiveExtentDirection
        assert inp.setOneSideExtent(extent,direction)
        inp.participantBodies=list(c.bRepBodies)
        f=c.features.extrudeFeatures.add(inp)
    else:
        f=c.features.extrudeFeatures.addSimple(selected,vi(distance),op)
    assert f,name
    assert all(b.parentComponent==c for b in f.bodies),'Feature escaped owning component: '+name
    f.name=name
    s.isVisible=False
    return f


def box(c,name,width,depth,height):
    s=rect_sketch(c,'SK-'+name+'-OUTLINE',width,depth)
    f=extrude(c,s,height,adsk.fusion.FeatureOperations.NewBodyFeatureOperation,'EX-'+name)
    b=f.bodies.item(0);b.name=name
    return b


def cut_rect(c,name,w,h,length,cx='0 mm',cy='0 mm'):
    s=rect_sketch(c,'SK-'+name,w,h,cx,cy)
    return extrude(c,s,length,adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-'+name)


def circle_sketch(c,name,diameter,x='0 mm',y='0 mm',plane=None):
    s=c.sketches.add(plane or c.xYConstructionPlane);s.name=name
    px,py=val(x),val(y)
    cir=s.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(px,py,0),val(diameter)/2)
    p=cir.centerSketchPoint;ori=adsk.fusion.DimensionOrientations
    if abs(px)<1e-9 and abs(py)<1e-9:s.geometricConstraints.addCoincident(p,s.originPoint)
    else:
        if abs(px)<1e-9:s.geometricConstraints.addVerticalPoints(s.originPoint,p)
        else:s.sketchDimensions.addDistanceDimension(s.originPoint,p,ori.HorizontalDimensionOrientation,adsk.core.Point3D.create(px/2,py+0.5,0)).parameter.expression=x.lstrip('-') if px<0 else x
        if abs(py)<1e-9:s.geometricConstraints.addHorizontalPoints(s.originPoint,p)
        else:s.sketchDimensions.addDistanceDimension(s.originPoint,p,ori.VerticalDimensionOrientation,adsk.core.Point3D.create(px+0.5,py/2,0)).parameter.expression=y.lstrip('-') if py<0 else y
    s.sketchDimensions.addDiameterDimension(cir,adsk.core.Point3D.create(px+0.5,py+0.5,0)).parameter.expression=diameter
    assert s.isFullyConstrained,name
    return s


def cut_circle(c,name,diameter,length,x='0 mm',y='0 mm'):
    s=circle_sketch(c,'SK-'+name,diameter,x,y)
    return extrude(c,s,length,adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-'+name)


def plane_z(c,name,offset):
    i=c.constructionPlanes.createInput()
    assert i.setByOffset(c.xYConstructionPlane,vi(offset))
    p=c.constructionPlanes.add(i);p.name=name
    return p


def bore(c,name,diameter,length,x='0 mm',y='0 mm',z='0 mm'):
    p=None if abs(val(z))<1e-9 else plane_z(c,'PL-'+name,z)
    s=circle_sketch(c,'SK-'+name,diameter,x,y,p)
    return extrude(c,s,length,adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-'+name)


def axes_transform(x,y,z,axes):
    m=adsk.core.Matrix3D.create()
    m.setWithCoordinateSystem(adsk.core.Point3D.create(x/10,y/10,z/10),
        *[adsk.core.Vector3D.create(*a) for a in axes])
    return m


def audit(d):
    seen=set();rows=[];bodies=0
    def walk(c):
        nonlocal bodies
        if c.entityToken in seen:return
        seen.add(c.entityToken)
        bodies+=c.bRepBodies.count
        for s in c.sketches:rows.append((c.name,s.name,s.isFullyConstrained))
        for o in c.occurrences:walk(o.component)
    walk(d.rootComponent)
    bad=[r for r in rows if not r[2]]
    print('AUDIT unique components',len(seen),'unique bodies',bodies,'unique sketches',len(rows),'unconstrained',bad,'params',d.userParameters.count,'timeline',d.timeline.count)
    assert not bad,bad
