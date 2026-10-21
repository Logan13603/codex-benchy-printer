"""Native constrained sketches/features for frozen RevF gantry supports.

Load common.py and the tested04_toolhead.py helper definitions first. Motor
plate native builder05 is independent. All custom support solids are built
with features; only purchased shafts/spacers and standard hardware importSTEP.
Source interfaces match frozen06_gantry_supports_cq.py. No custom sketch fix.
"""
import os
import json


_G6_BASE=r'C:\Users\logan\Documents\Codex\2026-09-20\this-will-take-multiple-trys-because-3\outputs\codex-benchy-printer\cad\revf'


def _g6_new(parent,name,notes):
    assert not any(o.component.name==name for o in parent.occurrences),'Already built '+name
    c=part(parent,name).component;c.partNumber=name;c.description=notes
    return c


def _g6_parameters(d):
    for n,e,note in [
        ('rf_drive_cx','88.75 mm','Frozen motor/moving-idler center X magnitude'),
        ('rf_drive_pitch_r','11.4591559026 mm','36T2mm pitch radius'),
        ('rf_drive_a_z','282.3 mm','A belt center plane'),
        ('rf_drive_b_z','269.3 mm','B belt center plane'),
        ('rf_drive_motor_offset','24.5 mm','Motor face below belt plane'),
        ('rf_cf_clamp_x','65 mm','Clamp center on150mm closed CF beam'),
        ('rf_gantry_fork_top','289.3 mm','Fork rib top/cap underside'),
        ('rf_gantry_portal_bottom','305 mm','Top portal underside clears returns'),
    ]:param(d,n,e,note)


def _g6_bore(c,name,dia,length,p,axis):
    return _cyl(c,name,dia,length,p,axis,adsk.fusion.FeatureOperations.CutFeatureOperation)


def _g6_adapter(parent,side,hand):
    op=adsk.fusion.FeatureOperations
    c=_g6_new(parent,'CBP-M205_'+hand+'_CARRIAGE_ADAPTER',
        'Native4mm6061,Z254..305. MGNcounterboresØ6x2.5 useM3x4,2.5mm thread. Head/belt nominal gap0.60mm requires tolerance check. ForkM3x6 lowerZ259/upper293; upperrearY-6.')
    _box(c,'ADAPTER',4,38,51,(side*104,0,279.5),op.NewBodyFeatureOperation)
    for y in [-8,8]:
        for z in [272.5,287.5]:
            _g6_bore(c,'MGN-THRU-'+str(y)+'-'+str(z),3.3,4,(side*102,y,z),(side,0,0))
            _g6_bore(c,'MGN-COUNTERBORE-'+str(y)+'-'+str(z),6,2.5,(side*102,y,z),(side,0,0))
    for y,z in [(-14,259),(14,259),(-6,293),(14,293)]:
        _g6_bore(c,'FORK-M3-TAP-'+str(y)+'-'+str(z),2.5,4,(side*102,y,z),(side,0,0))
    for y in [-10,10]:_g6_bore(c,'PORTAL-M3-TAP-'+str(y),2.5,4,(side*104,y,301),(0,0,1))
    return c


def _g6_clamp(parent,side,hand):
    op=adsk.fusion.FeatureOperations;cut=op.CutFeatureOperation
    c=_g6_new(parent,'CBP-M206_'+hand+'_SPLIT_BEAM_CLAMP',
        'Native printed clamp150mmclosedCF;20.3mm socket coupon required. Rail relief endsX70.5 leaving4.5mmweb. Heat inserts4.6x4 provisional. CrossclampsX60/70,Z298. No beam belt ports.')
    _box(c,'CLAMP-SHELL',20,28,28,(side*65,0,280),op.NewBodyFeatureOperation)
    _box(c,'CF-SOCKET',20.2,20.3,20.3,(side*65,0,280),cut)
    _box(c,'TOP-FLANGE',20,18,8,(side*65,0,298),op.JoinFeatureOperation)
    _box(c,'COMPRESSION-SPLIT',20.2,.8,22,(side*65,0,291.1),cut)
    _box(c,'RAIL-END-RELIEF',15.7,5.6,8,(side*62.65,-12.5,280),cut)
    for x in [60,70]:
        _g6_bore(c,'CROSSCLAMP-M3-'+str(x),3.3,18,(side*x,-9,298),(0,1,0))
        _hexcut(c,'CROSSCLAMP-NUT-'+str(x),5.7,2.6,(side*x,9,298),(0,-1,0))
    for y in [-5,5]:
        _g6_bore(c,'INSERT-'+str(y),4.6,4,(side*65,y,298),(0,0,1))
        _g6_bore(c,'SCREW-EXIT-'+str(y),3.3,4,(side*65,y,294),(0,0,1))
    return c


def _g6_fork(parent,side,hand):
    op=adsk.fusion.FeatureOperations;cut=op.CutFeatureOperation
    c=_g6_new(parent,'CBP-M208_'+hand+'_SEPARATE_IDLER_FORK',
        'Native fork, lower attachmentZ259,upper293/rearY-6. Outer belt windows and MGN head reliefs. Independent cap below portal; precision shaft/retention SKU remains HOLD.')
    _box(c,'CARRIAGE-PLATE',7,38,44,(side*98.5,0,276),op.NewBodyFeatureOperation)
    _box(c,'IDLER-BASE',18,33,6,(str(side)+'*rf_drive_cx',-28.5,260),op.JoinFeatureOperation)
    _box(c,'BACK-RIB',20,8,32.3,(side*92,-16,273.15),op.JoinFeatureOperation)
    _g6_bore(c,'SHAFT-LOWER',5.2,6,(str(side)+'*rf_drive_cx',-35,257),(0,0,1))
    for dx in [-6,6]:
        _g6_bore(c,'CAP-M3-TAP-'+str(dx),2.5,8,
                 (str(side)+'*(rf_drive_cx+('+str(dx)+' mm))',-16,281.3),(0,0,1))
    _box(c,'CAP-SERVICE-CLEARANCE',18.4,33.4,6.4,(str(side)+'*rf_drive_cx',-28.5,292.3),cut)
    for plane in ['rf_drive_a_z','rf_drive_b_z']:
        _box(c,'BELT-WINDOW-'+plane,3.2,40.4,10,(side*100.6,0,plane),cut)
    for y in [-8,8]:
        for z in [272.5,287.5]:_g6_bore(c,'MGN-HEAD-RELIEF-'+str(y)+'-'+str(z),6.5,7,(side*95,y,z),(side,0,0))
    _g6_bore(c,'REAR-LOWER-TOOL-ACCESS',6,24,(side*75,-14,259),(side,0,0))
    for y,z in [(-14,259),(14,259),(-6,293),(14,293)]:
        _g6_bore(c,'FORK-M3-'+str(y)+'-'+str(z),3.3,7,(side*95,y,z),(side,0,0))
        if (y,z)!=(-14,259):_g6_bore(c,'FORK-HEAD-'+str(y)+'-'+str(z),6,4,(side*95,y,z),(side,0,0))
    return c


def _g6_cap(parent,side,hand):
    op=adsk.fusion.FeatureOperations
    c=_g6_new(parent,'CBP-M207_'+hand+'_REMOVABLE_IDLER_CAP',
        'Native cap18x33x6,Z289.3..295.3. TwoM3x10 heads recessed3mm flush;7mm thread engagement in8mm tap; actual shaft retention HOLD.')
    _box(c,'CAP',18,33,6,(str(side)+'*rf_drive_cx',-28.5,292.3),op.NewBodyFeatureOperation)
    _g6_bore(c,'SHAFT-UPPER',5.2,6,(str(side)+'*rf_drive_cx',-35,289.3),(0,0,1))
    for dx in [-6,6]:
        x=str(side)+'*(rf_drive_cx+('+str(dx)+' mm))'
        _g6_bore(c,'M3-'+str(dx),3.3,6,(x,-16,289.3),(0,0,1))
        _g6_bore(c,'HEAD-'+str(dx),6,3,(x,-16,292.3),(0,0,1))
    return c


def _g6_portal(parent,side,hand):
    op=adsk.fusion.FeatureOperations
    c=_g6_new(parent,'CBP-M209_'+hand+'_AL_PORTAL_BRIDGE',
        'Native50x38x4,X60..110. Outer M3 hole has6mmedgedistance. Z305..309;2M3x8intoAladapter,2M3x12through3mmspacersintoclamp inserts with0.5washers.')
    _box(c,'PORTAL',50,38,4,(side*85,0,307),op.NewBodyFeatureOperation)
    for y in [-10,10]:_g6_bore(c,'ADAPTER-M3-'+str(y),3.3,4,(side*104,y,305),(0,0,1))
    for y in [-5,5]:_g6_bore(c,'CLAMP-M3-'+str(y),3.3,4,(side*65,y,305),(0,0,1))
    return c


def _g6_hanger(parent,axis,k,x,y,face):
    op=adsk.fusion.FeatureOperations;cut=op.CutFeatureOperation
    sy=130 if y>0 else -130;sx=1 if x>0 else -1
    c=_g6_new(parent,'CBP-D402_'+axis+'_FRAME_HANGER_'+str(k),
        'Native printed motorhanger DEVELOPMENT. Rail/idler and motorhead keepouts; A-front upperinnerwall island omitted explicitly. Remaining webs, hotmotorcreep/cyclicstiffness unvalidated. Fit motor/plate before hanging due frontcap tool obstruction.')
    _box(c,'FRAME-TOP',45,20,7,(x,sy,276.5),op.NewBodyFeatureOperation)
    y0=min(y-31,sy-10);y1=max(y+31,sy+10)
    for dx in [-20,20]:
        _box(c,'WALL-'+str(dx),5,y1-y0,280-(face-6),
             (x+dx,(y0+y1)/2,(face-6+280)/2),op.JoinFeatureOperation)
    # Cut the walls before adding the feet: sourceCQ limits these two tools
    # to walls, so this order preserves the complete bearing faces of feet.
    _box(c,'MOTOR-BODY-CLEARANCE',43,43,60,(x,y,face-30),cut)
    _box(c,'MOTOR-PLATE-CLEARANCE',45.1,64.1,6.1,(x,y,face+3),cut)
    for dy in [-27,27]:
        _box(c,'PLATE-FOOT-'+str(dy),42,8,6,(x,y+dy,face-3),op.JoinFeatureOperation)
        for dx in [-17,17]:
            _g6_bore(c,'M4-'+str(dx)+'-'+str(dy),4.4,6,(x+dx,y+dy,face-6),(0,0,1))
            _hexcut(c,'M4-NUT-'+str(dx)+'-'+str(dy),7.2,3.3,(x+dx,y+dy,face-5.7),(0,0,1))
    for dx in [-15,15]:_g6_bore(c,'FRAME-M5-'+str(dx),5.5,7,(x+dx,sy,273),(0,0,1))
    _box(c,'Y-RAIL-CLEARANCE',8,202,10,(sx*113,0,280),cut)
    for dx in [-15.5,15.5]:
        for dy in [-15.5,15.5]:_g6_bore(c,'MOTOR-HEAD-ACCESS-'+str(dx)+'-'+str(dy),8,280-(face+6),(x+dx,y+dy,face+6),(0,0,1))
    # Trim the future island before the circular idler cut, so native history
    # does not have to create then remove a disconnected body.
    if axis=='A' and k==2:
        low,high=face+5.95,280.1
        _box(c,'OMIT-DISCONNECTED-INNER-TIP',5.5,19.5,high-low,(x-20,-83.25,(low+high)/2),cut)
    if k==2:
        r=88.75-2*11.459155902616464
        _g6_bore(c,'FIXED-RETURN-CLEARANCE',28.5,26.2,((1 if axis=='A' else -1)*r,-105,262.8),(0,0,1))
    return c


def _g6_import_hardware(fixed,moving):
    base=globals().get('REVF_NATIVE_EXPORT_ROOT',os.path.join(_G6_BASE,'exports'))
    folder=os.path.join(base,'gantry_supports')
    path=os.path.join(folder,'CBP_RevF_Gantry_Supports_DEVELOPMENT-parts.json')
    assert os.path.isfile(path),'Export06_gantry_supports_cq.py before native hardware import'
    app=adsk.core.Application.get()
    for row in json.load(open(path,encoding='utf-8')):
        if row['category'] in ('printed','cnc'):continue
        parent=fixed if row['motion_group']=='fixed' else moving
        name=row['name'];file=os.path.join(folder,name+'.step')
        assert os.path.isfile(file),file
        assert not any(o.component.name==name for o in parent.occurrences),'Already imported '+name
        o=part(parent,name);o.component.partNumber=name
        o.component.description='PURCHASED/FASTENER REFERENCE; '+row.get('notes','')+' Position frozen to standalone export.'
        options=app.importManager.createSTEPImportOptions(file)
        assert app.importManager.importToTarget(options,o.component),name


def build_native_gantry_supports():
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    assert d and d.designType==adsk.fusion.DesignTypes.ParametricDesignType
    _g6_parameters(d)
    motion=group(d.rootComponent,'20_XY_MOTION').component
    fixed=group(motion,'24_AWD_DRIVES_FIXED').component
    moving=group(group(motion,'22_Y_GANTRY').component,'27_GANTRY_END_SUPPORTS').component
    for side in [-1,1]:
        hand='R' if side>0 else 'L'
        for build in [_g6_adapter,_g6_clamp,_g6_fork,_g6_cap,_g6_portal]:
            c=build(moving,side,hand)
            assert c.bRepBodies.count==1,(c.name,c.bRepBodies.count)
            c.bRepBodies.item(0).name=c.name
    for axis,z in [('A',282.3),('B',269.3)]:
        sign=1 if axis=='A' else -1;face=z-24.5
        for k,(x,y) in enumerate([(-sign*88.75,95),(sign*88.75,-105)],1):
            c=_g6_hanger(fixed,axis,k,x,y,face)
            assert c.bRepBodies.count==1,(c.name,c.bRepBodies.count)
            c.bRepBodies.item(0).name=c.name
    _g6_import_hardware(fixed,moving)
    d.computeAll();audit(d)
    print('Native06 custom supports built with driving sketches; hardware imported individually. ReducedY-20..+30 only. Native recomputation/interference/material/joint verification still required.')


def run(_context: str):
    build_native_gantry_supports()
