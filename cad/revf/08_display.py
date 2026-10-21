"""Readable engineering display. Appearance only; no physical material change."""
import adsk.core,adsk.fusion

def run(_context: str):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeProduct)
    assert d.parentDocument.name=='Codex Benchy Printer RevF Detailed Bowden'
    d.activateRootComponent()
    lib=app.materialLibraries.itemByName('Fusion Appearance Library')
    roles={}
    for role,source in [('aluminum','Aluminum - Bead Blasted'),('printed','Plastic - Matte (Blue)'),
                        ('black','Plastic - Matte (Black)'),('steel','Steel - Satin')]:
        name='CBP display - '+role
        roles[role]=d.appearances.itemByName(name) or d.appearances.addByCopy(lib.appearances.itemByName(source),name)
    def role_for(name,inherited):
        if name.startswith(('CBP-P501','CBP-P502')):return 'vendor'
        if inherited=='vendor':return inherited
        if name.startswith('CBP-H'):return 'steel'
        if any(s in name for s in ['CARBON','TPU','MAGNET','SILICONE','MOTOR_PROXY']):return 'black'
        if name.startswith(('CBP-F120','CBP-F123','CBP-Z307','CBP-Z309','CBP-Z310','CBP-M203')):return 'printed'
        if name.startswith(('CBP-F101','CBP-F102','CBP-F103','CBP-F104','CBP-F105','CBP-F121','CBP-F122','CBP-M201','CBP-M204','CBP-Z301','CBP-Z302','CBP-Z303','CBP-Z304','CBP-Z306','CBP-Z308')):return 'aluminum'
        if any(s in name for s in ['RAIL','MOUNT_CAP','SCREW_ENVELOPE','STEEL_PEI']):return 'steel'
        return inherited
    seen=set();changed=[]
    def walk(c,inherited=None):
        role=role_for(c.name,inherited)
        if c.entityToken in seen:return
        seen.add(c.entityToken)
        if c!=d.rootComponent:c.opacity=1.0
        c.isOriginFolderLightBulbOn=False;c.isConstructionFolderLightBulbOn=False;c.isSketchFolderLightBulbOn=False
        for b in c.bRepBodies:
            b.opacity=1.0
            if role in roles:b.appearance=roles[role];changed.append((c.name,b.name,role))
        for o in c.occurrences:
            child_role=role_for(o.component.name,role)
            if child_role!='vendor':o.appearance=None
            walk(o.component,role)
    walk(d.rootComponent)
    viewport=app.activeViewport
    viewport.visualStyle=adsk.core.VisualStyles.ShadedWithVisibleEdgesOnlyVisualStyle
    camera=viewport.camera
    camera.eye=adsk.core.Point3D.create(55,-75,60);camera.target=adsk.core.Point3D.create(0,0,15)
    camera.upVector=adsk.core.Vector3D.create(0,0,1)
    camera.cameraType=adsk.core.CameraTypes.OrthographicCameraType
    camera.isSmoothTransition=False;camera.isFitView=True
    viewport.camera=camera
    print('Engineering display applied',len(changed),'bodies; opaque, visible edges, Z up. Physical materials unchanged.')
