# Rev F independent CAD audit — checkpoint from 2026-10-20

Recorded 2026-10-21 from the completed frozen-source audit. **Manufacturing release is on hold.** This report preserves the exact last completed Oct 20 audit rather than silently relabeling subsequent builder changes as verified. A new Oct 21 audit will be reported separately.

## Method and scope

Built the source snapshots with the bundled CadQuery/OpenCascade runtime in world millimetres. Used `cq_common.interference` with a 0.1 mm³ overlap threshold; structural pair screens excluded fasteners, and the toolhead was also screened with fasteners included. Each builder was compiled from captured bytes. Source hashes below identify the tested revision. This checks material intersection, not strength, tolerance margin, manufacture, wire/hose behavior or physical performance.

Native Fusion was unavailable; these offline BReps do not establish an executed native Fusion feature-history checkpoint.

## Audited source identities

| Builder | SHA256 at capture | Changed before audit ended? |
|---|---|---|
| 01_frame_xy_cq.py | `4d3a9e7aebf3d5f70b6e56d1fd10abe910c7bfe0ba8db6da933c2015ac74453c` | No |
| 05_drives_cq.py | `75bdf382d7f4f45d119591bfdcc77189d2a2f10fc2f447ea27bd709882b634a4` | No |
| 06_gantry_supports_cq.py | `61a287709dd31154143c7fd262ce7a1aab1cc4f9a635efdfcc9417d735f12788` | No |
| 04_toolhead_cq.py | `35e501d91f0425e53e0e640e41d29af4aaee726157a8773d1663ae19e264cea5` | Yes |

The 04 toolhead changed during this audit. Its wire-saddle screw-head collisions below belong to the captured version and were subsequently reported corrected by the toolhead author. This audit did not rerun that final change.

## Structural clashes in the captured closed-tube/portal variant

All 17 pairs below are solid material clashes. They are not intentional screw engagement. The revised drive assembly by itself cleared the frame; the remaining problems are integration with its supports.

| Check | Part A | Part B | Intersection mm³ |
|---|---|---|---:|
| supports_vs_frame | CBP-M206_L_SPLIT_BEAM_CLAMP | CBP-P203_MGN7_X_RAIL_140 | 269.820736 |
| supports_vs_frame | CBP-M206_R_SPLIT_BEAM_CLAMP | CBP-P203_MGN7_X_RAIL_140 | 269.820736 |
| supports_vs_frame | CBP-D402_A_FRAME_HANGER_1 | CBP-P201_MGN9_Y_RAIL_L | 715.261347 |
| supports_vs_frame | CBP-D402_A_FRAME_HANGER_2 | CBP-P201_MGN9_Y_RAIL_R | 537.630673 |
| supports_vs_frame | CBP-D402_B_FRAME_HANGER_1 | CBP-P201_MGN9_Y_RAIL_R | 715.261347 |
| supports_vs_frame | CBP-D402_B_FRAME_HANGER_2 | CBP-P201_MGN9_Y_RAIL_L | 537.630673 |
| supports_vs_drives | CBP-M205_L_CARRIAGE_ADAPTER | CBP-P406_A_9MM_BELT_ROUTE | 466.335703 |
| supports_vs_drives | CBP-M205_R_CARRIAGE_ADAPTER | CBP-P406_B_9MM_BELT_ROUTE | 436.144952 |
| supports_vs_drives | CBP-D402_A_FRAME_HANGER_2 | CBP-P406_A_9MM_BELT_ROUTE | 15.180000 |
| supports_vs_drives | CBP-D402_A_FRAME_HANGER_2 | CBP-P403_B_RETURN_IDLER | 429.403148 |
| supports_vs_drives | CBP-D402_A_FRAME_HANGER_2 | CBP-P404_B_RETURN_625_0 | 61.831391 |
| supports_vs_drives | CBP-D402_A_FRAME_HANGER_2 | CBP-P404_B_RETURN_625_1 | 325.428374 |
| supports_vs_drives | CBP-D402_A_FRAME_HANGER_2 | CBP-P406_B_9MM_BELT_ROUTE | 46.520113 |
| supports_vs_drives | CBP-D402_B_FRAME_HANGER_2 | CBP-P403_A_RETURN_IDLER | 153.384696 |
| supports_vs_drives | CBP-D402_B_FRAME_HANGER_2 | CBP-P404_A_RETURN_625_0 | 240.816997 |
| supports_vs_drives | CBP-D402_B_FRAME_HANGER_2 | CBP-P406_A_9MM_BELT_ROUTE | 15.867325 |
| supports_vs_drives | CBP-D402_B_FRAME_HANGER_2 | CBP-P406_B_9MM_BELT_ROUTE | 62.100000 |

Required corrections: add real rail/carriage clearances to the beam clamps and hangers; route return-idler support around the opposite belt and bearings; retain accessible bolt seats and a continuous load path after each clearance cut. Do not remove purchased rail or belt material to make the model appear clear. Rerun all cross-subsystem and moving-pose screens after the support changes.

## Checks without a captured structural overlap

- Revised drives versus frame:0 pairs above 0.1 mm³.
- Supports versus toolhead:0 pairs above 0.1 mm³.
- Toolhead versus belt routes at the nominal pose:0 pairs above 0.1 mm³.
- An earlier source snapshot screened bed versus frame at 0/20/40/60 mm descent and found 0 pairs. The bed builder changed during that earlier run, so this is historical evidence rather than acceptance of its later revision.
- That earlier snapshot screened toolhead/frame at X−40/0/+40 and Y−40/0/+40, finding 0 volume overlaps. The front fan screw heads approached the front top-frame face at nominal Y−40 with zero nominal clearance. A zero-volume contact is not a manufacturing or homing margin.

## Intentional thread-envelope intersections and stale head finding

The captured head has one non-fastener pair: M6 coupler thread envelope versus the 5 mm platform tap drill,51.836279 mm³. This is an intentional simplified M6 thread/minor-bore representation, provided that the actual fitting and thread engagement are verified. The other expected head hits include the four M2.5 hotend screw pilots, screw/nut mating threads and named tapped attachment holes. They require correct lengths and thread specifications, not clearance bores through their mates.

Including fasteners also found two genuine captured collisions: each `CBP-H403_0/_1_PLATFORM_M3x10` head intersected `CBP-P406_R1_WIRE_SADDLE` by 50.672602 mm³. The author subsequently added driver/head access to the saddle and moved its mounting screws; the final 04 hash differs from the audited hash. Treat these two as historical defects awaiting independent verification of the new version.

## Mass and interface holds

The earlier modeled head alone was 183.887 g, including 31.975 g of fasteners, before the separate 15 g MGN7H block and supported hose/wire/filament contributions. Including that carriage gave 198.887 g and an illustrative mass-overridden COM near(−0.043,−35.741,278.358) mm. Against the actual revised mean belt point Y−35/Z275.8, the offsets were approximately−0.741 mm Y/+2.558 mm Z. These values are tied to that snapshot; the new hardware must be recalculated. Hotend 80 g, fan 8 g and fitting 5 g were unverified estimates, and simplified purchased geometry is not a valid substitute for its true mass distribution.

The captured mass audit also had unknown belt masses, a magnetic surface allowance without a density, and no complete reconciled motor-plus-integrated-screw mass assignment. Moving idler bearing/shaft hardware and the later portal/fasteners materially change gantry mass. The earlier 04 `motiongroup` field did not match the common exporter `motion_group`; the author subsequently corrected the field. A total assembled mass and XYZ COM must use one consistent grouping and avoid counting the carriage or integrated Z screw twice.

Release holds include actual pulley/idler envelopes and shaft bearings, belt tooth compatibility, cold fan and Bowden fitting interfaces, exact Z nut/pilot geometry, all slot nuts and attachment lengths, endstops/homing clearance, heater/surface/wire routing, and supported hose loads. A valid individual BRep does not close any of these interfaces.

## Rejected carbon return-port option

The rejected option cut 2.8 mm-wide,9.8 mm-high full-Y ports in a 20×20×1.5 mm carbon tube near X±81.54. Ideal section arithmetic gives upper-port vertical/horizontal-I losses 7.0%/39.6%, and lower-port losses 71.2%/26.6% after shifting the neutral axis. For an ideal 190 mm simply supported beam under a center point load, the short near-end notches add only about 0.226% global vertical Euler–Bernoulli compliance. Thus local section-I loss must not be mistaken for whole-beam stiffness loss. The larger unresolved risks are local shear transfer, broken closed-section torsion, warping, fiber interruption and notch/delamination sensitivity. A matching printed-clamp notch is not a demonstrated reinforcement bypass.

The selected development replacement keeps a shorter 158 mm carbon tube closed and carries its ends through an explicit aluminium portal above the belts. That avoids cutting the tube, but its support collisions in this report still need correction and structural validation. No physical vibration, belt tracking or Benchy result is claimed.

## Next audit

Freeze the corrected 01/03/04/05/06/07 builders, regenerate the assembly, retain this historical audit, and screen 80 mm X×60 mm Y×60 mm Z travel with minimum distances as well as overlap volumes. Include fastener-head access, actual purchased interface envelopes and hose sweeps. Native Fusion rebuild, constraint audit, manufacturing drawings and physical commissioning remain separate acceptance steps.
