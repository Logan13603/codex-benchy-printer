# RevF010 detailed CAD checkpoint — 2026-10-20

**Development assembly, not a manufacturing release.** Mandatory short Bowden, fixed Sherpa Micro, external CPAP, 9 mm belts, compact AWD CoreXY. No hard budget cap. Full-size Benchy performance remains unvalidated.

The native Fusion design is **Codex Benchy Printer RevF AWD CoreXY**, in Default Project / Codex Benchy Printer. Last verified native cloud checkpoint was version5 on2026-09-30, with frame, rail/gantry and vendor hotend/fixed extruder. Native009 F3D and STEP are preserved in `cad/native/`; recoverable GitHub copies are under `cad/backups/RevF-009/`. They precede the newer detailed geometry below.

On2026-10-20 Fusion was launched successfully, but Windows showed the lock screen. No further Windows input was sent. New parts were therefore built and exported with an independent solid-CAD kernel. They are real STEP/STL solids, with editable source builders; they have **not** yet been run in Fusion's native feature history. Do not describe offline exports as a newer native cloud version.

## Current geometry

- Extrusion frame:280×280×300 nominal,2020 posts/caps and2040 upper Y supports; accurate simplified slot interfaces and drilled connections. Catalog extrusion masses override simplified volumes.
- Side-supported Z: two additional guide posts,200mmMGN9H rails, adapters, bed fork/yoke,100×100×4 aluminum plate, provisional magnetic/spring-steel stack, three-point silicone leveling, motor riser, Tr8×8 drive envelope, floating-nut cassette and hardware.138 valid instances passed seven hardware-inclusive Z poses. Exact nut/pilot/surface interfaces remain held.
- Bowden toolhead: maker Goliath solid, carriage spine, aluminum platform, metal fitting, separate2510 cold-side fan/shroud, hollow CPAP branches, split printable shells, nuts/bolts and harness support. Exact current counts/mass are in generated component ledgers. Hotend80g/fan8g/coupler5g remain estimates.
- AWD drive: four maker-dimensioned LDO42STH48-2804AC(S35) proxies,35mmshaft/31mmmountholes;2GT36T9mmpulley assumption, idlers/bearings, slotted45×64×6 motor plates and hanging supports. Operating torque/current and pulley SKU are not frozen.
- Two817.08mm nominal belt pitch paths are length-invariant over the studied workspace. Their derivatives are qA=x−y and qB=−x−y; firmware assignment/direction must follow this actual routing. Belt planes269.3/282.3 and mean forceY−35 closely approach the current estimated head center of mass.
- Beam revision: closed158mm carbon tube,140mmXrail, separate beam clamps and metal portal bridges above the returns. A proposed transverse carbon-port option was rejected because it interrupted the closed torsion cell. Latest support/return clearances require the recorded whole-assembly audit.
- Usable travel is **80×60×60**, reducing Y from80 to retain about10mm front-fan screw clearance. The full-size Benchy fits.

## Files and reproducibility

`cad/revf/assemble_rebuild.py` builds the combined offline assembly, mass ledger, source hashes and preview. Individual modules export component STEP and printed STL. Use CadQuery2.6.1; the local environment is `work/cad-runtime` outside the repository package. `cad/revf/common.py` plus numbered native builders retain the intended Fusion sketch/feature implementation. Native03/04 and later builders remain unexecuted.

The combined outputs are in `cad/revf/exports/checkpoint010/`; module outputs are in `exports/bed_z`, `exports/frame_xy`, `exports/drives`, `exports/gantry_supports` and `generated/toolhead`. Export files can lag source during a checkpoint; compare `builder-hashes.json` before treating them as matching.

## Required next work

1. Unlock desktop, open the saved native RevF design, and verify009 against its manifest before applying newer builders. Preserve009 and all earlier versions.
2. Regenerate the combined offline exports after all builders are frozen; classify every overlap, including screw heads/driver access. A zero-volume screen does not prove a useful clearance.
3. Complete/verify motor hangers, return-idler retention, portal fasteners, frame-extruder mount, Bowden/CPAP sweeps, wiring/endstops, feet, shear panels and electrical packaging. Do not release placeholder purchased interfaces.
4. Transfer the detailed parts into Fusion with named components, driving constraints and intentional joints; recompute, sweep travel and reconcile actual mass/COM. Native assembly occurrence placement is not yet fully expression-driven.
5. Freeze exact bought interfaces and torque-speed/flow/cooling evidence; finish BOM, drawings, tolerances, fabrication access, electronics/firmware/slicer package and commissioning. No under60second print has been physically demonstrated.

Check usage before work and near each milestone. Start saving by15% remaining, aim to stop near1%, and never redeem reset credits without a new explicit request.
