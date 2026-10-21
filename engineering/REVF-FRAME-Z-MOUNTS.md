# RevF frame and Z mechanics — dimensioned development basis

Date: 2026-10-20. Coordinates and dimensions are mm. X right, Y rear, Z up. This document defines buildable custom-part geometry; it is **not a production release**. The nut, heater/surface stack, fastener access in the final XY drive assembly, rail preload, and physical alignment still require verification. Never manufacture the placeholder nut cassette before measuring the supplied nut.

## Architecture and datums

The Bowden toolhead moves in XY. The bed moves only in Z, so the heavier, stiff bed support below does not increase XY moving mass. The first-layer print surface is Z225; the surface descends to Z165 for a 60 mm build height. Bed center is (0,−38). Two side guides lie close to the bed center of mass in Y, avoiding a long bed cantilever from rear guides. A single screw behind the bed drives a ribbed center arm. The guide blocks constrain bed rotation; the screw nut must float slightly in XY and must not act as a third rigid guide.

An 80×80 nominal print rectangle is X±40, Y−78…2. Full-size Benchy remains the required test artifact; the reduced area is not permission to scale it. The 100×100 plate occupies X±50, Y−88…12. The clearance screen must include the hotend, ducts, growing print, belt clamps, hose, and wire loops, not just the nozzle point.

## Frame members and primary joining

Keep the established 280×280×300 outside extrusion envelope:

| Part | Quantity | Cut length | Placement |
|---|---:|---:|---|
| HFS5-2020 X caps | 4 | 280 | X−140…140; Y±130; Z centers10/290 |
| HFS5-2020 corner posts | 4 | 260 | X/Y±130; Z20…280 |
| HFS5-2020 lower Y members | 2 | 240 | X±130; Y−120…120; Z center10 |
| HFS5-2040 upper Y members | 2 | 240 | X±130; Y−120…120; Z260…300 |
| **Additional HFS5-2020 Z-guide posts** | **2** | **240** | **X±130; Y−38; Z20…260** |

The additional guide posts weigh 240 g together using the maker's 0.50 kg/m value. They add no XY moving mass. Do not calculate their mass from simplified cross sections.

Corner-post ends receive M5×0.8 threads, at least 12 mm full useful thread, pilot drilled to at least17 mm where a blind tap requires runout. Deburr without rounding the square bearing faces. Fit M5×30 socket screws and 1 mm thick, 10 mm OD washers through the X caps from the outside top/bottom. A Ø5.5 transverse clearance hole passes through each cap at X±130, Y±130. **No head counterbore:** the washer must bridge the 6 mm slot mouth on intact outer lands. Nominal engagement is9 mm: `30−20−1=9`. Top screw heads stand above the extrusion envelope; allow6.5 mm clearance. Do not promise a completely flush300 mm outside height.

The lower screw heads also extend approximately6 mm below the extrusion base. Provide at least12 mm firm feet/stands, with screw access holes or removable feet. A bottom electronics panel cannot occupy these head volumes.

The new Z-posts similarly receive M5 end taps. Through the bottom Y member, use M5×30+1 mm washer at (X±130,Y−38), giving9 mm engagement. Through the upper2040, use M5×50+1 mm washer, giving9 mm engagement: `50−40−1=9`. These holes run vertically through the extrusion; they do not cut a blind threaded bore in the upper Y beam. Drill in a supported jig so a hand drill cannot follow the internal cavity off axis. Rail-adapter screws at Y0/±100 do not share the Y−38 station; the Z-post anchor shaft at X±130 does not enter the inner-side rail mounting plates at X±116…120.

**Do not combine the original HCJ5 end-joint proposal with these through-cap bolts.** An upper Y-beam anchor at Z270 intersects the upper15 mm of a corner-post end tap. Moving it to Z290 avoids the post but crosses the vertical cap screw in the cap. Lower Y anchors at Z10 likewise cross the lower vertical cap screw. Use separate external brackets/shear panels for Y-member retention. Primary maker information for compatible joints is the [MISUMI blind-joint drawing](https://us.misumi-ec.com/pdf/fa/2019/2019_US_2844.pdf); this is an interference conclusion from the assembly coordinates, not a vendor restriction.

For the first build, use metal brackets at each Y-member end, with the exact purchased bracket CAD checked before drilling. Printed gussets below assist assembly and protect panels; they are not the sole structural connection at record acceleration. The [MISUMI HBLFSN5 page](https://uk.misumi-ec.com/vona2/detail/110300437260/?HissuCode=HBLFSN5) identifies the compatible5-series bracket and M5 hardware. Its allowable-load number does not validate this whole printer or cyclic joint stiffness.

### Shear panels and printed corner gussets

Do not depend on a freely racking extrusion cube. Add three1.5 mm aluminum panels, drilled by the assembled frame. Rear panel: X−140…140, Z0…300, Y140…141.5. Side panels: Y−140…140, Z0…300, X140…141.5 and−141.5…−140. Leave the front open for bed access. Deburr all sheet edges and fit edge trim near wiring.

Rear-panel Ø5.5 holes: X−90/0/90 at Z10 and290 (6); X±130 at Z50/110/190/250 (8). Side-panel Ø5.5 holes: Y−90/0/90 at Z10/270/290 (9); Y±130 at Z60/130/210 (6), total15 per side. Holes coincide with the corresponding external extrusion slot lines. Use M5×8 with1 mm washers: `8−1.5−1=5.5 mm` projection into the slot; use matching5-series M5 T nuts. Verify a sample nut depth before ordering all screws. Panel stock total area0.252 m² and mass approximately1.02 kg at2.70 g/cm³. Static panel mass does not penalize XY acceleration.

Printed external gusset **CBP-F120**, qty8, is a flat right triangle in its panel plane, legs70, thickness8, external corner R3. It occupies each side-panel front/rear top/bottom corner and sits outside the panel. Local coordinates measured inward from the outside frame corner: triangle vertices(0,0),(70,0),(0,70); four Ø5.5 holes at(10,30),(10,55),(30,10),(55,10). These holes land on the adjacent extrusion slot centerlines10 mm in from each outer boundary. Add 12 mm OD washer lands and optional removable slot-locating tabs5.7 wide×0.8 high. The two holes at55 are gusset fasteners; the panel hole schedule above must be supplemented where needed. Gussets must not replace metal Y-end brackets until assembled-joint stiffness is measured.

For each gusset, use four M5×16+1 mm washers through8 mm print and1.5 mm sheet: projection5.5 mm. For these four stations remove/replace the panel's ordinary M5×8 screws if a station overlaps. Do not stack two bolts in the same T-slot location. Use solid perimeters around the holes and print the broad face flat. PA-CF/ASA or equivalent heat-resistant structural filament; PETG creep at a loaded joint is not assumed acceptable. For a final metal brace, the same hole pattern can be cut in3 mm aluminum and use M5×10+1 mm washers (projection4.5 mm). Aluminum compression sleeves for printed gussets may be added, but their actual measured length must equal the print thickness; an oversize sleeve leaves the gusset loose, an undersize sleeve does not stop creep.

## Side Z guides

Use two MGN9H rails200 long, ordered with10 mm end margins and ten holes on20 mm pitch. Rails are vertical Z45…245, centered Y−38, mounted inward from the guide posts. End margins on marketplace rails must be measured; do not blindly reuse this drilling pattern.

**CBP-Z301** rail adapter, qty2: 6061-T6 strip240×20×4. World limits: Z20…260, Y−48…−28; left X−120…−116, right X116…120. Rail mounting taps M3 through at Z55/75/95/115/135/155/175/195/215/235, Y−38. Adapter end anchors Ø5.5 at Z30 and255, Y−38. Use M5×10+1 mm washer, giving5 mm slot projection. There is intentionally no M5 head under the rail: the heads are outside the rail ends. The top anchor center255 with4.25 mm head radius clears the rail end245 by5.75 mm. Rail screws M3×6 sit in the3.5 mm deep rail counterbores:3 mm remaining rail grip+3 mm thread into4 mm aluminum. Do not substitute M3×8 without accounting for the additional penetration.

Rail back faces: left X−116; right X116. Assembly mounting faces: left X−106; right X106. Rail/block dimensions follow the official [HIWIN guide catalog](https://www.hiwin.com/wp-content/uploads/HIWIN-Linear-Guideway-Catalog.pdf). Mounting caps omit raceway geometry. MGN9H block full assembly height10, block mounting rectangle15 across Y×16 along Z, M3 holes3 deep. Home block center Z203; final center Z143. Maximum block envelope40.9 gives Z182.55…223.45 at home,122.55…163.45 at bottom. Both are inside rail45…245. The unused lower rail length is deliberate assembly/endstop clearance, not extra rated travel.

**CBP-Z302** side plate, qty2: 6061-T6,5 thick×42 Y×42 Z. Left X−106…−101; right X101…106. Y−59…−17; Z182…224 at home. Four Ø3.3 block holes at Y−45.5/−30.5, Z195/211. Install M3×8 plus0.5 mm washer through5 mm plate:2.5 mm thread engagement,0.5 mm nominal bottoming clearance. The two yoke-joint holes are Ø4.4 at Y−55/−21, Z206.5. They do not overlap the MGN mounting pattern. Heads face inward; install them before the plate is enclosed by the bed. M4×12+0.8 mm washers engage6.2 mm of each yoke end tap.

Align one rail as the datum, then loosely fit the opposite adapter and cycle Z manually before tightening. The opposite rail is not a new kinematic degree of freedom; parallelism and coplanarity matter. Set initial assembly targets0.05 mm rail parallelism over200 and no detectable binding; these are build targets to verify, not guaranteed from raw extrusion. Use shims under adapters where needed. An abrasive-filled printed support must not substitute for a flat rail datum.

## Bed plate, yoke and leveling

**CBP-Z303** fork yoke: one6 mm6061 plate, home Z203.5…209.5. Main rectangle X±101, Y−63…−13. Front fingers X−51…−33 and33…51, Y−87…−63. Rear center arm X±20, Y−13…75. All features form a single connected plate. Outside corners R2; slot/window corners minimumR2 if milled. Drill/hand-saw fabrication can use round-corner chain-drilled windows; do not leave sharp notches.

At each end add two Ø8 screw-head scallops,4 mm deep inward alongX, centered Y−45.5/−30.5,Z211. These remove only the upper portion of the yoke end and clear the upper MGN mounting screws/OD7 washers. Without these scallops, their heads extend into the fork even though the nominal mounting-hole patterns do not overlap. They remain separated from the end M4 taps.

Through lightening windows: two40×22 rectangles centered(±65,−38) and one26×22 centered(0,−38). Leave end-tap engagement zones X94…101 and−101…−94 solid. Each end has two M4×0.7 holes tapped7 mm deep, along X at Y−55/−21, Z206.5. PilotØ3.3; drill at least10 mm for tap runout. These cross holes are in the6 mm edge; use a jig and verify they emerge in the center of the thickness. Manufacturing by a local CNC/router shop is preferable if a straight end-tap cannot be made reliably by hand.

Three level stations are(−42,−80),(42,−80),(0,4). At the left front use a Ø3.5 through hole; right front use a3.5×4.5 slot alongX; rear use a3.5×4.5 slot alongY. Slots accommodate thermal expansion and alignment; they do not provide bed XY travel. Use Ø7 washers under all three screw heads. Do not clamp the sliding points with separate lock nuts against the yoke.

**CBP-Z304** bed plate: stress-relieved flat aluminum100×100×4, centered(0,−38), Z220…224. Prefer cast tooling plate or a supplier-provided flat plate; an unknown saw-cut sheet is not assumed flat. Three M3×0.5 through taps at the level stations above. The locations are just outside the80 mm print square and6/8 mm from the plate edges. Deburr the top surface without a raised edge. Use M3×20 socket screws from underneath with0.5 mm washers. Home underside-head plane203; tip223; engagement3 mm in the plate and1 mm clearance to its top surface. Screw tips must never dimple the print surface. Limit useful leveling adjustment to±0.5 mm around nominal until actual screw lengths and sheet thickness are measured.

Three silicone tubes form **CBP-Z305** spacers:16 OD,4 ID,12 free length; nominal compressed height10.5. They bear between yoke top209.5 and bed bottom220. The M3 bolts pull the plate down against the elastomer and retain it against lifting. The rear station and front slots must slide enough that thermal expansion does not bow the plate. The spacer hardness and compression force are not sourced/calibrated: measure and substitute suitable commercial spacers if preload bows the plate. Fit printed clip-on thumb knobs only after verifying they cannot reach the motor bridge or wires at Z60.

The provisional unheated print stack is0.6 magnetic adhesive sheet plus0.4 spring-steel/PEI sheet above Al224, giving print surface225. These are **design allowances**, not a frozen supplier stack or validated adhesive thickness. Measure the actual stack, update the named parameters, and rerun nozzle/bed clearance. Unheated PLA with an appropriate adhesion surface avoids bed-heater mass, wiring and warmup cost; adhesion at the record attempt still needs testing. If a heated bed is needed, source its exact pad/insulation/lead exit and revise surface/mass/wiring, rather than hiding a generic heater inside the plate.

Nominal Z-moving masses using geometry/material density: aluminum plate108 g; yoke about197 g before final rounded corners/cross drills; two side plates47.6 g; rail blocks52 g; nut/cassette/spacers/surface/hardware still to weigh. A reasonable development allowance is500–650 g for the full Z carriage. This is not the XY toolhead mass and does not enter CoreXY rotor-torque calculations. Do not quote the earlier 100 g bed-only number as the complete Z mass.

## Screw drive and stationary motor bridge

Use the selected LDO42STH25-1004CL200E(VRN) integrated Tr8×8(P2,four-start) candidate. The reference maker interface is42.3 square×26 maximum body,31 square M3 mount spacing,200±1 screw, two nut mounts12.6 apart. Source: [LDO product page](https://store.ldomotion.com/products/ldo-42sth25-1004cl200e-vrn-nema17-linear-stepper-motor-200mm-tr8x8). Its exact pilot diameter, supplied nut flange thickness/body envelope and mounting orientation still need a drawing or measurement. Do not drill the cassette from nominal18 mm flange width alone.

Screw axis is(0,55), motor mounting faceZ29, bodyZ3…29, screw nominalZ29…229. Lowest body clears frame floorZ0 by3 mm; verify actual connector and wiring projection. The first-layer nut-cassette base datum isZ209.5; final is149.5. Actual nut flange position within the cassette is unverified. With a verified nut length≤20 and flange location suitably set, both remain on usable screw; recompute with the actual nut/lead-in/runout.

**CBP-Z306** stationary bridge:6061 plate270×80×6, X±135, Y15…95, Z20…26. It sits on the two lowerY extrusions. Cut centered44×44 motor-body clearance at(0,55), cornersR2 or sufficient for the actual motor corner radius. Four Ø5.5 anchors atX±130,Y30/80 use M5×12+1 mm washer,5 mm slot entry. Do not use a3 mm plate here: a simple260 mm span screen with7 N central load gives about0.28 mm for3×60 stock, versus about0.03 mm for6×80 stock before the motor aperture; the aperture still requires a physical stiffness check.

**CBP-Z307** printed motor riser:70×70×6, centered(0,55), Z26…32, in two steps. The lower3 mm frame Z26…29 has a44×44 body aperture withR2 corners; the upper3 mm web Z29…32 has the pilot hole. The motor front face contacts the **underside of the upper web atZ29**. A solid3 mm ring placed beneath that face would overlap the motor body and is incorrect. Center pilot clearanceØ24 is a **placeholder**, to replace with exact measured pilot+0.3 mm. Four motor holesØ3.3 atX±15.5,Y55±15.5 pass only through the upper web. Fit M3×6+0.5 mm washer from above:2.5 mm engagement. Four bridge anchorsØ4.4 atX±28,Y55±28 pass through the full6 mm riser and matching bridge through holes. Fit M4×20+0.8 mm washers on each side and full-height M4 nuts below the bridge. Do not countersink a3 mm printed web. Increase web thickness/update bolt lengths if actual motor loads distort it. A3 mm metal upper plate with3 mm perimeter stand-offs can replace the print using the same interfaces.

**CBP-Z308** optional rear-arm stiffener:20×20×2 aluminum angle, length54 alongY−16…38, vertical flange down from yoke underside203.5 to183.5, horizontal flange X−9…11, vertical legX9…11. Two M3 through bolts atX0,Y−10/20 attach it to the yoke. This first bolt position clears the rear silicone spacer: do not move it toY−6, where its top washer/head overlaps the spacer. Add Ø9 clearance through the horizontal foot at(0,4) for the rear-level screw head/washer; omitting this hole physically interferes with that adjustment. Use M3×16,0.5 mm washers each side and M3 nuts. Cut the angle so it ends before the nut cassette startsY39; it must not foul the nut body. Round/deburr its lower corner near wiring. This improves the stiffness of the drive arm without adding XY moving mass. The axisymmetric screw has no upper rigid radial bearing: allow its integrated shaft to seek alignment and use a floating nut rather than bending the screw between three incompatible datums.

### Z-only fastener schedule

This schedule excludes the main frame's corner caps, panels and gussets. Quantities include the two added guide posts.

| Fastener | Qty | Connection / nominal thread or slot engagement |
|---|---:|---|
| M5×30 SHCS | 2 | Lower Z-post end taps;9 mm with1 mm washer |
| M5×50 SHCS | 2 | Upper Z-post end taps through2040;9 mm |
| M5×10 SHCS | 4 | Rail-adapter ends;5 mm projection into slot |
| M5×12 SHCS | 4 | Motor bridge to bottom Y beams;5 mm projection |
| 5-series M5 T nut | 8 | Four adapters/four bridge; actual nut depth verify |
| M5 washer1 thick, OD10 | 12 | All above M5 screw heads |
| M3×6 SHCS | 24 | Twenty rail screws, four motor screws |
| M3×8 SHCS | 8 | Guideblock side plates;2.5 mm engagement |
| M4×12 SHCS | 4 | Side plates to end-tapped yoke;6.2 mm engagement |
| M3×20 SHCS | 7 | Three leveling and four cassette retaining bolts |
| M4×20 SHCS | 4 | Stepped riser through bridge into nuts |
| M3×16 SHCS | 2 | Angle through yoke into nuts |
| M3 washer0.5 thick | 23 | Eight block, four motor, three level, four cassette, four angle |
| M4 washer0.8 thick | 12 | Four end-yoke and eight riser washers |
| M4 nut | 4 | Riser mounts |
| M3 nut | 2 | Rear arm angle |

M3 washers at leveling/cassette stations are OD7. No washers under the20 rail screw heads because theØ6 counterbores do not acceptOD7 washers. Thread depths and screw tolerances must be checked against the actual purchased blocks/motor; do not bottom a screw in a3 mm blind mounting hole.

**CBP-Z309** floating-nut cassette and **Z310** cover are a development envelope only: lower body40×32×12 atX±20,Y39…71,Z209.5…221.5; cover40×32×2 at221.5…223.5. Four mountsX±16,Y43/67. Four M3×20+0.5 washers go through cover/body into the yoke, about5.5 mm engagement. A nominal22×18×6 flange pocket andØ14.5 body hole are provisional, explicitly not verified. The modeled12.6 mm reference nut-hole spacing must not be used as proof the nut fits this pocket. After measuring the nut, set0.2–0.3 mm lateral float per side,0.1–0.2 mm axial retention clearance and a broad anti-rotation contact. The nut may translate laterally slightly but must not lift, rotate, or be squeezed out of round. Use a replaceable insert rather than redesigning the entire yoke when the purchased nut changes.

## Assembly and checks

1. Deburr/cut/tap frame; dry-build on a flat surface. Set base diagonals, upright squareness and upper rail-carrier parallelism. Install side/rear panels while the frame is square, then tighten in passes.
2. Insert Z-post/end fasteners and adapters before closing access with motors/XY belts. Confirm the upper M5 post shafts do not intersect adapter screws, and that their top heads do not meet a belt/hose.
3. Install Z rails loosely, then fit two side plates and yoke. Cycle with the screw absent. It must move freely through the complete60 mm range without perceptible rail preload changes.
4. Install motor bridge/riser and screw. Mount the nut loosely in its cassette. Adjust motor position/shims until adding the nut does not change manual Z friction. Keep screw lubrication off the print surface.
5. Install silicone spacers and plate, then actual surface stack. Set nominal10.5 mm gap, verify screw-tip clearance and level within±0.5. Add a separate secured Z endstop/physical stop before powered homing. Do not use a hard stop as a homing sensor.
6. Set initial Z speed5 mm/s, acceleration50 mm/s², max travel60, with low current sufficient to prevent unintended descent. Test disabled-motor descent because Tr8×8 can backdrive. Add a catch/parking rest if it falls; never rely on a hot bed hanging from energized torque during servicing.
7. Verify swept clearances at all XY corners and Z0/Z60. Check a representative60×31×48 Benchy envelope, screw top229, cassette223.5, hotend/duct sweep, adjustment knobs, lead loops, motor connector and printed-part thermal exposure.
8. Measure bed flatness and Z repeatability, then measure the assembled frame/gantry modes. A first Euler beam calculation does not establish a usable input-shaper frequency; joint/panel stiffness, motor mounting and belt tension must be included and ultimately measured.

Initial acceptance targets: no binding through travel; no screw-tip print-surface damage; no loose spacer at the highest permitted adjustment; no panel screw bottoming; no guide/bed/toolhead interference; no uncontrolled bed fall with disabled motors; repeatable Z homing and bed plane before thermal or speed tests. The final mechanical audit must also reconcile all added nuts/washers and measured material masses with the assembly BOM.

## Generated geometry and completed subsystem checks

The builder `cad/revf/03_bed_z_cq.py` produces138 separate, valid BRep part instances and an assembly STEP in `cad/revf/exports/bed_z/`. Standard screws include shafts, heads and hex-drive recesses; washers and nuts are individual instances. Threads are represented by nominal screw shafts and tapped pilot holes. The exact named mating pairs are recorded as intentional thread overlaps, rather than blanket-excluding every fastener from interference testing. The purchased5-series T-nut shape and supplied LDO leadscrew nut are not fabricated from guesses.

The generated clearance report tests Z descent0/10/20/30/40/50/60 with a0.1 mm³ volume threshold. All seven poses have zero unexpected overlaps **within this Z subsystem**, including modeled bolt heads/washers. These checks found and resolved the motor-riser overlap, rear leveling-screw/angle collision, upper guideblock-head/yoke collisions and angle-bolt/silicone-spacer collision described above. They do not include the full XY assembly, frame anchor drill holes, hose, wiring, unmodeled nut, endstop or physical stops. Whole-printer clearance and switch design remain required.

The exported nominal Z-moving mass is497.15 g plus the unknown magnetic sheet, supplied nut and any later added wires/stops; some purchased masses use catalog overrides and others assumed material densities. Its partial mass-model COM isapproximately(0.11,−26.48,210.67) at home. This is not the completed toolhead COM or a measured mass. All printed-part export volumes assume solid material; an actual printed infill/perimeter specification and weighing are still needed.

The companion `cad/revf/03_bed_z.py` parses successfully and retains native Fusion dimensioned sketch/feature construction. It has **not been executed in Fusion** because the desktop was locked during this subtask. STEP generation does not establish that native sketches recompute or that Fusion joints/constraints have passed audit. Preserve the source and perform that native execution/audit when the desktop is available.
