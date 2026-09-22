# CAD progress — development checkpoint 002, 2026-09-22

The user authorized Fusion MCP scripting on 2026-09-22 to accelerate the CAD. Native design **Codex Benchy Printer Main** is saved in **Default Project / Codex Benchy Printer**, verified Fusion cloud version **4** (`urn:adsk.wipprod:fs.file:vf.wAwg5QGJR0iXFu87oGiFbA?version=4`). Fusion's native coordinate convention in this design is machine X = Fusion X, machine Y = Fusion −Z, machine Z = Fusion Y.

Current organized tree: `10_FRAME`, `20_XY_MOTION`, `30_BED`, `40_Z_AXIS`, `50_TOOLHEAD`, `60_CPAP_COOLING`, `70_ELECTRONICS`, and `80_HARNESS`. The first three groups contain sixteen solid body instances: a 400 × 400 × 12 mm base with a 148 × 98 mm sweep aperture and four Ø9 mounting holes, two 40 mm Z-column envelopes and crossbeam, two matched rail shims, a low crossed-guide arrangement, a 112 × 84 × 2 mm carbon-stage stock envelope, a 76 × 50 × 3 mm bed substrate, and a 0.25 mm build-surface film. The purchased MGN7 rail/carriage models are **envelope proxies**; raceways, rail mounting holes, fasteners and exact supplier variant remain to be detailed. The Fusion audit found **18 sketches, all fully constrained**, 53 user parameters, and an editable feature timeline.

This is development geometry, **not a build-ready or performance-validated printer**. The guide mechanism is not yet joined or belted; motors, Z motion, toolhead, extruder, hotend, CPAP duct, electronics, harness, service clearances and manufacturing details remain. Reference dimension and mass assumptions are in the CSV and CAD scripts. The sub-minute time calculation still depends on unproven motion, flow and cooling limits.

[Native Fusion and STEP checkpoint files](native/) are accompanied by [hash/backup manifest](native/checkpoint002-manifest.json). Source scripts are in [fusion/](fusion/). Reopen the exported F3D and verify local geometry before release; the exports currently demonstrate a recoverable development checkpoint, not manufacturing acceptance.

Next CAD sequence: finish rail and carriage interfaces plus attachment/kinematic joints; then belt/motor routing; Z carriage and stationary-XY hotend; CPAP duct and hose support; wiring and electronics. After each stage, audit constraint status, interference, moving mass and toolhead center of mass, save Fusion cloud and export native/STEP backups.

