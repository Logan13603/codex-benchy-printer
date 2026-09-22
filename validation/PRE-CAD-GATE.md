# Pre-CAD acceptance gate — checkpoint 008

## Final checkpoint update — read first

The initial52.91s concentric slice is rejected as a build candidate because its roof uses closed loops over the cabin void. The sixth slice `slicing/cura-travel-study/concentric-bridges/analysis.gcode` enables bridge handling with all three bridge-skin densities and flows100%, wall flow100% and wall coast0. Its SHA256 is `1f433cc376e53d6a91ca1b6878e1910c85140c5e84e500d589a1906728327ded`.

Corrected timing: **53.5361s**;0.10s layer floor **55.1475s**;0.20s floor **60.3826s**;Q200 **64.5032s**. These caps remain unproven. The corrected slice needs pressure/spatial/motor checks rerun; existing concentric dynamics refer to the earlier hash. The model-volume support screen reduces closed-loop flags from14 to1, but does not certify full coverage, bridge anchoring, bead width or physical print quality.

**Exact next operation:** investigate the remaining support flag, audit actual solid coverage and bridge endpoints on the corrected slice, then rerun its extrusion and spatial dynamics. Use `bridge_support_screen.py <numpy directory> concentric-bridges bridge-corrected-support-screen.json bridge-corrected-support-008.png` to reproduce the screen. Keep all CAD gated. The earlier notes below are historical intermediate results within this checkpoint and must not be mistaken for the corrected candidate's dynamics.


**NOT PASSED. No CAD should begin under the current instruction.** This is an engineering decision checkpoint, not a claim that a sub-minute machine is impossible. The current analysis has identified necessary performance that has not yet been tied to a buildable mechanism and verified extrusion/cooling system.

| Requirement | Current evidence | What is needed |
|---|---|---|
| Full-size compliant model/toolpath | Original model/checksum frozen; five new slices preserve counts/width settings and pass definite-width audit | Inspect local shell coverage, concentric center gaps, bridges and all small features |
| ≤55 s nominal, credible <60 s margin | Concentric candidate52.91 s at extreme caps;54.52 s with0.10 s layer floor;60.05 s with0.20 s floor | Combined motion, extrusion and thermal limits in the same path model, not unrelated best cases |
| Motion and positional accuracy | Improved slice still needs8.05 Nm peak per motor in the four-motor Cartesian fixture at 800 Hz smoothing; cable alternative failed earlier | Select a mechanically guided mechanism, calculate full changing inertia/COM, and demonstrate coincident torque-speed and tracking margin |
| Extrusion | Purchased-flow audit does not support300 mm³/s through eligible nozzle; PA exposes severe transient feed demands | Exact material/hotend/extruder combination, sustained and pulsed flow/force evidence, identified pressure dynamics |
| Cooling | Floor sensitivity only; owned CPAP model unknown | Blower pressure-flow operating point with actual hose/duct, short-layer tests and nozzle heat-loss check |
| Lowest credible cost | No budget ceiling; owned parts credited | Freeze performance-backed interfaces first, then compare complete delivered cost |
| CAD/manufacture | Verified Fusion folder; blank unsaved Hybrid document only | Begin only after the preceding evidence supports the combined performance; then fully constrained components and export audit |

## Exact next engineering work

The former54.30 s path is superseded as the leading research candidate. Use `slicing/cura-travel-study/concentric-skin/analysis.gcode`, with its stored checksum/settings, and the new extruder-aware planner. Do not return to a planner that omits extrusion junction checks merely to recover its lower time.

1. Inspect the concentric candidate's actual deposition coverage against layer cross-sections and required small features. Retain the original mesh and all shell requirements.
2. Evaluate a low-compliance stationary-XY melt system with multiple filament inputs and **direct hob drives**, comparing rotor inertia and pressure force against the old heavily geared LGX option. A four-feed split lowers each filament's speed; pressure at each inlet is still the common chamber pressure. Use a measured torque-speed curve and a pressure range until pressure is measured. Do not assign zero PA or arbitrarily short smoothing as a validated cure.
3. Pair that extrusion result with a guided moving-bed mechanism; include the printed boat, yaw restraint, pulleys, fasteners, wires and full swept clearance. The existing60 g/axis fixture remains an assumption. Closed-loop control requires encoder resolution and measured/identified tracking bandwidth, not only current-loop frequency.
4. Apply the resulting limits and cooling behavior to the exact same path. Require ≤55 s nominal and a documented plausible adverse case under 60 s before CAD. If this cannot be supported, retain the no-CAD decision and report the specific missing evidence.

## Concrete experimental evidence needed

Experiments are not represented as completed. They are useful next evidence if a prototype or test hardware becomes available; they are not instructions to buy unselected parts.

- **Flow/pressure:** log filament identity, drying, nozzle measurement, temperatures, heater voltage/power, force and collected mass. Progress through60/100/150/200/250/300 mm³/s only while the preceding stage is stable and within component ratings. Use repeated timed60 s collections; weigh actual output against commanded volume×measured/declared density. Stop increasing at sustained force saturation, feed slip, temperature loss or material degradation. A useful project screen is±5% mass agreement with no slip, followed by a pulsed path-like test; this threshold is a chosen engineering screen, not a race rule.
- **Transient extrusion:** measure starts/stops and representative1–40 ms variations at the working pressure/temperature. Identify lag and limits rather than copying another printer's PA. Verify material placement along a moving test path; a free-air flow test cannot validate short-segment printing.
- **Cooling:** measure installed airflow and static pressure at full hose/duct restriction. Exercise chimney/bridge geometry at 0.24,0.20,0.15 and0.10 s revisit times with the chosen filament, checking shape and layer bonding. Air bulk heat capacity alone is not the bead heat-transfer rate.
- **Motion:** measure tracking at representative corners and reversals with the complete moving mass. Log actual torque/current/RPM where available and position error. Establish a measured tolerance budget; the calculation's nominal centerline error does not include structural flex or belt stretch.

No board-specific wiring or runnable record profile is released until hardware is selected. Physical acceptance remains three consecutive compliant Benchys under 60 s, with target50–55 s. Predicted, simulated and physically measured results remain separate.
