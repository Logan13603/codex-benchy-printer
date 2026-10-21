"""RevF side-guided Z/three-point bed, native parametric Fusion development CAD.

Execute after common.py in the RevF document. Custom geometry is dimensioned;
only the maker-owned extrusion section uses explicitly immutable reference
lines. Purchased rail raceways/threads are simplified. Nut/pilot/print-stack
interfaces marked HOLD must be measured before manufacturing release.
"""


def z_plate(c,name,width,depth,thickness,x='0 mm',y='0 mm',z='0 mm',join=False):
    p=None if abs(val(z))<1e-9 else plane_z(c,'PL-'+name,z)
    s=rect_sketch(c,'SK-'+name,width,depth,x,y,p)
    f=extrude(c,s,thickness,adsk.fusion.FeatureOperations.JoinFeatureOperation if join else adsk.fusion.FeatureOperations.NewBodyFeatureOperation,'EX-'+name)
    if not join:f.bodies.item(0).name=name
    return f


def z_cylinder(c,name,diameter,height,x='0 mm',y='0 mm',z='0 mm'):
    p=None if abs(val(z))<1e-9 else plane_z(c,'PL-'+name,z)
    s=circle_sketch(c,'SK-'+name,diameter,x,y,p)
    f=extrude(c,s,height,adsk.fusion.FeatureOperations.NewBodyFeatureOperation,'EX-'+name)
    f.bodies.item(0).name=name
    return f


def z_xbore(c,name,diameter,length,x,y,z):
    # Model coordinates of this component are world-mm for side plate/yoke.
    inp=c.constructionPlanes.createInput()
    base_sign=1 if c.yZConstructionPlane.geometry.normal.x>0 else -1
    assert inp.setByOffset(c.yZConstructionPlane,vi(str(x*base_sign)+' mm'))
    p=c.constructionPlanes.add(inp);p.name='PL-'+name
    s=c.sketches.add(p);s.name='SK-'+name
    pt=s.modelToSketchSpace(adsk.core.Point3D.create(x/10,y/10,z/10))
    cir=s.sketchCurves.sketchCircles.addByCenterRadius(pt,diameter/20)
    cp=cir.centerSketchPoint;ori=adsk.fusion.DimensionOrientations
    if abs(pt.x)<1e-9:s.geometricConstraints.addVerticalPoints(s.originPoint,cp)
    else:s.sketchDimensions.addDistanceDimension(s.originPoint,cp,ori.HorizontalDimensionOrientation,adsk.core.Point3D.create(pt.x/2,pt.y+.5,0)).parameter.expression=str(abs(pt.x*10))+' mm'
    if abs(pt.y)<1e-9:s.geometricConstraints.addHorizontalPoints(s.originPoint,cp)
    else:s.sketchDimensions.addDistanceDimension(s.originPoint,cp,ori.VerticalDimensionOrientation,adsk.core.Point3D.create(pt.x+.5,pt.y/2,0)).parameter.expression=str(abs(pt.y*10))+' mm'
    s.sketchDimensions.addDiameterDimension(cir,adsk.core.Point3D.create(pt.x+.5,pt.y+.5,0)).parameter.expression=str(diameter)+' mm'
    assert s.isFullyConstrained,name
    sign=1 if p.geometry.normal.x>0 else -1
    return extrude(c,s,str(sign*length)+' mm',adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-'+name)


def z_slot(c,name,x,y,z,along_x=True):
    # Native fully dimensioned capsule: two rounded ends plus joining web.
    for i,off in enumerate([-.5,.5],1):
        bore(c,name+'-END'+str(i),'3.5 mm','6 mm',str(x+(off if along_x else 0))+' mm',str(y+(0 if along_x else off))+' mm',str(z)+' mm')
    p=plane_z(c,'PL-'+name+'-WEB',str(z)+' mm')
    s=rect_sketch(c,'SK-'+name+'-WEB','1 mm' if along_x else '3.5 mm','3.5 mm' if along_x else '1 mm',str(x)+' mm',str(y)+' mm',p)
    extrude(c,s,'6 mm',adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-'+name+'-WEB')


def z_fillet_vertical(c,name,height,radius,points=None):
    edges=adsk.core.ObjectCollection.create()
    for e in c.bRepBodies.item(0).edges:
        a,b=e.startVertex.geometry,e.endVertex.geometry
        if abs(a.x-b.x)<1e-7 and abs(a.y-b.y)<1e-7 and abs(abs(a.z-b.z)-height/10)<1e-7:
            if points is None or any(abs(a.x*10-x)<1e-5 and abs(a.y*10-y)<1e-5 for x,y in points):edges.add(e)
    assert edges.count>0,name
    fi=c.features.filletFeatures.createInput()
    fi.addConstantRadiusEdgeSet(edges,vi(str(radius)+' mm'),True)
    ff=c.features.filletFeatures.add(fi);ff.name=name


def z_post_profile(c):
    box(c,'CBP-F105','20 mm','20 mm','z_post_l')
    base=[(-3,12),(-3,8),(-6,8),(-6,7),(-3,4),(3,4),(6,7),(6,8),(3,8),(3,12)]
    for turns in range(4):
        points=[]
        for x,y in base:
            for _ in range(turns):x,y=-y,x
            points.append((x,y))
        s=c.sketches.add(c.xYConstructionPlane);s.name='SK-SUPPLIER-HFS5-SECTION-'+str(turns)
        lines=[]
        for i,(x,y) in enumerate(points):
            a=adsk.core.Point3D.create(x/10,y/10,0) if i==0 else lines[-1].endSketchPoint
            b=lines[0].startSketchPoint if i==len(points)-1 else adsk.core.Point3D.create(points[i+1][0]/10,points[i+1][1]/10,0)
            lines.append(s.sketchCurves.sketchLines.addByTwoPoints(a,b))
        for line in lines:line.isFixed=True
        adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct).computeAll()
        assert s.isFullyConstrained,s.name
        extrude(c,s,'z_post_l',adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-SUPPLIER-SLOT-'+str(turns))
    cut_circle(c,'CENTER-BORE-M5-TAP-REF','4.2 mm','z_post_l')
    c.description='HFS5-2020 purchased profile240mm, maker mass120g, M5 useful thread12mm at both ends. Fixed supplier section only; never custom-part fixing.'


def z_rail(c):
    box(c,'CBP-P301','200 mm','9 mm','6.5 mm')
    for i in range(10):
        x=-90+i*20
        bore(c,'RAIL-THRU-'+str(i),'3.5 mm','6.5 mm',str(x)+' mm')
        bore(c,'RAIL-COUNTERBORE-'+str(i),'6 mm','3.5 mm',str(x)+' mm',z='3 mm')
    c.description='MGN9 rail200mm, ten20mm pitch holes,10mm end margins. Purchased raceway omitted; mass76g. Confirm actual hole margins.'


def run(_context: str):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    assert 'RevF' in d.parentDocument.name
    assembly=group(d.rootComponent,'30_BED_Z').component
    assert assembly.occurrences.count==0,'30_BED_Z must be empty before a fresh build; preserve/review existing work first.'
    fixed=group(assembly,'31_Z_FIXED').component
    moving=group(assembly,'32_Z_MOVING').component
    for n,e,note in [
        ('z_post_l','240 mm','Additional side-guide posts'),
        ('z_rail_l','200 mm','MGN9 vertical rails with10mm hole end margin'),
        ('z_guide_y','-38 mm','Guide plane aligned with nominal bedCOM inY'),
        ('z_block_home','203 mm','First-layer guideblock center height'),
        ('z_yoke_t','6 mm','6061 fork plate thickness'),
        ('z_yoke_bottom','203.5 mm','Home yoke bottom'),
        ('z_bed_bottom','220 mm','Home aluminum plate bottom'),
        ('z_spacer_h','10.5 mm','Compressed12mm silicone tubes'),
        ('z_magnet_t','0.6 mm','HOLD exact magnetic adhesive stack'),
        ('z_surface_t','0.4 mm','HOLD exact springsteelPEI stack'),
        ('z_motor_face','29 mm','Integrated200mm screw mounting face'),
        ('z_nut_body_clearance','14.5 mm','HOLD measured nut body plus lateral float'),
        ('z_motor_pilot_clearance','24 mm','HOLD measured LDO pilot plus0.3mm'),
    ]:param(d,n,e,note)

    p=part(fixed,'CBP-F105_HFS5_2020_Z_POST_240',transform(-130,-38,20))
    if not p.component.bRepBodies.count:z_post_profile(p.component)
    fixed.occurrences.addExistingComponent(p.component,transform(130,-38,20))
    # Rail localX goes upZ,localY acrossY,localZ toward interior. Both right-handed.
    axleft=[(0,0,1),(0,-1,0),(1,0,0)]
    axright=[(0,0,1),(0,1,0),(-1,0,0)]
    a=part(fixed,'CBP-Z301_RAIL_ADAPTER_AL4',axes_transform(-120,-38,140,axleft))
    box(a.component,'CBP-Z301','240 mm','20 mm','4 mm')
    for z in range(55,236,20):bore(a.component,'RAIL-M3-TAP-'+str(z),'2.5 mm','4 mm',str(z-140)+' mm')
    for z in [30,255]:bore(a.component,'END-M5-'+str(z),'5.5 mm','4 mm',str(z-140)+' mm')
    fixed.occurrences.addExistingComponent(a.component,axes_transform(120,-38,140,axright))
    r=part(fixed,'CBP-P301_MGN9_Z_RAIL_200',axes_transform(-116,-38,145,axleft));z_rail(r.component)
    fixed.occurrences.addExistingComponent(r.component,axes_transform(116,-38,145,axright))
    cap=part(moving,'CBP-P302_MGN9H_Z_MOUNT_CAP',axes_transform(-109.5,-38,203,axleft))
    box(cap.component,'CBP-P302','39.9 mm','20 mm','3.5 mm')
    for z in [-8,8]:
        for y in [-7.5,7.5]:bore(cap.component,'M3-BLOCK-'+str(z)+'-'+str(y),'2.5 mm','3 mm',str(z)+' mm',str(y)+' mm',z='0.5 mm')
    cap.component.description='Mounting cap only; complete MGN9H block mass26g; full block envelope40.9long. MountthreadsM3x3deep.'
    moving.occurrences.addExistingComponent(cap.component,axes_transform(109.5,-38,203,axright))

    for side,hand in [(-1,'L'),(1,'R')]:
        c=part(moving,'CBP-Z302_SIDE_PLATE_'+hand).component
        z_plate(c,'CBP-Z302'+hand,'5 mm','42 mm','42 mm',str(side*103.5)+' mm','-38 mm','182 mm')
        for y in [-45.5,-30.5]:
            for z in [195,211]:z_xbore(c,'MGN-M3-'+str(y)+'-'+str(z),3.3,5,side*103.5-2.5,y,z)
        for y in [-55,-21]:z_xbore(c,'YOKE-M4-'+str(y),4.4,5,side*103.5-2.5,y,206.5)
        c.description='6061 5x42x42. M3x8+0.5washer gives2.5engagement. M4x12+0.8washer into fork gives6.2engagement.'
    c=part(moving,'CBP-Z303_BED_FORK_YOKE_AL6').component
    z_plate(c,'CBP-Z303-MAIN','202 mm','50 mm','z_yoke_t','0 mm','-38 mm','z_yoke_bottom')
    for x in [-42,42]:z_plate(c,'FRONT-FINGER-'+str(x),'18 mm','24 mm','z_yoke_t',str(x)+' mm','-75 mm','z_yoke_bottom',True)
    z_plate(c,'REAR-NUT-ARM','40 mm','88 mm','z_yoke_t','0 mm','31 mm','z_yoke_bottom',True)
    z_fillet_vertical(c,'FILLET-OUTLINE-R2',6,2)
    for x,w in [(-65,40),(0,26),(65,40)]:
        p=plane_z(c,'PL-WINDOW-'+str(x),'z_yoke_bottom')
        s=rect_sketch(c,'SK-WINDOW-'+str(x),str(w)+' mm','22 mm',str(x)+' mm','-38 mm',p)
        extrude(c,s,'z_yoke_t',adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-WINDOW-'+str(x))
    # Round the twelve window corners, before slots/circular holes add seam edges.
    wanted=[(x+dx,y) for x,w in [(-65,40),(0,26),(65,40)] for dx in [-w/2,w/2] for y in [-49,-27]]
    z_fillet_vertical(c,'FILLET-WINDOWS-R2',6,2,wanted)
    bore(c,'LEVEL-LEFT','3.5 mm','6 mm','-42 mm','-80 mm','z_yoke_bottom')
    z_slot(c,'LEVEL-RIGHT-X',42,-80,203.5,True);z_slot(c,'LEVEL-REAR-Y',0,4,203.5,False)
    for x in [-101,94]:
        for y in [-55,-21]:z_xbore(c,'M4-END-TAP-'+str(x)+'-'+str(y),3.3,7,x,y,206.5)
    for x in [-101,97]:
        for y in [-45.5,-30.5]:z_xbore(c,'BLOCK-HEAD-SCALLOP-'+str(x)+'-'+str(y),8,4,x,y,211)
    for x in [-16,16]:
        for y in [43,67]:bore(c,'CASSETTE-M3-TAP-'+str(x)+'-'+str(y),'2.5 mm','6 mm',str(x)+' mm',str(y)+' mm','z_yoke_bottom')
    bore(c,'NUT-BODY-HOLD','z_nut_body_clearance','6 mm','0 mm','55 mm','z_yoke_bottom')
    for y in [-10,20]:bore(c,'ANGLE-M3-'+str(y),'3.3 mm','6 mm','0 mm',str(y)+' mm','z_yoke_bottom')
    c.description='Single6mm6061 fork. M4end taps7deep need jig. NutbodyclearanceHOLD; exactfloatcassetteunverified.'

    c=part(moving,'CBP-Z304_AL_BED_100').component
    z_plate(c,'CBP-Z304','100 mm','100 mm','4 mm','0 mm','-38 mm','z_bed_bottom')
    for x,y in [(-42,-80),(42,-80),(0,4)]:bore(c,'M3-LEVEL-TAP-'+str(x),'2.5 mm','4 mm',str(x)+' mm',str(y)+' mm','z_bed_bottom')
    c.description='Flat100x100x4aluminumtoolingplate. M3x20tipZ223 leaves1mm toAltop224. Fullfirstlayersurface225includesunfrozen1mmprintstack.'
    for name,z,h in [('CBP-P303_MAGNET_STACK_ALLOWANCE','224 mm','z_magnet_t'),('CBP-P304_STEEL_PEI_STACK_ALLOWANCE','224 mm+z_magnet_t','z_surface_t')]:
        c=part(moving,name).component;z_plate(c,name,'100 mm','100 mm',h,'0 mm','-38 mm',z)
        c.description='HOLD exact purchased stack; this dimensional allowance is not a sourced material mass.'
    for i,(x,y) in enumerate([(-42,-80),(42,-80),(0,4)],1):
        c=part(moving,'CBP-Z305_SILICONE_SPACER_'+str(i)).component
        z_cylinder(c,'CBP-Z305-'+str(i),'16 mm','z_spacer_h',str(x)+' mm',str(y)+' mm','209.5 mm')
        bore(c,'M3-CENTER','4 mm','z_spacer_h',str(x)+' mm',str(y)+' mm','209.5 mm')
        c.description='12mmfree,10.5compressednominal. Hardness/preloadunverified; boughtsiliconetube16OD4ID.'

    c=part(fixed,'CBP-Z306_Z_MOTOR_BRIDGE_AL6').component
    z_plate(c,'CBP-Z306','270 mm','80 mm','6 mm','0 mm','55 mm','20 mm')
    p=plane_z(c,'PL-MOTOR-BODY','20 mm');s=rect_sketch(c,'SK-MOTOR-BODY','44 mm','44 mm','0 mm','55 mm',p)
    extrude(c,s,'6 mm',adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-MOTOR-BODY')
    z_fillet_vertical(c,'FILLET-MOTOR-BODY-R2',6,2,[(x,y) for x in [-22,22] for y in [33,77]])
    for x in [-130,130]:
        for y in [30,80]:bore(c,'FRAME-M5-'+str(x)+'-'+str(y),'5.5 mm','6 mm',str(x)+' mm',str(y)+' mm','20 mm')
    for x in [-28,28]:
        for y in [27,83]:bore(c,'RISER-M4-'+str(x)+'-'+str(y),'4.4 mm','6 mm',str(x)+' mm',str(y)+' mm','20 mm')
    c.description='270x80x6 fixedbridge, M5x12+1washer5mmslotprojection. Motor44apertureR2corners.'
    c=part(fixed,'CBP-Z307_Z_MOTOR_RISER_HOLD').component
    z_plate(c,'CBP-Z307','70 mm','70 mm','6 mm','0 mm','55 mm','26 mm')
    p=plane_z(c,'PL-RISER-BODY','26 mm');s=rect_sketch(c,'SK-RISER-BODY','44 mm','44 mm','0 mm','55 mm',p)
    extrude(c,s,'3 mm',adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-RISER-BODY')
    z_fillet_vertical(c,'FILLET-RISER-BODY-R2',3,2,[(x,y) for x in [-22,22] for y in [33,77]])
    bore(c,'PILOT-HOLD','z_motor_pilot_clearance','3 mm','0 mm','55 mm','29 mm')
    for x in [-15.5,15.5]:
        for y in [39.5,70.5]:bore(c,'MOTOR-M3-'+str(x)+'-'+str(y),'3.3 mm','3 mm',str(x)+' mm',str(y)+' mm','29 mm')
    for x in [-28,28]:
        for y in [27,83]:bore(c,'BRIDGE-M4-'+str(x)+'-'+str(y),'4.4 mm','6 mm',str(x)+' mm',str(y)+' mm','26 mm')
    c.description='6mmsteppedPA-CF riser: lower3mmbodyclearance,upper3mmmountwebABOVEmotorface29. Pilot24HOLD. M3x6+0.5washer2.5engagement; bridgeM4x20.'
    c=part(fixed,'CBP-P305_LDO_Z_MOTOR_PROXY').component
    z_plate(c,'CBP-P305','42.3 mm','42.3 mm','26 mm','0 mm','55 mm','3 mm')
    for x in [-15.5,15.5]:
        for y in [39.5,70.5]:bore(c,'MOTOR-THREAD-'+str(x)+'-'+str(y),'2.5 mm','3 mm',str(x)+' mm',str(y)+' mm','26 mm')
    c.description='LDO42STH25integratedscrewproxy, mountpilot/connectorHOLD;26maxbody. Maker150gincludes200mmscrew, do not sumproxyweights.'
    c=part(fixed,'CBP-P306_TR8X8_SCREW_ENVELOPE').component
    z_cylinder(c,'CBP-P306','8 mm','200 mm','0 mm','55 mm','z_motor_face')
    c.description='PurchasedintegratedTr8x8P2fourstart;thread/runoutomitted. No upperrigidradialbearing.'

    c=part(moving,'CBP-Z308_REAR_ARM_ANGLE').component
    z_plate(c,'ANGLE-FOOT','20 mm','54 mm','2 mm','1 mm','11 mm','201.5 mm')
    z_plate(c,'ANGLE-WALL','2 mm','54 mm','20 mm','10 mm','11 mm','183.5 mm',True)
    for y in [-10,20]:bore(c,'M3-ANGLE-'+str(y),'3.3 mm','2 mm','0 mm',str(y)+' mm','201.5 mm')
    bore(c,'REAR-LEVEL-HEAD-CLEARANCE','9 mm','2 mm','0 mm','4 mm','201.5 mm')
    c.description='20x20x2Alangle54long, Y-16..38; endsbeforecassetteY39. Rearlevelheadclears9mmfootaperture.'
    for cover in [False,True]:
        c=part(moving,'CBP-Z310_NUT_COVER_HOLD' if cover else 'CBP-Z309_FLOATING_NUT_CASSETTE_HOLD').component
        z0='221.5 mm' if cover else '209.5 mm';h='2 mm' if cover else '12 mm'
        z_plate(c,'COVER' if cover else 'CASSETTE','40 mm','32 mm',h,'0 mm','55 mm',z0)
        bore(c,'BODY-HOLD','10 mm' if cover else 'z_nut_body_clearance',h,'0 mm','55 mm',z0)
        if not cover:
            p=plane_z(c,'PL-FLANGE-POCKET','215.5 mm');s=rect_sketch(c,'SK-FLANGE-POCKET','22 mm','18 mm','0 mm','55 mm',p)
            extrude(c,s,'6 mm',adsk.fusion.FeatureOperations.CutFeatureOperation,'CUT-FLANGE-POCKET-HOLD')
        for x in [-16,16]:
            for y in [43,67]:bore(c,'M3-CASSETTE-'+str(x)+'-'+str(y),'3.4 mm',h,str(x)+' mm',str(y)+' mm',z0)
        c.description='HOLD manufacture until actual suppliedLDO nutbody/flange/runoutmeasured. 0.2-0.3lateralfloatand0.1-0.2axialretentiontarget; no fabricatednutmodel.'
    audit(d)
    print('RevF Z developmentgeometrycomplete; nutpilotprintstackandfastenersweepstillHOLD.')
