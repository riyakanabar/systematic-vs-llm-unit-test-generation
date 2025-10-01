from optimal_algorithms.pc_linear_apx import plot_piecewise_linear_approximation, approximate_pc_linear_fx
from test_cases import test_cases
from pc_linear_adversarial_search.cpu_parallel import is_within_epsilon
from pc_linear_adversarial_search.candidate_algorithms.free_knot_LP import free_knot_LP

pc_linear_fx = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]#18,19 good ones to test
epsilon = 0.0

optimal_pc_linear_fx, optimal_num_pieces, given_num_pieces = approximate_pc_linear_fx(pc_linear_fx, epsilon)
print(pc_linear_fx)
print(optimal_pc_linear_fx)
print(optimal_num_pieces)
print(given_num_pieces)
plot_piecewise_linear_approximation(pc_linear_fx, optimal_pc_linear_fx, epsilon)
print(is_within_epsilon(pc_linear_fx,optimal_pc_linear_fx,epsilon))