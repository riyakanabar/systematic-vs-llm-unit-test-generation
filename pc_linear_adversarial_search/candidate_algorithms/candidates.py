import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .candidate_algos_1 import (
    improved_greedy_with_lookahead as candidate1,
    douglas_peucker_approximation as candidate2,
)
from .candidate_algos_2 import (
piecewise_linear_apx_furthest_scan as candidate3,
piecewise_linear_apx_beam_search as candidate4,
piecewise_linear_apx_visvalingam as candidate5,
piecewise_linear_apx_bottom_up_merge as candidate6,
)
from .modified_imai_iri import modified_imai_iri as candidate7


candidate_algorithms = [candidate1, candidate2, candidate3, candidate4, candidate5, candidate6,
                         candidate7]