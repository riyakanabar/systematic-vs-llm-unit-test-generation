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

@njit
def numba_lookahead_split(pc_fx, epsilon):
    """
    Numba-compiled lookahead split algorithm.

    Parameters
    ----------
    pc_fx : (n,2) float64 array
        Includes sentinels [(-inf,inf), (x1,y1), ... (xn,yn), (x_{n+1},inf)]
    epsilon : float

    Returns
    -------
    segs : (m+1,2) float64 array
    num_pieces : int
    given_pieces : int
    """
    X = pc_fx[1:, 0]      # includes right boundary
    Y = pc_fx[1:-1, 1]    # interior only
    n = Y.shape[0]

    out = List()

    i = 0
    while i < n:
        vmin = Y[i]
        vmax = Y[i]
        j = i + 1
        while j < n:
            vmin2 = vmin if vmin < Y[j] else Y[j]
            vmax2 = vmax if vmax > Y[j] else Y[j]

            # check feasibility
            if abs(vmax2 - vmin2) <= 2.0*epsilon + 1e-9*abs(vmin2):
                vmin = vmin2
                vmax = vmax2
                j += 1
            else:
                # choose best split k in [i..j-1] minimizing left band width
                best_k = i
                best_width = 1e308
                cur_min = Y[i]
                cur_max = Y[i]
                for k in range(i, j):
                    yk = Y[k]
                    if yk < cur_min:
                        cur_min = yk
                    if yk > cur_max:
                        cur_max = yk
                    width = cur_max - cur_min
                    if width < best_width:
                        best_width = width
                        best_k = k

                # compute c = midpoint of min/max in [i..best_k]
                block_min = Y[i]
                block_max = Y[i]
                for kk in range(i+1, best_k+1):
                    ykk = Y[kk]
                    if ykk < block_min:
                        block_min = ykk
                    if ykk > block_max:
                        block_max = ykk
                c = 0.5*(block_min + block_max)

                out.append((X[i], c))
                i = best_k + 1
                break
        else:
            # j == n: close segment
            c = 0.5*(vmin + vmax)
            out.append((X[i], c))
            i = j

    # finalize with right boundary
    segs = np.empty((len(out)+1, 2), dtype=np.float64)
    for k in range(len(out)):
        segs[k, 0] = out[k][0]
        segs[k, 1] = out[k][1]
    segs[len(out), 0] = X[-1]
    segs[len(out), 1] = np.inf

    return segs, len(out), n

@njit
def numba_agglomerative_yspread(pc_fx, eps):
    """
    Bottom-up agglomerative merge by smallest y-spread.
    Numba version (no heapq).
    pc_fx: (n,2) float64 array with [(-inf,inf),(x1,y1),...,(xn,yn),(x_{n+1},inf)]
    eps: float
    Returns: (out_segments, num_pieces, given_pieces)
    """

    n = pc_fx.shape[0] - 2  # number of true pieces
    if n <= 0:
        segs = np.empty((1,2),dtype=np.float64)
        segs[0,0] = pc_fx[-1,0]
        segs[0,1] = np.inf
        return segs, 0, 0

    X = pc_fx[1:-1,0]
    Y = pc_fx[1:-1,1]

    alive = np.ones(n, dtype=np.bool_)  # all active initially

    changed = True
    while changed:
        changed = False
        best_s = 1e308
        best_i = -1
        for i in range(n-1):
            if not alive[i] or not alive[i+1]:
                continue
            lo = min(Y[i], Y[i+1])
            hi = max(Y[i], Y[i+1])
            if abs(hi - lo) <= 2.0*eps + 1e-9*abs(lo):
                s = hi - lo
                if s < best_s:
                    best_s = s
                    best_i = i
        if best_i != -1:
            # merge best_i and best_i+1
            alive[best_i+1] = False
            changed = True

    # Build blocks
    out = []
    i = 0
    while i < n:
        if not alive[i]:
            i += 1
            continue
        lo = Y[i] - eps
        hi = Y[i] + eps
        x_left = X[i]
        j = i+1
        while j < n and not alive[j]:
            yj = Y[j]
            lo = max(lo, yj - eps)
            hi = min(hi, yj + eps)
            j += 1
        val = 0.5*(lo+hi)
        out.append((x_left, val))
        i = j

    # Convert to numpy array with boundary
    m = len(out)
    segs = np.empty((m+1,2), dtype=np.float64)
    for k in range(m):
        segs[k,0] = out[k][0]
        segs[k,1] = out[k][1]
    segs[m,0] = pc_fx[-1,0]
    segs[m,1] = np.inf

    return segs, m, n

@njit
def _best_split(Y, i, j):
    """
    Choose k in [i, j-1] minimizing max(range(i..k), range(k+1..j)).
    """
    best_k = i
    best_cost = 1e308

    pre_min = np.empty(j - i + 1, dtype=np.float64)
    pre_max = np.empty(j - i + 1, dtype=np.float64)
    suf_min = np.empty(j - i + 1, dtype=np.float64)
    suf_max = np.empty(j - i + 1, dtype=np.float64)

    cur_min = Y[i]
    cur_max = Y[i]
    for t in range(i, j + 1):
        if Y[t] < cur_min:
            cur_min = Y[t]
        if Y[t] > cur_max:
            cur_max = Y[t]
        pre_min[t - i] = cur_min
        pre_max[t - i] = cur_max

    cur_min = Y[j]
    cur_max = Y[j]
    for t in range(j, i - 1, -1):
        if Y[t] < cur_min:
            cur_min = Y[t]
        if Y[t] > cur_max:
            cur_max = Y[t]
        suf_min[t - i] = cur_min
        suf_max[t - i] = cur_max

    for k in range(i, j):
        left_range = pre_max[k - i] - pre_min[k - i]
        right_range = suf_max[k + 1 - i] - suf_min[k + 1 - i]
        cost = left_range if left_range > right_range else right_range
        if cost < best_cost:
            best_cost = cost
            best_k = k

    return best_k


@njit
def numba_binary_split(pc_fx, epsilon):
    """
    Binary split algorithm in Numba.

    Parameters
    ----------
    pc_fx : (n,2) float64 array with sentinels
    epsilon : float

    Returns
    -------
    segs : (m+1,2) float64 array
    num_pieces : int
    given_pieces : int
    """
    X = pc_fx[1:, 0]      # includes right boundary
    Y = pc_fx[1:-1, 1]    # interior values
    n = Y.shape[0]

    # stack of (i,j) indices
    stack = List()
    stack.append((0, n - 1))

    segments = List()  # (i,j,c)

    while len(stack) > 0:
        i, j = stack.pop()
        # compute min/max in [i..j]
        vmin = Y[i]
        vmax = Y[i]
        for t in range(i + 1, j + 1):
            if Y[t] < vmin:
                vmin = Y[t]
            if Y[t] > vmax:
                vmax = Y[t]

        if abs(vmax - vmin) <= 2.0 * epsilon + 1e-9 * abs(vmin):
            c = 0.5 * (vmin + vmax)
            segments.append((i, j, c))
        else:
            k = _best_split(Y, i, j)
            stack.append((k + 1, j))
            stack.append((i, k))

    # sort by start index
    # simple insertion sort (since n small)
    for a in range(len(segments)):
        for b in range(a + 1, len(segments)):
            if segments[b][0] < segments[a][0]:
                tmp = segments[a]
                segments[a] = segments[b]
                segments[b] = tmp

    # build output array
    m = len(segments)
    segs = np.empty((m + 1, 2), dtype=np.float64)
    for k in range(m):
        s, e, c = segments[k]
        segs[k, 0] = X[s]
        segs[k, 1] = c
    segs[m, 0] = X[-1]
    segs[m, 1] = np.inf

    return segs, m, n



