# Purchased flow/control source audit — 2026-09-21

These are research comparisons, not a shopping list or complete delivered-price estimate. No part is selected or purchased here. Owned Pi, CPAP blower/hose, SD/cord,9 mm belts/pulleys and usable screws retain zero acquisition-cost credit; unidentified interfaces and performance cannot be assumed.

| Item / primary source | Evidence and limits | Decision |
|---|---|---|
| [Phaetus Rapido X](https://www.phaetus.com/products/rapido-x) | Store lists $89 before delivery,103 mm³/s maximum,24V120 W,153 g,Ø24×79.2 mm and supplied0.4/0.5 mm nozzles. Inspected text does not establish the material/nozzle/temperature test conditions for103 mm³/s. | Even granting103 as sustained usable flow, the new slice takes at least86.75 s to extrude its volume alone. It cannot support the single-head target. |
| [E3D Volcano support](https://e3d-online.com/pages/e3d-classics-support-volcano-nozzles) | Table lists20 mm³/s for0.4 mm brass withPLA220°C. Its higher-diameter rows do not establish performance through a 0.5 mm outlet. | Useful reference; no basis for a300 mm³/s claim. |
| [Bondtech CHT white paper](https://www.bondtech.se/intranet/white-paper-max-flow-rate/) | Printed-flow tests use0.6,0.8,1.0,1.4 and1.8 mm nozzles with a50 W Copperhead setup. | No tested eligible0.5 mm point in this study. Do not extrapolate its largest-nozzle result. |
| [Slice Magnum+](https://www.sliceengineering.com/products/mosquito-magnum-plus) | Manufacturer advertises up to88 mm³/s PLA and91 mm³/s ABS, expandable100 W,73 g. | Even the favorable flow claim is below the required average. Not selected. |
| [Original Bondtech LGX guide](https://www.bondtech.se/downloads/QuickStartGuides/bondtech_EXT-LGX_LGX-Large-Gears-eXtruder_quick-start-guide.pdf) |8 mm motor rotation distance; speed requirement follows from filament speed×60/8. | No torque-speed curve or transient PA proof in this guide. |
| [LGX PRO Metal TDS](https://www.bondtech.se/downloads/TDS/Bondtech_EXT01LGX41036.pdf) | SKU EXT01LGX41036,300 g,7.785 mm rotation distance; push-force statement7–10 kg is not a torque-speed/acceleration curve. | Do not substitute this product for the original LGX geometry, mass or gearing. |

The revised slice contains 8935.39 mm³, needing at least 162.46 mm³/s averaged across a 55-second print, including travel. A300 mm³/s working cap remains an unvalidated requirement from the timing study, not an available purchased-hotend specification.

## Control and cable evidence

The [Analog Devices TMC4671](https://www.analog.com/en/products/tmc4671.html) supports closed-loop control of two-phase steppers, but the IC alone is not a motor power stage or complete driver. Its electrical control rate is not mechanical tracking bandwidth.

The [community Klipper driver](https://github.com/andrewmcgr/tmc-4671) identifies itself as beta and lightly tested. Its README lists OpenFFBoard and Ouroboros options for steppers, while the TMC4671+TMC6100-BOB supports brushed/brushless motors rather than two-phase steppers. It requires encoder/loop setup and braking provision. This makes closed-loop tracking a research option; it does not add motor torque or prove high-acceleration accuracy. No board, firmware revision or pinout is frozen.

A [winch-geometry discussion involving the Minuteman builder and Klipper maintainer](https://klipper.discourse.group/t/winch-kinematiks-missmatch/23834) identifies pulley-wrap geometry as a possible source of nonlinear position error. The [cable-flex compensation developer discussion](https://klipper.discourse.group/t/flex-compensation-for-winch-kinematics/25031) reports simulation work and explicitly lacks physical testing at that stage. Neither substitutes for a validated mechanism here. A constant point-anchor model misses real spool/tangent changes.

## Material identity

The [original FormFutura Volcano PLA TDS](https://www.formfutura.com/web/content/256653?download=true) specifies density 1.27 g/cm³. That would make this slice11.348 g, compared with 11.080 g under the historical generic1.24 assumption. The old generic calculations remain labeled. Melt-flow-index conditions and annealed heat resistance do not establish transient0.5 mm-nozzle flow or immediate cooling of a fresh layer. Newer Volcano PLA150C is a separate product; no filament SKU is frozen.
