from pc_cons_apx import approximate_pc_cons_fx, plot_pc_cons_fx, plot_single_pc_fx, approximate_pc_shortest_path,approximate_pc_reverse_shortest_path,variant
from test_cases import test_cases

#from test_cases import test_cases
pc_cons_fx = test_cases[3][0]
epsilon = test_cases[3][1]
optimal_pc_fx, optimal_num_pieces, given_num_pieces = variant(pc_cons_fx, epsilon)
#optimal_pc_fx, optimal_num_pieces, given_num_pieces = approximate_pc_cons_fx0(pc_cons_fx, epsilon)
print(f"optimal pc is {optimal_pc_fx}")
print(f"\nGiven number of pieces: {given_num_pieces}")
print(f"Optimal number of pieces: {optimal_num_pieces}")
plot_pc_cons_fx(pc_cons_fx, optimal_pc_fx)