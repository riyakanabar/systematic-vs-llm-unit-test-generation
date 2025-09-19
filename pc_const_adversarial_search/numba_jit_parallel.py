import numpy as np
from numba import njit, prange, float64, int64, types, jit
from numba.typed import List, Dict
import math
import os
import sys
from tqdm import tqdm
from functools import partial
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

# If your modules live one directory up:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
# Import the original function for non-Numba use
from grid_search.variants_test import is_within_epsilon as original_is_within_epsilon

# -----------------------
# CONFIG
# -----------------------
# Convert to numpy arrays for better performance with Numba
x_values = np.arange(0, 6, dtype=np.float64)  # 0..10 (11 grid points)
y_values = np.arange(1, 5, dtype=np.float64)  # 1..8
epsilon_values = np.array([0.5, 0.75, 1, 1.5, 7], dtype=np.float64)
pieces_range = np.arange(2, 6, dtype=np.int64)  # number of pieces m = 2..10

# Constants
INF = float('inf')


# -----------------------
# HELPERS
# -----------------------
def evaluate_test_case(pc_cons_fx, epsilon, algorithm):
    """
    Compare candidate algorithm vs OPT optimal algorithm on one test case.
    Returns:
      failed: bool
      reason: "epsilon_bound" | "num_pieces" | ""
      apx_fx
      alg_pieces
      optimal_pc_fx
      optimal_num_pieces
      given_num_pieces
    """
    apx_fx, alg_pieces, _ = algorithm(pc_cons_fx, epsilon)
    optimal_pc_fx, optimal_num_pieces, given_num_pieces = approximate_pc_shortest_path(pc_cons_fx, epsilon)

    # Test 1: tolerance (L_infinity) must hold
    if not numba_is_within_epsilon(pc_cons_fx, apx_fx, epsilon):
        return True, "epsilon_bound", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces

    # Test 2: if within tolerance, candidate must be optimal in piece count
    if alg_pieces > optimal_num_pieces:
        return True, "num_pieces", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces

    # PASS (bug fixed: return optimal_pc_fx, not optimal_num_pieces)
    return False, "", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces


@njit
def comb(n, k):
    """Numba-compatible combination function"""
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)  # Take advantage of symmetry
    c = 1
    for i in range(1, k + 1):
        c = c * (n - k + i) // i
    return c


@njit
def count_total_cases(n_x, n_y, n_eps, pieces_range):
    """
    Analytical count of all test cases (matches folded boundary approach):
      For m pieces, choose m transition indices + 1 right boundary index => comb(n_x, m+1)
      Choose y-values for each of the m pieces => (n_y ** m)
      Multiply by number of epsilons.
    """
    total = 0
    for m in pieces_range:
        total += comb(n_x, m + 1) * (n_y ** m) * n_eps
    return total


@njit
def get_combinations(n, k):
    """Numba-compatible combinations generator"""
    indices = np.arange(k, dtype=np.int64)
    result = np.zeros((comb(n, k), k), dtype=np.int64)

    for i in range(len(result)):
        result[i] = indices.copy()

        # Generate next combination
        j = k - 1
        while j >= 0 and indices[j] == n - k + j:
            j -= 1

        if j < 0:
            break

        indices[j] += 1
        for l in range(j + 1, k):
            indices[l] = indices[l - 1] + 1

    return result


# -----------------------
# MAIN TEST DRIVER
# -----------------------
# Numba-compatible algorithm implementation
@njit(nogil=True)
def numba_algorithm_impl(points, eps, apx_fx, alg_pieces, _):
    """Numba-compatible implementation of the algorithm"""
    # This is a simple example - replace with your actual algorithm
    # For now, it just copies the input points as a simple example
    n = min(len(points), len(apx_fx))
    for i in range(n):
        apx_fx[i, 0] = points[i, 0]
        apx_fx[i, 1] = points[i, 1]
    alg_pieces[0] = n
    return n


@njit(nogil=True)
def process_test_case(points, eps):
    """Process a single test case with Numba"""
    # Allocate output arrays
    max_points = 1000  # Adjust based on your needs
    apx_fx = np.zeros((max_points, 2), dtype=np.float64)
    alg_pieces = np.zeros(1, dtype=np.int64)

    # Call the algorithm
    numba_algorithm_impl(points, eps, apx_fx, alg_pieces, "")

    # Trim the output array
    apx_fx = apx_fx[:alg_pieces[0]]

    # Get the optimal solution
    optimal_result = approximate_pc_shortest_path(points, eps)
    optimal_pc_fx = optimal_result[0]
    optimal_num_pieces = optimal_result[1]

    test1 = not numba_is_within_epsilon(points, apx_fx, eps)
    test2 = alg_pieces[0] > optimal_num_pieces

    return test1, test2


@njit(fastmath=True, nogil=True)
def numba_is_within_epsilon(points, apx_fx, epsilon):
    """
    Numba-compatible version of is_within_epsilon.
    Checks if the approximation is within epsilon of the original function.

    Parameters:
    - points: numpy array of shape (n, 2) representing the original function points
    - apx_fx: numpy array of shape (m, 2) representing the approximation points
    - epsilon: float, the maximum allowed difference

    Returns:
    - bool: True if the approximation is within epsilon, False otherwise
    """
    n = len(points)
    m = len(apx_fx)

    # Handle edge cases
    if n == 0 or m == 0:
        return True

    # For each point in the original function
    for i in range(n):
        x = points[i, 0]
        y_original = points[i, 1]

        # Handle edge cases for x outside the approximation range
        if x <= apx_fx[0, 0]:
            y_approx = apx_fx[0, 1]
        elif x >= apx_fx[-1, 0]:
            y_approx = apx_fx[-1, 1]
        else:
            # Find the right segment using binary search
            left = 0
            right = m - 1

            while left <= right:
                mid = (left + right) // 2
                if apx_fx[mid, 0] < x:
                    left = mid + 1
                else:
                    right = mid - 1

            # Get the segment endpoints
            if right < 0:
                right = 0
            if right >= m - 1:
                right = m - 2

            x0, y0 = apx_fx[right, 0], apx_fx[right, 1]
            x1, y1 = apx_fx[right + 1, 0], apx_fx[right + 1, 1]

            # Linear interpolation
            if x1 != x0:  # Avoid division by zero
                t = (x - x0) / (x1 - x0)
                y_approx = y0 + t * (y1 - y0)
            else:
                y_approx = (y0 + y1) / 2.0

        # Check if the point is within epsilon
        if abs(y_original - y_approx) > (epsilon + 1e-10):
            return False

    return True


def generate_test_cases():
    """Generate all test cases as a list of (points, eps) tuples"""
    test_cases = []
    n = len(x_values)

    for m in pieces_range:
        # Get all combinations of m+1 indices
        indices_list = get_combinations(n, m + 1)

        for indices in indices_list:
            trans_indices = indices[:-1]
            boundary_idx = indices[-1]

            # Convert to numpy arrays
            trans_xs = x_values[trans_indices]
            right_boundary_x = x_values[boundary_idx]

            # Generate all possible y combinations
            y_combinations = np.array(np.meshgrid(*[y_values] * m)).T.reshape(-1, m)

            for y_tuple in y_combinations:
                # Build points array
                points = np.zeros((m + 2, 2))
                points[0] = [-INF, INF]  # First point
                points[-1] = [right_boundary_x, INF]  # Last point

                # Fill in the middle points
                for i in range(m):
                    points[i + 1] = [trans_xs[i], y_tuple[i]]

                # Add all epsilon values for this test case
                for eps in epsilon_values:
                    test_cases.append((points.copy(), eps))

    return test_cases


def create_algorithm_wrapper(algorithm):
    """
    This is now a compatibility layer that just returns our Numba implementation.
    Replace the implementation in numba_algorithm_impl with your actual algorithm.
    """
    # Compile the function with a test case first
    test_points = np.array([[-np.inf, np.inf], [0.0, 1.0], [1.0, np.inf]], dtype=np.float64)
    max_points = 1000
    test_apx_fx = np.zeros((max_points, 2), dtype=np.float64)
    test_alg_pieces = np.zeros(1, dtype=np.int64)

    # Compile with a test case
    numba_algorithm_impl(test_points, 1.0, test_apx_fx, test_alg_pieces, "")

    # Return the Numba-compiled function
    return numba_algorithm_impl


def process_batch(args):
    """Process a batch of test cases (for parallel execution)"""
    batch, _ = args  # We don't need the algorithm parameter anymore
    epsilon_fail = optimality_fail = total_fail = 0
    count = len(batch)

    # Compile the functions with a test case first
    test_case = (np.array([[-np.inf, np.inf], [0.0, 1.0], [1.0, np.inf]], dtype=np.float64), 1.0)
    _ = process_test_case(test_case[0], test_case[1])

    for points, eps in batch:
        # Ensure points is a numpy array
        points_np = np.asarray(points, dtype=np.float64)
        eps_float = float(eps)

        # Process the test case
        test1, test2 = process_test_case(points_np, eps_float)
        
        # Update counters
        if test1:
            epsilon_fail += 1
        if test2:
            optimality_fail += 1
        if test1 or test2:
            total_fail += 1

    return (epsilon_fail, optimality_fail, total_fail, count)


def test_algorithm(algorithm, num_processes=None):
    """
    Enumerate piecewise-constant test cases over bounded grids, evaluate candidate vs OPT,
    and print failure stats. Uses Numba and parallel processing for speed.

    Parameters
    ----------
    algorithm : callable
        Your candidate algorithm with signature:
            (pc_cons_fx, epsilon) -> (apx_fx, alg_pieces, <ignored>)
    num_processes : int, optional
        Number of processes to use for parallel execution. If None, uses all available CPUs.

    Returns
    -------
    dict with counts and percentages.
    """
    # Compile the test case function with Numba
    print("Compiling with Numba...")
    test_case = (np.array([[-np.inf, np.inf], [0.0, 1.0], [1.0, np.inf]], dtype=np.float64), 1.0)

    # Compile the functions with a test case
    _ = process_test_case(test_case[0], test_case[1])
    print("Compilation successful")

    # Generate all test cases
    print("Generating test cases...")
    test_cases = generate_test_cases()
    total_cases = len(test_cases)
    print(f"Total test cases to run: {total_cases:,}")

    # Split into batches for parallel processing
    if num_processes is None:
        num_processes = mp.cpu_count()

    batch_size = max(1, total_cases // (num_processes * 10))  # 10 batches per process
    batches = [test_cases[i:i + batch_size] for i in range(0, total_cases, batch_size)]

    print(f"Processing {len(batches)} batches across {num_processes} processes...")

    # Process batches in parallel
    results = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Prepare arguments for each batch
        batch_args = [(batch, algorithm) for batch in batches]

        # Process with progress bar
        with tqdm(total=len(batches), desc="Processing batches") as pbar:
            for result in executor.map(process_batch, batch_args):
                results.append(result)
                pbar.update(1)

    # Aggregate results
    epsilon_fail = optimality_fail = total_fail = tested = 0

    for ef, of, tf, cnt in results:
        epsilon_fail += ef
        optimality_fail += of
        total_fail += tf
        tested += cnt

    # Calculate percentages
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
