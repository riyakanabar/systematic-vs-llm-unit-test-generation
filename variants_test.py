from get_variants import get_variation_algorithms, print_algorithm_code
from pc_cons_apx import approximate_pc_cons_fx
from test_cases import test_cases
import unittest
import numpy as np
import multiprocessing
from functools import partial
import time


def is_within_epsilon(pc_cons_fx, optimal_pc_fx, epsilon):
    optimal_pc_fx_sorted = sorted(optimal_pc_fx, key=lambda x: x[0])
    if not optimal_pc_fx_sorted:
        return False

    for i in range(1, len(pc_cons_fx) - 1):
        y = pc_cons_fx[i][1]
        y_opt = optimal_pc_fx_sorted[i - 1][1]

        if not np.isclose(y, y_opt, atol=epsilon, rtol=1e-9):
            return False

    return True


def run_test_case(algorithm, pc_cons_fx, epsilon):
    _, optimal_num_pieces, _ = algorithm(pc_cons_fx, epsilon)
    return optimal_num_pieces


# Parallel test functions
def test_variant_number_of_pieces(variant_index, algorithm, test_cases):
    """Test if a variant passes the number_of_pieces test for all test cases"""
    for pc_cons_fx, epsilon in test_cases:
        _, optimal_num_pieces, given_num_pieces = algorithm(pc_cons_fx, epsilon)
        if given_num_pieces < optimal_num_pieces:
            return None  # Variant failed
    return variant_index  # Variant passed


def test_variant_epsilon_difference(variant_index, algorithm, test_cases):
    """Test if a variant passes the epsilon_difference test for all test cases"""
    for pc_cons_fx, epsilon in test_cases:
        optimal_pc_fx, _, _ = algorithm(pc_cons_fx, epsilon)
        if not is_within_epsilon(pc_cons_fx, optimal_pc_fx, epsilon):
            return None  # Variant failed
    return variant_index  # Variant passed


def test_variant_simpler_approximation(args):
    """Test how many test cases a variant passes for simpler_approximation"""
    variant_index, algorithm, test_cases, original_algorithm = args
    score = 0
    for pc_cons_fx, epsilon in test_cases:
        optimal_pieces = run_test_case(original_algorithm, pc_cons_fx, epsilon)
        variant_pieces = run_test_case(algorithm, pc_cons_fx, epsilon)
        if variant_pieces <= optimal_pieces:
            score += 1
    return variant_index, score


class AlgorithmFunctionalityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up test cases and algorithms...")
        cls.algorithms = get_variation_algorithms()
        print(f"Generated {len(cls.algorithms)} algorithm variants.")
        cls.original_algorithm = staticmethod(approximate_pc_cons_fx)
        cls.test_cases = test_cases
        cls.valid_variants = list(range(0, len(cls.algorithms)))  # Start with all variants as valid
        cls.num_processes = max(1, multiprocessing.cpu_count() - 1)
        print(f"Using {cls.num_processes} CPU cores for parallel testing")

    def test_01_number_of_pieces(self):
        """Ensures that the optimal number of pieces is less than or equal to the given pieces."""
        print("Running test_number_of_pieces in parallel...")
        start_time = time.time()

        # Create a partial function with fixed arguments
        test_func = partial(test_variant_number_of_pieces,
                            test_cases=self.test_cases)

        # Process variants in parallel
        valid_variants = []
        try:
            with multiprocessing.Pool(processes=self.num_processes) as pool:
                # Create tasks for each variant
                tasks = [(i, self.algorithms[i]) for i in self.valid_variants]

                # Use a smaller chunksize for better load balancing
                chunksize = max(1, len(tasks) // (self.num_processes * 4))

                # Process results as they come in
                for i, result in enumerate(pool.starmap(test_func, tasks, chunksize=chunksize)):
                    if result is not None:  # Variant passed
                        valid_variants.append(result)

                    # Print progress occasionally
                    if (i + 1) % 25000 == 0 or i + 1 == len(tasks):
                        elapsed = time.time() - start_time
                        print(
                            f"Progress: {i + 1}/{len(tasks)} variants processed ({(i + 1) / len(tasks) * 100:.1f}%) in {elapsed:.2f} seconds")
        except Exception as e:
            print(f"Error during parallel processing: {type(e).__name__}: {e}")

        print(f"Test completed in {time.time() - start_time:.2f} seconds")
        print(f"{len(valid_variants)} variants passed the number_of_pieces test")
        self.__class__.valid_variants = valid_variants  # Persist changes across tests

    def test_02_epsilon_difference(self):
        """Validates that the epsilon difference is maintained between old and new function values."""
        print("Running test_epsilon_difference in parallel...")
        start_time = time.time()

        # Create a partial function with fixed arguments
        test_func = partial(test_variant_epsilon_difference,
                            test_cases=self.test_cases)

        # Process variants in parallel
        valid_variants = []
        try:
            with multiprocessing.Pool(processes=self.num_processes) as pool:
                # Create tasks for each variant
                tasks = [(i, self.algorithms[i]) for i in self.valid_variants]

                # Use a smaller chunksize for better load balancing
                chunksize = max(1, len(tasks) // (self.num_processes * 4))

                # Process results as they come in
                for i, result in enumerate(pool.starmap(test_func, tasks, chunksize=chunksize)):
                    if result is not None:  # Variant passed
                        valid_variants.append(result)

                    # Print progress occasionally
                    if (i + 1) % 25000 == 0 or i + 1 == len(tasks):
                        elapsed = time.time() - start_time
                        print(
                            f"Progress: {i + 1}/{len(tasks)} variants processed ({(i + 1) / len(tasks) * 100:.1f}%) in {elapsed:.2f} seconds")
        except Exception as e:
            print(f"Error during parallel processing: {type(e).__name__}: {e}")

        print(f"Test completed in {time.time() - start_time:.2f} seconds")
        print(f"{len(valid_variants)} variants passed the epsilon_difference test")
        self.__class__.valid_variants = valid_variants

    def test_03_simpler_approximation(self):
        """Evaluates whether valid variants provide a simpler approximation compared to the original algorithm."""
        print("Running test_simpler_approximation in parallel...")
        start_time = time.time()

        threshold = 13
        successful_variants = []

        # Create tasks for each variant
        tasks = [(i, self.algorithms[i], self.test_cases, self.original_algorithm)
                 for i in self.valid_variants]

        try:
            with multiprocessing.Pool(processes=self.num_processes) as pool:
                # Use a smaller chunksize for better load balancing
                chunksize = max(1, len(tasks) // (self.num_processes * 4))

                # Process results as they come in
                results = []
                for i, result in enumerate(pool.imap(test_variant_simpler_approximation, tasks, chunksize=chunksize)):
                    variant_index, score = result
                    results.append((variant_index, score))

                    # Print progress occasionally
                    if (i + 1) % 1000 == 0 or i + 1 == len(tasks):
                        elapsed = time.time() - start_time
                        print(
                            f"Progress: {i + 1}/{len(tasks)} variants processed ({(i + 1) / len(tasks) * 100:.1f}%) in {elapsed:.2f} seconds")

                # Filter successful variants
                successful_variants = [(idx, score) for idx, score in results if score >= threshold]
        except Exception as e:
            print(f"Error during parallel processing: {type(e).__name__}: {e}")

        print(f"Test completed in {time.time() - start_time:.2f} seconds")
        print(f"{len(successful_variants)} Variants passed functionality tests:")
        for index, score in successful_variants:
            print(f"Variant {index}: Passed {score} test cases.")
            print_algorithm_code(self.algorithms[index])

        self.assertGreaterEqual(len(successful_variants), 1, "No variants passed the simpler_approximation tests!")


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(AlgorithmFunctionalityTests)
    )