#30 Sept few-shot prompt with ChatGPT Free 5:11PM
test_cases1 = [
    # 1. Perfectly linear function, no approximation needed
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 2. Flat line with noise within epsilon → should collapse to one segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.05), (2.0, 0.95), (3.0, 1.02)],
        "epsilon": 0.1
    },

    # 3. Piecewise exact V-shape, must break at center
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.0
    },

    # 4. Slightly noisy V-shape, should merge into one line within epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 0.0)],
        "epsilon": 0.1
    },

    # 5. Large jump discontinuity, must split
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 0.5
    },

    # 6. Many collinear points (redundant, should reduce to one segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 7. Zigzag oscillations smaller than epsilon → should compress
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.05), (4.0, -0.05)],
        "epsilon": 0.2
    },

    # 8. Zigzag oscillations larger than epsilon → must preserve
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 1.0), (4.0, -1.0)],
        "epsilon": 0.5
    },

    # 9. Single point repeated (degenerate case)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)],
        "epsilon": 0.0
    },

    # 10. Non-uniform spacing of x values (important edge case)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.5), (5.0, 25.0), (10.0, 50.0)],
        "epsilon": 1.0
    }
]
test_cases2 = [
    # 1. Simple flat line (epsilon = 0 allows no approximation slack)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.0
    },

    # 2. Increasing line perfectly linear (should compress to 1 segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.1
    },

    # 3. Zig-zag function with tight epsilon (forces many pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.01
    },

    # 4. Zig-zag function with loose epsilon (can be compressed to fewer segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.6
    },

    # 5. Duplicate consecutive points (tests robustness to redundant data)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.1
    },

    # 6. Large gap between points (forces long linear approximation)
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 100.0), (20.0, 200.0)],
        "epsilon": 1.0
    },

    # 7. Non-monotonic function with high curvature (forces more segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -5.0), (3.0, 5.0), (4.0, -5.0)],
        "epsilon": 0.5
    },

    # 8. Non-monotonic function with high tolerance (fewer pieces allowed)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -5.0), (3.0, 5.0), (4.0, -5.0)],
        "epsilon": 6.0
    },

    # 9. Minimal case: just two points (always 1 piece)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5
    },

    # 10. Nearly collinear but slightly noisy data (tests tolerance handling)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.1), (2.0, 3.9), (3.0, 6.2), (4.0, 8.0)],
        "epsilon": 0.25
    }
]
test_cases3 = [
    # 1. Flat line: should reduce to 1 piece regardless of epsilon > 0
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Perfect line: exact line, epsilon small, should reduce to 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 1e-6
    },

    # 3. V-shape (absolute value function): forces at least 2 pieces
    {
        "pw_linear_fx": [(-2.0, 2.0), (-1.0, 1.0), (0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.1
    },

    # 4. Small epsilon on noisy data: each point is distinct, must use many pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.2), (4.0, -0.2)],
        "epsilon": 0.05
    },

    # 5. Larger epsilon allows simplification: same noisy data but looser tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.2), (4.0, -0.2)],
        "epsilon": 0.5
    },

    # 6. Horizontal segments with jumps: requires multiple pieces if epsilon small
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 3.0), (4.0, 1.0)],
        "epsilon": 0.2
    },

    # 7. Duplicate x-values (vertical spike): invalid or must handle gracefully
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0)],
        "epsilon": 0.1
    },

    # 8. Large flat section, then sharp corner
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.5
    },

    # 9. Almost collinear but within epsilon: should merge into 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 1.98), (3.0, 3.05)],
        "epsilon": 0.1
    },

    # 10. Staircase function: each step must be kept if epsilon is small
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.05
    }
]
test_cases4 = [
    # 1. Flat line: all y-values same, should compress to 1 piece
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Perfect line: exact straight line, no approximation error
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 3. Small wiggles under tolerance: should collapse to fewer pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.04), (3.0, 0.02)],
        "epsilon": 0.1
    },

    # 4. Wiggles just above tolerance: must keep more pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.3), (2.0, -0.25), (3.0, 0.4)],
        "epsilon": 0.2
    },

    # 5. Non-uniform spacing in x: algorithm must handle irregular intervals
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (2.0, 3.9), (5.0, 10.1)],
        "epsilon": 0.2
    },

    # 6. Sharp corner: cannot merge across corner under small epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 4.0), (2.0, 8.0), (4.0, 12.0)],
        "epsilon": 0.5
    },

    # 7. Multiple slopes, piecewise linear but within epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0), (4.0, 2.0)],
        "epsilon": 0.5
    },

    # 8. High epsilon: should collapse almost everything to 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -3.0), (3.0, 4.0), (4.0, -2.0)],
        "epsilon": 10.0
    },

    # 9. Dense sampling of sine wave: must split where necessary
    {
        "pw_linear_fx": [(x, __import__("math").sin(x)) for x in [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]],
        "epsilon": 0.1
    },

    # 10. Duplicate x-values with different y: degenerate case
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0), (2.0, 5.0)],
        "epsilon": 0.5
    },
]
test_cases5 = [
    # 1. Perfectly linear data (should compress to 1 piece for any ε ≥ 0)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
        "epsilon": 0.0
    },

    # 2. Horizontal line (flat function, no error regardless of ε)
    {
        "pw_linear_fx": [(0, 2), (1, 2), (2, 2), (3, 2)],
        "epsilon": 0.1
    },

    # 3. Single "spike" in the middle (forces extra piece if ε is too small)
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 10), (3, 0), (4, 0)],
        "epsilon": 1.0
    },

    # 4. Alternating up and down (zigzag, tests compression under ε)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.5
    },

    # 5. Data with redundant points on a line (algorithm should ignore them)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (2.5, 2.5), (3, 3), (4, 4)],
        "epsilon": 0.0
    },

    # 6. Large flat region, then sharp change (tests selective splitting)
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 10), (4, 20)],
        "epsilon": 2.0
    },

    # 7. Non-uniform spacing (tests handling of different x intervals)
    {
        "pw_linear_fx": [(0, 0), (0.1, 1), (1, 2), (10, 12), (20, 22)],
        "epsilon": 0.5
    },

    # 8. Very tight epsilon forces maximal segmentation
    {
        "pw_linear_fx": [(0, 0), (1, 1.1), (2, 2.2), (3, 3.3)],
        "epsilon": 0.01
    },

    # 9. Large epsilon allows full compression (all points approximated by 1 line)
    {
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 1.1), (3, 1.5), (4, 2.0)],
        "epsilon": 10.0
    },

    # 10. Edge case with only two points (always 1 segment, regardless of ε)
    {
        "pw_linear_fx": [(0, 5), (10, 15)],
        "epsilon": 0.001
    }
]
test_cases6 = [
    # 1. Perfectly linear data (should collapse to 1 segment if epsilon >= 0)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 2. Redundant points on the same line (should still be 1 segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 2.0), (1.5, 3.0), (2.0, 4.0)],
        "epsilon": 0.1
    },

    # 3. Flat segments with sharp jump (forces multiple pieces)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.5
    },

    # 4. Oscillating function (forces many small pieces for small epsilon)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.2
    },

    # 5. Same oscillating function but with large epsilon (can compress to fewer pieces)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 1.0
    },

    # 6. Single outlier point (algorithm should keep extra piece for accuracy)
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 0), (4, 0)],
        "epsilon": 0.5
    },

    # 7. Dense sampling of a smooth curve (should reduce points aggressively)
    {
        "pw_linear_fx": [(x, x**2) for x in [0.0, 0.5, 1.0, 1.5, 2.0]],
        "epsilon": 0.5
    },

    # 8. Vertical-ish segments (steep slope differences)
    {
        "pw_linear_fx": [(0, 0), (0.1, 10), (0.2, 20), (1.0, 30)],
        "epsilon": 1.0
    },

    # 9. Random noisy line close to y=x (tests tolerance handling)
    {
        "pw_linear_fx": [(0, 0.1), (1, 0.9), (2, 2.2), (3, 3.1), (4, 4.05)],
        "epsilon": 0.3
    },

    # 10. Long flat with sudden slope change (tests segment splitting at right place)
    {
        "pw_linear_fx": [(0, 0), (2, 0), (4, 0), (6, 6), (8, 12), (10, 18)],
        "epsilon": 0.5
    }
]
test_cases7 = [
    # 1. Exact line (should compress to 1 piece for any epsilon >= 0)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 2. Horizontal flat line with noise just within epsilon
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.9), (3.0, 1.05), (4.0, 1.0)],
        "epsilon": 0.2
    },

    # 3. Single sharp corner (forces extra segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 4. Repeated points (duplicate x,y values should not add segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0
    },

    # 5. Large gap between points (forces long interpolation check)
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0), (20.0, 10.0), (30.0, 20.0)],
        "epsilon": 1.0
    },

    # 6. Zigzag pattern within tolerance (should compress aggressively)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.1
    },

    # 7. Zigzag pattern just below tolerance (forces more pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.9
    },

    # 8. Non-uniform spacing in x (tests interpolation accuracy)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (2.0, 2.0), (5.0, 10.0)],
        "epsilon": 0.2
    },

    # 9. Nearly collinear points but slightly off (within epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 2.0), (3.0, 2.99), (4.0, 4.02)],
        "epsilon": 0.05
    },

    # 10. Extreme values (tests numerical stability under large coordinates)
    {
        "pw_linear_fx": [(-1e6, -1e6), (0.0, 0.0), (1e6, 1e6)],
        "epsilon": 1e-3
    }
]
test_cases8 = [
    # 1. Simple flat line (should collapse to 1 piece if epsilon >= 0)
    {
        "pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 1)],
        "epsilon": 0.0
    },

    # 2. Single sharp corner (forces extra piece if epsilon is small)
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0)],
        "epsilon": 0.5
    },

    # 3. Zig-zag small oscillations (should reduce pieces when epsilon > amplitude)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 1.0
    },

    # 4. Increasing straight line (can be approximated by 1 piece)
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6)],
        "epsilon": 0.1
    },

    # 5. Steep slope change in the middle (tests piece splitting)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 10), (3, 11)],
        "epsilon": 0.5
    },

    # 6. Duplicate x values with jumps (tests vertical "step")
    {
        "pw_linear_fx": [(0, 0), (1, 0), (1, 5), (2, 5)],
        "epsilon": 0.1
    },

    # 7. Long flat + sudden spike + flat (spike must force segmentation)
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 10), (3, 0), (4, 0)],
        "epsilon": 1.0
    },

    # 8. Very small epsilon compared to noise (forces many pieces)
    {
        "pw_linear_fx": [(i, (i % 2)) for i in range(10)],
        "epsilon": 0.01
    },

    # 9. Very large epsilon (everything collapses to one piece)
    {
        "pw_linear_fx": [(0, 0), (1, 10), (2, -10), (3, 20)],
        "epsilon": 50.0
    },

    # 10. Non-uniform spacing in x (tests handling irregular intervals)
    {
        "pw_linear_fx": [(0, 0), (0.1, 1), (5, 10), (6, 10.5), (10, 20)],
        "epsilon": 0.5
    }
]
test_cases9 = [
    # 1. Single line segment, should need only 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.1
    },

    # 2. Perfectly linear sequence, high epsilon (should compress to 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 1.0
    },

    # 3. Perfectly linear sequence, tiny epsilon (forces all original segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 4. Flat then jump (edge case: discontinuity-like behavior)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 5.0)],
        "epsilon": 0.5
    },

    # 5. Alternating up/down "zig-zag", small epsilon (forces many pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1
    },

    # 6. Zig-zag with large epsilon (compressible into fewer pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 7. Non-uniform spacing of x-values (tests handling long segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 4.0), (5.0, 10.0), (10.0, 20.0)],
        "epsilon": 0.5
    },

    # 8. Sudden steep slope change (forces split at slope break)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 11.0)],
        "epsilon": 0.5
    },

    # 9. Horizontal line (flat), any epsilon > 0 should give 1 piece
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.3
    },

    # 10. Non-monotonic function (up, down, up), small epsilon to force detail
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, -1.0), (3.0, 3.0), (4.0, 0.0)],
        "epsilon": 0.2
    },
]
test_cases10 = [
    # 1. Perfectly linear, should compress to 1 segment regardless of epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.1
    },

    # 2. Horizontal flat line, should compress to 1 segment
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0
    },

    # 3. Single sharp corner (forces break at corner)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 0.5
    },

    # 4. Alternating zig-zag, tight epsilon means many pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1
    },

    # 5. Alternating zig-zag, loose epsilon should allow compression
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 6. Non-uniform spacing between x’s (important for optimality)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.5), (1.0, 1.0), (5.0, 5.0)],
        "epsilon": 0.2
    },

    # 7. Large epsilon allows reduction to 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 3.0)],
        "epsilon": 10.0
    },

    # 8. Tight epsilon requires keeping all points (almost no compression)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 9. Plateau followed by slope (corner detection needed)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 3.0), (4.0, 6.0)],
        "epsilon": 0.5
    },

    # 10. Large input, slow slope changes (check scalability and optimality)
    {
        "pw_linear_fx": [(x, x + (0.1 * ((-1) ** x))) for x in range(11)],
        "epsilon": 0.2
    }
]
test_cases11 = [
    # 1. Simple horizontal line (all points same y), should compress to 1 segment
    {"pw_linear_fx": [(0, 2), (1, 2), (2, 2), (3, 2)], "epsilon": 0.1},

    # 2. Single sharp peak, tolerance too small to merge
    {"pw_linear_fx": [(0, 1), (1, 1), (2, 5), (3, 1)], "epsilon": 0.5},

    # 3. Two points exactly at epsilon limit
    {"pw_linear_fx": [(0, 0), (1, 1.0), (2, 2.0)], "epsilon": 1.0},

    # 4. Linear increasing, should compress to 1 segment
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.01},

    # 5. Linear decreasing, small epsilon, no compression
    {"pw_linear_fx": [(0, 3), (1, 2), (2, 1), (3, 0)], "epsilon": 0.0},

    # 6. Alternating up and down, challenging for optimality
    {"pw_linear_fx": [(0, 0), (1, 2), (2, -1), (3, 1), (4, 0)], "epsilon": 0.5},

    # 7. Flat section in middle, should merge start and end separately
    {"pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 3), (4, 3)], "epsilon": 0.2},

    # 8. Very close points, epsilon larger than variation
    {"pw_linear_fx": [(0, 0), (0.1, 0.05), (0.2, 0.1), (0.3, 0.15)], "epsilon": 0.2},

    # 9. Zig-zag pattern with small epsilon, forcing many segments
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.1},

    # 10. Large jump at end, should form separate segment
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 10)], "epsilon": 0.5}
]
test_cases12 = [
    # 1. Simple linear increase (should remain 1 segment for small epsilon)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.1},

    # 2. Horizontal segment followed by sharp increase
    {"pw_linear_fx": [(0, 2), (1, 2), (2, 5), (3, 8)], "epsilon": 0.5},

    # 3. Sharp peak in the middle
    {"pw_linear_fx": [(0, 0), (1, 5), (2, 0), (3, 0)], "epsilon": 0.5},

    # 4. Small oscillations (tests epsilon tolerance)
    {"pw_linear_fx": [(0, 0), (1, 0.2), (2, -0.1), (3, 0)], "epsilon": 0.25},

    # 5. Flat line (should return single segment for any epsilon > 0)
    {"pw_linear_fx": [(0, 3), (1, 3), (2, 3), (4, 3)], "epsilon": 0.1},

    # 6. Two identical points (tests repeated coordinates)
    {"pw_linear_fx": [(0, 0), (0, 0), (1, 1), (2, 2)], "epsilon": 0.1},

    # 7. Large epsilon allows merging multiple segments
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6)], "epsilon": 5.0},

    # 8. Single sudden jump at the end
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 1), (3, 10)], "epsilon": 0.5},

    # 9. Non-uniform x spacing (tests generality)
    {"pw_linear_fx": [(0, 0), (0.5, 1), (2, 2), (5, 5)], "epsilon": 0.2},

    # 10. Zig-zag pattern (tests multiple minimum segments)
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)], "epsilon": 0.1}
]
test_cases13 = [
    # 1. Simple linear function, should be approximated by 1 segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.1},

    # 2. Function with a sharp jump, needs multiple segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 6.0)], "epsilon": 0.5},

    # 3. Function with small oscillations, testing tight epsilon
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.05)], "epsilon": 0.05},

    # 4. Flat function, epsilon large enough to allow full approximation by 1 segment
    {"pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.5},

    # 5. Alternating peaks, each peak needs its own segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)], "epsilon": 0.3},

    # 6. Function with small slope change, testing if algorithm merges segments correctly
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.05), (3.0, 3.0)], "epsilon": 0.1},

    # 7. Large jump exceeding epsilon, must force new segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)], "epsilon": 1.0},

    # 8. Single segment already within epsilon, edge case with 2 points
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.5)], "epsilon": 0.6},

    # 9. Multiple flat sections with small jumps, testing merge behavior
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.0), (3.0, 2.0), (4.0, 2.1)], "epsilon": 0.15},

    # 10. Oscillatory function with tight epsilon to force max segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.1}
]
test_cases14 = [
    # 1. Simple exact linear segments, epsilon smaller than deviation
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.01},

    # 2. Small deviation, epsilon allows merging two segments into one
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 2.02), (3.0, 3.0)], "epsilon": 0.05},

    # 3. Oscillating data points, small epsilon prevents merging
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.5), (2.0, 1.0), (3.0, 2.0)], "epsilon": 0.1},

    # 4. Single sharp peak, tests handling of abrupt changes
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0)], "epsilon": 0.5},

    # 5. Flat data, epsilon zero, algorithm should recognize single segment
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.0},

    # 6. Flat data with small noise, epsilon allows ignoring noise
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.01), (2.0, 1.99), (3.0, 2.0)], "epsilon": 0.05},

    # 7. Minimal x spacing, very small segments, tests algorithm precision
    {"pw_linear_fx": [(0.0, 0.0), (0.001, 0.001), (0.002, 0.002), (0.003, 0.003)], "epsilon": 1e-6},

    # 8. Large slope, tests handling of steep segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 200.0), (3.0, 300.0)], "epsilon": 1.0},

    # 9. Mixed small and large slopes, complex merging decisions
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 5.0), (3.0, 5.5), (4.0, 10.0)], "epsilon": 0.5},

    # 10. Plateau followed by sharp rise, tests optimal segmentation
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 10.0), (4.0, 20.0)], "epsilon": 1.0},
]
test_cases15 = [
    # 1. Perfectly linear – should require 1 segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.1},

    # 2. Single sharp peak in the middle – must break at peak
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 0.0)], "epsilon": 0.5},

    # 3. Step function – horizontal segments, testing flat regions
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.1},

    # 4. Oscillating small deviations – epsilon should allow skipping small oscillations
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.05), (4.0, 0.0)], "epsilon": 0.15},

    # 5. Large jump – must create separate segment for jump
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.2},

    # 6. Monotone but nonlinear – epsilon allows single segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 1.8), (3.0, 2.7)], "epsilon": 0.15},

    # 7. Linear with one outlier – should break at outlier
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 3.0)], "epsilon": 0.5},

    # 8. Small variations around a straight line – epsilon too small to allow merge
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.05)], "epsilon": 0.05},

    # 9. Long flat region followed by a steep rise
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 10.0)], "epsilon": 0.3},

    # 10. Alternating peaks – forces maximum splits
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, -2.0), (3.0, 2.0), (4.0, -2.0)], "epsilon": 0.5}
]
test_cases16 = [
    # 1. Simple linear points - should need only 1 segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.1},

    # 2. Single peak - algorithm should split at the peak
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.5},

    # 3. Flat line - all points same y, should be 1 segment
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.0},

    # 4. Steep slope exceeding epsilon - must split each point
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 10.0), (3.0, 15.0)], "epsilon": 2.0},

    # 5. Oscillating points around line - tests ε handling
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.1), (3.0, 0.1), (4.0, 0.0)], "epsilon": 0.15},

    # 6. Collinear but spaced points - should need 1 segment
    {"pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (4.0, 4.0), (6.0, 6.0)], "epsilon": 0.0},

    # 7. Horizontal plateau in middle - split at plateau edges
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 3.0)], "epsilon": 0.1},

    # 8. Points exactly at epsilon limit - tests boundary condition
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0)], "epsilon": 0.1},

    # 9. Rapidly changing slope - should force multiple splits
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)], "epsilon": 0.2},

    # 10. Increasing then flat then decreasing - complex pattern
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 4.0), (4.0, 2.0), (5.0, 0.0)], "epsilon": 0.3},
]
test_cases17 = [
    # 1. Perfectly linear, should return 1 segment for any ε > 0
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.1},

    # 2. Slight deviation at middle point, tests algorithm tolerance
    {"pw_linear_fx": [(0, 0), (1, 1.05), (2, 2), (3, 3)], "epsilon": 0.05},

    # 3. Sharp corner, requires at least 2 segments
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, -1)], "epsilon": 0.1},

    # 4. Multiple small deviations, tests if algorithm avoids unnecessary segments
    {"pw_linear_fx": [(0, 0), (1, 0.05), (2, 0.1), (3, 0.05), (4, 0)], "epsilon": 0.1},

    # 5. Increasing slope, tests variable slopes handling
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 3), (3, 6), (4, 10)], "epsilon": 0.5},

    # 6. Alternating peaks, forces algorithm to create multiple segments
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.1},

    # 7. Flat region followed by slope, tests merging flat points
    {"pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 10), (4, 15)], "epsilon": 0.1},

    # 8. Single spike in middle, should only split around spike
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 0), (4, 0)], "epsilon": 0.5},

    # 9. Large uniform points, high epsilon, algorithm should reduce to minimal segments
    {"pw_linear_fx": [(0, 0), (1, 0.2), (2, 0.4), (3, 0.6), (4, 0.8)], "epsilon": 1.0},

    # 10. Oscillating pattern, tests if algorithm avoids over-segmentation
    {"pw_linear_fx": [(0, 0), (1, 2), (2, -1), (3, 3), (4, 0)], "epsilon": 1.5},
]
test_cases18 = [
    # 1. Simple linear, should be approximated with 1 segment
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.1},

    # 2. Sharp corner in the middle, cannot merge into 1 segment
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 2), (3, 2)], "epsilon": 0.5},

    # 3. Flat segment followed by linear increase
    {"pw_linear_fx": [(0, 1), (1, 1), (2, 2), (3, 3)], "epsilon": 0.2},

    # 4. Oscillating points, tests tolerance handling
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.5},

    # 5. Single segment almost flat, epsilon allows small deviation
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.05), (3, -0.05)], "epsilon": 0.2},

    # 6. Minimal points, only 2 points, should always be 1 segment
    {"pw_linear_fx": [(0, 0), (1, 1)], "epsilon": 0.1},

    # 7. Long linear segment with small deviation at the end
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 2.9)], "epsilon": 0.15},

    # 8. Zig-zag pattern, epsilon tight, requires multiple segments
    {"pw_linear_fx": [(0, 0), (1, 2), (2, -1), (3, 3), (4, 0)], "epsilon": 0.1},

    # 9. Repeated y-values, tests flat regions
    {"pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 10)], "epsilon": 0.3},

    # 10. Nearly perfect linear, but last point just outside epsilon
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3.51)], "epsilon": 0.5},
]
test_cases19 = [
    # 1. Perfectly linear, should return 1 segment
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.1},

    # 2. One sharp corner exceeding epsilon
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 3), (3, 3)], "epsilon": 0.5},

    # 3. Flat region, tolerance allows skipping intermediate points
    {"pw_linear_fx": [(0, 5), (1, 5.1), (2, 5.05), (3, 5)], "epsilon": 0.2},

    # 4. Noisy data just within epsilon
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, -0.05), (3, 0.05)], "epsilon": 0.15},

    # 5. Repeated points, should be compressed to fewer segments
    {"pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 2)], "epsilon": 0.1},

    # 6. Oscillating pattern, tolerance too small to skip peaks
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.1},

    # 7. Single large jump, epsilon allows straight line
    {"pw_linear_fx": [(0, 0), (1, 10), (2, 20)], "epsilon": 15},

    # 8. Slight curve, just under tolerance, should be 1 segment
    {"pw_linear_fx": [(0, 0), (1, 0.9), (2, 1.8), (3, 2.7)], "epsilon": 0.2},

    # 9. Increasing slope, small tolerance forces more segments
    {"pw_linear_fx": [(0, 0), (1, 0.5), (2, 2), (3, 4.5), (4, 8)], "epsilon": 0.5},

    # 10. Combination of flat and sharp rise, tests multiple break points
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 3), (4, 6)], "epsilon": 0.2}
]
test_cases20 = [
    # 1. Simple linear segment, should need only 1 piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)], "epsilon": 0.1},

    # 2. Two segments with sharp corner, epsilon smaller than deviation
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.1},

    # 3. Constant function, should need only 1 piece
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.05},

    # 4. Small deviation from line, epsilon larger than deviation
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.0)], "epsilon": 0.1},

    # 5. Large deviations, multiple pieces required
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 1.0), (3.0, 4.0), (4.0, 2.0)], "epsilon": 0.5},

    # 6. Very small epsilon, forcing maximum number of pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.9), (3.0, 1.1)], "epsilon": 0.01},

    # 7. Almost linear, epsilon allows one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 2.02), (3.0, 3.03)], "epsilon": 0.05},

    # 8. Step function, should force multiple pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.1},

    # 9. Single sharp peak, tolerance allows flattening?
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)], "epsilon": 2.0},

    # 10. Noisy data, moderate epsilon
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (1.0, -0.1), (1.5, 0.2), (2.0, 0.0)], "epsilon": 0.15}
]
test_cases21 = [
    # 1. Perfectly linear, epsilon small → should return 1 segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.1},

    # 2. One large deviation, epsilon small → should break into multiple segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 3.0)], "epsilon": 0.5},

    # 3. Horizontal line, zero slope, epsilon small → one segment
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.1},

    # 4. Vertical jump in y (step function), epsilon allows small jumps → multiple segments
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 3.0)], "epsilon": 0.5},

    # 5. Oscillating pattern, epsilon small → algorithm should break at peaks
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)], "epsilon": 0.1},

    # 6. Oscillating pattern, epsilon large → algorithm can merge multiple peaks
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)], "epsilon": 2.5},

    # 7. Single spike in middle, epsilon allows ignoring it → fewer segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)], "epsilon": 5.0},

    # 8. Multiple equal-length segments forming a staircase, epsilon small → many segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.05},

    # 9. Flat then steep slope, epsilon allows merging → should merge flat part
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 3.0)], "epsilon": 0.5},

    # 10. Random noisy points, epsilon tight → should produce maximum segments
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.9), (3.0, 1.2), (4.0, 1.0)], "epsilon": 0.05},
]
test_cases22 = [
    # 1. Simple linear function, should approximate with a single segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.1},

    # 2. Single sharp change, needs multiple segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.5},

    # 3. Step function, each step may require a segment
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 2), (3, 2), (4, 4)], "epsilon": 0.1},

    # 4. Noisy linear data, epsilon allows smoothing
    {"pw_linear_fx": [(0, 0), (1, 1.1), (2, 1.9), (3, 3.05), (4, 3.95)], "epsilon": 0.2},

    # 5. Flat sections with a spike
    {"pw_linear_fx": [(0, 1), (1, 1), (2, 10), (3, 1), (4, 1)], "epsilon": 0.5},

    # 6. Multiple increasing slopes
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 3), (3, 6), (4, 10)], "epsilon": 0.5},

    # 7. Small epsilon forcing many segments
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.4), (3, 0.9), (4, 1.6)], "epsilon": 0.05},

    # 8. Large epsilon, whole function approximated as one segment
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6)], "epsilon": 10},

    # 9. Alternating peaks and valleys
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)], "epsilon": 0.5},

    # 10. Constant function, should return single segment
    {"pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5)], "epsilon": 0.01},
]

test_cases23 = [
    # 1. Simple straight line, should need only 1 segment
    {"pw_linear_fx": [(0,0), (1,1), (2,2), (3,3)], "epsilon": 0.1},

    # 2. Small "kink" exceeding epsilon, should split into multiple segments
    {"pw_linear_fx": [(0,0), (1,0.05), (2,1), (3,1.05)], "epsilon": 0.01},

    # 3. Horizontal line, tolerance larger than deviations, should return 1 segment
    {"pw_linear_fx": [(0,5), (1,5), (2,5), (3,5)], "epsilon": 0.1},

    # 4. Vertical jump in data, forces split into multiple segments
    {"pw_linear_fx": [(0,0), (1,0), (2,10), (3,10)], "epsilon": 0.5},

    # 5. Repeated points, algorithm should ignore duplicates
    {"pw_linear_fx": [(0,0), (0,0), (1,1), (2,2)], "epsilon": 0.1},

    # 6. Oscillating points around a line, epsilon allows skipping some
    {"pw_linear_fx": [(0,0), (1,0.1), (2,-0.1), (3,0), (4,0.1)], "epsilon": 0.2},

    # 7. Large tolerance, all points fit in a single segment
    {"pw_linear_fx": [(0,0), (1,5), (2,2), (3,7)], "epsilon": 10.0},

    # 8. Points with very small epsilon, each segment should be minimal
    {"pw_linear_fx": [(0,0), (1,0.5), (2,1.5), (3,2.5)], "epsilon": 0.01},

    # 9. Non-monotonic curve, forcing multiple segments
    {"pw_linear_fx": [(0,0), (1,2), (2,1), (3,3), (4,0)], "epsilon": 0.5},

    # 10. Single segment repeated exactly within tolerance
    {"pw_linear_fx": [(0,0), (1,1), (2,2), (3,3), (4,4)], "epsilon": 1.0},
]
test_cases24 = [
    # 1. Perfectly linear — should return 1 segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)],
        "epsilon": 0.1
    },
    # 2. Single small jump — might merge into one segment depending on epsilon
    {
        "pw_linear_fx": [(0, 0), (1, 1.05), (2, 2.0), (3, 3)],
        "epsilon": 0.1
    },
    # 3. Zigzag pattern — forces multiple segments
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.2
    },
    # 4. Plateau (flat region) — should allow merging into fewer segments
    {
        "pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 2)],
        "epsilon": 0.1
    },
    # 5. Large jump exceeding epsilon — cannot merge
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 5)],
        "epsilon": 1.0
    },
    # 6. Small noise within epsilon — should merge into one segment
    {
        "pw_linear_fx": [(0, 0), (1, 0.05), (2, -0.02), (3, 0.03)],
        "epsilon": 0.1
    },
    # 7. Exponentially increasing — likely needs multiple segments
    {
        "pw_linear_fx": [(0, 1), (1, 2), (2, 4), (3, 8), (4, 16)],
        "epsilon": 1.0
    },
    # 8. Alternating small oscillations around a line
    {
        "pw_linear_fx": [(0, 0), (1, 0.05), (2, -0.05), (3, 0.04), (4, -0.04)],
        "epsilon": 0.1
    },
    # 9. Long flat then sharp rise — edge case for segment merging
    {
        "pw_linear_fx": [(0, 2), (1, 2), (2, 2), (3, 10)],
        "epsilon": 0.5
    },
    # 10. Single segment — all points identical
    {
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5)],
        "epsilon": 0.1
    }
]
test_cases25 = [
    # 1. Simple straight line, should be approximated by 1 segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.1},

    # 2. Slight deviation, requires two segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.05},

    # 3. Step function, each step likely becomes its own segment
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)], "epsilon": 0.1},

    # 4. Oscillating data, tests handling of local maxima/minima
    {"pw_linear_fx": [(0, 0), (1, 2), (2, -1), (3, 3), (4, 0)], "epsilon": 1.0},

    # 5. Large flat region followed by a sharp jump
    {"pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 20)], "epsilon": 0.5},

    # 6. Minimal points, only 2 points, should always be 1 segment
    {"pw_linear_fx": [(0, 0), (1, 1)], "epsilon": 0.0},

    # 7. Repeated points, tests zero-length segments
    {"pw_linear_fx": [(0, 1), (0, 1), (1, 2), (2, 3)], "epsilon": 0.1},

    # 8. Linear with small noise, tolerance allows a single segment
    {"pw_linear_fx": [(0, 0), (1, 0.05), (2, -0.02), (3, 0.03)], "epsilon": 0.1},

    # 9. Large data with alternating peaks
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0), (5, 2)], "epsilon": 0.5},

    # 10. Decreasing then increasing, tolerance requires multiple segments
    {"pw_linear_fx": [(0, 5), (1, 3), (2, 1), (3, 2), (4, 4)], "epsilon": 0.5},
]
test_cases26 = [
    # 1. Simple linear, should return 1 segment
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.1},

    # 2. One sharp corner, tolerance too low, should split at corner
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 2), (3, 2)], "epsilon": 0.5},

    # 3. Small oscillation within epsilon, should keep as one segment
    {"pw_linear_fx": [(0, 0), (1, 0.05), (2, -0.03), (3, 0)], "epsilon": 0.1},

    # 4. Large jump exceeding epsilon, requires split
    {"pw_linear_fx": [(0, 1), (1, 2), (2, 10), (3, 11)], "epsilon": 1},

    # 5. Multiple peaks and valleys, check multiple splits
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)], "epsilon": 0.5},

    # 6. Flat segments with tiny deviation, should merge into one
    {"pw_linear_fx": [(0, 1), (1, 1.01), (2, 0.99), (3, 1)], "epsilon": 0.05},

    # 7. Increasing slope just at epsilon, tests boundary condition
    {"pw_linear_fx": [(0, 0), (1, 0.5), (2, 1.0), (3, 1.5)], "epsilon": 0.5},

    # 8. Single segment, epsilon large enough to merge
    {"pw_linear_fx": [(0, 1), (1, 2), (2, 3), (3, 4)], "epsilon": 5},

    # 9. Zig-zag with exact epsilon difference, tests exact tolerance
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 1},

    # 10. Non-uniform spacing in x, large jump in y, requires careful segmenting
    {"pw_linear_fx": [(0, 0), (0.5, 0.1), (2, 5), (5, 5.1)], "epsilon": 0.2}
]

test_cases27 = [
    # 1. Simple linear, should remain a single segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)], "epsilon": 0.1},

    # 2. Slight deviation, epsilon allows merging into one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 2.0)], "epsilon": 0.1},

    # 3. Two distinct slopes, must remain two segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 2.0)], "epsilon": 0.1},

    # 4. Multiple flat sections with small spikes
    {"pw_linear_fx": [(0, 1), (1, 1.1), (2, 1.0), (3, 1.0), (4, 1.2)], "epsilon": 0.15},

    # 5. Oscillating function, small epsilon, should not merge segments
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.05},

    # 6. Large jump exceeding epsilon, must split at jump
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 5)], "epsilon": 1.0},

    # 7. Slowly increasing function, high epsilon allows full merge
    {"pw_linear_fx": [(0, 0), (1, 0.5), (2, 1.0), (3, 1.5)], "epsilon": 1.0},

    # 8. Piecewise linear with exact horizontal segments
    {"pw_linear_fx": [(0, 2), (1, 2), (2, 2), (3, 2)], "epsilon": 0.0},

    # 9. Two peaks within epsilon, should merge into fewer segments
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0.9), (3, 1.1), (4, 0)], "epsilon": 0.2},

    # 10. Increasing then decreasing slope, epsilon smaller than slope change
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 3), (4, 2)], "epsilon": 0.5}
]

test_cases28 = [
    # 1. Perfectly linear, epsilon small (should return 1 segment)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.01},

    # 2. Sharp corner, epsilon small (forces extra segment)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, -1)], "epsilon": 0.1},

    # 3. Flat region followed by slope, epsilon moderate
    {"pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 2), (4, 3)], "epsilon": 0.5},

    # 4. Alternating up and down, tight tolerance
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)], "epsilon": 0.1},

    # 5. Single peak, moderate epsilon
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 5), (3, 1), (4, 0)], "epsilon": 1.0},

    # 6. Increasing slope, large epsilon (can merge multiple segments)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 3), (3, 6), (4, 10)], "epsilon": 2.0},

    # 7. Repeated points, epsilon small
    {"pw_linear_fx": [(0, 0), (0, 0), (1, 1), (2, 2)], "epsilon": 0.01},

    # 8. Negative slope, epsilon moderate
    {"pw_linear_fx": [(0, 5), (1, 4), (2, 2), (3, -1)], "epsilon": 0.5},

    # 9. Small oscillations, very tight tolerance
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, -0.1), (3, 0.2), (4, -0.2)], "epsilon": 0.05},

    # 10. Long flat line, large epsilon
    {"pw_linear_fx": [(0, 10), (1, 10), (2, 10), (3, 10), (4, 10)], "epsilon": 1.0},
]
test_cases29 = [
    # 1. Simple straight line (no approximation needed)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.1},

    # 2. Single large jump (epsilon smaller than jump)
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 10)], "epsilon": 1},

    # 3. Small oscillations around a line (epsilon should allow skipping points)
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, -0.1), (3, 0)], "epsilon": 0.2},

    # 4. Increasing then decreasing slope (convex/concave)
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 5), (3, 3), (4, 0)], "epsilon": 1},

    # 5. All points on a perfect horizontal line
    {"pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5)], "epsilon": 0.01},

    # 6. Single outlier far from line
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 100), (3, 3)], "epsilon": 2},

    # 7. Two identical consecutive points (zero-length segment)
    {"pw_linear_fx": [(0, 0), (1, 1), (1, 1), (2, 2)], "epsilon": 0.1},

    # 8. Points forming a zigzag pattern
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)], "epsilon": 1},

    # 9. Very tight epsilon, must preserve all points
    {"pw_linear_fx": [(0, 0), (1, 1.1), (2, 2.05), (3, 3.02)], "epsilon": 0.01},

    # 10. Large number of points along a noisy sine wave
    {"pw_linear_fx": [(x, round(5 * (0.5 * x + (0.1 * (-1)**x)), 2)) for x in range(10)], "epsilon": 0.2},
]
test_cases30 = [
    # 1. Simple linear increasing, should be approximated by one segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)],
        "epsilon": 0.1
    },

    # 2. Single sharp peak, needs separate segments to meet epsilon
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0)],
        "epsilon": 0.5
    },

    # 3. Flat line, should approximate with one segment easily
    {
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5)],
        "epsilon": 0.01
    },

    # 4. Small oscillations within epsilon, should collapse to one segment
    {
        "pw_linear_fx": [(0, 0), (1, 0.05), (2, -0.03), (3, 0.02)],
        "epsilon": 0.1
    },

    # 5. Small oscillations exceeding epsilon, must separate segments
    {
        "pw_linear_fx": [(0, 0), (1, 0.2), (2, -0.15), (3, 0.25)],
        "epsilon": 0.1
    },

    # 6. Repeated points, should not create extra segments
    {
        "pw_linear_fx": [(0, 0), (1, 0), (1, 0), (2, 1)],
        "epsilon": 0.05
    },

    # 7. Discontinuous jump, each jump must start new segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 10), (3, 11)],
        "epsilon": 0.5
    },

    # 8. Long linear segment with small deviation, epsilon allows full collapse
    {
        "pw_linear_fx": [(0, 0), (2, 2.05), (4, 4.02), (6, 5.95)],
        "epsilon": 0.1
    },

    # 9. Edge case: just at the epsilon limit
    {
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 1.0), (3, 1.5)],
        "epsilon": 0.5
    },

    # 10. Zig-zag pattern, each peak/trough needs its own segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.2
    }
]


























