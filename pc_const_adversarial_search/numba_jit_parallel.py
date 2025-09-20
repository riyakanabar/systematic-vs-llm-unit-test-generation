# test_harness_pc_const.py
import itertools
import math
import os
import sys
import numpy as np

# If your modules live one directory up:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimal_algorithms.pc_cons_apx import numba_approximate_pc_shortest_path
from numba import njit

# -----------------------
# CONFIG
# -----------------------
x_values = list(range(0, 9))             # 0..10 (11 grid points)
y_values = list(range(1, 9))              # 1..8
epsilon_values = [0.5, 0.75, 1, 2, 4, 7]
pieces_range = range(2, 7)               # number of pieces m = 2..10



# -----------------------
# HELPERS
# -----------------------

@njit
def numba_is_within_epsilon(pc_cons_fx, optimal_pc_fx, epsilon):
    """Check if the approximation is within epsilon of the original function."""
    # optimal_pc_fx_sorted = sorted(optimal_pc_fx, key=lambda x: x[0])
    xs = optimal_pc_fx[:, 0]
    ys = optimal_pc_fx[:, 1]

    n = pc_cons_fx.shape[0]

    for i in range(1, n - 1):
        x = pc_cons_fx[i, 0]
        y = pc_cons_fx[i, 1]

        # manual bisect_right
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
        if abs(y - y_opt) > epsilon + 1e-9 * abs(y_opt):  # mimic np.isclose
            return False

    return True


# def evaluate_test_case(pc_cons_fx, epsilon, algorithm):
#     """
#     Compare candidate algorithm vs OPT optimal algorithm on one test case.
#     Returns:
#       failed: bool
#       reason: "epsilon_bound" | "num_pieces" | ""
#       apx_fx
#       alg_pieces
#       optimal_pc_fx
#       optimal_num_pieces
#       given_num_pieces
#     """
#     apx_fx, alg_pieces, _ = algorithm(pc_cons_fx, epsilon)
#     optimal_pc_fx, optimal_num_pieces, given_num_pieces = approximate_pc_shortest_path(pc_cons_fx, epsilon)
#
#     # Test 1: tolerance (L_infinity) must hold
#     if not is_within_epsilon(pc_cons_fx, apx_fx, epsilon):
#         return True, "epsilon_bound", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces
#
#     # Test 2: if within tolerance, candidate must be optimal in piece count
#     if alg_pieces > optimal_num_pieces:
#         return True, "num_pieces", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces
#
#     # PASS (bug fixed: return optimal_pc_fx, not optimal_num_pieces)
#     return False, "", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces


def count_total_cases(n_x, n_y, n_eps, pieces_range):
    """
    Analytical count of all test cases (matches folded boundary approach):
      For m pieces, choose m transition indices + 1 right boundary index => comb(n_x, m+1)
      Choose y-values for each of the m pieces => (n_y ** m)
      Multiply by number of epsilons.
    """
    total = 0
    for m in pieces_range:
        total += math.comb(n_x, m + 1) * (n_y ** m) * n_eps
    return total


def x_combos(m):
    """
    Stream all strictly increasing (m+1)-tuples of indices from [0, n-1].
    Tuple = (i1, i2, ..., im, b) where the last index is the right boundary.
    """
    return itertools.combinations(range(len(x_values)), m)


# -----------------------
# MAIN TEST DRIVER
# -----------------------
def test_algorithm(algorithm):
    """
    Enumerate piecewise-constant test cases over bounded grids, evaluate candidate vs OPT,
    and print failure stats.

    Parameters
    ----------
    algorithm : callable
        Your candidate algorithm with signature:
            (pc_cons_fx, epsilon) -> (apx_fx, alg_pieces, <ignored>)

    Prints
    ------
      - % epsilon failures
      - % optimality failures
      - total failure rate (% that failed epsilon OR optimality)

    Returns
    -------
    dict with counts and percentages.
    """
    # Try optional progress bar
    try:
        from tqdm import tqdm
        pbar = tqdm(desc="Testing", unit="case")
        use_pbar = True
    except ImportError:
        pbar = None
        use_pbar = False

    # Heads-up: theoretical total can be astronomically large
    total_theoretical = count_total_cases(len(x_values), len(y_values), len(epsilon_values), pieces_range)
    print(f"Theoretical total test cases (full grid): {total_theoretical:,}")

    # Preconvert to floats once (avoid float() in inner loop)
    x_as_float = [float(v) for v in x_values]
    y_as_float = [float(v) for v in y_values]

    # Stats
    tested = 0
    epsilon_fail = 0
    optimality_fail = 0
    total_fail = 0

    n = len(x_values)

    for m in pieces_range:
        for eps in epsilon_values:
            # Each indices tuple includes the boundary as the last element
            for indices in x_combos(m+1):
                trans_indices = indices[:-1]
                boundary_idx = indices[-1]

                # Build transition x’s and boundary x once
                trans_xs = [x_as_float[i] for i in trans_indices]
                right_boundary_x = x_as_float[boundary_idx]


                y_combo = itertools.product(y_as_float, repeat=m)

                for y_tuple in y_combo:
                    # Assemble testcase in required format:
                    # [(-inf, inf), (x1,y1), ..., (xm, ym), (x_{m+1}, inf)]
                    points = [[-float('inf'), float('inf')]]
                    for xx, yy in zip(trans_xs, y_tuple):
                        points.append([xx, yy])
                    points.append([right_boundary_x, float('inf')])

                    points = np.array(points)
                    apx_fx, alg_pieces, _ = algorithm(points, eps)
                    optimal_pc_fx, optimal_num_pieces, given_num_pieces = numba_approximate_pc_shortest_path(points,eps)
                    # apx_fx = np.array(apx_fx) algorithm already returns np.array
                    test1 = not numba_is_within_epsilon(points, apx_fx, eps)
                    test2 = alg_pieces > optimal_num_pieces

                    if test1 :
                        epsilon_fail += 1

                    # Test 2: if within tolerance, candidate must be optimal in piece count
                    if test2:
                        optimality_fail += 1
                    if test1 or test2:
                        total_fail += 1
                    tested += 1

                    if use_pbar:
                        pbar.update(1)

    if use_pbar:
        pbar.close()

    # Reporting
    if tested == 0:
        print("No testcases were generated (check your grids or caps).")
        return {
            "tested": 0,
            "epsilon_fail": 0,
            "optimality_fail": 0,
            "epsilon_fail_pct": 0.0,
            "optimality_fail_pct": 0.0,
            "total_fail_pct": 0.0,
        }

    epsilon_fail_pct = 100.0 * epsilon_fail / tested
    optimality_fail_pct = 100.0 * optimality_fail / tested
    total_fail_pct = 100.0 * total_fail / tested

    print("\n=== RESULTS ===")
    print(f"Tested cases:       {tested:,}")
    print(f"Epsilon failures:   {epsilon_fail}  ({epsilon_fail_pct:.3f}%)")
    print(f"Optimality failures:{optimality_fail}  ({optimality_fail_pct:.3f}%)")
    print(f"Total failure rate: {total_fail}  ({total_fail_pct:.3f}%)")

    return {
        "tested": tested,
        "epsilon_fail": epsilon_fail,
        "optimality_fail": optimality_fail,
        "epsilon_fail_pct": epsilon_fail_pct,
        "optimality_fail_pct": optimality_fail_pct,
        "total_fail_pct": total_fail_pct,
    }

import os
import math
import itertools
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

# ---- You should already have these fast/JITed: ----
# from yourmodule import approximate_pc_shortest_path
# from yourmodule import numba_is_within_epsilon
# from yourmodule import x_values, y_values, epsilon_values, pieces_range, x_combos

# ------------- Worker -----------------
def _worker_batch(args):
    """
    Processes a batch of y-tuples for one (m, eps, indices) combo.
    Returns partial counts: (tested, eps_fail, opt_fail, total_fail)
    """
    (m, eps, trans_indices, boundary_idx, y_batch, x_as_float, algorithm) = args

    tested = 0
    epsilon_fail = 0
    optimality_fail = 0
    total_fail = 0

    trans_xs = [x_as_float[i] for i in trans_indices]
    right_boundary_x = x_as_float[boundary_idx]

    for y_tuple in y_batch:
        # Assemble testcase
        points = [[-float('inf'), float('inf')]]
        for xx, yy in zip(trans_xs, y_tuple):
            points.append([xx, yy])
        points.append([right_boundary_x, float('inf')])

        points = np.array(points, dtype=np.float64)

        # Candidate algo
        apx_fx, alg_pieces, _ = algorithm(points, eps)

        # Oracle optimal (piece count) for comparison
        optimal_pc_fx, optimal_num_pieces, given_num_pieces = numba_approximate_pc_shortest_path(points, eps)

        # Tests
        test1 = not numba_is_within_epsilon(points, apx_fx, eps)         # ε-feasibility
        test2 = (alg_pieces > optimal_num_pieces)                        # optimality

        if test1:
            epsilon_fail += 1
        if test2:
            optimality_fail += 1
        if test1 or test2:
            total_fail += 1
        tested += 1

    return tested, epsilon_fail, optimality_fail, total_fail

# ------------- Batching helper -----------------
def _batched(iterable, batch_size):
    """Yield lists of length up to batch_size from iterable."""
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, batch_size))
        if not batch:
            break
        yield batch

# ------------- Parallel driver -----------------
def test_algorithm_parallel(algorithm,
                            max_workers=None,
                            batch_size=2000,
                            show_progress=True):
    """
    Parallel version of test_algorithm using ProcessPoolExecutor with batching.

    max_workers: int|None  -> defaults to os.cpu_count()
    batch_size:  size of each y-product batch turned into one task
    """

    # Optional progress bar
    try:
        from tqdm import tqdm
        pbar = tqdm(desc="Testing", unit="case") if show_progress else None
    except ImportError:
        pbar = None

    # Preconvert to floats once
    x_as_float = [float(v) for v in x_values]
    y_as_float = [float(v) for v in y_values]

    # Stats
    tested = 0
    epsilon_fail = 0
    optimality_fail = 0
    total_fail = 0

    total_theoretical = count_total_cases(len(x_values), len(y_values), len(epsilon_values), pieces_range)
    print(f"Theoretical total test cases (full grid): {total_theoretical:,}")

    # Tip: avoid thread oversubscription if your JIT code also uses threads
    # os.environ.setdefault("NUMBA_NUM_THREADS", "1")
    # os.environ.setdefault("OMP_NUM_THREADS", "1")

    futures = []
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        for m in pieces_range:
            for eps in epsilon_values:
                for indices in x_combos(m + 1):
                    trans_indices = indices[:-1]
                    boundary_idx = indices[-1]

                    # Huge cartesian product -> chunk it
                    y_iter = itertools.product(y_as_float, repeat=m)

                    for y_batch in _batched(y_iter, batch_size):
                        args = (m, eps, trans_indices, boundary_idx, y_batch, x_as_float,algorithm)
                        futures.append(ex.submit(_worker_batch, args))

        # Collect results
        if pbar is None:
            for fut in as_completed(futures):
                t, e1, e2, tf = fut.result()
                tested += t
                epsilon_fail += e1
                optimality_fail += e2
                total_fail += tf
        else:
            for fut in as_completed(futures):
                t, e1, e2, tf = fut.result()
                tested += t
                epsilon_fail += e1
                optimality_fail += e2
                total_fail += tf
                pbar.update(t)

    if pbar is not None:
        pbar.close()

    if tested == 0:
        print("No testcases were generated.")
        return {
            "tested": 0,
            "epsilon_fail": 0,
            "optimality_fail": 0,
            "epsilon_fail_pct": 0.0,
            "optimality_fail_pct": 0.0,
            "total_fail_pct": 0.0,
        }

    epsilon_fail_pct = 100.0 * epsilon_fail / tested
    optimality_fail_pct = 100.0 * optimality_fail / tested
    total_fail_pct = 100.0 * total_fail / tested

    print("\n=== RESULTS (parallel) ===")
    print(f"Tested cases:        {tested:,}")
    print(f"Epsilon failures:    {epsilon_fail}  ({epsilon_fail_pct:.3f}%)")
    print(f"Optimality failures: {optimality_fail}  ({optimality_fail_pct:.3f}%)")
    print(f"Total failure rate:  {total_fail}  ({total_fail_pct:.3f}%)")

    return {
        "tested": tested,
        "epsilon_fail": epsilon_fail,
        "optimality_fail": optimality_fail,
        "epsilon_fail_pct": epsilon_fail_pct,
        "optimality_fail_pct": optimality_fail_pct,
        "total_fail_pct": total_fail_pct,
    }
