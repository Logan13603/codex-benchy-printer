"""Fusion MCP CAD milestone 003: provisional crossed CoreXY moving-bed guides.

Read common.py into the same script invocation before executing this file.
HIWIN MGN7/H reference dimensions are from the manufacturer's guideway catalog;
rail ends, holes and carriage raceways require a purchased interface freeze.
"""


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root = design.rootComponent
    motion_root_occ = find_child(root, '20_XY_MOTION')
    bed_root_occ = find_child(root, '30_BED')
    motion = motion_root_occ.component
    bed = bed_root_occ.component

    for name, expr, note in [
        ('x_rail_l', '130 mm', 'X rail cut length; MGN7 candidate'),
        ('y_rail_l', '110 mm', 'Y rail cut length; MGN7 candidate'),
        ('x_rail_sep', '120 mm', 'Center-to-center X rail spacing'),
        ('mgn7_rail_w', '7 mm', 'HIWIN MGN7 rail envelope width'),
        ('mgn7_rail_h', '4.8 mm', 'HIWIN MGN7 rail envelope height'),
        ('mgn7h_block_l', '30.8 mm', 'HIWIN MGN7H block overall length'),
        ('mgn7h_block_w', '17 mm', 'HIWIN MGN7H block overall width'),
        ('mgn7h_block_cap_h', '3.2 mm', '8 mm overall assembly height less 4.8 mm rail height; proxy cap only'),
        ('bridge_w', '10 mm', 'X moving bridge X-section'),
        ('bridge_span', '140 mm', 'X moving bridge length along machine Y'),
        ('bridge_h', '10 mm', 'X moving bridge vertical envelope'),
    ]:
        dimension(design, name, expr, note)

    x_rail_a = child(motion, 'CBP-P201_MGN7_X_RAIL_130_PROXY',
                     (0, 1.4, -6.0))
    constrained_box(x_rail_a.component, 'SK-P201-01_X_RAIL_ENVELOPE',
                    'CBP-P201_X_RAIL_ENVELOPE',
                    'x_rail_l', 'mgn7_rail_w', 'mgn7_rail_h')
    x_rails = [o for o in motion.occurrences if o.component == x_rail_a.component]
    if len(x_rails) == 1:
        motion.occurrences.addExistingComponent(
            x_rail_a.component, moved(0, 1.4, 6.0))

    x_block_a = child(motion, 'CBP-P202_MGN7H_X_BLOCK_PROXY',
                      (0, 1.88, -6.0))
    constrained_box(x_block_a.component, 'SK-P202-01_X_BLOCK_CAP',
                    'CBP-P202_X_BLOCK_UPPER_ENVELOPE',
                    'mgn7h_block_l', 'mgn7h_block_w', 'mgn7h_block_cap_h')
    x_blocks = [o for o in motion.occurrences if o.component == x_block_a.component]
    if len(x_blocks) == 1:
        motion.occurrences.addExistingComponent(
            x_block_a.component, moved(0, 1.88, 6.0))

    bridge = child(motion, 'CBP-2200_CARBON_X_BRIDGE', (0, 2.2, 0))
    constrained_box(bridge.component, 'SK-2200-01_BRIDGE_ENVELOPE',
                    'CBP-2200_BRIDGE_STOCK',
                    'bridge_w', 'bridge_span', 'bridge_h')

    y_rail = child(motion, 'CBP-P203_MGN7_Y_RAIL_110_PROXY',
                   (0, 3.2, 0))
    constrained_box(y_rail.component, 'SK-P203-01_Y_RAIL_ENVELOPE',
                    'CBP-P203_Y_RAIL_ENVELOPE',
                    'mgn7_rail_w', 'y_rail_l', 'mgn7_rail_h')
    y_block = child(motion, 'CBP-P204_MGN7H_Y_BLOCK_PROXY',
                    (0, 3.68, 0))
    constrained_box(y_block.component, 'SK-P204-01_Y_BLOCK_CAP',
                    'CBP-P204_Y_BLOCK_UPPER_ENVELOPE',
                    'mgn7h_block_w', 'mgn7h_block_l', 'mgn7h_block_cap_h')

    # Set assembly-context positions. The low rail level leaves only a 2 mm
    # shim between the 12 mm base and rail, reducing guide support bending.
    levels = {
        'CBP-P201_MGN7_X_RAIL_130_PROXY': 1.4,
        'CBP-P202_MGN7H_X_BLOCK_PROXY': 1.88,
        'CBP-2200_CARBON_X_BRIDGE': 2.2,
        'CBP-P203_MGN7_Y_RAIL_110_PROXY': 3.2,
        'CBP-P204_MGN7H_Y_BLOCK_PROXY': 3.68,
        'CBP-2100_CARBON_XY_STAGE': 4.0,
    }
    for occurrence in motion.occurrences:
        proxy = occurrence.createForAssemblyContext(motion_root_occ)
        transform = proxy.transform2
        old = transform.translation
        transform.translation = adsk.core.Vector3D.create(
            old.x, levels[occurrence.component.name], old.z)
        proxy.transform2 = transform
    for occurrence, level in [
        (find_child(bed, 'CBP-3100_BED_SUBSTRATE'), 4.2),
        (find_child(bed, 'CBP-3110_BUILD_SURFACE'), 4.5),
    ]:
        proxy = occurrence.createForAssemblyContext(bed_root_occ)
        transform = proxy.transform2
        old = transform.translation
        transform.translation = adsk.core.Vector3D.create(old.x, level, old.z)
        proxy.transform2 = transform

    print('motion', [(o.component.name,
                      round(o.createForAssemblyContext(motion_root_occ).transform2.translation.y, 3),
                      round(o.createForAssemblyContext(motion_root_occ).transform2.translation.z, 3))
                     for o in motion.occurrences])
    print('bed', [(o.component.name,
                   round(o.createForAssemblyContext(bed_root_occ).transform2.translation.y, 3))
                  for o in bed.occurrences])
