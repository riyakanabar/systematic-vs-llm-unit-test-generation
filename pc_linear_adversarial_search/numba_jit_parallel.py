import itertools
import math
import os
import sys
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from numba import njit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimal_algorithms.numba_pc_linear_apx import numba_approximate_pc_linear_fx
from cpu_parallel import x_values, y_values, epsilon_values, pieces_range, count_total_cases
from numba import njit

# -----------------------
# HELPERS
# -----------------------


@njit(fastmath=True)
def round2(x):
    """Manual rounding to 2 decimals (JIT-safe)."""
    if x >= 0:
        return np.floor(x * 1e2 + 0.5) / 1e2
    else:
        return np.ceil(x * 1e2 - 0.5) / 1e2


@njit(fastmath=True, cache=True)
def numba_is_within_epsilon(original_fx, approximation, epsilon):
    """
    Check if the approximation is within epsilon of the original function.
    Numba version: same logic, faster execution.
    """
    n_orig = len(original_fx)
    n_appr = len(approximation)

    for oi in range(n_orig):
        x = original_fx[oi, 0]
        orig_y = original_fx[oi, 1]
        approx_y = np.nan
        # rounded_approx_y = np.nan

        # Find segment containing x
        for i in range(n_appr - 1):
            x1 = approximation[i, 0]
            y1 = approximation[i, 1]
            x2 = approximation[i + 1, 0]
            y2 = approximation[i + 1, 1]
            if x1 <= x <= x2:
                dx = x2 - x1
                if abs(dx) < 1e-12:
                    slope = 0.0
                else:
                    slope = (y2 - y1) / dx
                intercept = y1 - slope * x1
                approx_y = slope * x + intercept
                # rounded_approx_y = round2(approx_y)
                break

        # Handle x outside range
        if np.isnan(approx_y) and n_appr > 0:
            approx_y = approximation[-1, 1]
            # rounded_approx_y = round2(approx_y)

        # Check closeness
        if abs(orig_y - approx_y) > epsilon + 1e-9 * abs(orig_y):
            # Return False with empty string because numba can’t return formatted text
            return False, 0.0  # placeholder second value

    return True, 0.0  # placeholder

def x_combos(m):
    """
    Stream all strictly increasing (m+1)-tuples of indices from [0, n-1].
    Tuple = (i1, i2, ..., im, b) where the last index is the right boundary.
    """
    return itertools.combinations(range(len(x_values)), m)

# ---------------- Worker ----------------
_worker_warmed_up = False
def _worker_chunk(args):
    """
    Process a chunk of y-tuples for one (m, eps, indices) config.
    Only stores the slice (start, end) not the full y_batch.
    """
    global _worker_warmed_up
    (m, eps, trans_indices, y_range, x_as_float, algorithm) = args
    start, end = y_range

    # ---------------- Warm-up ----------------
    if not _worker_warmed_up:
        dummy_points = np.array([[0.0, 2.0], [1.0, 3.0], [2.0, 1.0]], dtype=np.float64)
        dummy_apx = np.array([[0.0, 2.0], [2.0, 1.0]], dtype=np.float64)
        _ = numba_is_within_epsilon(dummy_points, dummy_points, 0.1)
        _ = numba_approximate_pc_linear_fx(dummy_points, 0.1)
        _worker_warmed_up = True
    # ------------------------------------------

    tested = epsilon_fail = optimality_fail = total_fail = 0
    trans_xs = np.array([x_as_float[i] for i in trans_indices], dtype=np.float64)

    # regenerate product lazily
    y_iter = itertools.islice(itertools.product(y_values, repeat=m+1), start, end)
    for y_tuple in y_iter:
        points = np.array([(float(x), float(y)) for x, y in zip(trans_xs, y_tuple)], dtype=np.float64)

        # Candidate algo
        apx_fx, alg_pieces, _ = algorithm(points, eps)
        apx_fx = np.array(apx_fx, dtype=np.float64)
        # Oracle
        optimal_pc_fx, optimal_num_pieces, given_num_pieces = numba_approximate_pc_linear_fx(points, eps)

        test1 = not numba_is_within_epsilon(points, apx_fx, eps)
        test2 = (alg_pieces > optimal_num_pieces)

        if test1: epsilon_fail += 1
        if test2: optimality_fail += 1
        if test1 or test2: total_fail += 1
        tested += 1

    return tested, epsilon_fail, optimality_fail, total_fail

# ---------------- Parallel driver ----------------
def numba_test_algorithm_parallel(algorithm,
                            max_workers=None,
                            chunk_size=500000,
                            show_progress=True):
    """
    Parallel version of test_algorithm using ProcessPoolExecutor with streaming.
    Does not store all configs or batches.
    """
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
                    trans_indices = indices
                    total_y = len(y_values) ** (m+1)
                    for start in range(0, total_y, chunk_size):
                        end = min(start + chunk_size, total_y)
                        yield (m, eps, trans_indices,(start, end), x_as_float, algorithm)

    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        for t, e1, e2, tf in ex.map(_worker_chunk, task_generator(), chunksize=1):
            tested += t
            epsilon_fail += e1
            optimality_fail += e2
            total_fail += tf
            if pbar is not None: pbar.update(t)

    if pbar is not None: pbar.close()
    end = time.time()
    runtime = end - start
    avg_speed = tested / runtime if runtime > 0 else 0.0

    epsilon_fail_pct = 100.0 * epsilon_fail / tested if tested else 0.0
    optimality_fail_pct = 100.0 * optimality_fail / tested if tested else 0.0
    total_fail_pct = 100.0 * total_fail / tested if tested else 0.0

    print("\n=== RESULTS (parallel) ===")
    print(f"Tested cases:        {tested:,}")
    print(f"Runtime (s):         {runtime:.2f}")
    print(f"Average speed:       {avg_speed:,.0f} cases/s")
    print(f"Epsilon failures:    {epsilon_fail}  ({epsilon_fail_pct:.1f}%)")
    print(f"Optimality failures: {optimality_fail}  ({optimality_fail_pct:.1f}%)")
    print(f"Total failure rate:  {total_fail}  ({total_fail_pct:.1f}%)")

    return {
        "tested": tested,
        "epsilon_fail": epsilon_fail,
        "optimality_fail": optimality_fail,
        "epsilon_fail_pct": epsilon_fail_pct,
        "optimality_fail_pct": optimality_fail_pct,
        "total_fail_pct": total_fail_pct,
    }
