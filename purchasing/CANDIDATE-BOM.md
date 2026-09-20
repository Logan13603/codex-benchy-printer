# Candidate cost and mass study � revision A

This is an estimate for the independent-axis, short-Bowden reference. It does not meet the cost/performance gate and is not a shopping list for a released machine. Prices are USD on 2026-09-20; no orders placed.

| Part | Candidate / scope | Qty | Unit $ | Extended $ | Unit installed g | Evidence |
|---|---|---:|---:|---:|---:|---|
| CBP-P101 | LDO-42STH48-2504AC XY motors | 2 | 17.99 | 35.98 | 350.0 | Sourced variant 39580977791047; manufacturer 350 g reference |
| CBP-P102 | LDO-42STH25-1404MAC E/Z motors | 2 | 16.99 | 33.98 | 150.0 | Sourced variant 17240374935623; mass estimate, E/Z suitability unverified |
| CBP-P103 | Phaetus Rapido 2 UHF Black | 1 | 99.00 | 99.00 | 44.5 | Sourced variant 45177211191573; installed mass estimate |
| CBP-P104 | BIQU Universal Turbo Kit SKU1060000677 | 1 | 69.99 | 69.99 | 185.0 | Sourced variant 41311385157730; installed kit mass estimate |
| CBP-P105 | BIQU fan pipe SKU3020030069 | 1 | 14.66 | 14.66 | 100.0 | Sourced variant 41311385190498; trim length and installed mass estimate |
| CBP-P106 | BTT SKR Pico V1.0 SKU1060000513 | 1 | 39.85 | 39.85 | 70.0 | Sourced variant 40565262155874; mass estimate |
| CBP-P107 | Raspberry Pi Zero 2 W | 1 | 15.00 | 15.00 | 11.0 | Manufacturer advertised price; US reseller stock/cart pending |
| CBP-P108 | Host microSD, USB data cable, 24V-to-5V regulator | 1 | 14.00 | 14.00 | 30.0 | Allowance; search 32GB high endurance microSD, USB OTG, regulated 5V 3A buck |
| CBP-P109 | Mean Well LRS-350-24 PSU candidate | 1 | 35.00 | 35.00 | 900.0 | Allowance; exact supply seller/revision not quoted |
| CBP-P110 | MGN7H 150mm rail with carriage | 3 | 12.00 | 36.00 | 110.0 | Allowance; generic supplier, preload and accuracy unverified |
| CBP-P111 | 2GT 6mm belts, two 20T 5mm-bore pulleys, idlers | 1 | 18.00 | 18.00 | 50.0 | Allowance; 1m belt; final lengths and tooth engagement not frozen |
| CBP-P112 | Remote dual-drive geared extruder mechanism | 1 | 14.00 | 14.00 | 50.0 | Allowance; search BMG dual drive gear kit; housing printed; no motor included |
| CBP-P113 | Small 24V bed heater and thermistor | 1 | 12.00 | 12.00 | 12.0 | Allowance; search 60x40 silicone heater 20-30W NTC100K |
| CBP-P114 | 75x45x1.5mm aluminum bed material | 1 | 6.00 | 6.00 | 13.7 | Allowance for stock and waste; installed volume*rho=13.669g |
| CBP-P115 | Adhesive build surface film | 1 | 6.00 | 6.00 | 5.0 | Allowance; no magnetic sheet |
| CBP-P116 | Short T8 lead screw, nut and coupler | 1 | 8.00 | 8.00 | 100.0 | Allowance; hand cut; exact lead and usable stroke unfrozen |
| CBP-P117 | Short aluminum frame profiles, base and gusset material | 1 | 32.00 | 32.00 | 700.0 | Allowance; envelope study only, stock/cutting waste included in cost |
| CBP-P118 | M2/M3/M5 fasteners, washers, inserts, feet | 1 | 18.00 | 18.00 | 100.0 | Allowance; final fastener schedule unavailable before CAD |
| CBP-P119 | Printed-part filament and fabrication waste | 1 | 12.00 | 12.00 | 150.0 | Allowance; custom bracket, duct, tensioner and enclosure material; installed mass excludes waste |
| CBP-P120 | Compatible 0.5mm brass nozzle | 1 | 10.00 | 10.00 | 0.0 | Allowance; replaces nozzle included in hotend mass; exact thread must be frozen |
| CBP-P121 | Heat sink fan and electronics fan | 1 | 7.00 | 7.00 | 35.0 | Allowance; 24V 2510 and 4010 search terms |
| CBP-P122 | AC cord, fused switch, ground leads, DC wire/connectors, strain relief | 1 | 24.00 | 24.00 | 180.0 | Allowance; final protection/wire schedule not released |
| CBP-P123 | Three mechanical endstops and accelerometer module | 1 | 8.00 | 8.00 | 15.0 | Allowance; search microswitch endstop and ADXL345 |

Parts/materials: **$568.46**. Shipping allowance: **$25.00**. Estimated tax (8.5%, including shipping): **$50.44**. Total: **$643.90**, exceeding $500 by **$143.90**.
Installed machine mass estimate: **4.08 kg**, excluding spool, filament inventory and discarded stock. Practical uncertainty at least +/-25% before CAD. The 136 g toolhead and 89.7 g moving bed are subsets, not additional masses.

The sourced prices are recorded in [source-price-snapshot.json](source-price-snapshot.json). Product links: [LDO motors](https://www.filastruder.com/products/ldo-stepper-motors-nema-17), [Rapido 2](https://www.phaetus.com/products/rapido2), [CPAP and hose](https://biqu.equipment/products/universal-turbo-kit), [SKR Pico](https://biqu.equipment/products/btt-skr-pico-v1-0), [Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/). Variant prices came from the stores' public product data, not the default variant display. Shopify shipping weights were deliberately excluded from mass calculations.

Cost sensitivity: $0 shipping and 0% tax still leaves the listed reference above $500. Substituting a $35 hotend for the $99 UHF saves $64 before tax but adds an unvalidated thermal interface and flow capability. The BTT Pi V1.2.1 alternative is $65.99, adding $50.99 before tax relative to the advertised Pi Zero 2 W. Bulk bundles, bare CPAP components, lower-cost mechanics and a different host could reduce cost; none establishes a 55-second machine without measurements.
