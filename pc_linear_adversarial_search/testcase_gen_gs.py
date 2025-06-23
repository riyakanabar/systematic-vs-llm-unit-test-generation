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
    total = 0
    for num_pieces in pieces:
        num_x_choices = len(list(itertools.combinations(x_values, num_pieces + 1)))
        num_y_combinations = len(y_values) ** (num_pieces + 1)
        total += num_x_choices * num_y_combinations * len(epsilon_values)
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
    Test an algorithm to find a counterexample where it's not optimal.
    Generates valid piecewise linear test cases.
    """
    print("Running test_algorithm...")
    start_time = time.time()

    total_cases = estimate_total_cases()
    print(f"Estimated total test cases: {total_cases}")

    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=total_cases, desc="Testing", unit="case")
    except ImportError:
        progress_bar = None
        print("Install tqdm for progress tracking")

    count = 0

    for num_pieces in pieces:
        # You need num_pieces + 1 x-points
        x_combinations = list(itertools.combinations(x_values, num_pieces + 1))

        for epsilon in epsilon_values:
            for x_comb in x_combinations:
                for y_comb in itertools.product(y_values, repeat=len(x_comb)):
                    points = [(float(x), float(y)) for x, y in zip(x_comb, y_comb)]

                    count += 1
                    if progress_bar:
                        progress_bar.update(1)
                    print(f"Testcase{count}: {points} and epsilon is {epsilon}")
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

    if progress_bar:
        progress_bar.close()
    elapsed_time = time.time() - start_time
    print(f"No counterexample found after testing {count} cases. (Time: {elapsed_time:.2f}s)")
    return None
