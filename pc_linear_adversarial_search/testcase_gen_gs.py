import itertools
import time
import numpy as np
import sys
import os

# Add parent directory to path to import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from optimal_algorithms.pc_linear_apx import approximate_pc_linear_fx, reconstruct_piecewise_function

# Test case parameters
x_values =  range(0, 4)
y_values =  range(1, 4)
epsilon_values = [0.1, 0.25,0.5]
pieces = range(1,4)


def is_within_epsilon(original_fx, approximation, epsilon):
    original_y_values = reconstruct_piecewise_function(original_fx)
    approx_y_values = reconstruct_piecewise_function(approximation)
    for orig_y, approx_y in zip(original_y_values, approx_y_values):
        if not np.isclose(orig_y, approx_y, atol=epsilon, rtol=1e-6):
            print("here")
            print(original_y_values, approx_y_values)
            return False
    return True


def estimate_total_cases():
    """
    Estimate the total number of test cases to be generated
    """
    total = 0
    for num_pieces in pieces:
        # Number of ways to select x transition points
        x_combinations = len(list(itertools.combinations(range(len(x_values) - 1), num_pieces)))
        # For each x combination, we have |y_values|^num_pieces possible y values
        total += x_combinations * (len(y_values) ** num_pieces) * len(epsilon_values)
    return total


def evaluate_test_case(points, epsilon, algorithm):
    """
    Evaluate if the algorithm fails the test case compared to the optimal algorithm
    """
    # Run the algorithm being tested
    apx_fx, alg_pieces, _ = algorithm(points, epsilon)

    # Run the optimal algorithm for comparison
    optimal_fx, opt_pieces, given_pieces = approximate_pc_linear_fx(points, epsilon)

    # Test 1: Check if the approximation is within epsilon
    if not is_within_epsilon(points, np.round(apx_fx,2), epsilon):
        return True, "epsilon_bound", apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces

    # Test 2: Check if algorithm uses more pieces than optimal
    if alg_pieces > opt_pieces:
        return True, "num_pieces", apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces

    return False, "", apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces


def test_algorithm(algorithm):
    """
    Test an algorithm to find a counterexample where it's not optimal
    """
    print("Running test_algorithm...")
    start_time = time.time()

    # Calculate total test cases for progress tracking
    total_cases = estimate_total_cases()
    print(f"Estimated total test cases: {total_cases}")

    # Set up progress tracking
    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=total_cases, desc="Testing", unit="case")
    except ImportError:
        progress_bar = None
        print("Install tqdm for progress tracking")

    count = 0

    # Precompute x combinations for each number of pieces
    precomputed_x_combinations = {
        num_pieces: list(itertools.combinations(range(len(x_values) - 1), num_pieces))
        for num_pieces in pieces
    }

    for num_pieces in pieces:
        x_combinations = precomputed_x_combinations[num_pieces]
        for epsilon in epsilon_values:
            for x_indices in x_combinations:
                # Get the boundary index (last x value)
                boundary_idx = len(x_values) - 1

                # Generate all combinations of y values for the transition points
                for y_comb in itertools.product(y_values, repeat=num_pieces):
                    # Create the test case with the specified transition points
                    points = []

                    # Add the start point
                    points.append((float(x_values[0]), float(y_values[0])))

                    # Add each transition point with its y-value
                    for i, x_idx in enumerate(x_indices):
                        points.append((float(x_values[x_idx + 1]), float(y_comb[i])))

                    # Add the end point
                    points.append((float(x_values[boundary_idx]), float(y_values[-1])))

                    count += 1

                    if progress_bar:
                        progress_bar.update(1)

                    # Evaluate this test case
                    failed, test_name, apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces = evaluate_test_case(
                        points, epsilon, algorithm)

                    if failed:
                        if progress_bar:
                            progress_bar.close()
                        elapsed_time = time.time() - start_time
                        print(f"\nFound counterexample after {count} cases! (Time: {elapsed_time:.2f}s)")
                        print(f"Failure type: {test_name}")
                        print(f"Testcase: {points}")
                        print(f"Epsilon: {epsilon}")
                        print(f"Approximated function: {apx_fx}")
                        print(f"Algorithm pieces: {alg_pieces}")
                        print(f"Optimal pieces: {opt_pieces}")
                        print(f"Given pieces: {given_pieces}")
                        return points, epsilon

    # Clean up and report results
    if progress_bar:
        progress_bar.close()

    elapsed_time = time.time() - start_time
    print(f"No counterexample found after testing {count} cases. (Time: {elapsed_time:.2f}s)")
    return None
