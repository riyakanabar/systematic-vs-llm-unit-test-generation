import operator
import functools
import itertools

# Parameter Ranges
a_values = range(1, 11)
b_values = range(1, 11)
c_values = range(1, 11)
d_values = range(1, 11)
alpha_values = [-1, 1]

# Condition Operators
condition_ops = [operator.ge, operator.le]

# Traversal Strategies
def left_to_right(pc_fx):
    return pc_fx[1:-1]

def lowest_to_highest(pc_fx):
    return sorted(pc_fx[1:-1], key=lambda x: x[1])

def highest_to_lowest(pc_fx):
    return sorted(pc_fx[1:-1], key=lambda x: x[1], reverse=True)

loop_variations = [left_to_right, lowest_to_highest, highest_to_lowest]

# Linear-absolute function
def m(x, y, v):
    a, b, c, d, alpha = v
    return (a * x + b * y + alpha * abs(c * x - d * y)) / 2

# Condition wrapper
def cond(a, b, op):
    return op(a, b)

# Variant core function
def variant_function(pc_fx, epsilon, loop_behavior, params_min, params_max, condition_params):
    optimal_pc_fx = []
    pc_fx_traversal_order = list(loop_behavior(pc_fx))
    n = len(pc_fx_traversal_order)
    U = [pc_fx_traversal_order[i][1] + epsilon for i in range(n)]
    L = [pc_fx_traversal_order[i][1] - epsilon for i in range(n)]
    op1, op2, op3 = condition_params

    i = 0
    optimal_num_pieces = 0
    while i < n:
        U_min, L_max = U[i], L[i]
        k = i + 1
        segment_x_values = []
        progress = False
        while k <= n:
            new_U_min = m(U_min, U[k - 1], params_min)
            new_L_max = m(L_max, L[k - 1], params_max)

            if (cond(new_U_min, new_L_max, op1) and
                cond(U[i], new_L_max, op2) and
                cond(L[i], new_U_min, op3)):
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
            i = k - 1

    optimal_pc_fx.append([pc_fx[-1][0], float('inf')])
    given_num_pieces = len(pc_fx) - 2
    return optimal_pc_fx, optimal_num_pieces, given_num_pieces

# Generate all variant configurations
def generate_variant_configs():
    for loop_behavior in loop_variations:
        for params_min in itertools.product(a_values, b_values, c_values, d_values, alpha_values):
            for params_max in itertools.product(a_values, b_values, c_values, d_values, alpha_values):
                for condition_params in itertools.product(condition_ops, repeat=3):
                    yield (loop_behavior, params_min, params_max, condition_params)

# Create variant wrapper
def create_variant_wrapper(args):
    loop_behavior, params_min, params_max, condition_params = args
    variant_func = functools.partial(
        variant_function,
        loop_behavior=loop_behavior,
        params_min=params_min,
        params_max=params_max,
        condition_params=condition_params
    )
    # Map operator functions to readable strings
    op_str_map = {
        operator.ge: '>=',
        operator.le: '<='
    }
    condition_ops_str = tuple(op_str_map[op] for op in condition_params)

    meta_info = {
        "loop_behavior": loop_behavior.__name__,
        "params_min": params_min,
        "params_max": params_max,
        "condition_params": condition_ops_str  # human-readable
    }

    return variant_func, meta_info