import adsk.core, adsk.fusion

def run(context):
    app=adsk.core.Application.get()
    doc=app.activeDocument
    assert doc.name=='Codex Benchy Printer RevF AWD CoreXY',doc.name
    project=next(p for p in app.data.dataProjects if p.name=='Default Project')
    folder=next(f for f in project.rootFolder.dataFolders if f.name=='Codex Benchy Printer')
    assert not any(f.name=='Codex Benchy Printer RevF Detailed Bowden' for f in folder.dataFiles)
    assert doc.saveAs('Codex Benchy Printer RevF Detailed Bowden',folder,
        'Detailed Bowden development assembly; preserves RevF AWD v5. Manufacturing release pending interface and travel audits.','')
    d=adsk.fusion.Design.cast(app.activeProduct)
    print('working copy',doc.name,doc.dataFile.id,doc.dataFile.versionNumber)
    print('groups',[(o.component.name,o.component.occurrences.count) for o in d.rootComponent.occurrences])
