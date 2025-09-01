from input_algorithms import variant1, variant2, variant5, variant3, variant7, pc_beam_search, pc_center_grid_dp
from cpu_parallel import test_algorithm_parallel
import multiprocessing
from optimal_algorithms.pc_cons_apx import  approximate_pc_cons_fx

# This guard is essential for Windows multiprocessing
if __name__ == "__main__":
    # Set the start method to 'spawn' for Windows compatibility
    multiprocessing.set_start_method('spawn', force=True)
    test_algorithm_parallel(pc_center_grid_dp)

