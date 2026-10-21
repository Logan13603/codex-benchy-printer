"""CBP RevF motor-free Bowden toolhead, world coordinates in mm.

build() returns named physical parts for the common assembly exporter.  Purchased
interfaces marked PROVISIONAL must be checked against the purchased item before
manufacture.  No slicer, thermal, airflow or physical performance claim is made.
This is the executable solid counterpart to 04_toolhead.py, not native Fusion
feature history.  Imported maker STEP is retained separately by the main builder.
"""
from pathlib import Path
import json
import math
import cadquery as cq

NOZZLE = (0.0, -38.0, 225.0)
MOUNT_Z = 294.26
PLATE_T = 6.0
WALL = 1.2
PARTS = []


def block(dx, dy, dz, center):
    return cq.Workplane("XY").box(dx, dy, dz).val().translate(center)


def cylinder(radius, length, start, axis=(0, 0, 1)):
    return cq.Solid.makeCylinder(radius, length, cq.Vector(*start), cq.Vector(*axis))


def drill(shape, diameter, length, start, axis=(0, 0, 1)):
    return shape.cut(cylinder(diameter / 2.0, length, start, axis))


def wire_rect(center, normal, width_y, height_xz):
    return cq.Workplane(cq.Plane(origin=center, xDir=(0, 1, 0), normal=normal)).rect(width_y, height_xz).val()


def tube_loft(sections, extra=0.0):
    wires = [wire_rect(p, n, wy + 2 * extra, hx + 2 * extra) for p, n, wy, hx in sections]
    # Ruled sections prevent the uncontrolled overshoot of an interpolating loft
    # into the nozzle / heater envelope.  Five transitions spread the two turns.
    return cq.Solid.makeLoft(wires, ruled=True)


def hex_prism(across_flats, length, start, axis=(0, 0, 1)):
    plane = cq.Plane(origin=start, normal=axis)
    return cq.Workplane(plane).polygon(6, across_flats / math.cos(math.pi / 6)).extrude(length).val()


def add(name, shape, material, category, notes="", density=None, motiongroup="toolhead"):
    shape = shape.clean()
    if shape.isNull() or not shape.isValid():
        raise ValueError("Invalid solid: " + name)
    row = dict(name=name, shape=shape, material=material, category=category,
               notes=notes, motion_group=motiongroup)
    if density is not None:
        row["density_g_cm3"] = density
    PARTS.append(row)
    return shape


def screw(name, diameter, length, start, axis, head_d=None, head_h=None, material="Steel"):
    head_d = head_d or diameter * 1.8
    head_h = head_h or diameter
    a = cq.Vector(*axis)
    p = cq.Vector(*start)
    shank = cylinder(diameter / 2, length, start, axis)
    head_start = p - a.multiply(head_h)
    head = cylinder(head_d / 2, head_h, head_start.toTuple(), axis)
    # Socket is a real hex recess; external thread is a cylindrical simplification.
    socket = hex_prism(diameter * .8, head_h * .65,
                       (head_start + a.multiply(head_h * .05)).toTuple(), axis)
    add(name, shank.fuse(head).cut(socket), material, "fastener",
        "External thread simplified; length measured below head", 7.85)


def nut(name, diameter, start, axis, across_flats=None, thickness=None):
    af = across_flats or (5.5 if diameter == 3 else 5.0 if diameter == 2.5 else 4.0)
    t = thickness or (2.4 if diameter == 3 else 2.0 if diameter == 2.5 else 1.6)
    s = hex_prism(af, t, start, axis)
    s = drill(s, diameter * .85, t + .2, start, axis)
    add(name, s, "Steel", "fastener", "Nut thread simplified to minor bore", 7.85)


def branch_sections(side):
    rt2 = math.sqrt(.5)
    a = math.radians(17)
    return [
        ((side * 8, -14, 331), (0, 0, -1), 10, 12),
        ((side * 24, -26, 315), (side * rt2, 0, -rt2), 10, 12),
        ((side * 42, -38, 297), (0, 0, -1), 10, 12),
        ((side * 42, -38, 247), (0, 0, -1), 10, 12),
        ((side * 38, -38, 237), (-side * .5, 0, -math.sqrt(.75)), 14, 7),
        ((side * 27, -38, 231), (-side * math.sqrt(.75), 0, -.5), 16, 4),
        ((side * 12, -38, 228.8), (-side * math.cos(a), 0, -math.sin(a)), 16, 3),
    ]


def make_air_system():
    # The inlet is deliberately 24 mm behind the filament axis.  A coaxial CPAP
    # inlet would collide with the Bowden tube directly above the hotend.
    outer = cylinder(12.5, 24, (0, -14, 326))
    inner = cylinder(11, 26, (0, -14, 325))
    for side in (-1, 1):
        sec = branch_sections(side)
        outer = outer.fuse(tube_loft(sec, WALL))
        # Extend through each final outlet by .25 mm to avoid a numerical cap.
        last = sec[-1]
        n = cq.Vector(*last[1])
        p = cq.Vector(*last[0]) + n.multiply(.25)
        ins = list(sec)
        ins[-1] = (p.toTuple(), last[1], last[2], last[3])
        inner = inner.fuse(tube_loft(ins))
    air = outer.cut(inner)
    # Each branch has three seam bolts, with tabs extending outboard of the
    # airflow. The shell will be split at Y=-38 over the lower trunks, whereas
    # the sloping inlet portion requires a second split plane at Y=-14.
    # A single global center split cannot intersect both offset centerlines.
    # Manufacture as complete left/right branches split in their own vertical
    # median surfaces; the robust implementation below uses a vertical X=0
    # split for the inlet fork, and Y=-38 for each lower trunk module.
    # The inlet fork is a separate front/back part cut at Y=-14; lower ducts
    # attach via rectangular four-screw flanges at Z=297.
    top = air.intersect(block(200, 200, 100, (0, -20, 347)))
    lower_cut = block(200, 200, 100, (0, -38, 247))
    lower = air.intersect(lower_cut)
    # Z=297 mating flanges, outer 37 x 20.2, four M2.5 on 31x14.2 mm.
    # Wide ears keep the nuts clear of the inward-sloping fork immediately above.
    # 2 mm top and lower flange plates have shared free flow apertures.
    for side in (-1, 1):
        for zc, dest in [(298, "top"), (296, "lower")]:
            flange = block(37, 20.2, 2, (side * 42, -38, zc))
            flange = flange.cut(block(12, 10, 4, (side * 42, -38, zc)))
            for xx in (-15.5, 15.5):
                for yy in (-7.1, 7.1):
                    flange = drill(flange, 2.7, 4, (side * 42 + xx, -38 + yy, zc - 2))
            if dest == "top":
                top = top.fuse(flange)
            else:
                lower = lower.fuse(flange)
        # Outboard trunk seam tabs, split halves 2.5 mm each.
        for z in (248, 271, 289):
            lower = lower.fuse(block(8, 5, 6, (side * 52.4, -38, z)))
            lower = drill(lower, 2.7, 7, (side * 52.4, -41.5, z), (0, 1, 0))
            lower = lower.cut(hex_prism(5.0, 2, (side * 52.4, -35.5, z), (0, -1, 0)))
        # Rear boss engages M3 nut without perforating the 1.2 mm air wall.
        lower = lower.fuse(block(10, 4, 10, (side * 42, -29.8, 292)))
        lower = drill(lower, 3.3, 3.7, (side * 42, -27.8, 292), (0, -1, 0))
        lower = lower.cut(hex_prism(5.5, 2.4, (side * 42, -27.8, 292), (0, -1, 0)))
    # Paired bolt pads provide positive assembly at the inlet and arm midpoints.
    for x in (-16, 16):
        top = top.fuse(block(10, 6, 8, (x, -14, 339)))
        top = drill(top, 2.7, 8, (x, -18, 339), (0, 1, 0))
        top = top.cut(hex_prism(5, 2, (x, -11, 339), (0, -1, 0)))
    for side in (-1, 1):
        top = top.fuse(block(22, 6, 8, (side * 39, -26, 315)))
        top = drill(top, 2.7, 8, (side * 39, -30, 315), (0, 1, 0))
        top = top.cut(hex_prism(5, 2, (side * 39, -23, 315), (0, -1, 0)))
    # The seam follows the branch median Y(Z), rather than cutting at one global
    # Y. This exposes both angled arms for support removal and internal sealing.
    front_mask = cq.Workplane("YZ").polyline([
        (-150, 190), (-38, 190), (-38, 297), (-26, 315),
        (-14, 331), (-14, 400), (-150, 400)]).close().extrude(110, both=True).val()
    front_top = top.intersect(front_mask)
    rear_top = top.cut(front_mask)
    add("CBP-P411_R1_CPAP_FORK_FRONT", front_top, "PA12", "printed",
        "22 mm inlet ID / 25 mm spigot OD PROVISIONAL; two M2.5 seam bolts; seal seam with thin neutral-cure silicone", 1.01)
    add("CBP-P412_R1_CPAP_FORK_REAR", rear_top, "PA12", "printed",
        "Matching median-surface cover; both arm channels open for support removal; mating faces need thin sealant", 1.01)
    for side, word in [(-1, "LEFT"), (1, "RIGHT")]:
        side_lower = lower.intersect(block(100, 150, 100, (side * 50, -38, 247)))
        front = side_lower.intersect(block(200, 100, 120, (0, -88, 247)))
        rear = side_lower.intersect(block(200, 100, 120, (0, 12, 247)))
        add("CBP-P41" + ("3" if side < 0 else "5") + "_R1_" + word + "_DUCT_FRONT", front, "PA12", "printed",
            "1.2 mm nominal wall; open seam Y=-38 faces print bed; opposed 16x3 mm outlet aims down 17 deg; lower outer lip >=226.2 mm", 1.01)
        add("CBP-P41" + ("4" if side < 0 else "6") + "_R1_" + word + "_DUCT_REAR", rear, "PA12", "printed",
            "Three M2.5 seam bolts, captive nuts; M3 support nut pocket does not enter airflow", 1.01)
        for z in (248, 271, 289):
            screw("CBP-H41_%s_SEAM_%d_M2p5x8" % (word, z), 2.5, 8,
                  (side * 52.4, -40.5, z), (0, 1, 0), 4.5, 2.5)
            nut("CBP-H42_%s_SEAM_%d_M2p5" % (word, z), 2.5,
                (side * 52.4, -35.5, z), (0, -1, 0))
        for i, xx in enumerate((-15.5, 15.5)):
            for j, yy in enumerate((-7.1, 7.1)):
                screw("CBP-H43_%s_FLANGE_%d%d_M2p5x8" % (word, i, j), 2.5, 8,
                      (side * 42 + xx, -38 + yy, 295), (0, 0, 1), 4.5, 2.5)
                nut("CBP-H44_%s_FLANGE_%d%d_M2p5" % (word, i, j), 2.5,
                    (side * 42 + xx, -38 + yy, 299), (0, 0, 1))
        screw("CBP-H45_%s_SUPPORT_M3x10" % word, 3, 10,
              (side * 42, -21, 292), (0, -1, 0))
        nut("CBP-H46_%s_SUPPORT_M3" % word, 3,
            (side * 42, -27.8, 292), (0, -1, 0))
    for side in (-1, 1):
        screw("CBP-H47_FORK_%s_M2p5x10" % side, 2.5, 10,
              (side * 16, -17, 339), (0, 1, 0), 4.5, 2.5)
        nut("CBP-H48_FORK_%s_M2p5" % side, 2.5,
            (side * 16, -11, 339), (0, -1, 0))
        screw("CBP-H49_FORK_ARM_%s_M2p5x10" % side, 2.5, 10,
              (side * 39, -29, 315), (0, 1, 0), 4.5, 2.5)
        nut("CBP-H50_FORK_ARM_%s_M2p5" % side, 2.5,
            (side * 39, -23, 315), (0, -1, 0))


def make_carrier():
    spine = block(36, 3, 46.26, (0, -19.5, 279.13))
    for x in (-6.5, 6.5):
        for z in (274, 286):
            spine = drill(spine, 2.2, 4, (x, -17.5, z), (0, -1, 0))
    for x in (-10, 10):
        spine = drill(spine, 3.3, 4, (x, -17.5, 297.26), (0, -1, 0))
    for x in (-11, 11):
        spine = drill(spine, 2.5, 4, (x, -17.5, 292), (0, -1, 0))
    for x in (-10, 10):
        spine = drill(spine, 1.6, 4, (x, -17.5, 260), (0, -1, 0))
    for x in (-15, 15):
        spine = drill(spine, 1.6, 4, (x, -17.5, 294), (0, -1, 0))
    add("CBP-P401_R1_AL_CARRIAGE_SPINE", spine, "6061-T6", "cnc",
        "3 mm plate; 4x M2 clearance on 13x12 mm MGN7H pattern; 2x M3 tapped support holes; deburr .2 mm", 2.70)
    plate = block(32, 30, 6, (0, -36, 297.26))
    for x in (-5.657, 5.657):
        for dy in (-5.657, 5.657):
            plate = drill(plate, 2.7, 7, (x, -38 + dy, MOUNT_Z - .5))
    # Real M6x1 tapped interface; model uses the 5 mm tap drill, not a loose
    # pressure socket. A verified tube-through PC4-M6 fitting must be purchased.
    plate = drill(plate, 5, 7, (0, -38, MOUNT_Z - .5))
    for x in (-10, 10):
        plate = drill(plate, 2.5, 10, (x, -21, 297.26), (0, -1, 0))
    for x in (-12, 12):
        plate = drill(plate, 2.5, 4.5, (x, -48, 300.26), (0, 0, -1))
    for x in (-11, 11):
        plate = drill(plate, 6.4, 1, (x, -29.8, MOUNT_Z))
    add("CBP-P402_R1_AL_HOTEND_PLATFORM", plate, "6061-T6", "cnc",
        "6 mm plate; center M6x1 THRU; four maker-pattern M2.5 clearance holes; rear 2x M3x.5 tapped depth8/drill10; fan top 2x M3 tapped4/drill4.5; underside 2x D6.4 x1 screw-head reliefs. Confirm maker hotend mount thread before release", 2.70)
    brace = block(104, 6.8, 7, (0, -24.4, 292))
    # Clear the aluminum platform without dropping into the upper belt envelope
    # Z277.8..286.8. The central bridge remains 5.76 mm tall after this notch.
    brace = brace.cut(block(34, 9, 5, (0, -24.4, 296.76)))
    # Maker STEP has an upper flange that projects to Y=-27.1. Clear it by
    # 2 mm without moving the hotend or weakening the two mounting pads.
    brace = brace.cut(block(13, 4, 9, (0, -27.1, 292)))
    for x in (-11, 11, -42, 42):
        brace = drill(brace, 3.3, 8, (x, -28.4, 292), (0, 1, 0))
    # Two service windows reduce mass while retaining continuous top/bottom rails.
    for x in (-25, 25):
        brace = brace.cut(block(18, 8, 3, (x, -24.4, 292)))
    add("CBP-P403_R1_DUCT_SUPPORT_BRIDGE", brace, "PA12-CF", "printed",
        "Attaches to tapped aluminum spine with 2x M3x10 + .5 mm washers; duct mounting M3x10 each side", 1.08)
    # Purchased coupler is an interface proxy, not an invented certified part.
    fitting = cylinder(3, 6, (0, -38, 294.26))
    fitting = fitting.fuse(hex_prism(8, 5, (0, -38, 300.26)))
    fitting = fitting.fuse(cylinder(3.5, 5, (0, -38, 305.26)))
    fitting = drill(fitting, 4.1, 17, (0, -38, 294))
    add("CBP-C401_R1_PC4_M6_THROUGH_COUPLER_PROXY", fitting, "Brass/steel", "purchased",
        "PROVISIONAL envelope: M6x1 x6 male, AF8 body, 16 mm total; buy a genuine 4 mm tube-through metal fitting and verify actual engagement/pullout", 7.5)
    PARTS[-1]["mass_override_g"] = 5.0
    PARTS[-1]["mass_status"] = "unverified estimate; geometric density mass is not the assembly mass"
    tube = cylinder(2, 38, (0, -38, 294.26))
    tube = drill(tube, 2, 39, (0, -38, 294))
    add("CBP-C402_R1_BOWDEN_ENTRY_PTFE", tube, "PTFE", "purchased",
        "4 OD / 2 ID, first 38 mm only; remainder of short Bowden route is modeled by fixed extruder layout; tube must seat against maker stop, measure depth", 2.2)
    # Four hotend screws: 6 mm plate + 1 mm controlled shim + 3 mm thread.
    for i, x in enumerate((-5.657, 5.657)):
        for j, dy in enumerate((-5.657, 5.657)):
            shim = cylinder(2.5, 1, (x, -38 + dy, 300.26))
            shim = drill(shim, 2.7, 1.2, (x, -38 + dy, 300.16))
            add("CBP-H401_%d%d_HOTEND_SHIM_1MM" % (i, j), shim, "Steel", "fastener",
                "Controlled 1.0 mm thickness; two verified .5 mm washers allowed; 3.0 mm thread engagement / .375 mm nominal tip clearance", 7.85)
            screw("CBP-H402_%d%d_M2p5x10" % (i, j), 2.5, 10,
                  (x, -38 + dy, 301.26), (0, 0, -1), 4.5, 2.5)
    for i, x in enumerate((-10, 10)):
        screw("CBP-H403_%d_PLATFORM_M3x10" % i, 3, 10,
              (x, -18, 297.26), (0, -1, 0))
    for i, x in enumerate((-11, 11)):
        washer = cylinder(3, .5, (x, -28.3, 292), (0, 1, 0))
        washer = drill(washer, 3.2, .7, (x, -28.4, 292), (0, 1, 0))
        add("CBP-H404_%d_BRIDGE_WASHER" % i, washer, "Steel", "fastener", "M3 DIN433 small washer OD6 / t.5 mm", 7.85)
        screw("CBP-H405_%d_BRIDGE_M3x10" % i, 3, 10,
              (x, -28.3, 292), (0, 1, 0))
    for i, x in enumerate((-6.5, 6.5)):
        for j, z in enumerate((274, 286)):
            screw("CBP-H409_%d%d_CARRIAGE_M2x5" % (i, j), 2, 5,
                  (x, -21, z), (0, 1, 0), 3.8, 2)
    shield = block(24, .5, 20, (0, -22.75, 253))
    for x in (-10, 10):
        shield = drill(shield, 2.2, 1, (x, -23.2, 260), (0, 1, 0))
    add("CBP-P405_R1_REAR_THERMAL_WIRE_GUARD", shield, "5052-H32", "cnc",
        ".5 mm sheet; rear radiant/wire guard only; minimum 7 mm hotend gap; top Z263 clears lower belt envelope starting Z264.8. Not a substitute for maker silicone sock", 2.68)
    for i, x in enumerate((-10, 10)):
        spacer = cylinder(2, 1.5, (x, -22.5, 260), (0, 1, 0))
        spacer = drill(spacer, 2.2, 1.7, (x, -22.6, 260), (0, 1, 0))
        add("CBP-H410_%d_GUARD_STANDOFF" % i, spacer, "Aluminum", "fastener", "OD4/ID2.2/L1.5 precision spacer", 2.70)
        screw("CBP-H411_%d_GUARD_M2x4" % i, 2, 4,
              (x, -23, 260), (0, 1, 0), 3.8, 2)
    saddle = block(36, 7, 8, (0, -14.5, 295))
    cover = block(36, 2, 8, (0, -10, 295))
    for x in (-3, 3):
        saddle = drill(saddle, 3.5, 9, (x, -11, 290.5))
        cover = drill(cover, 3.5, 9, (x, -11, 290.5))
    for x in (-15, 15):
        saddle = drill(saddle, 2.2, 8, (x, -10.5, 294), (0, -1, 0))
        cover = drill(cover, 2.2, 3, (x, -8.5, 294), (0, -1, 0))
    for x in (-10, 10):
        saddle = drill(saddle, 7, 11, (x, -18.5, 297.26), (0, 1, 0))
        cover = drill(cover, 7, 11, (x, -18.5, 297.26), (0, 1, 0))
    add("CBP-P406_R1_WIRE_SADDLE", saddle, "PA12-CF", "printed",
        "Two separate 3.5 mm vertical bundle grooves keep heater and sensor leads separated; screw to tapped spine; no connector or wire bend below belt plane", 1.08)
    add("CBP-P407_R1_WIRE_SADDLE_COVER", cover, "PA12-CF", "printed",
        "Removable cover; do not crush insulation; use compliant silicone sleeve or adjust groove to actual wire bundle diameter", 1.08)
    for i, x in enumerate((-15, 15)):
        washer = cylinder(2.5, .3, (x, -9, 294), (0, 1, 0))
        washer = drill(washer, 2.2, .5, (x, -9.1, 294), (0, 1, 0))
        add("CBP-H412_%d_WIRE_WASHER" % i, washer, "Steel", "fastener", "M2 washer OD5 / t.3 mm", 7.85)
        screw("CBP-H413_%d_WIRE_M2x12" % i, 2, 12,
              (x, -8.7, 294), (0, -1, 0), 3.8, 2)


def make_fan():
    ring = block(30, 3, 30, (0, -66.5, 272))
    ring = drill(ring, 22, 4, (0, -68.5, 272), (0, 1, 0))
    for x in (-10, 10):
        for z in (262, 282):
            ring = drill(ring, 2.2, 4, (x, -68.5, z), (0, 1, 0))
    # Here xDir cannot be parallel to plane normal; use a dedicated XZ profile.
    # Recreate these two wires with X along world X.
    outer = cq.Solid.makeLoft([cq.Workplane(cq.Plane(origin=(0, y, 272), xDir=(1, 0, 0), normal=(0, 1, 0))).rect(w, w).val()
                              for y, w in [(-65, 22.4), (-52, 26.4)]], ruled=True)
    inner = cq.Solid.makeLoft([cq.Workplane(cq.Plane(origin=(0, y, 272), xDir=(1, 0, 0), normal=(0, 1, 0))).rect(w, w).val()
                              for y, w in [(-65.2, 20), (-51.8, 24)]], ruled=True)
    ring = ring.fuse(outer.cut(inner))
    for x in (-10, 10):
        for z in (262, 282):
            ring = drill(ring, 5.4, 8, (x, -65, z), (0, 1, 0))
    for x in (-12, 12):
        ring = ring.fuse(block(4, 3, 17.26, (x, -66.5, 294.63)))
        ring = ring.fuse(block(8, 18.5, 3, (x, -57.25, 301.76)))
        ring = drill(ring, 3.3, 4, (x, -48, 299.76))
    add("CBP-P404_R1_COLDEND_FAN_CRADLE", ring, "PA12-CF", "printed",
        "2510 axial-fan 20 mm hole pitch PROVISIONAL; verify mounting pattern, voltage, airflow and hotend vendor thermal requirements. Shroud exits Y=-52 leaving a nominal 2.5 mm fin clearance", 1.08)
    fan = block(25, 10, 25, (0, -73, 272))
    fan = drill(fan, 22, 11, (0, -78.5, 272), (0, 1, 0))
    hub = cylinder(4, 9.5, (0, -77.75, 272), (0, 1, 0))
    fan = fan.fuse(hub)
    # Four narrow stator spokes avoid a visually misleading solid fan plug.
    for a in (0, 90, 180, 270):
        spoke = block(8, 1.2, 1.2, (7, -69, 272)).rotate((0, -69, 272), (0, -68, 272), a)
        fan = fan.fuse(spoke)
    for x in (-10, 10):
        for z in (262, 282):
            fan = drill(fan, 2.2, 11, (x, -78.5, z), (0, 1, 0))
    add("CBP-C403_R1_2510_COLDEND_FAN_PROXY", fan, "Purchased mixed", "purchased",
        "PROVISIONAL 25x25x10 / 20 mm hole pitch; use supplier declared mass rather than geometric mass", 1.1)
    PARTS[-1]["mass_override_g"] = 8.0
    PARTS[-1]["mass_status"] = "unverified estimate; geometric density mass is not the assembly mass"
    for i, x in enumerate((-10, 10)):
        for j, z in enumerate((262, 282)):
            screw("CBP-H406_%d%d_FAN_M2x16" % (i, j), 2, 16,
                  (x, -78, z), (0, 1, 0), 3.8, 2)
            nut("CBP-H407_%d%d_FAN_M2" % (i, j), 2,
                (x, -65, z), (0, 1, 0))
    for i, x in enumerate((-12, 12)):
        screw("CBP-H408_%d_CRADLE_M3x6" % i, 3, 6,
              (x, -48, 303.26), (0, 0, -1))


def build():
    PARTS.clear()
    vendor = Path(__file__).resolve().parent.parent / "vendor" / "Goliath_Mockup_AIR.STEP"
    hotend = cq.importers.importStep(str(vendor)).val().translate((0, -38, 250.7500006854531))
    add("CBP-C404_R1_GOLIATH_AIR_MAKER_STEP", hotend, "Purchased mixed", "purchased",
        "Official VzBoT maker STEP; exact modeled mounting interface, 80 g provisional mass estimate until weighed; no uniform-density mass assumption")
    PARTS[-1]["mass_override_g"] = 80.0
    PARTS[-1]["mass_status"] = "unverified estimate"
    make_carrier()
    make_air_system()
    make_fan()
    return PARTS


def export_standalone(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    assy = cq.Assembly(name="CBP_RevF_Bowden_Toolhead")
    for p in build():
        name, shape = p["name"], p["shape"]
        cq.exporters.export(shape, str(folder / (name + ".step")))
        if p["category"] in ("printed", "cnc"):
            cq.exporters.export(shape, str(folder / (name + ".stl")), tolerance=.03, angularTolerance=.15)
        assy.add(shape, name=name)
        com = shape.Center()
        density = p.get("density_g_cm3")
        rows.append({k: v for k, v in p.items() if k != "shape"} | dict(
            volume_mm3=shape.Volume(), com_mm=list(com.toTuple()),
            geometric_mass_g=shape.Volume() / 1000 * density if density else None,
            solids=len(shape.Solids())))
    assy.save(str(folder / "CBP_RevF_Bowden_Toolhead.step"))
    (folder / "toolhead-components.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return rows


if __name__ == "__main__":
    import sys
    rows = export_standalone(sys.argv[1] if len(sys.argv) > 1 else "outputs/codex-benchy-printer/cad/revf/generated/toolhead")
    print("Exported", len(rows), "named parts")
