# Current checkpoint: display, metal mounts and native recovery

2026-10-21. This supersedes older checkpoint012 status. Development CAD; manufacturing release and sub-minute performance remain unvalidated.

## Last verified native state

Default Project / Codex Benchy Printer / **Codex Benchy Printer RevF Detailed Bowden, cloud v5**. Local **013 Complete-Bracing-Display** contains562 unique components,318 bodies,423 fully constrained sketches,54 user parameters and1832 timeline entries; no feature-health warnings. The full07 hardware import eventually completed after the reentrant runner prematurely exported partial012. Runner is stopped; do not restart without a BUSY guard.

013 F3D/STEP/manifest are local in cad/native. Hashes are recorded in the manifest. Files have not been uploaded or reopened for restore verification.008/009 remains the latest complete GitHub native rollback set;011 has36/45 chunks.

## Shading

Saved visible edges, opaque bodies, bead-blasted aluminum, matte blue printed parts, black carbon/rubber and steel hardware. Do not rerun whole-assembly08_display.py: hundreds of appearance writes stalled Fusion for many minutes. Apply appearances only to new parts.

## Exact next operation

**Inspect Fusion before any mutation.** Native02_motion_r2.py was started with explicit `REPLACE_OLD_190_180_GANTRY_AFTER_CHECKPOINT` after013. Its MCP call timed out at300s; a subsequent read-only state query also timed out. UI showed Not Responding. Completion and staging are unverified. Do not retry02 or start05/06 until live state is known.

If Fusion recovers, verify all six150/140mm gantry bodies against the contract, fixed21 preservation, and any staging subtree. Save, audit and export014 only after a coherent result. If recovery fails, reopen013/cloudv5 rather than treating the operation as complete. Do not discard unsaved work before inspecting recovery options.

## Detailed motor mounts

Offline source is complete and audited:64 drive parts and218 support parts, including four6mm6061 motor plates and six metal mount pieces per station. Native05/06 has not run. Read [mount design](REVF-METAL-MOTOR-MOUNTS.md), [native entry points](REVF-METAL-MOUNTS-NATIVE-STATUS.md) and validation/revf-metal-mount-audit.json.

Load common.py,04 helper definitions,05 and06; build per station with hardware separately. Do not call04.run. Tight nominal0.200mm plate/idler and0.434mm washer/idler gaps remain tolerance holds. ReducedY-20..+30 mount sweep clears by at least4mm; this does not validate the complete head workspace.

## Native cut-scope defect

Legacy extrusion cuts could target other assembly components. Current common.py scopes Cut/Intersect to owned bodies;04 loft cuts do likewise. This does not repair existing features. The old190mm carbon beam was trimmed to150mm by socket cuts;02's guard recognizes only the reviewed feature/bounds signature. Legacy03 cassette/cover cuts may have split the Z screw (two bodies in prior manifests). Join scope also needs review. Read [cut audit](REVF-NATIVE-CUT-SCOPE-AUDIT-OCT21.md) before manufacturing or rebuilding03.

## Remaining holds

Head04 failed full travel, with duct walls sampled down to0.472mm. No demonstrated Benchy-sized envelope or physical sub60 result. After native recovery/mounts, redesign true duct wall thickness and head/idler/belt/front-motor clearances, then check hose/Bowden/wire sweeps. Exact purchased interfaces, hardware retention, joints, drawings, electronics and physical motor/flow/cooling evidence remain pending.

Automatic review rejected binary backup-payload staging in a prior step. Do not bypass via a different tool. Text source/documentation backup is independent. No usage reset used; save early and stop near1% remaining.
