#30 Sept few-shot prompt with ChatGPT 5 Plus 3:55PM - took 30 minutes
# Test cases for piecewise linear approximation under L∞ norm
test_cases1 = [
    # 1. Flat line (should need only 1 piece regardless of epsilon)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Perfectly linear increasing line (optimal: 1 piece if epsilon=0)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 3. Sharp "V" shape (forces at least 2 pieces for small epsilon)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.1
    },

    # 4. Tolerance allows merging into fewer pieces
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.9), (3.0, 1.05)],
        "epsilon": 0.2
    },

    # 5. Large gap in x-values (algorithm must handle wide domains)
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0), (20.0, 0.0)],
        "epsilon": 1.0
    },

    # 6. Oscillating values (forces multiple segments if epsilon is small)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2
    },

    # 7. Duplicate consecutive x-values (degenerate case)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.5
    },

    # 8. Non-uniform x-spacing (algorithm shouldn’t assume uniform spacing)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (2.0, 4.0), (5.0, 25.0)],
        "epsilon": 1.0
    },

    # 9. Very tight epsilon (forces nearly exact fit)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.1), (3.0, 6.0)],
        "epsilon": 0.05
    },

    # 10. Horizontal with a single outlier (tests robustness with one bad point)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 10.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.5
    },
]
test_cases2 = [
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 10.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 2.0)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 10.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 5.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0), (20.0, 20.0)],
        "epsilon": 0.01
    },
    {
        "pw_linear_fx": [(0.0, 3.0), (1.0, 3.0), (2.0, 3.0), (3.0, 6.0), (4.0, 9.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 3.0), (2.0, 2.0), (3.0, 6.0), (4.0, 5.0), (5.0, 10.0)],
        "epsilon": 1.0
    }
]
test_cases3 = [
    # 1. Flat line, should compress to 1 piece even with small epsilon
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Perfect straight line, exact fit possible with 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 3. Small zig-zag around a line, tolerance decides if 1 or many pieces needed
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.2), (3.0, 0.2), (4.0, -0.2)],
        "epsilon": 0.25
    },

    # 4. Sharp jump discontinuity, must split at jump
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.5
    },

    # 5. Non-uniform spacing of x-values (dense region vs sparse region)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 2.0), (5.0, 10.0)],
        "epsilon": 0.5
    },

    # 6. Piecewise constant with small perturbations (should be merged if ε allows)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.9), (3.0, 1.05)],
        "epsilon": 0.2
    },

    # 7. Alternating slopes forming a “V” shape
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 3.0), (2.0, 1.0), (3.0, 3.0), (4.0, 5.0)],
        "epsilon": 0.5
    },

    # 8. Large ε should collapse everything into one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0), (3.0, 8.0), (4.0, 2.0)],
        "epsilon": 20.0
    },

    # 9. Duplicate y-values but different x spacing
    {
        "pw_linear_fx": [(0.0, 2.0), (2.0, 2.0), (5.0, 2.0), (10.0, 2.0)],
        "epsilon": 0.0
    },

    # 10. Nearly collinear points with small deviation
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.01), (2.0, 3.99), (3.0, 6.02)],
        "epsilon": 0.05
    }
]
test_cases4 = [
    # 1. Perfectly flat line, should compress into a single piece for any ε ≥ 0
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 2. Single sharp peak, small epsilon forces multiple pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 0.0)],
        "epsilon": 0.5
    },

    # 3. Single sharp peak, larger epsilon allows 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 0.0)],
        "epsilon": 3.0
    },

    # 4. Zig-zag pattern, small epsilon requires many pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.1
    },

    # 5. Zig-zag pattern, but large epsilon compresses into 1–2 pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 2.1
    },

    # 6. Non-uniform spacing of x-values
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (5.0, 1.0), (10.0, 2.0)],
        "epsilon": 0.5
    },

    # 7. Duplicate y-values but different slopes, tests flat segments and slopes
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 2.0), (3.0, 2.0), (4.0, 3.0)],
        "epsilon": 0.5
    },

    # 8. High curvature (parabolic-like points)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 1.0
    },

    # 9. Alternating close & far x-values (tests tolerance with irregular spacing)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (5.0, 1.0), (5.1, 2.0), (10.0, 2.0)],
        "epsilon": 0.5
    },

    # 10. Large epsilon trivializes everything (should collapse into 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 5.0), (4.0, -3.0), (6.0, 7.0)],
        "epsilon": 100.0
    }
]
test_cases5 = [
    # 1. Flat line with exact fit (epsilon = 0.0)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.0
    },

    # 2. Perfectly linear increasing sequence (algorithm should compress to 1 segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.1
    },

    # 3. Sharp “V” shape (forces break in middle)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 0.0), (2.0, 5.0)],
        "epsilon": 0.5
    },

    # 4. Small wiggles under tolerance (algorithm should merge into one)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.05), (3.0, 0.05), (4.0, 0.0)],
        "epsilon": 0.2
    },

    # 5. Small wiggles exceeding tolerance (forces multiple pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.6), (3.0, 0.8), (4.0, -1.0)],
        "epsilon": 0.2
    },

    # 6. Duplicate x-values (vertical step, should be infeasible or handled)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.5
    },

    # 7. Large gap in x with small epsilon (forces careful slope calculation)
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 1.0), (20.0, 2.0)],
        "epsilon": 0.1
    },

    # 8. Oscillating sine-like shape (forces multiple pieces even if smooth)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.25
    },

    # 9. Almost linear but one outlier (should need extra piece for outlier)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5
    },

    # 10. High density points on a straight line (algorithm should compress all into one)
    {
        "pw_linear_fx": [(i, 2*i) for i in range(11)],
        "epsilon": 0.0
    }
]
test_cases6 = [
    # 1. Flat horizontal line (should compress to 1 piece regardless of length if ε ≥ 0)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0,
    },

    # 2. Perfectly linear function (all points on y = 2x, should collapse to 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.1,
    },

    # 3. Alternating zig-zag (forces multiple segments for small ε)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2,
    },

    # 4. Duplicate x-values (vertical segment, degenerate case)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0)],
        "epsilon": 0.5,
    },

    # 5. Single large jump (forces break despite large ε)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0)],
        "epsilon": 1.0,
    },

    # 6. Tight tolerance with mild curve (forces multiple cuts)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 2.0), (3.0, 4.5)],
        "epsilon": 0.1,
    },

    # 7. High tolerance absorbs large deviations (should reduce to 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -4.0), (3.0, 6.0)],
        "epsilon": 10.0,
    },

    # 8. Step function-like data (should force multiple small segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.01, 5.0), (2.0, 5.0)],
        "epsilon": 0.2,
    },

    # 9. Very close points (numerical precision stress-test)
    {
        "pw_linear_fx": [(0.0, 0.0), (1e-9, 1e-9), (2e-9, 2e-9), (3e-9, 3e-9)],
        "epsilon": 1e-10,
    },

    # 10. Non-monotonic curve with varying slopes (classic approximation test)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0), (6.0, 5.0)],
        "epsilon": 0.5,
    },
]
test_cases7 = [
    # 1. Flat constant function – should collapse to 1 segment
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 2. Perfectly collinear points – all points on same line
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 3. Sharp V-shape – algorithm must split at the vertex
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.5
    },

    # 4. Small oscillations within tolerance – should compress to 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.0)],
        "epsilon": 0.2
    },

    # 5. Alternating highs and lows – requires many cuts
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.1
    },

    # 6. Horizontal plateau followed by slope – split at change
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 3.0)],
        "epsilon": 0.2
    },

    # 7. Near-vertical jump (large discontinuity) – must insert breakpoint
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0)],
        "epsilon": 0.5
    },

    # 8. Dense points on quadratic curve – may approximate with fewer pieces
    {
        "pw_linear_fx": [(x, x**2) for x in range(6)],  # 0..5
        "epsilon": 1.0
    },

    # 9. Duplicate x-values (degenerate input) – algorithm should handle safely
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0)],
        "epsilon": 0.5
    },

    # 10. Large flat region with tiny spike – should force at least one extra cut
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 1.0
    }
]
test_cases8 = [
    # 1. Constant function – should collapse into 1 segment for any epsilon
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Perfectly linear function – should need only 1 piece even for tiny epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 1e-6
    },

    # 3. Step function (jump discontinuity) – algorithm must insert break at discontinuity
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0)],
        "epsilon": 0.5
    },

    # 4. Zig-zag / alternating peaks – small epsilon forces many segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 0.0)],
        "epsilon": 0.25
    },

    # 5. Zig-zag but relaxed epsilon – algorithm should merge into fewer segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 0.0)],
        "epsilon": 3.0
    },

    # 6. Duplicate x values (vertical segment) – should detect infeasible / degenerate
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 3.0), (1.0, 3.0), (2.0, 4.0)],
        "epsilon": 0.5
    },

    # 7. Nearly linear but small perturbations – tiny epsilon forces multiple segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 1.98), (3.0, 3.05)],
        "epsilon": 0.01
    },

    # 8. Nearly linear but larger epsilon – should merge into single segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 1.98), (3.0, 3.05)],
        "epsilon": 0.1
    },

    # 9. Sharp spike in the middle – must cut around spike
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 10. Long flat regions with one small slope – should reduce to minimal pieces
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.1), (3.0, 5.2), (4.0, 5.2), (5.0, 5.2)],
        "epsilon": 0.2
    }
]
test_cases9 = [
    # 1. Flat constant function (should collapse to 1 piece regardless of epsilon)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Perfect straight line (already linear)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 3. Small oscillations around a line (tests tolerance handling)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.05), (4.0, -0.05)],
        "epsilon": 0.15
    },

    # 4. Sharp corner (forces an extra piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.2
    },

    # 5. Vertical-ish slope changes (steep variations, epsilon small)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 2.0), (1.0, 0.0), (1.5, -2.0), (2.0, 0.0)],
        "epsilon": 0.1
    },

    # 6. Large epsilon should allow collapse to one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, -1.0), (3.0, 4.0), (4.0, 0.0)],
        "epsilon": 5.0
    },

    # 7. Non-uniform spacing in x (check algorithm robustness)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (2.0, 2.0), (10.0, 5.0)],
        "epsilon": 0.5
    },

    # 8. Zig-zag pattern (forces multiple pieces for small epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.25
    },

    # 9. Duplicate x-values with different y (degeneracy test)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.5
    },

    # 10. Long flat followed by spike (should isolate spike as separate piece)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 10.0), (4.0, 1.0)],
        "epsilon": 1.0
    },
]
test_cases10 = [
    # 1. Flat line (should collapse to one piece if epsilon ≥ 0)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 2. Simple V-shape symmetric around x=1
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.5
    },

    # 3. Tight tolerance forces multiple segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.1
    },

    # 4. Large epsilon allows aggressive merging
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.5), (2.0, 3.0), (3.0, 5.0), (4.0, 8.0)],
        "epsilon": 2.0
    },

    # 5. Step function (sharp jumps should not be merged if epsilon is small)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.4
    },

    # 6. Duplicate x values (degenerate vertical case)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.5
    },

    # 7. Nearly collinear points with tiny epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.001), (2.0, 2.002), (3.0, 3.003)],
        "epsilon": 0.0005
    },

    # 8. Increasing then decreasing sequence (hill shape)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 3.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 9. Sparse large x-range with small changes in y
    {
        "pw_linear_fx": [(0.0, 1.0), (10.0, 1.2), (20.0, 1.5)],
        "epsilon": 0.3
    },

    # 10. Zig-zag pattern stresses optimal segmentation
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5
    }
]
test_cases11 = [
    # 1. Flat line (should compress into 1 piece regardless of epsilon)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Single jump discontinuity (forces cut at the jump)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.4
    },

    # 3. Alternating up and down (oscillation)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2
    },

    # 4. Perfect line (all points collinear, no cuts needed)
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (4.0, 4.0), (6.0, 6.0)],
        "epsilon": 0.01
    },

    # 5. Near-collinear but slightly off (tests tolerance handling)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 2.02), (3.0, 3.0)],
        "epsilon": 0.05
    },

    # 6. Very tight tolerance (forces exact fitting, more pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 2.0), (3.0, 1.5), (4.0, 3.0)],
        "epsilon": 0.01
    },

    # 7. Large tolerance (should compress aggressively)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 2.0), (3.0, 1.5), (4.0, 3.0)],
        "epsilon": 2.0
    },

    # 8. Vertical-like slope (tests steep gradients)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (0.2, 20.0), (0.3, 30.0)],
        "epsilon": 0.5
    },

    # 9. Duplicate x-values with different y (degenerate case)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (1.0, 3.0), (2.0, 4.0)],
        "epsilon": 0.5
    },

    # 10. Long flat then spike (tests localized fitting)
    {
        "pw_linear_fx": [(0.0, 1.0), (2.0, 1.0), (4.0, 1.0), (5.0, 10.0)],
        "epsilon": 1.0
    }
]
test_cases12 = [
    # 1. Flat line (should compress to 1 piece if epsilon >= 0)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)], "epsilon": 0.0},

    # 2. Slight slope (can be one piece for larger epsilon)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.0)], "epsilon": 0.2},

    # 3. Sharp V shape (forces multiple pieces at small epsilon)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)], "epsilon": 0.1},

    # 4. Increasing quadratic-like curve (tests tolerance band fitting)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], "epsilon": 0.5},

    # 5. Oscillating small deviations (epsilon needs to absorb noise)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.2), (4.0, 0.0)], "epsilon": 0.2},

    # 6. Large tolerance that allows collapsing all into one line
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 10.0), (3.0, 15.0)], "epsilon": 10.0},

    # 7. Uneven spacing in x (long gaps may hide violations)
    {"pw_linear_fx": [(0.0, 0.0), (5.0, 1.0), (6.0, 5.0), (10.0, 10.0)], "epsilon": 1.0},

    # 8. Nearly collinear but with small deviations (tests piece count optimality)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 2.0), (3.0, 3.05), (4.0, 4.0)], "epsilon": 0.1},

    # 9. Step function shape (flat then jump)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.5},

    # 10. Zig-zag high frequency (forces many cuts if epsilon small)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.2},
]
test_cases13 = [
    # 1. Flat constant function, should be approximable with 1 segment for large ε
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Strictly linear increasing function (already a line) → optimal is 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 3. Sharp jump at one point, requires more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.5
    },

    # 4. Oscillating zig-zag forcing multiple segments if ε is small
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.25
    },

    # 5. Wide tolerance allows collapsing zig-zag into fewer segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 2.5
    },

    # 6. Duplicate y values but spread x, should be approximable with fewer segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0), (4.0, 2.0)],
        "epsilon": 0.2
    },

    # 7. Very steep slope section — tests handling of scaling
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 20.0), (3.0, 21.0)],
        "epsilon": 0.5
    },

    # 8. Duplicate x values (degenerate case, algorithm should detect)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.1
    },

    # 9. Plateau in middle with sharp rise
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 10.0)],
        "epsilon": 0.5
    },

    # 10. Minimal tolerance on nonlinear shape, forces nearly exact segmentation
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0)],
        "epsilon": 0.01
    }
]
test_cases14 = [
    # 1. Flat function (should compress to 1 piece if epsilon >= 0)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 2. Sharp V-shape, low epsilon forces 2 pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 0.1
    },

    # 3. Same as above, but higher epsilon should allow 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 2.0
    },

    # 4. Duplicate x values (vertical step, should be infeasible for some ε)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 2.0)],
        "epsilon": 0.5
    },

    # 5. Large jump between points, tolerance too small forces multiple segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 20.0)],
        "epsilon": 1.0
    },

    # 6. Oscillating pattern (forces many cuts for small epsilon)
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)],
        "epsilon": 0.5
    },

    # 7. Oscillating pattern, but with large epsilon should compress
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)],
        "epsilon": 2.5
    },

    # 8. Nearly collinear points (tests numerical precision)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0001), (2.0, 2.0002), (3.0, 3.0003)],
        "epsilon": 0.001
    },

    # 9. Step function pattern (forces piece at discontinuities)
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 5), (4, 10)],
        "epsilon": 0.5
    },

    # 10. Long flat → slope → flat (tests compression in mixed regimes)
    {
        "pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 4), (4, 7), (5, 7), (6, 7)],
        "epsilon": 1.0
    },
]
test_cases15 = [
    # 1. Flat line (epsilon should allow 1 segment)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Perfectly linear increasing line (should need only 1 segment regardless of epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0
    },

    # 3. Zig-zag small oscillations (tight epsilon forces multiple pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.25
    },

    # 4. Sharp jump (large epsilon may reduce needed pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 5.0
    },

    # 5. Uneven spacing in x-values
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (5.0, 1.5), (10.0, 3.0)],
        "epsilon": 0.5
    },

    # 6. Single spike in the middle
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 7. Dense points along a quadratic curve (epsilon must decide piece count)
    {
        "pw_linear_fx": [(x, x*x) for x in range(6)],  # (0,0), (1,1), (2,4), (3,9), (4,16), (5,25)
        "epsilon": 2.0
    },

    # 8. Horizontal-vertical combination (like step function)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0)],
        "epsilon": 0.1
    },

    # 9. Almost collinear points but with noise (epsilon filters noise)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 2.1), (3.0, 2.95), (4.0, 4.1)],
        "epsilon": 0.2
    },

    # 10. Large epsilon dominates (should collapse to 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0), (3.0, 20.0)],
        "epsilon": 100.0
    }
]
test_cases16 = [
    # 1. Flat line, should need only 1 piece regardless of epsilon
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.1},

    # 2. Single sharp corner, epsilon too small to ignore corner
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)], "epsilon": 0.1},

    # 3. Same corner but larger epsilon allows skipping middle point
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)], "epsilon": 2.1},

    # 4. Monotone increasing line (already linear)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0), (3.0, 7.0)], "epsilon": 0.01},

    # 5. Oscillating pattern forces multiple pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)], "epsilon": 0.4},

    # 6. Duplicate consecutive points (shouldn’t increase piece count)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)], "epsilon": 0.1},

    # 7. Nearly collinear but small epsilon forces extra pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 2.0)], "epsilon": 0.005},

    # 8. Large ε allows collapsing everything into one piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, -2.0), (3.0, 4.0)], "epsilon": 10.0},

    # 9. Non-uniform x spacing, must handle gaps correctly
    {"pw_linear_fx": [(0.0, 1.0), (0.5, 1.5), (5.0, 2.0), (10.0, 3.0)], "epsilon": 0.2},

    # 10. Edge case with minimal 2 points (always 1 piece)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0)], "epsilon": 0.01},
]
test_cases17 = [
    # 1. Simple straight line (should need 1 piece for any ε >= 0)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 2. Horizontal flat line with small noise (tests tolerance handling)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.9), (3.0, 1.05)],
        "epsilon": 0.2
    },

    # 3. Sharp bend (forces at least 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.5
    },

    # 4. Very small ε (forces almost exact fitting)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.1), (3.0, 6.2)],
        "epsilon": 0.05
    },

    # 5. Very large ε (should allow collapsing to 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -3.0), (3.0, 10.0)],
        "epsilon": 20.0
    },

    # 6. Repeated x-values (degenerate case, should be handled)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.5
    },

    # 7. Alternating up and down (forces multiple pieces unless ε is big)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 8. Many points nearly collinear (tests merging ability)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.51), (1.0, 1.02), (1.5, 1.49), (2.0, 2.01)],
        "epsilon": 0.1
    },

    # 9. Step function (flat → sudden jump → flat)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.2
    },

    # 10. Random noisy data (robustness check)
    {
        "pw_linear_fx": [(0.0, 2.0), (0.5, 1.8), (1.0, 2.3), (1.5, 2.1), (2.0, 1.9), (2.5, 2.2)],
        "epsilon": 0.3
    }
]
test_cases18 = [
    # 1. Perfectly linear, epsilon=0 → should need only 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },
    # 2. Small vertical deviation, epsilon too tight → forces multiple pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.0)],
        "epsilon": 0.05
    },
    # 3. Flat then jump → must break exactly at discontinuity
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 10.0)],
        "epsilon": 0.5
    },
    # 4. Zigzag pattern with tight epsilon → requires each segment preserved
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1
    },
    # 5. Zigzag but relaxed epsilon → can collapse into fewer pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.0
    },
    # 6. Duplicate x-values → degenerate edge case (vertical segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 2.0), (1.0, 3.0)],
        "epsilon": 0.5
    },
    # 7. Large scale coordinates with small epsilon → precision test
    {
        "pw_linear_fx": [(0.0, 1e6), (1.0, 1e6 + 1), (2.0, 1e6 + 2)],
        "epsilon": 0.1
    },
    # 8. Many points on same line, epsilon=0 → should compress to 1 piece
    {
        "pw_linear_fx": [(x, 2*x + 1) for x in range(6)],
        "epsilon": 0.0
    },
    # 9. Non-monotonic y-values with wide epsilon → may reduce drastically
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -5.0), (3.0, 5.0), (4.0, -5.0)],
        "epsilon": 6.0
    },
    # 10. Very short segment with noise → epsilon determines sensitivity
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.05), (0.2, -0.05), (0.3, 0.02)],
        "epsilon": 0.01
    },
]
test_cases19 = [
    # 1. Constant function, small epsilon (should compress to 1 segment)
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.1},

    # 2. Strictly linear function, epsilon=0 (algorithm must use only 1 segment)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)], "epsilon": 0.0},

    # 3. Small wiggles within epsilon (should collapse into 1 segment)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.05), (3.0, 0.0)], "epsilon": 0.1},

    # 4. Wiggles exceeding epsilon (requires multiple pieces)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.2), (3.0, 0.0)], "epsilon": 0.1},

    # 5. Flat then jump (tests handling of discontinuity-like behavior)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 5.0)], "epsilon": 0.5},

    # 6. Alternating high/low spikes (forces many segments if epsilon small)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 0.0)], "epsilon": 1.0},

    # 7. Large epsilon tolerance (collapses a nonlinear function into 1 piece)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], "epsilon": 10.0},

    # 8. Uneven x-spacing (tests slope scaling)
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 2.0), (2.0, 3.0), (5.0, 5.0)], "epsilon": 0.5},

    # 9. Non-monotone with plateau (flat region in the middle)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 2.0), (3.0, 0.0)], "epsilon": 0.5},

    # 10. Long sequence with gradual slope changes (tests greedy vs. optimal segmentation)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 2.1), (3.0, 3.05), (4.0, 4.1), (5.0, 5.0)], "epsilon": 0.2},
]
test_cases20 = [
    # 1. Simple flat + slope (baseline example)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },

    # 2. Perfectly linear function (should compress to 1 piece if ε ≥ 0)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 3. Horizontal line with noise within ε (algorithm must merge all)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.1), (2.0, 4.9), (3.0, 5.05)],
        "epsilon": 0.2
    },

    # 4. Sharp “V” shape (forces segmentation at turning point)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 1.0), (2.0, 5.0)],
        "epsilon": 0.5
    },

    # 5. Duplicate x-values (degenerate input, must be handled carefully)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0), (2.0, 5.0)],
        "epsilon": 1.0
    },

    # 6. High oscillation (sin-like, many breakpoints required if ε small)
    {
        "pw_linear_fx": [
            (0.0, 0.0), (0.5, 1.0), (1.0, 0.0),
            (1.5, -1.0), (2.0, 0.0), (2.5, 1.0), (3.0, 0.0)
        ],
        "epsilon": 0.2
    },

    # 7. Long flat then sudden jump
    {
        "pw_linear_fx": [(0.0, 0.0), (5.0, 0.0), (6.0, 10.0)],
        "epsilon": 1.0
    },

    # 8. Very tight ε, must keep all original pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, -0.2)],
        "epsilon": 0.05
    },

    # 9. Large ε tolerance allows heavy compression
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 20.0), (3.0, 30.0)],
        "epsilon": 15.0
    },

    # 10. Non-monotone zigzag pattern
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, -1.0), (3.0, 3.0), (4.0, 0.0)],
        "epsilon": 1.0
    }
]
test_cases21 = [
    # 1. Flat function (should collapse to 1 piece for any epsilon >= 0)
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.0},

    # 2. Perfectly linear increasing line (already linear)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.0},

    # 3. Small noise around linear function (tolerance allows collapse)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.1)], "epsilon": 0.2},

    # 4. Sharp corner (forces a breakpoint)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.5},

    # 5. High-frequency zigzag (forces many pieces if epsilon small)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.25},

    # 6. Same x-values repeated (vertical step — degenerate case)
    {"pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (2.0, 2.0)], "epsilon": 0.1},

    # 7. Large epsilon (should allow collapsing to just one piece)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0), (3.0, 8.0)], "epsilon": 10.0},

    # 8. Very tight epsilon (forces exact fit, max pieces kept)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0), (3.0, 8.0)], "epsilon": 0.0},

    # 9. Long flat segment then sharp jump
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 10.0)], "epsilon": 0.5},

    # 10. Unevenly spaced x-values (tests non-uniform domain)
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (2.0, 2.1), (5.0, 5.0), (10.0, 10.2)], "epsilon": 0.3},
]
test_cases22 = [
    # 1. Flat function, zero tolerance -> should need just 1 segment
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.0},

    # 2. Strict tolerance, non-flat step -> should require a breakpoint at each jump
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)], "epsilon": 0.1},

    # 3. Loose tolerance, jagged function -> approximation should collapse to fewer pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 2.0},

    # 4. Nearly linear with small noise, tight epsilon -> must keep multiple breakpoints
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.05)], "epsilon": 0.05},

    # 5. Piecewise exactly linear, moderate epsilon -> should reduce to 2 segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (4.0, 8.0)], "epsilon": 0.5},

    # 6. Vertical-ish slope change, tiny epsilon -> needs exact segmentation
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 10.0), (1.0, 0.0), (1.5, 10.0)], "epsilon": 0.01},

    # 7. Sparse points with huge ε -> should approximate with one segment
    {"pw_linear_fx": [(0.0, -10.0), (5.0, 30.0), (10.0, -20.0)], "epsilon": 100.0},

    # 8. Oscillating sine-like shape, ε too small -> needs nearly every point
    {"pw_linear_fx": [(x, (-1)**x) for x in range(6)], "epsilon": 0.0},

    # 9. Long flat followed by sharp rise, moderate ε -> must keep breakpoint at rise
    {"pw_linear_fx": [(0.0, 0.0), (2.0, 0.0), (4.0, 0.0), (5.0, 10.0), (6.0, 20.0)], "epsilon": 1.0},

    # 10. Non-uniform spacing, tight ε -> must detect optimal placement with irregular x
    {"pw_linear_fx": [(0.0, 0.0), (0.1, 5.0), (1.0, 10.0), (2.5, 15.0), (5.0, 20.0)], "epsilon": 0.2},
]
test_cases23 = [
    # 1. Flat line (should need only 1 piece for any epsilon)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },
    # 2. Perfectly linear increasing (already one straight line, epsilon irrelevant)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.01
    },
    # 3. Tight tolerance forces exact fit
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0), (3.0, 3.0)],
        "epsilon": 0.0
    },
    # 4. Loose tolerance allows merging into 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0), (3.0, 3.0)],
        "epsilon": 2.0
    },
    # 5. Large jump/discontinuity (forces break despite large epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0
    },
    # 6. Repeated x-values not allowed; near-duplicate x to test robustness
    {
        "pw_linear_fx": [(0.0, 0.0), (0.01, 0.1), (1.0, 1.0), (2.0, 2.1)],
        "epsilon": 0.2
    },
    # 7. Oscillating pattern (forces many small segments if epsilon is small)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.2
    },
    # 8. Oscillating but high epsilon allows compression into fewer pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 2.5
    },
    # 9. Non-uniform x-spacing (tests if algorithm adapts to unequal spacing)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (2.5, 2.0), (10.0, 10.0)],
        "epsilon": 0.5
    },
    # 10. Sharp corner (forces breakpoint exactly at the bend for small epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.1
    }
]
test_cases24 = [
    # 1. Flat line (should collapse to 1 piece for any epsilon ≥ 0)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 2. Increasing straight line (exactly linear, so should use 1 piece for ε=0)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 3. Large jump (algorithm must break at discontinuity if ε too small)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0
    },

    # 4. Small zigzag (tight tolerance forces multiple pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 0.5
    },

    # 5. Same zigzag but looser tolerance (fewer pieces possible)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 2.0
    },

    # 6. Unequally spaced x-values (check handling of non-uniform spacing)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (5.0, 2.0), (10.0, 5.0)],
        "epsilon": 0.5
    },

    # 7. High curvature (quadratic-like data, tight ε forces more segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 0.5
    },

    # 8. High curvature but loose tolerance (algorithm can reduce to 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 5.0
    },

    # 9. Nearly collinear points with tiny noise (algorithm must ignore noise if ε > noise)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 1.99), (3.0, 3.02)],
        "epsilon": 0.05
    },

    # 10. Constant then slope change (tests whether algorithm detects breakpoint)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 2.0), (3.0, 4.0)],
        "epsilon": 0.25
    }
]
test_cases25 = [
    # 1. Simple flat function (constant) – should collapse to 1 piece regardless of epsilon
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.1},

    # 2. Single sharp corner – must decide if one line can cover within epsilon
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)], "epsilon": 1.0},

    # 3. Small oscillations around a line – tolerance may merge into one piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.2), (3.0, 0.1), (4.0, -0.1)], "epsilon": 0.3},

    # 4. Steep slope then flat – algorithm must not waste extra breakpoints
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 10.0), (3.0, 10.0)], "epsilon": 0.5},

    # 5. Equally spaced increasing line – perfectly linear, should always give 1 piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.01},

    # 6. Zigzag pattern – epsilon determines if it can merge or must keep multiple pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)], "epsilon": 0.5},

    # 7. Duplicate consecutive points – test handling redundant vertices
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 5.0)], "epsilon": 0.2},

    # 8. Long flat then sudden jump – forces extra segment
    {"pw_linear_fx": [(0.0, 0.0), (2.0, 0.0), (4.0, 0.0), (5.0, 5.0)], "epsilon": 0.9},

    # 9. Highly nonlinear curve (quadratic samples) – approximation needs multiple pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)], "epsilon": 2.0},

    # 10. Very small epsilon with noisy points – should force algorithm to keep nearly all
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 2.1), (3.0, 2.9), (4.0, 4.2), (5.0, 5.1)], "epsilon": 0.05},
]
test_cases26 = [
    # 1. Flat function (should collapse to one piece for any epsilon >= 0)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },
    # 2. Perfectly linear increasing function (optimal is one piece if epsilon = 0)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },
    # 3. Single sharp corner (forces extra break unless epsilon is large)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.5
    },
    # 4. Alternating up and down (zigzag, stresses piece reduction under epsilon tolerance)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 1.0
    },
    # 5. Very small epsilon, should force all original segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.01
    },
    # 6. Large epsilon, should collapse into one piece even if nonlinear
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0), (3.0, 8.0)],
        "epsilon": 20.0
    },
    # 7. Duplicate x-values (edge case, vertical step – algorithm must handle or reject)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5
    },
    # 8. Large domain with few points (check scaling)
    {
        "pw_linear_fx": [(0.0, 0.0), (50.0, 25.0), (100.0, 50.0)],
        "epsilon": 0.1
    },
    # 9. Nearly collinear points (tiny deviations, should merge unless epsilon is tiny)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 2.0), (3.0, 2.99)],
        "epsilon": 0.05
    },
    # 10. Random noise around a line (epsilon tests robustness to small variations)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.05), (4.0, 3.9)],
        "epsilon": 0.2
    }
]
test_cases27 = [
    # 1. Simple flat line (should compress to one piece if epsilon >= 0)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 2. Small slope, within tolerance (tests whether multiple points collapse to one segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.2
    },

    # 3. Zigzag pattern (forces more segments if epsilon is small)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.25
    },

    # 4. Duplicate x-values not allowed (edge case to check handling of vertical segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5
    },

    # 5. Large jump in y-values (forces split even with large epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0
    },

    # 6. Non-uniform spacing in x (tests whether spacing is respected in approximation)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (2.0, 2.0), (10.0, 3.0)],
        "epsilon": 0.5
    },

    # 7. Minimal case with only two points (should always be 1 segment regardless of epsilon)
    {
        "pw_linear_fx": [(0.0, 1.0), (5.0, 5.0)],
        "epsilon": 0.1
    },

    # 8. Parabolic shape (tests curvature handling vs tolerance)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 2.0
    },

    # 9. Single outlier point (forces decision: keep extra piece or absorb within epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 50.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 5.0
    },

    # 10. Long sequence with repeating pattern (tests scaling and efficiency)
    {
        "pw_linear_fx": [(i, (i % 2)) for i in range(20)],
        "epsilon": 0.4
    }
]
test_cases28 = [
    # 1. Flat line (should compress into 1 segment)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)], "epsilon": 0.0},

    # 2. Small slope within epsilon tolerance
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)], "epsilon": 0.2},

    # 3. Sharp jump at a single point (forces extra piece)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.5},

    # 4. Zigzag pattern (alternating slopes)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.2},

    # 5. Long nearly linear sequence, small perturbations within epsilon
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 2.0), (3.0, 3.1), (4.0, 4.0)], "epsilon": 0.2},

    # 6. Duplicate x-values (vertical jump, should force pieces)
    {"pw_linear_fx": [(0.0, 0.0), (0.0, 2.0), (1.0, 2.0), (2.0, 2.0)], "epsilon": 0.1},

    # 7. Very high tolerance (everything collapses into 1 segment)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -5.0), (3.0, 10.0)], "epsilon": 20.0},

    # 8. Very tight tolerance (every point must be kept)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5)], "epsilon": 0.0},

    # 9. Non-uniform spacing of x values (gaps matter)
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.2), (2.0, 1.5), (5.0, 4.0), (10.0, 10.0)], "epsilon": 0.3},

    # 10. Plateau followed by sharp increase (transition forces breakpoint)
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 10.0), (4.0, 18.0)], "epsilon": 1.0},
]
test_cases29 = [
    # 1. Flat function, should be approximated with 1 piece if epsilon >= 0
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.0},

    # 2. Single sharp jump, epsilon too small to cover with 1 line
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.5},

    # 3. Noisy but within tolerance, should collapse to fewer pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.0)], "epsilon": 0.2},

    # 4. Perfectly linear increasing, epsilon small, still compressible to 1 piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)], "epsilon": 0.0},

    # 5. Zig-zag pattern, requires multiple pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.1},

    # 6. Nearly collinear but with small deviations, test tolerance smoothing
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 1.99), (3.0, 3.0)], "epsilon": 0.05},

    # 7. Vertical steep increase, forces exact segmentation
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.0), (0.5, 10.0), (1.0, 10.0)], "epsilon": 0.1},

    # 8. Long flat followed by slope, should test segmentation decision
    {"pw_linear_fx": [(0.0, 1.0), (2.0, 1.0), (4.0, 1.0), (6.0, 5.0)], "epsilon": 0.5},

    # 9. Tight tolerance, prevents any simplification
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 2.5), (3.0, 2.7)], "epsilon": 0.01},

    # 10. Large epsilon, allows collapsing into a single line
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, -1.0), (3.0, 2.0), (4.0, 0.0)], "epsilon": 5.0},
]
test_cases30 = [
    # 1. Flat function (should collapse to one piece if epsilon >= 0)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 2. Perfectly linear function (no simplification needed)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (4.0, 8.0)],
        "epsilon": 0.1
    },

    # 3. Sharp corner requiring multiple segments (V-shape)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 0.0)],
        "epsilon": 0.5
    },

    # 4. Multiple identical consecutive points
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 5.0)],
        "epsilon": 0.2
    },

    # 5. Highly oscillatory data (forces more pieces if epsilon small)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2
    },

    # 6. Large epsilon tolerance (should collapse everything to 1 segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 10.0), (3.0, 15.0)],
        "epsilon": 20.0
    },

    # 7. Non-monotone but smooth variation
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.5), (3.0, 2.5), (4.0, 2.0)],
        "epsilon": 0.3
    },

    # 8. Long interval with tiny change (tests merging ability)
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.01)],
        "epsilon": 0.05
    },

    # 9. Steep jump that cannot be merged (forces segmentation)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 0.5
    },

    # 10. Random jagged pattern (general robustness test)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.2), (2.0, 0.8), (3.0, 1.5), (4.0, 1.0), (5.0, 2.0)],
        "epsilon": 0.4
    }
]



























