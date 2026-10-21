"""Export/audit an already-saved native design without bulk display mutations."""
import adsk.core,adsk.fusion
from pathlib import Path
import json,hashlib,datetime

def snapshot(name):
    app=adsk.core.Application.get();doc=app.activeDocument
    assert doc.name=='Codex Benchy Printer RevF Detailed Bowden',doc.name
    d=adsk.fusion.Design.cast(app.activeProduct)
    assert not doc.isModified,'Save with the native document operation before snapshot'
    root=Path(__file__).resolve().parents[2];target=root/'native';target.mkdir(exist_ok=True)
    assert name.startswith('CBP-RevF-') and '/' not in name and '\\' not in name
    seen=set();components=[];sketches=[];warnings=[]
    def walk(c):
        if c.entityToken in seen:return
        seen.add(c.entityToken)
        components.append({'name':c.name,'bodies':c.bRepBodies.count,'occurrences':c.occurrences.count,
            'volume_mm3':sum(b.volume*1000 for b in c.bRepBodies)})
        for s in c.sketches:sketches.append({'component':c.name,'sketch':s.name,'fully_constrained':s.isFullyConstrained})
        for f in c.features:
            if f.healthState!=adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState:
                warnings.append({'component':c.name,'feature':f.name,'message':f.errorOrWarningMessage})
        for o in c.occurrences:walk(o.component)
    walk(d.rootComponent)
    ex=d.exportManager;assets=[]
    for suffix in ['.f3d','.step']:
        p=target/(name+suffix)
        opt=ex.createFusionArchiveExportOptions(str(p)) if suffix=='.f3d' else ex.createSTEPExportOptions(str(p))
        assert ex.execute(opt),p.name
        assets.append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    report={'status':'DEVELOPMENT_NOT_MANUFACTURING_RELEASE','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'document':doc.name,'fusion_data_id':doc.dataFile.id,'fusion_version':doc.dataFile.versionNumber,
        'components':components,'sketches':sketches,'unconstrained':[s for s in sketches if not s['fully_constrained']],
        'feature_health':warnings,'parameters':d.userParameters.count,'timeline':d.timeline.count,
        'all_occurrences':d.rootComponent.allOccurrences.count,'assets':assets,'modified_after_export':doc.isModified}
    (target/(name+'-manifest.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('CHECKPOINT',name,'cloud',report['fusion_version'],'components',len(components),'bodies',sum(c['bodies'] for c in components),'sketches',len(sketches),'unconstrained',len(report['unconstrained']),'warnings',len(warnings),'modified',doc.isModified)
    return report

def run(_context: str):
    snapshot('CBP-RevF-013-Complete-Bracing-Display')
