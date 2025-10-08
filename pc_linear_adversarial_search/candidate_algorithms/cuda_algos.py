from numba import cuda, float64, int32
import math

@cuda.jit(device=True, inline=True)
def _dist_point_to_segment_scalar_dev(x0, y0, x1, y1, x2, y2):
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
                if _dist_point_to_segment_scalar_dev(x0, y0, x1, y1, x2, y2) > epsilon:
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
