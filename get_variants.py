import inspect
import multiprocessing

a_values = range(1, 2)
b_values = range(1, 2)
c_values = range(1, 2)
d_values = range(1, 2)
alpha_values = [-1, 1]  # Coefficient for the absolute term

# Define traversal strategies as named functions instead of lambdas for pickling
def left_to_right(pc_fx):
    return pc_fx[1:-1]
def lowest_to_highest(pc_fx):
    return sorted(pc_fx[1:-1], key=lambda x: x[1])
def highest_to_lowest(pc_fx):
    return sorted(pc_fx[1:-1], key=lambda x: x[1], reverse=True)

loop_variations = [
    left_to_right,
    lowest_to_highest,
    highest_to_lowest
]

def m(x, y, v):
    """Linear-absolute function: m(x, y, v) = (v[0]*x + v[1]*y + v[4]*|v[2]*x - v[3]*y|) / 2 """
    a, b, c, d, alpha = v
    return (a * x + b * y + alpha * abs(c * x - d * y)) / 2


def print_algorithm_code(algorithm):
    try:
        loop_name = algorithm.loop_behavior.__name__
        print(f"Traversal variant used: {loop_name}")
        print(
            f"a_min = {algorithm.a_min}, b_min = {algorithm.b_min}, c_min = {algorithm.c_min}, d_min = {algorithm.d_min}, alpha_min = {algorithm.alpha_min}")
        print(
            f"a_max = {algorithm.a_max}, b_max = {algorithm.b_max}, c_max = {algorithm.c_max}, d_max = {algorithm.d_max}, alpha_max = {algorithm.alpha_max}")
    except Exception as e:
        print(f"Error retrieving source code: {e}")


def create_variant_wrapper(args):
    """Wrapper function for multiprocessing"""
    loop_behavior, params_min, params_max = args
    return create_variant(loop_behavior, params_min, params_max)


def get_variation_algorithms():
    # Calculate the number of parameter combinations
    param_combinations_count = len(a_values) * len(b_values) * len(c_values) * len(d_values) * len(alpha_values)
    total_count = len(loop_variations) * param_combinations_count * param_combinations_count

    print(f"Generating {total_count} algorithm variants in parallel...")

    # Create all parameter combinations to process in parallel
    tasks = []
    for loop_behavior in loop_variations:
        for a_min in a_values:
            for b_min in b_values:
                for c_min in c_values:
                    for d_min in d_values:
                        for alpha_min in alpha_values:
                            params_min = (a_min, b_min, c_min, d_min, alpha_min)
                            for a_max in a_values:
                                for b_max in b_values:
                                    for c_max in c_values:
                                        for d_max in d_values:
                                            for alpha_max in alpha_values:
                                                params_max = (a_max, b_max, c_max, d_max, alpha_max)
                                                tasks.append((loop_behavior, params_min, params_max))

    # Use multiprocessing to generate variants in parallel
    # Determine the number of processes to use (leave one core free for system)
    num_processes = max(1, multiprocessing.cpu_count() - 1)
    print(f"Using {num_processes} CPU cores")

    # Create a pool of workers and distribute the tasks
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Use imap with chunking for better memory efficiency
        chunk_size = max(1, len(tasks) // (num_processes * 10))  # Adjust chunk size based on task count
        algorithms = list(pool.imap(create_variant_wrapper, tasks, chunk_size))

    return algorithms


def variant_function(pc_fx, epsilon, loop_behavior, params_min, params_max):
    """The algorithm implementation, separated from create_variant for pickling"""

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
            new_U_min = m(U_min, U[k - 1], params_min)
            new_L_max = m(L_max, L[k - 1], params_max)

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


class VariantAlgorithm:
    def __init__(self, loop_behavior, params_min, params_max):
        self.loop_behavior = loop_behavior
        # Store original parameters for debugging/analysis
        self.a_min, self.b_min = params_min[0], params_min[1]
        self.c_min, self.d_min = params_min[2], params_min[3]
        self.alpha_min = params_min[4]
        self.a_max, self.b_max = params_max[0], params_max[1]
        self.c_max, self.d_max = params_max[2], params_max[3]
        self.alpha_max = params_max[4]

    def __call__(self, pc_fx, epsilon):
        return variant_function(pc_fx, epsilon, self.loop_behavior,
                                (self.a_min, self.b_min, self.c_min, self.d_min, self.alpha_min),
                                (self.a_max, self.b_max, self.c_max, self.d_max, self.alpha_max))


def create_variant(loop_behavior, params_min, params_max):
    """Create a variant algorithm with the given parameters"""
    return VariantAlgorithm(loop_behavior, params_min, params_max)
