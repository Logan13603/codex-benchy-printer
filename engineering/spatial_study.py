"""Stroke-preserving spatial screen of the checkpoint-006 smoothed command.

No printer is controlled. Distances are between command centerlines, not bead
surfaces or a finished part. Each uninterrupted same-role/layer extrusion stroke
is compared only to itself, so nearby infill cannot hide a missing perimeter.
Requires NumPy and SciPy; --numpy-dir accepts an optional dependency directory.
"""
import argparse, json, sys, math, hashlib
from pathlib import Path
from path_model import ROOT, parse, summarize
import smoothed_motion as sm


def strokes(planned, source):
    result = []; clock = 0.; previous = None
    assert len(planned) == len(source)
    for m, raw in zip(planned, source):
        total = m.accel_t + m.cruise_t + m.decel_t
        role = (raw.role, raw.z) if m.cbp_deposit else None
        if role is not None:
            if role != previous:
                result.append({'role': role[0], 'z': role[1], 'start': clock,
                               'points': [np.array(m.start_pos[:2])], 'volume': 0.})
            result[-1]['points'].append(np.array(m.end_pos[:2]))
            result[-1]['end'] = clock + total
            result[-1]['volume'] += raw.e * sm.AF
        previous = role
        clock += total
    return result


def resample_polyline(vertices, spacing):
    pieces = []
    for p, q in zip(vertices[:-1], vertices[1:]):
        n = max(1, math.ceil(float(np.linalg.norm(q - p)) / spacing))
        pieces.append(p + np.arange(n)[:, None] / n * (q - p))
    return np.vstack(pieces + [np.asarray(vertices[-1])[None, :]])


def polyline_bounds(a, b):
    # For piecewise-linear paths, every segment lies within half its length
    # of an endpoint. Nearest-neighbor queries are exact (eps=0).
    da = cKDTree(b).query(a, eps=0)[0]
    db = cKDTree(a).query(b, eps=0)[0]
    gap_a = np.linalg.norm(np.diff(a, axis=0), axis=1).max(initial=0.) / 2
    gap_b = np.linalg.norm(np.diff(b, axis=0), axis=1).max(initial=0.) / 2
    return {
        'ref_to_smoothed_lower_mm': max(0., float(da.max() - gap_b)),
        'ref_to_smoothed_upper_mm': float(da.max() + gap_a),
        'smoothed_to_ref_lower_mm': max(0., float(db.max() - gap_a)),
        'smoothed_to_ref_upper_mm': float(db.max() + gap_b),
    }


def spatial_metrics(groups, t, shaped, spacing):
    rows = []; total_raw = 0.; total_shaped = 0.
    for index, group in enumerate(groups):
        a = resample_polyline(group['points'], spacing)
        lo, hi = np.searchsorted(t, [group['start'], group['end']])
        # Include exact stroke times, interpolating only the sampled command.
        endpoints = np.column_stack([np.interp([group['start'], group['end']], t, shaped[:, k]) for k in (0, 1)])
        b = np.vstack([endpoints[0], shaped[lo:hi], endpoints[1]])
        raw_length = float(np.linalg.norm(np.diff(a, axis=0), axis=1).sum())
        new_length = float(np.linalg.norm(np.diff(b, axis=0), axis=1).sum())
        total_raw += raw_length; total_shaped += new_length
        rows.append({'stroke': index, 'role': group['role'], 'layer_z_mm': group['z'],
                     'raw_length_mm': raw_length, 'smoothed_length_mm': new_length,
                     'unchanged_volume_length_ratio': raw_length / new_length if new_length else None,
                     **polyline_bounds(a, b)})
    keys = [k for k in rows[0] if k.endswith('_mm') and ('lower' in k or 'upper' in k)]
    by_role = {}
    for role in sorted(set(g['role'] for g in groups)):
        selected = [r for r in rows if r['role'] == role]
        by_role[role] = {k: max(r[k] for r in selected) for k in keys}
    worst = sorted(rows, key=lambda r: max(r['ref_to_smoothed_lower_mm'], r['smoothed_to_ref_lower_mm']), reverse=True)[:12]
    return {'stroke_count': len(groups), 'raw_deposition_length_mm': total_raw,
            'smoothed_deposition_interval_length_mm': total_shaped,
            'unchanged_volume_global_length_ratio': total_raw / total_shaped,
            'by_role': by_role, 'worst_strokes': worst}, rows


def verify():
    # Offset lines have an exact 0.3 mm Hausdorff distance, including interiors.
    a = np.column_stack([np.linspace(0, 10, 101), np.zeros(101)])
    b = a + [0., .3]
    r = polyline_bounds(a, b)
    for direction in ('ref_to_smoothed', 'smoothed_to_ref'):
        assert r[direction + '_lower_mm'] <= .3 <= r[direction + '_upper_mm']
    # A shortcut deleting a right angle must not be hidden by along-path timing.
    a = resample_polyline(np.array([[0., 0.], [1., 0.], [1., 1.]]), .01)
    b = resample_polyline(np.array([[0., 0.], [1., 1.]]), .01)
    r = polyline_bounds(a, b)
    assert r['ref_to_smoothed_lower_mm'] <= 1 / math.sqrt(2) <= r['ref_to_smoothed_upper_mm']
    assert r['smoothed_to_ref_lower_mm'] <= .5 <= r['smoothed_to_ref_upper_mm']
    return ['parallel offset lines', 'right-angle shortcut, both directions']


def run(args):
    source = ROOT / 'slicing/cura-4.13.1-simplified/analysis.gcode'
    raw = parse(source)
    planned = sm.planned_moves(raw, 2400, 2000000, 500, 300)
    groups = strokes(planned, raw)
    t, p, mask, layers, total = sm.sample(planned, args.dt)
    assert abs(sum(g['volume'] for g in groups) - summarize(raw)['volume_mm3']) < 1e-6
    defs, metadata = sm.load_smoothers()
    result = {'status': 'Command-centerline spatial screen; no physical quality certification',
              'gcode_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'kalico_commit': metadata['commit'], 'dt_s': args.dt,
              'reference_maximum_sample_spacing_mm': args.spacing,
              'base_time_s': total, 'analytic_checks': verify(), 'runs': []}
    figure_data = []
    for frequency in args.frequencies:
        shaped, v, a, T, mu = sm.smooth(p, t, args.dt, defs.get_zv_smoother, frequency)
        metrics, rows = spatial_metrics(groups, t, shaped, args.spacing)
        row = {'smoother': 'smooth_zv', 'frequency_Hz': frequency,
               'duration_ms': T * 1000,
               'torque_Nm_per_motor': sm.metrics(p, mask, shaped, v, a)['max_abs_inertial_torque_Nm_per_motor'],
               **metrics}
        result['runs'].append(row)
        # Retain one closed upper-boat outer stroke across every frequency.
        choices = [i for i, g in enumerate(groups) if g['role'] == 'WALL-OUTER' and g['z'] == 46.]
        if choices:
            i = max(choices, key=lambda i: rows[i]['raw_length_mm'])
            g = groups[i]; lo, hi = np.searchsorted(t, [g['start'], g['end']])
            figure_data.append((frequency, np.array(g['points']), shaped[lo:hi:2].copy(), row))
        print('Hz', frequency, 'outer', row['by_role']['WALL-OUTER'],
              'length ratio', row['unchanged_volume_global_length_ratio'], flush=True)
    (ROOT / 'engineering' / args.output).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    if args.figure and figure_data:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, len(figure_data), figsize=(4 * len(figure_data), 5.2), squeeze=False)
        for ax, (frequency, original, shaped, row) in zip(axes.flat, figure_data):
            ax.plot(original[:, 0], original[:, 1], color='#343a40', lw=1.4, label='Original centerline')
            ax.plot(shaped[:, 0], shaped[:, 1], color='#c54c35', lw=1, label='Smoothed command')
            ax.set_title(f'{frequency} Hz | Z = 46 mm')
            ax.set_aspect('equal'); ax.grid(alpha=.2); ax.set_xlabel('X (mm, relative origin)')
        axes[0, 0].set_ylabel('Y (mm, relative origin)'); axes[0, 0].legend(fontsize=8)
        fig.suptitle('Chimney perimeter: smoothing changes spatial geometry', fontsize=14)
        fig.text(.5, .015, 'Calculated commands only. Assumed limits are not validated hardware settings.', ha='center', fontsize=10)
        fig.tight_layout(rect=[0, .09, 1, .94]); fig.savefig(ROOT/'engineering/figures/spatial-smoothing.png', dpi=170)
        plt.close(fig)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--numpy-dir')
    ap.add_argument('--dt', type=float, default=.000025)
    ap.add_argument('--spacing', type=float, default=.04)
    ap.add_argument('--frequencies', nargs='+', type=int, default=[100, 200, 400, 800])
    ap.add_argument('--output', default='spatial-results.json'); ap.add_argument('--figure', action='store_true')
    args = ap.parse_args()
    if args.numpy_dir: sys.path.insert(0, args.numpy_dir)
    import numpy as np
    from scipy.spatial import cKDTree
    sm.np = np
    run(args)
