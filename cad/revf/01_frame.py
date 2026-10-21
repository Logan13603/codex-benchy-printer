"""RevF HFS5 extrusion frame. Read common.py first.

280 × 280 × 300 mm frame, 2020 posts and crossmembers, 2040 upper
Y rail carriers. Mounting slots are dimensioned simplified HFS5 interfaces;
small root reliefs/diagonal internal voids and R1 corners are omitted.
Use catalog mass and inertia, not proxy solid volume, for engineering.
"""


def slot_polygon(c,name,length,points):
    s=c.sketches.add(c.xYConstructionPlane);s.name='SK-'+name
    # Supplier-owned cross-section is intentionally immutable reference
    # geometry. Custom manufactured parts never use this fixing route.
    initial=[adsk.core.Point3D.create(x/10,y/10,0) for x,y in points]
    lines=[]
    for i in range(len(initial)):
        start=initial[0] if i==0 else lines[-1].endSketchPoint
        end=lines[0].startSketchPoint if i==len(initial)-1 else initial[i+1]
        lines.append(s.sketchCurves.sketchLines.addByTwoPoints(start,end))
    for line in lines:line.isFixed=True
    adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct).computeAll()
    assert s.isFullyConstrained,name
    extrude(c,s,length,adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-'+name)


def profile(c,name,width,depth,length,wide=False):
    box(c,name,width,depth,length)
    # The true cavity tapers45deg; rectangular cavities would sever the
    # diagonal webs. Small corner radii and120deg root relief are omitted.
    base=[(-3,12),(-3,8),(-6,8),(-6,7),(-3,4),(3,4),(6,7),(6,8),(3,8),(3,12)]
    height=40 if wide else 20
    for side,suffix in [(-1,'B'),(1,'T')]:
        pts=[(x,side*(y+height/2-10)) for x,y in base]
        slot_polygon(c,name+'-'+suffix+'-TSLOT',length,pts)
    for side,suffix in [(-1,'L'),(1,'R')]:
        for i,offset in enumerate([-10,10] if wide else [0],1):
            pts=[(side*y,x+offset) for x,y in base]
            slot_polygon(c,name+'-'+suffix+str(i)+'-TSLOT',length,pts)
    for index,off in enumerate(['-10 mm','10 mm'] if wide else ['0 mm'],1):
        cut_circle(c,name+'-M5-END-BORE-'+str(index),'ex_bore_d',length,'0 mm',off)
    c.description='MISUMI HFS5 simplified mounting proxy; mass '+('0.88' if wide else '0.50')+' kg/m; mounting interface per official catalog.'
    assert c.bRepBodies.count==1,(name,c.bRepBodies.count)


def run(_context: str):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    assert 'RevF' in d.parentDocument.name
    for n,e,note in [
        ('frame_x','280 mm','Outer frame X'),('frame_y','280 mm','Outer frame Y'),
        ('frame_z','300 mm','Outer frame Z'),('ex20','20 mm','HFS5-2020 section'),
        ('ex40','40 mm','HFS5-2040 strong axis vertical'),
        ('frame_horiz_l','frame_x-2*ex20','Square crossmember cut length'),
        ('frame_x_l','frame_x','X crossmembers span over post ends'),
        ('frame_post_l','frame_z-2*ex20','Vertical post cut length'),
        ('slot_open','6 mm','HFS5 external slot opening'),
        ('slot_cavity','12 mm','HFS5 internal Tslot cavity width'),
        ('slot_depth','4 mm','HFS5 cavity depth below2mm lip'),
        ('ex_bore_d','4.2 mm','HFS5 center bore for M5 end tapping'),
        ('travel_x','80 mm','Usable print X'),('travel_y','60 mm','Usable print Y;10mmfrontfan-screwclearance'),
        ('travel_z','60 mm','Usable print Z'),('belt_w','9 mm','Owned belt width; pitch assumed GT2 pending inventory'),
        ('belt_pitch','2 mm','Provisional GT2 pitch'),('bed_size','100 mm','Z-only bed XY'),
        ('bed_t','4 mm','Aluminum bed thickness'),('gantry_z','280 mm','X beam/carriage force reference'),
        ('belt_a_z','284 mm','Lower belt force plane'),('belt_b_z','294 mm','Upper belt force plane'),
        ('nozzle_z','225 mm','Nominal nozzle/bed first-layer height'),('nozzle_y','-38 mm','Nozzle offset forward of beam'),
    ]:param(d,n,e,note)
    for name in ['10_FRAME','20_XY_MOTION','30_BED_Z','40_TOOLHEAD','50_CPAP_COOLING','60_ELECTRONICS','70_WIRING','80_FASTENERS']:
        group(d.rootComponent,name)
    frame=group(d.rootComponent,'10_FRAME').component
    a=part(frame,'CBP-F101_HFS5_2020_240',transform(-130,120,10,'Y'))
    if not a.component.bRepBodies.count:profile(a.component,'CBP-F101','ex20','ex20','frame_horiz_l')
    matrices=[transform(130,120,10,'Y')]
    if len([o for o in frame.occurrences if o.component==a.component])==1:
        for m in matrices:frame.occurrences.addExistingComponent(a.component,m)
    p=part(frame,'CBP-F102_HFS5_2020_260',transform(-130,-130,20))
    if not p.component.bRepBodies.count:profile(p.component,'CBP-F102','ex20','ex20','frame_post_l')
    if len([o for o in frame.occurrences if o.component==p.component])==1:
        for x,y in [(-130,130),(130,-130),(130,130)]:frame.occurrences.addExistingComponent(p.component,transform(x,y,20))
    b=part(frame,'CBP-F103_HFS5_2040_240',transform(-130,120,280,'Y'))
    if not b.component.bRepBodies.count:profile(b.component,'CBP-F103','ex20','ex40','frame_horiz_l',True)
    if len([o for o in frame.occurrences if o.component==b.component])==1:frame.occurrences.addExistingComponent(b.component,transform(130,120,280,'Y'))
    x=part(frame,'CBP-F104_HFS5_2020_280',transform(-140,-130,10,'X'))
    if not x.component.bRepBodies.count:profile(x.component,'CBP-F104','ex20','ex20','frame_x_l')
    if len([o for o in frame.occurrences if o.component==x.component])==1:
        for m in [transform(-140,130,10,'X'),transform(-140,-130,290,'X'),transform(-140,130,290,'X')]:frame.occurrences.addExistingComponent(x.component,m)
    print('frame instances',frame.occurrences.count)
    audit(d)
