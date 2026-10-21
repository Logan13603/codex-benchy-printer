"""First stationary-XY Z guide placement, with honest purchased proxies.

The rear mast touches the crossbeam's forward face and begins 10 mm above
the existing bed surface. A 125 mm MGN12 rail proxy and MGN12H cap proxy
allow 60 mm commanded carriage travel with end allowance. Interfaces,
fasteners, screw drive and block raceway still require detail.
HIWIN catalog: MGN12 rail 12 × 8 mm, MGN12H 27 × 45.4 mm,
assembly height 13 mm, block mass 54 g, rail mass 0.65 kg/m.
Read common.py before running.
"""


def run(_context: str):
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    for name, expr, note in [
        ('z_mast_w', '20 mm', 'Central fixed Z mast X width'),
        ('z_mast_depth', '20 mm', 'Central fixed Z mast front-back depth'),
        ('z_mast_h', '137 mm', 'Mast from machine height 55 to 192 mm'),
        ('z_rail_l', '125 mm', 'Development MGN12 Z rail length'),
        ('mgn12_rail_w', '12 mm', 'HIWIN MGN12 rail width'),
        ('mgn12_rail_h', '8 mm', 'HIWIN MGN12 rail height'),
        ('mgn12h_block_w', '27 mm', 'HIWIN MGN12H block width'),
        ('mgn12h_block_l', '45.4 mm', 'HIWIN MGN12H block length'),
        ('mgn12h_cap_depth', '5 mm', 'Proxy cap: 13 mm assembly less 8 mm rail'),
    ]:
        dimension(d, name, expr, note)
    frame = find_child(d.rootComponent, '10_FRAME').component
    mast = child(frame, 'CBP-1220_REAR_Z_MAST',
                 (0, 5.5, -6.0))
    constrained_box(mast.component, 'SK-1220-01_MAST_SECTION',
                    'CBP-1220_MAST_SOLID_STOCK',
                    'z_mast_w', 'z_mast_depth', 'z_mast_h')
    z_axis = find_child(d.rootComponent, '40_Z_AXIS').component
    rail = child(z_axis, 'CBP-P401_MGN12_Z_RAIL_125_PROXY',
                 (0, 6.2, -4.6))
    constrained_box(rail.component, 'SK-P401-01_Z_RAIL_ENVELOPE',
                    'CBP-P401_MGN12_RAIL_ENVELOPE',
                    'mgn12_rail_w', 'mgn12_rail_h', 'z_rail_l')
    block = child(z_axis, 'CBP-P402_MGN12H_Z_BLOCK_PROXY',
                  (0, 7.0, -3.95))
    constrained_box(block.component, 'SK-P402-01_Z_BLOCK_CAP',
                    'CBP-P402_MGN12H_UPPER_CAP_ENVELOPE',
                    'mgn12h_block_w', 'mgn12h_cap_depth',
                    'mgn12h_block_l')
    print('mast', mast.component.bRepBodies.item(0).volume,
          'rail', rail.component.bRepBodies.item(0).volume,
          'cap', block.component.bRepBodies.item(0).volume)
