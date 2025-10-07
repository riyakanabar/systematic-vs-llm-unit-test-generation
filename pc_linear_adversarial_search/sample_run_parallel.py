import sys
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
    greedy_farthest as candidate6,
    top_down_split as candidate7,
    botton_up_merge as candidate8,
)
from candidate_algorithms.modified_imai_iri import modified_imai_iri as candidate9
from cpu_parallel import test_algorithm_parallel
from numba_jit_parallel import numba_test_algorithm_parallel
from candidate_algorithms.numba_algorithms import greedy_approximation_numba

if __name__ == "__main__":
    numba_test_algorithm_parallel(greedy_approximation_numba)
