import adsk.core,adsk.fusion


def run(context):
    app=adsk.core.Application.get()
    project=next(p for p in app.data.dataProjects if p.name=='Default Project')
    folder=next(f for f in project.rootFolder.dataFolders if f.name=='Codex Benchy Printer')
    files=[f for f in folder.dataFiles]
    print('saved designs',[(f.name,f.versionNumber) for f in files])
    df=next(f for f in files if f.name=='Codex Benchy Printer RevF AWD CoreXY')
    doc=app.documents.open(df)
    print('opened',doc.name,df.id,df.versionNumber)
    d=adsk.fusion.Design.cast(app.activeProduct)
    print('native state',d.rootComponent.allOccurrences.count,'occurrences',d.userParameters.count,'parameters',d.timeline.count,'timeline')
