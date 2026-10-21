"""Native parametric motor plates plus individual purchased AWD components.

Load common.py and the tested helper definitions from04_toolhead.py first.
No custom plate is imported as STEP. Hardware remains a purchased reference
at the frozen interface coordinates; re-joint/reposition it when changing
layout parameters. The native jobs must be recomputed/audited before release.
"""
import os
import json


_D5_BASE = r'C:\Users\logan\Documents\Codex\2026-09-20\this-will-take-multiple-trys-because-3\outputs\codex-benchy-printer\cad\revf'


def _d5_parameters(d):
    for n,e,note in [
        ('rf_drive_cx','88.75 mm','Frozen motor/moving-idler center X magnitude'),
        ('rf_drive_pitch_r','11.4591559026 mm','36T,2mm pitch pulley pitch radius'),
        ('rf_drive_a_z','282.3 mm','A belt center plane'),
        ('rf_drive_b_z','269.3 mm','B belt center plane'),
        ('rf_drive_motor_offset','24.5 mm','Motor face below its belt plane; native purchased references remain frozen'),
        ('rf_drive_front_y','-105 mm','Front motor/fixed-return station'),
        ('rf_drive_back_y','95 mm','Rear motor station'),
        ('rf_y_travel_min','-20 mm','Verified reduced Y envelope minimum'),
        ('rf_y_travel_max','30 mm','Verified reduced Y envelope maximum'),
    ]:param(d,n,e,note)


def _d5_new(parent,name,description):
    assert not any(o.component.name==name for o in parent.occurrences),'Already built '+name
    c=part(parent,name).component
    c.partNumber=name
    c.description=description
    return c


def _d5_import_references(fixed,moving,belts):
    base=globals().get('REVF_NATIVE_EXPORT_ROOT',os.path.join(_D5_BASE,'exports'))
    folder=os.path.join(base,'drives')
    manifest=os.path.join(folder,'CBP_RevF_AWD_Drives_DEVELOPMENT-parts.json')
    assert os.path.isfile(manifest),'Export05_drives_cq.py before native purchased import'
    rows=json.load(open(manifest,encoding='utf-8'))
    app=adsk.core.Application.get()
    for row in rows:
        if row['category']=='cnc':continue
        parent=belts if row['motion_group']=='belt_distributed' else moving if row['motion_group']=='gantry' else fixed
        name=row['name'];path=os.path.join(folder,name+'.step')
        assert os.path.isfile(path),path
        assert not any(o.component.name==name for o in parent.occurrences),'Already imported '+name
        o=part(parent,name);o.component.partNumber=name
        o.component.description='PURCHASED/FASTENER REFERENCE; '+row.get('notes','')+' Native position frozen to the standalone export; thread/pulley tooth proxies are simplified.'
        options=app.importManager.createSTEPImportOptions(path)
        assert app.importManager.importToTarget(options,o.component),name


def _d5_outer_round(c):
    edges=adsk.core.ObjectCollection.create()
    for e in c.bRepBodies.item(0).edges:
        a,b=e.startVertex.geometry,e.endVertex.geometry
        if abs(a.x-b.x)<1e-7 and abs(a.y-b.y)<1e-7 and abs(abs(a.z-b.z)-.6)<1e-7:edges.add(e)
    assert edges.count==4,edges.count
    inp=c.features.filletFeatures.createInput()
    inp.addConstantRadiusEdgeSet(edges,vi('2 mm'),True)
    c.features.filletFeatures.add(inp).name='OUTER-CORNERS-R2'


def _d5_motor_plate(fixed,axis,k):
    op=adsk.fusion.FeatureOperations
    sign=1 if axis=='A' else -1
    plane='rf_drive_a_z' if axis=='A' else 'rf_drive_b_z'
    face='('+plane+')-rf_drive_motor_offset'
    sx=-sign if k==1 else sign;y='rf_drive_back_y' if k==1 else 'rf_drive_front_y'
    x=str(sx)+'*rf_drive_cx'
    c=_d5_new(fixed,'CBP-D401_'+axis+'_MOTOR_PLATE_'+str(k),
        '6061-T6 native45x64x6 plate withR2 corners. Shaft bore8; underside pilot pocket22.10x2.15, nominal fit HOLD pending maker tolerance. M3x10+0.5washer gives3.5mm motor engagement and1.0mm minimum bottom clearance in4.5mmdeep maker hole. A-front shallow0.70mm return pocket preserves full pilot. Flatness/parallelism0.05,deburr0.2; stiffness unvalidated.')
    _box(c,'MOTOR-PLATE',45,64,6,(x,y,'('+face+')+3 mm'),op.NewBodyFeatureOperation)
    _d5_outer_round(c)
    _cyl(c,'SHAFT-BORE',8,6,(x,y,face),(0,0,1),op.CutFeatureOperation)
    _cyl(c,'PILOT-SOCKET-HOLD',22.10,2.15,(x,y,face),(0,0,1),op.CutFeatureOperation)
    for dx in [-15.5,15.5]:
        for dy in [-15.5,15.5]:
            _cyl(c,'MOTOR-M3-'+str(dx)+'-'+str(dy),3.5,6,
                 ('('+x+')+('+str(dx)+' mm)','('+y+')+('+str(dy)+' mm)',face),(0,0,1),op.CutFeatureOperation)
    for dx in [-17,17]:
        for dy in [-27,27]:
            _cyl(c,'HANGER-M4-'+str(dx)+'-'+str(dy),4.4,6,
                 ('('+x+')+('+str(dx)+' mm)','('+y+')+('+str(dy)+' mm)',face),(0,0,1),op.CutFeatureOperation)
    if k==2:
        for dx in [-6,6]:
            _cyl(c,'M5-ALLEN-ACCESS-'+str(dx),6,6,('('+x+')+('+str(dx)+' mm)','-130 mm',face),(0,0,1),op.CutFeatureOperation)
    if axis=='A' and k==2:
        _cyl(c,'NEIGHBOR-RETURN-SHALLOW-POCKET',28.5,.70,
             ('rf_drive_cx-2*rf_drive_pitch_r','rf_drive_front_y','263.10 mm'),(0,0,1),op.CutFeatureOperation)
    assert c.bRepBodies.count==1,c.name
    c.bRepBodies.item(0).name=c.name
    return c


def import_native_drive_station_hardware(axis,k):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    fixed=group(group(d.rootComponent,'20_XY_MOTION').component,'24_AWD_DRIVES_FIXED').component
    folder=os.path.join(globals().get('REVF_NATIVE_EXPORT_ROOT',os.path.join(_D5_BASE,'exports')),'drives')
    rows=json.load(open(os.path.join(folder,'CBP_RevF_AWD_Drives_DEVELOPMENT-parts.json'),encoding='utf-8'))
    names=['CBP-P401_'+axis+'_LDO_MOTOR_'+str(k),'CBP-P402_'+axis+'_36T_DRIVE_'+str(k)]
    prefixes=['CBP-H501_'+axis+'_MOTOR_'+str(k)+'_','CBP-H502_'+axis+'_MOTOR_'+str(k)+'_']
    app=adsk.core.Application.get();count=0
    for row in rows:
        n=row['name']
        if not(n in names or any(n.startswith(p) for p in prefixes)):continue
        if any(o.component.name==n for o in fixed.occurrences):continue
        o=part(fixed,n);o.component.partNumber=n;o.component.description=row.get('notes','')
        assert app.importManager.importToTarget(app.importManager.createSTEPImportOptions(os.path.join(folder,n+'.step')),o.component),n
        count+=1
    print('Imported drive station',axis,k,count,'purchased/fastener components')


def build_native_drive_station(axis,k,include_hardware=False):
    assert axis in ('A','B') and k in (1,2)
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    assert d and d.designType==adsk.fusion.DesignTypes.ParametricDesignType
    _d5_parameters(d)
    fixed=group(group(d.rootComponent,'20_XY_MOTION').component,'24_AWD_DRIVES_FIXED').component
    c=_d5_motor_plate(fixed,axis,k)
    if include_hardware:import_native_drive_station_hardware(axis,k)
    d.computeAll();print('Completed native drive plate',axis,k,c.name)
    return c


def build_native_drives():
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    _d5_parameters(d)
    motion=group(d.rootComponent,'20_XY_MOTION').component
    fixed=group(motion,'24_AWD_DRIVES_FIXED').component
    moving=group(group(motion,'22_Y_GANTRY').component,'25_AWD_IDLERS_GANTRY').component
    belts=group(motion,'26_BELT_ROUTES_REFERENCE').component
    for axis in ['A','B']:
        for k in [1,2]:_d5_motor_plate(fixed,axis,k)
    _d5_import_references(fixed,moving,belts)
    d.computeAll();audit(d)
    print('Native05 motor plates built. Nominal fit, joints, materials and structural validation remain HOLD.')


def run(_context: str):
    build_native_drives()
