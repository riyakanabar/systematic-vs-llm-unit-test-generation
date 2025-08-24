import numpy as np
from itertools import combinations, product
from optimal_algorithm import MATLABOptimalAlgorithm
N_values = range(1,6)  # 1 to 5 pieces
a_values = [x for x in range(-5, 5) if x != 0]  # -5 to 5, excluding 0
b_values = list(range(-5, 5))  # -5 to 5
c_values = list(range(-5, 5))  # -5 to 5
breakpoint_values = [-np.inf, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, np.inf]  # -5 to 5
epsilon_values = [0.1, 0.25, 0.5, 0.7, 1, 1.5, 2, 3, 5, 7]


def test_algorithm(algorithm):
    optimal_algorithm = MATLABOptimalAlgorithm()
    count = 0
    for N in N_values:
        for epsilon in epsilon_values:
            for breakpoints in combinations(breakpoint_values, N + 1):
                for coeffs in product(a_values, b_values, c_values, repeat=N):
                    # Create f matrix (3xN)
                    f = np.array([coeffs[i::3] for i in range(3)])

                    count += 1
                    # print(f"Testcase#",count)
                    # print(f"Input N: {N}, Input function f: {f}")
                    # print(f"Input breakpoints: {breakpoints}")
                    # print(f"epsilon: {epsilon}")

                    apx_fx, alg_breakpoints, alg_num_pieces = algorithm(f, list(breakpoints),epsilon)
                    optimal_fx, optimal_breakpoints, optimal_num_pieces = optimal_algorithm(f, list(breakpoints),epsilon)
                    # Check if number of pieces exceeds N
                    if alg_num_pieces > optimal_num_pieces:
                        print(f"\nFound counterexample after testing {count} cases!")
                        print("\nTest Failed! Number of pieces > Optimal pieces")
                        print(f"Input N: {N}, Input function f: {f}")
                        print(f"Input breakpoints: {breakpoints}")
                        print(f"epsilon: {epsilon}")
                        print(f"Approximated function: {apx_fx}")
                        print(f"Algorithm pieces: {alg_num_pieces}")
                        print(f"Algorithm breakpoints: {alg_breakpoints}")
                        print(f"Optimal function: {optimal_fx}")
                        print(f"Optimal breakpoints: {optimal_breakpoints}")
                        print(f"Optimal pieces: {optimal_num_pieces}")
                        return



        print(f"All test cases passed for N = {N}")

    print(f"\nAll {count} test cases passed successfully!")
    return None