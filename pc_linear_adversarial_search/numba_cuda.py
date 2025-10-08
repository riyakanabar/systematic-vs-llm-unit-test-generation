import itertools
import math
import os
import sys
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from numba import njit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimal_algorithms.cuda_pc_linear_apx import approx_pc_linear_fx_device
from cpu_parallel import x_values, y_values, epsilon_values, pieces_range, count_total_cases
from numba import njit


GLOBAL_XVALS = np.asarray(x_values, dtype=np.float64)
GLOBAL_YVALS = np.asarray(y_values, dtype=np.float64)
GLOBAL_ALGO = None

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



@njit(cache=True, fastmath=True)
def _find_segment(xs, x):
    # xs is increasing, returns i such that xs[i] <= x <= xs[i+1]
    n = xs.shape[0]
    if x <= xs[0]:
        return 0
    if x >= xs[n-1]:
        return n - 2
    lo, hi = 0, n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xs[mid] <= x:
            lo = mid
        else:
            hi = mid
    return lo

@njit(cache=True, fastmath=True)
def numba_is_within_epsilon(original_fx, approximation, epsilon):
    """
    O(n log m) check: n original points, m segments in approx.
    No Python objects, no NaNs, no per-point division.
    """
    n_orig = original_fx.shape[0]
    n_appr = approximation.shape[0]
    if n_appr < 2:
        # treat as constant segment
        ay0 = approximation[0,1] if n_appr == 1 else 0.0
        for oi in range(n_orig):
            if abs(original_fx[oi,1] - ay0) > epsilon + 1e-9*abs(original_fx[oi,1]):
                return False, 0.0
        return True, 0.0

    ax = approximation[:,0]
    ay = approximation[:,1]

    # precompute slopes once
    seg_n = n_appr - 1
    slopes = np.empty(seg_n, np.float64)
    for i in range(seg_n):
        dx = ax[i+1] - ax[i]
        if abs(dx) < 1e-12:
            slopes[i] = 0.0
        else:
            slopes[i] = (ay[i+1] - ay[i]) / dx

    for oi in range(n_orig):
        x = original_fx[oi,0]
        y = original_fx[oi,1]
        i = _find_segment(ax, x)
        # y_hat = y_i + slope_i * (x - x_i)
        y_hat = ay[i] + slopes[i] * (x - ax[i])
        if abs(y - y_hat) > epsilon + 1e-9 * abs(y):
            return False, 0.0
    return True, 0.0

from numba import cuda, float64
import math

@cuda.jit(device=True)
def device_is_within_epsilon(orig_x, orig_y, appr_x, appr_y, n_orig, n_appr, eps):
    """
    GPU device version of numba_is_within_epsilon.
    orig_x, orig_y, appr_x, appr_y are 1D float64 arrays on device/local memory.
    Returns True if all original points are within epsilon tolerance of approximation.
    """
    # Handle degenerate case (constant segment)
    if n_appr < 2:
        ay0 = appr_y[0] if n_appr == 1 else 0.0
        for oi in range(n_orig):
            diff = abs(orig_y[oi] - ay0)
            if diff > eps + 1e-9 * abs(orig_y[oi]):
                return False
        return True

    seg_n = n_appr - 1
    # Precompute slopes
    slopes = cuda.local.array(64, dtype=float64)  # adjust if you ever have >64 segments
    for i in range(seg_n):
        dx = appr_x[i+1] - appr_x[i]
        if abs(dx) < 1e-12:
            slopes[i] = 0.0
        else:
            slopes[i] = (appr_y[i+1] - appr_y[i]) / dx

    # For each original point
    for oi in range(n_orig):
        x = orig_x[oi]
        y = orig_y[oi]

        # binary search for segment index
        lo = 0
        hi = n_appr - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if appr_x[mid] <= x:
                lo = mid
            else:
                hi = mid

        y_hat = appr_y[lo] + slopes[lo] * (x - appr_x[lo])
        if abs(y - y_hat) > eps + 1e-9 * abs(y):
            return False

    return True


def x_combos(m):
    """
    Stream all strictly increasing (m+1)-tuples of indices from [0, n-1].
    Tuple = (i1, i2, ..., im, b) where the last index is the right boundary.
    """
    return itertools.combinations(range(len(GLOBAL_XVALS)), m)

# -------- helper for base-B tuple generation --------
@njit(cache=True)
def _digits_base(idx, base, length, out):
    """Convert idx into base-`base` digits (left-padded) of length `length`."""
    for p in range(length - 1, -1, -1):
        out[p] = idx % base
        idx //= base


def _worker_init(algorithm):
    global GLOBAL_ALGO
    GLOBAL_ALGO = algorithm

from numba import cuda, float64, int64

@cuda.jit
def cuda_worker_chunk(x_vals, y_vals, trans_xs, eps, base, start, end,
                      epsilon_fails, optimality_fails, total_fails):
    """
    GPU kernel version of the inner test loop.
    Each thread processes one linear_idx (test case).
    """
    tid = cuda.grid(1)
    linear_idx = start + tid
    if linear_idx >= end:
        return

    m_plus_1 = trans_xs.shape[0]
    idx_buf = cuda.local.array(10, dtype=int64)  # supports up to 10 breakpoints
    points_x = cuda.local.array(10, dtype=float64)
    points_y = cuda.local.array(10, dtype=float64)

    # base-B digit expansion
    idx = linear_idx
    for p in range(m_plus_1 - 1, -1, -1):
        idx_buf[p] = idx % base
        idx //= base
        points_x[p] = trans_xs[p]
        points_y[p] = y_vals[idx_buf[p]]

    # ---------- Buffers for optimizer ----------
    MAX_OUT = 16 #32
    CAP_YBUF = 256 #1024
    Q_CAP = 64 #256
    out_x = cuda.local.array(MAX_OUT, dtype=float64)
    out_y = cuda.local.array(MAX_OUT, dtype=float64)
    ybuf = cuda.local.array(CAP_YBUF, dtype=float64)
    q_xy = cuda.local.array(Q_CAP, dtype=float64)


    test1 = not device_is_within_epsilon(points_x, points_y,
                                  points_x, points_y,
                                  m_plus_1, m_plus_1, eps)

    # ---------- Call optimizer (device version) ----------
    n_piv = m_plus_1
    count = approx_pc_linear_fx_device(points_x, points_y, n_piv, eps,
                                       out_x, out_y, MAX_OUT,
                                       ybuf, CAP_YBUF,
                                       q_xy, Q_CAP)
    test2 = count > n_piv

    if test1:
        cuda.atomic.add(epsilon_fails, 0, 1)
    if test2:
        cuda.atomic.add(optimality_fails, 0, 1)
    if test1 or test2:
        cuda.atomic.add(total_fails, 0, 1)


def _worker_chunk_cuda(args):
    (m, eps, trans_indices, y_range) = args
    start, end = y_range
    total_cases = end - start

    threads_per_block = 64 #128
    blocks_per_grid = (total_cases + threads_per_block - 1) // threads_per_block

    epsilon_fails = cuda.to_device(np.zeros(1, dtype=np.int64))
    optimality_fails = cuda.to_device(np.zeros(1, dtype=np.int64))
    total_fails = cuda.to_device(np.zeros(1, dtype=np.int64))

    # ✅ FIX START — flatten trans_indices safely before indexing
    trans_idx = np.asarray(trans_indices, dtype=np.int64).ravel()
    trans_xs = np.asarray(GLOBAL_XVALS[trans_idx], dtype=np.float64)
    # ✅ FIX END

    cuda_worker_chunk[blocks_per_grid, threads_per_block](
        GLOBAL_XVALS, GLOBAL_YVALS,
        trans_xs,               # use flattened version here
        eps, len(GLOBAL_YVALS), start, end,
        epsilon_fails, optimality_fails, total_fails
    )

    cuda.synchronize()

    return (
        total_cases,
        int(epsilon_fails.copy_to_host()[0]),
        int(optimality_fails.copy_to_host()[0]),
        int(total_fails.copy_to_host()[0]),
    )


# -------- optimized worker function --------
_worker_warmed_up = False

# def _worker_chunk(args):
#     """
#     Process a chunk of y-tuples for one (m, eps, indices) config.
#     Optimized for minimal allocations and Python overhead.
#     """
#     global _worker_warmed_up
#     (m, eps, trans_indices, y_range) = args
#     x_vals = GLOBAL_XVALS
#     y_vals = GLOBAL_YVALS
#     algorithm = GLOBAL_ALGO
#     start, end = y_range
#
#     # --------------- Warm-up (JIT compile numba kernels once) ---------------
#     if not _worker_warmed_up:
#         dummy_points = np.array([[0.0, 2.0], [1.0, 3.0], [2.0, 1.0]], dtype=np.float64)
#         _ = numba_is_within_epsilon(dummy_points, dummy_points, 0.1)
#         _ = algorithm(dummy_points, 0.1)
#         _ = numba_approximate_pc_linear_fx(dummy_points,0.1)
#
#         _worker_warmed_up = True
#     # -----------------------------------------------------------------------
#
#     tested = epsilon_fail = optimality_fail = total_fail = 0
#
#     x_arr = GLOBAL_XVALS
#     trans_idx = np.asarray(trans_indices, dtype=np.int64)
#     trans_xs = x_arr[trans_idx]
#
#     m_plus_1 = trans_xs.shape[0]
#
#     # preallocate reusable arrays
#     points = np.empty((m_plus_1, 2), dtype=np.float64)
#     points[:, 0] = trans_xs  # x fixed
#     idx_buf = np.empty(m_plus_1, dtype=np.int64)
#     #y_vals = np.asarray(y_values, dtype=np.float64)
#     base = GLOBAL_YVALS.shape[0]
#
#     # iterate through the range using base-B digit expansion
#     for linear_idx in range(start, end):
#         _digits_base(linear_idx, base, m_plus_1, idx_buf)
#
#         # fill y-values
#         for k in range(m_plus_1):
#             points[k, 1] = GLOBAL_YVALS[idx_buf[k]]
#
#         # candidate algorithm
#         apx_fx, alg_pieces, _ = algorithm(points, eps)
#         if not isinstance(apx_fx, np.ndarray):
#             apx_fx = np.asarray(apx_fx, dtype=np.float64)
#         else:
#             apx_fx = apx_fx.astype(np.float64, copy=False)
#
#         # oracle (optimal)
#         optimal_pc_fx, optimal_num_pieces, given_num_pieces = numba_approximate_pc_linear_fx(points, eps)
#
#         # tests
#         test1 = not numba_is_within_epsilon(points, apx_fx, eps)
#         test2 = alg_pieces > optimal_num_pieces
#
#         if test1:
#             epsilon_fail += 1
#         if test2:
#             optimality_fail += 1
#         if test1 or test2:
#             total_fail += 1
#
#         tested += 1
#
#     return tested, epsilon_fail, optimality_fail, total_fail


# ---------------- Parallel driver ----------------
def test_algorithm(algorithm,
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

    #x_as_float = [float(v) for v in x_values]

    tested = epsilon_fail = optimality_fail = total_fail = 0
    total_theoretical = count_total_cases(len(x_values), len(y_values), len(epsilon_values), pieces_range)
    print(f"Theoretical total test cases (full grid): {total_theoretical:,}")

    def task_generator():
        for m in pieces_range:
            for eps in epsilon_values:
                for indices in x_combos(m + 1):
                    trans_indices = indices
                    total_y = len(GLOBAL_YVALS) ** (m+1)
                    for start in range(0, total_y, chunk_size):
                        end = min(start + chunk_size, total_y)
                        yield (m, eps, trans_indices,(start, end))

    with ProcessPoolExecutor(max_workers=max_workers, initializer=_worker_init, initargs=(algorithm,)) as ex:
        for t, e1, e2, tf in ex.map(_worker_chunk_cuda, task_generator(), chunksize=64):
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
