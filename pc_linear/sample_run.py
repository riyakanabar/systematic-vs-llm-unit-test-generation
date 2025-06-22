from optimal_algorithms.pc_linear_apx import approximate_pc_linear_fx, plot_piecewise_linear_approximation
from test_cases import test_cases

pc_linear_fx = test_cases[11][0]
epsilon = test_cases[11][1]

optimal_pc_linear_fx, optimal_num_pieces, given_num_pieces = approximate_pc_linear_fx(pc_linear_fx, epsilon)
print(pc_linear_fx)
print(optimal_pc_linear_fx)
print(optimal_num_pieces)
print(given_num_pieces)
plot_piecewise_linear_approximation(pc_linear_fx, optimal_pc_linear_fx, epsilon)