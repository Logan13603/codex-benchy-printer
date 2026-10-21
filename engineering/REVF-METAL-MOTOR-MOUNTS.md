# RevF metal motor mounts — development revision, 2026-10-21

The previous printed motor hangers are replaced by modular aluminum bars and two-dimensional sheet profiles. This removes printed material from the motor load path and permits ordinary straight drilling/tapping. It does **not** establish assembled stiffness, fatigue life, joint slip resistance, or a validated sub-minute print.

## Frozen interfaces and parts

All coordinates are world millimeters. Motor face Z is 24.5 below its belt plane. Motor shaft, pulley centers, belt planes, 31 mm motor screw patterns and the four M4 motor-plate anchors are unchanged.

| Station | Motor X,Y | Motor face Z | Belt Z | Frame slot Y |
|---|---|---:|---:|---:|
| A1 rear | -88.75, 95 | 257.8 | 282.3 | 130 |
| A2 front | 88.75, -105 | 257.8 | 282.3 | -130 |
| B1 rear | 88.75, 95 | 244.8 | 269.3 | 130 |
| B2 front | -88.75, -105 | 244.8 | 269.3 | -130 |

Per station, `CBP-D401_*_MOTOR_PLATE_*` is a 6061-T6 plate 45 × 64 × 6 with R2 XY corners. Six `CBP-D402_<axis>_<station>_*` parts complete the hanger: one top bar, two foot bars, two cheeks, one cable-tie tab. The shared numerical feature specification is `cad/revf/motor_mount_dimensions.py`; it drives both CQ and native Fusion builders.

- **Top bar:** 42 × 20 × 8, Z272…280, centered on the frame slot. M5 clearance holes diameter5.5 at motor X±6 and frame-slot Y. The revised positions clear the front M4 heads. Two side M3 taps per end at slot Y±5, Z276.
- **Foot bars:** 42 × 14.3 × 6, Zface−6…face. Their Y bounds relative to the motor are +21.7…+36 and −36…−21.7. M4 through-tap centers are X±17, Y±27. End M3 axes are at Y±32, Zface−3. Front mounts have diameter6 vertical Allen access holes at motor X±6, world Y−130.
- **Cheeks:** 6061-T6 sheet4; local X bounds ±21…±25. Outer Y bounds are the union of motor Y±36 and slot Y±10. Bottom Zface−56.5, top280. The motor window is 49 × 52 with R3 corners; the plate/head window is 64.2 × 12.1 with R0.5 corners. A 5 mm lower U bridge preserves a connected path around the motor. The outer rail step and front-inner return-idler step are intentional profile cuts. Each cheek is one valid solid.
- **Cable tab:** 30 × 25 × 1.5 flat aluminum sheet, outside the frame-side foot bar. Two M3 holes and four 2 × 5 tie slots; no structural print. All cable-contact edges require deburring and protection. Motor connector position, pigtail exit and actual bend radius remain a hold.

The 24 new hanger customs total **400.410 g** from nominal aluminum density2.70 g/cm³. Four revised motor plates total **166.557 g**. These are fixed masses. The 06 fixed group, including new mount hardware, is **542.536 g**; moving supports are unchanged by this revision.

## Manufacture and fit

Use saw/drill/tap stock for the bars and laser/waterjet profiles for the cheeks and tabs; a small end mill can finish profiles. The cheeks have no undercuts. R3 applies to the large motor window; the smaller R0.5 plate window requires a suitable profile-cutting process. Do not substitute a 6 mm router cutter at that window without changing the geometry and rechecking its fit. Use the shared numerical specification and individual STEP parts as the coordinate authority.

Drill the bar end M3 pilots diameter2.5 × 9 deep and obtain at least 7 mm of full thread. The M3×10 side bolts engage5.5 mm, leaving at least1.5 mm of full-thread tip allowance. Cable-tab M3 pilots are diameter2.5 × 7 deep, with at least5.5 mm full thread; M3×6 screws engage4 mm. Include drill-tip/runout clearance when preparing the shop operation. Blind pilot bores near the foot end/cable intersections leave a nominal **0.5 mm minimum web** beyond the working threads; verify drilling position and depth with a fixture. This thin runout web is not a validated structural margin.

M4 pilots diameter3.3 pass through the 6 mm foot bars. Deburr the exit; the M4×16 screws project3.2 mm below the bar and require the modeled free space. No M4 captive nut is used.

Machine the motor plate in two setups: locate/drill the through pattern and outer profile, then indicate/fixture the underside for the pilot socket. Finish the motor-bearing face flat within0.05 and parallel to the opposite face within0.05; locate mounting/pilot features within0.05 of a common datum. These are requested manufacturing tolerances, not measured results.

The motor plate has an **8 mm through shaft bore** and an underside **diameter22.10 × 2.15 deep pilot socket**. The drawing proxy has a22 × 2 pilot, giving0.05 radial and0.15 axial nominal clearance. **Final diameter/fit tolerance remains held until the actual motor pilot tolerance is confirmed.** Deburr edges0.2 without rolling material onto bearing faces.

Only A2 needs the opposite-level return-idler pocket: diameter28.5, floorZ263.10, depth0.70 from the upper plate surface. It leaves the complete pilot register intact. The plate/idler clearance is only0.20 nominal and requires an actual purchased-part tolerance stack before release.

## Fastener schedule for all four stations

Dimensions below are nominal. Thread geometry is simplified in CAD, and each intended screw/thread mate is explicitly identified in the part metadata.

| Use | Quantity | Hardware | Nominal engagement / allowance |
|---|---:|---|---|
| Motor to plate | 16 | M3×10 ISO4762 +0.5 washer | 3.5 into ≥4.5 deep maker hole; ≥1.0 bottom margin |
| Motor washers | 14 | OD7, ID3.2, thickness0.5 | ordinary stations |
| A2 inner motor washers | 2 | **OD6**, ID3.2, thickness0.5 | do not substitute OD7; it clashes with B return flange |
| Cheeks to top/foot bars | 32 | M3×10 ISO4762 +OD7/ID3.2/0.5 washer | 5.5 into ≥7 full thread |
| Plate to foot bars | 16 | M4×16 ISO4762 +OD9/ID4.3/0.8 washer | all6 of bar; tip projects3.2 |
| Top bars to frame | 8 | M5×14 ISO4762 +OD10/ID5.3/1 washer | 5 into slot; about3.8 nominal T-nut thread engagement |
| Frame nuts | 8 | HNTT5-5 drawing proxy | preinsert; exact slot/nut compatibility held |
| Cable tabs | 8 | M3×6 ISO4762 +OD7/ID3.2/0.5 washer | 4 into ≥5.5 full thread |

Motor M3×8 is not an equivalent substitute: it would give only1.5 mm engagement through the6 mm plate and0.5 washer. Check fastener grade, actual washer dimensions and bottom clearance before assembly. Tightening torque/preload is not yet validated; use the actual fastener/material supplier guidance and verify resistance to joint slip.

## Assembly and service order

1. Deburr, clean and gauge the parts. Dry-fit the pilot and verify the actual motor, pulley, T-nut and slot dimensions. Preinsert the frame nuts before closing extrusion ends.
2. Install each top bar to the underside slot with its two M5×14 screws and washers. Tighten these **before installing the rear foot bar and cable tab**. The rear tool path is obstructed after those parts are fitted; this is a documented service limitation.
3. Fit the two cheeks to the top bar with four M3×10 screws and washers. Their upper bar interfaces must seat without forcing the sheet profiles.
4. Assemble the motor, motor plate and foot bars on the bench. Use the two OD6 washers on A2's inner motor screws. Check the six-millimeter tapped M4 grip and motor-screw bottom clearance. Fit the drive pulley to the measured belt plane and verify grub-screw access.
5. Offer the motor/plate/foot-bar subassembly between the cheeks and install four end M3×10 bolts. Their lateral tool axes must be accessible before fitting exterior panels.
6. Install the cable tab and secure a protected pigtail loop without pulling on the motor connector. Actual connector/bend clearance requires the purchased motor. Refit panels only after wrench and wire access is confirmed.
7. Front M5 frame screws can be reached from below using a **4 mm AF Allen key**, whose conservative5 mm shaft envelope passes through the6 mm holes in both plate and foot bar. A generic6.35 mm driver bit does not fit these access holes. Rear M5 service requires removing the cable tab and rear foot bar/associated motor subassembly.

## Focused verification result

`validation/revf-metal-mount-audit.json` records source hashes and the full pair results. It checks new mounts/plates/hardware against source01 frame,03 bed,05 drives,06 supports and07 braces. Intersection threshold is0.01 mm³. The independent analytic review found and prompted correction of the M5/M4 head clash, two motor-washer/idler clashes, inverted T-nut proxies and missing blind-tap allowance.

- All28 revised custom solids are valid and individually connected. Both regenerated assembly exports are valid:05 has64 parts;06 has218 parts.
- New mounts versus all checked geometry have **64 intersections, all exactly declared screw/thread mates**, and no other nominal overlap above threshold.
- Drive-internal checks have16 motor screw/thread mates and10 expected belt/tooth-envelope proxy contacts; no other overlap.
- Full continuous gantry sweep Y−20…+30 has **positive bounding-box separation for every new mount/moving-part pair**; the smallest bound is4.000 mm, right fork versus A2 rear foot bar. X travel does not move these gantry-end parts. This does not certify the separate toolhead travel envelope.
- Exact critical distances: A2 plate/B return0.200000 mm; A2 OD6 motor washers/B return0.433753 mm; motor screw head/belt0.600844 mm; front inner cheeks/opposite returns1.250000 mm. These are nominal CAD distances, **not tolerance-approved margins**.
- Conservative5 mm front Allen shaft envelopes have no clashes. Both rear Allen paths hit the rear foot bar, cable tab and tab screw; the assembly sequence above is required.

Native Fusion builders are supplied and syntax-checked, but **this report does not claim they have executed**. Parent integration must execute/recompute/audit the native station features and save a new cloud/native checkpoint. The CQ export manifests were rehashed successfully (05:66 listed files;06:226 listed files). Superseded printed hanger STEP/STL files are retained under `exports/gantry_supports/superseded-printed-hangers/` and are absent from the active manifest.

Release remains held for the tight plate/return and washer/return tolerance stack, exact owned pulleys and shaft retention, actual motor/connector dimensions, slot/nut compatibility, joint slip/preload, strength/resonance/thermal testing and the separate toolhead travel issues. This focused mount revision does not validate the printer as production ready.

## Native per-station entry points

Load `common.py`, the tested04 helper definitions, `05_drives.py`, then `06_gantry_supports.py`. Use one station per Fusion operation:

```python
build_native_drive_station('A', 1, False)       # one motor plate
build_native_motor_station('A', 1, False)       # six metal mount parts
import_native_drive_station_hardware('A', 1)   # separate reference import
import_native_motor_station_hardware('A', 1)   # separate reference import
```

Repeat for A2/B1/B2. The optional third argument controls hardware import; leave it false when splitting transactions. Avoid rerunning a custom builder on existing named components. Hardware import stages safely skip components already present. Native component descriptions identify metal stock and development holds; applied native material/appearance still requires the parent integration pass.
