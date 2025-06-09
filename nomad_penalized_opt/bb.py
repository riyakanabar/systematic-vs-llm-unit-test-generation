#!/usr/bin/env python3
import sys
import operator
import os
import functools
import numpy as np

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from grid_search.get_variants import variant_function, loop_variations
from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
from test_cases import test_cases

# Create a log file for valid variants
valid_variants_log = os.path.join(os.path.dirname(__file__), "valid_variants.txt")
if not os.path.exists(valid_variants_log) or os.path.getsize(valid_variants_log) == 0:
	with open(valid_variants_log, 'w') as f:
		f.write("# Parameters and scores for valid variants (obj < 1000)\n")
		f.write("# Format: traversal a_min b_min c_min d_min alpha_min a_max b_max c_max d_max alpha_max op1 op2 op3 score\n\n")

def evaluate_variant(params_file, lambda_value=0.5):
    """
    Evaluate a variant using the penalized objective function:
    min_θ ∑[i=1 to m] [(N_i(θ) - N_i*) + λ·||A_θ(f_i) - f_i||_∞]
    """
    # Read parameters from file
    with open(params_file, 'r') as f:
        params = [float(x) for x in f.read().split()]
   
    # Extract traversal strategy index (0-2)
    traversal_idx = min(2, max(0, int(round(params[0]))))
    loop_behavior = loop_variations[traversal_idx]
   
    # Convert parameters to algorithm format
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
   
    # Calculate the penalized objective
    total_penalty = 0
    valid_test_cases = 0
    
    for pc_cons_fx, epsilon in test_cases:
        try:
            # Run variant
            opt_fx, opt_num_pieces, given_num_pieces = variant_func(pc_cons_fx, epsilon)
            
            # Run baseline algorithm to get N_i*
            _, baseline_pieces, _ = approximate_pc_shortest_path(pc_cons_fx, epsilon)
            
            # Calculate piece count difference (N_i(θ) - N_i*)
            piece_count_diff = max(0, opt_num_pieces - baseline_pieces)
            
            # Calculate approximation error ||A_θ(f_i) - f_i||_∞
            max_error = 0
            opt_fx_sorted = sorted(opt_fx,key=lambda x: x[0])
            for i in range(1, len(pc_cons_fx) - 1):
                y_true = pc_cons_fx[i][1]
                y_approx = opt_fx_sorted[i-1][1]
                error = abs(y_true - y_approx)
                max_error = max(max_error, error)
            
            # Ensure error is within epsilon (otherwise, solution is invalid)
            if np.isclose(y_true,y_approx,atol=epsilon,rtol=1e-9):
                # Add to total penalty using the penalized formulation
                case_penalty = piece_count_diff + lambda_value * max_error
                total_penalty += case_penalty
                valid_test_cases += 1
            else:
                # Invalid solution for this test case
                total_penalty += 1000  # Large penalty
            
        except Exception as e:
            # Add a large penalty for failed cases
            total_penalty += 1000
    
    # If no valid test cases, return a very large penalty
    if valid_test_cases == 0:
        total_penalty = 1e6
        
    if total_penalty < 1000:  # No large penalties
	    with open(valid_variants_log, 'a') as f:
		    params_str = ' '.join(map(str, params))
		    f.write(f"{params_str} {total_penalty}\n")
    
    # Return the objective (NOMAD minimizes)
    print(total_penalty)
    return 0
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bb.py params_file")
        sys.exit(1)
    evaluate_variant(sys.argv[1])
