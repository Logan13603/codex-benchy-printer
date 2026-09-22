# Motion smoothing and primary evidence — checkpoint 006

The hard budget remains removed. This checkpoint adds primary-source evidence and a reproducible motion-smoothing study. **It does not select a build-ready printer or pass the 50–55-second performance gate.**

## Newly recovered primary evidence

The creator's [Minuteman final episode](https://www.youtube.com/watch?v=iMAWa9vfxcE) was accessible on this turn. Its auto-generated transcript and selected video frames were inspected; the complete transcript is retained only in temporary research, not redistributed.

At 34:47 the screen identifies Nanotec SCB5618L4204-B. The narration describes 50 mm pulleys, approximately 2.2 Nm at 570 rpm, 60 V motor power and 3 A configured current. The overview describes a custom, two-zone hotend and an approximately 60 g moving platform. The slicing discussion explicitly includes reduced bridge/top densities, contour compensation and a 0.95 flow ratio; it also describes aggressive smoothing and corner rounding. Those modifications cannot certify this project's stricter slice. The firmware discussion names Kalico bleeding-edge-v2 and a not-yet-released winch derivative. These are creator-reported details, not independent measurements.

The [Nanotec manufacturer page](https://www.nanotec.com/us/en/products/2892-scb5618l4204-b) specifies 480 g cm² rotor inertia (48e-6 kg m²). Its published winding-current conditions must be reconciled with driver RMS/peak conventions before using a curve as a guaranteed margin. A similar-sized cheaper motor cannot inherit this motor's performance.

## What the new calculation does

`smoothed_motion.py` samples the existing pinned Klipper Move/LookAheadQueue trajectory and convolves polynomial kernels from a pinned Kalico source. Kalico source commit: `e0a57a0b55c65d8b9112c812a01bd32f88476618`; source, license and hashes are under validation/third_party/kalico. The [Kalico documentation](https://github.com/KalicoCrew/kalico/blob/main/docs/Bleeding_Edge.md) distinguishes continuous polynomial smoothers from conventional discrete shapers.

Base assumptions remain V2400 mm/s, A2000000 mm/s², SCV500, Q300 mm³/s, with first-layer deposition limited to 300 mm/s. Calculated base time is **54.29852 s**. This is the same rigid commanded trajectory as before, with no motor tracking or structural dynamics.

The illustrative mechanical fixture has two motors on each independent Cartesian axis, 60 g translating mass per axis, 30 mm-radius drums, 48e-6 kg m² rotor inertia per motor, and 7.5 g drums with inertia factor 0.5. It excludes belts, idlers, bearings, friction, load-sharing error, frame flex and electrical dynamics. It is not a cable robot, exact BOM, or selected machine.

## Results using the finest 10-microsecond grid

| Hypothetical smoother | Frequency | Maximum time-aligned XY departure during deposition | Maximum inertial torque on either axis, per motor |
|---|---:|---:|---:|
| smooth_zv | 50 Hz | 10.410 mm | 2.128 Nm |
| smooth_zv | 100 Hz | 4.711 mm | 3.686 Nm |
| smooth_zv | 200 Hz | 1.842 mm | 5.359 Nm |
| smooth_zv | 400 Hz | 0.581 mm | 6.485 Nm |
| smooth_zv | 800 Hz | 0.185 mm | 9.431 Nm |
| smooth_mzv | 200 Hz | 2.014 mm | 4.683 Nm |
| smooth_mzv | 400 Hz | 0.685 mm | 6.630 Nm |
| smooth_mzv | 800 Hz | 0.214 mm | 9.350 Nm |

The departure metric compares the smoothed path to the original command at matching, centroid-corrected times. **It is not a nearest-surface distance, printed dimensional error, or inspection of a finished Benchy.** Along-path displacement contributes to it. Surface/feature loss must be assessed separately; these values cannot by themselves certify or reject physical quality.

The calculation demonstrates a tradeoff on this path: strong smoothing lowers peak inertia demand but substantially changes the trajectory. Narrow smoothing preserves it more closely while retaining large torque demand. No row has a verified operating torque-speed margin. The reported frequencies are sensitivity inputs, never recommended printer.cfg values.

## Cooling floor

Applying a minimum-time floor to each of the 192 existing layer durations gives:

| Minimum layer time | Optimistic total |
|---|---:|
| 0.10 s | 56.081 s |
| 0.15 s | 57.852 s |
| 0.20 s | 61.287 s |
| 0.24 s | 64.839 s |

This is an optimistic floor calculation, not a re-sliced cooling profile. Actual slowdown changes motion, flow and thermal behavior. It shows that the nominal 54.30-second case has no established cooling margin. The owned CPAP system still needs pressure-flow and local cooling evidence; compressed-shop-air performance cannot be assigned to it.

## Verification and limits

The calculation integrates the polynomial kernel over each sampling bin, normalizes it, checks a straight-motion unity-gain/centroid identity, and retains the padded trajectory tail during alignment. A detected end-clamping artifact was corrected before these results were saved. Runs at 100, 25 and 10 microseconds are preserved. From 25 to 10 microseconds, peak-torque changes are at most 0.15% through 200 Hz, 1.34% at 400 Hz and 3.09% at 800 Hz. The 800 Hz rows are still resolution-sensitive and need further convergence before design use. This is not an independently validated firmware emulator.

Missing: real extruder junction limits, pressure-advance synchronization, step quantization, MCU capacity, plant response, structural modes, spatial surface error, temperature/flow coupling, and physical acceptance. Standard winch source also lacks implemented homing/boundary checks; it is not ready-to-run printer firmware for this project.

## Next engineering decision

Use spatial feature-preservation metrics and motion/flow/cooling co-optimization before selecting a cheap drive. Compare a lightweight crossed-rod bed with a planar cable/link system using actual geometry, Jacobians, tension/pretension and all moving masses. The closed-loop/custom-firmware implications must be costed explicitly. A larger motor alone does not establish the cheapest credible solution.

Reproduce with `python engineering/smoothed_motion.py --dt 0.00001`; provide a NumPy installation or `--numpy-dir`. No CAD geometry, assembly, manufacturing files or physical test was completed in this checkpoint.
