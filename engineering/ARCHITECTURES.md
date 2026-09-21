# Architecture comparison — revision A, pre-CAD

No architecture is selected for manufacture. These are screening envelopes and mass estimates; the common nozzle/toolpath bottleneck prevents a supported 55-second selection. All four would use the same unscaled model and frozen rules. Checkpoint 004 adds same-path torque screening and two Cura slices with no definite width violations; complete feature/physical compliance remains unverified. See TRANSMISSION-SCREEN.md for current results. The envelope table below preserves the original 136 g head study; the preferred 9 mm case adds a 4 g clamp/saddle allowance to reach 140 g.

| Candidate | Screening geometry | Estimated translating mass | Motor / belt implications | Main limitation |
|---|---|---|---|---|
| Miniature CoreXY | 180 x 180 mm XY structure, 150 mm rails; bed moves only in Z | X 136 g, Y about 320 g including X rail, beam and end carriages | Two belt loops about 0.9–1.2 m each; A=x+y, B=x-y. Two rotor equivalents add 417 g for any XY direction with the studied 20T drive | Diagonal motor speed reaches sqrt(2) times Cartesian speed; belt length, stacked force planes, gantry torsion |
| Independent Cartesian, light bed | About 210 x 190 x 170 mm envelope; X head, Y bed; whole X support lifted slowly in Z | X 136 g; Y 89.7 g including a finished 11 g boat | Independent fixed XY motors; loops about 0.34 m and 0.32 m; one rotor adds 208 g to each axis | Tall hot print accelerates with bed; bed yaw, adhesion, heater cable drag; moving Z support stiffness |
| Crossed gantry Cartesian | About 190 x 190 mm XY frame; intersecting lightweight beams; bed Z | Approximately 230 g equivalent translating load per axis before detailed rod/rail choice | Independent drive, but synchronized ends require additional belt/shaft inertia; about 0.6–0.8 m belt per axis | Alignment and bearing preload can overconstrain the intersection; four guide interfaces cost more |
| Delta | Three towers, roughly 220 mm footprint and 300 mm height; 160 mm rods, 85 mm tower radius screening geometry | 136 g head + estimated 18 g rod contribution; three 26 g tower carriages | Three loops about 0.65 m each. At center h=sqrt(160²−85²)=135.55 mm; tower Jacobian lateral magnitude R/h=0.627. Reflected rotor mass along horizontal motion is about 123 g at center | Jacobian varies over the boat and adds velocity-squared acceleration; rod joints, tower bending and hose torques; three drives |

CoreXY's two motors also supply force together: pure-axis force capacity is approximately twice one motor's belt force. Counting both rotors while counting only one motor's torque would unfairly reject it. Diagonal motion is less favorable because one motor spins faster. Delta's center calculation cannot be transferred to the complete path: the nonlinear Jacobian and its derivative must be evaluated at every position.

The independent-axis machine is the first **budget screening candidate**, because the small bed can weigh less than a moving gantry and the belts are short. This does not establish the highest probability of a reliable record. CoreXY protects the growing print from XY inertia and may win after adhesion and hose tests. Crossed gantry and delta remain alternatives; neither reduces required polymer throughput.

## Balance and drive calculations

[mechanics_results.json](mechanics_results.json) contains each toolhead item's estimated mass, XYZ centroid and local inertia envelope, including nozzle, heater, fan, duct, carriage, fasteners, wires, supported hose, PTFE and filament. The proposed short-Bowden head totals 136 g. Its center is (0, +4.91, −2.79) mm relative to the carriage/belt origin. At 100 m/s² X acceleration the resulting moments are −0.0379 Nm about Y and −0.06675 Nm about Z. These coordinates are an analytical arrangement, not frozen purchased interfaces or CAD mass properties. Changing hose support changes them.

Adding a 90 g motor and 28 g drive raises the head to 254 g and its center to (0, +1.82, +9.66) mm. Y balance improves but pitch moment rises to 0.2453 Nm. Short Bowden therefore deserves testing, but compression, filament friction and extrusion-force bandwidth could outweigh its mechanical benefit. Neither option has measured pressure advance or extrusion force.

The [LDO drawing](https://cdn.shopify.com/s/files/1/0239/9287/files/LDO-42STH48-2504AC_RevA.pdf?v=1643851583) specifies 84.5 g cm² reference rotor inertia and 350 g reference motor weight. With pulley radius r, reflected mass is J/r². For 16/20/24/32 teeth it is 326/208/145/81 g. Larger pulleys reduce rotor inertia and RPM but also reduce belt force per Nm; they need a torque-speed optimization, not a smallest-pulley rule.

The [manufacturer torque test](https://cdn.shopify.com/s/files/1/0239/9287/files/LDO-42STH48-2504AC_Torque_Curve.pdf?v=1645112191) is at 24 V, 2.5 A, full step. It reports 0.239 Nm at 1500 RPM and 0.168 Nm at 2100 RPM. The latter corresponds to 1400 mm/s on a 20T belt drive. At 1500 mm/s this drive requires 2250 RPM, outside the measured range; a CoreXY 45-degree move requires 3182 RPM. Do not extrapolate holding torque, substitute a lower current, or assume 48 V performance. The candidate SKR Pico's installed-driver thermal/current behavior has not been reconciled with the motor test.

## Stiffness and manufacturing limits

Effective belt/frame stiffness is not measured. Sweeping 10–100 kN/m and 0.35–0.60 kg effective mass gives resonances around 21–85 Hz and 0.2–2.0 mm deflection under 20 N. This sensitivity is not a prediction of this frame or an input-shaper frequency. Belt elastic modulus, span lengths, joints, rail preload and frame boundary conditions must replace those assumptions.

A single aluminum cantilever 120 mm long, 40 mm wide and 6 mm thick has I=720 mm4. Taking E=69,000 N/mm2 and a 30 N tip load gives FL³/(3EI)=0.348 mm deflection. Reducing the unsupported span to 60 mm reduces this to 0.0435 mm. Triangulated supports and short rail standoffs are necessary; a visually thick bracket is insufficient evidence.

Printed brackets, tensioners, a duct, hose suspension and wire supports are allowed in the cost envelope. Precision rail datum surfaces and bearing fits are not assumed to emerge from an FDM print without alignment work. No CNC service has been quoted; no drawing tolerances or fastener lengths are frozen.
