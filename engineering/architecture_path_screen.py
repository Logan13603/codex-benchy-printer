"""Pre-CAD transmission screen. This is NOT a validated machine time prediction.

Each segment receives a fixed acceleration cap using the lowest documented
running torque from zero to its allowed motor speed. This is conservative for
torque as the segment may never reach that speed. Conversely, no belt/frame
flex, shaper delay, extrusion-force junction or hose dynamics are simulated.
The delta case is a center-workspace linearization, not full delta dynamics.
Units inside force calculations: m, s, kg, N. Planner uses mm and s.
"""
import math,json,hashlib
from functools import lru_cache
from path_model import ROOT,parse,duration,summarize

J=8.45e-6
RPM=[60,180,300,420,540,660,780,900,1020,1140,1260,1380,1500,1620,1740,1860,1980,2100]
TORQUE=[.401,.420,.451,.471,.492,.478,.430,.386,.347,.314,.287,.261,.239,.224,.205,.194,.181,.168]
MASS={'cartesian':(.140,.090),'corexy':(.140,.325),'crossed':(.235,.235)}
CURVE='https://cdn.shopify.com/s/files/1/0239/9287/files/LDO-42STH48-2504AC_Torque_Curve.pdf?v=1645112191'

def torque_floor(rpm):
    """No extrapolation above the published curve; first point below 60 RPM."""
    if rpm>2100+1e-7:raise ValueError('outside measured speed range')
    if rpm<=60:return TORQUE[0]
    for i in range(1,len(RPM)):
        if rpm<=RPM[i]:
            t=TORQUE[i-1]+(TORQUE[i]-TORQUE[i-1])*(rpm-RPM[i-1])/(RPM[i]-RPM[i-1])
            return min(TORQUE[:i]+[t])
    return min(TORQUE)

def coefficients(kind,teeth,u,mass_scale=1.):
    """Return motor speed ratios and N per m/s2 for signed XY acceleration."""
    x,y=u; r=teeth*.002/(2*math.pi); jr=J/r**2
    # 9 mm pulley/idler inertia expressed as an assumed equivalent mass.
    extra=.015
    if kind=='corexy':
        mx,my=(v*mass_scale for v in MASS[kind])
        return (x+y,x-y),(.5*(mx*x+my*y)+(jr+extra)*(x+y),
                          .5*(mx*x-my*y)+(jr+extra)*(x-y))
    if kind=='delta-center':
        # Equal towers, 85 mm effective rod offset / 160 mm rods at XY center.
        k=.085/math.sqrt(.160**2-.085**2)
        ratios=tuple(k*(math.cos(a)*x+math.sin(a)*y) for a in (0,2*math.pi/3,4*math.pi/3))
        # J.T*F=m*a. At symmetry, horizontal solution F=m*J*u/(1.5*k^2).
        mhead=.158*mass_scale; mcar=.026*mass_scale
        c=tuple((mhead/(1.5*k*k)+mcar+jr+extra)*j for j in ratios)
        return ratios,c
    mx,my=(v*mass_scale for v in MASS[kind])
    sync=.030 if kind=='crossed' else 0.
    return (x,y),((mx+jr+extra+sync)*x,(my+jr+extra+sync)*y)

@lru_cache(maxsize=200000)
def cap(kind,teeth,x,y,mass_scale=1.,drag=2.,reserve=.30):
    ratios,c=coefficients(kind,teeth,(x,y),mass_scale)
    r=teeth*.002/(2*math.pi)
    vmax=min(2.,(2100/60*2*math.pi*r)/max(abs(j) for j in ratios))
    acceleration=100. # generous common rigid-mechanism ceiling; not achievable rating
    for ratio,coefficient in zip(ratios,c):
        rpm=vmax*abs(ratio)/(2*math.pi*r)*60
        force=(1-reserve)*torque_floor(rpm)/r
        # Delta supports static head/rod/carriage weight even during horizontal motion.
        gravity=(.158*mass_scale/3+.026*mass_scale)*9.80665 if kind=='delta-center' else 0.
        usable=force-drag-gravity
        if abs(coefficient)>1e-12:acceleration=min(acceleration,max(0.,usable)/abs(coefficient))
    return vmax*1000,acceleration*1000

def caps_for(moves,kind,teeth,mass_scale=1.,drag=2.):
    values=[]
    for m in moves:
        if not m.xyz or abs(m.u[2])>1e-8:values.append((2000.,100000.));continue
        values.append(cap(kind,teeth,m.u[0],m.u[1],mass_scale,drag))
    return values

def run():
    # Independent force/energy identity checks catch factors of two in CoreXY.
    for kind in MASS:
        ratios,c=coefficients(kind,20,(1.,0.))
        expected=MASS[kind][0]+(2 if kind=='corexy' else 1)*(J/(.040/(2*math.pi))**2+.015)
        if kind=='crossed':expected+=.030
        assert abs(sum(a*b for a,b in zip(ratios,c))-expected)<1e-12
    assert torque_floor(2100)==.168 and torque_floor(0)==.401
    path=ROOT/'slicing/cura-4.13.1-simplified/analysis.gcode';moves=parse(path)
    result={'status':'screening scenarios; no selected architecture or build release',
      'gcode_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'summary':summarize(moves),
      'motor_curve':CURVE,'curve_conditions':'24 V, 2.5 A, full step, 200 steps/revolution; actual driver equivalence unverified',
      'pulley_assumption':'2 mm pitch, 9 mm belt; user pulley tooth count and pitch unknown',
      'assumed_9mm_pulley_idler_reflected_mass_kg_per_motor':.015,
      'rotor_inertia_kg_m2':J,'translating_mass_kg':MASS,'runs':[],'mass_drag_sensitivity':[]}
    for kind in ['cartesian','corexy','crossed','delta-center']:
        for teeth in (16,20,24,32):
            caps=caps_for(moves,kind,teeth)
            row={'architecture':kind,'teeth':teeth,'min_segment_accel_mm_s2':min(a for v,a in caps),
                 'max_segment_accel_mm_s2':max(a for v,a in caps),'scenarios':[]}
            for flow in (75,200):
                d=duration(moves,flow,2000,100000,100,axis_caps=caps)
                row['scenarios'].append(d)
            result['runs'].append(row)
            print(kind,teeth,[(r['assumed_flow_cap_mm3_s'],round(r['seconds'],2)) for r in row['scenarios']],flush=True)
        # Sensitivity held at 20T; does not invent a known owned pulley size.
        for scale,drag in [(0.75,1.),(1.25,4.)]:
            d=duration(moves,200,2000,100000,100,axis_caps=caps_for(moves,kind,20,scale,drag))
            result['mass_drag_sensitivity'].append({'architecture':kind,'teeth':20,'translating_mass_scale':scale,'drag_N_per_motor':drag,**d})
    result['limitations']=[
      'Acceleration caps use torque minima up to allowed segment speed, including speeds never reached; conservative within that torque model.',
      'All cases assume the documented full-step current/voltage curve is available. This is not verified for the candidate controller.',
      'Delta is linearized at workspace center; Jacobian variation, velocity-squared forces and tilt stiffness are omitted. Delta time is not a nominal prediction.',
      'No belt compliance, frame flex, actual hose drag curve, thermal droop, pressure advance, input shaping or extrusion-ratio junction checks.',
      'Short Bowden only; direct drive adds the independently tabulated toolhead mass and has not been shown to improve this path.',
      'No architecture-specific delivered BOM is frozen; reference cost is for a two-XY-motor Cartesian/CoreXY-class layout, not a delta quote.'
    ]
    (ROOT/'engineering/architecture-path-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':run()
