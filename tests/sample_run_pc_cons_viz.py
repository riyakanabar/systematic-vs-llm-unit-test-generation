from optimal_algorithms.pc_cons_apx import approximate_pc_cons_fx, plot_pc_cons_fx
from test_cases import test_cases
from pc_const_adversarial_search.llms.iteration2 import test_cases
from pc_const_adversarial_search.input_algorithms import variant1

pc_cons_fx = test_cases[3]["pc_fx"]
epsilon = test_cases[3]["epsilon"]
# pc_cons_fx = test_cases[3][0]
# epsilon = test_cases[3][1]
#optimal_pc_fx, optimal_num_pieces, given_num_pieces = approximate_pc_cons_fx(pc_cons_fx, epsilon)
optimal_pc_fx, optimal_num_pieces, given_num_pieces = variant1(pc_cons_fx, epsilon)

print(f"Given function is {pc_cons_fx}")
print(f"\nGiven number of pieces: {given_num_pieces}")
print(f"epsilon: {epsilon}")
print(f"Optimal function is {optimal_pc_fx}")

print(f"Optimal number of pieces: {optimal_num_pieces}")
plot_pc_cons_fx(pc_cons_fx, optimal_pc_fx)