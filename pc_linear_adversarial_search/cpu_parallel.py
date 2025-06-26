import itertools
import time
import numpy as np
import sys
import os
import multiprocessing as mp
from functools import partial
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from optimal_algorithms.pc_linear_apx import approximate_pc_linear_fx

# Test case parameters
x_values = range(0, 11)
y_values = range(1, 11)
epsilon_values = [0.1, 0.25, 0.5, 0.7, 1, 1.5, 2, 3, 5, 7]
pieces = range(1, 11)


def is_within_epsilon(original_fx, approximation, epsilon):
    """
    Check if the approximation is within epsilon of the original function
    """
    # Sort both functions by x-values
    original_fx = sorted(original_fx, key=lambda p: p[0])
    approximation = sorted(approximation, key=lambda p: p[0])

    for x, orig_y in original_fx:
        approx_y = None
        for i in range(len(approximation) - 1):
            if approximation[i][0] <= x <= approximation[i + 1][0]:
                slope = (approximation[i + 1][1] - approximation[i][1]) / (
                        approximation[i + 1][0] - approximation[i][0])
                intercept = approximation[i][1] - slope * approximation[i][0]
                approx_y = slope * x + intercept
                rounded_approx_y = round(approx_y, 1)
                break
        if approx_y is None and approximation:  # Handle case where x is outside the range
            approx_y = approximation[-1][1]

        if not np.isclose(orig_y, rounded_approx_y, atol=epsilon, rtol=1e-6):
            return False, f"At x={x}: orig_y={orig_y}, approx_y={approx_y} rounded={rounded_approx_y}"

    return True, ""


def generate_test_cases():
    """
    Generator function that yields test cases
    """
    count = 0
    for num_pieces in pieces:
        # You need num_pieces + 1 x-points
        x_combinations = list(itertools.combinations(x_values, num_pieces + 1))

        for epsilon in epsilon_values:
            for x_comb in x_combinations:
                for y_comb in itertools.product(y_values, repeat=len(x_comb)):
                    points = [(float(x), float(y)) for x, y in zip(x_comb, y_comb)]
                    yield (points, epsilon, count)
                    count += 1


def estimate_total_cases():
    """
    Estimate the total number of test cases
    """
    total = 0
    for num_pieces in pieces:
        num_x_choices = len(list(itertools.combinations(x_values, num_pieces + 1)))
        num_y_combinations = len(y_values) ** (num_pieces + 1)
        total += num_x_choices * num_y_combinations * len(epsilon_values)
    return total


def evaluate_test_case(args):
    """
    Evaluate if the algorithm fails the test case compared to the optimal algorithm
    """
    points, epsilon, count, algorithm = args

    # Run the algorithm being tested
    apx_fx, alg_pieces, _ = algorithm(points, epsilon)

    # Run the optimal algorithm for comparison
    optimal_fx, opt_pieces, given_pieces = approximate_pc_linear_fx(points, epsilon)

    # Test 1: Check if the approximation is within epsilon
    within_epsilon, error_msg = is_within_epsilon(points, apx_fx, epsilon)
    if not within_epsilon:
        return (True, "epsilon_bound", points, epsilon, apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces, count,
                error_msg)

    # Test 2: Check if algorithm uses more pieces than optimal
    if alg_pieces > opt_pieces:
        return (
        True, "num_pieces", points, epsilon, apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces, count, "")

    return (False, "", None, None, None, None, None, None, None, count, "")


def test_algorithm_parallel(algorithm):
    """
    Test an algorithm in parallel to find a counterexample where it's not optimal.
    Generates valid piecewise linear test cases.
    """
    print("Running test_algorithm in parallel...")
    start_time = time.time()

    def test_case_generator():
        for points, epsilon, count in generate_test_cases():
            yield (points, epsilon, count, algorithm)

    total_cases = estimate_total_cases()
    print(f"Estimated total test cases: {total_cases}")

    # Use all available CPU cores except one
    num_processes = max(1, mp.cpu_count() - 1)
    print(f"Using {num_processes} processes")

    with mp.Pool(processes=num_processes) as pool:
        try:
            with tqdm(total=total_cases, desc="Testing", unit="case") as progress:
                for result in pool.imap_unordered(evaluate_test_case, test_case_generator(), chunksize=10):
                    failed, test_name, points, epsilon, apx_fx, alg_pieces, optimal_fx, opt_pieces, given_pieces, count, error_msg = result
                    progress.update(1)

                    if failed:
                        progress.close()
                        pool.terminate()
                        elapsed_time = time.time() - start_time
                        print(f"\nFound counterexample after {count} cases! (Time: {elapsed_time:.2f}s)")
                        print(f"Failure type: {test_name}")
                        print(f"Testcase: {points}")
                        print(f"Epsilon: {epsilon}")
                        if error_msg:
                            print(f"Error: {error_msg}")
                        print(f"Approximated function: {apx_fx}")
                        print(f"Algorithm pieces: {alg_pieces}")
                        print(f"Optimal function: {optimal_fx}")
                        print(f"Optimal pieces: {opt_pieces}")
                        print(f"Given pieces: {given_pieces}")
                        return points, epsilon
        except KeyboardInterrupt:
            print("\nInterrupted by user. Terminating...")
            pool.terminate()
            return None

    elapsed_time = time.time() - start_time
    print(f"No counterexample found after testing {total_cases} cases. (Time: {elapsed_time:.2f}s)")
    return None
