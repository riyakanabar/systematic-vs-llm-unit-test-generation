import math
from numba import cuda, float64, int32

# ==============================
# Device helpers
# ==============================

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

# ==============================
# Dense reconstruction (integer-x grid)
# Inputs: pcx/pcy (length n_pivots, sorted by x)
# Outputs: ybuf[0:out_len), and x0_out[0] = starting x (int)
# ==============================
@cuda.jit(device=True)
def reconstruct_piecewise_function_dev(pcx, pcy, n_pivots, ybuf, cap_ybuf, x0_out):
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

# ==============================
# Corridor-based approximation (array stacks)
# API:
#   pcx/pcy,n_pivots,w            : input pivots and corridor half-width
#   out_x/out_y,max_out           : output pivot buffers + capacity
#   ybuf,cap_ybuf                 : scratch for dense y
#   q_xy,q_cap                    : intersection list buffer (x,y pairs interleaved)
# returns: count of output pivots (>=2) or 0 on overflow/failure
# ==============================
@cuda.jit(device=True)
def approx_pc_linear_fx_device(pcx, pcy, n_pivots, w,
                               out_x, out_y, max_out,
                               ybuf, cap_ybuf,
                               q_xy, q_cap):
    # 1) reconstruct dense y over integer grid
    x0_arr = cuda.local.array(1, dtype=float64)
    ylen = reconstruct_piecewise_function_dev(pcx, pcy, n_pivots, ybuf, cap_ybuf, x0_arr)
    if ylen == 0:
        return 0
    x0 = int(x0_arr[0])

    # FAST PATHS
    if ylen <= 2:
        m = n_pivots
        if m > max_out:
            return 0
        for i in range(m):
            out_x[i] = pcx[i]
            out_y[i] = pcy[i]
        return m

    if abs(w) < 1e-10:
        # check straight line from first to last
        x_first = float(x0)
        x_last  = float(x0 + (ylen - 1))
        dx = x_last - x_first
        if abs(dx) < 1e-10:
            m = n_pivots
            if m > max_out:
                return 0
            for i in range(m):
                out_x[i] = pcx[i]
                out_y[i] = pcy[i]
            return m

        y0 = round6_dev(ybuf[0])
        yN = round6_dev(ybuf[ylen - 1])
        slope = (yN - y0) / dx
        intercept = y0 - slope * x_first
        ok = True
        for k in range(ylen):
            xk = float(x0 + k)
            dev = abs(round6_dev(ybuf[k]) - (slope * xk + intercept))
            if dev > 1e-10:
                ok = False
                break
        if ok:
            if max_out < 2:
                return 0
            out_x[0] = x_first; out_y[0] = y0
            out_x[1] = x_last;  out_y[1] = yN
            return 2
        else:
            m = n_pivots
            if m > max_out:
                return 0
            for i in range(m):
                out_x[i] = pcx[i]
                out_y[i] = pcy[i]
            return m

    # ==============================
    # Corridor stacks
    # ==============================
    # Since max pieces=10 => 11 grid-defining pivots typically enough for stacks.
    # We operate in the dense grid (xk, yk ± w).
    MAX_STACK = 16  # safe headroom
    plus_x = cuda.local.array(MAX_STACK, dtype=float64)
    plus_y = cuda.local.array(MAX_STACK, dtype=float64)
    minus_x = cuda.local.array(MAX_STACK, dtype=float64)
    minus_y = cuda.local.array(MAX_STACK, dtype=float64)
    plus_sz = 0
    minus_sz = 0

    # q buffer holds intersections/waypoints (x,y pairs)
    q_sz = 0  # counts points (each point uses 2 doubles in q_xy)

    # init with k=0 and k=1
    xk0 = float(x0 + 0)
    xk1 = float(x0 + 1)
    yk0 = round6_dev(ybuf[0])
    yk1 = round6_dev(ybuf[1])

    # initial corridor points
    p_plus_x = xk0; p_plus_y = yk0 + w
    p_minus_x = xk0; p_minus_y = yk0 - w

    # stacks start with first + second points
    plus_x[0] = p_plus_x; plus_y[0] = p_plus_y; plus_sz = 1
    px1 = xk1; py1 = yk1 + w
    plus_x[1] = px1; plus_y[1] = py1; plus_sz = 2

    minus_x[0] = p_minus_x; minus_y[0] = p_minus_y; minus_sz = 1
    mx1 = xk1; my1 = yk1 - w
    minus_x[1] = mx1; minus_y[1] = my1; minus_sz = 2

    # For convenience
    tmp_xy = cuda.local.array(2, dtype=float64)
    tmp2_xy = cuda.local.array(2, dtype=float64)

    # sweep k = 2..ylen-1
    for k in range(2, ylen):
        xk = float(x0 + k)
        yk = round6_dev(ybuf[k])

        # new corridor points
        pip_x = xk; pip_y = yk + w  # p_i_plus
        pim_x = xk; pim_y = yk - w  # p_i_minus

        # ---- Update PLUS stack: pop while angle(new, top, prev) > pi
        while plus_sz >= 2:
            top_x = plus_x[plus_sz - 1]; top_y = plus_y[plus_sz - 1]
            prv_x = plus_x[plus_sz - 2]; prv_y = plus_y[plus_sz - 2]
            ang = calculate_angle_dev(pip_x, pip_y, top_x, top_y, prv_x, prv_y, True)
            if ang > math.pi:
                plus_sz -= 1  # pop
            else:
                break
        if plus_sz < MAX_STACK:
            plus_x[plus_sz] = pip_x; plus_y[plus_sz] = pip_y; plus_sz += 1
        else:
            return 0  # overflow; increase MAX_STACK

        # ---- Update MINUS stack: pop while angle(new, top, prev) > pi in '-' sense
        while minus_sz >= 2:
            top_x = minus_x[minus_sz - 1]; top_y = minus_y[minus_sz - 1]
            prv_x = minus_x[minus_sz - 2]; prv_y = minus_y[minus_sz - 2]
            ang = calculate_angle_dev(pim_x, pim_y, top_x, top_y, prv_x, prv_y, False)
            if ang > math.pi:
                minus_sz -= 1  # pop
            else:
                break
        if minus_sz < MAX_STACK:
            minus_x[minus_sz] = pim_x; minus_y[minus_sz] = pim_y; minus_sz += 1
        else:
            return 0  # overflow; increase MAX_STACK

        # Current ends and lasts
        # l_plus = second-to-last on plus stack (if exists), r_plus = last
        # l_minus, r_minus similarly
        if plus_sz >= 2 and minus_sz >= 2:
            lpx = plus_x[plus_sz - 2]; lpy = plus_y[plus_sz - 2]
            rpx = plus_x[plus_sz - 1]; rpy = plus_y[plus_sz - 1]
            lmx = minus_x[minus_sz - 2]; lmy = minus_y[minus_sz - 2]
            rmx = minus_x[minus_sz - 1]; rmy = minus_y[minus_sz - 1]

            # Check crossing conditions (mirror your CPU code’s tests)
            # if angle(p_i_plus, l_plus, r_minus, '+') < pi: emit intersection on (+ with -)
            ang_plus = calculate_angle_dev(pip_x, pip_y, lpx, lpy, rmx, rmy, True)
            crossed = False
            if ang_plus < math.pi:
                # Intersection of (l_plus, r_minus) with (last confirmed p_plus, p_minus).
                # Use last confirmed endpoints on stacks as approximations.
                # Intersect lines (l_plus -> r_minus) with (r_plus -> r_minus)'s "axes"
                ok1 = find_intersection_dev(lpx, lpy, rmx, rmy,
                                            plus_x[0], plus_y[0], minus_x[0], minus_y[0],
                                            tmp_xy)
                if q_sz + 2 <= q_cap:
                    q_xy[q_sz] = tmp_xy[0]; q_xy[q_sz + 1] = tmp_xy[1]
                    q_sz += 2
                    crossed = True
                else:
                    return 0  # q buffer overflow

            # elif angle(p_i_minus, l_minus, r_plus, '-') < pi: emit intersection
            if not crossed:
                ang_minus = calculate_angle_dev(pim_x, pim_y, lmx, lmy, rpx, rpy, False)
                if ang_minus < math.pi:
                    ok2 = find_intersection_dev(lmx, lmy, rpx, rpy,
                                                minus_x[0], minus_y[0], plus_x[0], plus_y[0],
                                                tmp2_xy)
                    if q_sz + 2 <= q_cap:
                        q_xy[q_sz] = tmp2_xy[0]; q_xy[q_sz + 1] = tmp2_xy[1]
                        q_sz += 2
                    else:
                        return 0

            # No else: if neither crossing condition met, continue sweeping.
        # else: not enough points on both stacks yet

    # Tail: add midpoint of last crossing of corridor ends as in your CPU code.
    # Use intersection of (last l_plus, r_minus) and (last l_minus, r_plus) averaged.
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
        if q_sz + 2 <= q_cap:
            q_xy[q_sz] = midx; q_xy[q_sz + 1] = midy
            q_sz += 2
        else:
            return 0

    # ==============================
    # Emit output pivots from q (points)
    # q_xy stores (x,y) pairs; ensure at least 2 points (start+end)
    # ==============================
    pts = q_sz // 2
    if pts < 2:
        # fallback: just return endpoints of dense series
        if max_out < 2:
            return 0
        out_x[0] = float(x0)
        out_y[0] = round6_dev(ybuf[0] + 0.0)
        out_x[1] = float(x0 + (ylen - 1))
        out_y[1] = round6_dev(ybuf[ylen - 1] + 0.0)
        return 2

    # copy to output (cap at max_out)
    use = pts if pts <= max_out else max_out
    for i in range(use):
        out_x[i] = q_xy[2 * i]
        out_y[i] = q_xy[2 * i + 1]
    return use
