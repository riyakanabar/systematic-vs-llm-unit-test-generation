import numpy as np
from numba import njit
import matplotlib.pyplot as plt
#sliding window - heuristic

def approximate_pc_cons_fx(pc_fx, epsilon):
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

def approximate_pc_shortest_path(pc_fx, epsilon):
    optimal_pc_fx = []
    n = len(pc_fx) - 2  # Excluding boundary points

    # Compute upper and lower bounds
    U = [pc_fx[i][1] + epsilon for i in range(1, n + 1)]
    L = [pc_fx[i][1] - epsilon for i in range(1, n + 1)]

    i = 0  # Start at the first segment
    while i < n:
        U_max, L_min = float('inf'), -float('inf')
        k = i + 1 # next segment

        # Find the furthest reachable segment satisfying conditions
        while k <= n:
            new_U_max = min(U_max, U[k - 1])
            new_L_min = max(L_min, L[k - 1])

            if new_U_max >= new_L_min and U[i] >= new_L_min and L[i] <= new_U_max:
                U_max = new_U_max
                L_min = new_L_min
                k += 1
            else:
                break

        segment_value = (U_max + L_min) / 2
        optimal_pc_fx.append([pc_fx[i + 1][0], segment_value])
        i = k - 1  # Move to next segment

    # Append last boundary point
    optimal_pc_fx.append([pc_fx[-1][0], float('inf')])

    optimal_num_pieces = len(optimal_pc_fx) - 1
    given_num_pieces = n

    return optimal_pc_fx, optimal_num_pieces, given_num_pieces

def plot_pc_cons_fx(pc_fx, optimal_pc_fx):
    plt.figure(figsize=(10, 8))
    for i in range(1, len(pc_fx) - 1):
        x_start = pc_fx[i][0]
        x_end = pc_fx[i + 1][0]
        y_value = pc_fx[i][1]
        plt.hlines(y_value, x_start, x_end, colors='blue', linewidth=2, alpha=0.7,
                   label='Given Function' if i == 1 else "")

    for i in range(len(optimal_pc_fx) - 1):
        x_start = optimal_pc_fx[i][0]
        x_end = optimal_pc_fx[i + 1][0]
        y_value = optimal_pc_fx[i][1]
        plt.hlines(y_value, x_start, x_end, colors='red', linestyles='dashed', linewidth=2, alpha=0.7,
                   label='Optimized Function' if i == 0 else "")

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Comparison of Given and Optimized Piecewise Constant Functions')
    plt.legend(loc='lower right', bbox_to_anchor=(1.1, -0.12))  # Moves legend outside
    plt.grid(True)
    plt.margins(x=0)
    plt.show()

def plot_single_pc_fx(pc_cons_fx):
    for i in range(1, len(pc_cons_fx) - 1):
        x_start = pc_cons_fx[i][0]
        x_end = pc_cons_fx[i + 1][0]
        y_value = pc_cons_fx[i][1]
        plt.hlines(y_value, x_start, x_end, colors='blue', linewidth=2, alpha=0.7,
                   label='Piecewise Constant Function' if i == 1 else "")

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.show()
