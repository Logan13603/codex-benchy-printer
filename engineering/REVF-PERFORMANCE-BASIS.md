# Rev F performance basis and architecture decision

2026-09-30. Engineering recommendation for a new extrusion-frame design. This is a design basis, not physical acceptance or a released manufacturing specification.

## Decision

Use a **compact four-motor AWD CoreXY, with a bed that moves only in Z**, a light carbon gantry, direct extrusion, and remote CPAP cooling. The chosen architecture offers the strongest practical route from available purchased parts and normal Klipper-compatible controls to a very fast printer. Freeze dimensions only after the belt and purchased-interface checks below. Sub-minute performance remains an experimental target.

This changes the prior research preference for a stationary-XY hotend and moving XY bed. New creator-owned evidence makes the CoreXY route more defensible for an accessible build: the [T250 repository](https://github.com/MSzturc/T250) describes a quad-motor CoreXY, TMC2160 drives up to 60 V, a balanced direct-drive head, remote CPAP cooling, and claimed physical printing at 250,000 mm/s². Its README currently says a Speedboat under two minutes. The [creator's linked 54.733-second video](https://www.youtube.com/watch?v=rbLPCK5fKhc) is the reported record-run lead; fresh video retrieval failed in this audit, and its exact slice, dimensional quality, and rules compliance were not independently checked. Do not transfer that time or acceleration to our CAD.

The [Minuteman creator's final episode](https://www.youtube.com/watch?v=iMAWa9vfxcE), whose transcript and frames were inspected in checkpoint 006, demonstrates another physical route using a light moving platform, specialized hotend, strong cooling and custom motion firmware. That published implementation is valuable evidence that the overall problem is solvable. It does not validate our conventional stacked-rail bed, strict slice, CPAP blower, or a cheaper derivative. Its reported slice includes material and contour adjustments absent from our frozen rules profile.

## Why not continue the stacked XY bed

The old guide stack has lower-bound translating masses about **154 g X and 77 g Y**, before belt clamps, fasteners, heater, cable and the growing print. At the old 2,000,000 mm/s² requirement, the associated inertia forces are **308 N and 154 N**; rotor and idler inertia add drive demand. These values defeat the rationale for a roughly 60 g record platform. Replacing the massive base with extrusions does not remove this moving mass or change the motor limitation.

A finished 11.35 g boat has lateral inertia of 1.14/3.41/22.7 N at 100,000/300,000/2,000,000 mm/s². For an illustrative 20 mm boat center-of-mass height, its overturning moments are 0.023/0.068/0.454 Nm. Actual hull adhesion area and temperature-dependent shell stiffness must be tested; the simple force calculation is not an adhesion prediction. These loads are manageable research questions at the lower range, but the hot chimney and cabin are additionally excited by every bed reversal. A Z-only bed removes these XY print loads.

An air-bearing or planar cable bed could reduce mass further, but needs a surface datum, full tension allocation, nonlinear transmission correction, yaw restraint and different firmware. The prior four-cable study demanded 9.1–14.0 Nm per motor; it is rejected as a production baseline. A parallel linkage remains a separate research prototype, not a conventional drive replacement that can be released immediately.

Delta has low head mass but varying Jacobians, additional tower-carriage/rod inertia and custom hose management. Crossed gantry has more guide interfaces and synchronization mass. A two-motor CoreXY is simpler and cheaper, but its available torque margin is lower. AWD retains standard XY kinematics while providing two drives per belt; added rotor inertia must still be counted.

## Concrete CAD starting envelope

These are proposed layout parameters, not purchased tolerances:

| Item | Initial design value | Engineering reason |
|---|---:|---|
| Usable workspace | 80 × 80 × 60 mm | Full-size 60.001 × 31.004 × 48 mm model with margin |
| Extrusion cube, outside | About 280 × 280 × 300 mm | Short rail/belt spans; accommodates four 48 mm motors and service clearances |
| Frame section | 2020 cube; 2040 at top rail carriers if needed | Metal joint load paths and reduced top-plane racking |
| Frame stabilization | Bolted 3 mm aluminium rear/side shear panels or diagonal metal braces | Joint/racking stiffness matters more than cosmetically thick printed corners |
| Bed substrate | 100 × 100 × 4 mm aluminium, three-point mount, Z only | Flat, small, easy to heat; bed mass is not an XY penalty |
| Y guides | Approximately 200 mm rails, one rail each side | Short guide span; exact block length sets usable travel |
| X bridge | About 200 mm, 20 × 20 × 1.5 mm carbon square tube | Stiff vertical section with low translating mass |
| X rail | MGN7 initially; validate block moments/rail datum | Lower mass than MGN9/12; avoid unsupported carriage moments |
| Toolhead allowance | ≤200 g complete, including supported hose and wires | Must include actual extruder, hotend, block, clamps, duct and fasteners |
| Whole Y translating allowance | ≤300 g | Head plus beam, rail, end blocks, belts and hardware |
| XY transmission | 9 mm 2 mm-pitch belts; compare 32T and 36T drives | Larger radius lowers rotor equivalent mass and RPM; force falls with radius |
| Z | Two rear guides, one lead screw, rigid three-point bed support | Slow Z; do not spend XY mass/performance budget on unnecessary lift mechanisms |
| Extrusion | Compact direct drive, short guided filament path | High PA bandwidth; a short Bowden alternative requires measured compliance/force-response evidence |
| Cooling | One light symmetric CPAP duct with supported overhead hose | Opposed jets and symmetric hose support reduce yaw/pitch loading |

Allow at least 10 mm nozzle/body clearance throughout nominal travel and a separate homing/overshoot margin. Exact frame dimensions should grow if purchased motor bodies, belt routing or duct sweep require it. Do not claim a 280 mm envelope before interference checks.

The tube estimate is 35.5 g at assumed carbon density 1.6 g/cm³. Its section second moment is 6,373 mm⁴. Under a 50 N center load, a 200 mm simply supported span and an assumed longitudinal modulus of 70 GPa give 0.019 mm elastic deflection. This is a beam screening result; tube laminate/shear, rail offset, drilled holes, printed ends, bearing blocks and joints are omitted. Measure actual gantry vibration before using any input-shaper frequency.

## Motor and drive basis

The [LDO manufacturer page](https://ldomotion.com/products/ldo42sth482504ac) specifies the 42STH48-2504AC as a 48 mm, 350 g, 2.5 A/phase, 1.5 mH motor. Its preserved drawing gives rotor inertia **8.45×10⁻⁶ kg m²**. The [published operating curve](https://cdn.shopify.com/s/files/1/0239/9287/files/LDO-42STH48-2504AC_Torque_Curve.pdf?v=1645112191) is a 24 V, 2.5 A, full-step test: approximately 0.239 Nm at 1,500 RPM and 0.168 Nm at 2,100 RPM. Fresh PDF retrieval failed, so these are retained checkpoint-004 values, not a newly inspected curve. **48 V operation does not grant an invented 48 V torque curve.** Obtain the exact curve or test motor/driver assembly before freezing record limits.

For four identical AWD motors and a pure-axis move, the rotor mass equivalent is `4J/r²`. If the belt-drive pair on A and pair on B share force ideally, each motor's torque is:

`Tmotor = (M + 4J/r² + Mpulley_equivalent) × a × r / 4 + Tdrag`

Here `a` is in m/s² and `r` in metres. This is a pure-axis identity only. For every diagonal path segment, use CoreXY A=X+Y and B=X−Y and solve all four motor speeds/torques. One diagonal belt can move √2 faster; imperfect AWD phase/load sharing is not modeled by multiplying torque by four.

| 2 mm-pitch pulley | Pitch radius | Four-rotor equivalent mass | RPM at 1,500 mm/s pure X/Y | Worst 45° RPM at same tool speed |
|---|---:|---:|---:|---:|
| 32T | 10.186 mm | 326 g | 1,406 | 1,989 |
| 36T | 11.459 mm | 257 g | 1,250 | 1,768 |

At Y translating mass 300 g and 36T, 250,000 mm/s² demands **0.399 Nm per motor before friction/pulley inertia**. A 30% torque reserve requires at least **0.570 Nm operating torque**, already above the listed 0.55 Nm holding value; high-RPM torque is lower. Thus this exact LDO/36T arrangement cannot be described as supporting 250k throughout the path. At 100k the ideal demand is 0.160 Nm, or 0.228 Nm for 30% reserve before drag. This is much more credible but still needs the selected voltage/current curve and diagonal analysis.

Larger pulleys do not automatically increase acceleration. Larger NEMA23 motors have additional rotor inertia. For example, the [Nanotec SCB5618L4204-B](https://www.nanotec.com/us/en/products/2892-scb5618l4204-b) lists **48×10⁻⁶ kg m²**, 4.2 A/winding and 1.7 mH. Use its actual operating curves/current definitions, not holding torque or a similar motor's data. Its frame-fixed mass is cheap in motion terms, but inertia and required pulley radius are not.

Select a 48 V capable driver architecture with a separate 24 V heater/fan supply, and retain NEMA17 motor-interface compatibility while screening better low-inductance/high-speed motors. TMC2160/TMC5160-class module voltage/current ratings vary by board and power stage; the IC rating alone is insufficient. Never apply 48 V to a 24 V hotend. The complete exact board revision remains to be frozen.

## Flow and thermal basis

The corrected frozen slice deposits **8,935.39 mm³**. It requires **162.46 mm³/s average over 55 s**, including travel. Its extreme planner scenario needs a **300 mm³/s peak cap**. At 1.75 mm filament diameter, that is 124.7 mm/s filament speed. These are toolpath requirements, not a hotend rating.

The [Goliath designer's documentation](https://docs.vzbot.org/goliath) provides an available high-flow hotend and assembly/mounting basis. It does **not** provide an inspected PLA/0.5 mm-nozzle test substantiating 300 mm³/s in this audit. Goliath plus a 0.5 mm CHT is a useful commissioning candidate, not a supported sub-minute thermal solution. The [Bondtech CHT white paper](https://www.bondtech.se/intranet/white-paper-max-flow-rate/) uses larger nozzle diameters and a different heater arrangement; do not extrapolate those values to the allowed outlet.

The [Phaetus Rapido X page](https://www.phaetus.com/products/rapido-x) advertises 103 mm³/s with a 24 V 120 W assembly. Even granting that maximum continuously, extrusion alone takes **86.75 s** on this slice. Test conditions for the listed maximum are not sufficient to establish exact PLA/0.5 mm output. Rapido X is rejected as the sole basis for a 55 s claim. The [E3D Volcano support table](https://e3d-online.com/pages/e3d-classics-support-volcano-nozzles) also shows that nozzle diameter, material and temperature change usable flow; larger-outlet results cannot be transferred.

For the old 300 mm³/s requirement, sensible heat alone is roughly 120–160 W using the prior stated 25→240°C PLA heat-capacity assumptions. Phase-transition and block/air losses are additional. A 100 W heater cannot sustain the upper end of that assumed energy requirement merely because its set-point trace looks stable. Melt residence/temperature and extrusion pressure must be checked with the actual filament.

A custom multi-filament hotend could reach the required throughput while reducing each feed speed. It increases melt volume, fabrication complexity and PA demands; keep it as an interchangeable later thermal module until documented test results exist. A CAD envelope is not a flow proof.

## Balance, belts and cooling

Compute toolhead COM from measured supplier/component masses and CAD centroid coordinates for every item. Include filament, supported hose/wire lengths, screws, rail block and belt clamps. Mount the extruder motor close to and behind the carriage, hotend below the center, and make the cooling duct left/right symmetric. Put the mean of the two belt force planes close to the carriage/complete-head COM; report the remaining lever arms. At head mass 200 g, a 5 mm offset generates 0.25 Nm at 250,000 mm/s². This is a strong reason to position by mass rather than fit.

Two stacked 9 mm belts require deliberate plane separation, straight clamp entry, flanged compatible idlers, tension access and motor synchronization. Do not constrain the belts to an attractive line that lacks a manufacturable wrap. Record belt lengths, free spans, pretension and force-plane offsets. Reuse the owned belts only after pitch/tooth compatibility is confirmed; their unknown inventory cannot freeze a pulley interface.

Use a short, large-bore overhead hose and a lightweight split duct. Prefer a 22–25 mm main trunk if the owned blower accepts it; use a removable adapter for the owned hose, whose bore is still unknown. A provisional symmetric four-slot outlet, each about 14×2 mm, totals 112 mm². At 4 L/s its ideal outlet speed is 35.7 m/s. This geometry is a starting test article, not a validated cooling requirement. Keep jets directed to deposited plastic, provide heater shielding, and measure nozzle cooling/draft effects. Two directed jets plus two wider side jets may outperform a narrow continuous ring and are easier to inspect/clean.

Prior 15 mm-hose sensitivity at 4 L/s demanded roughly 4.4–5.0 kPa before proving local heat transfer. Blower free-air volume is not installed flow. The Minuteman's reported pressure-air supply cannot be assigned to the user's CPAP. Measure the blower operating point, duct losses and part temperature; upper chimney layers are the critical cooling test.

## Honest performance envelope and next calculations

Commission at 10,000 mm/s² and 200 mm/s, then increase stepwise. Use **100,000 mm/s², 1,000 mm/s travel, and the measured 0.5 mm flow limit** as the first advanced performance-study point. A 250,000 mm/s²/1,500 mm/s trial is conditional on motor tracking, belt load, frame response and flow tests; it is not a recommended default configuration. Do not invent calibrated PA, PID or input-shaper values.

The old **53.5361 s** result is an ideal planner calculation at **2,400 mm/s, 2,000,000 mm/s², SCV500 and Q300**, not a physical estimate for this revision. A 0.10 s layer floor gives 55.1475 s; a 0.20 s floor gives 60.3826 s. Lowering Q to 200 yields 64.50 s before cooling floors. The earlier 0.5 mm Cura toolpath cannot simply be run on this conventional AWD machine at its assumed caps. Re-slice and co-optimize compliant paths after freezing actual hardware capabilities; preserve the original model/width/shell/solid-layer requirements.

A new calculation on 2026-09-30 used `parse` and the preserved pinned-Klipper `extrusion_dynamics.plan/summary` on `slicing/cura-travel-study/concentric-bridges/analysis.gcode` (SHA256 `1f433cc376e53d6a91ca1b6878e1910c85140c5e84e500d589a1906728327ded`). The extruder corner limit was 1 mm/s, minimum cruise ratio 0, finite queue, and first-layer cap 300 mm/s, matching the preceding study defaults:

| Acceleration mm/s² | Velocity mm/s | Peak flow mm³/s | SCV mm/s | Planner seconds | With 0.20 s layer floor |
|---:|---:|---:|---:|---:|---:|
| 100,000 | 1,000 | 100 | 30 | 203.57 | 204.91 |
| 100,000 | 1,000 | 200 | 30 | 195.83 | 197.16 |
| 250,000 | 1,500 | 200 | 50 | 128.16 | 130.84 |
| 250,000 | 1,500 | 300 | 100 | 120.84 | 123.73 |

These four scenarios are still kinematic simulations with no motor tracking, shaping, friction or thermal coupling. The large time penalty confirms that the existing path's many short moves and junctions remain a central problem. The physical creator record is a reason to investigate different compliant path generation and actual settings; it is not evidence that selecting similar architecture makes this saved path sub-minute. Raising SCV/flow until the number fits would not resolve the hardware or dimensional problem.

Acceptance before any claim of a probable sub-minute result requires:

1. Exact-nozzle extrusion tests with weighed output, extrusion force/current, temperature and several relevant PA transitions.
2. Full A/B/A2/B2 torque-speed/inertia analysis on the corrected path, including synchronization error, driver current and voltage.
3. Belt and structure measurements under the actual inertia loads, plus toolhead COM and full-travel collision/access audit.
4. Measured CPAP cooling and progressively faster complete Benchys, preserving all small features.
5. Three consecutive compliant complete runs under 60 s. The design target remains 50–55 s.

**CAD may be developed now under the user's explicit instruction, but a production release must still wait for purchased-interface, interference, tolerance and assembly audits. Physical validation remains pending.**
