import sys
import multiprocessing
import os

# Add parent directory to path to import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from optimal_algorithms.pc_linear_apx import approximate_pc_linear_fx
from cpu_parallel import test_algorithm_parallel

# This guard is essential for Windows multiprocessing
if __name__ == "__main__":
    # Set the start method to 'spawn' for Windows compatibility
    multiprocessing.set_start_method('spawn', force=True)

    # Test our algorithm against the optimal Imai-Iri algorithm
    test_algorithm_parallel(approximate_pc_linear_fx)
