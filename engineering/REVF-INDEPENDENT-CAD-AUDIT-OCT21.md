# Rev F independent CAD audit — 2026-10-21

**Manufacturing release remains on hold.** This is an independent offline BRep check of the captured sources below. Native Fusion feature history, interface selection, material strength, belt tolerances, thermal behavior, wire/hose clearance and physical performance remain separate checks.

## Completed check: frame bracing, feet and fixed-frame travel

07 contains 251 named physical part instances: shear panels, gussets, feet and mounting hardware. With all fasteners included, it has **no unintended material overlap** with the frame, bed/Z assembly or nominal toolhead. Its eight frame overlaps are declared M5 corner-post thread engagement, each 52.024774 mm³. Its 72 internal overlaps are all declared screw/T-nut thread engagement. Structural self-interference is zero above the 0.1 mm³ reporting threshold.

The nine checked toolhead poses X=−40/0/+40 and Y=−30/0/+30 have no overlap with fixed frame, fixed Z components or 07. Their smallest exact BRep distance is **10.000 mm**, from fan screw CBP-H406_01_FAN_M2x16 to the front top X extrusion. At X=±40,Y≥0 the nearest pair is an outboard duct flange screw and the Y rail, 12.611998 mm apart.

The complete continuous 80×60 mm XY translation envelope also has a conservative swept-part bounding-box separation lower bound of **9.000000 mm** to those fixed components. A positive bound establishes separation throughout this nominal rigid-body envelope, rather than only at the nine samples. The true minimum over this full nominal envelope lies between the 9.000 mm conservative lower bound and the 10.000 mm sampled BRep distance. This statement excludes gantry-moving supports and regenerating belt routes, which require the next integration check.

For 60 mm of bed descent, the bed/Z moving parts stay at least **29.200000 mm** from 07 throughout the continuous stroke. Four exact BRep checks at descent 0/20/40/60 mm give 29.200 mm from CBP-H314_YOKE_END_M4X12_L1 to the left side panel. Guide/raceway and nut/screw function are not established by this 07 clearance check.

## Source identities

| Builder | SHA256 |
|---|---|
| 01_frame_xy_cq.py | `4d3a9e7aebf3d5f70b6e56d1fd10abe910c7bfe0ba8db6da933c2015ac74453c` |
| 03_bed_z_cq.py | `7bd3d8e7fec8169acf0d756d23d0b8fb6fe719ce7eeb562fecbc4ec43c00ea54` |
| 04_toolhead_cq.py | `13714490bf1c7237a9960c9a95d558dc467c735ebc776f2de131a699566cc75a` |
| 07_frame_bracing_cq.py | `8673ac64917d7deb3cce043ba918f1e15e8ccadcee24ad266a489add19334831` |

All four source files were unchanged at the end of this run. 01 was the prior closed-158-mm-tube snapshot; its pending tube/support redesign is not being presented as verified by this report. Fixed-frame geometry in that redesign must be compared to this hash before reusing the fixed-frame result.

## Mass-accounting observations

| Subsystem | Known modeled mass g | Parts with unknown mass |
|---|---:|---|
| head | 190.116 | none |
| bracing | 1727.468 | CBP-F124_TPU_FOOT_PAD_-1_-1, CBP-F124_TPU_FOOT_PAD_-1_1, CBP-F124_TPU_FOOT_PAD_1_-1, CBP-F124_TPU_FOOT_PAD_1_1 |
| bed | 1513.011 | CBP-P303_MAGNET_STACK_ALLOWANCE, CBP-P305_LDO_Z_MOTOR |

Density-derived printed mass uses a solid-wall geometric model and assumed material density. It is an estimate, not a measured manufactured-part mass. Purchased mass overrides remain vendor/declared values; simplified geometry does not establish the true component center of mass. The four TPU95A pads have no assigned density and are therefore omitted from the known total. Bed magnetic sheet and Z motor mass accounting remain unresolved. Supported hose, full Bowden tube, wires, connectors, rail screws and any as-yet-unmodeled retention hardware still require reconciliation.

## Pending integration and release holds

The revised 01/05/06 frozen source passed the integration checks below. The original 04 did not provide the requested X travel: its wide vertical CPAP trunks and seam hardware collide with the moving idlers already at X+20 mm. The upper-idler overlaps there were 1.761581 mm³ with the right duct front and 3.171865 mm³ with its rear. At X+30 mm there were 19 reported head/idler pairs, including seam screws and nuts. Revised 04 is being checked separately before its native Fusion execution. The earlier upper-portal suspicion was an envelope check target, not a confirmed collision; gantry Y translation cancels in the head-to-portal relative position.

## Frozen drive/support integration and accepted Y range

The following hashes identify the unchanged sources checked after the coordinated clearance revision:

| Builder | SHA256 |
|---|---|
| 01_frame_xy_cq.py | `ca96f5a8c68f1ecc88ab372e5f045fb85980d3829cd5c846886b9fd997de3de7` |
| 05_drives_cq.py | `955edcd2164db202951f018dc1ee15efa79652ef5c25e23ad624de1677d167fa` |
| 06_gantry_supports_cq.py | `18d7d7f59790fa84562451f7cafe2d3ff7f2b265001b23a01b3106fce1a22a84` |

These builders contain 148 named parts. Drives versus frame and supports versus drives have zero overlaps above 0.1 mm³ with fasteners included. Supports versus frame report only eight explicitly declared MGN9 block screw thread mates, 5.399612 mm³ each.

The formerly proposed Y=−30…+30 mm stroke is rejected. At Y−30, the right idler fork intersected the front A motor hanger by 14.400000 mm³ and its plate by 187.200000 mm³; the lower right moving idler intersected that plate by 45.056448 mm³. This failure was preserved rather than concealed by a zero-position assembly view.

The accepted geometry uses **Y=−20…+30 mm**, a 50 mm stroke with print center Y+5. A 31 mm wide Benchy has nominal 9.5 mm travel margin at each side of that centered placement. Exact BRep checks at both endpoints show zero unintended overlap. A continuous swept-part bounding-box screen has only four zero-bound pairs, all MGN9 block-to-rail or block-to-adapter interfaces; their nominal touching guide geometry is not a manufacturing-clearance validation. Every other moving/fixed pair has a positive bounding-box separation throughout the stroke.

| Critical pair | Exact distance at Y−20, mm | Continuous-stroke lower bound, mm |
|---|---:|---:|
| Lower right moving idler / front A motor plate | 4.250 | 4.250 |
| Right idler fork / front A motor plate | 8.000 | 8.000 |
| Right idler fork / front A motor hanger | 9.000 | 9.000 |

The current 04 and its 15 g MGN7H carriage sum to 205.116 g at proxy COM (−0.0416, −35.0227, 278.8246) mm. The modeled offset from the belt mean Y−35/Z275.8 is Y−0.0227/Z+3.0246 mm. This is the pre-dogleg source; recompute it for the revised ducts and overhead support. Supported hose, remaining Bowden tube and wires are not included. A low nominal screw-to-belt gap is not a tolerance analysis, and actual belt clamps/tensioning and idler shaft retention remain release interfaces.

The previous source-specific hold report remains at [REVF-INDEPENDENT-CAD-AUDIT.md](REVF-INDEPENDENT-CAD-AUDIT.md). Raw numerical evidence and the independent audit scripts are under work/; these checks are calculated development evidence, not physical validation.

## Rejected forward-only CPAP revision

The next 04 revision moved the trunks forward to Y−62 and added an overhead bridge. It passes the zero-position view but **does not pass full X travel**. Its exact source SHA256 is `1408bed0534a8b8b42cc33c5201b77af2379f37af528fbe4cc7aac54ae3b5323`. 01/05/06 retain the frozen hashes above; all four source hashes were unchanged at audit completion.

The moving-support results below include all fasteners. All listed intersections are unintended material overlap. The left/right names identify the actual mirrored instances, and the pose is toolhead X offset; gantry Y cancels in these relative positions.

| X offset mm | Head part | Gantry part | Overlap mm³ |
|---:|---|---|---:|
| -40 | CBP-P403_R1_DUCT_SUPPORT_BRIDGE | CBP-M207_L_REMOVABLE_IDLER_CAP | 129.924675 |
| -40 | CBP-P406_R1_WIRE_SADDLE | CBP-M206_L_SPLIT_BEAM_CLAMP | 24.149005 |
| -40 | CBP-P407_R1_WIRE_SADDLE_COVER | CBP-M206_L_SPLIT_BEAM_CLAMP | 16.099336 |
| -40 | CBP-H412_0_WIRE_WASHER | CBP-M206_L_SPLIT_BEAM_CLAMP | 2.375044 |
| -40 | CBP-H413_0_WIRE_M2x12 | CBP-M206_L_SPLIT_BEAM_CLAMP | 14.298313 |
| -40 | CBP-H45_LEFT_SUPPORT_M3x12 | CBP-M207_L_REMOVABLE_IDLER_CAP | 41.353347 |
| -30 | CBP-P403_R1_DUCT_SUPPORT_BRIDGE | CBP-M207_L_REMOVABLE_IDLER_CAP | 54.625000 |
| 30 | CBP-P403_R1_DUCT_SUPPORT_BRIDGE | CBP-M207_R_REMOVABLE_IDLER_CAP | 54.625000 |
| 40 | CBP-P403_R1_DUCT_SUPPORT_BRIDGE | CBP-M207_R_REMOVABLE_IDLER_CAP | 129.924675 |
| 40 | CBP-P406_R1_WIRE_SADDLE | CBP-M206_R_SPLIT_BEAM_CLAMP | 24.149005 |
| 40 | CBP-P407_R1_WIRE_SADDLE_COVER | CBP-M206_R_SPLIT_BEAM_CLAMP | 16.099336 |
| 40 | CBP-H412_1_WIRE_WASHER | CBP-M206_R_SPLIT_BEAM_CLAMP | 2.375044 |
| 40 | CBP-H413_1_WIRE_M2x12 | CBP-M206_R_SPLIT_BEAM_CLAMP | 14.298313 |
| 40 | CBP-H45_RIGHT_SUPPORT_M3x12 | CBP-M207_R_REMOVABLE_IDLER_CAP | 41.353347 |

At X−40, both left duct halves intersect the regenerated A belt, 14.904000 mm³ each. At X+40 the same happens to both right halves against the B belt. These four part/belt pairs repeat at every tested Y offset −20/0/+30. They are the fixed inner vertical return spans at world X=±77.290844 mm, not the moving idlers. Moving a duct forward cannot clear a belt span extending along Y.

| Head part | Actual belt part | X offsets mm | Tested Y offsets mm | Overlap each pose mm³ |
|---|---|---:|---|---:|
| CBP-P413_R1_LEFT_DUCT_FRONT | CBP-P406_A_9MM_BELT_ROUTE | −40 | −20, 0, +30 | 14.904000 |
| CBP-P414_R1_LEFT_DUCT_REAR | CBP-P406_A_9MM_BELT_ROUTE | −40 | −20, 0, +30 | 14.904000 |
| CBP-P415_R1_RIGHT_DUCT_FRONT | CBP-P406_B_9MM_BELT_ROUTE | +40 | −20, 0, +30 | 14.904000 |
| CBP-P416_R1_RIGHT_DUCT_REAR | CBP-P406_B_9MM_BELT_ROUTE | +40 | −20, 0, +30 | 14.904000 |

The zero-X head-to-moving-gantry minimum is 1.000 mm, from the wire saddle cover to the carbon tube. The zero-X head-to-belt minimum is 2.725 mm, from the spine to the A belt, at all three tested Y offsets. These center-position distances do not override the travel failures.

The fixed inner return leaves a local half-width budget of 77.290844−0.690−40 = **36.600844 mm** at the two belt height intervals Z264.8…273.8 and Z277.8…286.8. This is zero-clearance geometry; subtract a deliberate tolerance/deflection allowance. A further revision needs narrower midheight ducts/seam hardware, cap-clearing support feet, and narrower or relocated saddle hardware. Those changes must be re-audited; a proposed envelope is not a passed BRep result.

For this rejected head revision, known modeled head plus 15 g carriage is 215.704 g at proxy COM (−0.0396, −38.7270, 280.6118) mm. The Y-moving gantry excluding that toolhead is 364.393 g; total modeled Y-moving mass is therefore 580.097 g before belt mass and supported hose/wire corrections. Belt mass is unknown. The offsets from belt mean Y−35/Z275.8 are Y−3.727/Z+4.812 mm. Purchased mass/COM estimates and omitted supported services prevent treating these as measured mass properties.

Detailed raw evidence is preserved at `work/revf-oct21-head-rejected-1408bed0534a.json`. Manufacturing release and native execution of this head revision remain on hold.

## Final checkpoint: 50 × 65 mm workspace also rejected

At the requested clean stopping point, the proposed smaller workspace X=−25…+25, Y=−20…+45 mm was tested. **It also fails; it is not an accepted build envelope. No further tests or geometry edits were performed by this auditor after this result.** The full-size Benchy must not be represented as fitting a validated travel envelope at this checkpoint.

The tested 04 source was `b2377b89f2314d6a5ae632140c6894580b9c2db4ab1a7a0f24c771ee0255f3de`; the other three source hashes match the frozen drive/support table above. The toolhead author states that the change after 1408bed0534a is audit/report code only. The tested source bytes, rather than an equivalence assumption, identify these results. All source hashes were unchanged when each final run ended.

| Pose/check | Moving part | Fixed or gantry part | Overlap mm³ |
|---|---|---|---:|
| gantry_vs_fixed_Y45.0 | CBP-P202_MGN9H_Y_BLOCK_L | CBP-D402_A_FRAME_HANGER_1 | 36.812500 |
| gantry_vs_fixed_Y45.0 | CBP-P202_MGN9H_Y_BLOCK_R | CBP-D402_B_FRAME_HANGER_1 | 36.812500 |
| gantry_vs_fixed_Y45.0 | CBP-M205_L_CARRIAGE_ADAPTER | CBP-D401_A_MOTOR_PLATE_1 | 24.000000 |
| gantry_vs_fixed_Y45.0 | CBP-M208_L_SEPARATE_IDLER_FORK | CBP-D401_A_MOTOR_PLATE_1 | 42.000000 |
| head_vs_moving_supports_X-25.0 | CBP-P403_R1_DUCT_SUPPORT_BRIDGE | CBP-M207_L_REMOVABLE_IDLER_CAP | 10.925000 |
| head_vs_moving_supports_X25.0 | CBP-P403_R1_DUCT_SUPPORT_BRIDGE | CBP-M207_R_REMOVABLE_IDLER_CAP | 10.925000 |

Fixed-return belt collisions below repeat at all three tested Y offsets −20/0/+45. The printed seam tabs and their hardware remain in the vertical return spans even though the main trunks clear the moving idlers.

| X mm | Head part | Belt | Overlap per tested Y mm³ |
|---:|---|---|---:|
| -25 | CBP-P413_R1_LEFT_DUCT_FRONT | CBP-P406_A_9MM_BELT_ROUTE | 2.760000 |
| -25 | CBP-P414_R1_LEFT_DUCT_REAR | CBP-P406_A_9MM_BELT_ROUTE | 1.428077 |
| -25 | CBP-H42_LEFT_SEAM_289_M2p5 | CBP-P406_A_9MM_BELT_ROUTE | 1.331923 |
| 25 | CBP-P415_R1_RIGHT_DUCT_FRONT | CBP-P406_B_9MM_BELT_ROUTE | 11.153697 |
| 25 | CBP-P416_R1_RIGHT_DUCT_REAR | CBP-P406_B_9MM_BELT_ROUTE | 3.456964 |
| 25 | CBP-H41_RIGHT_SEAM_271_M2p5x8 | CBP-P406_B_9MM_BELT_ROUTE | 36.995136 |
| 25 | CBP-H42_RIGHT_SEAM_271_M2p5 | CBP-P406_B_9MM_BELT_ROUTE | 9.401133 |

The original Y−20…+30 support-only stroke remains the previously checked result. Extending it to +45 introduces the four rear-end clashes above. At X±25 the bridge/cap clash remains 10.925 mm³ per side. Center-X checks remain clear, but center clearance cannot establish a buildable Benchy envelope.

The toolhead author additionally reports a sampled isolated ruled-loft wall as thin as 0.472 mm, despite the 1.2 mm nominal offset. That is a separate manufacturing blocker requiring corrected loft/wall construction and renewed self/integration checks; this auditor has not independently repeated that wall-thickness test.

Next resume operation: choose and fully verify the actual Benchy travel envelope, clear the bridge feet and fixed-return seam hardware, correct the thin loft wall, and rerun the focused integration audit before executing/releasing the native head. A narrower X and longer Y candidate must be tested rather than inferred from this failed 50×65 result. The raw final workspace data are preserved under `work/revf-oct21-workspace-50x65-head.json` and `work/revf-oct21-workspace-50x65-support.json`.

## Last four-endpoint check: 40 × 60 mm candidate rejected

The final requested check used only the four corners X=±20 and Y=−23/+37 mm. It **fails** because the forward ducts enter the front drive hardware at the negative Y end. All four corners clear the moving gantry and the gantry clears fixed structure. Both positive-Y corners also clear the tested fixed drive hardware. However, nominal head-to-belt clearance is only **0.200844 mm** at all four corners, before tolerance, belt motion or duct deflection.

The exact negative-Y intersections are recorded below. This is the stopping-point result; no further candidate or geometry change was tested.

| X / Y mm | Head part | Fixed part | Overlap mm³ |
|---|---|---|---:|
| X-20_Y-23 | CBP-P413_R1_LEFT_DUCT_FRONT | CBP-P401_B_LDO_MOTOR_2 | 0.881350 |
| X-20_Y-23 | CBP-P413_R1_LEFT_DUCT_FRONT | CBP-D401_B_MOTOR_PLATE_2 | 155.919372 |
| X-20_Y-23 | CBP-P413_R1_LEFT_DUCT_FRONT | CBP-H502_B_MOTOR_2_WASHER_4 | 1.209337 |
| X-20_Y-23 | CBP-P413_R1_LEFT_DUCT_FRONT | CBP-D402_B_FRAME_HANGER_2 | 302.396532 |
| X-20_Y-23 | CBP-P414_R1_LEFT_DUCT_REAR | CBP-D401_B_MOTOR_PLATE_2 | 106.379414 |
| X-20_Y-23 | CBP-P414_R1_LEFT_DUCT_REAR | CBP-D402_B_FRAME_HANGER_2 | 316.582989 |
| X-20_Y-23 | CBP-H41_LEFT_SEAM_248_M2p5x8 | CBP-D401_B_MOTOR_PLATE_2 | 52.840773 |
| X-20_Y-23 | CBP-H41_LEFT_SEAM_248_M2p5x8 | CBP-H501_B_MOTOR_2_M3X10_4 | 14.304048 |
| X-20_Y-23 | CBP-H42_LEFT_SEAM_248_M2p5 | CBP-D401_B_MOTOR_PLATE_2 | 36.182073 |
| X-20_Y-23 | CBP-H41_LEFT_SEAM_271_M2p5x8 | CBP-D402_B_FRAME_HANGER_2 | 0.432016 |
| X-20_Y-23 | CBP-H42_LEFT_SEAM_271_M2p5 | CBP-D402_B_FRAME_HANGER_2 | 9.898670 |
| X20_Y-23 | CBP-P415_R1_RIGHT_DUCT_FRONT | CBP-P401_A_LDO_MOTOR_2 | 205.320884 |
| X20_Y-23 | CBP-P415_R1_RIGHT_DUCT_FRONT | CBP-D401_A_MOTOR_PLATE_2 | 51.974572 |
| X20_Y-23 | CBP-P415_R1_RIGHT_DUCT_FRONT | CBP-D402_A_FRAME_HANGER_2 | 7.140000 |
| X20_Y-23 | CBP-P416_R1_RIGHT_DUCT_REAR | CBP-P401_A_LDO_MOTOR_2 | 35.082637 |
| X20_Y-23 | CBP-P416_R1_RIGHT_DUCT_REAR | CBP-D401_A_MOTOR_PLATE_2 | 57.240000 |
| X20_Y-23 | CBP-P416_R1_RIGHT_DUCT_REAR | CBP-D402_A_FRAME_HANGER_2 | 46.260000 |
| X20_Y-23 | CBP-H41_RIGHT_SEAM_248_M2p5x8 | CBP-P401_A_LDO_MOTOR_2 | 52.048512 |
| X20_Y-23 | CBP-H42_RIGHT_SEAM_248_M2p5 | CBP-P401_A_LDO_MOTOR_2 | 11.767646 |

The corner data are preserved at `work/revf-oct21-candidate-40x60.json`. All captured builder hashes were unchanged at completion. This evidence does not establish a continuously collision-free, tolerance-safe Benchy-sized workspace. The forward-only dogleg is insufficient: the next revision must consider moving idlers, fixed inner belt returns, beam clamps/caps, and front motor/plate/hanger envelopes together.

**Clean handoff:** 01/05/06 and 07 remain source-frozen at their recorded hashes. 04 is a rejected development head with known travel and thin-wall blockers. Preserve the passed 07/fixed-frame checks and support baseline; resume with a coordinated narrower midheight head/hardware design or an explicitly revised drive layout, then repeat only the relevant self and motion checks. No native manufacturing release or subminute performance validation is implied.
