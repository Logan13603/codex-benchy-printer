from pathlib import Path

def run(context):
    base=Path(__file__).resolve().parents[2]/'revf'
    ns={'__name__':'cbp_bed_z','__file__':str(base/'03_bed_z.py')}
    for name in ['common.py','03_bed_z.py']:
        exec(compile((base/name).read_text(encoding='utf-8-sig'),str(base/name),'exec'),ns)
    ns['run'](context)
