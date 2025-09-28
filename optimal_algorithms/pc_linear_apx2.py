import numpy as np
import matplotlib.pyplot as plt

def calculate_angle(point1, point2, point3, direction='+'):
    """
    Measures angle between three points in positive or negative direction

    Args:
        point1 (list): x and y coordinates of first point
        point2 (list): x and y coordinates of center point (vertex)
        point3 (list): x and y coordinates of third point
        direction (str, optional): direction of angle '+' = counterclockwise, '-' = clockwise

    Returns:
        float: angle in radians
    """
    angle1 = np.arctan2(point1[1] - point2[1], point1[0] - point2[0])
    angle2 = np.arctan2(point3[1] - point2[1], point3[0] - point2[0])
    angle_diff = angle2 - angle1
    if angle_diff < 0:
        angle_diff += 2 * np.pi
    if direction == '-':
        angle_diff = 2 * np.pi - angle_diff
    return np.round(angle_diff, 6)
def find_intersection(line1_start, line1_end, line2_start, line2_end):
    """
    Returns intersection of two lines defined by their endpoints

    Args:
        line1_start (list): x and y coordinates of first line's start point
        line1_end (list): x and y coordinates of first line's end point
        line2_start (list): x and y coordinates of second line's start point
        line2_end (list): x and y coordinates of second line's end point

    Returns:
        tuple: x and y coordinates of the intersection, or None if lines are parallel
    """
    denominator = (line1_end[0] - line1_start[0]) * (line2_end[1] - line2_start[1]) - (
            line2_end[0] - line2_start[0]) * (line1_end[1] - line1_start[1])
    if abs(denominator) < 1e-10:
        x = (line1_start[0] + line1_end[0]) / 2
        y = (line1_start[1] + line1_end[1]) / 2
        return (np.round(x, 6), np.round(y, 6))
    x = ((line1_end[0] * line1_start[1] - line1_start[0] * line1_end[1]) * (line2_end[0] - line2_start[0]) -
         (line2_end[0] * line2_start[1] - line2_start[0] * line2_end[1]) * (
                     line1_end[0] - line1_start[0])) / denominator
    y = ((line1_end[0] * line1_start[1] - line1_start[0] * line1_end[1]) * (line2_end[1] - line2_start[1]) -
         (line2_end[0] * line2_start[1] - line2_start[0] * line2_end[1]) * (
                     line1_end[1] - line1_start[1])) / denominator
    return (np.round(x, 6), np.round(y, 6))

def clip_to_band(x, y, pc_linear_fx, epsilon):
    """Clip a candidate (x, y) into the tolerance band at exact breakpoints if possible."""
    for ox, oy in pc_linear_fx:
        if abs(x - ox) < 1e-9:  # match x
            ymin, ymax = oy - epsilon, oy + epsilon
            return (x, min(max(y, ymin), ymax))
    return (x, y)
def is_segment_feasible(p1, p2, pc_linear_fx, epsilon):
    """Check if line p1->p2 stays inside tolerance band at all breakpoints."""
    x1, y1 = p1
    x2, y2 = p2
    for ox, oy in pc_linear_fx:
        if x1 <= ox <= x2:
            if abs(x2 - x1) < 1e-12:
                y_apx = y1
            else:
                t = (ox - x1) / (x2 - x1)
                y_apx = y1 + t * (y2 - y1)
            if not (oy - epsilon <= y_apx <= oy + epsilon):
                return False
    return True
def force_cut_if_needed(p1, p2, pc_linear_fx, epsilon):
    """If segment p1->p2 violates tolerance, cut at the first offending breakpoint."""
    x1, y1 = p1
    x2, y2 = p2
    for ox, oy in sorted(pc_linear_fx):
        if x1 < ox < x2:
            # interpolation
            y_line = y1 + (y2 - y1) * (ox - x1) / (x2 - x1)
            if not (oy - epsilon <= y_line <= oy + epsilon):
                cut_y = min(max(y_line, oy - epsilon), oy + epsilon)
                return (ox, cut_y)
    return None

def approximate_pc_linear_fx(pc_linear_fx, w):
    y = reconstruct_piecewise_function(pc_linear_fx)
    y = np.array(y)
    x = np.arange(pc_linear_fx[0][0], pc_linear_fx[0][0] + len(y))
    y = np.round(y, 6)

    if len(y) <= 2:
        optimal_pc_linear_fx = np.array(pc_linear_fx)
        optimal_num_pieces = len(pc_linear_fx) - 1
        given_num_pieces = optimal_num_pieces
        return optimal_pc_linear_fx, optimal_num_pieces, given_num_pieces

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
        while (p != p_plus) and calculate_angle(p_i_plus, p, t_plus[p], '+') > np.pi:
            p = t_plus[p]
        s_plus[p] = p_i_plus
        t_plus[p_i_plus] = p

        p = (x[i - 1], y[i - 1] - w)
        p_i_minus = (x[i], y[i] - w)
        while (p != p_minus) and calculate_angle(p_i_minus, p, t_minus[p], '-') > np.pi:
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
    # midpoint candidate
    # Candidate midpoint
    p = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    p = clip_to_band(p[0], p[1], pc_linear_fx, w)

    # Final sequence of vertices
    q = []
    # Always start with first point
    q.append((pc_linear_fx[0][0], pc_linear_fx[0][1] - w))

    # Enforce feasibility of p
    if not is_segment_feasible(q[-1], p, pc_linear_fx, w):
        cut = force_cut_if_needed(q[-1], p, pc_linear_fx, w)
        if cut is not None:
            cut = clip_to_band(cut[0], cut[1], pc_linear_fx, w)
            q.append(cut)
    else:
        q.append(p)

    # End point handling
    end = (pc_linear_fx[-1][0], pc_linear_fx[-1][1])
    end = clip_to_band(end[0], end[1], pc_linear_fx, w)

    if not is_segment_feasible(q[-1], end, pc_linear_fx, w):
        cut = force_cut_if_needed(q[-1], end, pc_linear_fx, w)
        if cut is not None:
            cut = clip_to_band(cut[0], cut[1], pc_linear_fx, w)
            q.append(cut)
    q.append(end)

    optimal_pc_linear_fx = np.array(q)
    return optimal_pc_linear_fx, len(optimal_pc_linear_fx) - 1, len(pc_linear_fx) - 1

def reconstruct_piecewise_function(pc_linear_fx):
    pivot_points = sorted(pc_linear_fx, key=lambda p: p[0])
    y_values = []
    for i in range(len(pivot_points) - 1):
        start_point = pivot_points[i]
        end_point = pivot_points[i + 1]
        if end_point[0] == start_point[0]:
            continue
        slope = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
        intercept = start_point[1] - slope * start_point[0]
        for x in range(int(start_point[0]), int(end_point[0])):
            y_values.append(x * slope + intercept)
    y_values.append(pivot_points[-1][1])
    return np.array(y_values)
def plot_piecewise_linear_approximation(pc_linear_fx, optimal_pc_linear_fx, epsilon):
    """
    Plots the original piecewise linear function, the optimal approximation, and the error bounds.

    Args:
        pc_linear_fx (list): List of (x,y) points defining the original piecewise linear function
        optimal_pc_linear_fx (list): List of (x,y) points defining the optimal approximation
        epsilon (float): Error bound used for the approximation
    """
    # Reconstruct the original function for plotting
    y_values = reconstruct_piecewise_function(pc_linear_fx)
    x_values = np.arange(pc_linear_fx[0][0], pc_linear_fx[0][0] + len(y_values))
    plt.figure(figsize=(12, 6))
    plt.plot(x_values, y_values, label="Original function", color='blue', linewidth=4)

    # Plot the error bounds
    plt.fill_between(x_values,
                     y_values - epsilon,
                     y_values + epsilon,
                     color='lightgray',
                     alpha=0.5,
                     label=f'Error bounds (±{epsilon})')

    # Plot the optimal approximation
    if optimal_pc_linear_fx is not None:
        opt_x = [p[0] for p in optimal_pc_linear_fx]
        opt_y = [p[1] for p in optimal_pc_linear_fx]
        plt.plot(opt_x, opt_y, '-o', label="Optimal approximation", color='red', linewidth=2, markersize=6)

    # Add plot decorations
    plt.title(f"Piecewise Linear Approximation (ε={epsilon})", fontsize=14)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()