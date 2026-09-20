# Codex Benchy Printer

Purpose-built FDM printer study: 50–55-second full-size SpeedBoatRace Benchy, maximum $500 delivered in the continental US.

**Status: feasibility investigation; not a released or validated printer design.** Detailed Fusion CAD is conditional on passing the engineering gate. No hardware purchases are authorized or necessary for this digital investigation.

## Requirements

- Original unscaled Benchy; documented SpeedBoatRace settings.
- Budget includes printer, external CPAP blower and hose, host, electrical hardware, custom-part materials, tax and shipping. Existing FDM printer, hand tools and labor excluded.
- Manufacture with FDM and hand tools, or cost essential outsourced work explicitly.
- Fusion location: `Default Project / Codex Benchy Printer`; use native computer interaction, not Fusion MCP.
- Stop before detailed CAD if 55-second nominal performance with credible sub-60-second margin is not supported within budget.

## Organization

| Directory | Purpose |
|---|---|
| engineering | Reproducible calculations, architecture decision, assumptions |
| purchasing | Candidate BOM, current sources, cost and mass estimates |
| slicing | Original model provenance, pinned profiles and toolpath evidence |
| validation | Tests, results, source register, backup manifests |
| cad | Native Fusion archives and assembly exports after gate passes |
| manufacturing | Released printable files and drawings after gate passes |
| electronics | Wiring and pin assignments after parts are frozen |
| firmware | Configuration after hardware selection |
| assembly | Assembly and commissioning instructions after design release |

Start with [RESUME.md](RESUME.md). Candidate specifications are not manufacturing instructions. Calculated, manufacturer-claimed, simulated, and measured evidence must remain distinguishable.
