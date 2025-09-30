import numpy as np
from scipy.optimize import linprog
import bisect
#I think so it's an optimal algorithm
def interpolate_f(x, points):
    if not points:
        raise ValueError("No points provided")
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    if x <= x_vals[0]:
        return y_vals[0]
    if x >= x_vals[-1]:
        return y_vals[-1]
    idx = bisect.bisect_left(x_vals, x) - 1
    if idx < 0:
        idx = 0
    x_l, y_l = x_vals[idx], y_vals[idx]
    x_r, y_r = x_vals[idx + 1], y_vals[idx + 1]
    t = (x - x_l) / (x_r - x_l)
    return y_l + t * (y_r - y_l)

def get_end_interval(xs, xe, lo_start, hi_start, points, epsilon):
    if xs >= xe:
        return None, None
    dx = xe - xs
    if dx <= 0:
        return None, None
    x_list = [p[0] for p in points]
    constr_xs = [xk for xk in x_list if xs <= xk <= xe]
    if xs not in constr_xs:
        constr_xs.append(xs)
    if xe not in constr_xs:
        constr_xs.append(xe)
    constr_xs = sorted(set(constr_xs))
    constr_ys = [interpolate_f(xc, points) for xc in constr_xs]
    num_k = len(constr_xs)
    num_cons_base = 2 * num_k
    num_cons = num_cons_base + 2
    A_ub = np.zeros((num_cons, 2))
    b_ub = np.zeros(num_cons)
    cons_idx = 0
    for ii in range(num_k):
        t = (constr_xs[ii] - xs) / dx
        A_ub[cons_idx, 0] = 1 - t
        A_ub[cons_idx, 1] = t
        b_ub[cons_idx] = constr_ys[ii] + epsilon
        cons_idx += 1
        A_ub[cons_idx, 0] = -(1 - t)
        A_ub[cons_idx, 1] = -t
        b_ub[cons_idx] = -(constr_ys[ii] - epsilon)
        cons_idx += 1
    A_ub[cons_idx, 0] = 1.0
    A_ub[cons_idx, 1] = 0.0
    b_ub[cons_idx] = hi_start
    cons_idx += 1
    A_ub[cons_idx, 0] = -1.0
    A_ub[cons_idx, 1] = 0.0
    b_ub[cons_idx] = -lo_start
    c_feas = np.array([0.0, 0.0])
    res_feas = linprog(c_feas, A_ub=A_ub, b_ub=b_ub, bounds=(None, None), method='highs')
    if not res_feas.success:
        return None, None
    c_min = np.array([0.0, 1.0])
    res_min = linprog(c_min, A_ub=A_ub, b_ub=b_ub, bounds=(None, None), method='highs')
    if not res_min.success:
        return None, None
    lo_end = res_min.fun
    c_max = np.array([0.0, -1.0])
    res_max = linprog(c_max, A_ub=A_ub, b_ub=b_ub, bounds=(None, None), method='highs')
    if not res_max.success:
        return None, None
    hi_end = -res_max.fun
    if lo_end > hi_end + 1e-8:
        return None, None
    return lo_end, hi_end

def binary_search_max_xe(xs, xn, lo_start, hi_start, points, epsilon):
    low = xs
    high = xn
    for _ in range(100):
        mid = (low + high) / 2
        lo_end, hi_end = get_end_interval(xs, mid, lo_start, hi_start, points, epsilon)
        if lo_end is not None and lo_end <= hi_end + 1e-8:
            low = mid
        else:
            high = mid
    return low

def reconstruct_optimal_points(points, kept_x, epsilon):
    num_kept = len(kept_x)
    if num_kept < 2:
        if num_kept == 1:
            y_prime = interpolate_f(kept_x[0], points)
            return [(kept_x[0], y_prime + 0.0)], 0  # Adjust if needed
        return [], 0
    A_ub_list = []
    b_ub_list = []
    for r in range(num_kept - 1):
        xs_r = kept_x[r]
        xe_r = kept_x[r + 1]
        dx = xe_r - xs_r
        if dx <= 0:
            continue
        x_list = [p[0] for p in points if xs_r <= p[0] <= xe_r]
        constr_xs = list(set(x_list + [xs_r, xe_r]))
        constr_xs.sort()
        constr_ys = [interpolate_f(xc, points) for xc in constr_xs]
        for ii in range(len(constr_xs)):
            t = (constr_xs[ii] - xs_r) / dx
            row_upper = np.zeros(num_kept)
            row_upper[r] = 1 - t
            row_upper[r + 1] = t
            A_ub_list.append(row_upper)
            b_ub_list.append(constr_ys[ii] + epsilon)
            row_lower = np.zeros(num_kept)
            row_lower[r] = -(1 - t)
            row_lower[r + 1] = -t
            A_ub_list.append(row_lower)
            b_ub_list.append(-(constr_ys[ii] - epsilon))
    if not A_ub_list:
        y_primes = [interpolate_f(kx, points) for kx in kept_x]
        return [(kept_x[i], y_primes[i]) for i in range(num_kept)]
    A_ub = np.vstack(A_ub_list)
    b_ub = np.array(b_ub_list)
    c = np.zeros(num_kept)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=(None, None), method='highs')
    if res.success:
        y_primes = res.x
        return [(kept_x[i], y_primes[i]) for i in range(num_kept)]
    else:
        return points

def free_knot_LP(pc_linear_fx, epsilon):
    points = pc_linear_fx
    m = len(points)
    if m < 2:
        return points, 0, 0
    given_num_pieces = m - 1
    x0 = points[0][0]
    xn = points[-1][0]
    y0 = points[0][1]
    lo_start = y0 - epsilon
    hi_start = y0 + epsilon
    kept_x = [x0]
    xs = x0
    while xs < xn - 1e-8:
        max_reachable = binary_search_max_xe(xs, xn, lo_start, hi_start, points, epsilon)
        if max_reachable >= xn - 1e-8:
            if abs(kept_x[-1] - xn) > 1e-8:
                kept_x.append(xn)
            break
        elif max_reachable <= xs + 1e-8:
            return points, given_num_pieces, given_num_pieces
        else:
            kept_x.append(max_reachable)
            lo_end, hi_end = get_end_interval(xs, max_reachable, lo_start, hi_start, points, epsilon)
            xs = max_reachable
            lo_start = lo_end
            hi_start = hi_end
    optimal_pc_linear_fx = reconstruct_optimal_points(points, kept_x, epsilon)
    optimal_num_pieces = len(optimal_pc_linear_fx) - 1 if len(optimal_pc_linear_fx) > 1 else 0
    if len(optimal_pc_linear_fx) != len(kept_x):
        optimal_pc_linear_fx = points
        optimal_num_pieces = given_num_pieces
    return optimal_pc_linear_fx, optimal_num_pieces, given_num_pieces