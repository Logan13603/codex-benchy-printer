"""Fusion MCP CAD milestone 005: compact the static frame around bed sweep.

The RevD 400 mm plate/tall rear portal was an intentionally generous starting
envelope. RevE keeps the same guided bed but reduces static stock and the Z
support cantilever. Tower spacing and clearances remain to be physically proven.
"""


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root = design.rootComponent
    for name, expression in [
        ('base_x', '300 mm'),
        ('base_y', '260 mm'),
        ('tower_span', '220 mm'),
        ('tower_y', '90 mm'),
        ('tower_h', '180 mm'),
    ]:
        design.userParameters.itemByName(name).expression = expression
    dimension(design, 'tower_center_span', '180 mm',
              'Center-to-center distance of two rear Z columns')

    frame_occ = find_child(root, '10_FRAME')
    frame = frame_occ.component
    for native in frame.occurrences:
        if native.component.name not in (
            'CBP-1200_40MM_Z_COLUMN',
            'CBP-1210_Z_CROSSBEAM_ENVELOPE',
        ):
            continue
        proxy = native.createForAssemblyContext(frame_occ)
        transform = proxy.transform2
        if native.component.name == 'CBP-1200_40MM_Z_COLUMN':
            side = -1 if transform.translation.x < 0 else 1
            transform.translation = adsk.core.Vector3D.create(
                side * 9.0, 1.2, -9.0)
        else:
            transform.translation = adsk.core.Vector3D.create(
                0, 15.2, -9.0)
        proxy.transform2 = transform

    base = find_child(frame, 'CBP-1100_BASE_PLATE').component
    assert all(s.isFullyConstrained for s in base.sketches)
    print('base cm3', base.bRepBodies.item(0).volume)
    print('tower mm', design.userParameters.itemByName('tower_center_span').value * 10,
          design.userParameters.itemByName('tower_h').value * 10)
    for native in frame.occurrences:
        if native.component.name.startswith('CBP-12'):
            xyz = native.createForAssemblyContext(frame_occ).transform2.translation
            print(native.component.name, xyz.x, xyz.y, xyz.z)

