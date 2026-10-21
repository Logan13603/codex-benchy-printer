# Modular metal mounts: resumable status, 2026-10-21

**Offline source geometry is complete and audited. Native Fusion 05/06 execution is pending.** Do not infer native completion from the source files or STEP exports.

The focused revision contains 64 drive parts and 218 gantry-support parts, including the four revised aluminum motor plates and 24 modular metal hanger parts. Both export manifests were rehashed successfully: 66 listed drive files and 226 listed support files. The full audit, manufacturing/assembly sequence and fastener schedule are in `REVF-METAL-MOTOR-MOUNTS.md`; detailed pair results are in `validation/revf-metal-mount-audit.json`.

There are no undeclared nominal mount clashes above0.01 mm³ against the audited frame, bed, drives, supports and braces. The64 mount intersections are exactly declared screw/thread mates. Continuous gantry Y−20…+30 bounding boxes are separated from every new mount part by at least4.000 mm. Separate toolhead travel issues remain outside this focused result.

Tight exact nominal gaps remain release holds: A-front plate/B return0.200000 mm; OD6 inner motor washers/return0.433753 mm; motor screw head/belt0.600844 mm. Purchased-part tolerances, deformation and actual assembly have not validated these margins. Rear frame M5 access requires the documented top-bar-first assembly order; front access is checked for a4 mm AF Allen key through diameter6 holes.

## Frozen source and next native operation

`validation/revf-metal-mount-source-hashes.json` records the complete SHA-256 values for `05_drives_cq.py`, `06_gantry_supports_cq.py`, `05_drives.py`, `06_gantry_supports.py` and the required shared `motor_mount_dimensions.py`. Keep those files together. No builder or CQ geometry changes were made for this status note.

Load `common.py`, the tested04 helper definitions, `05_drives.py` and `06_gantry_supports.py`. Execute separate short operations, one station at a time:

```python
build_native_drive_station('A', 1, False)
build_native_motor_station('A', 1, False)
import_native_drive_station_hardware('A', 1)
import_native_motor_station_hardware('A', 1)
```

Then repeat for A2/B1/B2. Station1 is rear; station2 is front. Inspect the document before retrying any timed-out mutation: a response timeout does not prove that the native operation stopped. Custom builders reject duplicate named components. Hardware import stages skip existing components.

Root's native02R2 replacement reached the300-second response timeout, and its read-only inspection was pending when this note was requested. This note does not claim the replacement finished or failed. The modular mounts have not yet been executed natively.

## Source/cloud checkpoint intent

The metal mount source, audit and export manifests form the resumable **source checkpoint**. The last cloud version explicitly reported to this subtask was the complete whole assembly at version4, before native05/06 integration. Parent recovery may establish a later verified cloud checkpoint; record its actual Fusion version and saved component counts before treating it as current.

After the pending native operation is inspected and the document responds, the intended **cloud checkpoint** is: preserve the recovered assembly, execute one metal mount station, recompute and inspect its component/body/sketch status, save a new Fusion cloud version, then export and verify a matching native archive/STEP before advancing. Record actual Fusion version, archive checksums and source commit in the project manifest and `RESUME.md`. Until those actions are verified, describe these mounts as offline-complete/native-pending.
