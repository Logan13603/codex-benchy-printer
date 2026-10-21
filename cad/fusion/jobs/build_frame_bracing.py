from pathlib import Path

def run(context):
    base=Path(__file__).resolve().parents[2]/'revf'
    ns={'__name__':'cbp_frame_bracing','__file__':str(base/'07_frame_bracing.py')}
    for name in ['common.py','04_toolhead.py','07_frame_bracing.py']:
        exec(compile((base/name).read_text(encoding='utf-8-sig'),str(base/name),'exec'),ns)
    ns['run'](context)
