# Rev F Bowden toolhead, CPAP duct and hose design basis

2026-10-20. The user now requires **Bowden extrusion**. The Sherpa Micro and its motor mount to the frame; neither belongs in the moving-head mass. This supersedes the direct-drive placement study in `REVF-MASS-DYNAMICS.md`. It is a CADable development specification, with explicit purchased-interface and physical-test holds before manufacturing release.

## Datums and purchased components

Machine coordinates: X right, Y rear, Z up. Nominal nozzle tip `(0, −38, 225)` mm; carbon X beam center Y0/Z280, section 20×20 mm; carriage mounting front plane Y−18; belt planes Z284/Z294, mean Z289. The belt resultant's Y coordinate has not been frozen; moment examples below assume Y−18 and must be updated to the actual clamp force path.

The previously imported Goliath AIR mockup has stated source bounds X−27.93…15.98, Y−22.88…15.98 and Z−25.76…43.51 mm. Placing its tip at the stated nozzle datum gives the working assembly envelope X−27.93…15.98, Y−60.88…−22.02, Z225…294.27 mm. This is a whole-model clearance envelope, including asymmetrical features; it is not the hot-block boundary at every height. The top mounting plane is Z294.26/294.27 within rounding. The four reported M2.5 mounting holes at X±5.657, Y−38±5.657 need depth, thread engagement and screw-head access checked against the actual purchased revision. The imported model is a mockup, not a verified purchased assembly mass.

The [Goliath maker assembly guide](https://docs.vzbot.org/goliath/assembly) specifies a separate 2510 cold-end fan and stabilized fan shroud. Its heater leads and PT1000 sensor need tool access and strain relief. Reserve the actual lead route, not merely the metal block. CPAP part cooling does not replace cold-end cooling.

The [Sherpa Micro maker repository](https://github.com/Annex-Engineering/Sherpa_Micro-Extruder) supplies standard Release 2. Use its standard spring idler, not the fixed-idler public Alpha, which the maker identifies as experimental. The official standard STL directory contains `housing_core`, `housing_front`, `housing_rear`, and `idler_arm_long`; `housing_front_k` and `idler_arm_short` are optional alternatives. In the imported assembly, suppress those alternative occurrences from the active standard assembly. Preserve them in a separate source-reference component. The source `adapter` can likewise be excluded when a custom frame mount replaces it. Keep bearings, shared hardware, gears, pins and motor; overlap alone is not a reason to delete them.

Source datum extraction supplied by the CAD integration work: Sherpa outlet `(4.3, −13.5, 6)` along sourceY; front M3 mounting axes at `(−9.7, −13.5, 6)` and `(22.3, −13.5, 6)`,32 mm pitch. These are useful frame-mount datums, not a moving-head attachment. The previous sourceX→machineX/sourceY→machineZ/sourceZ→−machineY orientation is optional on the fixed bracket; keep a straight, serviceable exit path to the Bowden tube.

## Bowden routing and interfaces

Start with **4 mm OD,2 mm ID PTFE, approximately 220 mm long**. Use a frame-fixed extruder outlet approximately above the center of travel, with an overhead support near `(0, −38, 410)` mm, and a head tube-entry datum near `(0, −38, 304)` mm. These are layout points. The hotend's actual PTFE seating depth, collet/fitting type, insertion stop, temperature boundary and connector body must be confirmed before drilling a final inlet. Do not put a guessed pneumatic thread into the heatsink or let PTFE enter an unverified hot zone.

At ±40 mm XY travel, the largest endpoint horizontal separation is 56.6 mm. With 106 mm vertical separation the straight chord is 120.1 mm, so a 220 mm tube leaves about 100 mm for a gentle service loop. Model that loop with explicit swept OD and **at least 40 mm provisional bend radius**, then inspect every corner of travel. This bend radius is a conservative layout allowance, not a supplier-certified value. Keep the tube outside belts and hot surfaces. Its sleeve must not cross the cold-fan inlet. Provide a positive collet clip and retention at both ends; include fitting slip in the measured extrusion-response test.

Keep the fixed extruder/first tube support rigid. A swing arm that moves freely in XY can remove some drag but changes the stored tube shape and adds an unmodeled mode; it is not automatically better. Route the Bowden and CPAP separately so their bends do not push each other around. The CPAP hose should receive most of its weight from an independent overhead sling; the PTFE guide should carry only the filament and its own loop.

The complete 220 mm 4×2 mm PTFE tube is about 4.46 g at the assumed 2.15 g/cm³ density. Effective carried mass depends on the support. Do not count the entire tube as rigidly translating, and do not treat supported mass as proof of negligible endpoint force.

For an illustrative straight-tube elastic screen:

`C = L/(E_PLA × A_filament) + L/(E_PTFE × A_tube)`

Use filament diameter 1.75 mm, `A_filament=2.4053 mm²`, `A_tube=9.4248 mm²`, assumed room-temperature PLA modulus 2–3 GPa, and PTFE tangent modulus 0.4–0.8 GPa. These are sensitivity assumptions, not this spool/tube's measured modulus. At 220 mm, `C=0.0597–0.1041 mm/N`. A40 N feed-force change stores **2.39–4.16 mm of filament-equivalent displacement**, about **5.74–10.02 mm³**. At 200 mm³/s that volume corresponds to 29–50 ms; this quotient is not an identified pressure time constant. Bowden curvature/buckling clearance, tube creep, fittings, friction and the hotend's own pressure storage are additional.

For 180/260 mm tube lengths, the same elastic screen gives 0.0488–0.0852/0.0705–0.1230 mm/N. Shortening the tube reduces axial compliance but increases bending stiffness and can worsen head drag. A simple straight-beam screen for 220 mm 4×2 PTFE and 56.6 mm lateral motion gives roughly 0.075–0.60 N, depending on end rotation constraint and assumed modulus. Real curved-loop endpoint force requires a spring-scale measurement across the whole workspace. Target less than 0.5 N lateral drag initially; this is an acceptance target, not a prediction.

The [Annex firmware starting block](https://github.com/Annex-Engineering/ANNEX-Printer-Firmware/blob/main/Klipper_and_Klipper_Derivatives/Sherpa_Mini/Klipper_Config_Block.txt) gives 22.67895 mm gear-shaft rotation distance for the referenced Bondtech gearsets. With the Micro's supported 50:10 gearing, nominal motor RPM at 100/150/200/300 mm³/s is approximately 550/825/1100/1650, before pressure advance. The exact gearset and measured rotation distance must match.50:8 raises motor RPM another 25%; use 50:10 as the first high-flow candidate, subject to force testing.

[Klipper's pressure-advance documentation](https://www.klipper3d.org/Pressure_Advance.html) explains that pressure advance adds extruder movement during acceleration and can exceed available torque. Its [configuration reference](https://www.klipper3d.org/Config_Reference.html#extruder) distinguishes extrusion-only limits from normal printing moves. Raising a software velocity limit does not supply torque. Leave PA unvalidated until the actual Bowden loop/nozzle/filament is tuned at relevant flow transitions. Goliath plus an eligible 0.5 mm nozzle has not been demonstrated here to supply the old 300 mm³/s requirement.

## Symmetric part-cooling geometry

Use two equal left/right branches and replaceable opposing mouths. Give each mouth **16×3 mm clear area**, long dimension alongY, total 96 mm². Nominal mouth centers are `(−12, −38, 227.5)` and `(+12, −38, 227.5)` mm. The lower lips sit atZ226,1 mm above the nozzle. Aim their central axes at `(0, −38, 225)`, approximately 11.8° downward from horizontal. The jets overlap close to the deposition zone; do not point them at the heater body.

Those mouth positions assume the nozzle shoulder leaves the necessary space atZ226…229. Check the actual imported solid at those sections. A whole-model bounding box cannot verify that region. Increase mouth stand-off or raise lips if nozzle/wrench/sock geometry conflicts, then recompute the jet direction. Keep an unobstructed cone below the tip and ensure a slightly curled printed edge cannot catch a lower duct lip.

| Feature | CAD starting value | Release condition |
|---|---|---|
| Main trunk clear bore |22 mm | Match owned hose/blower adapter after measurement |
| Trunk collar |25 mm nominal OD,28 mm shoulder maximum | Real cuff clamp, retention and bend envelope pending |
| Trunk axis |X0/Y−60, Z308…330 | Bowden atY−38 must retain 6 mm or greater clearance to a 28 mm shoulder |
| Header |Equal split above/in front of the hotend, targetZ304…318 | Clear top mount screws, collet, cold-fan inlet and frame motors |
| Each branch clear section |12×10 mm | Area 120 mm² per branch; no narrower hidden throat |
| Straight side trunks |Centers X±42/Y−38; descend towardZ250 | Conservative 4 mm outer-model clearance and 8 mm hot-surface allowance, checked on actual solids |
| Outlet transition |Side trunk → approximatelyX±24/Z235 → mouthX±12/Z227.5 | Exact spline path must avoid heater wire, sock, sensor and wrench access |
| Wall |1.2 mm minimum; mounting tabs 2.4–3 mm | Reconcile slicer wall count, hole edge distance and pressure test |
| Curved-flow centerline radius |≥12 mm initial target | Avoid abrupt right-angle flow turns and excessive area expansion |
| Left/right flow-path length |Within 2 mm initially | Installed measured flow within±10% |

The source's heater-wire asymmetry means symmetric ducts need space based on the larger side. The ±42 mm trunk position is intentionally conservative; exact solid sections may permit inward movement and lower duct mass/inertia. Do not place a trunk where it only looks clear in one view. Reserve at least 3 mm to a cold rigid purchased body,5 mm to moving tubes/wires, and 8 mm initially to hot block/lead/sock surfaces. These are layout allowances; the final thermal soak may require more spacing or a small metal radiation shield.

The branch side runs can lie in planesY−38 and split into front/rear clamshells along that plane, exposing their full internal passages for printing and inspection. The upper header needs its own split along a plane that opens the bifurcation. Use locating tongues 0.6–0.8 mm deep, generous sealing lands, and accessible M2 screws or a material-compatible bonded seam after flow testing. Avoid trapped printed supports. Keep interchangeable mouth tips removable using two small screws each; use a sealing shoulder so their fasteners do not set jet angle by friction alone.

The resulting rigid head envelope is approximatelyX±50, Y−74…−22, Z226…330 before real connector/fan details. Union this with the actual XY travel and frame/pulley/homing volumes. Parts aboveZ300 can overhang the cube's top plane, but the lower side trunks must remain inside the gantry/frame clearance. Moving hose bends also need clearance to the overhead fixed extruder; above-frame geometry is still part of the machine envelope.

## Air and heater interaction

At assumed air density 1.2 kg/m³:

| Installed total flow | Ideal mouth speed | Exit dynamic pressure |
|---:|---:|---:|
|2 L/s (120 L/min) |20.8 m/s |260 Pa |
|3 L/s (180 L/min) |31.3 m/s |586 Pa |
|4 L/s (240 L/min) |41.7 m/s |1042 Pa |

These are continuity/velocity-head calculations, not a blower operating point or cooling proof. A preliminary combined outlet/contraction/bend coefficient of 2–5 would require roughly 0.5–5.2 kPa across the table's endpoints, plus upstream hose losses. That coefficient is an assumed sensitivity bracket; obtain installed pressure and flow. A free-air blower figure cannot determine this. At 4 L/s, air heat capacity is about 4.82 W/K; a 20 K bulk rise carries 96 W, but only an unknown fraction couples to deposited plastic.

Opposing horizontal jet momentum cancels approximately if branch flow matches; a common downward component remains. Hose-pressure thrust, an unequal branch or a curved hose can impose more head moment than the net balanced outlet reaction. Include these forces in testing rather than treating the duct's static COM as sufficient.

Run the separate 2510 cold-end fan whenever the hotend is above its qualified threshold. A candidate fan envelope is 25×25×10 mm, front of the heatsink aroundY−68/Z280, with a removable shroud discharging to the sides. Its exact bolt pattern, airflow direction, voltage, static-pressure curve and source fin clearances remain unresolved. Do not cut final fan holes from the nominal 25 mm size alone. The rear whole-model hotend envelope ends atY−22.02, only about 4 mm in front of the carriage planeY−18; avoid forcing all cold-side exhaust into that narrow gap.

## Moving mass and COM after the Bowden change

The following estimates are mass-placement inputs, not supplier-certified weights or CAD mass properties. Symmetry gives X0 nominal; real heater leads and fan placement can shift it.

| Moving item | Low / nominal / high g | Nominal centroid XYZ mm |
|---|---:|---|
| Goliath AIR complete |55 /80 /105 |(0,−38,263) |
|2510 cold-end fan |4 /6 /9 |(0,−68,280) |
| MGN7H block |15 /15 /15 |(0,−18,280) |
| Toolhead support |8 /12 /18 |(0,−25,286) |
| CPAP header |2 /4 /6 |(0,−54,310) |
| Two branch shells |6 /10 /16 |(0,−38,262) |
| Two mouths |1 /2 /3 |(0,−38,232) |
| Bowden inlet retention |2 /4 /7 |(0,−38,302) |
| CPAP cuff/retainer |1 /2 /4 |(0,−60,318) |
| Effective carried CPAP hose |5 /10 /20 |(0,−30,310) |
| Effective carried PTFE |2 /4 /8 |(0,−38,312) |
| Effective harness |3 /5 /8 |(0,−15,298) |
| Screws/inserts/clamps |6 /8 /12 |(0,−24,287) |
| Supported filament |0.5 /1 /1.5 |(0,−38,307) |

Total **110.5–232.5 g**, nominal **163 g**. Nominal COM is **(0, −35.09,275.83) mm**. A163 g head at 250,000 mm/s² has 40.75 N inertia. Relative to the assumed belt point `(0,−18,289)`, a pureX acceleration produces approximately **0.537 Nm pitch** from the 13.17 mm vertical offset and **0.696 Nm yaw** from the 17.09 mm fore/aft offset. At 100 k those become 0.215/0.279 Nm. Supported hose forces add separate moments.

Removing the high-mounted direct-drive motor lowers the COM substantially. The former motor-balance result cannot be retained. Do not add ballast. Prefer shortening/raising the hotend stack or moving the belt resultant nearer the actual head COM after mass reconciliation. Lowering the belt mean towardZ276 would reduce the drive-induced pitch lever, but rail reaction moments and clamp access still need analysis; changing only a label does not move a force path. A higher nozzle/hotend stack changes bed and cooling geometry, so it requires a coordinated CAD change.

Mass is reduced, but no assumption of a low rotational inertia should be made with long side trunks and a tall supported-hose collar. Compute the finished part centroids/tensors, assign purchased mass overrides and supported-tube mass explicitly, then reconcile this table. Fixed Sherpa components contribute to frame mass, power and vibration, not moving-head COM.

## Manufacture and acceptance

Use the standard Sherpa's [published print settings](https://raw.githubusercontent.com/Annex-Engineering/Sherpa_Micro-Extruder/main/Print_Settings_and_File_Key.txt) for its original parts; the maker recommends ASA or PC options. For custom duct trials, start with ASA at 0.2 mm layers and three 0.4 mm walls, solid sealing/mounting lands, no supports inside channels, and source-qualified material settings. Nylon/PC can be considered with their actual heat and moisture data; a generic material name is not proof of heat resistance. Keep prototype PLA away from the hotend.

Check all seam and outlet dimensions after printing. Ream only cold mounting holes as required; do not drill into purchased heatsink material until its interface is verified. Pressure-test the assembled duct below the blower's maximum operating pressure, inspect for leaks/loose tips, and compare branch delivery. Verify that hotend maintenance can remove the nozzle, sensor, sock and fan without stripping the main carriage.

Before a production release: fit a real Bowden collet and cold fan; check the complete swept loops and service-tool volumes; weigh the head; measure endpoint drag; measure installed blower flow/pressure; perform a hot stationary soak with CPAP both on and off; tune the nozzle/filament extrusion response with the fixed extruder; and then commission increasingly fast complete Benchys. Required acceptance remains three consecutive compliant runs under 60 s. The old 53.54 s planner result, the new lower mass and the nominal airflow calculations do not establish that physical result.
