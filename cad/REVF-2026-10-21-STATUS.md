# Detailed CAD checkpoint — 2026-10-21

Development only. The machine is not ready to manufacture, and no sub-minute Benchy has been physically demonstrated.

## Native Fusion

The old **Codex Benchy Printer RevF AWD CoreXY** cloud version5 is preserved. New work is in **Default Project / Codex Benchy Printer / Codex Benchy Printer RevF Detailed Bowden**.

The completed native bed/Z checkpoint011 has78 unique components,67 unique bodies,280 fully constrained sketches,50 parameters and795 timeline entries. Recompute and feature-health audit reported zero warnings/errors. Exact F3D and STEP hashes are in `cad/native/CBP-RevF-011-Native-Bed-Z-manifest.json`.

The native frame-bracing builder07 was subsequently started. A queued final job saves and exports checkpoint012, then stops the local workbench. Consult `work/fusion_jobs/result.json`, `runner.json` and the012 manifest to establish completion; do not infer it from this planned operation. Builders05/06 exist but have not been executed in Fusion. Native04 remains held. The older native gantry still precedes the frozen150mm carbon-beam revision.

## Detailed source geometry

- Frozen01/05/06: closed150mm carbon beam,140mm rail, four motor plates, hangers, beam clamps, portals, idler forks/caps, recessed mounting hardware and9mm belts. Motor centersX±88.75; motor faces24.5mm below belt planes.148 valid part instances; custom parts are individual single solids.
- Bed/Z:138 valid instances with mounting/leveling/retention hardware. Exact purchased nut, pilot, magnetic stack and thermal design remain held.
- Toolhead04:93 valid individual solids, mandatory Bowden, fixed extruder, separate cold-end fan, split CPAP ducts and actual fasteners. Estimated head mass200.704g before15g carriage and supported tube/wire loads; calculated COM(−0.043,−40.535,280.657)mm. Estimates use proxy component COMs and assumed densities.
- Bracing07:251 instances including three aluminum shear panels, eight gussets, rigid feet, TPU pads and separate fasteners. Its classified overlap checks passed.

## Critical audit findings

The forward cooling-duct dogleg clears the moving idlers at the center, but the proposed50×65 and40×60 travel windows both fail full travel. The40×60 candidate has front-drive clashes atY−23 and only0.200844mm nominal fixed-belt clearance. A Benchy-sized usable envelope has not been validated. Do not change firmware limits to those candidates.

The loft profile offsets also produce walls as thin as approximately0.472mm. Section offsets do not establish normal wall thickness. Redesign the duct as a properly thickened/shelled passage, coordinate its seams/support with the fixed belt returns and front motors, then repeat the head/self/full-travel audit. Detailed pairs, volumes and source hashes are in [the independent audit](../engineering/REVF-INDEPENDENT-CAD-AUDIT-OCT21.md) and [toolhead notes](revf/04_TOOLHEAD_DESIGN_NOTES.md).

Other release holds include exact purchased interfaces, fixed-return axle retention, belt anchors/tensioning, frame-extruder bracket, hose/Bowden/wire sweeps, native joints/parameter-driven placements, motor torque-speed evidence, flow/cooling validation, electronics packaging and manufacturing drawings.

## Backup state

RevF008/009 native rollback archives were committed and their remote manifest/sample identities verified at `ea004fb89331f10c893e5ecfe9a6d8d0b5d40eeb`. Local011 F3D/STEP reconstruction passed. The011 GitHub transfer was interrupted by automatic approval review; its partial-upload status is recorded separately. Do not call it a complete remote backup until every segment is verified and a restore succeeds.
