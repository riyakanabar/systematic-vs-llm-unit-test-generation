import itertools
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
from grid_search.variants_test import is_within_epsilon
import math
x_values = range(0, 11)
y_values = range(1, 11)
epsilon_values = [0.1, 0.25, 0.5, 0.7, 1, 1.5, 2, 3, 5, 7]
pieces = range(1,11)

def evaluate_test_case(pc_cons_fx, epsilon, algorithm):
    """
    Compare candidate algorithm vs OPT optimal algorithm on one test case.
    Returns: (failed: bool, reason: str, apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces)
    """

    apx_fx, alg_pieces, _ = algorithm(pc_cons_fx, epsilon)
    optimal_pc_fx, optimal_num_pieces, given_num_pieces = approximate_pc_shortest_path(pc_cons_fx, epsilon)

    # Test 1: tolerance (L_infinity) must hold
    if not is_within_epsilon(pc_cons_fx, apx_fx, epsilon):
        return True, "epsilon_bound", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces

    # Test 2: if within tolerance, candidate must be optimal in piece count
    if alg_pieces > optimal_num_pieces:
        return True, "num_pieces", apx_fx, alg_pieces, optimal_pc_fx, optimal_num_pieces, given_num_pieces

    # PASS
    return False, "", apx_fx, alg_pieces, optimal_num_pieces, optimal_num_pieces, given_num_pieces

def count_total_cases(x_values, y_values, epsilon_values, max_pieces):
    """
    Count total number of piecewise-constant test cases analytically.

    Args:
        x_values (int): number of discrete x-positions
        y_values (int): number of discrete y-values
        epsilon_values (int): number of epsilon values
        max_pieces (int): maximum number of pieces to consider

    Returns:
        total (int): total number of test cases
    """
    total = 0
    for m in range(1, max_pieces + 1):
        # number of ways to pick m breakpoints + 1 boundary from x_values
        ways_x = math.comb(x_values, m + 1)
        # number of ways to assign y-values to m pieces
        ways_y = y_values ** m
        # total for this m
        count_m = ways_x * ways_y * epsilon_values
        total += count_m
    return total

def test_algorithm(algorithm):
    """
    Enumerate PC test cases over bounded grids and search for a counterexample.
    Returns first failing (points, epsilon) or None if none found.
    """
    count = 0
    total_test_cases = count_total_cases(len(x_values),len(y_values), len(epsilon_values), len(pieces))
    precomputed_x_combinations = {
        num_pieces: list(itertools.combinations(range(len(x_values) - 1), num_pieces))
        for num_pieces in pieces
    }
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

                        failed, test_name, apx_fx, alg_pieces, optimal_pc_fx, optimal_pieces, given_num_pieces = evaluate_test_case(
                            points, epsilon, algorithm)

                        if failed:
                            if progress_bar:
                                progress_bar.close()
                            print(f"\nFound counterexample after testing {count} cases!")
                            print(f"Reason: {test_name}")
                            print(f"Testcase function: {points}")
                            print(f"Epsilon: {epsilon}")
                            print(f"Given #pieces: {given_num_pieces}")
                            print(f"Approximated function: {apx_fx}")
                            print(f"Candidate #pieces: {alg_pieces}")
                            print(f"Optimal function: {optimal_pc_fx}")
                            print(f"Optimal #pieces: {optimal_pieces}")
                            return points, epsilon

    if progress_bar:
        progress_bar.close()
    print(f"\nNo counterexample found after testing {count} cases!")
    return None
