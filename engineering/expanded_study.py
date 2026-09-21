"""Revision C: hypothetical high-acceleration path and drive requirements.

This is a screening calculation, not a printer capability prediction. See
REV-C-PERFORMANCE.md for exclusions, sources, and the unpassed release gate.
"""
import hashlib, json, math
from path_model import ROOT, parse, duration, summarize, AF
from validate_klipper_planner import klipper_duration


def drive_bound(torque, inertia, mass, count, reserve=.7):
    """Independent, identical actuators sharing ONE axis, ideal massless wheels.

    SI inputs: operating torque Nm, rotor inertia kg m2, load kg. Reserve
    multiplies torque. Does NOT represent a CoreXY or delta transformation.
    """
    radius = math.sqrt(count * inertia / mass)
    acceleration = reserve * math.sqrt(count) * torque / (2 * math.sqrt(inertia * mass))
    return dict(radius_mm=radius*1000, acceleration_mm_s2=acceleration*1000,
                rpm_at_2400_mm_s=2.4/radius*60/(2*math.pi),
                motor_reflected_mass_g=count*inertia/radius**2*1000,
                one_full_step_mm=radius*2*math.pi/200*1000)


def run():
    source=ROOT/'slicing/cura-4.13.1-simplified/analysis.gcode'
    moves=parse(source)
    result={'status':'Hypothetical screening only; no physical capability validated',
            'gcode_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'summary':summarize(moves), 'grid':[], 'sensitivity':[]}
    for a in (500000,1000000,1500000,2000000,3000000):
        for scv in (100,300,500):
            result['grid'].append(duration(moves,300,2400,a,scv))
    nominal=duration(moves,300,2400,2000000,500)
    result['hypothetical_target']=nominal
    for q,v,a,scv,first in [(200,2400,2000000,500,None),
                           (250,2400,2000000,500,None),
                           (300,1700,2000000,500,None),
                           (300,2400,1500000,500,None),
                           (300,2400,2000000,300,None),
                           (300,2400,2000000,500,100),
                           (300,2400,2000000,500,300),
                           (300,2400,2000000,500,500),
                           (250,1700,1500000,300,300)]:
        result['sensitivity'].append(duration(moves,q,v,a,scv,first))
    result['pinned_klipper']=[klipper_duration(moves,300,2400,2000000,500,mcr=mcr,finite_queue=finite)
                            for mcr,finite in [(0,False),(0,True),(.5,True)]]
    assert abs(result['pinned_klipper'][0]['seconds']-nominal['seconds'])<1e-5
    # Motor cases intentionally label their evidence level. Do not treat a
    # holding torque as an available operating torque or mix model inertias.
    cases=[('LDO-42STH48-2504AC',.401,8.45e-6,'24V curve value at 60 rpm; bound ignores further speed dependence'),
           ('Leadshine 57CM26',2.6,5.2e-5,'HOLDING torque ceiling only'),
           ('Leadshine 86CM120',12.,2.94e-4,'HOLDING torque ceiling only'),
           ('Leadshine 86CM120',9.,2.94e-4,'Illustrative lower graph reading near 200 rpm / 70V / 6A RMS; not digitized or guaranteed')]
    result['ideal_axis_drives']=[]
    for name,t,j,status in cases:
        for mass in (.06,.09,.14):
            for n in (1,2,4):
                row=drive_bound(t,j,mass,n)
                row.update(model=name,torque_Nm=t,rotor_inertia_kg_m2=j,
                           torque_evidence=status,axis_load_g=mass*1000,
                           motors_per_independent_axis=n,reserve_factor=.7)
                result['ideal_axis_drives'].append(row)
    # Simple rotor-only load angle and translational stiffness illustration.
    # Hybrid 1.8 degree stepper assumed 50 electrical cycles/revolution.
    # This includes motor rotor acceleration torque, not just load torque.
    sample=drive_bound(9.,2.94e-4,.06,4)
    r=sample['radius_mm']/1000
    load_angle=math.asin(.7)/50
    result['drive_accuracy_example']={
        'model':'Illustrative 4-motor independent axis, 86CM120, 60g, ideal optimum radius',
        'assumed_pole_pairs':50,'torque_fraction':.7,
        'motor_load_angle_degrees':load_angle*180/math.pi,
        'rim_lag_mm':r*load_angle*1000,
        'small_signal_stiffness_N_m':4*50*9/r**2,
        'note':'Quasistatic sine-torque illustration, not a dynamic error simulation. More microsteps do not remove load angle.'}
    result['thermal_requirements']=[{
        'flow_mm3_s':q, 'filament_feed_mm_s':q/AF,
        'polymer_mass_g_s':q*.00124,
        'sensible_power_W_range':[q*.00124*c*215 for c in (1.5,2.)],
        'four_equal_inputs_feed_mm_s_each':q/AF/4
    } for q in (200,250,300)]
    result['load_requirements']=[{
        'moving_mass_g':m, 'accel_mm_s2':2000000,
        'inertia_force_N':m/1000*2000,
        'stiffness_N_mm_for_0p05mm_deflection':m/1000*2000/.05,
        'single_mass_natural_frequency_Hz_at_that_stiffness':math.sqrt(2000/.00005)/(2*math.pi)
    } for m in (60,90,140)]
    (ROOT/'engineering/expanded-path-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'target':nominal,'sensitivity':[{'q':x['assumed_flow_cap_mm3_s'],'v':x['assumed_vmax_mm_s'],'a':x['assumed_accel_mm_s2'],'scv':x['assumed_scv_mm_s'],'first':x['first_layer_cap_mm_s'],'s':round(x['seconds'],4)} for x in result['sensitivity']],
                     'planner':[round(x['seconds'],6) for x in result['pinned_klipper']],
                     'accuracy_example':result['drive_accuracy_example']},indent=2))


if __name__=='__main__':
    # Dimensional / scaling identities of the independent-axis idealization.
    one=drive_bound(1.,1e-5,.1,1,1.)
    four=drive_bound(1.,1e-5,.1,4,1.)
    assert abs(four['acceleration_mm_s2']/one['acceleration_mm_s2']-2)<1e-12
    assert abs(one['motor_reflected_mass_g']-100)<1e-12
    run()
