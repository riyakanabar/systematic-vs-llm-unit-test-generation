import numpy as np
import inspect
from utils import middle_to_end_alternating_traversal, middle_divide_conquer_traversal
from itertools import product

a_values = range(1, 4)  # [1, 2, ..., 10]
b_values = range(1, 4)
c_values = range(1, 4)  # New coefficient for x inside abs
d_values = range(1, 4)  # New coefficient for y inside abs
alpha_values = [0.5, 1.0, 1.5] # Coefficient for the abs term
scaling_factors = [0.3, 0.5, 0.7] #[i / 10 for i in range(1, 11)]  [0.1, 0.2, ..., 1]


def min_function(x, y, a, b, c, d, alpha, scaling_factor):
    return scaling_factor * (a * x + b * y - alpha * abs(c * x - d * y))


def max_function(x, y, a, b, c, d, alpha, scaling_factor):
    return scaling_factor * (a * x + b * y + alpha * abs(c * x - d * y))


def print_algorithm_code(algorithm):
    try:
        source_code = inspect.getsource(algorithm)
        # print(f"Algorithm Code for that variant is:")
        # print(source_code)
        loop_behaviour_code = inspect.getsource(algorithm.loop_behavior)
        print(f"Traversal variant used: {loop_behaviour_code}")
        print(
            f"a_min = {algorithm.a_min}, b_min = {algorithm.b_min}, c_min = {algorithm.c_min}, d_min = {algorithm.d_min}, alpha_min = {algorithm.alpha_min}, scale_min = {algorithm.scale_min}")
        print(
            f"a_max = {algorithm.a_max}, b_max = {algorithm.b_max}, c_max = {algorithm.c_max}, d_max = {algorithm.d_max}, alpha_max = {algorithm.alpha_max}, scale_max = {algorithm.scale_max}")

    except Exception as e:
        print(f"Error retrieving source code: {e}")


def get_variation_algorithms():
    algorithms = []

    loop_variations = [
        lambda pc_fx: pc_fx[1:-1],  # left to right
        lambda pc_fx: reversed(pc_fx[1:-1]),  # right to left
        lambda pc_fx: sorted(pc_fx[1:-1], key=lambda x: x[1]),  # Lowest function value to highest
        lambda pc_fx: sorted(pc_fx[1:-1], key=lambda x: x[1], reverse=True),  # Highest function value to lowest
        lambda pc_fx: middle_to_end_alternating_traversal(pc_fx[1:-1]),  # middle to left and right
        lambda pc_fx: middle_divide_conquer_traversal(pc_fx[1:-1])  # middle-Divide-and-Conquer
    ]

    # Generate all combinations of parameters
    param_combinations = list(product(
        a_values, b_values, c_values, d_values,
        alpha_values, scaling_factors
    ))

    def create_variant(loop_behavior, params_min, params_max):
        a_min, b_min, c_min, d_min, alpha_min, scale_min = params_min
        a_max, b_max, c_max, d_max, alpha_max, scale_max = params_max

        def variant(pc_fx, epsilon):
            optimal_pc_fx = []
            pc_fx_traversal_order = list(loop_behavior(pc_fx))
            n = len(pc_fx_traversal_order)
            # Compute upper and lower bounds
            U = [pc_fx_traversal_order[i][1] + epsilon for i in range(n)]
            L = [pc_fx_traversal_order[i][1] - epsilon for i in range(n)]

            i = 0
            optimal_num_pieces = 0
            while i < n:
                U_min, L_max = U[i], L[i]
                k = i + 1  # next segment
                segment_x_values = []

                # Find the furthest reachable segment satisfying conditions
                progress = False  # Track if `k` increases
                while k <= n:
                    new_U_min = min_function(U_min, U[k - 1],
                                             a_min, b_min, c_min, d_min,
                                             alpha_min, scale_min)
                    new_L_max = max_function(L_max, L[k - 1],
                                             a_max, b_max, c_max, d_max,
                                             alpha_max, scale_max)

                    if new_U_min >= new_L_max and U[i] >= new_L_max and L[i] <= new_U_min:
                        U_min = new_U_min
                        L_max = new_L_max
                        segment_x_values.append(pc_fx_traversal_order[k - 1][0])
                        k += 1
                        progress = True
                    else:
                        break
                segment_value = (U_min + L_max) / 2
                if segment_x_values:
                    optimal_num_pieces += 1
                for x_val in segment_x_values:
                    optimal_pc_fx.append([x_val, segment_value])
                if not progress:
                    i += 1
                else:
                    i = k - 1  # Move to next segment

            optimal_pc_fx.append([pc_fx[-1][0], float('inf')])  # Append last boundary
            given_num_pieces = len(pc_fx) - 2
            return optimal_pc_fx, optimal_num_pieces, given_num_pieces

        variant.loop_behavior = loop_behavior
        # Store all parameters for debugging/analysis
        variant.a_min, variant.b_min = a_min, b_min
        variant.c_min, variant.d_min = c_min, d_min
        variant.alpha_min = alpha_min
        variant.scale_min = scale_min
        variant.a_max, variant.b_max = a_max, b_max
        variant.c_max, variant.d_max = c_max, d_max
        variant.alpha_max = alpha_max
        variant.scale_max = scale_max
        return variant

    for loop_behavior in loop_variations:
        for params_min in param_combinations:
            for params_max in param_combinations:
                algorithms.append(create_variant(loop_behavior, params_min, params_max))
    return algorithms
