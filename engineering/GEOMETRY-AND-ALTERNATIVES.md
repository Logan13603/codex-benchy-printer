# Spatial accuracy and architecture screening — checkpoint 007

The hard budget remains removed. These calculations investigate cheaper ways to satisfy the original full-size geometry and 50–55-second target. **No candidate passes the performance gate.** All times are calculated with assumed capabilities; no machine was built or tested.

## Spatial path preservation

The new study compares each of 4,594 uninterrupted same-role/layer deposition strokes only to itself. It uses the original pinned Cura slice and the checkpoint-006 polynomial smoother, with a 25-microsecond grid. Nearest-neighbor distances bound the Hausdorff distances between the original and sampled, piecewise-linear smoothed command centerlines. Reference samples are at most 0.04 mm apart; each direction's bounds include half the applicable endpoint spacing. Analytic offset-line and right-angle-shortcut cases pass.

| smooth_zv frequency | Largest original outer-wall departure from its smoothed stroke, bounded | Original / smoothed deposition-interval length |
|---|---:|---:|
| 100 Hz | 4.201–4.242 mm | 1.516 |
| 200 Hz | 1.653–1.695 mm | 1.234 |
| 400 Hz | 0.535–0.570 mm | 1.087 |
| 800 Hz | 0.162–0.205 mm | 1.032 |

![Calculated chimney paths](figures/spatial-smoothing.png)

These are command-centerline results, not measured bead dimensions. Deposition intervals retain their original, centroid-aligned timing; real extruder synchronization and melt dynamics are not modeled. A smoothed extruder may redistribute material outside those intervals. If original volume were deposited over the shortened intervals, average material per path length would rise. The ratios are not recommended flow corrections and cannot certify a nozzle-width violation or compliant finished part. The depicted open ends also reflect the chosen deposition interval, not a predicted physical seam.

The strong smoothing cases substantially change spatial geometry, beyond the previously reported time-aligned displacement. Narrow smoothing preserves geometry better but retains high drive demand. These frequencies are sensitivity inputs, not measured resonance settings. See [numerical data](spatial-results.json) and [previous study](SMOOTHING-STUDY.md).

## Four-cable moving-bed mechanism

A four-cable planar platform needs yaw restraint as well as XY force. With frame anchors at (±150, ±150) mm and proportional square attachments at (±55, ±55) mm, the first-order XY/yaw wrench map has rank two at every one of 2,275 sampled poses. This layout does not independently control yaw. Prestress or an external guide can supply stiffness, but neither is analyzed as a substitute here.

Changing bed attachments to (±95, ±55) mm gives full rank and a strictly positive tension self-stress throughout the sampled ±32 × ±17 mm working range. With yaw normalized using a 100 mm length scale, the worst sampled condition number is 1.977. These are concept coordinates, not frozen manufacturing interfaces.

For fixed yaw, cable length L, unit pull direction u, bed velocity v, acceleration a and drum radius r:

`q = -L/r; q_ddot = [u·a - (v·v - (u·v)^2)/L]/r`

The model balances XY force and zero yaw moment, then chooses the redundant tension coordinate to minimize peak absolute motor torque while maintaining at least 5 N in every cable. It includes the 48e-6 kg m² reference rotor and a 7.5 g drum with inertia factor 0.5. Bed mass remains an assumed 60 g. At 25 mm drum radius:

| Smoother | Largest motor torque | Largest cable tension |
|---|---:|---:|
| 200 Hz | 9.096 Nm | 234.3 N |
| 400 Hz | 10.693 Nm | 278.0 N |
| 800 Hz | 13.958 Nm | 342.6 N |

The 40 and 60 mm drum trials increase the peak demand in this geometry. At 25 mm radius the peak speed is about 917 rpm; peak torque and peak speed do not necessarily coincide. Full per-motor values and coincident speed are in [cable-results.json](cable-results.json).

This is a 100-microsecond screening grid, not a converged dynamic certification; high-frequency peaks need refinement before design use. Optimal tension control is a favorable assumption: an open-loop position-controlled winch does not independently command arbitrary cable pretension. Cable stretch, elastic spool correction, friction, compliance, electronics, frame/boat flex and actuator current limits remain absent. No constant 2.2 Nm reference is treated as a torque-speed curve. The result rejects this tested four-cable proposal as a supported cheap solution, not every possible cable robot.

Independent checks: finite-difference cable second derivative agrees within 0.001 m/s²; force/moment and power balances pass; three separate linear-program solutions match the nullspace torque allocator within 1e-7 Nm.

Bed clearance must include the moving boat, not just the moving plate. A 60.001 × 31.004 mm boat over ±32 × ±17 mm motion sweeps at least 124.001 × 65.004 mm in XY. This affects upper capture plates, supports and cables. A tiny upper glass opening around the stationary nozzle cannot clear the complete moving boat. Detailed support geometry and actual mass are still needed.

## Thinner-wall re-slicing

Three pinned Cura trials preserve two walls, three top/bottom layers, 10% infill, model scale, 0.25 mm layers and the 0.5 mm maximum width. Only wall widths/thickness change; skin and infill remain 0.5 mm. All three have zero definite rounding-aware width violations, which is not complete local coverage or physical compliance certification.

| Outer / inner widths | Calculated PLA mass | Best tested time |
|---|---:|---:|
| 0.50 / 0.50 mm, baseline | 11.060 g | 54.299 s |
| 0.45 / 0.45 mm | 10.579 g | 56.345 s |
| 0.40 / 0.50 mm | 10.591 g | 56.509 s |
| 0.40 / 0.40 mm | 10.036 g | 57.600 s |

Best rows use the same artificial V2400, A2 million, SCV500, Q300 and first-layer300 caps, without the minimum-layer floor. Thinner walls reduce polymer volume but increase path and repositioning length. Keep 0.5/0.5 as the faster tested baseline; a thinner wall is not automatically faster. [Full width results](width-study-results.json), settings, source hashes and analysis G-code are preserved.

## Multiple independent toolheads

An additional screen clips the original deposition segments into spatial bands without removing material or adding internal partition walls. Each head retains original segment order and repositions between assigned segments. Each layer ends at rest; a shared Z move follows. The assumed cooling floor is 0.2 s. This is one scheduling method, not a globally optimal lower bound.

At 1,500 mm/s, 500,000 mm/s², SCV50 and 150 mm³/s per head, the fastest tested cases are: two X bands 91.67 s, two Y bands 80.20 s, three Y bands 76.59 s and four Y bands 71.34 s. Increasing the two-head Y case to V2400, A1 million, SCV500 and Q200 per head yields **58.24 s**, still above the 55-second target before collision delays.

These figures exclude collision avoidance, seam bonding, head-envelope constraints, retraction and pressure dynamics, actual motor capability, synchronization and controller implementation. Multiple heads on a 60 mm part cannot be assumed to print simultaneously near their boundary. The frozen public [Annex announcement](https://www.youtube.com/watch?v=7zkKcFtLAks) does not explicitly specify a head-count limit; that absence is not organizer approval of a collaborative entry. No entry is submitted and no rules are relaxed.

This tested alternative lacks enough margin to justify buying extra heads and drives. [Partition results](parallel-head-results.json) and [expanded two-head grid](parallel-head-expanded-results.json) preserve the evidence.

## Decision and next operation

Keep the stationary-XY hotend/light moving-bed direction under investigation, but do not freeze the rejected cable mechanism. The next useful design comparison is a fully constrained mechanical guide or parallel linkage that supplies yaw restraint, with pose-dependent mass, tracking compensation and stiffness included. A measured high-flow/cooling test remains necessary. An inexpensive motor with similar holding torque cannot inherit another motor's dynamic behavior.

Before extending numerical claims, refine only shortlisted high-frequency cases and reconcile extrusion timing with smoothed geometry. Detailed Fusion manufacturing CAD, a purchasable final BOM and ready-to-run firmware remain gated. No supported cheapest total price is established.
