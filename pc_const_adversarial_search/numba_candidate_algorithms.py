import numpy as np
from numba import njit

@njit
def rec(pc_fx, epsilon, start_idx, end_idx):
    # Get segment values
    ys = pc_fx[start_idx:end_idx+1, 1]
    max_y = np.max(ys)
    min_y = np.min(ys)

    if abs(max_y - min_y) <= 2*epsilon + 1e-9 * abs(min_y):
        y_value = (max_y + min_y) / 2
        return np.array([[pc_fx[start_idx, 0], y_value]])

    # Find index of max error
    mid_idx = -1
    max_error = -1.0
    mid_value = (max_y + min_y) / 2
    for i in range(start_idx+1, end_idx):
        y = pc_fx[i, 1]
        if y > max_y or y < min_y:
            continue
        error = abs(y - mid_value)
        if error > max_error:
            max_error = error
            mid_idx = i

    if mid_idx == -1 or start_idx == mid_idx or end_idx == mid_idx:
        y_value = (max_y + min_y) / 2
        return np.array([[pc_fx[start_idx, 0], y_value]])

    # Recurse on left and right parts
    left = rec(pc_fx, epsilon, start_idx, mid_idx)
    right = rec(pc_fx, epsilon, mid_idx, end_idx)
    return np.vstack((left, right))

@njit
def numba_recursive_split1(pc_fx, epsilon):
    segments = rec(pc_fx, epsilon, 1, pc_fx.shape[0]-2)

    # Append last boundary
    last_row = np.array([[pc_fx[-1, 0], np.inf]])
    segments = np.vstack((segments, last_row))

    num_pieces = segments.shape[0] - 1
    given_pieces = pc_fx.shape[0] - 2
    return segments, num_pieces, given_pieces
