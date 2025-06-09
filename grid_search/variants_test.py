from grid_search.get_variants import generate_variant_configs, create_variant_wrapper
from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path
from test_cases import test_cases
import numpy as np
import multiprocessing
from tqdm import tqdm
import time

def is_within_epsilon(pc_cons_fx, optimal_pc_fx, epsilon):
    optimal_pc_fx_sorted = sorted(optimal_pc_fx, key=lambda x: x[0])
    for i in range(1, len(pc_cons_fx) - 1):
        y = pc_cons_fx[i][1]
        y_opt = optimal_pc_fx_sorted[i - 1][1]
        if not np.isclose(y, y_opt, atol=epsilon, rtol=1e-9):
            return False
    return True

def run_baseline_algorithm(pc_cons_fx, epsilon):
    _, optimal_num_pieces, _ = approximate_pc_shortest_path(pc_cons_fx, epsilon)
    return optimal_num_pieces

# --- Core Test Per Variant ---
def test_variant(variant_data):
    idx, (variant_func, meta) = variant_data
    try:
        score = 0  # for simpler approximation score
        for pc_cons_fx, epsilon in test_cases:
            # Run variant
            opt_fx, opt_num_pieces, given_num_pieces = variant_func(pc_cons_fx, epsilon)

            # -------------- Test 1: Piece Count Validity --------------
            if given_num_pieces < opt_num_pieces:
                return None  # FAIL if variant gives more pieces than input

            # -------------- Test 2: Epsilon Difference --------------
            if not is_within_epsilon(pc_cons_fx, opt_fx, epsilon):
                return None  # FAIL if variant output exceeds epsilon

            # -------------- Test 3: Simpler Approximation --------------
            baseline_pieces = run_baseline_algorithm(pc_cons_fx, epsilon)
            if opt_num_pieces <= baseline_pieces:
                score += 1  # Reward if variant matches or improves baseline

        return (idx, meta, score)

    except Exception as e:
        return None

# --- Main Testing Loop ---
def run_tests_on_the_fly(max_variants=None, score_threshold=None):
    print("Running on-the-fly variant testing with multiprocessing...")
    start_time = time.time()
    variant_gen = ((idx, create_variant_wrapper(config)) for idx, config in enumerate(generate_variant_configs()))
    num_processes = max(1, multiprocessing.cpu_count() - 1)

    successful_variants = []
    total_tested = 0

    if score_threshold is None:
        score_threshold = len(test_cases)  # By default, must pass all test cases

    with multiprocessing.Pool(processes=num_processes) as pool:
        with tqdm(total=max_variants, desc="Testing Variants", unit="variant") as pbar:
            for result in pool.imap(test_variant, variant_gen, chunksize=100):
                total_tested += 1
                if result is not None:
                    idx, meta, score = result
                    if score >= score_threshold:
                        successful_variants.append((idx, meta, score))
                        print(f"\nVariant {idx} passed with score {score}:")
                        print(f"  Traversal: {meta['loop_behavior']}")
                        print(f"  Params Min: {meta['params_min']}")
                        print(f"  Params Max: {meta['params_max']}")
                        print(f"  Condition Ops: {meta['condition_params']}")
                pbar.update(1)
                if max_variants is not None and total_tested >= max_variants:
                    break

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal tested: {total_tested}")
    print(f"Total successful variants: {len(successful_variants)}")
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"Time taken: {int(minutes)} minutes {seconds:.2f} seconds")

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    run_tests_on_the_fly()
