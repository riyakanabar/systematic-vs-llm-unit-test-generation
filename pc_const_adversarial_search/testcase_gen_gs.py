import itertools
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
from grid_search.variants_test import is_within_epsilon

x_values = range(0, 3)
y_values = range(1, 3)
epsilon_values = [0.1] #[0.1, 0.25, 0.5, 0.7, 1, 1.5, 2, 3, 5, 7]
pieces = [2]


def generate_test_case(x_indices, y_values_for_points, x_values):
    points = [[-float('inf'), float('inf')]]

    # Add the transition points
    for i, x_idx in enumerate(x_indices):
        x = x_values[x_idx]
        y = y_values_for_points[i]
        points.append([float(x), float(y)])

    # Add the next x-value after the last transition as the infinity boundary
    if len(x_indices) > 0:
        last_x_idx = x_indices[-1]
        next_x_idx = last_x_idx + 1
        if next_x_idx < len(x_values):
            next_x = float(x_values[next_x_idx])
        else:
            next_x = float(x_values[-1] + 1)
    else:
        next_x = float(x_values[0] + 1)

    points.append([next_x, float('inf')])

    return points


def evaluate_test_case(pc_cons_fx, epsilon, algorithm):
    """Evaluate if the algorithm fails the test case compared to the optimal algorithm"""

    apx_fx, alg_pieces, _ = algorithm(pc_cons_fx, epsilon)
    optimal_pc_fx, optimal_num_pieces, given_pieces = approximate_pc_shortest_path(pc_cons_fx, epsilon)

    # -------------- Test 1: Epsilon Difference --------------
    if not is_within_epsilon(pc_cons_fx, apx_fx, epsilon):
        return True, "epsilon_bound", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_pieces

    # -----Test 2:  Check if algorithm uses more pieces than optimal pieces
    if alg_pieces > optimal_num_pieces:
        return True, "num_pieces", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_pieces

    return False, "", apx_fx, alg_pieces, optimal_num_pieces, optimal_num_pieces, given_pieces


def test_algorithm(algorithm):
    """Find a counterexample where the given algorithm fails the optimality"""
    count = 0
    total_test_cases = 0

    # For each x-index, we want to test all possible next x-values as infinity boundaries
    # For pieces=1, this means for each x in [0,1,2], we test infinity at [1,2,3]
    # This gives us 3 x-indices × 3 y-values × 3 possible infinity boundaries = 27 test cases
    # But we exclude cases where infinity boundary ≤ x-index, so we get 3+2+1=6 valid x-index/boundary pairs
    # With 3 y-values, that's 6 × 3 = 18 test cases

    # Calculate total number of valid test cases
    for num_pieces in pieces:
        valid_combinations = 0
        for x_idx in range(len(x_values) - 1):  # Exclude last x-value as it needs a next value
            for boundary_idx in range(x_idx + 1, len(x_values)):
                valid_combinations += 1

        total_test_cases = valid_combinations * (len(y_values) ** num_pieces) * len(epsilon_values)

    print(f"Total test cases to evaluate: {total_test_cases}")

    # Set up progress bar if tqdm is available
    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=total_test_cases, desc="Testing", unit="case")
    except ImportError:
        progress_bar = None

    for num_pieces in pieces:
        for epsilon in epsilon_values:
            # Instead of using combinations, we'll manually create the test cases
            # to ensure we get all combinations of x-indices with different infinity boundaries
            for x_idx in range(len(x_values) - 1):  # Exclude last x-value
                for boundary_idx in range(x_idx + 1, len(x_values)):
                    for y_value in y_values:
                        # Create the test case with the specified x-index, y-value, and infinity boundary
                        points = [[-float('inf'), float('inf')]]
                        points.append([float(x_values[x_idx]), float(y_value)])
                        points.append([float(x_values[boundary_idx]), float('inf')])

                        count += 1
                        print(f"Testcase: {count}")
                        print(f"fx: {points}")
                        print(f"pieces: {num_pieces}")
                        print(f"epsilon: {epsilon}")

                        # Update progress bar
                        if progress_bar:
                            progress_bar.update(1)

                        failed, test_name, apx_fx, alg_pieces, optimal_pc_fx, optimal_pieces, given_pieces = evaluate_test_case(
                            points, epsilon, algorithm)

                        if failed:
                            if progress_bar:
                                progress_bar.close()
                            print(f"\nFound counterexample after testing {count} cases!")
                            print(f"Test failed: {test_name}")
                            print(f"Testcase: {points}")
                            print(f"Epsilon: {epsilon}")
                            print(f"Given Pieces: {given_pieces}")
                            print(f"Approximated function: {apx_fx}")
                            print(f"Algorithm pieces: {alg_pieces}")
                            print(f"Optimal function: {optimal_pc_fx}")
                            print(f"Optimal pieces: {optimal_pieces}")
                            return points, epsilon

    if progress_bar:
        progress_bar.close()
    print(f"\nNo counterexample found after testing {count} cases!")
    return None
