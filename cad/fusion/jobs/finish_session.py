from pathlib import Path

def run(context):
    base=Path(__file__).resolve().parent
    ns={'__name__':'cbp_checkpoint','__file__':str(base/'checkpoint.py')}
    exec(compile((base/'checkpoint.py').read_text(encoding='utf-8-sig'),str(base/'checkpoint.py'),'exec'),ns)
    ns['run'](context)
    # Cleanly stop the project workbench only after the save/export succeeds.
    work=Path(__file__).resolve().parents[5]/'work'/'fusion_jobs'
    (work/'STOP').write_text('Saved native session checkpoint; explicitly restart next session.\n')
