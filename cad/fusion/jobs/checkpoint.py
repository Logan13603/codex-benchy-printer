"""Save and export a named native checkpoint; the job config supplies its label."""
import adsk.core,adsk.fusion
from pathlib import Path
import json,hashlib,datetime

def run(context):
    app=adsk.core.Application.get()
    doc=app.activeDocument
    assert doc.name=='Codex Benchy Printer RevF Detailed Bowden',doc.name
    root=Path(__file__).resolve().parents[2]
    config=json.loads((root/'fusion'/'checkpoint-config.json').read_text())
    target=root/'native';target.mkdir(exist_ok=True)
    name=config['name']
    assert name.startswith('CBP-RevF-') and '/' not in name and '\\' not in name
    d=adsk.fusion.Design.cast(app.activeProduct)
    assert d.computeAll()
    sketch_rows=[];features=[];components=[];seen=set()
    def walk(c):
        if c.entityToken in seen:return
        seen.add(c.entityToken)
        components.append({'name':c.name,'bodies':c.bRepBodies.count,'occurrences':c.occurrences.count})
        for s in c.sketches:
            sketch_rows.append({'component':c.name,'sketch':s.name,'fully_constrained':s.isFullyConstrained})
            s.isVisible=False
        for p in c.constructionPlanes:p.isLightBulbOn=False
        for f in c.features:
            if f.healthState!=adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState:
                features.append({'component':c.name,'feature':f.name,'state':int(f.healthState),'message':f.errorOrWarningMessage})
        for o in c.occurrences:walk(o.component)
    walk(d.rootComponent)
    assert doc.save(config['description'])
    ex=d.exportManager
    f3d=target/(name+'.f3d');step=target/(name+'.step')
    assert ex.execute(ex.createFusionArchiveExportOptions(str(f3d)))
    assert ex.execute(ex.createSTEPExportOptions(str(step)))
    app.activeViewport.fit()
    assets=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [f3d,step]]
    report={'status':'DEVELOPMENT_NOT_MANUFACTURING_RELEASE','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'document':doc.name,'fusion_data_id':doc.dataFile.id,'fusion_version':doc.dataFile.versionNumber,
        'components':components,'sketches':sketch_rows,'unconstrained':[r for r in sketch_rows if not r['fully_constrained']],
        'feature_health':features,'parameters':d.userParameters.count,'timeline':d.timeline.count,'assets':assets}
    (target/(name+'-manifest.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('CHECKPOINT',name,'components',len(components),'sketches',len(sketch_rows),'unconstrained',len(report['unconstrained']),'feature warnings',len(features),'assets',assets)
