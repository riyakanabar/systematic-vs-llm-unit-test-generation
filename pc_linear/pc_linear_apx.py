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
    if abs(denominator) < 1e-10:  # Handle nearly parallel lines
        return None
    x = ((line1_end[0] * line1_start[1] - line1_start[0] * line1_end[1]) * (line2_end[0] - line2_start[0]) -
         (line2_end[0] * line2_start[1] - line2_start[0] * line2_end[1]) * (
                     line1_end[0] - line1_start[0])) / denominator
    y = ((line1_end[0] * line1_start[1] - line1_start[0] * line1_end[1]) * (line2_end[1] - line2_start[1]) -
         (line2_end[0] * line2_start[1] - line2_start[0] * line2_end[1]) * (
                     line1_end[1] - line1_start[1])) / denominator
    return (np.round(x, 6), np.round(y, 6))
def approximate_pc_linear_fx(pc_linear_fx, epsilon):
    """
    Constructs optimal polygon and returns pivot points.
    Based on 'An Optimal Algorithm for Approximating a Piecewise Linear
    Function' by HIROSHI IMAI and MASAO IRI.

    Args:
        y_values (np.array or list): Time series or y-values of the function to approximate
        epsilon (float, optional): Error bound

    Returns:
        np.array: Pivot points of the optimal approximation
    """
    # Convert input to numpy array and create x coordinates
    y_values = reconstruct_piecewise_function(pc_linear_fx)
    y_values = np.array(y_values)
    x_values = np.arange(len(y_values))

    # Initialization
    y_values = np.round(y_values, 6)

    # Upper tunnel boundary points and relationships
    upper_current = (x_values[0], y_values[0] + epsilon)
    upper_left_support = (x_values[0], y_values[0] + epsilon)
    upper_right_support = (x_values[1], y_values[1] + epsilon)
    upper_successors = {(x_values[0], y_values[0] + epsilon): (x_values[1], y_values[1] + epsilon)}
    upper_predecessors = {(x_values[1], y_values[1] + epsilon): (x_values[0], y_values[0] + epsilon)}

    # Lower tunnel boundary points and relationships
    lower_current = (x_values[0], y_values[0] - epsilon)
    lower_left_support = (x_values[0], y_values[0] - epsilon)
    lower_right_support = (x_values[1], y_values[1] - epsilon)
    lower_successors = {(x_values[0], y_values[0] - epsilon): (x_values[1], y_values[1] - epsilon)}
    lower_predecessors = {(x_values[1], y_values[1] - epsilon): (x_values[0], y_values[0] - epsilon)}

    # Result storage
    pivot_points = []
    current_index = 2

    # Maximum iterations to prevent infinite loops
    max_iterations = len(y_values) * 2

    while current_index < len(y_values):
        # Update upper convex hull
        upper_prev_point = (x_values[current_index - 1], y_values[current_index - 1] + epsilon)
        upper_current_point = (x_values[current_index], y_values[current_index] + epsilon)

        iteration_count = 0
        while (upper_prev_point != upper_current) and calculate_angle(upper_current_point, upper_prev_point,
                                                                      upper_predecessors[upper_prev_point],
                                                                      '+') > np.pi:
            upper_prev_point = upper_predecessors[upper_prev_point]
            iteration_count += 1
            if iteration_count > max_iterations:
                break  # Prevent infinite loops

        upper_successors[upper_prev_point] = upper_current_point
        upper_predecessors[upper_current_point] = upper_prev_point

        # Update lower convex hull
        lower_prev_point = (x_values[current_index - 1], y_values[current_index - 1] - epsilon)
        lower_current_point = (x_values[current_index], y_values[current_index] - epsilon)

        iteration_count = 0
        while (lower_prev_point != lower_current) and calculate_angle(lower_current_point, lower_prev_point,
                                                                      lower_predecessors[lower_prev_point],
                                                                      '-') > np.pi:
            lower_prev_point = lower_predecessors[lower_prev_point]
            iteration_count += 1
            if iteration_count > max_iterations:
                break  # Prevent infinite loops

        lower_successors[lower_prev_point] = lower_current_point
        lower_predecessors[lower_current_point] = lower_prev_point

        # Check if upper and lower convex hulls intersect
        if calculate_angle(upper_current_point, upper_left_support, lower_right_support, '+') < np.pi:
            # Hulls intersect - create a new pivot point
            intersection = find_intersection(upper_left_support, lower_right_support, upper_current, lower_current)
            if intersection:
                pivot_points.append(
                    (intersection, upper_left_support, lower_right_support, upper_current, lower_current))

                # Update hull points
                lower_current = lower_right_support
                upper_current = find_intersection(upper_left_support, lower_right_support,
                                                  (x_values[current_index - 1], y_values[current_index - 1] + epsilon),
                                                  upper_current_point)

                if upper_current:
                    upper_successors[upper_current] = upper_current_point
                    upper_predecessors[upper_current_point] = upper_current
                    upper_right_support = upper_current_point
                    lower_right_support = lower_current_point
                    upper_left_support = upper_current
                    lower_left_support = lower_current

                    iteration_count = 0
                    while lower_left_support in lower_successors and calculate_angle(lower_left_support,
                                                                                     upper_right_support,
                                                                                     lower_successors[
                                                                                         lower_left_support],
                                                                                     '-') < np.pi:
                        lower_left_support = lower_successors[lower_left_support]
                        iteration_count += 1
                        if iteration_count > max_iterations:
                            break

        elif calculate_angle(lower_current_point, lower_left_support, upper_right_support, '-') < np.pi:
            # Hulls intersect - create a new pivot point
            intersection = find_intersection(lower_left_support, upper_right_support, lower_current, upper_current)
            if intersection:
                pivot_points.append(
                    (intersection, lower_left_support, upper_right_support, lower_current, upper_current))

                # Update hull points
                upper_current = upper_right_support
                lower_current = find_intersection(lower_left_support, upper_right_support,
                                                  (x_values[current_index - 1], y_values[current_index - 1] - epsilon),
                                                  lower_current_point)

                if lower_current:
                    lower_successors[lower_current] = lower_current_point
                    lower_predecessors[lower_current_point] = lower_current
                    lower_right_support = lower_current_point
                    upper_right_support = upper_current_point
                    lower_left_support = lower_current
                    upper_left_support = upper_current

                    iteration_count = 0
                    while upper_left_support in upper_successors and calculate_angle(upper_left_support,
                                                                                     lower_right_support,
                                                                                     upper_successors[
                                                                                         upper_left_support],
                                                                                     '+') < np.pi:
                        upper_left_support = upper_successors[upper_left_support]
                        iteration_count += 1
                        if iteration_count > max_iterations:
                            break
        else:
            # Update the two separating and supporting lines
            if calculate_angle(upper_current_point, lower_left_support, upper_right_support, '+') < np.pi:
                upper_right_support = upper_current_point

                iteration_count = 0
                while calculate_angle(upper_current_point, lower_left_support, lower_successors[lower_left_support],
                                      '+') < np.pi:
                    lower_left_support = lower_successors[lower_left_support]
                    iteration_count += 1
                    if iteration_count > max_iterations:
                        break

            if calculate_angle(lower_current_point, upper_left_support, lower_right_support, '-') < np.pi:
                lower_right_support = lower_current_point

                iteration_count = 0
                while calculate_angle(lower_current_point, upper_left_support, upper_successors[upper_left_support],
                                      '-') < np.pi:
                    upper_left_support = upper_successors[upper_left_support]
                    iteration_count += 1
                    if iteration_count > max_iterations:
                        break

        current_index += 1

    # Add final pivot points
    intersection1 = find_intersection(upper_left_support, lower_right_support, upper_current, lower_current)
    intersection2 = find_intersection(lower_left_support, upper_right_support, lower_current, upper_current)

    if intersection1 and intersection2:
        midpoint = ((intersection1[0] + intersection2[0]) / 2, (intersection1[1] + intersection2[1]) / 2)
        pivot_points.append((midpoint, lower_right_support, upper_right_support, lower_current, upper_current))

        final_point1 = find_intersection(midpoint, upper_right_support, lower_current_point, upper_current_point)
        final_point2 = find_intersection(midpoint, lower_right_support, lower_current_point, upper_current_point)

        if final_point1 and final_point2:
            final_midpoint = ((final_point1[0] + final_point2[0]) / 2, (final_point1[1] + final_point2[1]) / 2)
            pivot_points.append((final_midpoint, (None, None), (None, None), lower_current_point, upper_current_point))

    optimal_pc_linear_fx = np.array([point[0] for point in pivot_points])
    optimal_num_pieces = len(optimal_pc_linear_fx) - 1
    given_num_pieces = len(pc_linear_fx) - 1
    return optimal_pc_linear_fx, optimal_num_pieces, given_num_pieces
def reconstruct_piecewise_function(pc_linear_fx):
    """
    Reconstructs a piecewise linear function from points.

    Args:
        pivot_points (np.array): Array of (x,y) pivot points defining the piecewise linear function

    Returns:
        np.array: y-values of the reconstructed function
    """
    pivot_points = sorted(pc_linear_fx, key=lambda p: p[0])
    y_values = []
    for i in range(len(pivot_points) - 1):
        start_point = pivot_points[i]
        end_point = pivot_points[i + 1]

        # Handle potential division by zero
        if end_point[0] == start_point[0]:
            continue

        # Calculate line equation: y = mx + b
        slope = (start_point[1] - end_point[1]) / (start_point[0] - end_point[0])
        intercept = start_point[1] - start_point[0] * slope

        # Generate points along the line segment
        for x in range(int(start_point[0]), int(end_point[0])):
            y_values.append(x * slope + intercept)

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
    x_values = np.arange(len(y_values))
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