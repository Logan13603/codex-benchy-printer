import adsk.core,adsk.fusion,json

def run(context):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    c=next(o.component for o in d.rootComponent.allOccurrences if o.component.name.startswith('CBP-F120_GUSSET'))
    for s in c.sketches:
        print('SK',s.name,'constraints',[(g.objectType) for g in s.geometricConstraints])
        print('points',[(p.geometry.asArray(),p.isFixed,p.isFullyConstrained) for p in s.sketchPoints])
        print('dims',[(q.parameter.name,q.parameter.expression) for q in s.sketchDimensions])
        print('directions',s.xDirection.asArray(),s.yDirection.asArray())
