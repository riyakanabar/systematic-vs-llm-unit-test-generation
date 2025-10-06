import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from testcase_gen_gs import test_algorithm
from candidate_algorithms.modified_imai_iri import modified_imai_iri as candidate9


if __name__ == "__main__":
    test_algorithm(candidate9)

