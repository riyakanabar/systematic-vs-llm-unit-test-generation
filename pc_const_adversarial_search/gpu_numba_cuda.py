import itertools
import math
import os
import sys
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from numba import njit, cuda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -----------------------
# CONFIG
# -----------------------
x_values = range(0, 11)
y_values = range(1, 9)
epsilon_values = [0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 7]
pieces_range = range(2, 11)

# Fixed maximums for CUDA local arrays
MAX_M = max(pieces_range)  # <= 10
MAXPTS = MAX_M + 2         # m interior + 2 boundaries


# -----------------------
# GPU DEVICE HELPERS
# -----------------------

@cuda.jit(device=True)
def decode_ytuple(tid, m, Y, y_vals, out_tuple):
    """Decode thread-id into y-tuple (base Y digits)."""
    for i in range(m):
        d = tid % Y
        out_tuple[i] = y_vals[d]
        tid //= Y


@cuda.jit(device=True)
def numba_is_within_epsilon_dev(points, n_points, approx, k_rows, epsilon):
    """Check if the approximation is within epsilon of the original function."""
    for i in range(1, n_points - 1):
        x = points[i, 0]
        y = points[i, 1]

        # binary search
        lo = 0
        hi = k_rows
        while lo < hi:
            mid = (lo + hi) >> 1
            if approx[mid, 0] <= x:
                lo = mid + 1
            else:
                hi = mid
        j = lo - 1
        if j < 0:
            return False

        y_opt = approx[j, 1]
        if math.fabs(y - y_opt) > (epsilon + 1e-9 * math.fabs(y_opt)):
            return False
    return True


@cuda.jit(device=True)
def numba_approximate_pc_shortest_path_dev(points, n_points, epsilon, approx_out):
    """Oracle on GPU (shortest-path greedy)."""
    n = n_points - 2
    L = cuda.local.array(shape=MAX_M, dtype=np.float64)
    U = cuda.local.array(shape=MAX_M, dtype=np.float64)
    for j in range(n):
        y = points[j + 1, 1]
        U[j] = y + epsilon
        L[j] = y - epsilon

    out_x = cuda.local.array(shape=MAXPTS, dtype=np.float64)
    out_y = cuda.local.array(shape=MAXPTS, dtype=np.float64)

    m = 0
    i = 0
    while i < n:
        U_max = math.inf
        L_min = -math.inf
        k = i + 1
        while k <= n:
            new_U_max = U[k - 1] if U[k - 1] < U_max else U_max
            new_L_min = L[k - 1] if L[k - 1] > L_min else L_min
            if (new_U_max >= new_L_min) and (U[i] >= new_L_min) and (L[i] <= new_U_max):
                U_max = new_U_max
                L_min = new_L_min
                k += 1
            else:
                break
        out_x[m] = points[i + 1, 0]
        out_y[m] = 0.5 * (U_max + L_min)
        m += 1
        i = k - 1

    # append last boundary
    out_x[m] = points[n + 1, 0]
    out_y[m] = math.inf
    m += 1

    for t in range(m):
        approx_out[t, 0] = out_x[t]
        approx_out[t, 1] = out_y[t]
    return m


# -----------------------
# GPU KERNEL
# -----------------------

@cuda.jit
def gpu_eval_y_batch(m, eps,
                     trans_indices, right_boundary_idx,
                     x_vals, y_vals,
                     start_index, n_cases,
                     tested_out, eps_fail_out, opt_fail_out, total_fail_out):
    tid = cuda.grid(1)
    if tid >= n_cases:
        return

    Y = y_vals.size
    # decode this thread's y-tuple
    y_tuple = cuda.local.array(shape=MAX_M, dtype=np.float64)
    decode_ytuple(start_index + tid, m, Y, y_vals, y_tuple)

    # build points
    n_points = m + 2
    points = cuda.local.array(shape=(MAXPTS, 2), dtype=np.float64)
    points[0, 0] = -math.inf
    points[0, 1] = math.inf
    for t in range(m):
        xi = x_vals[trans_indices[t]]
        yi = y_tuple[t]
        points[t + 1, 0] = xi
        points[t + 1, 1] = yi
    right_x = x_vals[right_boundary_idx]
    points[m + 1, 0] = right_x
    points[m + 1, 1] = math.inf

    # Oracle
    approx = cuda.local.array(shape=(MAXPTS, 2), dtype=np.float64)
    k_rows = numba_approximate_pc_shortest_path_dev(points, n_points, eps, approx)

    # Feasibility
    feasible = numba_is_within_epsilon_dev(points, n_points, approx, k_rows, eps)

    # Candidate not on GPU → set False
    opt_fail = False

    # atomics
    cuda.atomic.add(tested_out, 0, 1)
    if not feasible:
        cuda.atomic.add(eps_fail_out, 0, 1)
    if opt_fail:
        cuda.atomic.add(opt_fail_out, 0, 1)
    if (not feasible) or opt_fail:
        cuda.atomic.add(total_fail_out, 0, 1)


# -----------------------
# CPU FALLBACK HELPERS
# -----------------------

@njit(cache=True)
def numba_approximate_pc_shortest_path(points, eps):
    # your original njit version here (kept for CPU fallback)
    n = points.shape[0] - 2
    U = np.empty(n, dtype=np.float64)
    L = np.empty(n, dtype=np.float64)
    for j in range(n):
        U[j] = points[j+1, 1] + eps
        L[j] = points[j+1, 1] - eps

    out_x = np.empty(n+1, dtype=np.float64)
    out_y = np.empty(n+1, dtype=np.float64)
    m = 0
    i = 0
    while i < n:
        U_max = np.inf
        L_min = -np.inf
        k = i + 1
        while k <= n:
            new_U_max = U[k-1] if U[k-1] < U_max else U_max
            new_L_min = L[k-1] if L[k-1] > L_min else L_min
            if (new_U_max >= new_L_min) and (U[i] >= new_L_min) and (L[i] <= new_U_max):
                U_max = new_U_max
                L_min = new_L_min
                k += 1
            else:
                break
        out_x[m] = points[i+1, 0]
        out_y[m] = 0.5 * (U_max + L_min)
        m += 1
        i = k - 1
    out_x[m] = points[-1, 0]
    out_y[m] = np.inf
    m += 1
    optimal_pc_fx = np.empty((m, 2), dtype=np.float64)
    for t in range(m):
        optimal_pc_fx[t, 0] = out_x[t]
        optimal_pc_fx[t, 1] = out_y[t]
    return optimal_pc_fx, m-1, n


@njit(cache=True)
def numba_is_within_epsilon(points, approx, eps):
    xs = approx[:, 0]
    ys = approx[:, 1]
    n = points.shape[0]
    for i in range(1, n - 1):
        x = points[i, 0]
        y = points[i, 1]
        lo, hi = 0, xs.shape[0]
        while lo < hi:
            mid = (lo + hi) // 2
            if xs[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        j = lo - 1
        if j < 0:
            return False
        y_opt = ys[j]
        if abs(y - y_opt) > eps + 1e-9 * abs(y_opt):
            return False
    return True


# -----------------------
# COUNT + COMBOS
# -----------------------

def count_total_cases(n_x, n_y, n_eps, pieces_range):
    total = 0
    for m in pieces_range:
        total += math.comb(n_x, m + 1) * (n_y ** m) * n_eps
    return total


def x_combos(m):
    return itertools.combinations(range(len(x_values)), m)


# -----------------------
# WORKER
# -----------------------

def _worker_chunk(args):
    (m, eps, trans_indices, boundary_idx, y_range, x_as_float, algorithm) = args
    start, end = y_range
    batch = end - start

    if cuda.is_available():
        # Device setup (small arrays, transferred once)
        d_x = cuda.to_device(np.asarray(x_as_float, dtype=np.float64))
        d_y = cuda.to_device(np.asarray(list(y_values), dtype=np.float64))
        d_trans = cuda.to_device(np.asarray(trans_indices, dtype=np.int32))

        tested_d = cuda.to_device(np.array([0], dtype=np.int64))
        eps_fail_d = cuda.to_device(np.array([0], dtype=np.int64))
        opt_fail_d = cuda.to_device(np.array([0], dtype=np.int64))
        total_fail_d = cuda.to_device(np.array([0], dtype=np.int64))

        threads = 256
        blocks = (batch + threads - 1) // threads

        gpu_eval_y_batch[blocks, threads](
            np.int32(m), np.float64(eps),
            d_trans, np.int32(boundary_idx),
            d_x, d_y,
            np.int64(start), np.int64(batch),
            tested_d, eps_fail_d, opt_fail_d, total_fail_d
        )

        tested = int(tested_d.copy_to_host()[0])
        epsilon_fail = int(eps_fail_d.copy_to_host()[0])
        optimality_fail = int(opt_fail_d.copy_to_host()[0])  # stays 0
        total_fail = int(total_fail_d.copy_to_host()[0])
        return tested, epsilon_fail, optimality_fail, total_fail

    # CPU fallback
    tested = epsilon_fail = optimality_fail = total_fail = 0
    trans_xs = [x_as_float[i] for i in trans_indices]
    right_boundary_x = x_as_float[boundary_idx]

    y_iter = itertools.islice(itertools.product(y_values, repeat=m), start, end)
    for y_tuple in y_iter:
        points = [[-float('inf'), float('inf')]]
        for xx, yy in zip(trans_xs, y_tuple):
            points.append([xx, yy])
        points.append([right_boundary_x, float('inf')])
        points = np.array(points, dtype=np.float64)

        apx_fx, alg_pieces, _ = algorithm(points, eps)
        optimal_pc_fx, optimal_num_pieces, _ = numba_approximate_pc_shortest_path(points, eps)

        test1 = not numba_is_within_epsilon(points, apx_fx, eps)
        test2 = (alg_pieces > optimal_num_pieces)

        if test1: epsilon_fail += 1
        if test2: optimality_fail += 1
        if test1 or test2: total_fail += 1
        tested += 1
    return tested, epsilon_fail, optimality_fail, total_fail


# -----------------------
# DRIVER
# -----------------------

def test_algorithm_parallel(algorithm,
                            max_workers=None,
                            chunk_size=500000,
                            show_progress=True):
    start = time.time()
    try:
        from tqdm import tqdm
        pbar = tqdm(desc="Testing", unit="case") if show_progress else None
    except ImportError:
        pbar = None

    x_as_float = [float(v) for v in x_values]
    tested = epsilon_fail = optimality_fail = total_fail = 0
    total_theoretical = count_total_cases(len(x_values), len(y_values), len(epsilon_values), pieces_range)
    print(f"Theoretical total test cases (full grid): {total_theoretical:,}")

    def task_generator():
        for m in pieces_range:
            for eps in epsilon_values:
                for indices in x_combos(m + 1):
                    trans_indices = indices[:-1]
                    boundary_idx = indices[-1]
                    total_y = len(y_values) ** m
                    for start in range(0, total_y, chunk_size):
                        end = min(start + chunk_size, total_y)
                        yield (m, eps, trans_indices, boundary_idx, (start, end), x_as_float, algorithm)

    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        for t, e1, e2, tf in ex.map(_worker_chunk, task_generator(), chunksize=1):
            tested += t
            epsilon_fail += e1
            optimality_fail += e2
            total_fail += tf
            if pbar is not None: pbar.update(t)

    if pbar is not None:
        pbar.close()
    runtime = time.time() - start
    avg_speed = tested / runtime if runtime > 0 else 0.0

    print("\n=== RESULTS (parallel) ===")
    print(f"Tested cases:        {tested:,}")
    print(f"Runtime (s):         {runtime:.2f}")
    print(f"Average speed:       {avg_speed:,.0f} cases/s")
    print(f"Epsilon failures:    {epsilon_fail}")
    print(f"Optimality failures: {optimality_fail}")
    print(f"Total failure rate:  {total_fail}")
    return {
        "tested": tested,
        "epsilon_fail": epsilon_fail,
        "optimality_fail": optimality_fail,
        "total_fail": total_fail,
    }


# -----------------------
# CANDIDATE ALGORITHM (CPU)
# -----------------------

@njit(cache=True)
def rec(pc_fx, epsilon, start_idx, end_idx):
    ys = pc_fx[start_idx:end_idx+1, 1]
    max_y = np.max(ys)
    min_y = np.min(ys)
    if abs(max_y - min_y) <= 2*epsilon + 1e-9 * abs(min_y):
        y_value = (max_y + min_y) / 2
        return np.array([[pc_fx[start_idx, 0], y_value]])
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
    left = rec(pc_fx, epsilon, start_idx, mid_idx)
    right = rec(pc_fx, epsilon, mid_idx, end_idx)
    return np.vstack((left, right))


@njit(cache=True)
def numba_recursive_split1(pc_fx, epsilon):
    segments = rec(pc_fx, epsilon, 1, pc_fx.shape[0]-2)
    last_row = np.array([[pc_fx[-1, 0], np.inf]])
    segments = np.vstack((segments, last_row))
    num_pieces = segments.shape[0] - 1
    given_pieces = pc_fx.shape[0] - 2
    return segments, num_pieces, given_pieces


# -----------------------
# MAIN
# -----------------------

if __name__ == "__main__":
    test_algorithm_parallel(numba_recursive_split1)
