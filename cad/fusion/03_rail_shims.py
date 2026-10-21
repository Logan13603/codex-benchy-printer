"""Fusion MCP CAD milestone 004: low static X-rail alignment shims."""


def run(_context: str):
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root = design.rootComponent
    frame = find_child(root, '10_FRAME').component
    dimension(design, 'x_shim_w', '12 mm',
              'Machined X-rail support strip width across machine Y')
    dimension(design, 'x_shim_t', '2 mm',
              'Matched X-rail shim thickness; reference until measured')
    first = child(frame, 'CBP-1300_X_RAIL_ALIGNMENT_SHIM',
                  (0, 1.2, -6.0))
    constrained_box(first.component, 'SK-1300-01_SHIM_OUTLINE',
                    'CBP-1300_SHIM_STOCK',
                    'x_rail_l', 'x_shim_w', 'x_shim_t')
    matches = [o for o in frame.occurrences if o.component == first.component]
    if len(matches) == 1:
        frame.occurrences.addExistingComponent(
            first.component, moved(0, 1.2, 6.0))
    print('rail shims', len([o for o in frame.occurrences
                             if o.component == first.component]))
