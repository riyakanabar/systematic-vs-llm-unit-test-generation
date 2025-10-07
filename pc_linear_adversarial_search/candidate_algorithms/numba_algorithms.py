import numpy as np
from numba import njit

@njit(fastmath=True)
def numba_distance_point_to_line_segment(px, py, x1, y1, x2, y2):
    """Compute perpendicular distance from point (px,py) to segment (x1,y1)-(x2,y2)."""
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0.0 and dy == 0.0:
        return abs(py - y1)
    # projection factor t in [0,1]
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return abs(py - proj_y)   # L∞ vertical deviation

@njit(fastmath=True)
def numba_greedy_approximation(points, epsilon):
    """
    Greedy algorithm for piecewise linear approximation under L∞.
    points: 2D float64 array of shape (n, 2)
    Returns (result_points, optimal_num_pieces, given_num_pieces)
    """
    n = points.shape[0]
    given_num_pieces = max(0, n - 1)
    if n <= 2:
        return points.copy(), max(0, n - 1), given_num_pieces

    result = np.empty_like(points)
    result[0, 0] = points[0, 0]
    result[0, 1] = points[0, 1]
    result_count = 1

    current_start = 0
    while current_start < n - 1:
        farthest_valid = current_start + 1
        for end_idx in range(current_start + 2, n):
            valid_segment = True
            for mid_idx in range(current_start + 1, end_idx):
                distance = numba_distance_point_to_line_segment(
                    points[mid_idx, 0], points[mid_idx, 1],
                    points[current_start, 0], points[current_start, 1],
                    points[end_idx, 0], points[end_idx, 1]
                )
                if distance > epsilon:
                    valid_segment = False
                    break
            if valid_segment:
                farthest_valid = end_idx
            else:
                break
        result[result_count, 0] = points[farthest_valid, 0]
        result[result_count, 1] = points[farthest_valid, 1]
        result_count += 1
        current_start = farthest_valid

    result_trimmed = result[:result_count]
    optimal_num_pieces = max(0, result_count - 1)
    return result_trimmed, optimal_num_pieces, given_num_pieces
