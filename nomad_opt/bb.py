#!/usr/bin/env python3
import sys
import operator
import os
import functools
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from grid_search.get_variants import variant_function, loop_variations
from grid_search.variants_test import is_within_epsilon, run_baseline_algorithm
from test_cases import test_cases

def evaluate_variant(params_file):
    # Read parameters from file
    with open(params_file, 'r') as f:
        params = [float(x) for x in f.read().split()]
   
    # Extract traversal strategy index (0-2)
    traversal_idx = min(2, max(0, int(round(params[0]))))
    loop_behavior = loop_variations[traversal_idx]
   
    # Convert parameters to your algorithm format
    a_min, b_min, c_min, d_min = int(round(params[1])), int(round(params[2])), int(round(params[3])), int(round(params[4]))
    alpha_min = -1 if params[5] < 0 else 1
   
    a_max, b_max, c_max, d_max = int(round(params[6])), int(round(params[7])), int(round(params[8])), int(round(params[9]))
    alpha_max = -1 if params[10] < 0 else 1
   
    # Convert operator indices
    op_idx1, op_idx2, op_idx3 = int(round(params[11])), int(round(params[12])), int(round(params[13]))
    operators = [operator.ge, operator.le]
    op1 = operators[min(op_idx1, 1)]
    op2 = operators[min(op_idx2, 1)]
    op3 = operators[min(op_idx3, 1)]
   
    # Create parameter sets
    params_min = (a_min, b_min, c_min, d_min, alpha_min)
    params_max = (a_max, b_max, c_max, d_max, alpha_max)
    condition_params = (op1, op2, op3)
   
    # Create variant
    variant_func = functools.partial(
        variant_function,
        loop_behavior=loop_behavior,
        params_min=params_min,
        params_max=params_max,
        condition_params=condition_params
    )
   
    # Test variant
    score = 0
    for pc_cons_fx, epsilon in test_cases:
        try:
            # Run variant
            opt_fx, opt_num_pieces, given_num_pieces = variant_func(pc_cons_fx, epsilon)
           
            # Test 1: Piece Count Validity
            if given_num_pieces < opt_num_pieces:
                continue  # FAIL
           
            # Test 2: Epsilon Difference
            if not is_within_epsilon(pc_cons_fx, opt_fx, epsilon):
                continue  # FAIL
           
            # Test 3: Simpler Approximation
            baseline_pieces = run_baseline_algorithm(pc_cons_fx, epsilon)
            if opt_num_pieces <= baseline_pieces:
                score += 1
        except Exception as e:
            continue
   
    # Return negative score (since NOMAD minimizes)
    print(-score)
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bb.py params_file")
        sys.exit(1)
    evaluate_variant(sys.argv[1])
