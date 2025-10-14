import sys
import os

# Add parent directory to path to import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from candidate_algorithms.candidate_algos_1 import (
    greedy_approximation as candidate1,
    improved_greedy_with_lookahead as candidate2,
    douglas_peucker_approximation as candidate3,
)
from candidate_algorithms.candidate_algos_2 import (
    shortest_path_dp as candidate4,
    piecewise_linear_apx_furthest_scan as candidate5,
    piecewise_linear_apx_bottom_up_merge as candidate6,
    piecewise_linear_apx_visvalingam as candidate7,
    piecewise_linear_apx_beam_search as candidate8
)
from candidate_algorithms.modified_imai_iri import modified_imai_iri as candidate9
from cpu_parallel import test_algorithm_parallel
# from numba_jit_parallel import numba_test_algorithm_parallel
from candidate_algorithms.numba_algorithms import greedy_approximation_numba
from numba_cuda import test_algorithm

if __name__ == "__main__":
    # test_algorithm_parallel(candidate1) #Run this to get the first failure count
    test_algorithm() #run the cuda version
    # Given
    # cases_per_second = 250000 #41_542_118
    # total_cases = 34_867_814_400
    #
    # # Calculate time in seconds
    # time_seconds = total_cases / cases_per_second
    #
    # # Convert to hours, minutes, seconds
    # hours = int(time_seconds // 3600)
    # minutes = int((time_seconds % 3600) // 60)
    # seconds = time_seconds % 60
    #
    # print(f"Time taken: {hours}h {minutes}m {seconds:.2f}s")

