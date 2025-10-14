from numba import cuda, float64, int32, boolean

@cuda.jit(device=True, inline=True)
def distance_point_to_line_segment_dev(x0, y0, x1, y1, x2, y2):
    # Same as CPU version, rewritten for CUDA math
    if x1 == x2:
        return abs(y0 - y1)
    if x0 < x1 or x0 > x2:
        return 1e20  # effectively infinity
    y_line = y1 + (y2 - y1) * (x0 - x1) / (x2 - x1)
    d = y0 - y_line
    return abs(d)


@cuda.jit(device=True)
def greedy_approximation_device(points_x, points_y, n, epsilon,
                                out_x, out_y, max_out):
    """
    Greedy algorithm for piecewise linear approximation under L∞ (CUDA device version).
    Returns number of output pivots.
    """
    if n <= 0:
        return 0

    given_num_pieces = 0 if n <= 1 else n - 1
    if n <= 2:
        m = n
        if m > max_out:
            return 0
        for i in range(m):
            out_x[i] = points_x[i]
            out_y[i] = points_y[i]
        return m

    # Initialize
    result_count = 0
    out_x[result_count] = points_x[0]
    out_y[result_count] = points_y[0]
    result_count += 1

    current_start = 0

    while current_start < n - 1:
        farthest_valid = current_start + 1

        # Try to extend segment as far as epsilon allows
        end_idx = current_start + 2
        while end_idx < n:
            x1 = points_x[current_start]
            y1 = points_y[current_start]
            x2 = points_x[end_idx]
            y2 = points_y[end_idx]

            valid_segment = True

            # Check all intermediate points
            for mid_idx in range(current_start + 1, end_idx):
                x0 = points_x[mid_idx]
                y0 = points_y[mid_idx]
                if distance_point_to_line_segment_dev(x0, y0, x1, y1, x2, y2) > epsilon:
                    valid_segment = False
                    break

            if valid_segment:
                farthest_valid = end_idx
                end_idx += 1
            else:
                break  # cannot extend further

        # Commit the farthest feasible endpoint
        if result_count < max_out:
            out_x[result_count] = points_x[farthest_valid]
            out_y[result_count] = points_y[farthest_valid]
            result_count += 1
        else:
            return 0  # overflow

        current_start = farthest_valid

    return result_count  # number of pivots

@cuda.jit(device=True, inline=True)
def is_valid_segment_dev(points_x, points_y, start_idx, end_idx, epsilon):
    """
    Check if all intermediate points between start_idx and end_idx
    stay within epsilon tolerance (device version).
    """
    if end_idx <= start_idx + 1:
        return True

    x1 = points_x[start_idx]
    y1 = points_y[start_idx]
    x2 = points_x[end_idx]
    y2 = points_y[end_idx]

    for i in range(start_idx + 1, end_idx):
        x0 = points_x[i]
        y0 = points_y[i]
        d = distance_point_to_line_segment_dev(x0, y0, x1, y1, x2, y2)
        if d > epsilon:
            return False
    return True

#use default lookahead = 5
@cuda.jit(device=True)
def improved_greedy_with_lookahead_dev(points_x, points_y, n, epsilon, lookahead,
                                       out_x, out_y, max_out):
    """
    GPU-friendly greedy approximation with limited lookahead.
    Inputs:
        points_x, points_y : arrays of n points (strictly increasing x)
        epsilon            : tolerance
        lookahead          : integer (how many steps to peek ahead)
        out_x, out_y       : output buffers for selected breakpoints
        max_out            : maximum capacity of output buffers
    Returns:
        count of output points (result length)
    """

    if n <= 2:
        m = n
        if m > max_out:
            return 0
        for i in range(m):
            out_x[i] = points_x[i]
            out_y[i] = points_y[i]
        return m

    out_x[0] = points_x[0]
    out_y[0] = points_y[0]
    out_count = 1
    current_start = 0

    while current_start < n - 1:
        best_end = current_start + 1
        max_look = current_start + lookahead + 1
        if max_look > n:
            max_look = n

        for end_idx in range(current_start + 2, max_look):
            if is_valid_segment_dev(points_x, points_y, current_start, end_idx, epsilon):
                best_end = end_idx

        if out_count < max_out:
            out_x[out_count] = points_x[best_end]
            out_y[out_count] = points_y[best_end]
            out_count += 1
        else:
            # overflow protection — truncate gracefully
            return out_count

        current_start = best_end

    return out_count

@cuda.jit(device=True)
def douglas_peucker_device(points_x, points_y, n, epsilon,
                           out_x, out_y, max_out):
    """
    GPU-compatible Douglas–Peucker line simplification.
    Uses an explicit stack instead of recursion.
    Returns number of output pivots.
    """
    if n <= 2:
        # just copy input points
        count = n
        if count > max_out:
            count = max_out
        for i in range(count):
            out_x[i] = points_x[i]
            out_y[i] = points_y[i]
        return count

    # --- Explicit stack: store (start_idx, end_idx) pairs
    STACK_MAX = 64
    stack_start = cuda.local.array(STACK_MAX, dtype=int32)
    stack_end   = cuda.local.array(STACK_MAX, dtype=int32)
    stack_ptr = 0

    stack_start[0] = 0
    stack_end[0] = n - 1
    stack_ptr = 1

    # --- Keep mask for which points to retain
    KEEP = cuda.local.array(256, dtype=boolean)  # supports up to 256 points
    for i in range(n):
        KEEP[i] = False
    KEEP[0] = True
    KEEP[n - 1] = True

    # --- Main iterative loop
    while stack_ptr > 0:
        stack_ptr -= 1
        start_idx = stack_start[stack_ptr]
        end_idx   = stack_end[stack_ptr]

        if end_idx <= start_idx + 1:
            continue

        # find farthest point
        max_dist = 0.0
        max_idx = start_idx
        x1 = points_x[start_idx]
        y1 = points_y[start_idx]
        x2 = points_x[end_idx]
        y2 = points_y[end_idx]
        for i in range(start_idx + 1, end_idx):
            d = distance_point_to_line_segment_dev(points_x[i], points_y[i],
                                                   x1, y1, x2, y2)
            if d > max_dist:
                max_dist = d
                max_idx = i

        if max_dist > epsilon and stack_ptr + 2 < STACK_MAX:
            KEEP[max_idx] = True
            # push subsegments
            stack_start[stack_ptr] = start_idx
            stack_end[stack_ptr]   = max_idx
            stack_ptr += 1
            stack_start[stack_ptr] = max_idx
            stack_end[stack_ptr]   = end_idx
            stack_ptr += 1

    # --- Collect output points
    count = 0
    for i in range(n):
        if KEEP[i]:
            if count >= max_out:
                break
            out_x[count] = points_x[i]
            out_y[count] = points_y[i]
            count += 1

    return count


# =====================================================
# Helper: compute y on line (same as _y_on_line)
# =====================================================
@cuda.jit(device=True, inline=True)
def y_on_line_dev(x, x1, y1, x2, y2):
    if x2 == x1:
        return y1  # degenerate safeguard
    t = (x - x1) / (x2 - x1)
    return y1 + t * (y2 - y1)


# =====================================================
# Feasibility check (fixed endpoints)
# =====================================================
@cuda.jit(device=True, inline=True)
def feasible_fixed_endpoints_dev(points_x, points_y, i, j, eps):
    x1 = points_x[i]
    y1 = points_y[i]
    x2 = points_x[j]
    y2 = points_y[j]
    if x2 == x1:
        return False
    for k in range(i + 1, j):
        xk = points_x[k]
        yk = points_y[k]
        yhat = y_on_line_dev(xk, x1, y1, x2, y2)
        if abs(yk - yhat) > eps:
            return False
    return True


# =====================================================
# Shortest Path Dynamic Programming (device version)
# =====================================================
@cuda.jit(device=True)
def shortest_path_dp_device(points_x, points_y, n, eps,
                            out_x, out_y, max_out):
    """
    GPU-compatible version of shortest-path DP (optimal segmentation).
    Returns number of output pivots.
    """
    INF = 10**9
    MAX_N = 128  # supports up to 128 input points

    # dp and prev arrays
    dp = cuda.local.array(MAX_N, dtype=int32)
    prev = cuda.local.array(MAX_N, dtype=int32)

    for i in range(MAX_N):
        dp[i] = INF
        prev[i] = -1

    dp[0] = 0

    # === Main DP ===
    for i in range(n):
        if dp[i] == INF:
            continue
        for j in range(i + 1, n):
            if feasible_fixed_endpoints_dev(points_x, points_y, i, j, eps):
                if dp[i] + 1 < dp[j]:
                    dp[j] = dp[i] + 1
                    prev[j] = i

    # === Reconstruct path ===
    if dp[n - 1] == INF:
        # no feasible solution → copy input
        count = n if n < max_out else max_out
        for i in range(count):
            out_x[i] = points_x[i]
            out_y[i] = points_y[i]
        return count

    # Collect indices backward
    idx_buf = cuda.local.array(MAX_N, dtype=int32)
    idx_len = 0
    cur = n - 1
    while cur != -1 and idx_len < MAX_N:
        idx_buf[idx_len] = cur
        idx_len += 1
        cur = prev[cur]

    # reverse indices
    for i in range(idx_len // 2):
        tmp = idx_buf[i]
        idx_buf[i] = idx_buf[idx_len - 1 - i]
        idx_buf[idx_len - 1 - i] = tmp

    # write points to output
    count = idx_len
    if count > max_out:
        count = max_out
    for i in range(count):
        out_x[i] = points_x[idx_buf[i]]
        out_y[i] = points_y[idx_buf[i]]

    return count



import math

EPSX = 1e-9

# ------------------------------
# Small helpers (device)
# ------------------------------
@cuda.jit(device=True, inline=True)
def round6_dev(x):
    if x >= 0.0:
        return math.floor(x * 1e6 + 0.5) / 1e6
    else:
        return math.ceil(x * 1e6 - 0.5) / 1e6

@cuda.jit(device=True, inline=True)
def calculate_angle_dev(x1, y1, x2, y2, x3, y3, direction_plus):
    # angle at (x2,y2) from (x1,y1)->(x2,y2)->(x3,y3)
    a1 = math.atan2(y1 - y2, x1 - x2)
    a2 = math.atan2(y3 - y2, x3 - x2)
    diff = a2 - a1
    if diff < 0.0:
        diff += 2.0 * math.pi
    if not direction_plus:
        diff = 2.0 * math.pi - diff
    return round6_dev(diff)

@cuda.jit(device=True, inline=True)
def find_intersection_dev(x1, y1, x2, y2, x3, y3, x4, y4, out_xy):
    denom = (x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1)
    if abs(denom) < 1e-10:
        out_xy[0] = round6_dev(0.5 * (x1 + x2))
        out_xy[1] = round6_dev(0.5 * (y1 + y2))
        return False
    numx = (x2 * y1 - x1 * y2) * (x4 - x3) - (x4 * y3 - x3 * y4) * (x2 - x1)
    numy = (x2 * y1 - x1 * y2) * (y4 - y3) - (x4 * y3 - x3 * y4) * (y2 - y1)
    out_xy[0] = round6_dev(numx / denom)
    out_xy[1] = round6_dev(numy / denom)
    return True

@cuda.jit(device=True)
def reconstruct_piecewise_function_dev(pcx, pcy, n_pivots, ybuf, cap_ybuf, x0_out):
    # Reconstruct y on integer grid from pivot polyline
    if n_pivots <= 1:
        x0_out[0] = 0.0
        return 0

    start_x = int(pcx[0])
    out_i = 0

    for i in range(n_pivots - 1):
        x1 = pcx[i];     y1 = pcy[i]
        x2 = pcx[i+1];   y2 = pcy[i+1]
        if x2 == x1:
            continue
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        xi = int(x1)
        x2i = int(x2)
        while xi < x2i and out_i < cap_ybuf:
            ybuf[out_i] = slope * xi + intercept
            out_i += 1
            xi += 1
        if out_i >= cap_ybuf:
            break

    if out_i < cap_ybuf:
        ybuf[out_i] = pcy[n_pivots - 1]
        out_i += 1

    x0_out[0] = float(start_x)
    return out_i

@cuda.jit(device=True, inline=True)
def append_strict_dev(q_xy, q_sz_ptr, q_cap, x, y):
    # q_xy holds pairs: [x0,y0, x1,y1, ...]
    q_sz = q_sz_ptr[0]
    if q_sz == 0:
        if q_cap >= 2:
            q_xy[0] = x; q_xy[1] = y
            q_sz_ptr[0] = 2
        return
    last_x = q_xy[q_sz - 2]
    if x <= last_x + EPSX:
        return
    if q_sz + 2 <= q_cap:
        q_xy[q_sz] = x; q_xy[q_sz + 1] = y
        q_sz_ptr[0] = q_sz + 2

@cuda.jit(device=True, inline=True)
def clip_to_band_dev(x, y, pcx, pcy, n_pivots, w, out_xy):
    # If x matches a pivot x (within tol), clamp y into [oy-w, oy+w]
    matched = False
    oy = 0.0
    for i in range(n_pivots):
        if abs(x - pcx[i]) < 1e-9:
            oy = pcy[i]
            matched = True
            break
    if matched:
        ymin = oy - w
        ymax = oy + w
        if y < ymin: y = ymin
        if y > ymax: y = ymax
    out_xy[0] = x
    out_xy[1] = y

@cuda.jit(device=True, inline=True)
def is_segment_feasible_dev(p1x, p1y, p2x, p2y, pcx, pcy, n_pivots, w):
    # Check segment lies within ±w band relative to original pivots
    x1 = p1x; y1 = p1y
    x2 = p2x; y2 = p2y
    for i in range(n_pivots):
        ox = pcx[i]; oy = pcy[i]
        if (x1 <= ox <= x2) or (x2 <= ox <= x1):
            if abs(x2 - x1) < 1e-12:
                y_apx = y1
            else:
                t = (ox - x1) / (x2 - x1)
                y_apx = y1 + t * (y2 - y1)
            if not (oy - w <= y_apx <= oy + w):
                return False
    return True

@cuda.jit(device=True)
def force_cut_if_needed_dev(p1x, p1y, p2x, p2y, pcx, pcy, n_pivots, w, out_xy, found_ptr):
    # If segment violates band at some pivot x, return clamped intersection there
    found_ptr[0] = 0
    x1 = p1x; y1 = p1y
    x2 = p2x; y2 = p2y
    if x1 == x2:
        return
    # pcx is increasing
    for i in range(1, n_pivots-1):
        ox = pcx[i]; oy = pcy[i]
        if (x1 < ox < x2) or (x2 < ox < x1):
            t = (ox - x1) / (x2 - x1)
            y_line = y1 + (y2 - y1) * t
            if not (oy - w <= y_line <= oy + w):
                # clamp
                cut_y = y_line
                if cut_y < oy - w: cut_y = oy - w
                if cut_y > oy + w: cut_y = oy + w
                out_xy[0] = ox
                out_xy[1] = cut_y
                found_ptr[0] = 1
                return

# ---------------------------------------------
# The modified Imai–Iri candidate (device)
# ---------------------------------------------
@cuda.jit(device=True)
def modified_imai_iri_device(pcx, pcy, n_pivots, w,
                             out_x, out_y, max_out,
                             ybuf, cap_ybuf,
                             q_xy, q_cap):
    # 1) Dense reconstruction on integer-x grid
    x0_arr = cuda.local.array(1, dtype=float64)
    ylen = reconstruct_piecewise_function_dev(pcx, pcy, n_pivots, ybuf, cap_ybuf, x0_arr)
    if ylen == 0:
        return 0
    x0 = int(x0_arr[0])

    # Fast path
    if ylen <= 2:
        m = n_pivots
        if m > max_out:
            return 0
        for i in range(m):
            out_x[i] = pcx[i]
            out_y[i] = pcy[i]
        return m

    # Endpoints from original pivots
    x_start = pcx[0]; y_start = pcy[0]
    x_end   = pcx[n_pivots - 1]; y_end = pcy[n_pivots - 1]

    # 2) Try single piece inside band (two choices at each end)
    s_cand_x0 = x_start; s_cand_y_lo = y_start - w; s_cand_y_hi = y_start + w
    e_cand_xN = x_end;   e_cand_y_lo = y_end   - w; e_cand_y_hi = y_end   + w

    if is_segment_feasible_dev(s_cand_x0, s_cand_y_lo, e_cand_xN, e_cand_y_lo, pcx, pcy, n_pivots, w):
        if max_out < 2: return 0
        out_x[0] = s_cand_x0; out_y[0] = s_cand_y_lo
        out_x[1] = e_cand_xN; out_y[1] = e_cand_y_lo
        return 2
    if is_segment_feasible_dev(s_cand_x0, s_cand_y_lo, e_cand_xN, e_cand_y_hi, pcx, pcy, n_pivots, w):
        if max_out < 2: return 0
        out_x[0] = s_cand_x0; out_y[0] = s_cand_y_lo
        out_x[1] = e_cand_xN; out_y[1] = e_cand_y_hi
        return 2
    if is_segment_feasible_dev(s_cand_x0, s_cand_y_hi, e_cand_xN, e_cand_y_lo, pcx, pcy, n_pivots, w):
        if max_out < 2: return 0
        out_x[0] = s_cand_x0; out_y[0] = s_cand_y_hi
        out_x[1] = e_cand_xN; out_y[1] = e_cand_y_lo
        return 2
    if is_segment_feasible_dev(s_cand_x0, s_cand_y_hi, e_cand_xN, e_cand_y_hi, pcx, pcy, n_pivots, w):
        if max_out < 2: return 0
        out_x[0] = s_cand_x0; out_y[0] = s_cand_y_hi
        out_x[1] = e_cand_xN; out_y[1] = e_cand_y_hi
        return 2

    # 3) Corridor construction (plus/minus stacks) on dense grid
    MAX_STACK = 32
    plus_x  = cuda.local.array(MAX_STACK, dtype=float64)
    plus_y  = cuda.local.array(MAX_STACK, dtype=float64)
    minus_x = cuda.local.array(MAX_STACK, dtype=float64)
    minus_y = cuda.local.array(MAX_STACK, dtype=float64)
    plus_sz = 0; minus_sz = 0

    # initial two points k=0,1
    xk0 = float(x0 + 0); yk0 = round6_dev(ybuf[0])
    xk1 = float(x0 + 1); yk1 = round6_dev(ybuf[1])

    p_plus_x  = xk0; p_plus_y  = yk0 + w
    p_minus_x = xk0; p_minus_y = yk0 - w

    plus_x[0] = p_plus_x;  plus_y[0]  = p_plus_y;  plus_sz  = 1
    plus_x[1] = xk1;       plus_y[1]  = yk1 + w;   plus_sz  = 2

    minus_x[0] = p_minus_x; minus_y[0] = p_minus_y; minus_sz = 1
    minus_x[1] = xk1;       minus_y[1] = yk1 - w;   minus_sz = 2

    # q_tmp uses q_xy buffer; q_sz_ptr[0] = used scalars (pairs => q_sz_ptr/2 points)
    q_sz_ptr = cuda.local.array(1, dtype=int32)
    q_sz_ptr[0] = 0

    tmp_xy  = cuda.local.array(2, dtype=float64)
    tmp2_xy = cuda.local.array(2, dtype=float64)

    for k in range(2, ylen):
        xk = float(x0 + k)
        yk = round6_dev(ybuf[k])

        pip_x = xk; pip_y = yk + w  # p_i_plus
        pim_x = xk; pim_y = yk - w  # p_i_minus

        # Update PLUS stack
        while plus_sz >= 2:
            top_x = plus_x[plus_sz - 1]; top_y = plus_y[plus_sz - 1]
            prv_x = plus_x[plus_sz - 2]; prv_y = plus_y[plus_sz - 2]
            ang = calculate_angle_dev(pip_x, pip_y, top_x, top_y, prv_x, prv_y, True)
            if ang > math.pi:
                plus_sz -= 1
            else:
                break
        if plus_sz < MAX_STACK:
            plus_x[plus_sz] = pip_x; plus_y[plus_sz] = pip_y; plus_sz += 1
        else:
            break  # overflow; bail out gracefully

        # Update MINUS stack
        while minus_sz >= 2:
            top_x = minus_x[minus_sz - 1]; top_y = minus_y[minus_sz - 1]
            prv_x = minus_x[minus_sz - 2]; prv_y = minus_y[minus_sz - 2]
            ang = calculate_angle_dev(pim_x, pim_y, top_x, top_y, prv_x, prv_y, False)
            if ang > math.pi:
                minus_sz -= 1
            else:
                break
        if minus_sz < MAX_STACK:
            minus_x[minus_sz] = pim_x; minus_y[minus_sz] = pim_y; minus_sz += 1
        else:
            break  # overflow

        if plus_sz >= 2 and minus_sz >= 2:
            lpx = plus_x[plus_sz - 2]; lpy = plus_y[plus_sz - 2]
            rpx = plus_x[plus_sz - 1]; rpy = plus_y[plus_sz - 1]
            lmx = minus_x[minus_sz - 2]; lmy = minus_y[minus_sz - 2]
            rmx = minus_x[minus_sz - 1]; rmy = minus_y[minus_sz - 1]

            crossed = False
            ang_plus = calculate_angle_dev(pip_x, pip_y, lpx, lpy, rmx, rmy, True)
            if ang_plus < math.pi:
                find_intersection_dev(lpx, lpy, rmx, rmy,
                                      plus_x[0], plus_y[0], minus_x[0], minus_y[0],
                                      tmp_xy)
                append_strict_dev(q_xy, q_sz_ptr, q_cap, tmp_xy[0], tmp_xy[1])
                crossed = True

            if not crossed:
                ang_minus = calculate_angle_dev(pim_x, pim_y, lmx, lmy, rpx, rpy, False)
                if ang_minus < math.pi:
                    find_intersection_dev(lmx, lmy, rpx, rpy,
                                          minus_x[0], minus_y[0], plus_x[0], plus_y[0],
                                          tmp2_xy)
                    append_strict_dev(q_xy, q_sz_ptr, q_cap, tmp2_xy[0], tmp2_xy[1])

    # Tail: midpoint of last corridor ends
    if plus_sz >= 2 and minus_sz >= 2:
        lpx = plus_x[plus_sz - 2]; lpy = plus_y[plus_sz - 2]
        rpx = plus_x[plus_sz - 1]; rpy = plus_y[plus_sz - 1]
        lmx = minus_x[minus_sz - 2]; lmy = minus_y[minus_sz - 2]
        rmx = minus_x[minus_sz - 1]; rmy = minus_y[minus_sz - 1]

        a = cuda.local.array(2, dtype=float64)
        b = cuda.local.array(2, dtype=float64)
        find_intersection_dev(lpx, lpy, rmx, rmy, plus_x[0], plus_y[0], minus_x[0], minus_y[0], a)
        find_intersection_dev(lmx, lmy, rpx, rpy, minus_x[0], minus_y[0], plus_x[0], plus_y[0], b)
        midx = 0.5 * (a[0] + b[0]); midy = 0.5 * (a[1] + b[1])
        append_strict_dev(q_xy, q_sz_ptr, q_cap, midx, midy)

    # If no corridor points, fall back to endpoints
    if q_sz_ptr[0] < 2:
        if max_out < 2: return 0
        out_x[0] = x_start; out_y[0] = y_start
        out_x[1] = x_end;   out_y[1] = y_end
        return 2

    # 4) Choose feasible start on band and enforce feasibility with cuts
    # p = midpoint candidate (last q point)
    last_x = q_xy[q_sz_ptr[0] - 2]; last_y = q_xy[q_sz_ptr[0] - 1]
    p_xy = cuda.local.array(2, dtype=float64)
    clip_to_band_dev(last_x, last_y, pcx, pcy, n_pivots, w, p_xy)
    px = p_xy[0]; py = p_xy[1]

    start_lo_x = x_start; start_lo_y = y_start - w
    start_hi_x = x_start; start_hi_y = y_start + w

    start_x = start_lo_x; start_y = start_lo_y
    if not is_segment_feasible_dev(start_x, start_y, px, py, pcx, pcy, n_pivots, w):
        if is_segment_feasible_dev(start_hi_x, start_hi_y, px, py, pcx, pcy, n_pivots, w):
            start_x = start_hi_x; start_y = start_hi_y

    # Build final q -> out
    # We'll reuse q_xy as a builder; reset and push
    q_sz_ptr[0] = 0
    append_strict_dev(q_xy, q_sz_ptr, q_cap, start_x, start_y)

    # maybe cut before p
    if not is_segment_feasible_dev(start_x, start_y, px, py, pcx, pcy, n_pivots, w):
        cut_xy = cuda.local.array(2, dtype=float64)
        found = cuda.local.array(1, dtype=int32); found[0] = 0
        force_cut_if_needed_dev(start_x, start_y, px, py, pcx, pcy, n_pivots, w, cut_xy, found)
        if found[0] == 1:
            tmpc = cuda.local.array(2, dtype=float64)
            clip_to_band_dev(cut_xy[0], cut_xy[1], pcx, pcy, n_pivots, w, tmpc)
            append_strict_dev(q_xy, q_sz_ptr, q_cap, tmpc[0], tmpc[1])
    append_strict_dev(q_xy, q_sz_ptr, q_cap, px, py)

    # end point (clipped)
    end_xy = cuda.local.array(2, dtype=float64)
    clip_to_band_dev(x_end, y_end, pcx, pcy, n_pivots, w, end_xy)

    last_qx = q_xy[q_sz_ptr[0] - 2]; last_qy = q_xy[q_sz_ptr[0] - 1]
    if not is_segment_feasible_dev(last_qx, last_qy, end_xy[0], end_xy[1], pcx, pcy, n_pivots, w):
        cut2 = cuda.local.array(2, dtype=float64)
        found2 = cuda.local.array(1, dtype=int32); found2[0] = 0
        force_cut_if_needed_dev(last_qx, last_qy, end_xy[0], end_xy[1], pcx, pcy, n_pivots, w, cut2, found2)
        if found2[0] == 1:
            tmpc2 = cuda.local.array(2, dtype=float64)
            clip_to_band_dev(cut2[0], cut2[1], pcx, pcy, n_pivots, w, tmpc2)
            append_strict_dev(q_xy, q_sz_ptr, q_cap, tmpc2[0], tmpc2[1])
    append_strict_dev(q_xy, q_sz_ptr, q_cap, end_xy[0], end_xy[1])

    # Emit to out_x/out_y
    pts = q_sz_ptr[0] // 2
    use = pts if pts <= max_out else max_out
    for i in range(use):
        out_x[i] = q_xy[2 * i]
        out_y[i] = q_xy[2 * i + 1]
    return use



@cuda.jit(device=True, inline=True)
def _update_slope_interval_dev(x0, y0, xi, yi, eps, smin, smax):
    """
    Intersect current slope interval [smin, smax] with constraint from (xi, yi):
       |(y0 + s*(xi-x0)) - yi| <= eps
    => (yi - y0 - eps)/(xi - x0) <= s <= (yi - y0 + eps)/(xi - x0)
    Returns (new_smin, new_smax, ok_flag)
    """
    dx = xi - x0
    # For strictly increasing x, dx should be > 0
    if dx == 0.0:
        return smin, smax, 0  # infeasible
    lo = (yi - y0 - eps) / dx
    hi = (yi - y0 + eps) / dx
    if lo > smin:
        smin = lo
    if hi < smax:
        smax = hi
    return smin, smax, 1 if (smin <= smax) else 0



@cuda.jit(device=True)
def piecewise_linear_apx_furthest_scan_device(points_x, points_y, n, eps,
                                              out_x, out_y, max_out):
    """
    Exact minimal-piece segmentation under L∞ tolerance with endpoints
    restricted to the existing sample points.

    Returns: count of output pivots written to out_x/out_y.
    """
    # Trivial cases
    if n <= 2:
        count = n if n <= max_out else max_out
        for k in range(count):
            out_x[k] = points_x[k]
            out_y[k] = points_y[k]
        return count

    # Guard: x must be strictly increasing. If not, just copy input (safe fallback).
    strictly_inc = True
    for k in range(1, n):
        if not (points_x[k] > points_x[k - 1]):
            strictly_inc = False
            break
    if not strictly_inc:
        count = n if n <= max_out else max_out
        for k in range(count):
            out_x[k] = points_x[k]
            out_y[k] = points_y[k]
        return count

    # We emit the chosen breakpoints directly into out_* as we go.
    out_count = 0

    # Start with the first point
    if out_count < max_out:
        out_x[out_count] = points_x[0]
        out_y[out_count] = points_y[0]
        out_count += 1

    i = 0
    while i < n - 1:
        # New segment starting at i
        smin = -math.inf
        smax =  math.inf
        j = i + 1
        last_ok = i + 1

        # extend j while feasible
        while j < n:
            smin, smax, ok = _update_slope_interval_dev(points_x[i], points_y[i],
                                                        points_x[j], points_y[j],
                                                        eps, smin, smax)
            if ok == 0:
                break
            last_ok = j
            j += 1

        # Commit the farthest feasible endpoint: index last_ok
        if out_count < max_out:
            out_x[out_count] = points_x[last_ok]
            out_y[out_count] = points_y[last_ok]
            out_count += 1

        i = last_ok  # continue from there

        # Safety: if out buffer is full, we must stop
        if out_count >= max_out:
            break

    return out_count


# ---------- helper: furthest reach for one start ----------
@cuda.jit(device=True)
def _furthest_reach_dev(xs, ys, n, start, eps,
                        out_indices, out_count_ptr, max_count):
    """
    Write feasible end indices (>start) to out_indices; store count in out_count_ptr[0].
    """
    smin = -math.inf
    smax =  math.inf
    x0 = xs[start]
    y0 = ys[start]
    cnt = 0
    for j in range(start + 1, n):
        smin, smax, ok = _update_slope_interval_dev(x0, y0, xs[j], ys[j], eps, smin, smax)
        if ok == 0:
            break
        if cnt < max_count:
            out_indices[cnt] = j
            cnt += 1
        else:
            break
    out_count_ptr[0] = cnt


# ---------- main: beam-search approximation ----------
#beam_width = 10 used during calculations
@cuda.jit(device=True)
def piecewise_linear_apx_beam_search_device(xs, ys, n, eps,
                                            out_x, out_y, max_out,
                                            beam_width):
    """
    Beam-search piecewise linear approximation (L∞).
    Returns number of pivot points written to out_x/out_y.
    """

    # Trivial
    if n <= 2:
        m = n if n <= max_out else max_out
        for i in range(m):
            out_x[i] = xs[i]
            out_y[i] = ys[i]
        return m

    # limited static buffers (beam_width × n max)
    MAX_N = 64           # adjust if input longer
    MAX_BEAM = 16        # upper cap for beam
    # clamp beam width
    if beam_width > MAX_BEAM:
        beam_width = MAX_BEAM
    if n > MAX_N:
        n = MAX_N

    cost  = cuda.local.array(MAX_BEAM, dtype=float64)
    index = cuda.local.array(MAX_BEAM, dtype=int32)
    path_len = cuda.local.array(MAX_BEAM, dtype=int32)
    paths = cuda.local.array((MAX_BEAM, MAX_N), dtype=int32)

    # init beam with start at 0
    cost[0] = 0.0
    index[0] = 0
    path_len[0] = 1
    paths[0, 0] = 0
    beam_count = 1

    # temporary buffers
    next_cost  = cuda.local.array(MAX_BEAM, dtype=float64)
    next_index = cuda.local.array(MAX_BEAM, dtype=int32)
    next_path_len = cuda.local.array(MAX_BEAM, dtype=int32)
    next_paths = cuda.local.array((MAX_BEAM, MAX_N), dtype=int32)
    tmp_end = cuda.local.array(MAX_N, dtype=int32)
    tmp_count = cuda.local.array(1, dtype=int32)

    # main loop
    while True:
        new_beam_count = 0
        reached_end = 0

        for b in range(beam_count):
            i = index[b]
            if i == n - 1:
                reached_end = 1
                # copy best path to out
                plen = path_len[b]
                for k in range(plen):
                    out_x[k] = xs[paths[b, k]]
                    out_y[k] = ys[paths[b, k]]
                return plen

            # get feasible ends
            _furthest_reach_dev(xs, ys, n, i, eps, tmp_end, tmp_count, MAX_N)
            cnt = tmp_count[0]

            for e in range(cnt):
                j = tmp_end[e]
                if new_beam_count >= beam_width:
                    break
                new_cost = cost[b] + 1.0
                heuristic = (n - j - 1) / (n / 5.0)
                total_cost = new_cost + heuristic

                next_cost[new_beam_count] = total_cost
                next_index[new_beam_count] = j
                plen = path_len[b]
                next_path_len[new_beam_count] = plen + 1
                for t in range(plen):
                    next_paths[new_beam_count, t] = paths[b, t]
                next_paths[new_beam_count, plen] = j
                new_beam_count += 1

        if new_beam_count == 0:
            break

        # partial selection of top-beam_width (simple linear pick)
        # find smallest costs
        for i in range(min(new_beam_count, beam_width)):
            best = i
            for j in range(i + 1, new_beam_count):
                if next_cost[j] < next_cost[best]:
                    best = j
            # swap
            tmpc = next_cost[i]; next_cost[i] = next_cost[best]; next_cost[best] = tmpc
            tmpi = next_index[i]; next_index[i] = next_index[best]; next_index[best] = tmpi
            tmplen = next_path_len[i]; next_path_len[i] = next_path_len[best]; next_path_len[best] = tmplen
            for k in range(next_path_len[i]):
                tmpv = next_paths[i, k]
                next_paths[i, k] = next_paths[best, k]
                next_paths[best, k] = tmpv

        beam_count = min(new_beam_count, beam_width)
        for b in range(beam_count):
            cost[b] = next_cost[b]
            index[b] = next_index[b]
            path_len[b] = next_path_len[b]
            for k in range(path_len[b]):
                paths[b, k] = next_paths[b, k]

    # fallback: take best beam closest to end
    best_idx = 0
    best_gap = n
    for b in range(beam_count):
        gap = abs(index[b] - (n - 1))
        if gap < best_gap:
            best_gap = gap
            best_idx = b

    plen = path_len[best_idx]
    for k in range(plen):
        out_x[k] = xs[paths[best_idx, k]]
        out_y[k] = ys[paths[best_idx, k]]
    if paths[best_idx, plen - 1] != n - 1 and plen < max_out:
        out_x[plen] = xs[n - 1]
        out_y[plen] = ys[n - 1]
        plen += 1
    return plen

# ---------- helper: triangle area ----------
@cuda.jit(device=True, inline=True)
def _triangle_area_dev(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) +
                x2 * (y3 - y1) +
                x3 * (y1 - y2)) / 2.0)


# ---------- main: Visvalingam simplification ----------
@cuda.jit(device=True)
def piecewise_linear_apx_visvalingam_device(points_x, points_y, n, eps,
                                            out_x, out_y, max_out):
    """
    CUDA-device implementation of Visvalingam–Whyatt simplification
    under L∞ tolerance. Removes smallest-area points until all
    triangle heights ≤ epsilon.
    Returns number of pivot points written to out_x/out_y.
    """

    # trivial case
    if n <= 2:
        count = n if n <= max_out else max_out
        for i in range(count):
            out_x[i] = points_x[i]
            out_y[i] = points_y[i]
        return count

    MAX_N = 128  # maximum allowed points (adjust to your data)
    if n > MAX_N:
        n = MAX_N

    # static buffers
    areas = cuda.local.array(MAX_N, dtype=float64)
    removed = cuda.local.array(MAX_N, dtype=int32)

    # initialize
    for i in range(n):
        removed[i] = 0
        areas[i] = math.inf

    # compute initial triangle areas
    for i in range(1, n - 1):
        a = _triangle_area_dev(points_x[i - 1], points_y[i - 1],
                               points_x[i],     points_y[i],
                               points_x[i + 1], points_y[i + 1])
        areas[i] = a

    # iterative removal loop
    while True:
        # find smallest non-removed area
        min_a = math.inf
        min_idx = -1
        for i in range(1, n - 1):
            if removed[i] == 0 and areas[i] < min_a:
                min_a = areas[i]
                min_idx = i

        if min_idx == -1:
            break

        # compute height approximation
        base = points_x[min_idx + 1] - points_x[min_idx - 1]
        if base == 0.0:
            height = math.inf
        else:
            height = (2.0 * min_a / base)

        # stop if beyond epsilon
        if height > eps:
            break

        # remove that point
        removed[min_idx] = 1

        # update neighboring triangle areas
        for j in range(min_idx - 1, min_idx + 2):
            if 0 < j < n - 1 and removed[j] == 0:
                new_a = _triangle_area_dev(points_x[j - 1], points_y[j - 1],
                                           points_x[j],     points_y[j],
                                           points_x[j + 1], points_y[j + 1])
                areas[j] = new_a

    # collect simplified points
    count = 0
    for i in range(n):
        if removed[i] == 0 and count < max_out:
            out_x[count] = points_x[i]
            out_y[count] = points_y[i]
            count += 1

    return count
