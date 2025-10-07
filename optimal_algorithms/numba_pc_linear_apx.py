import numpy as np
from numba import njit

# ------------------------------
# Manual rounding (faster + JIT-safe)
# ------------------------------
@njit(inline='always')
def round6(x):
    if x >= 0:
        return np.floor(x * 1e6 + 0.5) / 1e6
    else:
        return np.ceil(x * 1e6 - 0.5) / 1e6


# ------------------------------
# calculate_angle (Numba version)
# ------------------------------
@njit(fastmath=True)
def calculate_angle(point1, point2, point3, direction='+'):
    """
    Measures angle between three points in positive or negative direction.
    Same logic, optimized for Numba.
    """
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    angle1 = np.arctan2(y1 - y2, x1 - x2)
    angle2 = np.arctan2(y3 - y2, x3 - x2)
    angle_diff = angle2 - angle1

    if angle_diff < 0:
        angle_diff += 2 * np.pi
    if direction == '-':
        angle_diff = 2 * np.pi - angle_diff

    return round6(angle_diff)


# ------------------------------
# find_intersection (Numba version)
# ------------------------------
@njit(fastmath=True)
def find_intersection(line1_start, line1_end, line2_start, line2_end):
    """
    Returns intersection of two lines defined by their endpoints.
    Same logic, optimized for Numba.
    """
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end

    denominator = (x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1)
    if np.abs(denominator) < 1e-10:
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return (round6(x), round6(y))

    x = ((x2 * y1 - x1 * y2) * (x4 - x3) - (x4 * y3 - x3 * y4) * (x2 - x1)) / denominator
    y = ((x2 * y1 - x1 * y2) * (y4 - y3) - (x4 * y3 - x3 * y4) * (y2 - y1)) / denominator

    return (round6(x), round6(y))


# ------------------------------
# reconstruct_piecewise_function (Numba version)
# ------------------------------
@njit(fastmath=True)
def reconstruct_piecewise_function(pc_linear_fx):
    """
    Reconstructs piecewise linear function values between pivot points.
    Same logic, optimized for Numba.
    """
    n = len(pc_linear_fx)
    if n <= 1:
        return np.empty(0, dtype=np.float64)

    # # Sort by x
    # idx = np.argsort(pc_linear_fx[:, 0])
    # pivot_points = pc_linear_fx[idx]

    # Preallocate output
    max_len = int(pc_linear_fx[-1, 0] - pc_linear_fx[0, 0]) + 2
    y_values = np.empty(max_len, dtype=np.float64)
    out_i = 0

    for i in range(n - 1):
        x1, y1 = pc_linear_fx[i]
        x2, y2 = pc_linear_fx[i + 1]

        if x2 == x1:
            continue
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        xi = int(x1)
        while xi < int(x2):
            y_values[out_i] = slope * xi + intercept
            out_i += 1
            xi += 1

    y_values[out_i] = pc_linear_fx[-1, 1]
    return y_values[:out_i + 1]

def numba_approximate_pc_linear_fx(pc_linear_fx, w):
    y = reconstruct_piecewise_function(np.array(pc_linear_fx, dtype=np.float64))
    y = np.array(y)
    x = np.arange(pc_linear_fx[0][0], pc_linear_fx[0][0] + len(y))
    y = np.array([round6(v) for v in y])

    if len(y) <= 2:
        optimal_pc_linear_fx = np.array(pc_linear_fx)
        optimal_num_pieces = len(pc_linear_fx) - 1
        given_num_pieces = optimal_num_pieces
        return optimal_pc_linear_fx, optimal_num_pieces, given_num_pieces
    if abs(w) < 1e-10:  # Treat as zero
        if len(y) > 1:
            dx = x[-1] - x[0]
            if abs(dx) < 1e-10:
                return np.array(pc_linear_fx), len(pc_linear_fx) - 1, len(pc_linear_fx) - 1
            slope = (y[-1] - y[0]) / dx
            intercept = y[0] - slope * x[0]
            deviations = np.abs(y - (slope * x + intercept))
            if np.all(deviations <= 1e-10):
                return np.array([(x[0], y[0]), (x[-1], y[-1])]), 1, len(pc_linear_fx) - 1
            else:
                return np.array(pc_linear_fx), len(pc_linear_fx) - 1, len(pc_linear_fx) - 1
        else:
            return np.array(pc_linear_fx), len(pc_linear_fx) - 1, len(pc_linear_fx) - 1

    # Rest unchanged — now calls Numba-accelerated helpers
    p_plus = (x[0], y[0] + w)
    l_plus = (x[0], y[0] + w)
    r_plus = (x[1], y[1] + w)
    s_plus = {(x[0], y[0] + w): (x[1], y[1] + w)}
    t_plus = {(x[1], y[1] + w): (x[0], y[0] + w)}
    p_minus = (x[0], y[0] - w)
    l_minus = (x[0], y[0] - w)
    r_minus = (x[1], y[1] - w)
    s_minus = {(x[0], y[0] - w): (x[1], y[1] - w)}
    t_minus = {(x[1], y[1] - w): (x[0], y[0] - w)}
    q = []
    i = 2
    while i < len(y):
        p = (x[i - 1], y[i - 1] + w)
        p_i_plus = (x[i], y[i] + w)
        while (p != p_plus) and (p in t_plus) and calculate_angle(p_i_plus, p, t_plus[p], '+') > np.pi:
            p = t_plus[p]
        s_plus[p] = p_i_plus
        t_plus[p_i_plus] = p

        p = (x[i - 1], y[i - 1] - w)
        p_i_minus = (x[i], y[i] - w)
        while (p != p_minus) and (p in t_minus) and calculate_angle(p_i_minus, p, t_minus[p], '-') > np.pi:
            p = t_minus[p]
        s_minus[p] = p_i_minus
        t_minus[p_i_minus] = p

        if calculate_angle(p_i_plus, l_plus, r_minus, '+') < np.pi:
            q.append((find_intersection(l_plus, r_minus, p_plus, p_minus), l_plus, r_minus, p_plus, p_minus))
            p_minus = r_minus
            p_plus = find_intersection(l_plus, r_minus, (x[i - 1], y[i - 1] + w), p_i_plus)
            s_plus[p_plus] = p_i_plus
            t_plus[p_i_plus] = p_plus
            r_plus = p_i_plus
            r_minus = p_i_minus
            l_plus = p_plus
            l_minus = p_minus
            while l_minus in s_minus and calculate_angle(l_minus, r_plus, s_minus[l_minus], '-') < np.pi:
                l_minus = s_minus[l_minus]
        elif calculate_angle(p_i_minus, l_minus, r_plus, '-') < np.pi:
            q.append((find_intersection(l_minus, r_plus, p_minus, p_plus), l_minus, r_plus, p_minus, p_plus))
            p_plus = r_plus
            p_minus = find_intersection(l_minus, r_plus, (x[i - 1], y[i - 1] - w), p_i_minus)
            s_minus[p_minus] = p_i_minus
            t_minus[p_i_minus] = p_minus
            r_minus = p_i_minus
            r_plus = p_i_plus
            l_minus = p_minus
            l_plus = p_plus
            while l_plus in s_plus and calculate_angle(l_plus, r_minus, s_plus[l_plus], '+') < np.pi:
                l_plus = s_plus[l_plus]
        else:
            if calculate_angle(p_i_plus, l_minus, r_plus, '+') < np.pi:
                r_plus = p_i_plus
                while l_minus in s_minus and calculate_angle(p_i_plus, l_minus, s_minus[l_minus], '+') < np.pi:
                    l_minus = s_minus[l_minus]

            if calculate_angle(p_i_minus, l_plus, r_minus, '-') < np.pi:
                r_minus = p_i_minus
                while l_plus in s_plus and calculate_angle(p_i_minus, l_plus, s_plus[l_plus], '-') < np.pi:
                    l_plus = s_plus[l_plus]
        i += 1

    a = find_intersection(l_plus, r_minus, p_plus, p_minus)
    b = find_intersection(l_minus, r_plus, p_minus, p_plus)
    if a is None or b is None:
        return np.array([])
    p = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    q.append((p, r_minus, r_plus, p_minus, p_plus))

    end_a = find_intersection(p, r_plus, p_i_minus, p_i_plus)
    end_b = find_intersection(p, r_minus, p_i_minus, p_i_plus)
    if end_a is not None and end_b is not None:
        end = ((end_a[0] + end_b[0]) / 2, (end_a[1] + end_b[1]) / 2)
        q.append((end, (None, None), (None, None), p_i_minus, p_i_plus))

    optimal_pc_linear_fx = np.array([o[0] for o in q])
    optimal_num_pieces = len(optimal_pc_linear_fx) - 1
    given_num_pieces = len(pc_linear_fx) - 1
    return optimal_pc_linear_fx, optimal_num_pieces, given_num_pieces
