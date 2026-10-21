import adsk.core,adsk.fusion

def run(context):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    c=next(o.component for o in d.rootComponent.allOccurrences if o.component.name.startswith('CBP-F120_GUSSET'))
    s=c.sketches.item(0)
    p=s.sketchPoints.item(3);ref=s.sketchPoints.item(1)
    print('before',p.isFullyConstrained)
    s.geometricConstraints.addHorizontalPoints(ref,p)
    print('after',p.isFullyConstrained,'sketch',s.isFullyConstrained)
