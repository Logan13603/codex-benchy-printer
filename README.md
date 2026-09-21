# Codex Benchy Printer

**Checkpoint 004: feasibility gate not passed.** Target: a full-size SpeedBoatRace Benchy in 50–55 seconds, with at most **$400 in new delivered spending**, using the owner's existing Pi, CPAP blower/hose, SD/cord, 9 mm belts/pulleys and some screws.

[Open the feasibility report](engineering/FEASIBILITY.md) · [Cost study](purchasing/CANDIDATE-BOM.md) · [Resume state](RESUME.md)

The latest fixed-width trial takes **181.18 seconds** under aggressive, unproven motion/flow assumptions. Its numerical width audit finds no definite violations, but does not certify every local feature or physical print. A pinned Klipper planner independently reproduces the timing arithmetic. The reference parts list remains **$505.40 estimated delivered** after owned-part credits; a cheaper complete system with adequate flow is not established.

No detailed CAD, final wiring, build firmware or manufacturing release exists. This follows the accepted instruction to stop before detailed CAD if performance and budget cannot be supported together. It does not establish universal impossibility.

| Folder | Contents |
|---|---|
| engineering | Feasibility, four-architecture comparison, mass/COM, torque, timing, heat and duct calculations |
| purchasing | Candidate parts, owned-inventory credits, prices and cost assumptions |
| slicing | Unchanged original mesh, rules, profiles, trial G-code and reproducible slicing tools |
| validation | Planner verification, width audits, third-party provenance, checksums and backup status |
| cad / manufacturing | Reserved for gated Fusion and fabrication deliverables |
| electronics / firmware / assembly | Reserved for the selected hardware and released build instructions |

Fusion destination: **Default Project / Codex Benchy Printer**. Last verified design: blank and unsaved. All trial G-code is analysis evidence and must not be sent to a printer. No parts have been purchased.

Checkpoint 004 is a complete local snapshot. Historical checkpoints remain in Git history and `backups/`; see [backup verification](validation/CHECKPOINT.md). Large native CAD archives will use release assets when CAD exists; interim engineering ZIPs are currently stored in the private repository.
