# Feasibility checkpoint 002 — 2026-09-20

**Gate NOT PASSED. Stop before detailed Fusion CAD.** The evidence gathered does not support a reliable 50–55-second full-size compliant Benchy for $500 delivered. This is an evidence-limited engineering result, not proof that every possible custom printer is incapable of it. No finished printer, manufacturing files or validated firmware are being claimed.

## What is established

The private repository is [Logan13603/codex-benchy-printer](https://github.com/Logan13603/codex-benchy-printer). The original CreativeTools mesh is preserved at scale 1 with a recorded checksum. OrcaSlicer 2.3.2 generated all five trial paths. The [rules checklist](../slicing/RULES.md) now cites the actual Annex announcement. Fusion's `Default Project / Codex Benchy Printer` destination was verified; its inspected design remains blank and unsaved.

| Trial | Deposited volume mm³ | Extruding path m | Minimum whole-print mean flow for 55 s, mm³/s |
|---|---:|---:|---:|
| Initial 0.50 mm nominal widths | 8757 | 77.63 | 159.2 |
| 0.40 mm, thin-feature detection | 8305 | 92.59 | 151.0 |
| 0.45 mm, thin-feature detection | 8574 | 85.97 | 155.9 |
| 0.50 mm, thin-feature detection | 8752 | 77.57 | 159.1 |
| Combined infill, no retractions, thinner internal bridges | 8469 | 73.41 | 154.0 |

These are **trial paths, not certified compliant profiles**. Generated width annotations reach 0.736–0.866 mm in the width trials, exceeding the 0.5 mm cap; the combined trial reaches 0.836 mm. The nominal width setting is not an effective maximum for all Orca gap/thin-feature paths. Small-feature and local shell coverage audits remain incomplete. We did not delete gap fill or model features merely to make the audit pass.

## Motion and flow

Volume comes from positive deposited filament length times pi*1.75²/4; stationary unretractions are excluded. Dividing by 55 s is a necessary average for each particular slice, not a universal minimum for all legal slicing strategies. Peak flow must be higher because some time is spent traveling and changing layers.

Even the optimistic combined trial takes **112.9 s at 75 mm³/s**, or **84.7 s at 100 mm³/s**, from extrusion alone with zero travel and infinite acceleration. 75 and 100 are comparison caps, not claims that the chosen hotend achieves them through a 0.5 mm nozzle.

The acceleration/junction model includes XY/Z paths, pure extrusion barriers, forward/backward velocity propagation and triangular/trapezoidal moves. Six analytical checks pass: single triangular and trapezoidal moves, straight-line partition invariance, reversal, a flow bound and corner slowdown. It is **not a Klipper emulator**: finite lookahead, extrusion-ratio junction constraints, shaping, minimum cruise ratio, pressure advance, heater behavior and actual torque-limited acceleration remain outside it. Feed-rate commands are deliberately superseded by the comparison caps, and minimum cruise ratio is effectively zero. See [model source and limitations](path_model.py) and [full results](path_results.json).

For the combined trial, assuming 200 mm³/s, 2000 mm/s, 100,000 mm/s² and 100 mm/s square-corner velocity gives **168.5 s**. These aggressive limits are not established capabilities. At 1500 mm/s, 50,000 mm/s² and 20 mm/s square-corner velocity, the same trial is **282.2 s**. Changing nozzle path planning, simplifying corners within dimensional tolerance, or using a different slicer could change these times. They are not predictions of an assembled machine and must not be used as a proof of impossibility.

[Architecture comparison](ARCHITECTURES.md) covers miniature CoreXY, independent light-bed Cartesian, crossed gantry and delta, including rotor inertia and direct-drive/Bowden balance. None has a complete, validated motion/torque model at the target. No nominal architecture is frozen.

## Heat and cooling

At 160 mm³/s of 1.75 mm PLA, filament feed is 66.5 mm/s and mass flow about 0.198 g/s. Assuming specific heat 1.5–2.0 J/g/K, heating from 25 to 240 C requires **64–85 W of sensible heat alone**. At 200 mm³/s this becomes 80–107 W. Heater losses and phase-transition enthalpy are additional. A heater's rated watts cannot establish nozzle flow or extrusion force. Polymer formulation, pressure and residence time are unmeasured.

The [published original Rapido test](https://trianglelab.net/u_file/2111/01/file/Rapidohot-endMaximumPracticalFlowRateTest-5d73.pdf) used PETG at 265 C and large 0.8/1.2 mm nozzles, reporting roughly 42–64 mm³/s for the tested combinations. It is not a test of Rapido 2 UHF through a 0.5 mm nozzle and cannot be extrapolated to the required flow. A suitable documented small-nozzle result has not been established for the costed candidate.

The [BIQU CPAP manual](https://ae01.alicdn.com/kf/Sb960b719f4e440b5ab5695711f920f235.pdf) identifies WS7040-24-V200 with its external driver. Maximum free-air flow and maximum static pressure are distinct operating points. Our assumed 0.6 m, 15 mm-ID hose, four 10x2 mm outlets and uncertain corrugation/turn losses require about **2.5–2.8 kPa at 3 L/s**, or **4.4–5.0 kPa at 4 L/s**. The system would not deliver its advertised free-air flow through those outlets.

At 4 L/s, bulk air heat capacity is 4.82 W/K, but the local transfer coefficient and bridge temperature are unknown. Proposed routing would suspend the hose above the carriage with a slack loop and symmetrical outlets below an insulated heater. Supported hose mass is included in the analytical toolhead; hose spring force is not measured. [Thermal/duct calculations](thermal_cooling_results.json) expose these assumptions.

## Delivered cost

The [candidate BOM](../purchasing/CANDIDATE-BOM.md) totals **$643.90 delivered estimate**: $568.46 parts/materials, $25 shipping allowance and $50.44 estimated tax. It includes CPAP/hose, host/storage/power, supply, wiring/protection, motors, mechanics, materials and fasteners. Installed mass is approximately 4.08 kg; moving-head estimate 136 g and bed estimate 89.7 g are included subsets.

Major motor, hotend, CPAP and board variant prices were retrieved from sellers; commodity rows remain allowances. The Pi Zero 2 W uses the manufacturer's advertised $15, not a verified delivered reseller cart. This is not a complete purchasing release. Even free shipping and no tax would leave this particular reference above $500; it is not a lower bound on all possible hardware combinations.

## Concrete routes forward

1. **Retain $500 and treat speed as a measured outcome.** Develop a lower-cost light-bed test machine only after a revised scope authorizes a slower target. The present model suggests a minutes-scale investigation; it does not justify promising a specific slower time.
2. **Retain 55 s and validate the critical subsystems first.** Obtain a compliant optimized path, then demonstrate its peak/average flow with the exact <=0.5 mm nozzle and filament. Measure extrusion force, temperature and cooling while operating. Price the resulting heater/extruder and a motor/driver combination with appropriate high-RPM torque before committing CAD. A higher budget alone does not guarantee success.
3. **Continue digital feasibility work within the original scope.** Resolve the width audit, compare a second slicer, validate the timing model against a pinned Klipper planner, and optimize pulley size and all four kinematics on the same compliant path. This may improve or strengthen the gate result. It must not silently become detailed CAD while the gate is unpassed.

No build firmware or wiring pin map is released because the architecture, drivers, heater and purchased interfaces are not frozen. No unmeasured PID, pressure advance or shaper frequencies are presented as calibrated settings. Physical acceptance remains three consecutive complete compliant prints under 60 s, with a 50–55 s target; no physical test has occurred.
