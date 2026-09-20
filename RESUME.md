# Resume checkpoint

## State

- Requirements accepted on 2026-09-20.
- Feasibility gate pending. No architecture or purchased interfaces frozen. This is checkpoint 001, not a completed feasibility report.
- Fusion inspected: blank unsaved design; destination `Default Project / Codex Benchy Printer` exists and was empty. No CAD edits performed.
- Original CreativeTools single-part STL downloaded from its official GitHub repository, linked by 3dbenchy.com.
- Installed OrcaSlicer CLI identifies version 2.3.2. `--help` alone returns no text; `--debug 5` confirms CLI execution.
- Private GitHub repository created and verified: https://github.com/Logan13603/codex-benchy-printer . Initial requirements commit: 67487a8a97530fdc8ecf3f69c56462504935d9ca.
- Reproducible OrcaSlicer 2.3.2 analysis slice completed: 192 layers, unscaled original mesh, nominal 0.50-mm extrusion widths, 0.25-mm layers, 2 walls, 3 top/bottom layers, 10% rectilinear infill. Full settings audit pending.
- Preliminary arithmetic: 8757.07 mm3 deposition, 10.859 g PLA at density 1.24 g/cm3, 77.63 m extruding path. A 55-second print requires at least 159.22 mm3/s average over the ENTIRE print; peak flow must exceed that. At a hypothetical 75 mm3/s continuous cap, extrusion alone takes 116.76 seconds. These are properties of this slice, not proof of an absolute optimum or global impossibility.
- Usage check at checkpoint: 89% of five-hour window consumed, 19% weekly consumed. End cleanly and await user resume. No reset credits used.

## Next operation

1. Verify checkpoint archive SHA256 and repository main commit before continuing. Extract if local project is unavailable.
2. Audit effective settings in analysis.3mf and analysis.gcode (especially bridge width, thin features, shell thickness, minimum layers, and actual original-model geometry). Read the rules sources; original Annex video fetch failed, so do not claim current Annex rule certification.
3. Add an explicit reslice runner: run slicing/prepare_slice.py, then Orca CLI with --debug 2 --slice 0 --load-settings "machine.json;process.json" --load-filaments filament.json --outputdir slicing --export-3mf analysis.3mf and the original STL. Use resolved full paths. Extract Metadata/plate_1.gcode from the 3MF as slicing/analysis.gcode. CLI emits plate_1.gcode too.
4. Implement and test acceleration/corner/flow-limited path analysis; compare nozzle widths 0.4–0.5 mm and permissible infill combinations without deleting model features.
5. Compare miniature CoreXY, independent Cartesian/light bed, crossed gantry, and delta using documented masses, force planes, reflected rotor inertia, torque-speed data, and CPAP system curve. Source a genuine >160 mm3/s small-nozzle candidate or establish that evidence is insufficient under $500 delivered. Complete priced candidate BOM and uncertainty ledger.
6. Resolve feasibility gate. If unsupported, publish the evidence and stop before detailed CAD. Do not silently relax budget/rules or make a slower printer.

## Persistence

Save each completed milestone locally and remotely. At 15% remaining usage, begin checkpoint/export; aim to end by 10%. Record exact next operation, remote commit, source/model hashes, and Fusion version. Do not consume reset credits.
