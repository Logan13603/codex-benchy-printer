# Codex Benchy Printer

**Checkpoint 008: improved toolpaths, more complete extrusion checks, no CAD release yet.** Target: the cheapest credible full-size compliant SpeedBoatRace Benchy printer for 50–55-second prints, with three consecutive physical prints under 60 seconds. There is no hard budget cap.

[Open the current feasibility report](engineering/FEASIBILITY.md) · [Latest engineering study](engineering/EXTRUSION-AND-TOOLPATH.md) · [Resume state](RESUME.md)

The latest bridge-aware slice calculates **53.54 seconds** at unproven motion/flow limits. A0.20-second layer floor gives60.38 seconds. The initially faster concentric slice was rejected after finding unsupported roof loops. Full bridge coverage, motor tracking, extrusion response and installed CPAP cooling remain unresolved, so the pre-CAD gate stays in effect.

Existing Pi, CPAP blower/hose, SD/cord,9 mm belts/pulleys and some screws remain credited. No purchased interface or complete delivered-price estimate is frozen. The old $400/$500 budgets and conventional-printer BOMs remain historical.

| Folder | Contents |
|---|---|
| engineering | Feasibility, architecture, mass/COM, path timing, extrusion dynamics, torque and heat studies |
| purchasing | Source audit, historical candidate prices and inventory credits |
| slicing | Original mesh, rules, pinned slicer trials and reproducible settings |
| validation | Numerical checks, source provenance, pre-CAD gate and backup manifests |
| cad / manufacturing | Reserved for gated Fusion assembly and fabrication deliverables |
| electronics / firmware / assembly | Reserved for selected hardware and released instructions |

Fusion destination: Default Project / Codex Benchy Printer. No geometry or cloud save exists. All trial G-code is analysis evidence and is not printer-ready. [Backup verification](validation/CHECKPOINT.md) distinguishes remote content-identity checking from a complete remote download/restore.
