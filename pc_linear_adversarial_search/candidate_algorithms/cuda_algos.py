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





