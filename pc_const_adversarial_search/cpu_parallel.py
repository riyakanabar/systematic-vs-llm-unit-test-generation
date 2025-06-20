import itertools
import time
import multiprocessing
import sys
import os
from functools import partial
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
from grid_search.variants_test import is_within_epsilon


x_values = range(0, 11)
y_values = range(1, 11)
epsilon_values = [0.1, 0.25, 0.5, 0.7, 1, 1.5, 2, 3, 5, 7]
pieces = range(1, 11)


def generate_test_cases(batch_size=1000):
    """
    Generator function that yields batches of test cases to reduce memory usage
    """
    count = 0
    batch = []

    # Precompute x combinations for each number of pieces
    precomputed_x_combinations = {
        num_pieces: list(itertools.combinations(range(len(x_values) - 1), num_pieces))
        for num_pieces in pieces
    }

    for num_pieces in pieces:
        x_combinations = precomputed_x_combinations[num_pieces]
        for epsilon in epsilon_values:
            for x_indices in x_combinations:
                if not x_indices:  # Handle empty combinations (0 pieces)
                    points = [[-float('inf'), float('inf')], [float(x_values[0]), float('inf')]]
                    batch.append((points, epsilon, count))
                    count += 1

                    if len(batch) >= batch_size:
                        yield batch
                        batch = []
                    continue

                # For each valid boundary position after the last x-index
                last_x_idx = x_indices[-1]
                for boundary_idx in range(last_x_idx + 1, len(x_values)):
                    # Generate all combinations of y-values for the transition points
                    for y_comb in itertools.product(y_values, repeat=num_pieces):
                        # Create the test case with the specified transition points
                        points = [[-float('inf'), float('inf')]]

                        # Add each transition point with its y-value
                        for i, x_idx in enumerate(x_indices):
                            points.append([float(x_values[x_idx]), float(y_comb[i])])

                        # Add the infinity boundary
                        points.append([float(x_values[boundary_idx]), float('inf')])

                        batch.append((points, epsilon, count))
                        count += 1

                        if len(batch) >= batch_size:
                            yield batch
                            batch = []

    # Yield any remaining test cases
    if batch:
        yield batch


def estimate_total_cases():
    total = 0
    for num_pieces in pieces:
        x_combinations = list(itertools.combinations(range(len(x_values) - 1), num_pieces))
        for x_indices in x_combinations:
            if not x_indices:
                total += len(epsilon_values)
                continue
            last_x_idx = x_indices[-1]
            for boundary_idx in range(last_x_idx + 1, len(x_values)):
                total += (len(y_values) ** num_pieces) * len(epsilon_values)
    return total


def evaluate_test_case_batch(batch, algorithm):
    """
    Evaluate a batch of test cases against the algorithm
    Returns the first counterexample found or None if all pass
    """
    for pc_cons_fx, epsilon, count in batch:
        # Run the algorithm being tested
        apx_fx, alg_pieces, _ = algorithm(pc_cons_fx, epsilon)

        # Run the optimal algorithm for comparison
        optimal_fx, opt_pieces, given_pieces = approximate_pc_shortest_path(pc_cons_fx, epsilon)

        # Test 1: Check if the approximation is within epsilon
        if not is_within_epsilon(pc_cons_fx, apx_fx, epsilon):
            return (
            True, "epsilon_bound", pc_cons_fx, epsilon, apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces, count)

        # Test 2: Check if algorithm uses more pieces than optimal
        if alg_pieces > opt_pieces:
            return (
            True, "num_pieces", pc_cons_fx, epsilon, apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces, count)

    # No counterexample found in this batch
    return (False, "", None, None, None, None, None, None, None, batch[-1][2] if batch else 0)


def test_algorithm_parallel(algorithm, batch_size=1000):
    """
    Test an algorithm in parallel to find a counterexample where it's not optimal
    Uses batched processing to reduce memory usage and improve performance
    """
    print("Running test_algorithm in parallel...")
    start_time = time.time()
    total_cases = estimate_total_cases()
    print(f"Estimated total test cases: {total_cases}")
    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=total_cases, desc="Testing", unit="case")
    except ImportError:
        progress_bar = None
        print("Install tqdm for progress tracking")
    num_processes = max(1, multiprocessing.cpu_count() - 1)
    print(f"Using {num_processes} processes")

    evaluate_batch = partial(evaluate_test_case_batch, algorithm=algorithm)

    # Process batches in parallel
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Process batches in parallel using imap_unordered (lazy evaluation)
        for result in pool.imap_unordered(evaluate_batch, generate_test_cases(batch_size)):
            failed, test_name, fx, epsilon, apx_fx, alg_pieces, opt_fx, opt_pieces, given_pieces, count = result

            # Update progress
            if progress_bar:
                progress_bar.update(batch_size)

            if failed:
                if progress_bar:
                    progress_bar.close()

                elapsed_time = time.time() - start_time
                print(f"\nFound counterexample after {count} cases! (Time: {elapsed_time:.2f}s)")
                print(f"Failure type: {test_name}")
                print(f"Input fx: {fx}")
                print(f"Epsilon: {epsilon}")
                print(f"Approximated fx: {apx_fx}")
                print(f"Algorithm pieces: {alg_pieces}")
                print(f"Optimal fx: {opt_fx}")
                print(f"Optimal pieces: {opt_pieces}")
                print(f"Given pieces: {given_pieces}")
                return fx, epsilon

    if progress_bar:
        progress_bar.close()

    elapsed_time = time.time() - start_time
    print(f"No counterexample found after testing all cases. (Time: {elapsed_time:.2f}s)")
    return None
