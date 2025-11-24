import numpy as np
from math import inf
from typing import List, Tuple
import heapq

#standard optimal algorithm - not a variant
# variant0 = functools.partial(
#         variant_function,
#         loop_behavior=loop_variations[0],
#         params_min=[1,1,1,1,-1],
#         params_max=[1,1,1,1,1],
#         condition_params=[operator.ge, operator.ge, operator.le]
#     )
#
# variant1 = functools.partial(
#         variant_function,
#         loop_behavior=loop_variations[1],
#         params_min=[1,2,1,2,-1],
#         params_max=[1,1,1,1,1], #standard
#         condition_params=[operator.ge, operator.ge, operator.le] #standard
#     )
# variant2 = functools.partial(
#         variant_function,
#         loop_behavior=loop_variations[1],
#         params_min=[1,1,1,1,-1], #standard
#         params_max=[1,1,1,1,1], #standard
#         condition_params=[operator.ge, operator.ge, operator.le] #standard
#     )
# variant3 = functools.partial(
#         variant_function,
#         loop_behavior=loop_variations[2],
#         params_min=[1,1,1,1,-1], #standard
#         params_max=[1,1,1,1,1], #standard
#         condition_params=[operator.ge, operator.ge, operator.le] #standard
#     )

def recursive_split1(pc_fx, epsilon):
        """
        Non-optimal greedy algorithm for approximating a piecewise constant function
        using a top-down ε-satisfying split.
        """

        def rec(start_idx, end_idx):
                segment = pc_fx[start_idx:end_idx + 1]
                ys = np.array([y for _, y in segment])
                max_y = np.max(ys)
                min_y = np.min(ys)
                #if abs(max_y - min_y) <= 2*epsilon + 1e-9 * abs(min_y):  # mimic np.isclose
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

                left = rec(start_idx, mid_idx)
                right = rec(mid_idx, end_idx)
                return left + right

        # Call recursive splitting on points between -inf and +inf
        segments = rec(1, len(pc_fx) - 2)
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

def lookahead_split(pc_fx, epsilon):
    X, Y, n = extract_XY(pc_fx)
    out = []
    i = 0
    while i < n:
        vmin = vmax = Y[i]
        j = i + 1
        while j < n:
            vmin2 = min(vmin, Y[j]); vmax2 = max(vmax, Y[j])
            #if vmax2 - vmin2 <= 2 * epsilon:
            if np.isclose(vmax2, vmin2, atol=2*epsilon, rtol=1e-9):
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

def binary_split(pc_fx, epsilon):
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
        if np.isclose(vmax, vmin, atol=2 * epsilon, rtol=1e-9):
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

def beam_search(pc_fx, epsilon, beam_size=8):
    X, Y, n = extract_XY(pc_fx)

    # precompute feasibility: furthest j you can reach from i
    furthest = [0]*n
    for i in range(n):
        vmin = vmax = Y[i]
        j = i
        while j < n:
            vmin = min(vmin, Y[j]); vmax = max(vmax, Y[j])
            #if (vmax - vmin) <= (2 * epsilon + TOL * max(1.0, abs(vmax), abs(vmin))):
            if np.isclose(vmax, vmin, atol=2*epsilon, rtol=1e-9):
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

def recursive_split2(pc_fx, epsilon):
    # Extract interior grid
    X = [pc_fx[i][0] for i in range(1, len(pc_fx))]          # includes last boundary at the end
    Y = [pc_fx[i][1] for i in range(1, len(pc_fx)-1)]        # interior values only
    n = len(Y)

    def rec(i, j):
        # interval indices are inclusive
        if i == j:
            return [[X[i], float(Y[i])]]

        seg = Y[i:j+1]
        mn, mx = float(np.min(seg)), float(np.max(seg))

        # Base case: ε-feasible -> emit midpoint, guaranteed max error ≤ ε
        if np.isclose(mx, mn, atol=2 * epsilon, rtol=1e-9):
        #if mx - mn <= 2.0 * epsilon:
            return [[X[i], 0.5 * (mn + mx)]]

        # Choose a split index s in (i..j) (prefer point of largest deviation from current midpoint)
        mid = 0.5 * (mn + mx)
        candidates = range(i+1, j+1)           # ensure both sides non-empty
        s = max(candidates, key=lambda t: abs(Y[t] - mid), default=None)
        if s is None or s <= i or s > j:
            s = (i + j + 1) // 2               # safe fallback split

        left  = rec(i, s-1)
        right = rec(s, j)
        return left + right

    if n == 0:
        return [[X[-1], float('inf')]], 0, 0

    segs = rec(0, n-1)
    segs.append([X[-1], float('inf')])
    return segs, len(segs) - 1, n



Piece = Tuple[float, float]  # (x_i, y_i) for the i-th true piece (left endpoint, value)

def extract_pieces(pc_fx: List[Tuple[float, float]]) -> List[Piece]:
    """Remove boundary sentinels and return [(x1,y1),...,(xn,yn)]."""
    assert len(pc_fx) >= 3, "pc_fx must have at least (-inf,inf), one piece, and (x_{n+1}, inf)"
    return pc_fx[1:-1]

def to_output(pieces: List[Piece], x_right: float) -> List[Tuple[float, float]]:
    """Convert back to sentinel format [(-inf,inf), (x1,y1),...,(xm,ym), (x_{m+1}, inf)]."""
    if not pieces:
        # Degenerate case: no pieces -> return a single dummy piece at -inf (rare in practice)
        return [(-inf, inf), (x_right, 0.0)]
    out = [(-inf, inf)]
    out.extend(pieces)
    out.append((x_right, inf))
    return out


def count_original_pieces(pc_fx: List[Tuple[float, float]]) -> int:
    return max(0, len(pc_fx) - 2)

# ========== 6) Bottom-Up Agglomerative by Smallest Y-Spread ==========
# Strategy: repeatedly merge the adjacent pair whose combined y-range (max-min) is the smallest
#           subject to (max-min) ≤ 2ε (feasible). Stops when no pair can be merged.
# Complexity: O(n log n) using a heap; updates only near merges.
def agglomerative_yspread(pc_fx: List[Tuple[float, float]], eps: float):
    pieces = extract_pieces(pc_fx)
    n = len(pieces)
    ys = [y for _, y in pieces]
    alive = [True]*n

    # Store (spread, i) for adjacent (i,i+1)
    def spread(i):
        if i < 0 or i >= n-1 or not alive[i] or not alive[i+1]:
            return None
        lo = min(ys[i], ys[i+1])
        hi = max(ys[i], ys[i+1])
        w = hi - lo
        return w if np.isclose(hi, lo, atol=2*eps, rtol=1e-9) else None

    heap = []
    for i in range(n-1):
        s = spread(i)
        if s is not None:
            heapq.heappush(heap, (s, i))

    # We’ll just mark j dead and keep y[i] as the merged representative, but clamp it later.
    while heap:
        s, i = heapq.heappop(heap)
        if s is None or not alive[i]:
            continue
        j = i+1
        while j < n and not alive[j]:
            j += 1
        if j >= n or not alive[j]:
            continue
        # Verify current spread is still feasible
        lo = min(ys[i], ys[j])
        hi = max(ys[i], ys[j])
        if np.isclose(hi, lo, atol=2*eps, rtol=1e-9):
            # merge j into i, keep ys[i] as representative (final value will be clamped)
            alive[j] = False
            # try to merge (i-1,i) and (i,i+1) next
            for k in (i-1, i):
                if 0 <= k < n-1:
                    s2 = spread(k)
                    if s2 is not None:
                        heapq.heappush(heap, (s2, k))

    # Build bands per live block by scanning and intersecting
    out = []
    i = 0
    while i < n:
        if not alive[i]:
            i += 1
            continue
        # start block
        lo, hi = ys[i] - eps, ys[i] + eps
        x_left = pieces[i][0]
        j = i + 1
        while j < n and not alive[j]:
            # merged into i; update band with their eps bands to remain valid
            yj = ys[j]
            lo = max(lo, yj - eps)
            hi = min(hi, yj + eps)
            j += 1
        val = (lo + hi) / 2.0
        out.append((x_left, val))
        i = j
    return to_output(out, pc_fx[-1][0]), len(out), count_original_pieces(pc_fx)


# ========== 8) Pruned Dynamic Programming (Feasible-Window) ==========
# Strategy: DP[i] = min pieces to cover first i segments.
#           Transition: choose j<i such that the block [j..i-1] is feasible (band intersection non-empty).
#           We prune by stopping leftward expansion once y-range exceeds 2ε (common early-stop).
# Complexity: O(n^2) worst case, typically much less with pruning.
def pruned_dp(pc_fx: List[Tuple[float, float]], eps: float):
    pieces = extract_pieces(pc_fx)
    n = len(pieces)
    INF = 10**9
    dp = [INF]*(n+1)
    prev = [-1]*(n+1)
    dp[0] = 0
    for i in range(1, n+1):
        lo, hi = pieces[i-1][1] - eps, pieces[i-1][1] + eps
        j = i-1
        while j >= 0:
            # block [j..i-1]
            if j < i-1:
                y = pieces[j][1]
                lo, hi = max(lo, y - eps), min(hi, y + eps)
            if lo > hi:
                break  # further left will only widen the y-span; safe prune
            if dp[j] + 1 < dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
            j -= 1
    # Reconstruct
    out = []
    i = n
    while i > 0:
        j = prev[i]
        # compute final band for [j..i-1]
        lo, hi = -inf, inf
        for k in range(j, i):
            y = pieces[k][1]
            lo = max(lo, y - eps)
            hi = min(hi, y + eps)
        val = (lo + hi) / 2.0
        out.append((pieces[j][0], val))
        i = j
    out.reverse()
    return to_output(out, pc_fx[-1][0]), len(out), count_original_pieces(pc_fx)

candidate_algorithms = [recursive_split1, recursive_split2, lookahead_split,
                        agglomerative_yspread, binary_split, beam_search, pruned_dp]
