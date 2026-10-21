# Rev F bounded mass, balance and vibration screen

**Calculated, not measured.** Run `python REVF-MASS-DYNAMICS.py` in the engineering folder to reproduce the paired JSON. This model does not change Fusion. Coordinates are machine X/right, Y/rear, Z/up.

The illustrative complete head is **255.0 g nominal**, with an assumed **188.0–335.0 g** bracket. Goliath AIR and Sherpa Micro supplier masses and exact mounting interfaces remain pending; 200 g is a goal, not an actual mass.

| Head item | Low / nominal / high g | Illustrative centroid XYZ mm |
|---|---:|---|
| Micro motor | 60 / 70 / 80 | [0, 15, 318] |
| Micro gears and printed body | 20 / 27 / 35 | [0, -18, 303] |
| Goliath AIR hotend complete | 55 / 80 / 105 | [0, -18, 257] |
| 2510 cold-end fan | 4 / 6 / 9 | [0, -35, 275] |
| MGN7H carriage | 15 / 15 / 15 | [0, 0, 280] |
| Carriage/hotend printed support | 10 / 15 / 22 | [0, -5, 285] |
| Symmetric CPAP duct | 8 / 15 / 22 | [0, -18, 240] |
| Supported CPAP hose length | 5 / 10 / 20 | [0, 15, 300] |
| Supported harness length | 3 / 5 / 9 | [0, 8, 293] |
| Screws, inserts, belt clamps | 7 / 10 / 15 | [0, -2, 283] |
| Filament and guide PTFE | 1 / 2 / 3 | [0, -18, 310] |

The original arrangement COM is (0.00, -5.09, 284.87) mm. Belt force planes are Z284/Z294, whose mean is Z289; the X rail center is Z280 and the nozzle is Z225.

A mass-only search with motor centroid Y0–35/Z300–325 mm places the motor at **[0, 34, 325] mm**, giving head COM **(0.00, 0.13, 286.79) mm**. Remaining vertical lever is **-2.21 mm**. Exact nominal balance would require motor centroid (0.0, 33.53, 333.06) mm, outside the searched Z envelope. The gear shaft, nozzle path, hotend mount and top-frame clearance must make any chosen placement physically possible.

Do not add ballast to force balance. If raising the motor adds a flexible tower, move the belt-force planes nearer the actual COM or shorten/raise the hotend stack. Keep belt spacing adequate for the 9 mm belt hardware. A small remaining offset is preferable to a weak bracket or large mass increase.

The CF tube is 35.52 g at 1.6 g/cm³, and the 180 mm MGN7 rail is 39.6 g at the HIWIN rate. Other gantry contributions total **167.1 g**, giving **X 255.0 g / Y 422.1 g** translating nominal masses. The Y bracket is **330.7–534.6 g**. The proposed guide/head combination therefore does not establish the earlier ≤300 g Y target.

The 100×100×4 mm aluminium bed is **108 g**, before surface/heater/support. It moves only in Z. The example extrusion cut scheme totals **1742.4 g** before joints/panels; reconcile it with CAD before pricing.

| Acceleration mm/s² | Head inertia N | Moment about belt point, X acceleration XYZ Nm |
|---:|---:|---|
| 10000 | 2.55 | (0, -0.0056, -0.0003) |
| 100000 | 25.50 | (0, -0.0564, -0.0033) |
| 250000 | 63.75 | (0, -0.141, -0.0083) |
| 2000000 | 510.00 | (0, -1.128, -0.066) |

The full local-envelope inertia tensor and parallel-axis calculation are in JSON. Hollow printed-part envelope inertia is approximate. Nozzle-to-bearing offset also creates a load path even if total COM is balanced.

## Four-motor rotor and torque screen

| Pulley | Four-rotor equivalent g | RPM at 1500 mm/s tool speed, 45° | Y250k ideal torque / motor Nm | With 30% reserve Nm |
|---:|---:|---:|---:|---:|
| 20T | 834.0 | 3182 | 0.500 | 0.714 |
| 24T | 579.2 | 2652 | 0.478 | 0.683 |
| 32T | 325.8 | 1989 | 0.476 | 0.680 |
| 36T | 257.4 | 1768 | 0.487 | 0.695 |
| 40T | 208.5 | 1591 | 0.502 | 0.717 |

These pure-axis torque cases use four LDO rotor inertias of 8.45×10⁻⁶ kg m², perfect load sharing, and omit pulley/idler inertia and friction. Diagonal moves require the full CoreXY transform. Holding torque is not operating torque. A 48 V capability claim needs the matching voltage/current driver curve or measurement.

## Vibration and stiffness sensitivity

Effective belt/rail/joint stiffness is not measured. The JSON sweeps 10–1000 N/mm, damping ratios 0.01/0.03/0.08, and head/Y translating masses and bounds. For a motor-end held fixed, natural frequency is sqrt(k/m)/(2π); the approximate 2% ring-down time is 4/(ζω). Damping and stiffness values are sensitivity inputs, never calibrated input-shaper settings.

| Effective stiffness N/mm | Y translating frequency Hz | Static deflection at 250k mm/s² | 2% settle at ζ0.03 s |
|---:|---:|---:|---:|
| 10 | 24.5 | 10.553 mm | 0.866 |
| 25 | 38.7 | 4.221 mm | 0.548 |
| 50 | 54.8 | 2.111 mm | 0.387 |
| 100 | 77.5 | 1.055 mm | 0.274 |
| 250 | 122.5 | 0.422 mm | 0.173 |
| 500 | 173.2 | 0.211 mm | 0.123 |
| 1000 | 245.0 | 0.106 mm | 0.087 |

Do not add rotor equivalent mass to the moving load when calculating belt stretch under prescribed axis acceleration: motor torque also accelerates its own rotor. For an ideal free two-inertia system with one spring between Y and the four-rotor equivalent, a separate JSON table gives the relative mode sqrt(k×(1/M_Y+1/M_rotor))/(2π); it also has a zero-frequency rigid-body mode. Actual motor electrical stiffness, drive control, multiple spans and frame modes change this. Static force/deflection is a compliance warning, not a prediction of printed error.

For the carbon tube alone, I=6373 mm⁴. At 70 GPa assumed longitudinal modulus and 200 mm simply supported span, a 50 N center load gives 0.019 mm bending. End blocks, rail eccentricity, laminate shear, holes and joints can dominate. MISUMI HFS5-2040 published second moments are 13,580/51,300 mm⁴; use the strong orientation intentionally. The frame still needs metal joint load paths and shear restraint.

## Sources and what must be replaced

- [HIWIN guideway catalogue](https://www.hiwin.com/wp-content/uploads/HIWIN-Linear-Guideway-Catalog.pdf): MGN7 rail rate and MGN7H mass retained from the earlier inspected source; MGN9H mass bracket needs exact SKU verification.
- [MISUMI HFS5-2040](https://jp.misumi-ec.com/vona2/detail/110302684350/): 0.88 kg/m and listed section properties. HFS5-2020 0.50 kg/m is retained from the [MISUMI catalogue](https://sg.misumi-ec.com/pdf/fa/2010/p2_0481.pdf); current cut/joint layout is illustrative.
- [Sherpa Micro maker repository](https://github.com/Annex-Engineering/Sherpa_Micro-Extruder): Release 2 interface/BOM reference; a complete weighed mass was not found here. [Annex motor/force study](https://github.com/Annex-Engineering/Annex-Engineering.github.io/blob/master/extruder_force.md) gives 70 g for a prior Mini motor, which is contextual, not a Micro assembly mass.
- [Goliath maker assembly guide](https://docs.vzbot.org/goliath/assembly): AIR version needs a 2510 cold-end fan and stabilized fan duct. Purchased component complete mass remains a bracket.
- [LDO official product](https://ldomotion.com/products/ldo42sth482504ac) and preserved vendor drawing: exact rotor/current references; 48 V operating torque remains unverified.

Replace estimated masses with supplier data and a scale, replace centroids with completed CAD placements, add inertia of every rotating pulley, and measure nozzle/gantry/frame response. Commission from low acceleration. The old 53.54 s planner scenario and these mass sensitivities do not establish a sub-minute physical printer.
