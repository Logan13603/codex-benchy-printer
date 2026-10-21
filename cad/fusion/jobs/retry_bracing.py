from pathlib import Path
import adsk.core,adsk.fusion

def run(context):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    for o in list(d.rootComponent.occurrences):
        if o.component.name=='11_FRAME_BRACING':assert o.deleteMe()
    base=Path(__file__).resolve().parents[2]/'revf'
    ns={'__name__':'cbp_frame_bracing','__file__':str(base/'07_frame_bracing.py')}
    for name in ['common.py','04_toolhead.py','07_frame_bracing.py']:
        exec(compile((base/name).read_text(encoding='utf-8-sig'),str(base/name),'exec'),ns)
    ns['run'](context)
