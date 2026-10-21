"""Native parametric frame panels, gussets and feet. Load common + 04 helpers.

Purchased fasteners are individual world-coordinate STEP references exported
by 07_frame_bracing_cq.py. This builder must be executed and audited in Fusion.
"""
from pathlib import Path

def _f_round_edges(c,axis,length,radius,name):
    edges=adsk.core.ObjectCollection.create()
    for e in c.bRepBodies.item(0).edges:
        if not e.startVertex or not e.endVertex:continue
        a,b=e.startVertex.geometry,e.endVertex.geometry
        delta=[abs(getattr(a,k)-getattr(b,k)) for k in 'xyz']
        if abs(delta[axis]-length/10)<1e-6 and sum(delta)-delta[axis]<1e-6:edges.add(e)
    assert edges.count,name
    inp=c.features.filletFeatures.createInput()
    inp.addConstantRadiusEdgeSet(edges,vi(str(radius)+' mm'),True)
    c.features.filletFeatures.add(inp).name=name

def run(context):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeProduct)
    root=group(d.rootComponent,'11_FRAME_BRACING').component
    assert root.occurrences.count==0,'Preserve existing bracing before rebuilding'
    for n,e,note in [('rf_shear_t','1.5 mm','Aluminum side/rear shear panels'),
        ('rf_gusset_t','8 mm','Printed external corner gussets'),
        ('rf_foot_h','10 mm','Rigid frame stand height'),
        ('rf_foot_pad_t','2 mm','TPU friction pad; compliance unmeasured')]:param(d,n,e,note)
    op=adsk.fusion.FeatureOperations;new=op.NewBodyFeatureOperation;cut=op.CutFeatureOperation
    gusset_holes=[]
    for sy in [-1,1]:
        for top in [False,True]:
            z=300 if top else 0;iz=-1 if top else 1
            holes=[(sy*140-sy*u,z+iz*v) for u,v in [(10,30),(10,55),(30,10),(55,10)]]
            gusset_holes.extend(holes)
            for side in [-1,1]:
                label=('R' if side>0 else 'L')+('_REAR' if sy>0 else '_FRONT')+('_TOP' if top else '_BOTTOM')
                c=_new(root,'CBP-F120_GUSSET_'+label)
                x=side*141.5
                s=_poly(c,'GUSSET', (x,0,0),(side,0,0),[(x,sy*140,z),(x,sy*70,z),(x,sy*140,z+iz*70)])
                extrude(c,s,'rf_gusset_t',new,'EX-GUSSET')
                _f_round_edges(c,0,8,3,'FILLET-THREE-CORNERS-R3')
                for y,zz in holes:_cyl(c,'M5-'+str(y)+'-'+str(zz),5.5,8,(x,y,zz),(side,0,0),cut)
                c.description='PA-CF70mm triangle,8thick,R3 corners; four M5 mounts. Assembled creep/stiffness requires testing.'
    simple=[(0,10),(0,290)]+[(y,270) for y in [-90,0,90]]+[(y,z) for y in [-130,130] for z in [100,160,220]]
    for side in [-1,1]:
        c=_new(root,'CBP-F121_SIDE_SHEAR_PANEL_'+('L' if side<0 else 'R'))
        _box(c,'SIDE-PANEL','rf_shear_t',280,300,('('+str(side)+')*(140 mm+rf_shear_t/2)',0,150),new)
        for i,(y,z) in enumerate(simple+gusset_holes):_cyl(c,'M5-'+str(i),5.5,2,(side*140,y,z),(side,0,0),cut)
        c.description='280x300x1.5mm aluminum;27 holes. Match drill while frame square. Deburr edges.'
    c=_new(root,'CBP-F122_REAR_SHEAR_PANEL')
    _box(c,'REAR-PANEL',280,'rf_shear_t',300,(0,'140 mm+rf_shear_t/2',150),new)
    rearholes=[(x,z) for x in [-90,0,90] for z in [10,290]]+[(x,z) for x in [-130,130] for z in [50,110,190,250]]
    for x,z in rearholes:_cyl(c,'M5-'+str(x)+'-'+str(z),5.5,2,(x,140,z),(0,1,0),cut)
    for sx in [-1,1]:
        for sy in [-1,1]:
            label=str(sx)+'_'+str(sy);x,y=sx*115,sy*130
            c=_new(root,'CBP-F123_RIGID_FOOT_'+label)
            _box(c,'FOOT',50,28,'rf_foot_h',(x,y,'-rf_foot_h/2'),new)
            _f_round_edges(c,2,10,4,'FILLET-FOOT-R4')
            for n,diameter,length,start in [('ATTACH',5.5,10,(x,y,-10)),('HEAD',10.5,6,(x,y,-10)),('POST-HEAD',12,7,(sx*130,y,-7)),('POST-TOOL',8,10,(sx*130,y,-10))]:_cyl(c,n,diameter,length,start,(0,0,1),cut)
            c=_new(root,'CBP-F124_TPU_FOOT_PAD_'+label)
            _box(c,'PAD',50,28,'rf_foot_pad_t',(x,y,'-rf_foot_h-rf_foot_pad_t/2'),new)
            _f_round_edges(c,2,2,4,'FILLET-PAD-R4')
            for xx,diameter in [(x,5),(sx*130,8)]:_cyl(c,'ACCESS-'+str(xx),diameter,2,(xx,y,-12),(0,0,1),cut)
    folder=Path(__file__).resolve().parent/'exports'/'frame_bracing'
    for path in sorted(folder.glob('CBP-H*.step')):
        o=part(root,path.stem)
        assert app.importManager.importToTarget(app.importManager.createSTEPImportOptions(str(path)),o.component)
    audit(d)
    print('Native frame bracing complete; verify hardware imports and travel before release.')
