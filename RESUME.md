# Resume checkpoint 007 — revision C

Latest instruction: no hard budget; make the cheapest credible full-size sub-minute printer. Keep 50–55 seconds as target and three consecutive compliant sub60 prints as physical acceptance. Do not ask questions; choose reasonably. Owner has Pi, CPAP blower/hose, SD/cord, 9 mm belts/pulleys and some screws, identities still unknown. Do not consume reset credits. Stop cleanly near 1% usage; weekly limit was at 95% used when checkpointing began, five-hour at 70% used.

## Completed this checkpoint

Read engineering/GEOMETRY-AND-ALTERNATIVES.md and current FEASIBILITY.md. New studies: spatial_study.py / spatial-results.json; cable_geometry.py / cable-results.json; width_optimize.py / width-study-results.json; parallel_heads.py / parallel-head*.json. Three complete new slices are under slicing/cura-width-study. Original model/rules remain unchanged. No physical validation or purchase.

Spatial screen: 4,594 strokes, dt25us, 0.04mm reference sampling. Bounded worst outer-wall reference-to-smoothed departure:100Hz4.20–4.24mm;200Hz1.65–1.70;400Hz0.535–0.570;800Hz0.162–0.205. Deposition intervals are unmodified; actual extrusion synchronization is not simulated. Figure was regenerated with readable labels.

Four-cable layout: anchors ±150/±150mm; attachments ±95/±55mm; 60g assumed bed; 5N minimum tension. Radial square layout lacks independent first-order yaw control. Rectangle passes sampled rank/positive-self-stress checks. At r25mm, peak per-motor torque9.096/10.693/13.958Nm at200/400/800Hz. dt100us screening only. Tests include length Hessian, wrench/power balance and three independent LP comparisons. Optimal tension control is a favorable assumption, not a working open-loop implementation.

New widths0.4/0.4,0.45/0.45,0.4/0.5 all have zero definite width violations and are slower than0.5/0.5 at common extreme caps. Two-head Y partition reaches58.23945s atQ200 per head,V2400,A1million,SCV500,0.2s layer floor; collisions/seams/real drives excluded. Do not call it a sub55 design or ready-to-run profile.

## Exact next engineering operation

1. Verify checkpoint-007 external manifest against local ZIP and file-manifest. It records its source commit and remote verification scope. Never claim full restore from metadata-only checks.
2. Preserve rejected alternatives. Next investigate mechanical yaw guidance or a parallel-link bed with full pose-dependent inertia, tracking compensation and compliance. Do not reuse the cable fixture as a selected machine.
3. Reconcile actual extrusion synchronization with spatial geometry, then refine only shortlisted high-frequency cases. Measured high-flow/cooling evidence remains missing; do not assign compressed-air capability to the owned CPAP.
4. Re-run the performance gate before detailed manufacturing CAD. Do not relax the frozen model/shell requirements or replace operating torque with holding torque.

## Fusion state

Computer use only, no Fusion MCP. Verified folder Default Project / Codex Benchy Printer. Fresh app window1968006 was found this turn; reacquire before input. Blank Untitled* document, mm/g, now Hybrid Design (conversion completed). No components, sketches, geometry or saves exist. Command-search typing did not enter the intended text; repeated detected input/window focus changes and non-target-window guards interrupted reference-layout creation. Last successful observation was the blank Hybrid Design; last attempted New Component click was rejected because the point was over Explorer. No new component dialog was reached. No CAD archive/STEP/cloud version exists. Do not claim CAD backup.

Use @oai/sky through node_repl after reading the computer-use skill. Select one returned app/window, observe, take exactly one action, refresh. A blank conversion is the only Fusion change so far. Do not repeat input against stale screenshots or target guards.

## Verified previous backup

Checkpoint006 source1f6e48cb7895c573014b8d1b58c8f5a2d0816559; final remote head7c7f9605981e38dfd5a7c1f7d9277ce17676f1e4; tree331687043d7435110f0eb640bb15f2a18ce8fef5. Complete ZIP24,744,088bytes; SHA25627614af9da93814d78541c0c6eb207ca18dbe9c3d2bbbcdf09798ab155419b34; Gitblobe7a0c123442f43c8e0c73f7a7d79a0cdeb246b8. Source, ZIP identity and manifest readback verified. Full remote ZIP redownload/extraction unverified. Latest007 external manifest supersedes these publication pointers once uploaded.

Private repo https://github.com/Logan13603/codex-benchy-printer . Engineering root outputs/codex-benchy-printer. Python C:/Users/logan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe. Optional --numpy-dir work/python-libs; NumPy2.5.3, SciPy1.18.1. Cura binary work/cura413/CuraEngine.exe. Runtime binaries and full research transcripts are excluded from backup. Current publication state is also in work/remote-state.json.
