# CAD progress — development checkpoint 003, 2026-09-22

RevE checkpoint 003 is saved as Fusion cloud version **5**. The 12 mm aluminum base is now **300 × 260 mm**, with the same centered 148 × 98 mm bed-sweep opening and four Ø9 mounting holes. The rear columns are on 180 mm centers at machine Y +90 mm, 180 mm high, with a 220 mm crossbeam. The base volume is 758.898 cm³, about 2.05 kg at 2.70 g/cm³. This is a compact development frame, not an optimized or stress-verified final structure. Nominal clearance between the swept 112 mm stage and the rear column faces is only about 8 mm before hardware. All **18 sketches remain fully constrained**; there are **54 named parameters**. See `CBP-0000-RevE-parameters.csv` and `native/checkpoint003-manifest.json`.

The purchased guideway dimensions are sourced from the [HIWIN guideway catalog](https://www.hiwin.com/wp-content/uploads/HIWIN-Linear-Guideway-Catalog.pdf). The MGN7 rail and MGN7H block are still simplified envelopes with no mounting holes. No mechanism joints, belts, motors, Z carriage, extrusion, cooling or electronics have been modeled yet. Sub-minute operation remains an untested hypothesis, not a claim from this CAD.

## Previous checkpoint 002

The user authorized Fusion MCP scripting on 2026-09-22 to accelerate the CAD. Native design **Codex Benchy Printer Main** is saved in **Default Project / Codex Benchy Printer**, verified Fusion cloud version **4** (`urn:adsk.wipprod:fs.file:vf.wAwg5QGJR0iXFu87oGiFbA?version=4`). Fusion's native coordinate convention in this design is machine X = Fusion X, machine Y = Fusion −Z, machine Z = Fusion Y.

Current organized tree: `10_FRAME`, `20_XY_MOTION`, `30_BED`, `40_Z_AXIS`, `50_TOOLHEAD`, `60_CPAP_COOLING`, `70_ELECTRONICS`, and `80_HARNESS`. The first three groups contain sixteen solid body instances: a 400 × 400 × 12 mm base with a 148 × 98 mm sweep aperture and four Ø9 mounting holes, two 40 mm Z-column envelopes and crossbeam, two matched rail shims, a low crossed-guide arrangement, a 112 × 84 × 2 mm carbon-stage stock envelope, a 76 × 50 × 3 mm bed substrate, and a 0.25 mm build-surface film. The purchased MGN7 rail/carriage models are **envelope proxies**; raceways, rail mounting holes, fasteners and exact supplier variant remain to be detailed. The Fusion audit found **18 sketches, all fully constrained**, 53 user parameters, and an editable feature timeline.

This is development geometry, **not a build-ready or performance-validated printer**. The guide mechanism is not yet joined or belted; motors, Z motion, toolhead, extruder, hotend, CPAP duct, electronics, harness, service clearances and manufacturing details remain. Reference dimension and mass assumptions are in the CSV and CAD scripts. The sub-minute time calculation still depends on unproven motion, flow and cooling limits.

[Native Fusion and STEP checkpoint files](native/) are accompanied by [hash/backup manifest](native/checkpoint002-manifest.json). Source scripts are in [fusion/](fusion/). Reopen the exported F3D and verify local geometry before release; the exports currently demonstrate a recoverable development checkpoint, not manufacturing acceptance.

Next CAD sequence: finish rail and carriage interfaces plus attachment/kinematic joints; then belt/motor routing; Z carriage and stationary-XY hotend; CPAP duct and hose support; wiring and electronics. After each stage, audit constraint status, interference, moving mass and toolhead center of mass, save Fusion cloud and export native/STEP backups.

