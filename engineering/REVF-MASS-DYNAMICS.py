"""Rev F bounded mass, center of mass and vibration screening.

Pure Python; no CAD mutation. Machine coordinates in mm: X right, Y rear,
Z up. All hotend/extruder centroids and their mass brackets are hypotheses
until the exact supplier assembly is weighed and mounted. Run this file to
write REVF-MASS-DYNAMICS.json and REVF-MASS-DYNAMICS.md beside it.
"""
from pathlib import Path
from itertools import product
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
BELT_PLANES_Z = [284.0, 294.0]
BELT_FORCE_POINT = [0.0, 0.0, sum(BELT_PLANES_Z) / 2]
X_RAIL_CENTER_Z = 280.0
NOZZLE_POINT = [0.0, -18.0, 225.0]
MOTOR_J_KG_M2 = 8.45e-6

# Separate the Micro motor from gears/housing to avoid hiding its location.
# The motor mass bracket covers a plausible NEMA14 package, not a chosen SKU.
# Each item: label, [low, nominal, high] g, XYZ centroid mm, box XYZ mm, status.
HEAD = [
    ('Micro motor', [60, 70, 80], [0, 15, 318], [36, 20, 36], 'unverified SKU; mass bracket'),
    ('Micro gears and printed body', [20, 27, 35], [0, -18, 303], [36, 25, 25], 'estimate; exact release/BOM pending'),
    ('Goliath AIR hotend complete', [55, 80, 105], [0, -18, 257], [24, 24, 64], 'estimate; no verified supplier assembly mass'),
    ('2510 cold-end fan', [4, 6, 9], [0, -35, 275], [25, 10, 25], 'estimate; fan SKU pending'),
    ('MGN7H carriage', [15, 15, 15], [0, 0, 280], [30.8, 17, 8], 'HIWIN catalogue mass; simplified local envelope'),
    ('Carriage/hotend printed support', [10, 15, 22], [0, -5, 285], [42, 24, 35], 'printed effective-density estimate'),
    ('Symmetric CPAP duct', [8, 15, 22], [0, -18, 240], [60, 54, 18], 'printed effective-density estimate'),
    ('Supported CPAP hose length', [5, 10, 20], [0, 15, 300], [25, 25, 60], 'effective carried mass; suspension unknown'),
    ('Supported harness length', [3, 5, 9], [0, 8, 293], [8, 8, 50], 'estimate; bend/support unknown'),
    ('Screws, inserts, belt clamps', [7, 10, 15], [0, -2, 283], [45, 12, 20], 'estimate; fastener schedule pending'),
    ('Filament and guide PTFE', [1, 2, 3], [0, -18, 310], [4, 4, 75], 'estimate; complete carried length'),
]

GANTRY_EXTRA = [
    {'name': 'CF square tube 200x20x20x1.5', 'mass_g': (20**2 - 17**2) * 200 * 1.6 / 1000,
     'mass_bounds_g': [(20**2 - 17**2) * 200 * x / 1000 for x in (1.4, 1.8)],
     'status': 'volume calculation; assumed density 1.4-1.8 g/cm3'},
    {'name': 'MGN7 rail 180 mm', 'mass_g': 0.22 * 0.180 * 1000,
     'mass_bounds_g': [39.6, 39.6], 'status': 'HIWIN 0.22 kg/m; holes included by supplier rate'},
    {'name': 'Two MGN9H moving blocks', 'mass_g': 56,
     'mass_bounds_g': [48, 64], 'status': 'unverified catalogue/SKU bracket; 24-32 g each'},
    {'name': 'Two printed gantry ends', 'mass_g': 20,
     'mass_bounds_g': [14, 30], 'status': 'estimate; rail alignment ribs/fasteners pending'},
    {'name': 'Rail/beam/end fasteners', 'mass_g': 9,
     'mass_bounds_g': [6, 14], 'status': 'estimate; all screws must enter schedule'},
    {'name': 'Carried belts', 'mass_g': 7,
     'mass_bounds_g': [4, 12], 'status': 'effective motion mass estimate; rotating belt spans not included'},
]

def mass_com(items, mode=1):
    masses = [p[1][mode] for p in items]
    total = sum(masses)
    return total, [sum(m * p[2][k] for m, p in zip(masses, items)) / total for k in range(3)]

def inertia(items, com):
    """Box centroid inertia + parallel axis, kg m2. Envelopes overestimate
    local inertia of hollow printed parts; not equivalent to CAD volume.
    """
    tensor = [[0.0]*3 for _ in range(3)]
    for _, bracket, pos, box, _ in items:
        m = bracket[1] / 1000
        d = [(pos[k] - com[k])/1000 for k in range(3)]
        b = [x/1000 for x in box]
        for i in range(3):
            tensor[i][i] += m * (sum(b[j]**2 for j in range(3) if j != i) / 12
                                  + sum(d[j]**2 for j in range(3) if j != i))
            for j in range(3):
                if i != j:
                    tensor[i][j] -= m*d[i]*d[j]
    return tensor

def mass_corner_com_bounds(items):
    vals = []
    for picks in product((0, 2), repeat=len(items)):
        weights = [p[1][idx] for p, idx in zip(items, picks)]
        total = sum(weights)
        vals.append([sum(w*p[2][j] for w,p in zip(weights,items))/total for j in range(3)])
    return [[min(v[j] for v in vals), max(v[j] for v in vals)] for j in range(3)]

def balance_motor(items):
    # Packaging search is deliberately limited. It is a mass arrangement
    # candidate; exact shaft/gear/mount and frame clearances are not solved.
    best = None
    for motor_y in range(0, 36):
        for motor_z in range(300, 326):
            c = [[p[0], p[1], list(p[2]), p[3], p[4]] for p in items]
            c[0][2] = [0, motor_y, motor_z]
            m, com = mass_com(c)
            cost = sum((com[j]-BELT_FORCE_POINT[j])**2 for j in range(3))
            if best is None or cost < best[0]:
                best = (cost, c, m, com)
    return best

def required_motor_position(items):
    mm = items[0][1][1]
    total = sum(p[1][1] for p in items)
    return [(BELT_FORCE_POINT[k]*total - sum(p[1][1]*p[2][k] for p in items[1:])) / mm
            for k in range(3)]

def moments(mass_g, com, accel_mm_s2):
    # About the stated belt-force point. X and Y acceleration cases.
    r = [(com[k]-BELT_FORCE_POINT[k])/1000 for k in range(3)]
    f = mass_g/1000*accel_mm_s2/1000
    return {'acceleration_mm_s2': accel_mm_s2, 'inertia_force_N': f,
            'X_accel_moment_Nm': [0, r[2]*f, -r[1]*f],
            'Y_accel_moment_Nm': [-r[2]*f, 0, r[0]*f]}

def run():
    nominal_mass, nominal_com = mass_com(HEAD)
    _, balanced, bm, bc = balance_motor(HEAD)
    head_bounds = [sum(p[1][k] for p in HEAD) for k in (0,2)]
    gantry_nom = sum(x['mass_g'] for x in GANTRY_EXTRA)
    gantry_bounds = [sum(x['mass_bounds_g'][k] for x in GANTRY_EXTRA) for k in (0,1)]
    moving_x = nominal_mass
    moving_y = nominal_mass+gantry_nom
    effective = []
    for teeth in (20, 24, 32, 36, 40):
        radius = teeth*0.002/(2*math.pi)
        rotor = 4*MOTOR_J_KG_M2/radius**2
        rows=[]
        for a in (100000,250000):
            for label,m in [('X',moving_x/1000),('Y',moving_y/1000)]:
                torque=(m+rotor)*a/1000*radius/4
                rows.append({'axis':label,'acceleration_mm_s2':a,'ideal_torque_Nm_per_motor':torque,
                             'required_operating_torque_30pct_reserve_Nm':torque/0.7})
        effective.append({'teeth':teeth,'pitch_radius_mm':radius*1000,
                          'four_rotor_equivalent_mass_g':rotor*1000,
                          'RPM_at_1000_mm_s_pure_axis':1000/(teeth*2)*60,
                          'RPM_at_1500_mm_s_45deg_toolpath':1500*math.sqrt(2)/(teeth*2)*60,
                          'torque_cases':rows})
    # Joint+rail+belt effective stiffness bracket; no measured stiffness.
    dynamic=[]
    r36=36*.002/(2*math.pi)
    for mass_label,mass in [('toolhead translation',moving_x/1000),
                            ('Y translation',moving_y/1000),
                            ('Y translation low mass', (head_bounds[0]+gantry_bounds[0])/1000),
                            ('Y translation high mass', (head_bounds[1]+gantry_bounds[1])/1000)]:
        for knmm in (10,25,50,100,250,500,1000):
            omega=math.sqrt(knmm*1000/mass)
            for zeta in (.01,.03,.08):
                dynamic.append({'mass_basis':mass_label,'effective_mass_kg':mass,
                    'stiffness_N_per_mm':knmm,'damping_ratio':zeta,
                    'frequency_Hz':omega/(2*math.pi),
                    'two_percent_settle_s_approx':4/(zeta*omega),
                    'step_overshoot_fraction':math.exp(-math.pi*zeta/math.sqrt(1-zeta*zeta)),
                    'static_deflection_mm_at_250k_accel':mass*250/knmm})
    # An alternative free two-inertia relative mode: a spring between the
    # translating load and the rotor-equivalent mass. Its rigid-body mode is
    # zero Hz; electrical stiffness/controller behavior are not included.
    rotor_relative=[]
    mr=4*MOTOR_J_KG_M2/r36**2
    my=moving_y/1000
    for knmm in (10,25,50,100,250,500,1000):
        rotor_relative.append({'stiffness_N_per_mm':knmm,
                               'rotor_equivalent_mass_kg':mr,'Y_translating_mass_kg':my,
                               'relative_frequency_Hz':math.sqrt(knmm*1000*(1/my+1/mr))/(2*math.pi),
                               'status':'ideal two-inertia relative mode; zero-frequency rigid-body mode omitted'})
    # Static beam point load screen. Frame beam stiffness excludes joints.
    cfI=(20**4-17**4)/12
    beam=[]
    for E in (50000,70000,100000):
        for force in (25,50,75):
            beam.append({'E_N_per_mm2_assumed':E,'span_mm':200,'I_mm4':cfI,
                         'center_load_N':force,'deflection_mm':force*200**3/(48*E*cfI)})
    frame={'outside_envelope_mm':[280,280,300],
           'HFS5_2020_assumed_kg_per_m':.50,'HFS5_2040_kg_per_m':.88,
           'cut_scheme':{'2020_260mm':4,'2020_280mm':4,'2020_240mm':2,'2040_240mm':2},
           'extrusions_only_mass_g':(.50*(4*.260+4*.280+2*.240)+.88*2*.240)*1000,
           'status':'bounding cut scheme; reconcile joint geometry with CAD cut list'}
    result={'status':'bounded analytical screen; no physically measured masses, modes or acceptance',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'coordinates':'machine mm: X right, Y rear, Z up; not Fusion raw axes',
            'belt_planes_Z_mm':BELT_PLANES_Z,'belt_force_point_mm':BELT_FORCE_POINT,
            'X_rail_center_Z_mm':X_RAIL_CENTER_Z,'nozzle_point_mm':NOZZLE_POINT,
            'head_items':[{'name':p[0],'mass_low_nominal_high_g':p[1],'centroid_mm':p[2],
                           'local_inertia_box_mm':p[3],'evidence':p[4]} for p in HEAD],
            'head_nominal_mass_g':nominal_mass,'head_mass_bounds_g':head_bounds,
            'head_nominal_COM_mm':nominal_com,
            'head_COM_bounds_only_from_mass_uncertainty_mm':mass_corner_com_bounds(HEAD),
            'head_nominal_inertia_kg_m2':inertia(HEAD,nominal_com),
            'balanced_candidate':{'motor_centroid_mm':balanced[0][2],'COM_mm':bc,
                                 'inertia_kg_m2':inertia(balanced,bc),
                                 'remaining_belt_z_lever_mm':bc[2]-BELT_FORCE_POINT[2],
                                 'motor_centroid_for_exact_balance_mm':required_motor_position(HEAD),
                                 'status':'mass-only candidate; physical mount/shaft/clearance pending'},
            'force_and_moment_sensitivity':[moments(bm,bc,a) for a in (10000,100000,250000,2000000)],
            'gantry_additional_items':GANTRY_EXTRA,'gantry_extra_nominal_mass_g':gantry_nom,
            'gantry_extra_bounds_g':gantry_bounds,
            'translating_X_nominal_g':moving_x,'translating_Y_nominal_g':moving_y,
            'translating_Y_bounds_g':[head_bounds[k]+gantry_bounds[k] for k in (0,1)],
            'bed_Al_100x100x4_mass_g':100*100*4*2.70/1000,
            'frame':frame,'motor_inertia_screen':effective,'dynamic_sensitivity':dynamic,
            'free_two_inertia_relative_mode':rotor_relative,
            'carbon_beam_screen':beam,
            'excluded':['idler/pulley inertia','compliant hose force and asymmetric wire drag',
                        'vendor centroid/dimension variation','motor electrical/tracking dynamics',
                        'belt tension/dynamic travelling-span effective mass',
                        'frame joints/rocking/shear modes','rail/carriage preload and moment ratings']}
    (ROOT/'REVF-MASS-DYNAMICS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    selected=next(x for x in effective if x['teeth']==36)
    lines=['# Rev F bounded mass, balance and vibration screen','',
           '**Calculated, not measured.** Run `python REVF-MASS-DYNAMICS.py` in the engineering folder to reproduce the paired JSON. This model does not change Fusion. Coordinates are machine X/right, Y/rear, Z/up.', '',
           f'The illustrative complete head is **{nominal_mass:.1f} g nominal**, with an assumed **{head_bounds[0]:.1f}–{head_bounds[1]:.1f} g** bracket. Goliath AIR and Sherpa Micro supplier masses and exact mounting interfaces remain pending; 200 g is a goal, not an actual mass.', '',
           '| Head item | Low / nominal / high g | Illustrative centroid XYZ mm |',
           '|---|---:|---|']
    for p in HEAD: lines.append(f'| {p[0]} | {p[1][0]} / {p[1][1]} / {p[1][2]} | {p[2]} |')
    lines += ['', f'The original arrangement COM is ({nominal_com[0]:.2f}, {nominal_com[1]:.2f}, {nominal_com[2]:.2f}) mm. Belt force planes are Z284/Z294, whose mean is Z289; the X rail center is Z280 and the nozzle is Z225.', '',
              f'A mass-only search with motor centroid Y0–35/Z300–325 mm places the motor at **{balanced[0][2]} mm**, giving head COM **({bc[0]:.2f}, {bc[1]:.2f}, {bc[2]:.2f}) mm**. Remaining vertical lever is **{bc[2]-289:.2f} mm**. Exact nominal balance would require motor centroid {tuple(round(x,2) for x in required_motor_position(HEAD))} mm, outside the searched Z envelope. The gear shaft, nozzle path, hotend mount and top-frame clearance must make any chosen placement physically possible.', '',
              'Do not add ballast to force balance. If raising the motor adds a flexible tower, move the belt-force planes nearer the actual COM or shorten/raise the hotend stack. Keep belt spacing adequate for the 9 mm belt hardware. A small remaining offset is preferable to a weak bracket or large mass increase.', '',
              f'The CF tube is {GANTRY_EXTRA[0]["mass_g"]:.2f} g at 1.6 g/cm³, and the 180 mm MGN7 rail is 39.6 g at the HIWIN rate. Other gantry contributions total **{gantry_nom:.1f} g**, giving **X {moving_x:.1f} g / Y {moving_y:.1f} g** translating nominal masses. The Y bracket is **{result["translating_Y_bounds_g"][0]:.1f}–{result["translating_Y_bounds_g"][1]:.1f} g**. The proposed guide/head combination therefore does not establish the earlier ≤300 g Y target.', '',
              f'The 100×100×4 mm aluminium bed is **{result["bed_Al_100x100x4_mass_g"]:.0f} g**, before surface/heater/support. It moves only in Z. The example extrusion cut scheme totals **{frame["extrusions_only_mass_g"]:.1f} g** before joints/panels; reconcile it with CAD before pricing.', '',
              '| Acceleration mm/s² | Head inertia N | Moment about belt point, X acceleration XYZ Nm |',
              '|---:|---:|---|']
    for q in result['force_and_moment_sensitivity']:
        lines.append(f'| {q["acceleration_mm_s2"]} | {q["inertia_force_N"]:.2f} | {tuple(round(x,4) for x in q["X_accel_moment_Nm"])} |')
    lines += ['', 'The full local-envelope inertia tensor and parallel-axis calculation are in JSON. Hollow printed-part envelope inertia is approximate. Nozzle-to-bearing offset also creates a load path even if total COM is balanced.', '',
              '## Four-motor rotor and torque screen', '',
              '| Pulley | Four-rotor equivalent g | RPM at 1500 mm/s tool speed, 45° | Y250k ideal torque / motor Nm | With 30% reserve Nm |',
              '|---:|---:|---:|---:|---:|']
    for p in effective:
        q=next(c for c in p['torque_cases'] if c['axis']=='Y' and c['acceleration_mm_s2']==250000)
        lines.append(f'| {p["teeth"]}T | {p["four_rotor_equivalent_mass_g"]:.1f} | {p["RPM_at_1500_mm_s_45deg_toolpath"]:.0f} | {q["ideal_torque_Nm_per_motor"]:.3f} | {q["required_operating_torque_30pct_reserve_Nm"]:.3f} |')
    lines += ['', 'These pure-axis torque cases use four LDO rotor inertias of 8.45×10⁻⁶ kg m², perfect load sharing, and omit pulley/idler inertia and friction. Diagonal moves require the full CoreXY transform. Holding torque is not operating torque. A 48 V capability claim needs the matching voltage/current driver curve or measurement.', '',
              '## Vibration and stiffness sensitivity', '',
              'Effective belt/rail/joint stiffness is not measured. The JSON sweeps 10–1000 N/mm, damping ratios 0.01/0.03/0.08, and head/Y translating masses and bounds. For a motor-end held fixed, natural frequency is sqrt(k/m)/(2π); the approximate 2% ring-down time is 4/(ζω). Damping and stiffness values are sensitivity inputs, never calibrated input-shaper settings.', '',
              '| Effective stiffness N/mm | Y translating frequency Hz | Static deflection at 250k mm/s² | 2% settle at ζ0.03 s |',
              '|---:|---:|---:|---:|']
    for p in dynamic:
        if p['mass_basis']=='Y translation' and p['damping_ratio']==.03:
            lines.append(f'| {p["stiffness_N_per_mm"]} | {p["frequency_Hz"]:.1f} | {p["static_deflection_mm_at_250k_accel"]:.3f} mm | {p["two_percent_settle_s_approx"]:.3f} |')
    lines += ['', 'Do not add rotor equivalent mass to the moving load when calculating belt stretch under prescribed axis acceleration: motor torque also accelerates its own rotor. For an ideal free two-inertia system with one spring between Y and the four-rotor equivalent, a separate JSON table gives the relative mode sqrt(k×(1/M_Y+1/M_rotor))/(2π); it also has a zero-frequency rigid-body mode. Actual motor electrical stiffness, drive control, multiple spans and frame modes change this. Static force/deflection is a compliance warning, not a prediction of printed error.', '',
              'For the carbon tube alone, I=6373 mm⁴. At 70 GPa assumed longitudinal modulus and 200 mm simply supported span, a 50 N center load gives 0.019 mm bending. End blocks, rail eccentricity, laminate shear, holes and joints can dominate. MISUMI HFS5-2040 published second moments are 13,580/51,300 mm⁴; use the strong orientation intentionally. The frame still needs metal joint load paths and shear restraint.', '',
              '## Sources and what must be replaced', '',
              '- [HIWIN guideway catalogue](https://www.hiwin.com/wp-content/uploads/HIWIN-Linear-Guideway-Catalog.pdf): MGN7 rail rate and MGN7H mass retained from the earlier inspected source; MGN9H mass bracket needs exact SKU verification.',
              '- [MISUMI HFS5-2040](https://jp.misumi-ec.com/vona2/detail/110302684350/): 0.88 kg/m and listed section properties. HFS5-2020 0.50 kg/m is retained from the [MISUMI catalogue](https://sg.misumi-ec.com/pdf/fa/2010/p2_0481.pdf); current cut/joint layout is illustrative.',
              '- [Sherpa Micro maker repository](https://github.com/Annex-Engineering/Sherpa_Micro-Extruder): Release 2 interface/BOM reference; a complete weighed mass was not found here. [Annex motor/force study](https://github.com/Annex-Engineering/Annex-Engineering.github.io/blob/master/extruder_force.md) gives 70 g for a prior Mini motor, which is contextual, not a Micro assembly mass.',
              '- [Goliath maker assembly guide](https://docs.vzbot.org/goliath/assembly): AIR version needs a 2510 cold-end fan and stabilized fan duct. Purchased component complete mass remains a bracket.',
              '- [LDO official product](https://ldomotion.com/products/ldo42sth482504ac) and preserved vendor drawing: exact rotor/current references; 48 V operating torque remains unverified.', '',
              'Replace estimated masses with supplier data and a scale, replace centroids with completed CAD placements, add inertia of every rotating pulley, and measure nozzle/gantry/frame response. Commission from low acceleration. The old 53.54 s planner scenario and these mass sensitivities do not establish a sub-minute physical printer.']
    (ROOT/'REVF-MASS-DYNAMICS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'head_mass_nominal_g':nominal_mass,'head_mass_bounds_g':head_bounds,
                      'initial_COM_mm':nominal_com,'candidate_COM_mm':bc,'motor_centroid_mm':balanced[0][2],
                      'Y_mass_nominal_g':moving_y,'Y_mass_bounds_g':result['translating_Y_bounds_g'],
                      'output_files':['REVF-MASS-DYNAMICS.json','REVF-MASS-DYNAMICS.md']},indent=2))

if __name__=='__main__':
    run()
