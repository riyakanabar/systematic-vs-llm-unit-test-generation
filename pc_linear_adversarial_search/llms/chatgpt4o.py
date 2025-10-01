#30 Sept few-shot prompt with ChatGPT-4o 4:28PM
test_cases1 = [
    # 1. Flat segments - should merge into one segment
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.0},

    # 2. Perfect line - ε=0 should allow all points to form one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.0},

    # 3. Slight noise - with small ε, should merge all into one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.95), (2.0, 2.1), (3.0, 2.95)], "epsilon": 0.15},

    # 4. Jump discontinuity - needs break even with large ε
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 1.0},

    # 5. Zig-zag pattern - cannot merge even with moderate ε
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)], "epsilon": 0.5},

    # 6. Constant followed by linear increase - tests greedy merging
    {"pw_linear_fx": [(0.0, 3.0), (1.0, 3.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0)], "epsilon": 0.1},

    # 7. Long range linear fit with outlier in middle - should split at outlier
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.5},

    # 8. Almost linear with ε just below needed to merge all
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.1), (3.0, 3.2)], "epsilon": 0.09},

    # 9. Dense but noisy points - tests how well approximation handles tiny ε
    {"pw_linear_fx": [(i * 0.1, i * 0.1 + (-1)**i * 0.01) for i in range(20)], "epsilon": 0.005},

    # 10. Sparse but nonlinear function (e.g., quadratic) - will require multiple segments
    {"pw_linear_fx": [(x, x**2) for x in range(6)], "epsilon": 1.5},
]
test_cases2 = [
    # Test 1: All points lie on a straight line — should return 1 segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)], "epsilon": 0.1},

    # Test 2: Sharp corner — ε too small to ignore the bend, should need 2 segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0)], "epsilon": 0.4},

    # Test 3: Flat segment then steep slope — check if it separates optimally
    {"pw_linear_fx": [(0.0, 1.0), (2.0, 1.0), (3.0, 3.0), (5.0, 7.0)], "epsilon": 0.5},

    # Test 4: High curvature — must require more than 2 segments for tight ε
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, -1.0), (2.0, 0.0)], "epsilon": 0.4},

    # Test 5: Duplicate consecutive points — should not add extra segments
    {"pw_linear_fx": [(0.0, 1.0), (0.0, 1.0), (1.0, 2.0), (2.0, 3.0)], "epsilon": 0.3},

    # Test 6: Vertical-ish near-horizontal near-vertical — captures turning points
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.01), (1.0, 0.0), (1.5, 5.0)], "epsilon": 0.1},

    # Test 7: Tiny ε on non-linear — should need all segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], "epsilon": 0.01},

    # Test 8: ε large enough to fit all into one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.2)], "epsilon": 0.5},

    # Test 9: Flat stairs with tight ε — force one segment per jump
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.1},

    # Test 10: Minimal perturbation on linear trend — test robustness to noise
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.01), (2.0, 3.98), (3.0, 6.02)], "epsilon": 0.05},
]
test_cases3 = [
    # 1. Flat segments: should be approximable by one segment
    {
        "pw_linear_fx": [(0, 2), (1, 2), (2, 2), (3, 2)],
        "epsilon": 0.0
    },
    # 2. Perfect linear with small ε: should still return one piece
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)],
        "epsilon": 0.1
    },
    # 3. Sudden jump: should require a new piece
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 5), (4, 5)],
        "epsilon": 0.4
    },
    # 4. Sharp turn in the middle: not ε-approximable as one segment
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 0), (4, -4)],
        "epsilon": 1.0
    },
    # 5. Close to ε-bound: just below threshold for breaking
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 3), (3, 6)],
        "epsilon": 0.99
    },
    # 6. High curvature, should force splits even with large ε
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, -2), (3, 2), (4, -2)],
        "epsilon": 1.5
    },
    # 7. One point just barely breaks linear fit
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 6), (4, 4)],
        "epsilon": 1.9
    },
    # 8. Monotonic but nonlinear shape (convex)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)],
        "epsilon": 2.5
    },
    # 9. Repeating pattern: force algorithm to consider long reuse
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1)],
        "epsilon": 0.6
    },
    # 10. Large x-spacing, high slope region
    {
        "pw_linear_fx": [(0, 0), (10, 50), (20, 100), (30, 0)],
        "epsilon": 5.0
    }
]
test_cases4 = [

    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.0
    },

    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.5
    },

    {
        "pw_linear_fx": [(0.0, 1.0), (2.0, 3.0), (4.0, 5.0), (6.0, 7.0)],
        "epsilon": 0.1
    },

    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.2), (2.0, 2.1), (3.0, 3.05)],
        "epsilon": 0.25
    },

    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.2), (3.0, 0.1), (4.0, -0.1)],
        "epsilon": 0.3
    },

    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 2.5), (2.0, 5.0)],
        "epsilon": 0.2
    },

    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 11.0)],
        "epsilon": 0.4
    },

    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 6.0)],
        "epsilon": 1.1
    },

    {
        "pw_linear_fx": [(0.0, 0.0), (0.01, 1.0), (0.02, 0.0), (0.03, 1.0)],
        "epsilon": 0.9
    },

    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.84), (2.0, 0.91), (3.0, 0.14), (4.0, -0.76)],
        "epsilon": 0.5
    }
]
test_cases5 = [
    # 1. Perfectly linear data — should be reduced to 1 segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)],
        "epsilon": 0.01
    },
    # 2. Piecewise linear with kinks — optimal needs 2 segments
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 1), (3, 2)],
        "epsilon": 0.1
    },
    # 3. Flat steps with sharp jump — tests tolerance control
    {
        "pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 10), (4, 10)],
        "epsilon": 0.5
    },
    # 4. Large ε should allow big segments (1 piece instead of 3)
    {
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 1.2), (3, 2)],
        "epsilon": 1.5
    },
    # 5. Very small ε forces exact fitting — tests tight error margin
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6)],
        "epsilon": 0.0001
    },
    # 6. Random oscillations — tests rejection of overfitting
    {
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, -0.1), (3, 0.05), (4, 0)],
        "epsilon": 0.2
    },
    # 7. Non-uniform spacing in x-values
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (2.5, 2.0), (10.0, 3.0)],
        "epsilon": 0.3
    },
    # 8. Just over the epsilon — tests rejection of nearly valid segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2.01)],  # linear with tiny bump
        "epsilon": 0.5
    },
    # 9. Repeated y-values with a sudden slope
    {
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 10)],
        "epsilon": 0.4
    },
    # 10. Mixed increasing, flat, and decreasing regions
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 2), (4, 2), (5, 1)],
        "epsilon": 0.6
    }
]
test_cases6 = [
    # 1. Flat segments - all y-values same, should fit into 1 segment even for small epsilon
    {
        "pw_linear_fx": [(0, 2), (1, 2), (2, 2), (3, 2)],
        "epsilon": 0.1
    },

    # 2. Perfectly linear - lies exactly on a line y = 2x + 1, should be 1 piece if epsilon = 0
    {
        "pw_linear_fx": [(0, 1), (1, 3), (2, 5), (3, 7)],
        "epsilon": 0.0
    },

    # 3. High curvature - zigzag shape that forces multiple segments
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)],
        "epsilon": 0.5
    },

    # 4. Slight perturbation - slight noise that shouldn't require many pieces if epsilon is large
    {
        "pw_linear_fx": [(0, 1.0), (1, 1.1), (2, 0.9), (3, 1.05)],
        "epsilon": 0.2
    },

    # 5. Breakpoint hiding - one point breaks an otherwise linear segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 10), (3, 3), (4, 4)],
        "epsilon": 0.9
    },

    # 6. Multiple equal slopes but jumps in value – non-continuous linear segments
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 4), (4, 5), (5, 6)],
        "epsilon": 0.5
    },

    # 7. Very large ε should force full compression to 1 segment even if function varies
    {
        "pw_linear_fx": [(0, 0), (1, 10), (2, 20), (3, 15)],
        "epsilon": 20
    },

    # 8. Minimum ε to force optimal segmentation: linear increase but one small bump in middle
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 1.5), (3, 2), (4, 3)],
        "epsilon": 0.4
    },

    # 9. Duplicate x values (should be caught or handled gracefully if input is invalid)
    {
        "pw_linear_fx": [(0, 1), (1, 2), (1, 3), (2, 4)],
        "epsilon": 0.5
    },

    # 10. Dense x-values over short interval, slight curvature
    {
        "pw_linear_fx": [(0, 0), (0.1, 0.01), (0.2, 0.04), (0.3, 0.09), (0.4, 0.16), (0.5, 0.25)],
        "epsilon": 0.02
    },
]
test_cases7 = [
    # 1. Constant function — should be approximated with 1 segment
    {
        'pw_linear_fx': [(0, 2), (1, 2), (2, 2), (3, 2)],
        'epsilon': 0.1
    },

    # 2. Perfect linear function — whole domain should be one segment
    {
        'pw_linear_fx': [(0, 0), (1, 1), (2, 2), (3, 3)],
        'epsilon': 0.0
    },

    # 3. Zigzag pattern — should need more segments even if epsilon is large
    {
        'pw_linear_fx': [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)],
        'epsilon': 0.4
    },

    # 4. Just above epsilon — minimal segment split should be triggered
    {
        'pw_linear_fx': [(0, 0), (1, 0.5), (2, 1.1)],
        'epsilon': 0.5
    },

    # 5. Long flat followed by spike — algorithm must isolate spike
    {
        'pw_linear_fx': [(0, 0), (1, 0), (2, 0), (3, 5), (4, 0)],
        'epsilon': 0.5
    },

    # 6. Non-uniform spacing in x
    {
        'pw_linear_fx': [(0, 0), (0.1, 1), (1.5, 1.5), (5, 5)],
        'epsilon': 0.6
    },

    # 7. Near-linear but slightly off — epsilon determines whether 1 segment suffices
    {
        'pw_linear_fx': [(0, 0), (1, 1.01), (2, 2.02)],
        'epsilon': 0.03
    },

    # 8. Random small oscillations — smooth curve that may be approximated coarsely
    {
        'pw_linear_fx': [(0, 0), (1, 0.1), (2, -0.1), (3, 0.2), (4, 0.05), (5, -0.05)],
        'epsilon': 0.25
    },

    # 9. Minimal input — only 2 points, always one segment
    {
        'pw_linear_fx': [(0, 0), (1, 1)],
        'epsilon': 0.0
    },

    # 10. Vertical jumps are forbidden in linear — must use horizontal spacing
    {
        'pw_linear_fx': [(0, 0), (0.5, 5), (1.0, 0)],
        'epsilon': 2.0
    }
]
test_cases8 = [
    # 1. Perfectly linear function, should return 1 segment for any ε >= 0
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.0},

    # 2. Constant function with noise within epsilon
    {"pw_linear_fx": [(0, 2), (1, 2.1), (2, 1.9), (3, 2.05)], "epsilon": 0.1},

    # 3. Sharp change in slope (corner): should require at least two segments
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 1), (3, 2)], "epsilon": 0.1},

    # 4. Flat segment then steep linear rise
    {"pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 10)], "epsilon": 1.0},

    # 5. Tiny domain with high precision needed
    {"pw_linear_fx": [(0.0, 0.0), (0.0001, 0.0001), (0.0002, 0.0003)], "epsilon": 0.00005},

    # 6. High-frequency noise superimposed on linear trend
    {"pw_linear_fx": [(0, 0), (1, 1.1), (2, 1.9), (3, 3.1), (4, 4.05)], "epsilon": 0.1},

    # 7. Repeated x-values (invalid input or should be rejected or handled)
    {"pw_linear_fx": [(0, 0), (1, 1), (1, 2), (2, 3)], "epsilon": 0.5},

    # 8. Discontinuous jump (testing if approximation crosses discontinuities)
    {"pw_linear_fx": [(0, 1), (1, 1), (2, 10), (3, 10)], "epsilon": 1.0},

    # 9. Zigzag pattern that flattens out
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0), (5, 0)], "epsilon": 1.5},

    # 10. Non-monotonic function with plateaus and dips
    {"pw_linear_fx": [(0, 0), (1, 3), (2, 1), (3, 1), (4, 5), (5, 4)], "epsilon": 0.75}
]
test_cases9 = [
    # 1. Flat region followed by steep slope (tests joining very different slopes)
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 5), (4, 10)],
        "epsilon": 1.0
    },
    # 2. Perfectly linear function, large epsilon (should return 1 segment)
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6), (4, 8)],
        "epsilon": 10.0
    },
    # 3. Piecewise linear with noise just under epsilon
    {
        "pw_linear_fx": [(0, 0), (1, 1.4), (2, 2.9), (3, 4.5), (4, 6.1)],
        "epsilon": 0.6
    },
    # 4. V-shaped sharp turn (ensures algorithm must split at corner)
    {
        "pw_linear_fx": [(0, 5), (1, 2), (2, 0), (3, 2), (4, 5)],
        "epsilon": 1.0
    },
    # 5. Oscillating pattern near epsilon (forces max usage of epsilon)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 1.0
    },
    # 6. Single sharp spike (algorithm should isolate the spike)
    {
        "pw_linear_fx": [(0, 1), (1, 1), (2, 10), (3, 1), (4, 1)],
        "epsilon": 2.0
    },
    # 7. Very close x-values with slight y variation (tests numerical stability)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0001, 0.001), (0.0002, 0.002), (0.0003, 0.0025)],
        "epsilon": 0.0006
    },
    # 8. Random small noise added to linear trend (should be approximated in one segment)
    {
        "pw_linear_fx": [(0, 0), (1, 2.01), (2, 4.0), (3, 6.05), (4, 8.0)],
        "epsilon": 0.1
    },
    # 9. Function that requires all segments to meet epsilon exactly (tight feasibility test)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 3), (3, 6), (4, 10)],
        "epsilon": 0.5
    },
    # 10. Z-shaped path (testing maximum piece-splitting due to direction changes)
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)],
        "epsilon": 0.4
    }
]
test_cases10 = [
    # 1. Flat segments — should be approximable with one segment
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 2. Linearly increasing — exact line, should need one segment for zero epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 3. V-shape — requires break at vertex for small epsilon
    {
        "pw_linear_fx": [(0.0, 3.0), (1.0, 1.0), (2.0, 3.0)],
        "epsilon": 1.0
    },

    # 4. Tiny perturbation in otherwise linear data — test if over-segmentation avoided
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.01), (3.0, 6.0)],
        "epsilon": 0.05
    },

    # 5. Large constant jump — no segment can cover both parts under small epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0
    },

    # 6. High-frequency zigzag within tolerance — should allow one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.4)],
        "epsilon": 1.0
    },

    # 7. Piecewise linear with break exactly at tolerance — edge of feasibility
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0)],
        "epsilon": 0.5
    },

    # 8. Segment with slope change that becomes feasible at higher epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 5.0)],
        "epsilon": 1.5
    },

    # 9. Minimal input — only 2 segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.0
    },

    # 10. Non-uniform spacing — tests algorithm's handling of irregular x
    {
        "pw_linear_fx": [(0.0, 0.0), (0.3, 1.0), (0.8, 3.0), (2.0, 8.0)],
        "epsilon": 0.4
    }
]
test_cases11 = [
    # 1. Flat line: entire segment can be approximated by a single line
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.1},

    # 2. Perfect straight line: no error across all segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.0},

    # 3. Zigzag pattern with tight epsilon
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)], "epsilon": 0.4},

    # 4. Small ε, forces 1 segment per original segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 2.1), (3.0, 3.05)], "epsilon": 0.05},

    # 5. Linear but with one noisy point
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.5},

    # 6. Discontinuous jump within tight epsilon: must split at jump
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.2},

    # 7. Large epsilon allows large segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)], "epsilon": 4.5},

    # 8. Short plateau then steep slope
    {"pw_linear_fx": [(0.0, 1.0), (0.5, 1.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], "epsilon": 1.0},

    # 9. Function with minor noise (ε allows smoothing)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.1), (4.0, 4.2)], "epsilon": 0.3},

    # 10. Extremely sharp curvature, tight epsilon
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 2.0), (1.5, 4.5), (2.0, 8.0)], "epsilon": 0.1}
]
test_cases12 = [
    # 1. Flat line - Should be compressed to 1 segment regardless of number of points
    {
        "pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],
        "epsilon": 0.0
    },

    # 2. Linear ramp - Perfectly linear increasing, should reduce to one segment if exact
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)],
        "epsilon": 0.0
    },

    # 3. Slightly off-linear - should require breakpoints if ε is small
    {
        "pw_linear_fx": [(0, 0), (1, 1.1), (2, 2.1), (3, 3.2)],
        "epsilon": 0.05
    },

    # 4. High curvature in middle - should require extra segment in center
    {
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 4), (3, 5)],
        "epsilon": 0.5
    },

    # 5. Zig-zag oscillation - alternating slopes (forces many breakpoints)
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)],
        "epsilon": 0.5
    },

    # 6. Vertical discontinuity (slope jump) - forces breakpoint
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 10)],
        "epsilon": 0.9
    },

    # 7. Redundant intermediate points - collinear but with noise
    {
        "pw_linear_fx": [(0, 0), (1, 0.05), (2, 0.1), (3, 0.15)],
        "epsilon": 0.1
    },

    # 8. Minimum 2-piece approximation - sudden slope change
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 1), (3, 2)],
        "epsilon": 0.2
    },

    # 9. Small ε, long dataset with slight noise – should preserve all segments
    {
        "pw_linear_fx": [(i, i + (-1)**i * 0.01) for i in range(10)],
        "epsilon": 0.005
    },

    # 10. Constant then linear – test for proper segmentation
    {
        "pw_linear_fx": [(0, 2), (1, 2), (2, 2), (3, 3), (4, 4)],
        "epsilon": 0.2
    }
]
test_cases13 = [
    # 1. Flat region, then steep slope (test breaking after flat)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },

    # 2. Linear data, perfectly within tolerance — should give 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.1
    },

    # 3. Zigzag pattern with small epsilon — should force many breaks
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)],
        "epsilon": 0.1
    },

    # 4. Multiple identical y-values — should collapse into one piece
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # 5. Sudden jump between two points — must break there
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0
    },

    # 6. Just touching the epsilon bound — tests tight optimality
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5
    },

    # 7. Random values near a straight line — ε controls tolerance
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.1), (2.0, 3.0), (3.0, 3.8)],
        "epsilon": 0.2
    },

    # 8. Function with kink at midpoint — cannot merge past kink
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0), (3.0, 1.5)],
        "epsilon": 0.4
    },

    # 9. Dense sampling of a smooth parabola — small ε should need more segments
    {
        "pw_linear_fx": [(x, x**2) for x in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]],
        "epsilon": 0.01
    },

    # 10. Two linear sections with different slopes — must detect slope change
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 5.0), (4.0, 8.0)],
        "epsilon": 0.2
    }
]
test_cases14 = [
    # 1. Constant function: Should be representable with 1 segment for large ε
    {
        "pw_linear_fx": [(0, 2.0), (1, 2.0), (2, 2.0), (3, 2.0)],
        "epsilon": 0.0
    },

    # 2. Perfectly linear function: Single segment should suffice
    {
        "pw_linear_fx": [(0, 1), (1, 3), (2, 5), (3, 7)],
        "epsilon": 0.0
    },

    # 3. Slight deviation within epsilon: Should still give 1 segment
    {
        "pw_linear_fx": [(0, 1), (1, 3.05), (2, 4.95)],
        "epsilon": 0.1
    },

    # 4. Sharp peak in the middle: Forces a breakpoint
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 0), (4, 0)],
        "epsilon": 1.0
    },

    # 5. Data with noise within ε: Algorithm should not overfit noise
    {
        "pw_linear_fx": [(0, 0), (1, 1.02), (2, 1.98), (3, 3.01)],
        "epsilon": 0.05
    },

    # 6. Step function with flat sections: Should break at jumps
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 5), (4, 10)],
        "epsilon": 0.5
    },

    # 7. Zig-zag pattern: Forces breakpoints even with large ε
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2), (4, 0)],
        "epsilon": 0.9
    },

    # 8. Two linear segments joined with small kink
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 1.8), (3, 3)],
        "epsilon": 0.1
    },

    # 9. Very small ε forces piece-per-segment: Algorithm must not merge
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6)],
        "epsilon": 0.001
    },

    # 10. Single interval: Trivial test case
    {
        "pw_linear_fx": [(0, 0), (1, 1)],
        "epsilon": 0.5
    }
]
test_cases15 = [
    # 1. Flat line with small epsilon (should compress to 1 segment)
    {
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5)],
        "epsilon": 0.1
    },

    # 2. Perfect straight line with noise below epsilon
    {
        "pw_linear_fx": [(0, 0), (1, 1.01), (2, 1.99), (3, 3)],
        "epsilon": 0.05
    },

    # 3. Minimal epsilon that forces breaking at every point
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.01
    },

    # 4. Staircase pattern with epsilon allowing skipping intermediate points
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 1), (3, 2), (4, 2), (5, 3)],
        "epsilon": 0.5
    },

    # 5. Zigzag with large epsilon that could compress to 1 segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, -1), (3, 1), (4, -1), (5, 0)],
        "epsilon": 1.5
    },

    # 6. Near-collinear with one high outlier that forces a split
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 10), (3, 3), (4, 4)],
        "epsilon": 0.5
    },

    # 7. All points on a piecewise-linear convex curve with sufficient ε to compress
    {
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 2), (3, 4.5), (4, 8)],
        "epsilon": 1.0
    },

    # 8. Duplicate x-values (should be rejected or handled gracefully)
    {
        "pw_linear_fx": [(0, 1), (1, 2), (1, 2.1), (2, 3)],
        "epsilon": 0.2
    },

    # 9. All y-values the same (constant function), should compress to 1 segment
    {
        "pw_linear_fx": [(0, 7), (1, 7), (2, 7), (3, 7)],
        "epsilon": 0.0
    },

    # 10. Precision test: values slightly beyond ε
    {
        "pw_linear_fx": [(0, 0), (1, 1.0001), (2, 2.0002)],
        "epsilon": 0.00005
    }
]
test_cases16 = [
    # 1. Flat segments with minor deviation within epsilon
    {
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, -0.1), (3, 0.05), (4, 0)],
        "epsilon": 0.2
    },

    # 2. Sharp corner that forces a split
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 5)],
        "epsilon": 1.0
    },

    # 3. Exactly epsilon deviation allowed, corner on the boundary
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2.0), (3, 3.0)],
        "epsilon": 1.0
    },

    # 4. Long flat, then steep linear segment — test merge ability
    {
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.05), (3, 5), (4, 10)],
        "epsilon": 0.5
    },

    # 5. Repeated zig-zag just below epsilon to tempt incorrect merge
    {
        "pw_linear_fx": [(0, 0), (1, 0.9), (2, 0.1), (3, 0.8), (4, 0.2)],
        "epsilon": 1.0
    },

    # 6. Perfect linear function — should give 1 segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)],
        "epsilon": 0.01
    },

    # 7. Discontinuity in values — test that it's not approximated as continuous
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 100), (3, 100)],
        "epsilon": 5.0
    },

    # 8. Vertical jumps (ill-conditioned x-values) — epsilon not helpful
    {
        "pw_linear_fx": [(0, 0), (1e-10, 10), (2e-10, 20)],
        "epsilon": 1.0
    },

    # 9. Constant alternating values at high frequency
    {
        "pw_linear_fx": [(i, 1 if i % 2 == 0 else -1) for i in range(10)],
        "epsilon": 0.9
    },

    # 10. Non-uniform spacing in x with a sharp spike
    {
        "pw_linear_fx": [(0, 0), (0.5, 0.1), (1.5, 0.2), (5.0, 100), (6.0, 100)],
        "epsilon": 1.0
    }
]
test_cases17 = [
    # 1. Flat region + increasing ramp – should merge into fewer segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },

    # 2. All points lie on a straight line – 1 segment should suffice
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },

    # 3. Small ε forces one segment per piece (tight constraint)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, -1)],
        "epsilon": 0.1
    },

    # 4. High ε allows merging a zig-zag into fewer segments
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 1.0
    },

    # 5. Piecewise constant with small bumps – tests merging tolerance
    {
        "pw_linear_fx": [(0, 2), (1, 2.1), (2, 2), (3, 2.05), (4, 2)],
        "epsilon": 0.1
    },

    # 6. Non-uniform spacing – algorithm must handle variable x spacing
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.2), (1.0, 2.0), (5.0, 10.0)],
        "epsilon": 0.3
    },

    # 7. Sudden jump (discontinuity) – must force a new segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 10.0), (3.0, 10.1)],
        "epsilon": 0.2
    },

    # 8. Horizontal line with redundant points – should detect and collapse
    {
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5)],
        "epsilon": 0.0
    },

    # 9. Single peak – test if peak forces correct segment boundary
    {
        "pw_linear_fx": [(0, 0), (1, 5), (2, 0)],
        "epsilon": 1.0
    },

    # 10. Long sequence with identical slopes but varying spacing – test greedy merge
    {
        "pw_linear_fx": [(0, 0), (1, 1), (3, 3), (6, 6), (10, 10)],
        "epsilon": 0.01
    }
]
test_cases18 = [
    # 1. Flat regions and a slope: Only one break needed
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 10.0)],
        "epsilon": 1.0
    },
    # 2. Slight zig-zag just under epsilon – should be approximated as a single segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.3), (2.0, -0.3), (3.0, 0.2)],
        "epsilon": 0.4
    },
    # 3. Sudden large jumps – must split
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 10.0)],
        "epsilon": 1.0
    },
    # 4. Line segments close to ε from both above and below (tight bound test)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.5), (2.0, 0.0), (3.0, -1.5), (4.0, 0.0)],
        "epsilon": 1.5
    },
    # 5. Exact fit to a known line: should give single segment
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 4.0), (2.0, 6.0), (3.0, 8.0)],
        "epsilon": 0.0
    },
    # 6. Plateau + steep slope + plateau (optimal split into 3)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 9.0), (4.0, 9.0)],
        "epsilon": 0.4
    },
    # 7. Repeating pattern within epsilon – should be approximated as one
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (1.0, -0.1), (1.5, 0.1), (2.0, -0.1)],
        "epsilon": 0.15
    },
    # 8. Very sharp corner (V-shape) – forces segmentation
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.1
    },
    # 9. Horizontal lines with slight noise – noise should not force segmentation
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.1), (2.0, 4.9), (3.0, 5.05), (4.0, 5.0)],
        "epsilon": 0.2
    },
    # 10. Two identical linear regions with a small bump in between – should need 3 pieces if bump exceeds ε
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 2.0), (4.0, 3.0)],
        "epsilon": 0.5
    }
]
test_cases19 = [
    # 1. Minimal input: only two points, zero tolerance → 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 2. Perfectly collinear five points, zero tolerance → 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 3. Slight noise around a straight line, epsilon just above noise → 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.10), (4.0, 3.90)],
        "epsilon": 0.15,
        "expected_segments": 1
    },

    # 4. Two distinct linear stretches with zero tolerance → 2 segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0),
                         (3.0, 3.0), (4.0, 6.0), (5.0, 9.0)],
        "epsilon": 0.0,
        "expected_segments": 2
    },

    # 5. Same two stretches with small random noise, epsilon accommodates noise → 2 segments
    {
        "pw_linear_fx": [(0.0,  0.10), (1.0, -0.05), (2.0,  0.00),
                         (3.0,  3.10), (4.0,  6.10), (5.0,  8.95)],
        "epsilon": 0.20,
        "expected_segments": 2
    },

    # 6. Zigzag pattern forces break at every point when epsilon < amplitude → 4 segments
    {
        "pw_linear_fx": [(0.0,  0.0), (1.0, -1.0), (2.0,  1.0),
                         (3.0, -1.0), (4.0,  1.0)],
        "epsilon": 0.5,
        "expected_segments": 4
    },

    # 7. Single outlier in an otherwise straight set → best optimal split into 2 segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0),
                         (3.0, 5.0), (4.0, 4.0), (5.0, 5.0)],
        "epsilon": 0.5,
        "expected_segments": 2
    },

    # 8. Flat plateau then gentle slope, epsilon too small to merge → 2 segments
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0),
                         (3.0, 2.5), (4.0, 3.0), (5.0, 4.0)],
        "epsilon": 0.40,
        "expected_segments": 2
    },

    # 9. Constant function at zero tolerance → always one flat segment
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 10. Quarter‐sine sampled at four points, small epsilon → must use three pieces
    {
        "pw_linear_fx": [
            (0.0000, 0.0000),
            (0.5236, 0.5000),  # π/6
            (1.0472, 0.8660),  # π/3
            (1.5708, 1.0000)   # π/2
        ],
        "epsilon": 0.05,
        "expected_segments": 3
    }
]
test_cases20 = [
    # 1. Flat segments - constant y values
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },
    # 2. Small ε barely fits the line, so every segment might be needed
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 0.5
    },
    # 3. Linear function with noise within ε — all can be merged
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.0), (3.0, 2.9)],
        "epsilon": 0.2
    },
    # 4. ε too small to merge anything (forces individual segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.1), (3.0, 3.3)],
        "epsilon": 0.01
    },
    # 5. Piecewise linear with exact segments (no noise)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0
    },
    # 6. Discontinuous jump in y values — forces break
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 11.0)],
        "epsilon": 0.4
    },
    # 7. High-frequency oscillation — approximation can't merge much
    {
        "pw_linear_fx": [(i, (-1)**i * 2) for i in range(8)],
        "epsilon": 0.5
    },
    # 8. Exact linear + single outlier
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (2.5, 10.0), (3.0, 6.0)],
        "epsilon": 1.0
    },
    # 9. Duplicate x-values (should handle or raise error)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (1.0, 2.5), (2.0, 3.0)],
        "epsilon": 0.5
    },
    # 10. Constant increase in slope — approximation must track change
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 6.0), (4.0, 10.0)],
        "epsilon": 0.5
    }
]
test_cases21 = [
    # 1. Flat line — Should require 1 piece regardless of epsilon
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.01
    },

    # 2. Sharp corner (V shape) — Should need more segments as ε gets smaller
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.5
    },

    # 3. Small ε on nonlinear trend — Should break into many segments
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0)],
        "epsilon": 0.1
    },

    # 4. Large ε on fluctuating pattern — May merge all into 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.5
    },

    # 5. Discontinuity — Should not interpolate across jumps (testing behavior)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 5.0), (2.0, 5.0)],
        "epsilon": 0.4
    },

    # 6. Redundant points along a line — Algorithm should not add unnecessary breaks
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0)],
        "epsilon": 0.01
    },

    # 7. Zig-zag noise with moderate ε — Tests how aggressively algorithm merges
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.6
    },

    # 8. Rapidly increasing slope — Should detect need for more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0
    },

    # 9. Constant, then sudden slope — Should break at slope change
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 4.0), (4.0, 7.0)],
        "epsilon": 0.5
    },

    # 10. Real-world trend-like data with noise — Verifies piece reduction vs accuracy
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.1), (2.0, 3.9), (3.0, 6.0), (4.0, 8.1)],
        "epsilon": 0.25
    }
]
test_cases22 = [
    # 1. Flat function — should return 1 segment regardless of ε
    {
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5)],
        "epsilon": 0.0
    },

    # 2. Perfectly linear function — should return 1 segment
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6)],
        "epsilon": 0.1
    },

    # 3. Small epsilon requires multiple segments (zigzag pattern)
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.25
    },

    # 4. Function with high curvature — tight ε forces more segments
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)],
        "epsilon": 0.5
    },

    # 5. Increasing step function — detects discontinuities if treated as linear
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 2), (3, 2), (4, 4)],
        "epsilon": 0.4
    },

    # 6. Function with noise — tests robustness to small deviations
    {
        "pw_linear_fx": [(0, 0), (1, 1.05), (2, 2.1), (3, 3.05), (4, 4)],
        "epsilon": 0.1
    },

    # 7. Multiple identical points — tests tolerance of redundancy
    {
        "pw_linear_fx": [(0, 1), (0.5, 1), (1, 1), (1.5, 2), (2, 3)],
        "epsilon": 0.1
    },

    # 8. Long segment with minor deviation — checks greedy vs optimal segmenting
    {
        "pw_linear_fx": [(0, 0), (1, 1.01), (2, 2.02), (3, 3.01), (4, 4)],
        "epsilon": 0.05
    },

    # 9. Very tight epsilon — should force each pair to be separate segments
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 0), (3, 2)],
        "epsilon": 0.01
    },

    # 10. Function with exact piecewise linear structure — tests detection of known optimality
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, -1), (4, 0)],
        "epsilon": 1.0
    },
]
test_cases23 = [
    # 1. Flat followed by sharp bend - tests epsilon transition
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 0.5
    },

    # 2. All points on a straight line - should be approximated with 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (4.0, 4.0), (6.0, 6.0)],
        "epsilon": 0.01
    },

    # 3. Zigzag pattern within epsilon – tests tolerance absorption
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.6
    },

    # 4. Zigzag pattern exceeding epsilon – must break into multiple segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.4
    },

    # 5. Noisy linear data – can be fitted in 1 segment if epsilon is large enough
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.0)],
        "epsilon": 0.15
    },

    # 6. Very close x-values – challenges numerical precision and floating point issues
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0001, 0.1), (0.0002, 0.2), (0.0003, 0.3)],
        "epsilon": 0.01
    },

    # 7. Disjoint flat regions – should produce at least 2 segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.3
    },

    # 8. Rapid slope change – approximation should respect sharp turning point
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 11.0)],
        "epsilon": 0.5
    },

    # 9. All y-values same – flat horizontal line
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0
    },

    # 10. Alternating convex-concave pattern – stress test for greedy algorithms
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0), (3.0, 3.0), (4.0, 2.0), (5.0, 4.0)],
        "epsilon": 0.4
    }
]
test_cases24 = [
    {
        # 1. Constant function: should return 1 segment for any ε ≥ 0
        "pw_linear_fx": [(0, 5.0), (1, 5.0), (2, 5.0), (3, 5.0)],
        "epsilon": 0.0
    },
    {
        # 2. Slight noise added, small ε should still allow 1 segment
        "pw_linear_fx": [(0, 1.0), (1, 1.1), (2, 0.9), (3, 1.05)],
        "epsilon": 0.15
    },
    {
        # 3. Two segments: line break at middle
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 0)],
        "epsilon": 0.25
    },
    {
        # 4. Nearly linear: small deviation, large ε should permit 1 segment
        "pw_linear_fx": [(0, 0), (1, 1.1), (2, 1.9), (3, 3.1)],
        "epsilon": 0.2
    },
    {
        # 5. Piecewise constant with a sharp jump
        "pw_linear_fx": [(0, 1), (1, 1), (2, 5), (3, 5)],
        "epsilon": 1.0
    },
    {
        # 6. Dense points on a curve: forces small segments if ε too tight
        "pw_linear_fx": [(x/10, (x/10)**2) for x in range(11)],  # y = x²
        "epsilon": 0.01
    },
    {
        # 7. Points with large gaps in x, slope changes slowly
        "pw_linear_fx": [(0, 0), (10, 10), (20, 21), (30, 31)],
        "epsilon": 1.5
    },
    {
        # 8. Zigzag function — each bend requires a new segment
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.3
    },
    {
        # 9. Flat with noise — checks tolerance exploitation
        "pw_linear_fx": [(0, 2), (1, 2.3), (2, 1.7), (3, 2.1), (4, 1.9)],
        "epsilon": 0.35
    },
    {
        # 10. Large epsilon allows over-approximation with fewer pieces
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 0), (4, -4), (5, -2)],
        "epsilon": 5.0
    }
]
test_cases25 = [
    # Test 1: All points on a straight line — should be approximated with a single segment
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3)], "epsilon": 0.0},

    # Test 2: Sudden jump between points just outside epsilon — should force segmentation
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 5)], "epsilon": 1.0},

    # Test 3: Slight curve with small epsilon — should result in multiple segments
    {"pw_linear_fx": [(0, 0), (1, 0.5), (2, 2), (3, 4.5)], "epsilon": 0.2},

    # Test 4: Points within ε of linear interpolation — should be grouped
    {"pw_linear_fx": [(0, 0), (1, 1.05), (2, 2.02), (3, 3.0)], "epsilon": 0.1},

    # Test 5: All points with same y-value — constant function should be one segment
    {"pw_linear_fx": [(0, 3), (1, 3), (2, 3), (3, 3)], "epsilon": 0.0},

    # Test 6: Oscillating pattern around a straight line — approximation depends on ε
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.6},

    # Test 7: Tiny ε on large linear slope — forces segmentation due to rounding error
    {"pw_linear_fx": [(0, 0), (0.1, 10), (0.2, 20), (0.3, 30)], "epsilon": 0.05},

    # Test 8: Dense linear sampling with large ε — all points should compress to one
    {"pw_linear_fx": [(x, 2 * x) for x in range(20)], "epsilon": 5.0},

    # Test 9: Almost colinear points with minimal deviation — test tight tolerances
    {"pw_linear_fx": [(0, 0), (1, 1.01), (2, 2.02), (3, 3.03)], "epsilon": 0.01},

    # Test 10: Local peak in middle — requires segmentation if ε < peak height
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 5), (3, 2), (4, 0)], "epsilon": 1.0}
]
test_cases26 = [
    # 1. Flat regions followed by a sharp slope – should use more segments after sharp change
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 10), (4, 20)],
        "epsilon": 1.0
    },

    # 2. Perfect line – can be approximated with one segment regardless of epsilon
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6), (4, 8)],
        "epsilon": 0.1
    },

    # 3. Step function – approximation will need more segments due to vertical jumps
    {
        "pw_linear_fx": [(0, 0), (1, 0), (1.01, 10), (2, 10)],
        "epsilon": 1.0
    },

    # 4. Noise within epsilon band – all points are near a single line
    {
        "pw_linear_fx": [(0, 0), (1, 1.05), (2, 1.9), (3, 3.1), (4, 4.05)],
        "epsilon": 0.2
    },

    # 5. Sharp peak in the middle – algorithm must split around the peak
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 10), (3, 1), (4, 0)],
        "epsilon": 2.0
    },

    # 6. Large flat followed by linear rise – low epsilon should force a cut at the change point
    {
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 6), (4, 7), (5, 8)],
        "epsilon": 0.2
    },

    # 7. Zig-zag pattern – greedy or lazy algorithms may perform suboptimally
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.6
    },

    # 8. Short range, small epsilon – force check of precision edge case
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.01), (0.2, 0.0), (0.3, -0.01), (0.4, 0.0)],
        "epsilon": 0.005
    },

    # 9. Multiple small linear segments that can be merged – test optimal merging
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 2.9), (4, 4)],
        "epsilon": 0.2
    },

    # 10. Repeating noisy pattern – test tolerance handling across multiple segments
    {
        "pw_linear_fx": [(i, (-1) ** i * 0.5 + i) for i in range(10)],
        "epsilon": 0.6
    }
]
test_cases27 = [
    # 1. Flat segments with epsilon = 0 (must preserve all changes)
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "epsilon": 0.0
    },

    # 2. All points lie exactly on one straight line — should return one segment
    {
        "pw_linear_fx": [(0, 0), (1, 2), (2, 4), (3, 6)],
        "epsilon": 0.1
    },

    # 3. Zigzag pattern with low epsilon — should split at every corner
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.2
    },

    # 4. Random noisy line within a large enough epsilon — can be compressed to fewer pieces
    {
        "pw_linear_fx": [(0, 1.1), (1, 1.2), (2, 1.05), (3, 0.9), (4, 1.0)],
        "epsilon": 0.3
    },

    # 5. Sharp jump in middle — algorithm must split exactly at jump
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 10), (3, 10)],
        "epsilon": 1.0
    },

    # 6. Multiple identical y-values (flat steps), tight ε — test breaking between flat steps
    {
        "pw_linear_fx": [(0, 1), (1, 1), (2, 2), (3, 2), (4, 3)],
        "epsilon": 0.4
    },

    # 7. Long linear region interrupted by one small outlier
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 10), (4, 4), (5, 5)],
        "epsilon": 0.5
    },

    # 8. Vertical “cliff” at one point — algorithm must detect that linear segments can't connect
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 100), (3, 101)],
        "epsilon": 1.0
    },

    # 9. Nearly colinear points with epsilon just below the deviation — should force more pieces
    {
        "pw_linear_fx": [(0, 0), (1, 1.01), (2, 2.02), (3, 3.03)],
        "epsilon": 0.01
    },

    # 10. Many close points with large ε — test if algorithm merges everything into one piece
    {
        "pw_linear_fx": [(i, 2 * i + (-1) ** i * 0.1) for i in range(10)],
        "epsilon": 1.0
    },
]
test_cases28 = [
    # 1. Horizontal lines (should be approximable with 1 piece)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1
    },

    # 2. Perfectly linear increasing function (1 segment suffices)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # 3. Zigzag pattern, epsilon allows simplification
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 4. Slight deviation from line: should not allow too much compression
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.05
    },

    # 5. Large vertical jumps — must use more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 10.0), (1.0, 0.0), (1.5, 10.0), (2.0, 0.0)],
        "epsilon": 4.0
    },

    # 6. Very close x-values (small gaps) — precision-sensitive
    {
        "pw_linear_fx": [(0.0, 0.0), (0.01, 0.1), (0.02, 0.2), (0.03, 0.3)],
        "epsilon": 0.01
    },

    # 7. Flat → steep → flat: check multiple behaviors
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 9.0), (4.0, 9.0)],
        "epsilon": 0.5
    },

    # 8. Noisy linear data (should tolerate noise if epsilon is high enough)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.0), (3.0, 3.1), (4.0, 4.2)],
        "epsilon": 0.25
    },

    # 9. Constant y, then sudden jump
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 10.0)],
        "epsilon": 1.0
    },

    # 10. Alternating steep slopes with same endpoints (forces multiple pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 0.0)],
        "epsilon": 0.5
    }
]
test_cases29 = [
    # 1. Flat function, should need only one segment
    {
        "pw_linear_fx": [(0, 2), (1, 2), (2, 2), (3, 2)],
        "epsilon": 0.1
    },

    # 2. V-shape — one piece not enough, two are
    {
        "pw_linear_fx": [(0, 2), (1, 1), (2, 0)],
        "epsilon": 0.5
    },

    # 3. High frequency zigzag, tight epsilon
    {
        "pw_linear_fx": [(i, (-1) ** i) for i in range(10)],
        "epsilon": 0.1
    },

    # 4. Function exactly linear but noisy within epsilon bounds — should compress to 1 segment
    {
        "pw_linear_fx": [(0, 0), (1, 1.01), (2, 2.02), (3, 2.98), (4, 4.01)],
        "epsilon": 0.05
    },

    # 5. Repeated values but with sudden jump — should require break at jump
    {
        "pw_linear_fx": [(0, 1), (1, 1), (2, 1), (3, 10), (4, 10), (5, 10)],
        "epsilon": 0.5
    },

    # 6. Sparse vs. dense x-values — should not affect approximation count
    {
        "pw_linear_fx": [(0, 0), (0.0001, 0.0001), (5, 5)],
        "epsilon": 0.1
    },

    # 7. Sharp peak in middle — must force at least 3 segments
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 0), (4, 0)],
        "epsilon": 1.0
    },

    # 8. Nearly piecewise linear but one point slightly outside — forces extra segment
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3.2), (4, 4)],
        "epsilon": 0.1
    },

    # 9. Perfect sawtooth — should require break at each peak/valley if ε small
    {
        "pw_linear_fx": [(i, (i % 2) * 2) for i in range(11)],
        "epsilon": 0.5
    },

    # 10. Nearly flat but last point jumps — test if algorithm can defer break
    {
        "pw_linear_fx": [(0, 1), (1, 1.05), (2, 1.02), (3, 3)],
        "epsilon": 0.1
    }
]
test_cases30 = [
    # 1. Constant function (should return 1 segment for any ε ≥ 0)
    {"pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.0},

    # 2. Piecewise linear with sharp jump — no approximation possible for small ε
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0)], "epsilon": 0.5},

    # 3. No approximation needed — linear function already within ε
    {"pw_linear_fx": [(0.0, 0.0), (2.0, 4.0), (4.0, 8.0)], "epsilon": 0.1},

    # 4. Slight wiggle just over ε — algorithm must split into more pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5)], "epsilon": 0.4},

    # 5. Near-horizontal line with one spike (should isolate spike if ε small)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 1.0), (4.0, 1.0)], "epsilon": 0.5},

    # 6. Long smooth segment just outside ε — should not merge all points
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0)], "epsilon": 0.05},

    # 7. Optimal segmentation needs skipping mid-points (non-greedy optimality test)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)], "epsilon": 0.15},

    # 8. Large ε — should allow entire data to be approximated in one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 5.0},

    # 9. Zig-zag pattern — algorithm must segment at each turn if ε small
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.4},

    # 10. Non-uniform spacing with sharp bend — tests sensitivity to spacing
    {"pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (1.0, 5.0), (2.0, 10.0)], "epsilon": 1.0},
]
































