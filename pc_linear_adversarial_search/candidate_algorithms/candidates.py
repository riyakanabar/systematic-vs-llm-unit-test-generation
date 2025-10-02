import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .candidate_algos_1 import (
    greedy_approximation as candidate1,
    improved_greedy_with_lookahead as candidate2,
    branch_and_bound as candidate3,
    douglas_peucker_approximation as candidate4,
)
from .candidate_algos_2 import (
    shortest_path_dp as candidate5,
    greedy_farthest as candidate6,
    top_down_split as candidate7,
    botton_up_merge as candidate8,
)
from .modified_imai_iri import modified_imai_iri as candidate9


candidate_algorithms = [candidate1, candidate2, candidate3, candidate4, candidate5,
                        candidate6, candidate7, candidate8, candidate9]