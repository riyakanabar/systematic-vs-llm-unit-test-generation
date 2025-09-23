import numpy as np
from numba import njit, types
from numba.typed import List

@njit(cache=True)
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

@njit(cache=True)
def numba_recursive_split1(pc_fx, epsilon):
    segments = rec(pc_fx, epsilon, 1, pc_fx.shape[0]-2)

    # Append last boundary
    last_row = np.array([[pc_fx[-1, 0], np.inf]])
    segments = np.vstack((segments, last_row))

    num_pieces = segments.shape[0] - 1
    given_pieces = pc_fx.shape[0] - 2
    return segments, num_pieces, given_pieces


@njit(cache=True)
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

@njit(cache=True)
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

@njit(cache=True)
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

@njit(cache=True)
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

@njit(cache=True)
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


@njit(cache=True)
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

@njit(cache=True)
def numba_pruned_dp(pc_fx, eps):
    """
    Numba-optimized pruned_dp.

    Parameters
    ----------
    pc_fx : np.ndarray of shape (n+2, 2)
        Array including boundary points [(-inf, inf), (x1,y1), ..., (xn,yn), (x_{n+1}, inf)]
    eps : float
        epsilon tolerance

    Returns
    -------
    optimal_pc_fx : np.ndarray of shape (m, 2)
        Output approximation with boundary points
    m : int
        number of approximation pieces
    n : int
        number of original pieces
    """
    n = pc_fx.shape[0] - 2  # exclude boundary points
    INF = 10 ** 9

    # dp arrays
    dp = np.full(n + 1, INF, dtype=np.int64)
    prev = np.full(n + 1, -1, dtype=np.int64)
    dp[0] = 0

    xs = pc_fx[:, 0]
    ys = pc_fx[:, 1]

    # DP loop
    for i in range(1, n + 1):
        lo = ys[i] - eps
        hi = ys[i] + eps
        j = i - 1
        while j >= 0:
            if j < i - 1:
                y = ys[j + 1]
                lo = max(lo, y - eps)
                hi = min(hi, y + eps)
            if lo > hi:
                break
            if dp[j] + 1 < dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
            j -= 1

    # Reconstruct solution
    out_x = np.empty(n + 2, dtype=np.float64)
    out_y = np.empty(n + 2, dtype=np.float64)
    m = 0

    i = n
    while i > 0:
        j = prev[i]
        lo = -np.inf
        hi = np.inf
        for k in range(j, i):
            y = ys[k + 1]
            lo = max(lo, y - eps)
            hi = min(hi, y + eps)
        val = 0.5 * (lo + hi)
        out_x[m] = xs[j + 1]
        out_y[m] = val
        m += 1
        i = j

    # Reverse results in-place
    for k in range(m // 2):
        kk = m - 1 - k
        tmpx, tmpy = out_x[k], out_y[k]
        out_x[k], out_y[k] = out_x[kk], out_y[kk]
        out_x[kk], out_y[kk] = tmpx, tmpy

    # Add last boundary point
    out_x[m] = xs[-1]
    out_y[m] = np.inf
    m += 1

    # Build final output (trim unused slots)
    optimal_pc_fx = np.empty((m, 2), dtype=np.float64)
    for t in range(m):
        optimal_pc_fx[t, 0] = out_x[t]
        optimal_pc_fx[t, 1] = out_y[t]

    return optimal_pc_fx, m - 1, n


@njit(cache=True)
def numba_beam_search(pc_fx, epsilon, beam_size=8):
    """
    Numba-safe beam search (no np.lexsort, no Python min/max).
    pc_fx: ndarray (n+2,2) with sentinels [(-inf, inf), (x1,y1), ... , (x_{n}, y_{n}), (x_{n+1}, inf)]
    Returns: (out_segments ndarray (m+1,2) incl. last boundary, m pieces, n original pieces)
    """
    X = pc_fx[:, 0]
    Y = pc_fx[:, 1]
    n = pc_fx.shape[0] - 2  # exclude boundaries

    # ---------- precompute feasibility: furthest j reachable from i ----------
    furthest = np.empty(n, dtype=np.int64)
    for i in range(n):
        vmin = Y[i+1]
        vmax = Y[i+1]
        j = i
        while j < n:
            ycur = Y[j+1]
            if ycur < vmin:
                vmin = ycur
            if ycur > vmax:
                vmax = ycur
            diff = vmax - vmin
            if diff < 0.0:
                diff = -diff
            # ref = max(1.0, abs(vmax), abs(vmin)) without max()
            ref = 1.0
            av = vmax
            if av < 0.0:
                av = -av
            if av > ref:
                ref = av
            bv = vmin
            if bv < 0.0:
                bv = -bv
            if bv > ref:
                ref = bv
            tol = 2.0 * epsilon + 1e-9 * ref
            if diff <= tol:
                j += 1
            else:
                break
        furthest[i] = j - 1

    # ---------- state representation (frontier) ----------
    # We'll store frontier as fixed arrays (no dicts). Each state points to a node in a pool that lets us backtrack.
    max_states = beam_size * (n + 1)  # per layer cap
    pieces = np.empty(max_states, dtype=np.int64)
    neg_span = np.empty(max_states, dtype=np.float64)
    last_idx = np.empty(max_states, dtype=np.int64)   # ending index j in [0..n-1], or -1 for root
    parent_state = np.empty(max_states, dtype=np.int64)  # parent state index in previous layer (only for bookkeeping here)
    node_id_of_state = np.empty(max_states, dtype=np.int64)  # id into node pool
    state_count = 0

    # ---------- node pool for backtracking ----------
    # Each new state adds one node that records (start_x, c) and a link to previous node.
    # Pool size is capped; if you hit it, reduce beam_size.
    max_nodes = max_states * (n + 1)
    node_start_x = np.empty(max_nodes, dtype=np.float64)
    node_c = np.empty(max_nodes, dtype=np.float64)
    node_parent = np.empty(max_nodes, dtype=np.int64)
    node_count = 0

    # root "state" (no segment)
    pieces[0] = 0
    neg_span[0] = 0.0
    last_idx[0] = -1
    parent_state[0] = -1
    node_id_of_state[0] = -1  # root has no node
    state_count = 1

    # ------------- main expansion loop -------------
    while True:
        # generate candidates
        n_pieces = np.empty(max_states, dtype=np.int64)
        n_neg_span = np.empty(max_states, dtype=np.float64)
        n_last_idx = np.empty(max_states, dtype=np.int64)
        n_parent_state = np.empty(max_states, dtype=np.int64)
        n_node_id = np.empty(max_states, dtype=np.int64)
        new_count = 0
        any_progress = False

        for si in range(state_count):
            li = last_idx[si]      # previous segment ended at li
            i = li + 1             # next start
            pcs = pieces[si]
            ns = neg_span[si]
            chain_node = node_id_of_state[si]

            if i >= n:
                # already complete — carry forward as a "complete" candidate with end at n-1
                if new_count < max_states:
                    n_pieces[new_count] = pcs
                    n_neg_span[new_count] = ns
                    n_last_idx[new_count] = n - 1
                    n_parent_state[new_count] = si
                    n_node_id[new_count] = chain_node
                    new_count += 1
                continue

            jmax = furthest[i]
            if jmax < i:
                jmax = i
            any_progress = True

            for j in range(jmax, i - 1, -1):  # prefer longer extensions first
                # compute [vmin, vmax] over Y[i..j]
                vmin = Y[i+1]
                vmax = Y[i+1]
                kk = i
                while kk <= j:
                    ycur = Y[kk+1]
                    if ycur < vmin:
                        vmin = ycur
                    if ycur > vmax:
                        vmax = ycur
                    kk += 1
                c = 0.5 * (vmin + vmax)
                # span addition
                span_add = 0.0
                if (j + 1) < X.shape[0]:
                    span_add = X[j+1 + 1] - X[i + 1]  # +1 because X has boundary at 0
                # add candidate
                if new_count < max_states and node_count < max_nodes:
                    # create node for this segment
                    node_start_x[node_count] = X[i + 1]  # piece starts at X[i+1] (skip left boundary)
                    node_c[node_count] = c
                    node_parent[node_count] = chain_node
                    n_pieces[new_count] = pcs + 1
                    n_neg_span[new_count] = ns - span_add
                    n_last_idx[new_count] = j
                    n_parent_state[new_count] = si
                    n_node_id[new_count] = node_count
                    node_count += 1
                    new_count += 1
                else:
                    # out of capacity; stop expanding further
                    break
            # capacity guard
            if new_count >= max_states:
                break

        if not any_progress:
            # nothing more to expand; either we already carried completes or nothing is possible
            # choose the best complete among candidates (end == n-1), if any
            best_idx = -1
            for ci in range(new_count):
                if n_last_idx[ci] == n - 1:
                    if best_idx == -1:
                        best_idx = ci
                    else:
                        # better if fewer pieces, or equal pieces and smaller neg_span
                        better = False
                        if n_pieces[ci] < n_pieces[best_idx]:
                            better = True
                        elif n_pieces[ci] == n_pieces[best_idx] and n_neg_span[ci] < n_neg_span[best_idx]:
                            better = True
                        if better:
                            best_idx = ci
            if best_idx == -1:
                # fallback
                out = np.empty((2, 2), dtype=np.float64)
                out[0, 0] = X[1]; out[0, 1] = Y[1]
                out[1, 0] = X[-1]; out[1, 1] = np.inf
                return out, 1, n
            # reconstruct from best complete candidate
            return _reconstruct_from_node_pool(n_node_id[best_idx], X[-1],
                                               node_start_x, node_c, node_parent), int(n_pieces[best_idx]), n

        # ---------- beam prune per ending index ----------
        # For each key in [0..n-1], keep top beam_size by (pieces asc, neg_span asc)
        # (We gather them into the next frontier arrays.)
        state_count = 0
        for key in range(n):
            # small fixed-size buffer for this key
            buf_used = 0
            buf_idx = np.empty(beam_size, dtype=np.int64)
            buf_pcs = np.empty(beam_size, dtype=np.int64)
            buf_span = np.empty(beam_size, dtype=np.float64)

            # collect best K for this key
            for ci in range(new_count):
                if n_last_idx[ci] != key:
                    continue
                if buf_used < beam_size:
                    buf_idx[buf_used] = ci
                    buf_pcs[buf_used] = n_pieces[ci]
                    buf_span[buf_used] = n_neg_span[ci]
                    buf_used += 1
                else:
                    # find worst in buffer
                    worst = 0
                    wi = 1
                    while wi < buf_used:
                        worse = False
                        if buf_pcs[wi] > buf_pcs[worst]:
                            worse = True
                        elif buf_pcs[wi] == buf_pcs[worst] and buf_span[wi] > buf_span[worst]:
                            worse = True
                        if worse:
                            worst = wi
                        wi += 1
                    # if candidate better than worst, replace
                    better = False
                    if n_pieces[ci] < buf_pcs[worst]:
                        better = True
                    elif n_pieces[ci] == buf_pcs[worst] and n_neg_span[ci] < buf_span[worst]:
                        better = True
                    if better:
                        buf_idx[worst] = ci
                        buf_pcs[worst] = n_pieces[ci]
                        buf_span[worst] = n_neg_span[ci]

            # selection sort the buffer (small K) by (pieces, neg_span)
            a = 0
            while a < buf_used:
                minpos = a
                b = a + 1
                while b < buf_used:
                    better = False
                    if buf_pcs[b] < buf_pcs[minpos]:
                        better = True
                    elif buf_pcs[b] == buf_pcs[minpos] and buf_span[b] < buf_span[minpos]:
                        better = True
                    if better:
                        minpos = b
                    b += 1
                if minpos != a:
                    # swap
                    tmpi = buf_idx[a]; tmpp = buf_pcs[a]; tmps = buf_span[a]
                    buf_idx[a] = buf_idx[minpos]; buf_pcs[a] = buf_pcs[minpos]; buf_span[a] = buf_span[minpos]
                    buf_idx[minpos] = tmpi; buf_pcs[minpos] = tmpp; buf_span[minpos] = tmps
                a += 1

            # append pruned states for this key to next frontier
            bi = 0
            while bi < buf_used and state_count < max_states:
                ci = buf_idx[bi]
                pieces[state_count] = n_pieces[ci]
                neg_span[state_count] = n_neg_span[ci]
                last_idx[state_count] = n_last_idx[ci]
                parent_state[state_count] = n_parent_state[ci]  # (not needed for backtrack)
                node_id_of_state[state_count] = n_node_id[ci]
                state_count += 1
                bi += 1

        # if any complete (key == n-1) reached, choose best and return
        best_idx = -1
        si = 0
        while si < state_count:
            if last_idx[si] == n - 1:
                if best_idx == -1:
                    best_idx = si
                else:
                    better = False
                    if pieces[si] < pieces[best_idx]:
                        better = True
                    elif pieces[si] == pieces[best_idx] and neg_span[si] < neg_span[best_idx]:
                        better = True
                    if better:
                        best_idx = si
            si += 1
        if best_idx != -1:
            return _reconstruct_from_node_pool(node_id_of_state[best_idx], X[-1],
                                               node_start_x, node_c, node_parent), int(pieces[best_idx]), n

    # fallback (shouldn’t hit)
    out = np.empty((2, 2), dtype=np.float64)
    out[0, 0] = X[1]; out[0, 1] = Y[1]
    out[1, 0] = X[-1]; out[1, 1] = np.inf
    return out, 1, n


@njit(cache=True)
def _reconstruct_from_node_pool(last_node_id, x_right, node_start_x, node_c, node_parent):
    # unwind nodes → segments, then add last boundary
    # count
    cnt = 0
    nid = last_node_id
    while nid != -1:
        cnt += 1
        nid = node_parent[nid]
    segs = np.empty((cnt + 1, 2), dtype=np.float64)  # +1 for final boundary
    # fill reversed
    nid = last_node_id
    idx = cnt - 1
    while nid != -1:
        segs[idx, 0] = node_start_x[nid]
        segs[idx, 1] = node_c[nid]
        nid = node_parent[nid]
        idx -= 1
    # append boundary
    segs[cnt, 0] = x_right
    segs[cnt, 1] = np.inf
    return segs

