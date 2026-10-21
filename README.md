# Codex Benchy Printer

**Detailed RevF Bowden CAD is in progress.** Saved native design: **Default Project / Codex Benchy Printer / Codex Benchy Printer RevF AWD CoreXY**. [Current detailed CAD checkpoint](cad/REVF010-STATUS.md) · [Resume instructions](RESUME.md) · [Native archive recovery](cad/backups/RevF-009/RESTORE.md). Newer offline STEP/STL geometry is separate from the last saved native Fusion version; manufacturing release remains pending.

The objective is a full-size compliant SpeedBoatRace Benchy in 50–55 seconds, with three consecutive physical prints under 60 seconds. There is no hard budget cap; the design should still be the cheapest credible path. The user's Pi, CPAP blower/hose, SD/cord, 9 mm belts/pulleys and usable screws are existing inventory.

The latest bridge-aware slice calculates **53.54 seconds** only at unproven 2400 mm/s, 2,000,000 mm/s² and 300 mm³/s limits. A 0.20-second layer floor gives **60.38 seconds**. This is a numerical scenario, not expected physical performance. [Feasibility report](engineering/FEASIBILITY.md) documents the limitations. The user explicitly authorized CAD development before those limits were physically validated.

| Folder | Contents |
|---|---|
| engineering | Architecture, mass, timing, extrusion, torque and heat studies |
| purchasing | Source audit, candidate prices and existing-inventory credits |
| slicing | Original mesh, rules and reproducible analysis slices |
| cad | Parametric Fusion assembly scripts, native archives, STEP checkpoints, CAD status |
| validation | Numerical checks, provenance and backup evidence |
| manufacturing / electronics / firmware / assembly | To be completed before a build release |

The current CAD is a development checkpoint. No purchasing release, complete build package, printer-ready G-code or physical validation is claimed.
