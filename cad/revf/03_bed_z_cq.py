"""RevF Z mechanism in world-mm CadQuery geometry.

Detailed development geometry, not a production release. Supplied nut, motor
pilot, surface stack and screw-end runout remain explicit interface holds.
See engineering/REVF-FRAME-Z-MOUNTS.md. No Fusion geometry is overwritten.
"""
from pathlib import Path
import math
import cadquery as cq


def build():
    parts = []

    def add(name, shape, material, category='manufactured', notes='', moving=False):
        parts.append(dict(name=name, shape=shape, material=material,
                          category=category, notes=notes,
                          motion_group='bed_z' if moving else 'fixed'))
        return shape

    def box(w, d, h, x=0, y=0, z=0):
        return cq.Workplane('XY').box(w, d, h).translate((x, y, z))

    def cylinder(d, h, p, axis=(0, 0, 1)):
        return cq.Workplane(obj=cq.Solid.makeCylinder(d/2, h, cq.Vector(*p), cq.Vector(*axis)))

    def hole(shape, d, length, p, axis=(0, 0, 1)):
        return shape.cut(cylinder(d, length, p, axis))

    def slot(shape, x, y, z, length=4.5, width=3.5, angle=0, height=6):
        cutter = cq.Workplane('XY').center(x, y).slot2D(length, width, angle).extrude(height).translate((0, 0, z))
        return shape.cut(cutter)

    def washer(name, x, y, z, inner, outer, thick, moving=False):
        s = cylinder(outer, thick, (x, y, z)).cut(cylinder(inner, thick, (x, y, z)))
        add(name, s, 'steel', 'fastener', 'Dimensional washer proxy; weigh actual hardware.', moving)

    def zbolt(name, x, y, underhead, length, d=3, head_d=5.5, head_h=3, moving=False, direction=1):
        # Positive length runs from underside of head to tip along direction Z.
        s = cylinder(d, length, (x, y, underhead),(0,0,direction)).union(cylinder(head_d, head_h, (x, y, underhead),(0,0,-direction)))
        across_flats = {3: 2.5, 4: 3, 5: 4}[d]
        recess = cq.Workplane('XY').center(x, y).polygon(6, across_flats*2/math.sqrt(3)).extrude(direction*head_h*.75).translate((0, 0, underhead-direction*(head_h+.01)))
        s = s.cut(recess)
        add(name, s, 'steel', 'fastener', 'Socket screw envelope; threads omitted. Length is under-head length.', moving)

    def axisbolt(name,p,axis,length,d,moving=False):
        hd,hh,af={3:(5.5,3,2.5),4:(7,4,3),5:(8.5,5,4)}[d]
        head_start=tuple(p[i]-axis[i]*hh for i in range(3))
        s=cylinder(d,length,p,axis).union(cylinder(hd,hh,head_start,axis))
        free=tuple(head_start[i]-axis[i]*.01 for i in range(3))
        plane=cq.Plane(origin=free,normal=axis,xDir=(0,1,0) if abs(axis[0])>.5 else (1,0,0))
        recess=cq.Workplane(plane).polygon(6,af*2/math.sqrt(3)).extrude(hh*.75)
        add(name,s.cut(recess),'steel','fastener','ISO4762 mounting envelope; threads omitted; underhead length'+str(length)+'.',moving)

    def axiswasher(name,p,axis,inner,outer,thick,moving=False):
        s=cylinder(outer,thick,p,axis).cut(cylinder(inner,thick,p,axis))
        add(name,s,'steel','fastener','Flatwasher; actual purchased dimensions/tolerance check.',moving)

    def znut(name,x,y,z,d,af,h,moving=False):
        s=cq.Workplane('XY').center(x,y).polygon(6,af*2/math.sqrt(3)).extrude(h).translate((0,0,z))
        s=hole(s,2.5 if d==3 else 3.3,h,(x,y,z))
        add(name,s,'steel','fastener','Fullheight metric nut envelope; internal thread pilot displayed.',moving)

    # Exact HFS5 nominal exterior/slot interface; published mass overrides proxy.
    def extrusion2020(length):
        s = box(20, 20, length, z=length/2)
        base = [(-3,12),(-3,8),(-6,8),(-6,7),(-3,4),(3,4),(6,7),(6,8),(3,8),(3,12)]
        for turns in range(4):
            pts=[]
            for x,y in base:
                for _ in range(turns): x,y=-y,x
                pts.append((x,y))
            s = s.cut(cq.Workplane('XY').polyline(pts).close().extrude(length))
        return hole(s, 4.2, length, (0,0,0))

    for side in [-1, 1]:
        hand = 'L' if side < 0 else 'R'
        add('CBP-F105_Z_GUIDE_POST_'+hand, extrusion2020(240).translate((side*130,-38,20)),
            'A6N01SS-T5', 'purchased', 'HFS5-2020 cut240, M5 end taps. Maker mass120g each; small radii omitted.')
        parts[-1]['mass_override_g']=120
        # Rail adapter: 240 along Z, 20 along Y, 4 along X.
        adapter=box(4,20,240,side*118,-38,140)
        start_x=side*120
        axis=(-side,0,0)
        for z in range(55,236,20): adapter=hole(adapter,2.5,4,(start_x,-38,z),axis)
        for z in [30,255]: adapter=hole(adapter,5.5,4,(start_x,-38,z),axis)
        add('CBP-Z301_RAIL_ADAPTER_'+hand,adapter,'6061-T6',notes='240x20x4. Ten M3 through taps, two M5 end anchors. Datum side faces require flattening/shimming.')
        rail=box(6.5,9,200,side*112.75,-38,145)
        for z in range(55,236,20):
            rail=hole(rail,3.5,6.5,(side*116,-38,z),axis)
            rail=hole(rail,6,3.5,(side*109.5,-38,z),(side,0,0))
        add('CBP-P301_MGN9_RAIL_200_'+hand,rail,'steel','purchased','HIWIN mounting proxy; raceways omitted. Ten holes,10mm end margins; source rail380g/m.')
        parts[-1]['mass_override_g']=76
        cap=box(3.5,20,39.9,side*107.75,-38,203)
        for y in [-45.5,-30.5]:
            for z in [195,211]:cap=hole(cap,2.5,3,(side*106,y,z),(side,0,0))
        add('CBP-P302_MGN9H_MOUNT_CAP_'+hand,cap,'steel','purchased','Mounting-cap proxy, not whole raceway. Override complete block mass26g.',True)
        parts[-1]['mass_override_g']=26
        sideplate=box(5,42,42,side*103.5,-38,203)
        for y in [-45.5,-30.5]:
            for z in [195,211]:sideplate=hole(sideplate,3.3,5,(side*106,y,z),(-side,0,0))
        for y in [-55,-21]:sideplate=hole(sideplate,4.4,5,(side*106,y,206.5),(-side,0,0))
        add('CBP-Z302_SIDE_PLATE_'+hand,sideplate,'6061-T6',notes='5x42x42, four M3 block holes, two M4 end-yoke holes. M3x8+0.5washer=2.5 thread engagement.',moving=True)

    yoke=box(202,50,6,0,-38,206.5)
    for x in [-42,42]:yoke=yoke.union(box(18,24,6,x,-75,206.5))
    yoke=yoke.union(box(40,88,6,0,31,206.5))
    yoke=yoke.edges('|Z').fillet(2)
    for x,w in [(-65,40),(0,26),(65,40)]:
        cutter=box(w,22,6,x,-38,206.5).edges('|Z').fillet(2)
        yoke=yoke.cut(cutter)
    yoke=hole(yoke,3.5,6,(-42,-80,203.5))
    yoke=slot(yoke,42,-80,203.5,angle=0)
    yoke=slot(yoke,0,4,203.5,angle=90)
    for side in [-1,1]:
        for y in [-55,-21]:yoke=hole(yoke,3.3,7,(side*101,y,206.5),(-side,0,0))
        # Upper MGN block screw heads and OD7 washers project into the fork's
        # end region. Scallop it rather than hiding a hardware collision.
        for y in [-45.5,-30.5]:yoke=hole(yoke,8,4,(side*101,y,211),(-side,0,0))
    # Nut cassette's four retaining bolts and body relief; nut dimensions HOLD.
    for x in [-16,16]:
        for y in [43,67]:yoke=hole(yoke,2.5,6,(x,y,203.5))
    yoke=hole(yoke,14.5,6,(0,55,203.5))
    for y in [-10,20]:yoke=hole(yoke,3.3,6,(0,y,203.5))
    add('CBP-Z303_BED_FORK_YOKE',yoke,'6061-T6',notes='6mm single plate. End M4 taps7deep; three-point leveling round/Xslot/Yslot. Cassette bore14.5 provisional.',moving=True)

    bed=box(100,100,4,0,-38,222)
    supports=[(-42,-80),(42,-80),(0,4)]
    for x,y in supports:bed=hole(bed,2.5,4,(x,y,220))
    add('CBP-Z304_AL_BED_100',bed,'aluminum tooling plate',notes='100x100x4. M3 through taps; first-layer surface is225 after actual measured print stack.',moving=True)
    add('CBP-P303_MAGNET_STACK_ALLOWANCE',box(100,100,.6,0,-38,224.3),'magnetic sheet','purchased','0.6mm planning allowance, exact vendor stack not frozen.',True)
    add('CBP-P304_STEEL_PEI_STACK_ALLOWANCE',box(100,100,.4,0,-38,224.8),'spring steel / PEI','purchased','0.4mm planning allowance; do not infer actual surface mass from single material.',True)
    for i,(x,y) in enumerate(supports,1):
        spacer=cylinder(16,10.5,(x,y,209.5)).cut(cylinder(4,10.5,(x,y,209.5)))
        add('CBP-Z305_SILICONE_SPACER_'+str(i),spacer,'silicone','purchased','12mm free,10.5mm compressed nominal. Hardness/preload unverified.',True)
        parts[-1]['mass_override_g']=math.pi*(16**2-4**2)/4*12*1.15/1000
        zbolt('CBP-H301_LEVEL_M3X20_'+str(i),x,y,203,20,moving=True)
        washer('CBP-H302_LEVEL_WASHER_'+str(i),x,y,203,3.2,7,.5,True)

    bridge=box(270,80,6,0,55,23)
    bridge=bridge.cut(box(44,44,6,0,55,23).edges('|Z').fillet(2))
    for x in [-130,130]:
        for y in [30,80]:bridge=hole(bridge,5.5,6,(x,y,20))
    for x in [-28,28]:
        for y in [27,83]:bridge=hole(bridge,4.4,6,(x,y,20))
    add('CBP-Z306_Z_MOTOR_BRIDGE',bridge,'6061-T6',notes='270x80x6,body aperture44 withR2corners. Four M5 frame anchors, four M4 riser anchors.')
    # Lower3mm frame clears the whole motor body; upper3mm web sits ABOVE
    # motor face29, so no printed material is embedded in the motor body.
    riser=box(70,70,6,0,55,29)
    riser=riser.cut(box(44,44,3,0,55,27.5).edges('|Z').fillet(2))
    riser=hole(riser,24,3,(0,55,29))
    for x in [-15.5,15.5]:
        for y in [39.5,70.5]:riser=hole(riser,3.3,3,(x,y,29))
    for x in [-28,28]:
        for y in [27,83]:riser=hole(riser,4.4,6,(x,y,26))
    add('CBP-Z307_Z_MOTOR_RISER',riser,'PA-CF','printed','6mm stepped: lower3mm clears44square body, upper3mm pilot24 web. Pilot24 unverified. M3x6+0.5washer motor; M4x20 bridge anchors.')
    motor=box(42.3,42.3,26,0,55,16).edges('|Z').fillet(2.5)
    for x in [-15.5,15.5]:
        for y in [39.5,70.5]:motor=hole(motor,2.5,3,(x,y,29),(0,0,-1))
    add('CBP-P305_LDO_Z_MOTOR',motor,'motor assembly','purchased','42.3x42.3x26 envelope. Pilot omitted pending exact drawing. Maker motor+screw assembly150g; do not sum proxy densities.')
    add('CBP-P306_TR8X8_INTEGRATED_SCREW',cylinder(8,200,(0,55,29)),'steel','purchased','8mm nominal screw envelope,8mm lead/2mm pitch/four starts; thread and end-runout omitted. Paired withP305 mass.')

    angle=box(20,54,2,1,11,202.5).union(box(2,54,20,10,11,193.5))
    for y in [-10,20]:angle=hole(angle,3.3,2,(0,y,201.5))
    angle=hole(angle,9,2,(0,4,201.5))
    add('CBP-Z308_REAR_ARM_ANGLE',angle,'6061-T6',notes='20x20x2 aluminum angle,54long. Two M3 through bolts;9mm rear-leveling washer/head clearance. EndsY38 before cassette.',moving=True)

    cassette=box(40,32,12,0,55,215.5)
    cassette=hole(cassette,14.5,12,(0,55,209.5))
    cassette=cassette.cut(box(22,18,6,0,55,218.5))
    cover=box(40,32,2,0,55,222.5)
    cover=hole(cover,10,2,(0,55,221.5))
    for x in [-16,16]:
        for y in [43,67]:
            cassette=hole(cassette,3.4,12,(x,y,209.5))
            cover=hole(cover,3.4,2,(x,y,221.5))
    add('CBP-Z309_FLOATING_NUT_CASSETTE_HOLD',cassette,'PA-CF','printed','HOLD: flange/body dimensions unverified. Replace insert pocket from measured LDO nut; retain lateral float.',True)
    add('CBP-Z310_NUT_COVER_HOLD',cover,'PA-CF','printed','HOLD: actual nut flange must retain0.1-0.2axial,0.2-0.3lateral clearance; current geometry not release.',True)
    for i,(x,y) in enumerate([(x,y) for x in [-16,16] for y in [43,67]],1):
        zbolt('CBP-H303_CASSETTE_M3X20_'+str(i),x,y,224,20,moving=True,direction=-1)
        washer('CBP-H304_CASSETTE_WASHER_'+str(i),x,y,223.5,3.2,7,.5,True)

    # Complete standard-hardware envelopes for this Z subsystem. T-nut shape
    # is deliberately not invented: choose the exact5-series purchased nuts
    # and add their vendor geometry before production release.
    for side in [-1,1]:
        h='L' if side<0 else 'R'
        x=side*130
        axisbolt('CBP-H305_ZPOST_BOTTOM_M5X30_'+h,(x,-38,-1),(0,0,1),30,5)
        axiswasher('CBP-H306_ZPOST_BOTTOM_WASHER_'+h,(x,-38,-1),(0,0,1),5.3,10,1)
        axisbolt('CBP-H307_ZPOST_TOP_M5X50_'+h,(x,-38,301),(0,0,-1),50,5)
        axiswasher('CBP-H308_ZPOST_TOP_WASHER_'+h,(x,-38,300),(0,0,1),5.3,10,1)
        for j,z in enumerate([30,255],1):
            axisbolt('CBP-H309_ADAPTER_M5X10_'+h+str(j),(side*115,-38,z),(side,0,0),10,5)
            axiswasher('CBP-H310_ADAPTER_WASHER_'+h+str(j),(side*116,-38,z),(-side,0,0),5.3,10,1)
        for j,z in enumerate(range(55,236,20),1):
            axisbolt('CBP-H311_RAIL_M3X6_'+h+str(j),(side*113,-38,z),(side,0,0),6,3)
        j=0
        for y in [-45.5,-30.5]:
            for z in [195,211]:
                j+=1
                axisbolt('CBP-H312_BLOCK_M3X8_'+h+str(j),(side*100.5,y,z),(side,0,0),8,3,True)
                axiswasher('CBP-H313_BLOCK_WASHER_'+h+str(j),(side*101,y,z),(-side,0,0),3.2,7,.5,True)
        for j,y in enumerate([-55,-21],1):
            axisbolt('CBP-H314_YOKE_END_M4X12_'+h+str(j),(side*106.8,y,206.5),(-side,0,0),12,4,True)
            axiswasher('CBP-H315_YOKE_END_WASHER_'+h+str(j),(side*106,y,206.5),(side,0,0),4.3,9,.8,True)
    j=0
    for x in [-130,130]:
        for y in [30,80]:
            j+=1
            axisbolt('CBP-H316_BRIDGE_M5X12_'+str(j),(x,y,27),(0,0,-1),12,5)
            washer('CBP-H317_BRIDGE_WASHER_'+str(j),x,y,26,5.3,10,1)
    j=0
    for x in [-15.5,15.5]:
        for y in [39.5,70.5]:
            j+=1
            axisbolt('CBP-H318_ZMOTOR_M3X6_'+str(j),(x,y,32.5),(0,0,-1),6,3)
            washer('CBP-H319_ZMOTOR_WASHER_'+str(j),x,y,32,3.2,7,.5)
    j=0
    for x in [-28,28]:
        for y in [27,83]:
            j+=1
            axisbolt('CBP-H320_RISER_M4X20_'+str(j),(x,y,32.8),(0,0,-1),20,4)
            washer('CBP-H321_RISER_TOP_WASHER_'+str(j),x,y,32,4.3,9,.8)
            washer('CBP-H322_RISER_BOTTOM_WASHER_'+str(j),x,y,19.2,4.3,9,.8)
            znut('CBP-H323_RISER_M4_NUT_'+str(j),x,y,16,4,7,3.2)
    for j,y in enumerate([-10,20],1):
        axisbolt('CBP-H324_ARM_M3X16_'+str(j),(0,y,210),(0,0,-1),16,3,True)
        washer('CBP-H325_ARM_TOP_WASHER_'+str(j),0,y,209.5,3.2,7,.5,True)
        washer('CBP-H326_ARM_BOTTOM_WASHER_'+str(j),0,y,201,3.2,7,.5,True)
        znut('CBP-H327_ARM_M3_NUT_'+str(j),0,y,198.6,3,5.5,2.4,True)

    # Deliberately omit a fabricated nut solid: unverified geometry is a HOLD,
    # not a dimensionally accurate purchased model. Screw/cassette form is clear.
    mates={}
    for h in ['L','R']:
        for k in ['CBP-H305_ZPOST_BOTTOM_M5X30_','CBP-H307_ZPOST_TOP_M5X50_']:mates[k+h]='CBP-F105_Z_GUIDE_POST_'+h
        for i in range(1,11):mates['CBP-H311_RAIL_M3X6_'+h+str(i)]='CBP-Z301_RAIL_ADAPTER_'+h
        for i in range(1,5):mates['CBP-H312_BLOCK_M3X8_'+h+str(i)]='CBP-P302_MGN9H_MOUNT_CAP_'+h
        for i in range(1,3):mates['CBP-H314_YOKE_END_M4X12_'+h+str(i)]='CBP-Z303_BED_FORK_YOKE'
    for i in range(1,5):
        mates['CBP-H303_CASSETTE_M3X20_'+str(i)]='CBP-Z303_BED_FORK_YOKE'
        mates['CBP-H318_ZMOTOR_M3X6_'+str(i)]='CBP-P305_LDO_Z_MOTOR'
        mates['CBP-H320_RISER_M4X20_'+str(i)]='CBP-H323_RISER_M4_NUT_'+str(i)
    for i in range(1,4):mates['CBP-H301_LEVEL_M3X20_'+str(i)]='CBP-Z304_AL_BED_100'
    for i in range(1,3):mates['CBP-H324_ARM_M3X16_'+str(i)]='CBP-H327_ARM_M3_NUT_'+str(i)
    for p in parts:
        if p['name'] in mates:p['intentional_thread_mate']=mates[p['name']]
    return parts


if __name__ == '__main__':
    import json
    from cq_common import exportAssembly, interference
    folder=Path(__file__).parent/'exports'/'bed_z'
    parts=build()
    exportAssembly(parts,folder,'CBP_RevF_Bed_Z_DEVELOPMENT')
    checks=[]
    expected={frozenset((p['name'],p['intentional_thread_mate'])) for p in parts if 'intentional_thread_mate' in p}
    for travel in range(0,61,10):
        posed=[dict(p,shape=p['shape'].translate((0,0,-travel))) if p['motion_group']=='bed_z' else p for p in parts]
        raw=interference(posed,min_volume=.1,skip_categories=())
        hits=[h for h in raw if frozenset((h['a'],h['b'])) not in expected]
        checks.append({'bed_descent_mm':travel,'interferences':hits,
                       'intentional_thread_pairs':len(raw)-len(hits)})
    report={'status':'partial offline BRep clearance screen; not full printer acceptance',
            'excluded':'only exact named bolt/thread-mate overlaps; unmodeled nut, leads, stops, XY assembly and hose remain outside this subsystem screen',
            'volume_threshold_mm3':.1,'poses':checks}
    (folder/'CBP_RevF_Bed_Z_DEVELOPMENT-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
    assert all(not c['interferences'] for c in checks),report
