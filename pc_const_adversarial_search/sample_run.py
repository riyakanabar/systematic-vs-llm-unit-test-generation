import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from numba_candidate_algorithms import numba_recursive_split1
from input_algorithms import beam_search, recursive_split1, pruned_dp
from numba_jit_parallel import test_algorithm

if __name__ == "__main__":
    test_algorithm(numba_recursive_split1)

