# Checkpoint 007 additions

Spatial study checks known offset-line and right-angle distances and preserved stroke volume. Cable study checks a finite-difference length Hessian, force/moment equilibrium, mechanical power balance and three independent scipy.optimize.linprog solutions. New width trials preserve model/engine/definition hashes, independent deposited-volume parsing and rounding-aware width audits. Parallel partitioning conserves original deposited volume within1e-6mm³. All remain numerical screening with exclusions documented in engineering/GEOMETRY-AND-ALTERNATIVES.md. SciPy1.18.1 and NumPy2.5.3 were used. No manufacturing or full physical simulation is certified.

# Checkpoint 006 additions

See engineering/SMOOTHING-STUDY.md for kernel integration, centroid identity, endpoint handling, three-resolution comparison and limits. Primary Kalico source is archived and hashed under validation/third_party/kalico. No full firmware or physical validation is claimed.

# Numerical verification — checkpoint 005 additions

`engineering/expanded_study.py` checks ideal-drive scaling and load/rotor inertia equivalence, then compares the hypothetical 51.748792767 s case to pinned Klipper planner classes within 0.00001 s. Finite queue gives the same rounded time; minimum cruise ratio 0.5 gives 52.603027 s. The same hardware/thermal/quality exclusions below remain. The new scenario is not a measured or validated printer capability.

The ideal-axis formula is verified algebraically by differentiating acceleration with respect to pulley radius: its maximum occurs at r²=nJ/M. Four identical motors double that ideal maximum relative to one, rather than quadrupling it, after the optimum radius is adjusted. This is not a CoreXY/delta model.

Historical checkpoint 004 checks follow.

# Numerical verification — checkpoint 004

Results are calculated or reproduced digitally. None is a physical machine measurement.

1. `python engineering/test_path_model.py` checks seven analytical cases: triangular/trapezoidal moves, straight-line partitioning, reversal, flow bound, corner slowdown and an externally supplied acceleration cap.
2. `python engineering/validate_klipper_planner.py` loads only unmodified upstream Move/LookAheadQueue classes from commit `ce7002bedf37e938bb483572949f3703ac6476cb`, verifies the archived source hash, and compares three synthetic cases plus Orca/Cura paths. Unlimited and finite lookahead agree for the checked cases; minimum cruise ratio 0.5 increases the no-gap Cura time from 192.04 to 202.89 s.
3. `python engineering/cura_study.py` compares baseline and simplified paths and checks the latter against the same pinned planner. Simplified result: 181.179331874 s versus 181.179331336 s. This independently checks planner implementation, but shares parsed moves and artificial limits; it is not a full firmware test.
4. `python engineering/audit_cura.py` independently parses raw G-code extrusion/motion, accounts for coordinate/E rounding and records every definite width violation. Original Cura optional gap fill: 95 violations. No-gap and simplified: zero. Combined infill is allowed up to 0.5 mm height; local stack placement, complete shells, actual deposited width and physical dimensional quality are not certified.
5. Reproduced the simplified slice using the checked-in runner and matching engine/definition hashes. G-code is byte-identical: SHA256 `0c9b7be63971d47e277d7d356e355679426fbcb2a8689739ef0f186c0d45722d`.
6. `python engineering/architecture_path_screen.py` verifies force/energy identities for Cartesian/CoreXY/crossed drives before computing the scenarios. Unit conversion is explicit: g cm² × 10⁻⁷ = kg m²; g mm² × 10⁻⁹ = kg m².

The two independent parsers agree on deposited Cura volume to less than 10⁻⁶ mm³. All checked final deposition layers reach Z48 mm in 192 steps of 0.25 mm. Numerical width checks use Cura's rectangular cross-section model. Rounding-safe non-rejection is not proof of complete competition compliance. The Cura CLI's placeholder TIME:6666, Filament used:0 and sentinel bounds are deliberately ignored.

Klipper source and GPLv3 license: [archived provenance](third_party/klipper/PROVENANCE.json). Cura LGPLv3 definitions/license: [archived provenance](../slicing/third_party/cura-4.13.1/PROVENANCE.json). Engine executables are not redistributed.
