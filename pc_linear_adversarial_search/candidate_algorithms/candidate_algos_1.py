from typing import List, Tuple
Point = Tuple[float, float]

def distance_point_to_line_segment(point: Tuple[float, float],
                                   start: Tuple[float, float],
                                   end: Tuple[float, float]) -> float:
    """
    Calculate the perpendicular distance from a point to a line segment.
    Returns infinity norm (maximum absolute deviation).
    """
    x0, y0 = point
    x1, y1 = start
    x2, y2 = end

    # If start and end are the same point
    if x1 == x2:
        return abs(y0 - y1)

    # Calculate y-value on line segment at x0
    if x0 < x1 or x0 > x2:
        # Point is outside the x-range of segment
        return float('inf')

    # Linear interpolation
    y_line = y1 + (y2 - y1) * (x0 - x1) / (x2 - x1)
    return abs(y0 - y_line)


def is_valid_segment(points: List[Tuple[float, float]],
                     start_idx: int, end_idx: int, epsilon: float) -> bool:
    """Check if all points between start_idx and end_idx are within epsilon tolerance."""
    if end_idx <= start_idx + 1:
        return True

    start_point = points[start_idx]
    end_point = points[end_idx]

    for i in range(start_idx + 1, end_idx):
        distance = distance_point_to_line_segment(points[i], start_point, end_point)
        if distance > epsilon:
            return False
    return True



def improved_greedy_with_lookahead(points: List[Point], epsilon: float, lookahead: int = 5) -> Tuple[List[Point], int, int]:
    """Greedy with limited lookahead (not guaranteed optimal)."""
    n = len(points)
    given_num_pieces = max(0, n - 1)
    if n <= 2:
        return points, max(0, n - 1), given_num_pieces

    result = [points[0]]
    current_start = 0

    while current_start < n - 1:
        best_end = current_start + 1
        max_look = min(current_start + lookahead + 1, n)
        for end_idx in range(current_start + 2, max_look):
            if is_valid_segment(points, current_start, end_idx, epsilon):
                best_end = end_idx
        result.append(points[best_end])
        current_start = best_end

    optimal_num_pieces = max(0, len(result) - 1)
    return result, optimal_num_pieces, given_num_pieces
def branch_and_bound(points: List[Point], epsilon: float) -> Tuple[List[Point], int, int]:
    """Branch and Bound - guaranteed optimal."""
    n = len(points)
    given_num_pieces = max(0, n - 1)
    if n <= 2:
        return points, max(0, n - 1), given_num_pieces

    # Precompute validity
    valid_segments = {(i, j): is_valid_segment(points, i, j, epsilon)
                      for i in range(n) for j in range(i+1, n)}

    best_solution, best_segments = None, float('inf')

    def dfs(path: List[int], pos: int):
        nonlocal best_solution, best_segments
        if len(path) >= best_segments:
            return
        if pos == n - 1:
            best_solution, best_segments = path.copy(), len(path)
            return
        for nxt in range(pos+1, n):
            if valid_segments[(pos, nxt)]:
                path.append(nxt)
                dfs(path, nxt)
                path.pop()

    dfs([0], 0)

    if best_solution:
        result = [points[i] for i in best_solution]
    else:
        result = points

    optimal_num_pieces = max(0, len(result) - 1)
    return result, optimal_num_pieces, given_num_pieces

def greedy_approximation(points: List[Point], epsilon: float) -> Tuple[List[Point], int, int]:
    """
    Greedy algorithm for piecewise linear approximation under L∞.
    Returns minimal number of segments (optimal for this model).
    """
    n = len(points)
    given_num_pieces = max(0, n - 1)
    if n <= 2:
        return points, max(0, n - 1), given_num_pieces

    result = [points[0]]
    current_start = 0

    while current_start < n - 1:
        farthest_valid = current_start + 1
        for end_idx in range(current_start + 2, n):
            valid_segment = True
            for mid_idx in range(current_start + 1, end_idx):
                distance = distance_point_to_line_segment(
                    points[mid_idx], points[current_start], points[end_idx]
                )
                if distance > epsilon:
                    valid_segment = False
                    break
            if valid_segment:
                farthest_valid = end_idx
            else:
                break
        result.append(points[farthest_valid])
        current_start = farthest_valid

    optimal_num_pieces = max(0, len(result) - 1)
    return result, optimal_num_pieces, given_num_pieces

def douglas_peucker_approximation(points: List[Point], epsilon: float) -> Tuple[List[Point], int, int]:
    """
    Douglas-Peucker algorithm for piecewise linear approximation.
    Not guaranteed optimal for L∞, but usually good.
    """
    n = len(points)
    given_num_pieces = max(0, n - 1)
    if n <= 2:
        return points, max(0, n - 1), given_num_pieces

    def dp_recursive(start_idx: int, end_idx: int) -> List[int]:
        if end_idx <= start_idx + 1:
            return []
        max_distance = 0
        max_idx = start_idx
        for i in range(start_idx + 1, end_idx):
            distance = distance_point_to_line_segment(
                points[i], points[start_idx], points[end_idx]
            )
            if distance > max_distance:
                max_distance = distance
                max_idx = i
        if max_distance <= epsilon:
            return []
        left_points = dp_recursive(start_idx, max_idx)
        right_points = dp_recursive(max_idx, end_idx)
        return left_points + [max_idx] + right_points

    keep_indices = [0] + dp_recursive(0, n - 1) + [n - 1]
    keep_indices = sorted(set(keep_indices))
    result = [points[i] for i in keep_indices]

    optimal_num_pieces = max(0, len(result) - 1)
    return result, optimal_num_pieces, given_num_pieces
