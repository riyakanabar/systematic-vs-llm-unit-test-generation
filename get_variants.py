import inspect
from utils import middle_to_end_alternating_traversal, middle_divide_conquer_traversal
from itertools import product

a_values = range(1, 4)
b_values = range(1, 4)
c_values = range(1, 4)
d_values = range(1, 4)
alpha_values = [-0.5, 0.5, 1.0]  # Coefficient for the abs term
scaling_factors = [0.75, 1.0,1.5]  # Scaling factors

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


def normalize_parameters(params):
    """Normalize parameters to eliminate duplicates by scaling appropriately"""
    a, b, c, d, alpha, scale = params
    # Normalize all parameters
    a_norm = a * scale
    b_norm = b * scale
    c_norm = c * alpha * scale
    d_norm = d * alpha * scale
    return (a_norm, b_norm, c_norm, d_norm)

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
        # Original parameters for display/debugging
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
                    # Use normalized parameters with simplified functions
                    new_U_min = min_function(U_min, U[k - 1],
                                                        a_min, b_min, c_min, d_min,alpha_min, scale_min)
                    new_L_max = max_function(L_max, L[k - 1],
                                                        a_max, b_max, c_max, d_max, alpha_max, scale_max)

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
        # Store original parameters for debugging/analysis
        variant.a_min, variant.b_min = a_min, b_min
        variant.c_min, variant.d_min = c_min, d_min
        variant.alpha_min = alpha_min
        variant.scale_min = scale_min
        variant.a_max, variant.b_max = a_max, b_max
        variant.c_max, variant.d_max = c_max, d_max
        variant.alpha_max = alpha_max
        variant.scale_max = scale_max
        return variant

    # Track unique normalized parameter sets
    unique_param_variants = {}

    # First pass: identify unique parameter sets after normalization
    for params in param_combinations:
        # Normalize parameters
        norm_params = normalize_parameters(params)
        param_key = tuple(round(x, 2) for x in norm_params)

        # Store original params with their normalized version
        if param_key not in unique_param_variants:
            unique_param_variants[param_key] = params

    unique_params_list = list(unique_param_variants.values())
    total_count = len(loop_variations)*len(param_combinations)*len(param_combinations)
    unique_count = len(loop_variations)*len(unique_params_list) * len(unique_params_list)
    print(f"Original number of variants: {total_count}")
    print(f"Unique variants after normalization: {unique_count}")
    print(
        f"Eliminated {total_count - unique_count} duplicates ({(total_count - unique_count) / total_count * 100:.2f}%)")

    # Second pass: generate algorithms using all combinations of unique parameter sets
    for loop_behavior in loop_variations:
        for params_min in unique_params_list:
            for params_max in unique_params_list:
                algorithms.append(create_variant(loop_behavior, params_min, params_max))

    return algorithms
