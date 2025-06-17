import itertools
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
from grid_search.variants_test import is_within_epsilon

x_values = range(0, 11)
y_values = range(1, 11)
epsilon_values = [0.1, 0.25, 0.5, 0.7, 1, 1.5, 2, 3, 5, 7]
pieces = range(1,11)

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
    precomputed_x_combinations = {
        num_pieces: list(itertools.combinations(range(len(x_values) - 1), num_pieces))
        for num_pieces in pieces
    }
    for num_pieces in pieces:
        x_combinations = precomputed_x_combinations[num_pieces]
        # For each combination, we need to add a boundary point after the last x-index
        valid_combinations = 0
        for x_indices in x_combinations:
            if not x_indices:  # Handle empty combinations (0 pieces)
                valid_combinations += 1
                continue

            # For each combination, count valid boundary positions
            last_x_idx = x_indices[-1]
            for boundary_idx in range(last_x_idx + 1, len(x_values)):
                valid_combinations += 1

        # Each test case has num_pieces y-values and 1 epsilon value
        total_test_cases += valid_combinations * (len(y_values) ** num_pieces) * len(epsilon_values)

    print(f"Total test cases to evaluate: {total_test_cases}")

    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=total_test_cases, desc="Testing", unit="case")
    except ImportError:
        progress_bar = None

    for num_pieces in pieces:
        x_combinations = precomputed_x_combinations[num_pieces]
        for epsilon in epsilon_values:
            for x_indices in x_combinations:
                # For each combination of x-indices, we need to add a boundary point after the last x-index
                if not x_indices:  # Handle empty combinations (0 pieces)
                    # Special case for 0 pieces: just -inf to +inf
                    points = [[-float('inf'), float('inf')], [float(x_values[0]), float('inf')]]
                    count += 1
                    # print(f"Testcase: {count}")
                    # print(f"fx: {points}")
                    # print(f"pieces: {num_pieces}")
                    # print(f"epsilon: {epsilon}")
                    continue

                # For each valid boundary position after the last x-index
                last_x_idx = x_indices[-1]
                for boundary_idx in range(last_x_idx + 1, len(x_values)):
                    # Generate all combinations of y-values for the transition points
                    for y_values_combination in itertools.product(y_values, repeat=num_pieces):
                        # Create the test case with the specified transition points
                        points = [[-float('inf'), float('inf')]]

                        # Add each transition point with its y-value
                        for i, x_idx in enumerate(x_indices):
                            points.append([float(x_values[x_idx]), float(y_values_combination[i])])

                        # Add the infinity boundary
                        points.append([float(x_values[boundary_idx]), float('inf')])

                        count += 1
                        # print(f"Testcase: {count}")
                        # print(f"fx: {points}")
                        # print(f"pieces: {num_pieces}")
                        # print(f"epsilon: {epsilon}")

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
