from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
from iteration2 import test_cases
from grid_search.variants_test import is_within_epsilon
from pc_const_adversarial_search.input_algorithms import candidate_algorithms, algs

for index, alg in enumerate(algs, start=1):
    count = 0
    for idx, tc in enumerate(test_cases):
        pc_fx = tc['pc_fx']
        epsilon = tc['epsilon']

        _, optimal_num_pieces, _ = approximate_pc_shortest_path(pc_fx, epsilon)
        fx, candidate_num_pieces, _ = alg(pc_fx, epsilon)
        if not is_within_epsilon(pc_fx, fx, epsilon):
            print(f"epsilon failure for testcase {idx}")
            print(f"pc_fx: {pc_fx} and epsilon: {epsilon}")
            count += 1
            continue
        if(candidate_num_pieces > optimal_num_pieces):
            print(f"optimality failure for testcase {idx}")
            print(f"pc_fx: {pc_fx} and epsilon: {epsilon}")
            count+=1

    print(f"Algorithm #{index}: Found {count} counterexamples")


