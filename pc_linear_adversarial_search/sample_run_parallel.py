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
from candidate_algorithms.candidate_algos_2 import (
    shortest_path_dp as candidate5,
    greedy_farthest_L2 as candidate6,
    greedy_farthest_Linf as candidate7,
    top_down_split_L2 as candidate8,
    top_down_split_Linf as candidate9,
    botton_up_merge as candidate10,
    fixed_knot_LP as candidate11
)
from candidate_algorithms.modified_imai_iri import modified_imai_iri as candidate12
from candidate_algorithms.free_knot_LP import free_knot_LP as candidate13
from cpu_parallel import test_algorithm_parallel

if __name__ == "__main__":
    # Set the start method to 'spawn' for Windows compatibility
    multiprocessing.set_start_method('spawn', force=True)

    test_algorithm_parallel(candidate12)
