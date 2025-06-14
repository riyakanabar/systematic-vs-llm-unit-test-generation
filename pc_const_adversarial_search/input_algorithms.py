import numpy as np

def variant1(pc_fx, epsilon): #approximate_pc_cons_fx function - optimal variant suggested by prof
    optimal_pc_fx = []
    min_val = pc_fx[1][1]  # Initialize min_val value
    max_val = pc_fx[1][1]  # Initialize max_val value
    x = pc_fx[1][0]

    for i in range(2, len(pc_fx) - 1):
        yi = pc_fx[i][1]
        min_old, max_old = min_val, max_val
        if yi < min_val :
            min_val = yi
            if not np.isclose(min_val, max_val, atol = 2*epsilon, rtol = 1e-9):  # If exceeding threshold
                y_value = (max_val + min_old) / 2  # Take midpoint before update
                optimal_pc_fx.append([x, y_value])  # Append segment
                x = pc_fx[i][0]  # Start new segment
                min_val = max_val = yi  # Reset min_val/max_val
        elif yi > max_val:
            max_val = yi
            if not np.isclose(min_val, max_val, atol = 2 * epsilon, rtol=1e-9):
                y_value = (max_old + min_val) / 2  # Take midpoint before update
                optimal_pc_fx.append([x, y_value])  # Append segment
                x = pc_fx[i][0]  # Start new segment
                min_val = max_val = yi  # Reset min_val/max_val

    # Store the last segment
    y_value = (max_val + min_val) / 2
    optimal_pc_fx.append([x, y_value])
    optimal_pc_fx.append([pc_fx[-1][0], float('inf')])  # Append last boundary
    optimal_num_pieces = len(optimal_pc_fx) - 1
    given_num_pieces = len(pc_fx) - 2
    return optimal_pc_fx, optimal_num_pieces, given_num_pieces

