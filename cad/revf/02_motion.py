"""RevF Bowden CoreXY rail/beam interfaces. Execute after common.py.

Purchased rails use verified HIWIN mounting envelopes. Raceways are simplified.
Custom parts use dimension-driven sketches. Remaining belt joints and travel
validation are explicitly pending; this is a development checkpoint.
"""

def rail(c,name,length,width,height,pitch,count,thru,cbore,cbdepth):
    box(c,name,length,width,height)
    for i in range(count):
        x=(i-(count-1)/2)*pitch
        bore(c,name+'-H'+str(i+1),str(thru)+' mm',height,str(x)+' mm')
        bore(c,name+'-CB'+str(i+1),str(cbore)+' mm',str(cbdepth)+' mm',str(x)+' mm',z='('+height+')-'+str(cbdepth)+' mm')
    c.description='HIWIN purchased mounting proxy: exact envelope and hole pattern; raceways omitted; catalog mass separate.'

def block(c,name,length,width,thickness,bpitch,cpitch,diam,tapdepth):
    box(c,name,length,width,thickness)
    for x in [-cpitch/2,cpitch/2]:
        for y in [-bpitch/2,bpitch/2]:
            bore(c,name+'-MOUNT-'+str(x)+'-'+str(y),diam,tapdepth,
                str(x)+' mm',str(y)+' mm',z='('+thickness+')-('+tapdepth+')')
    c.description='Purchased block mounting cap only. Overall carriage envelope includes rail. Thread pilot shown; use specified nominal screws.'

def run(_context: str):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    assert 'RevF' in d.parentDocument.name
    for n,e,note in [
        ('y_rail_l','200 mm','MGN9 custom cut,10mm end margins'),
        ('x_rail_l','180 mm','MGN7 custom cut,7.5mm end margins'),
        ('rail_adapter_l','230 mm','Aluminum Y rail mounting strip'),
        ('rail_adapter_h','36 mm','Two extrusion slot rows at20mm pitch'),
        ('rail_adapter_t','4 mm','M3 tapped blind rail mounting'),
        ('x_beam_l','190 mm','Hollow carbon tube length'),
        ('x_beam_side','20 mm','Square tube section'),
        ('x_beam_wall','1.5 mm','Carbon wall nominal; verify actual stock'),
        ('socket_clear','20.3 mm','Printed carbon beam socket, tune coupon'),
        ('y_rail_face','116 mm','Distance from frame center to rail back face'),
        ('y_block_face','106 mm','MGN9H block mounting face'),
        ('y_end_l','31 mm','Beam socket20+11mm carriage plate'),
        ('x_strip_t','2 mm','Bonded aluminum threaded backing strip'),
    ]:param(d,n,e,note)
    motion=group(d.rootComponent,'20_XY_MOTION').component
    fixed=group(motion,'21_Y_RAILS_FIXED').component
    moving=group(motion,'22_Y_GANTRY').component
    # Local rail XYZ = length,section-width,depth. Left/right mirrored properly.
    left=[(0,1,0),(0,0,1),(1,0,0)]
    right=[(0,-1,0),(0,0,1),(-1,0,0)]
    a=part(fixed,'CBP-M201_Y_RAIL_ADAPTER_AL4',axes_transform(-120,0,280,left))
    box(a.component,'CBP-M201','rail_adapter_l','rail_adapter_h','rail_adapter_t')
    for x in [-90,-70,-50,-30,-10,10,30,50,70,90]:
        bore(a.component,'RAIL-M3-PILOT-'+str(x),'2.5 mm','rail_adapter_t',str(x)+' mm')
    for x in [-100,0,100]:
        for y in [-10,10]:bore(a.component,'TSLOT-M5-'+str(x)+'-'+str(y),'5.5 mm','rail_adapter_t',str(x)+' mm',str(y)+' mm')
    fixed.occurrences.addExistingComponent(a.component,axes_transform(120,0,280,right))
    r=part(fixed,'CBP-P201_MGN9_RAIL_200',axes_transform(-116,0,280,left))
    rail(r.component,'CBP-P201','y_rail_l','9 mm','6.5 mm',20,10,3.5,6,3.5)
    fixed.occurrences.addExistingComponent(r.component,axes_transform(116,0,280,right))
    b=part(moving,'CBP-P202_MGN9H_MOUNT_CAP',axes_transform(-109.5,0,280,left))
    block(b.component,'CBP-P202','39.9 mm','20 mm','3.5 mm',15,16,'2.5 mm','3 mm')
    moving.occurrences.addExistingComponent(b.component,axes_transform(109.5,0,280,right))
    beam=part(moving,'CBP-M202_CARBON_X_TUBE_190',transform(-95,0,280,'X'))
    box(beam.component,'CBP-M202','x_beam_side','x_beam_side','x_beam_l')
    cut_rect(beam.component,'HOLLOW','x_beam_side-2*x_beam_wall','x_beam_side-2*x_beam_wall','x_beam_l')
    # Sockets use localXY = globalYZ; both halves are independently named parts.
    for hand,x,ax in [('R',75,[(0,1,0),(0,0,1),(1,0,0)]),('L',-75,[(0,-1,0),(0,0,1),(-1,0,0)])]:
        e=part(moving,'CBP-M203'+hand+'_Y_END_SOCKET',axes_transform(x,0,280,ax))
        box(e.component,'CBP-M203'+hand,'44 mm','28 mm','y_end_l')
        cut_rect(e.component,'CARBON-SOCKET','socket_clear','socket_clear','20 mm')
        for u in [-8,8]:
            for v in [-7.5,7.5]:
                bore(e.component,'CARRIAGE-M3-'+str(u)+'-'+str(v),'3.3 mm','11 mm',str(u)+' mm',str(v)+' mm',z='20 mm')
                bore(e.component,'HEAD-ACCESS-'+str(u)+'-'+str(v),'6 mm','7 mm',str(u)+' mm',str(v)+' mm',z='20 mm')
        e.component.description='Printed socket draft; compression clamp split and nut traps pending. MGN9H15x16pitch. Do not manufacture before clamp completion.'
    xr=part(moving,'CBP-P203_MGN7_X_RAIL_180',axes_transform(0,-10,280,[(1,0,0),(0,0,1),(0,-1,0)]))
    rail(xr.component,'CBP-P203','x_rail_l','7 mm','4.8 mm',15,12,2.3,4.2,2.4)
    # Strip localY reversed to keep right-handed coordinate system.
    xs=part(moving,'CBP-M204_X_RAIL_THREAD_STRIP',axes_transform(0,-8.5,280,[(1,0,0),(0,0,-1),(0,1,0)]))
    box(xs.component,'CBP-M204','x_rail_l','8 mm','x_strip_t')
    for i in range(12):bore(xs.component,'M2-TAP-'+str(i+1),'1.6 mm','x_strip_t',str(-82.5+i*15)+' mm')
    xs.component.description='6061 backing strip bonded inside carbon tube, M2 through taps; bond prep and fastener lengths must be validated.'
    head=group(moving,'23_X_CARRIAGE').component
    xb=part(head,'CBP-P204_MGN7H_MOUNT_CAP',axes_transform(0,-14.8,280,[(1,0,0),(0,0,1),(0,-1,0)]))
    block(xb.component,'CBP-P204','30.8 mm','17 mm','3.2 mm',12,13,'1.6 mm','2.5 mm')
    audit(d)
