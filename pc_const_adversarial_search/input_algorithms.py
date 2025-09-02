from optimal_algorithms.pc_cons_apx import approximate_pc_cons_fx
from grid_search.get_variants import variant_function, loop_variations
import functools
import operator
import numpy as np

#approximate_pc_cons_fx function - sliding window technique - optimal variant suggested by prof
variant1 = approximate_pc_cons_fx
variant2 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[1],
        params_min=[1,2,1,2,-1],
        params_max=[1,1,1,1,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )
variant3 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[2],
        params_min=[1,1,1,1,-1],
        params_max=[1,1,1,1,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )
variant5 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[1],
        params_min=[1,1,1,1,-1],
        params_max=[1,1,1,1,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )
#default algorithm - not a variant
variant6 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[0],
        params_min=[1,1,1,1,-1],
        params_max=[1,1,1,1,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )


def variant7(pc_fx, epsilon):
        """
        Non-optimal greedy algorithm for approximating a piecewise constant function
        using a top-down ε-satisfying split.
        """

        def recursive_split(start_idx, end_idx):
                segment = pc_fx[start_idx:end_idx + 1]
                ys = np.array([y for _, y in segment])
                max_y = np.max(ys)
                min_y = np.min(ys)

                if np.isclose(max_y, min_y, atol=2 * epsilon, rtol=1e-9):
                        y_value = (max_y + min_y) / 2
                        return [[pc_fx[start_idx][0], y_value]]

                # Find index of max error
                mid_idx = -1
                max_error = -1
                for i in range(start_idx + 1, end_idx):
                        y = pc_fx[i][1]
                        if y > max_y or y < min_y:
                                continue
                        error = abs(y - (max_y + min_y) / 2)
                        if error > max_error:
                                max_error = error
                                mid_idx = i

                if mid_idx == -1 or start_idx == mid_idx or end_idx == mid_idx:
                        y_value = (max_y + min_y) / 2
                        return [[pc_fx[start_idx][0], y_value]]

                left = recursive_split(start_idx, mid_idx)
                right = recursive_split(mid_idx, end_idx)
                return left + right

        # Call recursive splitting on points between -inf and +inf
        segments = recursive_split(1, len(pc_fx) - 2)
        segments.append([pc_fx[-1][0], float('inf')])

        num_pieces = len(segments) - 1
        given_pieces = len(pc_fx) - 2
        return segments, num_pieces, given_pieces

def extract_XY(pc_fx):
    """Extract arrays X=[x1..x_{n+1}], Y=[y1..y_n], n=pieces from boundary-sentinel input."""
    n = len(pc_fx) - 2
    X = [pc_fx[j][0] for j in range(1, n+1)] + [pc_fx[-1][0]]
    Y = [pc_fx[j][1] for j in range(1, n+1)]
    return X, Y, n

def pc_lookahead_split(pc_fx, epsilon):
    X, Y, n = extract_XY(pc_fx)
    out = []
    i = 0
    while i < n:
        vmin = vmax = Y[i]
        j = i + 1
        while j < n:
            vmin2 = min(vmin, Y[j]); vmax2 = max(vmax, Y[j])
            if vmax2 - vmin2 <= 2*epsilon:
                vmin, vmax = vmin2, vmax2
                j += 1
            else:
                # choose best split k in [i..j-1] minimizing left band width
                best_k = i
                best_width = float('inf')
                cur_min, cur_max = Y[i], Y[i]
                for k in range(i, j):  # inclusive
                    cur_min = min(cur_min, Y[k]); cur_max = max(cur_max, Y[k])
                    width = cur_max - cur_min
                    if width < best_width:
                        best_width = width; best_k = k
                c = 0.5*( (min(Y[i:best_k+1]) + max(Y[i:best_k+1])) )
                out.append([X[i], c])
                i = best_k + 1
                break
        else:
            # j == n: close segment
            c = 0.5*(vmin + vmax)
            out.append([X[i], c])
            i = j
    out.append([X[-1], float('inf')])
    return out, len(out)-1, n

def pc_binary_split(pc_fx, epsilon):
    X, Y, n = extract_XY(pc_fx)

    def best_split(i, j):
        # choose k in [i, j-1] minimizing max(range(i..k), range(k+1..j))
        best_k, best_cost = None, float('inf')
        # prefix mins/maxes for speed
        pre_min, pre_max = [0]*(j-i+1), [0]*(j-i+1)
        suf_min, suf_max = [0]*(j-i+1), [0]*(j-i+1)
        cur_min = cur_max = Y[i]
        for t in range(i, j+1):
            cur_min = min(cur_min, Y[t]); cur_max = max(cur_max, Y[t])
            pre_min[t-i], pre_max[t-i] = cur_min, cur_max
        cur_min = cur_max = Y[j]
        for t in range(j, i-1, -1):
            cur_min = min(cur_min, Y[t]); cur_max = max(cur_max, Y[t])
            suf_min[t-i], suf_max[t-i] = cur_min, cur_max
        for k in range(i, j):
            left_range  = pre_max[k-i] - pre_min[k-i]
            right_range = suf_max[k+1-i] - suf_min[k+1-i]
            cost = max(left_range, right_range)
            if cost < best_cost:
                best_cost, best_k = cost, k
        return best_k

    segments = []
    stack = [(0, n-1)]
    while stack:
        i, j = stack.pop()
        vmin = min(Y[i:j+1]); vmax = max(Y[i:j+1])
        if vmax - vmin <= 2*epsilon:
            c = 0.5*(vmin + vmax)
            segments.append((i, j, c))
        else:
            k = best_split(i, j)
            stack.append((k+1, j))
            stack.append((i, k))

    # order by start index and emit in required format
    segments.sort(key=lambda t: t[0])
    out = [[X[s], c] for (s, e, c) in segments]
    out.append([X[-1], float('inf')])
    return out, len(out)-1, n

def pc_beam_search(pc_fx, epsilon, beam_size=8):
    X, Y, n = extract_XY(pc_fx)

    # precompute feasibility: furthest j you can reach from i
    furthest = [0]*n
    for i in range(n):
        vmin = vmax = Y[i]
        j = i
        while j < n:
            vmin = min(vmin, Y[j]); vmax = max(vmax, Y[j])
            if vmax - vmin <= 2*epsilon:
                j += 1
            else:
                break
        furthest[i] = j-1

    # state: (pieces_so_far, -total_span, last_index, segments_list)
    # segments_list holds [ [X[i], c], ... ]
    init = (0, 0.0, -1, [])
    frontier = [init]

    for start in range(n):  # we advance index via states, not this loop
        pass  # dummy to emphasize no outer sweep

    # Use a dict keyed by last_index to keep top beam_size states per frontier layer
    states = { -1: [init] }

    # Expand until last_index == n-1
    while True:
        new_states = {}
        any_progress = False
        for last_idx, bucket in list(states.items()):
            for (pieces, neg_span, li, segs) in bucket:
                i = li + 1
                if i >= n:
                    # already complete
                    key = n-1
                    new_states.setdefault(key, []).append((pieces, neg_span, li, segs))
                    continue
                jmax = furthest[i]
                if jmax < i:
                    # infeasible single point (shouldn't happen), force cut
                    jmax = i
                any_progress = True
                for j in range(jmax, i-1, -1):  # prefer longer extensions first
                    vmin = min(Y[i:j+1]); vmax = max(Y[i:j+1])
                    c = 0.5*(vmin + vmax)
                    span_add = X[j+1] - X[i] if j+1 < len(X) else 0.0
                    new_segs = segs + [[X[i], c]]
                    new_state = (pieces+1, neg_span - span_add, j, new_segs)
                    new_states.setdefault(j, []).append(new_state)

        # beam prune per ending index
        if not any_progress:
            break
        pruned = {}
        for key, arr in new_states.items():
            arr.sort()  # by pieces asc, then -span asc (i.e., span desc)
            pruned[key] = arr[:beam_size]
        states = pruned
        if n-1 in states:
            # we have complete segmentations; return the best one
            best = min(states[n-1])  # by pieces, then by -span
            pieces, neg_span, li, segs = best
            out = segs + [[X[-1], float('inf')]]
            return out, len(out)-1, n

    # Fallback (shouldn't trigger)
    out = [[X[0], Y[0]], [X[-1], float('inf')]]
    return out, len(out)-1, n
def pc_quantized_rle(pc_fx, epsilon, centers=None):
    X, Y, n = extract_XY(pc_fx)
    if centers is None:
        # use unique sorted Y as candidate centers (or provide your own grid)
        centers = sorted(set(Y))

    # assign each y_i to nearest center within epsilon; otherwise use y_i itself
    labels = []
    for yi in Y:
        best = None; best_err = float('inf')
        for c in centers:
            err = abs(yi - c)
            if err < best_err:
                best_err, best = err, c
        if best is not None and best_err <= epsilon:
            labels.append(best)
        else:
            labels.append(yi)  # fallback: singleton feasible center

    # compress contiguous equal labels into segments
    out = []
    cur_c = labels[0]
    out.append([X[0], float(cur_c)])
    for i in range(1, n):
        if labels[i] != cur_c:
            # before switching, ensure old segment respected L_inf (safety)
            cur_c = labels[i]
            out.append([X[i], float(cur_c)])
    out.append([X[-1], float('inf')])
    return out, len(out)-1, n

def pc_center_grid_dp(pc_fx, epsilon, centers=None):
    """
    Center-Grid DP (CG-DP) for piecewise-constant approximation under L_infinity.

    Input:
      pc_fx : [[-inf, inf], [x1, y1], ..., [x_n, y_n], [x_{n+1}, inf]]
      epsilon : tolerance
      centers : optional list of candidate constants (floats).
                If None, use sorted unique Y-values (a natural, compact grid).

    Output:
      out : [[x_start1, c1], ..., [x_{K}, cK], [x_{n+1}, inf]]
      alg_pieces : K
      given_pieces : n
    """
    X, Y, n = extract_XY(pc_fx)
    if n == 0:
        return [[X[-1], float('inf')]], 0, 0

    # Candidate center grid
    if centers is None:
        centers = sorted(set(Y))  # compact, data-driven grid
    C = len(centers)

    # Precompute, for each (i, c_idx), the furthest j >= i such that all t in [i..j] satisfy |Y[t]-centers[c_idx]| <= epsilon.
    furthest = [[-1]*n for _ in range(C)]
    for ci, c in enumerate(centers):
        j = 0
        for i in range(n):
            if j < i:
                j = i
            # advance j while feasible for center c
            while j < n and abs(Y[j] - c) <= epsilon:
                j += 1
            furthest[ci][i] = j-1 if j > i else (i-1)  # j-1 is last feasible; if infeasible at i, set i-1

    # DP: dp[i] = minimal segments to cover indices [i..n-1].
    INF = 10**9
    dp = [INF]*(n+1)
    nxt = [(-1, -1)]*(n+1)  # (next_start_index, center_idx) choice
    dp[n] = 0  # base: nothing to cover

    for i in range(n-1, -1, -1):
        best_cost = INF
        best_choice = (-1, -1)
        for ci in range(C):
            j = furthest[ci][i]
            if j < i:
                continue  # center ci cannot start at i
            cost = 1 + dp[j+1]
            if cost < best_cost:
                best_cost = cost
                best_choice = (j+1, ci)  # next start is j+1
        dp[i] = best_cost
        nxt[i] = best_choice

    # Reconstruct segmentation
    out = []
    i = 0
    while i < n:
        j1, ci = nxt[i]
        if j1 == -1:
            # No feasible center at i; fall back to singleton segment at Yi
            c = Y[i]
            out.append([X[i], float(c)])
            i += 1
            continue
        c = centers[ci]
        out.append([X[i], float(c)])
        i = j1

    out.append([X[-1], float('inf')])
    return out, len(out)-1, n

def pc_naive_greedy(pc_fx, epsilon):
    segments = []
    x_start = pc_fx[1][0]
    y_val = pc_fx[1][1]

    for i in range(2, len(pc_fx) - 1):
        yi = pc_fx[i][1]
        if abs(yi - y_val) > epsilon:
            # Close previous segment
            segments.append([x_start, y_val])
            # Start new segment
            x_start = pc_fx[i][0]
            y_val = yi
        else:
            # Just average to stay inside epsilon
            y_val = (y_val + yi) / 2.0

    # Close final segment
    segments.append([x_start, y_val])
    segments.append([pc_fx[-1][0], float("inf")])

    return segments, len(segments) - 1, len(pc_fx) - 2



