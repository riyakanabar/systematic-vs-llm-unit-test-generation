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
def branch_and_bound_device(points_x, points_y, n, epsilon,
                            out_x, out_y, max_out):
    """
    Iterative Branch and Bound (device-safe, no recursion)
    Finds minimal-piece approximation under ε tolerance.
    """
    # === Precompute validity matrix ===
    valid = cuda.local.array((16, 16), dtype=boolean)  # supports up to 16 points
    for i in range(n):
        for j in range(i + 1, n):
            valid[i, j] = is_valid_segment_dev(points_x, points_y, i, j, epsilon)
        for j in range(0, i + 1):
            valid[i, j] = False  # unused region

    # === Stack for DFS ===
    stack = cuda.local.array(64, dtype=int32)
    depth = 1
    stack[0] = 0  # start from first point

    best_path = cuda.local.array(16, dtype=int32)
    best_len = n + 1  # initially infinite

    while depth > 0:
        pos = stack[depth - 1]

        if pos == n - 1:
            # Found a full path (reached last point)
            if depth < best_len:
                best_len = depth
                for k in range(depth):
                    best_path[k] = stack[k]
            depth -= 1
            continue

        extended = False
        for nxt in range(n - 1, pos, -1):  # reverse order for DFS-like behavior
            if valid[pos, nxt] and depth < 16:
                stack[depth] = nxt
                depth += 1
                extended = True
                break

        if not extended:
            depth -= 1  # backtrack

    # === Construct result ===
    if best_len == n + 1:
        # no valid segmentation found — return input
        count = n
        if count > max_out:
            count = max_out
        for i in range(count):
            out_x[i] = points_x[i]
            out_y[i] = points_y[i]
        return count

    count = best_len
    if count > max_out:
        count = max_out
    for i in range(count):
        out_x[i] = points_x[best_path[i]]
        out_y[i] = points_y[best_path[i]]

    return count


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




