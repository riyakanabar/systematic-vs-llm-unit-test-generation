import runpy
import numpy as np

from pc_const_adversarial_search.input_algorithms import candidate_algorithms
from optimal_algorithms.pc_cons_apx import approximate_pc_shortest_path as optimal_algorithm
from grid_search.variants_test import is_within_epsilon

SAMPLES = 30
TESTCASES_PER_SAMPLE = 10
TOTAL_TESTCASES = SAMPLES * TESTCASES_PER_SAMPLE
TESTCASE_FILE = "claude.py"

# ---------------------------
# Validation & duplicates
# ---------------------------
def is_finite(x):
    return np.isfinite(x)
def validate_test_case(tc):
    """
    Rules you specified:
      - epsilon > 0
      - pc_fx format: [(-inf, inf), (x1,y1), ... , (x_{n+1}, inf)]
      - x1, x2, ..., x_{n+1} strictly increasing
      - x_{n+1} must be finite (the last *y* is +inf sentinel)
    """
    try:
        pc_fx = tc["pc_fx"]
        eps = float(tc["epsilon"])
    except Exception:
        return False, "missing_keys"

    # epsilon > 0 (strict, per your instruction)
    if not (eps >= 0):
        return False, "epsilon_not_positive"

    if not isinstance(pc_fx, (list, tuple)) or len(pc_fx) < 3:
        return False, "bad_structure"

    # First sentinel must be (-inf, inf)
    x0, y0 = pc_fx[0]
    if not (x0 == -float("inf") and y0 == float("inf")):
        return False, "bad_first_sentinel"

    # Last sentinel must be (x_{n+1}, inf) with finite x_{n+1}
    x_last, y_last = pc_fx[-1]
    if not (is_finite(x_last) and y_last == float("inf")):
        return False, "bad_last_sentinel"

    # Extract xs, ys for real pieces: indices 1..len-2

    for i in range(1, len(pc_fx) - 1):
        xi, yi = pc_fx[i]
        if not (is_finite(xi) and is_finite(yi)):
            return False, "nonfinite_piece_value"

    # Strictly increasing x’s (no duplicates)
    for i in range(1, len(pc_fx) - 1):
        if not (pc_fx[i][0] < pc_fx[i + 1][0]):
            return False, "x_not_strictly_increasing"

    return True, "ok"

def testcase_key(tc):
    """Key for duplicate detection: exact match on epsilon and all (x,y)."""
    eps = float(tc["epsilon"])
    pc_fx = tuple((float(x), float(y)) for (x, y) in tc["pc_fx"])
    return (eps, pc_fx)


# --- simple sup-norm check (L∞) ---
# def sup_norm_distance(pc_fx, fx_hat):
#     xs1 = [pc_fx[i][0] for i in range(1, len(pc_fx) - 1)]
#     ys1 = [pc_fx[i][1] for i in range(1, len(pc_fx) - 1)]
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
# def is_within_epsilon(pc_fx, fx_hat, epsilon):
#     return sup_norm_distance(pc_fx, fx_hat) <= epsilon + 1e-12


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
        pc_fx = tc["pc_fx"]
        eps = float(tc["epsilon"])

        _, opt_pieces, _ = optimal_algorithm(pc_fx, eps)
        fx_hat, cand_pieces, _ = alg(pc_fx, eps)

        # record delta
        delta = cand_pieces - opt_pieces
        all_deltas.append(delta)

        fail_eps = not is_within_epsilon(pc_fx, fx_hat, eps)
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
