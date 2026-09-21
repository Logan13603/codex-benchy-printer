# Sources and evidence — 2026-09-20

Current evidence is summarized below. Older source interpretations remain in Git history; this file replaces stale pending/incorrect labels.

| Evidence | Primary source | What it supports / limitation |
|---|---|---|
| Original mesh | https://github.com/CreativeTools/3DBenchy at b542785f9642ab39db8a778a0ccc934b3ebd829a | Unchanged single-part mesh; checksum in slicing/provenance.json |
| Model license | https://www.3dbenchy.com/license/ | Current CC0 statement; preserve CreativeTools/Daniel Noree attribution |
| Public rules | https://www.youtube.com/watch?v=7zkKcFtLAks | Annex publisher description; paraphrased in RULES.md. Latest Discord amendments unverified |
| LDO motor drawing | https://cdn.shopify.com/s/files/1/0239/9287/files/LDO-42STH48-2504AC_RevA.pdf?v=1643851583 | Inspected: 84.5 g cm² rotor inertia; 350 g reference mass; mounting dimensions |
| Running torque | https://cdn.shopify.com/s/files/1/0239/9287/files/LDO-42STH48-2504AC_Torque_Curve.pdf?v=1645112191 | 24 V, 2.5 A, full step; no extrapolation above 2100 RPM or transfer to another drive condition |
| Motor prices | https://www.filastruder.com/products/ldo-stepper-motors-nema-17 | Exact variant price snapshots in purchasing/source-price-snapshot.json |
| Rapido 2 price | https://www.phaetus.com/products/rapido2 | UHF Black variant $99 snapshot; not small-nozzle flow evidence |
| Original Rapido test | https://trianglelab.net/u_file/2111/01/file/Rapidohot-endMaximumPracticalFlowRateTest-5d73.pdf | PETG, 265°C, 0.8/1.2 mm nozzles; different hardware/conditions from target |
| CPAP reference | https://global.bttwiki.com/Universal%20Turbo%20Kit.html | Reference only; owner's blower is not identified. Free-air and static endpoints differ |
| CPAP manual | https://ae01.alicdn.com/kf/Sb960b719f4e440b5ab5695711f920f235.pdf | WS7040-24-V200 / WS2403DY01V04 data; not an installed hose/duct test |
| Controller price | https://biqu.equipment/products/btt-skr-pico-v1-0 | $39.85 variant snapshot; thermal/current equivalence remains open |
| Budget hotend | https://trianglelab.net/products/trianglelab-chcb-ot-hotend-updated-kit-k1-hotend-for-sprite-extruder-creality-k1-3d-printer-creality-k1-max-cr-m4-printer | Displayed $25.18 initial option, nominal 67 W; no target-flow qualification or standalone BOM |
| PSU price investigation | https://www.digikey.com/en/products/detail/mean-well-usa-inc/LRS-350-24/7705034 | No usable current quantity-one price retrieved; retain allowance |
| OrcaSlicer | https://github.com/OrcaSlicer/OrcaSlicer/tree/v2.3.2 | Pinned trial version; variable gap/thin-feature width explains audit failures |
| Cura release | https://github.com/Ultimaker/Cura/releases/tag/4.13.1 | Signed official Windows release, hashes and LGPL definitions archived; runtime not redistributed |
| Klipper planner | https://github.com/Klipper3d/klipper/blob/ce7002bedf37e938bb483572949f3703ac6476cb/klippy/toolhead.py | Unmodified source/classes used in numerical comparison; GPL license archived |
| Tuning procedure basis | https://www.klipper3d.org/Resonance_Compensation.html and https://www.klipper3d.org/Pressure_Advance.html | Measurements required; no validated frequencies/PA/PID values claimed |

The earlier JdVZZ4i2dS8 link is a Josh Murrah printer run, not the Annex announcement. No architecture, delivered purchasing cart, thermal performance or physical firmware configuration has passed release acceptance.
