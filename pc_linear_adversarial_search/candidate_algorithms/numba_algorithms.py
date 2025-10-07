import numpy as np
from numba import njit

@njit(fastmath=True, cache=True)
def _dist_point_to_segment_scalar(x0, y0, x1, y1, x2, y2):
    # Vertical segment
    if x1 == x2:
        return abs(y0 - y1)
    # Outside x-range → infeasible for this segment
    if x0 < x1 or x0 > x2:
        return np.inf
    # Linear interpolation on the segment and L∞ deviation in y
    y_line = y1 + (y2 - y1) * (x0 - x1) / (x2 - x1)
    d = y0 - y_line
    return abs(d)

@njit(fastmath=True, cache=True)
def greedy_approximation_numba(points, epsilon):
    """
    Greedy algorithm for piecewise linear approximation under L∞ (Numba JIT).
    points: float64 array of shape (n, 2), with strictly increasing x.
    Returns: (result_points, optimal_num_pieces, given_num_pieces)
    """
    n = points.shape[0]
    given_num_pieces = 0 if n <= 1 else n - 1
    if n <= 2:
        return points.copy(), (0 if n <= 1 else 1), given_num_pieces

    # Preallocate result; we’ll slice at the end.
    result = np.empty_like(points)
    result[0, 0] = points[0, 0]
    result[0, 1] = points[0, 1]
    result_count = 1

    current_start = 0
    while current_start < n - 1:
        farthest_valid = current_start + 1
        # Try to extend the current segment as far as epsilon allows
        for end_idx in range(current_start + 2, n):
            x1 = points[current_start, 0]
            y1 = points[current_start, 1]
            x2 = points[end_idx, 0]
            y2 = points[end_idx, 1]

            valid_segment = True
            for mid_idx in range(current_start + 1, end_idx):
                x0 = points[mid_idx, 0]
                y0 = points[mid_idx, 1]
                if _dist_point_to_segment_scalar(x0, y0, x1, y1, x2, y2) > epsilon:
                    valid_segment = False
                    break

            if valid_segment:
                farthest_valid = end_idx
            else:
                break  # cannot extend further

        # Commit the farthest feasible endpoint
        result[result_count, 0] = points[farthest_valid, 0]
        result[result_count, 1] = points[farthest_valid, 1]
        result_count += 1
        current_start = farthest_valid

    optimal_num_pieces = result_count - 1 if result_count >= 2 else 0
    return result[:result_count].copy(), optimal_num_pieces, given_num_pieces
