"""Four-cable planar-bed screening; not a released mechanism or controller.

SI calculations; fixed yaw, horizontal cables, and externally supported Z/tilt.
Includes full cable length Hessian, redundant tension allocation and rotor/drum
inertia. No cable elasticity, bearing drag, thermal/boat flex or motor electronics.
"""
import argparse, json, math, sys
from path_model import ROOT, parse
import smoothed_motion as sm


def geometry(p, anchors, attachments):
    delta = anchors[None, :, :] - p[:, None, :] - attachments[None, :, :]
    length = np.linalg.norm(delta, axis=2)
    u = delta / length[:, :, None]
    moment = attachments[None, :, 0] * u[:, :, 1] - attachments[None, :, 1] * u[:, :, 0]
    B = np.concatenate([u.transpose(0, 2, 1), moment[:, None, :]], axis=1)
    return length, u, B


def null_vector(B):
    # Cofactors give an exact right null vector for a full-rank 3x4 matrix.
    n = np.stack([(-1.) ** i * np.linalg.det(np.delete(B, i, axis=2)) for i in range(4)], axis=1)
    n *= np.where(n.sum(axis=1) < 0, -1., 1.)[:, None]
    return n / np.linalg.norm(n, axis=1)[:, None]


def audit_geometry(anchors, attachment, x=.032, y=.017):
    p = np.array([(a, b) for a in np.linspace(-x, x, 65) for b in np.linspace(-y, y, 35)])
    length, u, B = geometry(p, anchors, attachment)
    normalized = B.copy(); normalized[:, 2, :] /= .1
    s = np.linalg.svd(normalized, compute_uv=False)
    good = s[:, -1] > 1e-10
    n = null_vector(B[good]) if good.any() else np.empty((0, 4))
    return {'grid_points': len(p), 'rank_deficient_points': int((~good).sum()),
            'points_without_strictly_positive_self_stress': int(np.any(n <= 1e-8, axis=1).sum()),
            'minimum_normalized_singular_value': float(s[:, -1].min()),
            'maximum_normalized_condition_number': float(np.max(s[good, 0] / s[good, -1])) if good.any() else None,
            'length_range_mm': [float(length.min() * 1000), float(length.max() * 1000)]}


def allocate(p, v, a, anchors, attachment, radius, mass=.06, minimum_tension=5.):
    L, u, B = geometry(p, anchors, attachment)
    wrench = np.column_stack([mass * a, np.zeros(len(p))])
    z = np.linalg.solve(B @ B.transpose(0, 2, 1), wrench[..., None])
    base = (B.transpose(0, 2, 1) @ z)[..., 0]
    n = null_vector(B)
    assert np.all(n > 0), 'No positive tension nullspace on path'
    lower = np.max((minimum_tension - base) / n, axis=1)
    uv = np.sum(u * v[:, None, :], axis=2)
    ua = np.sum(u * a[:, None, :], axis=2)
    # q=-L/r: qddot=(u.a - (v.v-(u.v)^2)/L)/r.
    alpha = (ua - (np.sum(v*v, axis=1)[:, None] - uv*uv) / L) / radius
    rotor_J = 48e-6
    drum_J = .5 * .0075 * radius**2
    inertial = (rotor_J + drum_J) * alpha
    offset = radius * base + inertial
    slope = radius * n
    # Minimax absolute motor torque in one redundant coordinate. All slopes
    # positive; max(torque) increases, max(-torque) decreases. Balance them,
    # subject to every cable retaining >=5 N. No winding torque limit imposed.
    left = lower.copy(); right = lower + 100000.
    for _ in range(45):
        middle = (left + right) / 2
        torque = offset + slope * middle[:, None]
        more = torque.max(axis=1) < -torque.min(axis=1)
        left = np.where(more, middle, left); right = np.where(more, right, middle)
    tension = base + n * ((left + right) / 2)[:, None]
    torque = inertial + radius * tension
    residual = np.einsum('nij,nj->ni', B, tension) - wrench
    assert np.max(np.abs(residual)) < 1e-8
    assert tension.min() >= minimum_tension - 1e-8
    omega = uv / radius
    # Work balance independently checks signs and nonlinear coordinate terms.
    motor_power = np.sum(torque * omega, axis=1)
    required_power = mass * np.sum(a*v, axis=1) + (rotor_J + drum_J) * np.sum(alpha*omega, axis=1)
    assert np.max(np.abs(motor_power - required_power)) < 1e-6
    return {'radius_mm': radius * 1000,
            'peak_abs_motor_torque_Nm': np.max(np.abs(torque), axis=0).tolist(),
            'peak_motor_rpm': np.max(np.abs(omega), axis=0).tolist(),
            'peak_motor_rpm_units_note': 'Converted to rpm below',
            'minimum_cable_tension_N': float(tension.min()),
            'maximum_cable_tension_N': float(tension.max()),
            'sample_fraction_any_motor_above_2p2Nm': float(np.any(np.abs(torque) > 2.2, axis=1).mean()),
            'max_equilibrium_residual_N_or_Nm': float(np.max(np.abs(residual))),
            'max_power_balance_residual_W': float(np.max(np.abs(motor_power-required_power))),
            'peak_at_speed': [{'torque_Nm': float(torque[k, i]), 'rpm': float(omega[k, i] * 60 / (2*math.pi))}
                              for i in range(4) for k in [np.argmax(np.abs(torque[:, i]))]]}


def run(args):
    signs = np.array([[-1., -1.], [1., -1.], [1., 1.], [-1., 1.]])
    anchors = signs * [.15, .15]
    attachment = signs * [.095, .055]
    # Numerical derivative of cable length for an off-center, mixed-axis path.
    p0 = np.array([[.011, -.007]]); v0 = np.array([[1.3, -.7]]); a0 = np.array([[350., 210.]])
    L, u, B = geometry(p0, anchors, attachment)
    h = 1e-5
    plus = geometry(p0 + v0*h + .5*a0*h*h, anchors, attachment)[0]
    minus = geometry(p0 - v0*h + .5*a0*h*h, anchors, attachment)[0]
    analytic = -np.sum(u*a0[:, None, :], axis=2) + (np.sum(v0*v0, axis=1)[:, None] - np.sum(u*v0[:, None, :], axis=2)**2)/L
    derivative_error = float(np.abs((plus - 2*L + minus)/h**2 - analytic).max())
    assert derivative_error < .001
    from scipy.optimize import linprog
    allocation_checks = []
    for px, py, vx, vy, ax, ay in [(0,0,0,0,0,0), (.01,-.008,1.2,-.3,800,-600), (-.023,.012,-.8,1.4,-1900,1300)]:
        pcheck = np.array([[px,py]]); vcheck = np.array([[vx,vy]]); acheck = np.array([[ax,ay]])
        lc, uc, bc = geometry(pcheck, anchors, attachment)
        r = .025; jc = 48e-6 + .5*.0075*r*r
        uv = np.sum(uc*vcheck[:,None,:],axis=2)
        alpha = (np.sum(uc*acheck[:,None,:],axis=2)-(np.sum(vcheck*vcheck)-uv*uv)/lc)/r
        offset = jc*alpha[0]
        # Independent linear program: four tensions and maximum absolute torque.
        A = np.vstack([np.column_stack([r*np.eye(4),-np.ones(4)]), np.column_stack([-r*np.eye(4),-np.ones(4)])])
        lp = linprog([0,0,0,0,1], A_ub=A, b_ub=np.r_[-offset,offset],
            A_eq=np.column_stack([bc[0],np.zeros(3)]), b_eq=[.06*ax,.06*ay,0],
            bounds=[(5,None)]*4+[(0,None)],method='highs')
        assert lp.success
        actual = max(allocate(pcheck,vcheck,acheck,anchors,attachment,r)['peak_abs_motor_torque_Nm'])
        assert abs(actual-lp.fun)<1e-7,(actual,lp.fun)
        allocation_checks.append({'expected_from_linear_program_Nm':float(lp.fun),'nullspace_allocator_Nm':actual})
    raw = parse(ROOT/'slicing/cura-4.13.1-simplified/analysis.gcode')
    planned = sm.planned_moves(raw, 2400, 2000000, 500, 300)
    t, p, mask, layers, total = sm.sample(planned, args.dt)
    defs, _ = sm.load_smoothers()
    result = {'status': 'Cable mechanism screening, not a selected or validated printer',
              'dt_s': args.dt, 'moving_mass_kg': .06, 'minimum_tension_N': 5.,
              'anchors_mm': (anchors * 1000).tolist(), 'bed_attachment_mm': (attachment * 1000).tolist(),
              'working_xy_half_range_mm': [32., 17.], 'normalized_yaw_length_mm': 100.,
              'radial_layout': audit_geometry(anchors, signs * [.055, .055]),
              'rectangular_layout': audit_geometry(anchors, attachment),
              'length_second_derivative_max_error_m_s2': derivative_error,
              'independent_linear_program_checks': allocation_checks,
              'rpm_curve_reference_Nm': 2.2,
              'rpm_curve_reference_note': 'Constant comparison only, NOT verified available torque at each RPM/current/voltage.',
              'runs': []}
    center = (p.min(axis=0) + p.max(axis=0)) / 2
    for frequency in (200, 400, 800):
        sp, v, a, _, _ = sm.smooth(p, t, args.dt, defs.get_zv_smoother, frequency)
        # Bed displacement is opposite toolpath displacement. Origin shift
        # puts the path center below the fixed nozzle. Units become SI.
        bp = -(sp - center) / 1000; bv = -v/1000; ba = -a/1000
        for radius in (.025, .04, .06):
            row = allocate(bp, bv, ba, anchors, attachment, radius)
            row['peak_motor_rpm'] = [x*60/(2*math.pi) for x in row['peak_motor_rpm']]
            del row['peak_motor_rpm_units_note']
            row['smoother_frequency_Hz'] = frequency
            result['runs'].append(row)
            print('Hz', frequency, 'r', radius, 'peak torque', max(row['peak_abs_motor_torque_Nm']),
                  'peak tension', row['maximum_cable_tension_N'], flush=True)
    (ROOT/'engineering/cable-results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--numpy-dir'); ap.add_argument('--dt', type=float, default=.0001)
    args = ap.parse_args()
    if args.numpy_dir: sys.path.insert(0, args.numpy_dir)
    import numpy as np
    sm.np = np
    run(args)
