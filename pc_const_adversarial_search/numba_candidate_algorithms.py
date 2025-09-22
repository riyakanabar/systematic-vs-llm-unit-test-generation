import numpy as np
from numba import njit
from numba.typed import List

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


@njit
def _rec_split2(X, Y, i, j, epsilon):
    segs = List()

    # base case: single interior point
    if i == j:
        segs.append((X[i], float(Y[i])))
        return segs

    # compute min and max
    mn, mx = Y[i], Y[i]
    for t in range(i+1, j+1):
        y = Y[t]
        if y < mn:
            mn = y
        if y > mx:
            mx = y

    # ε-feasible? mimic np.isclose(mx, mn, atol=2*eps, rtol=1e-9)
    if abs(mx - mn) <= 2.0 * epsilon + 1e-9 * abs(mn):
        segs.append((X[i], 0.5 * (mn + mx)))
        return segs

    # otherwise: split where deviation from midpoint is largest
    mid = 0.5 * (mn + mx)
    best_dev = -1.0
    s = -1
    for t in range(i+1, j+1):   # ensure both sides non-empty
        dev = abs(Y[t] - mid)
        if dev > best_dev:
            best_dev = dev
            s = t
    if s <= i or s > j:         # safe fallback split
        s = (i + j + 1) // 2

    left = _rec_split2(X, Y, i, s-1, epsilon)
    right = _rec_split2(X, Y, s, j, epsilon)

    for u in left:
        segs.append(u)
    for u in right:
        segs.append(u)

    return segs

@njit
def numba_recursive_split2(pc_fx, epsilon):
    """
    Numba-compiled version of recursive_split2.

    Parameters
    ----------
    pc_fx : (n,2) float64 array
        Piecewise-constant function representation with boundaries.
    epsilon : float

    Returns
    -------
    segs : (p+1,2) float64 array
    num_pieces : int
    given_pieces : int
    """
    # Extract interior grid
    X = pc_fx[1:, 0]      # includes last boundary
    Y = pc_fx[1:-1, 1]    # interior values
    n = Y.shape[0]

    if n == 0:
        segs = np.empty((1, 2), dtype=np.float64)
        segs[0, 0] = X[-1]
        segs[0, 1] = np.inf
        return segs, 0, 0

    lst = _rec_split2(X, Y, 0, n-1, float(epsilon))

    # convert typed.List → numpy array
    segs = np.empty((len(lst)+1, 2), dtype=np.float64)
    for k in range(len(lst)):
        segs[k, 0] = lst[k][0]
        segs[k, 1] = lst[k][1]
    segs[len(lst), 0] = X[-1]
    segs[len(lst), 1] = np.inf

    return segs, len(lst), n

