"""Heat/airflow sensitivity, no claimed heat-transfer validation."""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run():
    # cp bracket is an assumption, varies with formulation and temperature.
    thermal=[{'flow_mm3_s':q,'feed_mm_s':q/(math.pi*1.75**2/4),'mass_g_s':q*.00124,
              'sensible_heat_W_range':[q*.00124*cp*(240-25) for cp in (1.5,2.)]}
             for q in (75,100,150,160,200)]
    # Hose 0.6m long, ID15mm; Darcy factor0.035..0.08 for uncertain corrugation;
    # turns/connectors sumK3. Four outlets10x2mm, Cd0.7. Ambient rho1.2 kg/m3.
    hose=[]
    for flow_l_s in (2,3,4,5):
        q=flow_l_s/1000; v=q/(math.pi*.015**2/4)
        dyn=.5*1.2*v*v
        outlet=.5*1.2*(q/(.7*80e-6))**2
        losses=[(f*.6/.015+3)*dyn+outlet for f in (.035,.08)]
        hose.append({'flow_L_s':flow_l_s,'hose_speed_m_s':v,
                     'system_pressure_Pa_range':losses,
                     'outlet_speed_m_s':q/80e-6,'bulk_air_W_per_K':q*1.2*1005,
                     'outlet_momentum_force_N':1.2*q*q/80e-6})
    data={'thermal':thermal,'duct_sensitivity':hose,
          'not_validated':['Polymer cp bracket excludes phase-transition enthalpy and heater losses.',
              'No measured nozzle pressure/temperature or filament formulation data.',
              'Full blower pressure-flow curve at each PWM setting not digitized.',
              'No heat-transfer coefficient, printed-part temperature field, or hose-force measurement.',
              'Heat-removal capacity of air is not proof of cooling at the nozzle or on bridges.']}
    (ROOT/'engineering/thermal_cooling_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':run()
