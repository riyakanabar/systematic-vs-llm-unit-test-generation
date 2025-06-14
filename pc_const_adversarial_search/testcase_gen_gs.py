import itertools
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
from grid_search.variants_test import is_within_epsilon

x_values = range(0, 11)
y_values = range(1, 11)
epsilon_values = [0.1, 0.25, 0.5, 0.7, 1, 1.5, 2, 3, 5, 7]
num_pieces = range(1, 11)

def generate_test_case(x_indices, y_values_for_points, x_values):
    points = [[-float('inf'), float('inf')]]

    # Add the transition points
    for i, x_idx in enumerate(x_indices):
        x = x_values[x_idx]
        y = y_values_for_points[i]
        points.append([float(x), float(y)])

    # Add the final infinity point
    points.append([float(x_values[-1] + 1), float('inf')])

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
    for num_pieces in range(1, 11):
        for epsilon in epsilon_values:
            x_combinations = list(itertools.combinations(range(len(x_values)), num_pieces))
            for x_indices in x_combinations:
                for y_values_combination in itertools.product(y_values, repeat=num_pieces):
                    y_values_for_points = list(y_values_combination)
                    points = generate_test_case(x_indices, y_values_for_points, x_values)
                    count += 1
                    failed, test_name, apx_fx, alg_pieces,optimal_pc_fx, optimal_pieces, given_pieces = evaluate_test_case(points, epsilon, algorithm)

                    if failed:
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
    print(f"\nNo counterexample found after testing {count} cases!")
    return None
