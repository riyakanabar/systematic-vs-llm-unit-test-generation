import sys
import multiprocessing
import os

# Add parent directory to path to import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from candidate_algorithms.candidate_algos_1 import (
    greedy_approximation as candidate1,
    improved_greedy_with_lookahead as candidate2,
    branch_and_bound as candidate3,
    douglas_peucker_approximation as candidate4,
)
from cpu_parallel import test_algorithm_parallel

if __name__ == "__main__":
    # Set the start method to 'spawn' for Windows compatibility
    #844881
    multiprocessing.set_start_method('spawn', force=True)

    test_algorithm_parallel(candidate1)
