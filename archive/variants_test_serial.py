from get_variants_serial import get_variation_algorithms, print_algorithm_code
from optimal_algorithms.pc_cons_apx import approximate_pc_cons_fx
from test_cases import test_cases
import unittest
import numpy as np

def is_within_epsilon(pc_cons_fx, optimal_pc_fx, epsilon):

    optimal_pc_fx_sorted = sorted(optimal_pc_fx, key=lambda x: x[0])
    if not optimal_pc_fx_sorted:
        return False

    for i in range(1, len(pc_cons_fx)-1):
        y = pc_cons_fx[i][1]
        y_opt = optimal_pc_fx_sorted[i-1][1]

        if not np.isclose(y, y_opt, atol=epsilon, rtol=1e-9):
            return False

    return True

def run_test_case(algorithm, pc_cons_fx, epsilon):
    _, optimal_num_pieces, _ = algorithm(pc_cons_fx, epsilon)
    return optimal_num_pieces

class AlgorithmFunctionalityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up algorithms...")
        cls.algorithms = get_variation_algorithms()
        print(f"Generated {len(cls.algorithms)} algorithm variants.")
        cls.original_algorithm = staticmethod(approximate_pc_cons_fx)
        print("Setting up tests...")
        cls.test_cases = test_cases
        cls.valid_variants = list(range(0, len(cls.algorithms)))  # Start with all variants as valid (excluding original)

    def test_01_number_of_pieces(self):
        """
        Ensures that the optimal number of pieces is less than or equal to the given pieces.
        Removes invalid variants if the condition fails.
        """
        print("Running test_number_of_pieces...")
        new_valid_variants = []
        for i in self.valid_variants:
            algorithm = self.algorithms[i]
            is_valid = True
            for pc_cons_fx, epsilon in self.test_cases:
                _, optimal_num_pieces, given_num_pieces = algorithm(pc_cons_fx, epsilon)
                if given_num_pieces < optimal_num_pieces:
                    is_valid = False
                    break  # Stop further testing this variant

            if is_valid:
                new_valid_variants.append(i)
        self.__class__.valid_variants = new_valid_variants  # Persist changes across tests

    def test_02_epsilon_difference(self):
        """
        Validates that the epsilon difference is maintained between old and new function values.
        Removes invalid variants if the condition fails.
        """
        print("Running test_epsilon_difference...")
        new_valid_variants = []
        for i in self.valid_variants:
            algorithm = self.algorithms[i]
            is_valid = True
            for pc_cons_fx, epsilon in self.test_cases:
                optimal_pc_fx, _, _ = algorithm(pc_cons_fx, epsilon)

                if not is_within_epsilon(pc_cons_fx, optimal_pc_fx, epsilon):
                    is_valid = False
                    break

            if is_valid:
                new_valid_variants.append(i)
        self.__class__.valid_variants = new_valid_variants

    def test_03_simpler_approximation(self):
        """
        Evaluates whether valid variants provide a simpler approximation compared to the original algorithm.
        Only variants that pass functionality tests are considered for this test
        """
        print("Running test_simpler_approximation tests...")

        threshold = 13
        successful_variants = []
        variant_scores = [0] * len(self.valid_variants)

        for pc_cons_fx, epsilon in self.test_cases:
            optimal_pieces = run_test_case(self.original_algorithm, pc_cons_fx, epsilon)

            for i, variant_index in enumerate(self.valid_variants):
                variant_algorithm = self.algorithms[variant_index]
                variant_pieces = run_test_case(variant_algorithm, pc_cons_fx, epsilon)
                if variant_pieces <= optimal_pieces:
                    variant_scores[i] += 1

        for i, score in enumerate(variant_scores):
            if score >= threshold:
                successful_variants.append((self.valid_variants[i], score))


        print(f"{len(successful_variants)} Variants passed functionality tests:")
        for index, score in successful_variants:
            print(f"Variant {index}: Passed {score} test cases.")
            print_algorithm_code(self.algorithms[index])


        self.assertGreaterEqual(len(successful_variants), 1, "No variants passed the simpler_approximation tests!")


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(AlgorithmFunctionalityTests)
    )