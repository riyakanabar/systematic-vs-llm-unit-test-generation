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
    greedy_farthest_L2 as candidate6,
    greedy_farthest_Linf as candidate7,
    top_down_split_L2 as candidate8,
    top_down_split_Linf as candidate9,
    botton_up_merge as candidate10,
    fixed_knot_LP as candidate11
)
from .modified_imai_iri import modified_imai_iri as candidate12
from .free_knot_LP import free_knot_LP as candidate13


candidate_algorithms = [candidate1, candidate2, candidate3, candidate4, candidate5,
                        candidate6, candidate7, candidate8, candidate9, candidate10,
                        candidate11, candidate12, candidate13]