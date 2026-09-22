# Codex Benchy Printer

**Checkpoint 007: budget cap removed; optimize the cheapest credible sub-minute design.** Target: full-size compliant SpeedBoatRace Benchy in 50–55 seconds, then three consecutive physical prints under 60 seconds.

[Open the current feasibility report](engineering/FEASIBILITY.md) · [Design basis](engineering/DESIGN-BASIS-C.md) · [Resume state](RESUME.md)

[New geometry and alternatives study](engineering/GEOMETRY-AND-ALTERNATIVES.md) adds spatial accuracy, yaw/tension dynamics, three thinner-wall slices and independent-head scheduling. No build-ready architecture is selected.

The expanded study calculates **51.75 seconds** at hypothetical 204 g acceleration and 300 mm³/s flow. A pinned Klipper planner reproduces the arithmetic. Hardware capability and physical quality remain unproven; a combined shortfall case takes **70.29 seconds**. The preferred direction is a stationary-XY hotend and a very light XY bed. The detailed mechanism is still being engineered.

Existing Pi, CPAP blower/hose, SD/cord, 9 mm belts/pulleys and some screws remain credited. There is no current validated total price. Earlier $400 caps and conventional-printer cost studies are historical.

| Folder | Contents |
|---|---|
| engineering | Current feasibility, architecture studies, mass/COM, timing, torque, heat and cooling calculations |
| purchasing | Historical candidate pricing and owned-inventory credits; no frozen new BOM |
| slicing | Original mesh, frozen public rules, slicer trials and reproduction tools |
| validation | Planner checks, width audits, primary-source provenance and backup manifests |
| cad / manufacturing | Reserved for the gated Fusion and fabrication deliverables |
| electronics / firmware / assembly | Reserved for selected hardware and released instructions |

Fusion destination: **Default Project / Codex Benchy Printer**. No detailed CAD, wiring release, build firmware, parts purchase or physical result exists. All trial G-code is analysis evidence, not printer-ready output.

Checkpoint 007 preserves the revised study; [backup status](validation/CHECKPOINT.md) distinguishes remote content-identity verification from a full download/restore. Historical checkpoints remain in Git history and backups.
