# Resume checkpoint 004

**Feasibility gate NOT PASSED. No detailed CAD authorized under the accepted gate until performance and budget are supported together.** Read engineering/FEASIBILITY.md first. Do not quietly change the target or budget.

Current target: 50–55-second full-size SpeedBoatRace Benchy; physical acceptance is three consecutive compliant prints under 60 seconds. Budget: $400 NEW delivered spending. Owner has Pi, CPAP fan, fan pipe, SD, cord, 9 mm belts/pulleys and some screws. Prefer 9 mm. Exact models, pulley pitch/teeth/bore, hose geometry and fastener inventory are unknown. Ask no questions; make bounded assumptions explicit. User requested stopping with about 1% five-hour usage remaining; check usage at milestones and checkpoint early enough. No reset credit is authorized or used.

## Completed at this checkpoint

- Prior checkpoint 003 delta archive SHA256 matched its remote manifest at resume. Its parent checkpoint 002 remains preserved.
- Current budget reference $505.40; $391.64 is an unquoted allocation, not a validated BOM.
- Original mesh, checksum, frozen public rules and Orca 2.3.2 trials preserved.
- Pinned CuraEngine 4.13.1 study: no-gap and simplified variants have zero definite numerical width violations; local feature coverage and physical compliance remain open.
- Simplified G-code is byte-identical on re-slicing. Optimistic time 181.18 s at artificial 2,000 mm/s, 100,000 mm/s², SCV100 and Q200. Pinned Klipper planner agrees within one microsecond.
- Same-path torque/pulley screen covers Cartesian, CoreXY, crossed gantry and center-linearized delta. No design selected. Direct-drive and Bowden mass/COM options are calculated; preferred 9 mm Bowden allowance totals 140 g.
- No physical testing, purchases, manufacturing release or usable printer.cfg.

## Fusion state

Verified destination: Default Project / Codex Benchy Printer. Last inspected design: Untitled, blank, unsaved, mm/g. No Fusion edits were made in checkpoint 004. No cloud version, F3D, STEP or manufacturing export exists. Refresh the app/window identity before any UI work. Use computer use, never Fusion MCP for this request.

## Exact next operation on resume

1. Read the remote checkpoint-004 manifest and compare local archive SHA256. Verify the extracted validation/file-manifest.json. Remote Git blob identity and full remote download/restore are separate checks; see validation/CHECKPOINT.md.
2. Reassess the unpassed gate using new evidence only. Remaining useful digital work is to audit simplified Cura local shell/combined-infill coverage, or find a substantially different compliant path and demonstrate a major time improvement. Repeating the same capped scenarios does not justify CAD.
3. Any promising path still needs exact <=0.5 mm nozzle/filament flow and extrusion-force evidence, actual motor/driver equivalence, complete delivered quotes and full nonlinear dynamics before architecture selection. Delta-center results cannot be promoted to nominal times. Owned parts cannot inherit BIQU or Pi Zero specifications without identification.
4. Keep detailed CAD withheld if no candidate supports <=55 s nominal with credible sub-60 s uncertainty margin and <=$400 new delivered spending. The requested stop-at-feasibility outcome is documented; do not fabricate downstream deliverables.

## Runtime and reproduction

Bundled Python is under C:/Users/logan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe. Engineering tools use standard Python; figures additionally use matplotlib installed only in this task's work/python-libs. Cura extracted runtime is in work/cura413; its official installer/hash and reproducible runner are documented in slicing/CURA-REPRODUCTION.md. Runtime binaries are excluded from backups. Shared calculation files and immutable original model are in outputs/codex-benchy-printer.

Repository: https://github.com/Logan13603/codex-benchy-printer . Checkpoint 003 parent head: 7d6120393d9c92f2b8c1c5d383e40a4243eb6950. Checkpoint 004 source commit and ZIP/blob identifiers are recorded in the external backup manifest after publication, avoiding a self-referential archive checksum.
