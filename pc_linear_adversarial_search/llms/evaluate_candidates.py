import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import runpy
import numpy as np

from pc_linear_adversarial_search.candidate_algorithms.candidates import candidate_algorithms
from optimal_algorithms.pc_linear_apx import approximate_pc_linear_fx as optimal_algorithm
from pc_linear_adversarial_search.cpu_parallel import is_within_epsilon

SAMPLES = 30
TESTCASES_PER_SAMPLE = 10
TOTAL_TESTCASES = SAMPLES * TESTCASES_PER_SAMPLE
TESTCASE_FILE = "claude.py"

# ---------------------------
# Validation & duplicates
# ---------------------------

def validate_test_case(tc):
    """
    Validates a test case for piecewise linear approximation.

    Rules:
      - epsilon >= 0
      - pw_linear_fx length >= 2
      - x1, x2, ..., x_{n+1} strictly increasing
      - tuples in pw_linear_fx are 2-tuples of numbers
      - no repeated keys (not directly checkable in Python dicts unless parsing from raw input)
    """
    try:
        # Check keys and types
        if list(tc.keys()).count("pw_linear_fx") > 1 or list(tc.keys()).count("epsilon") > 1:
            return False, "duplicate_keys"

        pw_linear_fx = tc["pw_linear_fx"]
        epsilon = float(tc["epsilon"])
    except Exception:
        return False, "missing_keys"

    # Check epsilon
    if epsilon < 0:
        return False, "epsilon_not_positive"

    # Check structure
    if not isinstance(pw_linear_fx, (list, tuple)) or len(pw_linear_fx) < 2:
        return False, "bad_structure"

    # Check each element is a 2-tuple of numbers
    for pt in pw_linear_fx:
        if not isinstance(pt, (list, tuple)) or len(pt) != 2:
            return False, "bad_point_format"
        if not isinstance(pt[0], (int, float)) or not isinstance(pt[1], (int, float)):
            return False, "non_numeric_point"

    # Check strictly increasing x-values
    for i in range(len(pw_linear_fx) - 1):
        if pw_linear_fx[i][0] >= pw_linear_fx[i + 1][0]:
            return False, "x_not_strictly_increasing"

    return True, "ok"


def testcase_key(tc):
    """Key for duplicate detection: exact match on epsilon and all (x,y)."""
    eps = float(tc["epsilon"])
    pw_linear_fx = tuple((float(x), float(y)) for (x, y) in tc["pw_linear_fx"])
    return (eps, pw_linear_fx)


# --- simple sup-norm check (L∞) ---
# def sup_norm_distance(pw_linear_fx, fx_hat):
#     xs1 = [pw_linear_fx[i][0] for i in range(1, len(pw_linear_fx) - 1)]
#     ys1 = [pw_linear_fx[i][1] for i in range(1, len(pw_linear_fx) - 1)]
#     xs2 = [fx_hat[i][0] for i in range(1, len(fx_hat) - 1)]
#     ys2 = [fx_hat[i][1] for i in range(1, len(fx_hat) - 1)]
#     xs = sorted(set(xs1 + xs2))
#     i = j = 0
#     err = 0.0
#     for x in xs:
#         while i + 1 < len(xs1) and x >= xs1[i + 1]:
#             i += 1
#         while j + 1 < len(xs2) and x >= xs2[j + 1]:
#             j += 1
#         y1 = ys1[i] if i < len(ys1) else ys1[-1]
#         y2 = ys2[j] if j < len(ys2) else ys2[-1]
#         err = max(err, abs(y1 - y2))
#     return err
#
# def is_within_epsilon(pw_linear_fx, fx_hat, epsilon):
#     return sup_norm_distance(pw_linear_fx, fx_hat) <= epsilon + 1e-12


# --- load testcases from single file ---
def load_batches(filepath):
    g = runpy.run_path(filepath)
    batches = []
    for i in range(1, SAMPLES + 1):
        key = f"test_cases{i}"
        if key in g:
            batches.append(g[key])
    return batches

# ---------------------------
# Evaluate (valid-only; track duplicates)
# ---------------------------
def evaluate_algorithm(alg, valid_unique_cases):
    all_deltas = []
    eps_fail = 0
    opt_fail = 0
    total_fail = 0
    for tc in valid_unique_cases:
        pw_linear_fx = tc["pw_linear_fx"]
        eps = float(tc["epsilon"])
        _, opt_pieces, _ = optimal_algorithm(pw_linear_fx, eps)
        fx_hat, cand_pieces, _ = alg(pw_linear_fx, eps)

        # record delta
        delta = cand_pieces - opt_pieces
        all_deltas.append(delta)

        fail_eps = not is_within_epsilon(pw_linear_fx, fx_hat, eps)
        fail_opt = cand_pieces > opt_pieces

        if fail_eps:
            eps_fail += 1
        if fail_opt:
            opt_fail += 1
        if fail_eps or fail_opt:
            total_fail += 1

    mean_delta = np.mean(all_deltas)
    sd_delta = np.std(all_deltas, ddof=1)
    eps_fail_pct = 100 * eps_fail / TOTAL_TESTCASES
    opt_fail_pct = 100 * opt_fail / TOTAL_TESTCASES
    total_fail_pct = 100 * total_fail / TOTAL_TESTCASES

    return mean_delta, sd_delta, eps_fail_pct, opt_fail_pct, total_fail_pct

def main():
    batches = load_batches(TESTCASE_FILE)
    # for i, batch in enumerate(batches, start=1):
    #     print(f"test_cases{i} length = {len(batch)}")

    # Flatten to one list
    all_cases = [tc for batch in batches for tc in batch]
    total_cases = len(all_cases)

    # Validate + duplicate detection
    seen = set()
    valid_cases = []
    invalid_count = 0
    dup_count = 0

    for index, tc in enumerate(all_cases):
        ok, _reason = validate_test_case(tc)
        if not ok:
            # print(f"index: {index} {_reason} {tc}")
            invalid_count += 1
            continue
        k = testcase_key(tc)
        if k in seen:
            dup_count += 1
            # still skip running it (count as duplicate)
            continue
        seen.add(k)
        valid_cases.append(tc)
    valid_count = len(valid_cases)

    valid_pct = 100.0 * valid_count / total_cases if total_cases else 0.0
    invalid_pct = 100.0 * invalid_count / total_cases if total_cases else 0.0
    dup_pct = 100.0 * dup_count / total_cases if total_cases else 0.0

    print(f"Total cases: {total_cases}")
    print(f"Valid (unique) cases: {valid_count} ({valid_pct:.1f}%)")
    print(f"Invalid cases: {invalid_count} ({invalid_pct:.1f}%)")
    print(f"Duplicate cases: {dup_count} ({dup_pct:.1f}%)")
    print("-" * 60)

    for alg in candidate_algorithms:
        name = getattr(alg, "__name__", str(alg))
        mean_delta, sd_delta, eps_fail_pct, opt_fail_pct, total_fail_pct = evaluate_algorithm(alg, valid_cases)
        print(f"{name}: "
              f"%ε-fail={eps_fail_pct:.1f}%, %opt-fail={opt_fail_pct:.1f}%, "
              f"%total-fail={total_fail_pct:.1f}%")

if __name__ == "__main__":
    main()
