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


def build_native_drives():
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    assert d and d.designType==adsk.fusion.DesignTypes.ParametricDesignType
    _d5_parameters(d)
    motion=group(d.rootComponent,'20_XY_MOTION').component
    fixed=group(motion,'24_AWD_DRIVES_FIXED').component
    moving=group(group(motion,'22_Y_GANTRY').component,'25_AWD_IDLERS_GANTRY').component
    belts=group(motion,'26_BELT_ROUTES_REFERENCE').component
    op=adsk.fusion.FeatureOperations
    for axis,plane in [('A','rf_drive_a_z'),('B','rf_drive_b_z')]:
        sign=1 if axis=='A' else -1
        face='('+plane+')-rf_drive_motor_offset'
        for k,(sx,y) in enumerate([(-sign,'rf_drive_back_y'),(sign,'rf_drive_front_y')],1):
            x=str(sx)+'*rf_drive_cx'
            c=_d5_new(fixed,'CBP-D401_'+axis+'_MOTOR_PLATE_'+str(k),
                'Native6061 plate45x64x6. Fixed31mm motor pattern; belt tension belongs at anchors. FrontR14.25 return relief. Plates remain1mm below modeled lower belt; purchased dimensions/tolerances unvalidated.')
            _box(c,'MOTOR-PLATE',45,64,6,(x,y,'('+face+')+3 mm'),op.NewBodyFeatureOperation)
            _cyl(c,'PILOT-CLEARANCE',23,6,(x,y,face),(0,0,1),op.CutFeatureOperation)
            for dx in [-15.5,15.5]:
                for dy in [-15.5,15.5]:
                    _cyl(c,'MOTOR-M3-'+str(dx)+'-'+str(dy),3.5,6,
                         ('('+x+')+('+str(dx)+' mm)','('+y+')+('+str(dy)+' mm)',face),
                         (0,0,1),op.CutFeatureOperation)
            for dx in [-17,17]:
                for dy in [-27,27]:
                    _cyl(c,'HANGER-M4-'+str(dx)+'-'+str(dy),4.4,6,
                         ('('+x+')+('+str(dx)+' mm)','('+y+')+('+str(dy)+' mm)',face),
                         (0,0,1),op.CutFeatureOperation)
            if k==2:
                rx=str(sign)+'*(rf_drive_cx-2*rf_drive_pitch_r)'
                _cyl(c,'NEIGHBOR-RETURN-R14p25',28.5,6,(rx,'rf_drive_front_y',face),(0,0,1),op.CutFeatureOperation)
            assert c.bRepBodies.count==1,c.name
            c.bRepBodies.item(0).name=c.name
    _d5_import_references(fixed,moving,belts)
    d.computeAll();audit(d)
    print('Native05 motor plates built with driving sketches. Purchased AWD items imported individually. Verify joints, materials and interface tolerance stack before release.')


def run(_context: str):
    build_native_drives()
