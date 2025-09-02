from input_algorithms import variant1, variant2, variant5, variant3, variant7, pc_center_grid_dp, pc_lookahead_split, pc_quantized_rle, pc_binary_split, pc_naive_greedy
from cpu_parallel import test_algorithm_parallel
import multiprocessing
from optimal_algorithms.pc_cons_apx import  approximate_pc_cons_fx
from utils import plot_pc_case

# This guard is essential for Windows multiprocessing
if __name__ == "__main__":
    # Set the start method to 'spawn' for Windows compatibility
    multiprocessing.set_start_method('spawn', force=True)
    fx, epsilon, apx_fx, opt_fx = test_algorithm_parallel(pc_binary_split)
    plot_pc_case(fx, epsilon, apx_fx, opt_fx, "Algorithm #7 - Optimality Failure")

