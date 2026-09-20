"""Pre-CAD sensitivity calculations. Estimates are explicitly not purchased/CAD masses."""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

# name, mass g, XYZ centroid mm, bounding dimensions mm. Origin = carriage center;
# X belt travel, Y forward from rail, Z up. Belt force axis crosses origin.
# Boxes only estimate local inertia; masses are independent lumped estimates.
ITEMS=[
('rail carriage',26,(0,0,0),(17,23,8)),
('aluminum saddle',8,(0,2,0),(30,3,35)),
('heat sink',15,(0,13,-4),(22,16,20)),
('heat break',2,(0,15,-15),(7,7,10)),
('heater block and heater',21,(0,15,-24),(18,18,15)),
('nozzle',5,(0,15,-34),(7,7,9)),
('silicone sock',1.5,(0,15,-24),(20,20,16)),
('heat sink fan',7,(0,-12,-4),(25,10,25)),
('CPAP duct',10,(0,4,-20),(40,26,28)),
('fasteners and inserts',9,(0,3,-3),(28,22,28)),
('supported hose segment',18,(0,0,30),(18,18,60)),
('moving wires',6,(0,-4,15),(8,8,40)),
('PTFE segment',2,(0,12,15),(4,4,30)),
('PTFE coupling',2,(0,12,8),(9,9,9)),
('contained filament',.5,(0,14,0),(2,2,35)),
('belt clamps',3,(0,0,0),(24,5,8))]

def mass_properties(items):
    mass=sum(i[1] for i in items)
    com=[sum(m*p[k] for _,m,p,b in items)/mass for k in range(3)]
    inertia=[]
    for k in range(3):
        axes=[j for j in range(3) if j!=k]
        inertia.append(sum(m*(sum(b[j]**2 for j in axes)/12+
                                  sum((p[j]-com[j])**2 for j in axes)) for _,m,p,b in items)*1e-9)
    # g mm2 -> kg m2 factor 1e-9. Moment from a=100 m/s2 along +X.
    F=mass/1000*100
    return {'mass_g':mass,'com_mm':com,'I_com_diagonal_kg_m2':inertia,
            'moment_at_origin_Nm_for_100m_s2_X':[0,com[2]*.001*F,-com[1]*.001*F]}

def run():
    bare=mass_properties(ITEMS)
    direct=mass_properties(ITEMS+[('direct-drive motor',90,(0,-6,24),(36,36,20)),
                                ('drive gears housing',28,(0,12,24),(26,22,26))])
    J=84.5e-7 # g cm2 -> kg m2: 1e-7
    # Manufacturer curve, 24V, 2.5A, full step. No extrapolation.
    curve=list(zip([200,600,1000,1400,1800,2200,2600,3000,3400,3800,4200,4600,5000,5400,5800,6200,6600,7000],
                   [401,420,451,471,492,478,430,386,347,314,287,261,239,224,205,194,181,168]))
    pulley=[]
    for teeth in (16,20,24,32):
        r=teeth*.002/(2*math.pi)
        pulley.append({'teeth':teeth,'radius_m':r,'rotor_reflected_mass_kg':J/r**2,
                       'rpm_at_1500mm_s':1.5/(2*math.pi*r)*60,
                       'max_single_axis_speed_in_curve_mm_s':2100/60*2*math.pi*r*1000})
    r=.04/(2*math.pi)
    table=[]
    # Reserve 30% of measured running torque; allow 2N friction/hose, 0.010kg pulley inertia.
    for pps,torque in curve:
        rpm=pps/200*60;v=rpm/60*.04
        force=.7*torque*.001/r
        effective=bare['mass_g']/1000+J/r**2+.010
        table.append({'rpm':rpm,'v_mm_s':v*1000,'measured_running_torque_Nm':torque*.001,
                      'force_after_30pct_reserve_N':force,
                      'cartesian_X_accel_mm_s2_with_2N_drag':max(0,(force-2)/effective)*1000})
    bed={'al_plate_g':75*45*1.5*.0027,'surface_g':5,'heater_g':8,'carrier_g':12,
         'carriage_g':26,'fasteners_g':7,'moving_wires_g':4,'clamp_g':3,'printed_model_g':11}
    f=[{'effective_mass_kg':m,'stiffness_N_m':k,'natural_frequency_Hz':math.sqrt(k/m)/(2*math.pi),
        'deflection_at_20N_mm':20/k*1000} for m in (.35,.6) for k in (10000,40000,100000)]
    result={'status':'pre-CAD estimates; no measured complete toolhead',
            'coordinate_system':'X travel; Y forward of carriage; Z up; belt force through origin',
            'items':[dict(name=n,mass_g=m,centroid_mm=p,inertia_box_mm=b) for n,m,p,b in ITEMS],
            'bowden_toolhead':bare,'direct_drive_option':direct,'pulley_sensitivity':pulley,
            'motor_force_table':table,'bed_estimates':bed,'bed_total_g':sum(bed.values()),
            'stiffness_sensitivity':f}
    (ROOT/'engineering/mechanics_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['bowden_toolhead','direct_drive_option','pulley_sensitivity','bed_total_g']},indent=2))

if __name__=='__main__':run()
