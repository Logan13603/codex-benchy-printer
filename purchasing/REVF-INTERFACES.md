# RevF purchased-component interfaces

Research date: 2026-09-30. Units are mm, g, N, and USD unless shown otherwise. This register separates manufacturer dimensions from CAD simplifications and unresolved purchase choices. It is not a manufacturing release: imported hotend/extruder mounting measurements, actual owned belt/pulley/hose specifications, motor torque at speed, and the final bed/heater are still required.

## 1. Frame: MISUMI HFS5 rather than an unspecified 2020 profile

Use the exact **HFS5-2020** and **HFS5-2040** family. Profiles from other suppliers can share the outside dimensions while having different slot cavities, mass, and stiffness. The official [MISUMI section drawing and properties](https://jp.misumi-ec.com/pdf/fa/2011/p2_0513.pdf), printed pages 2-513/2-514, documents:

| Property | HFS5-2020 | HFS5-2040 |
|---|---:|---:|
| Outside section | 20 × 20 | 20 × 40 |
| Slot mouth | 6 | 6 |
| Maximum buried cavity width | 12 | 12 |
| Lip thickness | 2 | 2 |
| Nominal slot depth from outside face | 6 | 6 |
| Center bores | one Ø4.2 | two Ø4.2, 20 apart |
| Exterior corners | 4 × R1 | 4 × R1 |
| Cross-sectional area | 183 mm² | 324 mm² |
| Linear mass | 0.50 kg/m | 0.88 kg/m |
| Second moment, weak / strong | 7420 / 7420 mm⁴ | 13580 / 51300 mm⁴ |
| Material | A6N01SS-T5 | A6N01SS-T5 |
| Finish | clear anodize | clear anodize |

The HFS5 slot is **not a rectangular 12 × 4 cavity**. That approximation intersects adjacent slots and disconnects the profile's corner bodies. A useful simplified 2020 section places the origin at its center, outside faces at ±10, and the top slot void at nominal vertices:

`(-3,10), (-3,8), (-6,8), (-6,7), (-3,4), (3,4), (6,7), (6,8), (3,8), (3,10)`.

Rotate this polygon for the other faces. The 45° flanks preserve the diagonal connecting webs. The illustrated slot-root notch is 0.3 deep with a 120° included angle; a simplified V uses `(-0.519615,4), (0,3.7), (0.519615,4)`. These coordinates reconstruct the nominal drawing and omit small unspecified radii. They are a purchased-component proxy, **not extrusion manufacturing geometry**. Use the published linear mass and section moments for engineering; do not infer true mass or stiffness from this simplified solid. A single-solid outer envelope with 6 mm slot mouths and the center bore is also acceptable if explicitly labeled simplified. Use the vendor's actual extrusion for a physical frame.

The 2040 has one slot on each narrow face and two on each wide face, on 20 mm centers. Do not create two independent 2020 solids: the actual 2040 contains connecting webs. Its 0.88 kg/m published mass must override proxy mass.

Catalog cut-length tolerance is ±0.5. Specify deburred, square ends and verify lengths/diagonals before tightening. The center Ø4.2 bores can accommodate M5 end tapping; thread depth and end machining remain a fabrication callout. Use compatible 5-series nuts and M5 hardware. Historical yen prices in this 2011 catalog are not current purchasing prices.

## 2. Motion rails: HIWIN MGN miniature series

Use one catalog revision consistently: [HIWIN Linear Guideway Catalog](https://www.hiwin.com/wp-content/uploads/HIWIN-Linear-Guideway-Catalog.pdf), document G99TE24-2410, miniature guide table around page 88. Older MGN9H drawings differ slightly in block length.

| Interface | MGN9H | MGN12H |
|---|---:|---:|
| Rail width × height | 9 × 6.5 | 12 × 8 |
| Complete assembly height | 10 | 13 |
| Block width × nominal length | 20 × 39.9 | 27 × 45.4 |
| Maximum block length envelope | 40.9 | 45.8 |
| Block mounting | 4 × M3, depth 3 | 4 × M3, depth 3.5 |
| Block hole rectangle | 15 × 16 | 20 × 20 |
| Block mass | 26 | 54 |
| Rail linear mass | 380 g/m | 650 g/m |
| Rail hole pitch | 20 | 25 |
| Rail through hole / counterbore | Ø3.5 / Ø6 | Ø3.5 / Ø6 |
| Counterbore depth | 3.5 | 4.5 |
| Standard catalog end margin | 7.5 | 10 |

Specify rail end margins explicitly. A symmetric 250 mm MGN9 rail can use 12 holes with **15 mm end margins**: `15 + 11×20 + 15 = 250`. A symmetric 250 mm MGN12 rail can use 10 holes with **12.5 mm end margins**: `12.5 + 9×25 + 12.5 = 250`. These are custom order configurations, not guaranteed holes on an arbitrary marketplace 250 mm rail. Standard catalog margins instead suit a 255 mm MGN9 rail or a 245 mm MGN12 rail at those hole counts. Mounting drawings must match the purchased rail.

Choose genuine dimensions for the final BOM; generic rail accuracy, preload, and seal friction are unverified. Rail reference masses at 250 mm are 95 g for MGN9 and 162.5 g for MGN12. Block travel is constrained by its entire envelope, not just the hole spacing.

## 3. Toolhead purchased CAD and cold-side cooling

The official source assemblies have been downloaded locally and hashed. The file manifest also appears in `cad/REVF-INTERFACE-DATA.json`.

| Assembly | Local CAD | SHA256 |
|---|---|---|
| Goliath AIR mockup | `cad/vendor/Goliath_Mockup_AIR.STEP` | `5270113e67481bc8d14c25a5fa2b333afa3352342089f6acbc58c47f0662d347` |
| Sherpa Micro standard release 2, rev1 | `cad/vendor/sherpa_micro_release_2_rev1.STEP` | `8bea49f21001018af1484ccb95ded22dddecb829721a9c0dc1b7635743d4666e` |

Sources: [VzBoT Goliath CAD](https://github.com/VzBoT3D/Goliath/tree/main/CAD), [Annex Sherpa Micro CAD](https://github.com/Annex-Engineering/Sherpa_Micro-Extruder/tree/main/CAD). Source-file Git blob identities and exact download URLs are recorded in the JSON. Goliath is CC BY-NC 4.0; Sherpa uses the Annex Engineering license linked in its repository. Preserve attribution and inspect their respective license before distributing source models.

Import these files as reference purchased components and measure their mounting interfaces, nozzle datum, filament path, envelopes, and clearances in Fusion. Do not invent mounting-hole coordinates or infer actual weight from mockup material assignments. Mounting dimensions and independently verified assembly mass remain unset until measured from the imported model/manufacturer drawing and reconciled with the actual purchased hardware.

The [Goliath manufacturer/design repository](https://github.com/VzBoT3D/Goliath) and [assembly guide](https://docs.vzbot.org/goliath/assembly) establish an AIR cold-side shroud with 2010 or 2510 fan; the assembly guide recommends Delta 2510. This separate hotend fan is necessary regardless of part-cooling CPAP flow. The exact Delta part number, electrical current, and mass are not frozen. The hotend uses a V6-family M6 nozzle, a PT1000 sensor in an M3 brass holder, and a silicone sock rated to 300°C. The exposed nichrome heater region can become very hot; provide separation from plastic ducts, sensor wires, hose, and other wiring, and preserve heater-lead strain relief. Current official sources reviewed did not substantiate an exact assembly weight, heater wattage, or a reliable PLA flow at the intended temperature/nozzle. Reseller claims are not validated performance measurements.

The [Sherpa Micro official release](https://github.com/Annex-Engineering/Sherpa_Micro-Extruder) supports 50:10 or 50:8 gearing using a pinion-equipped compact stepper. Use standard release 2; the project's fixed alpha variant is expressly not recommended for production. The [LDO 36STH20-1004AHG](https://ldomotion.com/products/ldo36sth201004ahgvrn) candidate has a 10-tooth module-0.5, 20° pinion; its reference motor mass is 85 g, rotor inertia 16 g·cm², resistance 2.1 Ω, inductance 1.6 mH, rated current 1 A, and holding torque 100 mN·m. Manufacturer-store listing was $20.99 before shipping/tax. Do not buy the plain non-geared AH version for this interface. Extruder force and stepper torque at the required filament-feed rate still require measurement.

The user owns a CPAP blower and hose. Actual hose inside/outside diameter, cuff geometry, bend radius, supported mass, and blower pressure-flow curve remain unknown. Keep these as explicit interface parameters; do not release a friction-fit inlet sized from an assumed nominal hose. Place a supported hose junction on the moving gantry or overhead strain-relief so the toolhead receives a short compliant branch. A duct design is not thermally validated merely because it fits the STEP model.

## 4. XY drives and 9 mm belts

Low-inductance motor candidate: [LDO 42STH48-2804AC(S35)](https://ldomotion.com/products/ldo42sth482804acs35). Published reference motor mass is 350 g, rotor inertia 84.5 g·cm², phase resistance 0.7 Ω, inductance 0.6 mH, and holding torque about 420 mN·m. Manufacturer-store listing was $24.99, excluding shipping/tax. **The manufacturer's product page contains a current inconsistency:** its 1.8 A entry conflicts with its 1.96 V / 0.7 Ω values and the store's 2.8 A rating. Obtain the exact S35 drawing/current specification before setting driver current. Holding torque is not available torque at speed; no verified 48 V torque-speed curve has been frozen. Shaft projection, flats, pilot, and exact mounting-hole thread depths are still to be checked against the specific purchased variant.

Owned belts and pulleys are 9 mm wide, but pitch, reinforcement, tooth form, tooth count, bore, flange spacing, and hub projection are unverified. A planning candidate is genuine 2 mm GT3/2MGT belting with compatible pulleys. [Gates belt identification](https://www.gates.com/content/dam/gates/home/knowledge-center/resource-library/application-specs/gatescorporationbeltidchart.pdf) gives nominal belt thickness 1.52 mm and tooth height 0.76 mm. Do not assume that a generic belt labeled GT2 is dimensionally interchangeable with every Gates pulley.

For a **20-tooth, 2 mm-pitch** pulley, pitch diameter is calculated as `20×2/π = 12.7324 mm`; motor speed is `v / 40 × 60` RPM for direct axis belt speed `v` mm/s. CoreXY motor speeds follow transformed axis velocities and can exceed tool speed. A 10 mm clear belt face is a design allowance for a 9 mm belt, not a verified purchased idler dimension. Actual hub/flange envelopes and bearing dimensions remain unresolved until the inventory or exact sourced parts are measured. Use matching toothed idlers against teeth and smooth idlers against belt backs.

## 5. Z drive and bed

Compact Z candidate: [LDO 42STH25-1004CL200E(VRN)](https://store.ldomotion.com/products/ldo-42sth25-1004cl200e-vrn-nema17-linear-stepper-motor-200mm-tr8x8), manufacturer-store listing $28.99 before shipping/tax. Integrated **200 ±1 mm Tr8×8 screw, 2 mm pitch / four starts**; motor outside 42.3 square × 26 maximum; four M3 mounts on 31 ±0.1 square, thread depth 3 minimum. Reference total motor/screw assembly mass is 150 g. Holding torque 240 mN·m minimum, 1 A, 5.5 Ω, 7 mH, rotor inertia 35 g·cm². The included PEEK anti-backlash nut has two M3 mounts on 12.6 spacing and 18 mm flange width; complete nut thickness, height, and shaft pilot must be verified before releasing its bracket. An 8 mm-lead screw can backdrive, so assess bed descent with disabled motors rather than assuming it self-locks.

The small bed, heater, magnetic stack, screw points, and lead exit have not been frozen to an exact sourced assembly. Model a custom machined plate with separately named heater and surface components; do not assign a heater's manufacturing hole geometry or electrical rating without a selected manufacturer drawing. Z loads must include the entire plate, heater, surface, carriage, nut, wiring, and fasteners.

## 6. Electronics packaging and power interfaces

Candidate controller: **BIGTREETECH Octopus Pro V1.1**, with MCU variant recorded in the final purchase and firmware package. [Official repository](https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-Pro) separates motor power (up to 60 V) from main/bed power (up to 28 V). A nominal 48 V motor supply must not be connected to main or bed terminals. The [official size drawing](https://raw.githubusercontent.com/bigtreetech/BIGTREETECH-OCTOPUS-Pro/master/Hardware/BIGTREETECH%20Octopus%20Pro%20-%20SIZE.pdf) shows a **160 × 100 board** and **150 × 90 mounting-center rectangle**. Hole diameter, PCB thickness, highest connector/driver envelope, and exact weight are not dimensioned there and remain unset. The repository's 3D file is explicitly named beta, so it is not authoritative V1.1 manufacturing geometry.

Candidate driver: [BIGTREETECH TMC5160T Pro V1.0](https://biqu.equipment/collections/motor-driver/products/tmc5160-pro-v1-0), manufacturer-store price $18.99 each, supports up to 56 V. Do not substitute the earlier discontinued TMC5160 Pro or a Plus module without checking pinout, package, and current limits. Board maximum voltage does not supersede driver voltage limits.

[Mean Well LRS-350 datasheet](https://www.meanwell.com/Upload/PDF/LRS-350/LRS-350-SPEC.PDF): LRS-350-48 is **48 V, 7.3 A, 350.4 W**, **215 × 115 × 30**, reference weight **760 g**; selectable 115/230 V AC input. Its mounting-hole positions and terminal clearance must be taken from the drawing before bracket release. The LRS-350-24 is a compatible separate 24 V family member when the finalized heater/bed budget requires it. [LRS-150 datasheet](https://www.meanwell.com/Upload/PDF/LRS-150/LRS-150-SPEC.PDF): LRS-150-24 is **24 V, 6.5 A, 156 W**, **159 × 97 × 30**, reference weight **420 g**; it may be insufficient for a 100 W hotend plus a 100 W bed. Final power selection must include load diversity, blower/fan consumption, electronics, cooling, wiring losses, and margins.

## 7. Release checks that remain

1. Extract Goliath and Sherpa mounting datums from official imported STEP and verify purchased revision matches.
2. Confirm exact motor variant and dynamic torque at required RPM; verify pulley tooth count/bore and all owned belt/hose interfaces.
3. Freeze bed/heater and verify Z nut geometry, motor pilot, all purchased rail end margins, fan, and connector envelopes.
4. Measure or obtain credible component masses, then reconcile complete toolhead COM/inertia including hardware, filament, wires, duct, and supported hose.
5. Quote current delivered prices; the above manufacturer prices are dated component prices, not a complete delivered BOM.
6. Validate duct/hose pressure losses, hotend thermal limits, rail preload, driver thermal behavior, and physical mounting access before claiming production readiness.
