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


def _g6_station_custom(parent,axis,k,x,y,face):
    ns={}
    path=os.path.join(_G6_BASE,'motor_mount_dimensions.py')
    exec(compile(open(path,encoding='utf-8').read(),path,'exec'),ns)
    specs=ns['motor_mount_specs'](axis,k,x,y,face)
    op=adsk.fusion.FeatureOperations;done=[]
    for spec in specs:
        c=_g6_new(parent,spec['name'],'6061-T6 metal mount; '+spec['notes'])
        for f in spec['operations']:
            operation={'new':op.NewBodyFeatureOperation,'join':op.JoinFeatureOperation,'cut':op.CutFeatureOperation}[f['op']]
            if f['kind']=='box':_box(c,f['name'],*f['size'],f['p'],operation)
            else:_cyl(c,f['name'],f['d'],f['L'],f['p'],f['axis'],operation)
        assert c.bRepBodies.count==1,(c.name,c.bRepBodies.count)
        c.bRepBodies.item(0).name=c.name;done.append(c)
    return done


def import_native_motor_station_hardware(axis,k):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    fixed=group(group(d.rootComponent,'20_XY_MOTION').component,'24_AWD_DRIVES_FIXED').component
    base=globals().get('REVF_NATIVE_EXPORT_ROOT',os.path.join(_G6_BASE,'exports'))
    folder=os.path.join(base,'gantry_supports')
    rows=json.load(open(os.path.join(folder,'CBP_RevF_Gantry_Supports_DEVELOPMENT-parts.json'),encoding='utf-8'))
    app=adsk.core.Application.get();count=0
    prefixes=['CBP-H'+str(n)+'_'+axis+'_'+str(k)+'_' for n in [610,611,612,613,614]]
    for row in rows:
        n=row['name']
        if not any(n.startswith(p) for p in prefixes):continue
        if any(o.component.name==n for o in fixed.occurrences):continue
        o=part(fixed,n);o.component.partNumber=n;o.component.description=row.get('notes','')
        assert app.importManager.importToTarget(app.importManager.createSTEPImportOptions(os.path.join(folder,n+'.step')),o.component),n
        count+=1
    print('Imported metal mount hardware',axis,k,count,'components')


def build_native_motor_station(axis,k,include_hardware=False):
    assert axis in ('A','B') and k in (1,2)
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    assert d and d.designType==adsk.fusion.DesignTypes.ParametricDesignType
    _g6_parameters(d)
    fixed=group(group(d.rootComponent,'20_XY_MOTION').component,'24_AWD_DRIVES_FIXED').component
    sign=1 if axis=='A' else -1;face=(282.3 if axis=='A' else 269.3)-24.5
    x=(-sign if k==1 else sign)*88.75;y=95 if k==1 else -105
    components=_g6_station_custom(fixed,axis,k,x,y,face)
    if include_hardware:import_native_motor_station_hardware(axis,k)
    d.computeAll();print('Completed native metal motor mount',axis,k,len(components),'custom parts')
    return components


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
            _g6_station_custom(fixed,axis,k,x,y,face)
    _g6_import_hardware(fixed,moving)
    d.computeAll();audit(d)
    print('Native06 custom supports built with driving sketches; hardware imported individually. ReducedY-20..+30 only. Native recomputation/interference/material/joint verification still required.')


def run(_context: str):
    build_native_gantry_supports()
