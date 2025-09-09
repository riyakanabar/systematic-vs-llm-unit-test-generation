import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from input_algorithms import pruned_dp, alg7_beam_search, variant2, variant3, recursive_split1, recursive_split2, lookahead_split, binary_split
from cpu_parallel import test_algorithm_parallel
import multiprocessing
from utils import plot_pc_case

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)
    fx, epsilon, apx_fx, opt_fx = test_algorithm_parallel(alg7_beam_search)
    plot_pc_case(fx, epsilon, apx_fx, opt_fx, "Agglomerative Y-Spread - Optimality Failure")

