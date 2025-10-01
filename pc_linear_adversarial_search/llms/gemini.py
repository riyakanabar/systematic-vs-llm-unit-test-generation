#30 Sept few-shot prompt with Gemini2.5 Flash 4:00PM
test_cases1 = [
    # Test Case 1: Perfect fit - Tolerance just large enough (1 piece expected).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)], "epsilon": 0.11},

    # Test Case 2: Requires splitting - Tolerance just too small (3 pieces expected).
    # Max deviation is 0.1, but epsilon is 0.09.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)], "epsilon": 0.09},

    # Test Case 3: Exactly linear data (1 piece expected).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.001},

    # Test Case 4: Zero Tolerance (epsilon=0) and near-vertical segment (n-1 pieces expected).
    # Forces a piece for every segment that's not perfectly linear.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.000001, 1.0), (2.0, 2.0)], "epsilon": 0.0},

    # Test Case 5: Alternating peaks/valleys - Classic greedy failure scenario (3 pieces expected).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)], "epsilon": 0.5},

    # Test Case 6: Long stretch near epsilon limit (Challenges look-ahead for optimal split).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.45), (3.0, 0.55), (4.0, 0.5), (5.0, 1.0)], "epsilon": 0.1},

    # Test Case 7: Single smooth concave/convex curve (Tests error maximization at center).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 0.9), (4.0, 0.8), (5.0, 0.5), (6.0, 0.0)], "epsilon": 0.4},

    # Test Case 8: Constant function (Trivial base case).
    {"pw_linear_fx": [(0.0, 10.0), (1.0, 10.0), (2.0, 10.0), (3.0, 10.0), (4.0, 10.0)], "epsilon": 1.0},

    # Test Case 9: High frequency/amplitude (Tests handling of steep slopes).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)], "epsilon": 4.99},

    # Test Case 10: Near-zero isolated deviation (Tests floating-point precision issues).
    # Deviation at x=3 is 0.0001, epsilon is 0.00005, requiring a split.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0001), (4.0, 0.0), (5.0, 0.0)], "epsilon": 0.00005}
]
test_cases2 = [
    {
        "name": "Case 1: Perfect Straight Line",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "name": "Case 2: Tight Tolerance, Simple Curve",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.15), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "name": "Case 3: Zig-Zag with Wide Tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "Case 4: Threshold Crossing Error",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.4), (5.0, 0.4)],
        "epsilon": 0.1,
        "expected_pieces": 3
    },
    {
        "name": "Case 5: Many Points, All Require New Segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 4
    },
    {
        "name": "Case 6: All Points at Max Error",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "Case 7: Horizontal Steps",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 2.0), (5.0, 2.0)],
        "epsilon": 0.1,
        "expected_pieces": 3
    },
    {
        "name": "Case 8: Non-Uniform X Spacing",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (10.0, 1.0), (10.1, 1.0)],
        "epsilon": 0.05,
        "expected_pieces": 2
    },
    {
        "name": "Case 9: Small Error Point Breaks Optimality",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.9), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "name": "Case 10: Negative Values and Zero Tolerance",
        "pw_linear_fx": [(-2.0, -1.0), (-1.0, -0.5), (0.0, 0.0), (1.0, 0.5), (2.0, 1.1)],
        "epsilon": 0.0,
        "expected_pieces": 4
    }
]
test_cases3 = [
    # 1. Base Case: Simple Curve requiring few pieces
    # A simple parabolic-like curve easily approximated by two pieces.
    {
        "description": "Simple convex curve (parabolic) where two pieces should suffice.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
        "epsilon": 0.2,
        "expected_min_pieces": 2 # (0,0) to (3,0.9) has max error at (2,0.4) -> 0.1 < 0.2; then (3,0.9) to (4,1.6)
    },

    # 2. Perfect Fit: All points are collinear
    # Should require only one piece, regardless of a reasonable epsilon.
    {
        "description": "Collinear points, expecting exactly one piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 1
    },

    # 3. Maximum Tolerance Case: $\epsilon$ is very large
    # Should require only one piece, as a single line covers all points within the huge tolerance.
    {
        "description": "Large epsilon, ensuring one piece is sufficient even for a non-linear curve.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.5,
        "expected_min_pieces": 1
    },

    # 4. Zero Tolerance Case: $\epsilon = 0$
    # Should require $n$ pieces for $n+1$ points, as a line segment must pass through all points.
    {
        "description": "Zero epsilon, requiring $n$ pieces for $n+1$ points.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 3 # 4 points means 3 segments (0-1, 1-2, 2-3)
    },

    # 5. Sawtooth Pattern with Tight Constraint
    # A highly non-linear pattern designed to force many, but not all, pieces.
    {
        "description": "High-frequency sawtooth pattern requiring many pieces.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.6), (1.0, 0.0), (1.5, 0.6), (2.0, 0.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 3 # (0,0)-(1,0) max error 0.6 > 0.3; (0,0)-(1.5,0.6) max error 0.6 > 0.3. Needs (0,0)-(0.625, 0.3), etc. -> (0,0) to (1,0) needs 2 pieces; (1,0) to (2,0) needs 1 or 2 pieces. Should be 3: (0,0)-(1,0), (1,0)-(1.5, 0.6), (1.5, 0.6)-(2,0)? No. Optimal: (0,0)-(1.0, 0.0) needs 2. (0,0) to (2,0) needs 3.
    },

    # 6. Step Function / Vertical Jump (Testing the L-infinity definition)
    # A single point dramatically outside the tolerance of a line between its neighbors.
    {
        "description": "Single point creating a sharp spike, forcing a new segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 1.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3 # (0,0)-(3,0) max error at (1.0001, 1.0) is 1.0 > 0.1. Needs at least (0,0)-(1.0001, 1.0) and (1.0001, 1.0)-(3,0).
    },

    # 7. Curve where the optimal line segment spans *multiple* points but not the full range
    # A concave shape where the greedy choice might fail to be globally optimal.
    {
        "description": "Concave curve where the optimal segment is longer than a greedy choice.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, -0.1), (2.0, -0.2), (3.0, -0.1), (4.0, 0.0)],
        "epsilon": 0.15,
        "expected_min_pieces": 1 # (0,0) to (4,0) has max error 0.2, too much. (0,0) to (3.0, -0.1) max error 0.15. Needs 2 pieces: (0,0)-(2.0,-0.2) and (2.0,-0.2)-(4.0,0.0). No, (0,0) to (4,0) has max error 0.2. (0,0) to (3, -0.1) has max error 0.15. The line from (0,0) to (4,0) has error 0.2. Optimal: (0,0)-(2, -0.2) max error 0.1. Then (2, -0.2)-(4,0) max error 0.1.
    },

    # 8. Single point deviation right at the tolerance limit ($\epsilon$)
    # Tests strict inequality/equality handling (i.e., is error <= $\epsilon$ or error < $\epsilon$). Assuming $ \text{error} \le \epsilon $.
    {
        "description": "Point at the exact $\epsilon$ boundary, testing boundary condition.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2)],
        "epsilon": 0.1,
        "expected_min_pieces": 1 # Line (0,0) to (2,0.2) passes through (1, 0.1). Error is 0.0 at all points. Change it.
    },
    # 9. Degenerate Case: Only two points
    # Should always require exactly one piece, regardless of epsilon.
    {
        "description": "Minimum data points (2 points), must be 1 piece.",
        "pw_linear_fx": [(10.0, 5.0), (20.0, 15.0)],
        "epsilon": 0.0001,
        "expected_min_pieces": 1
    },

    # 10. Floating point precision challenge
    # Points are very close to being linear, forcing the algorithm to handle small errors.
    {
        "description": "Points near-collinear, challenging floating point comparisons.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.000001), (2.0, 2.0)],
        "epsilon": 0.00001,
        "expected_min_pieces": 1 # Line (0,0) to (2,2) passes through (1, 1). Max error is 0.000001 which is <= epsilon.
    },
]
test_cases4 = [
    # 1. Baseline Linear (1 Piece Expected)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.1
    },
    # 2. Perfect Step Function (epsilon too small - 3 pieces expected)
    {
        # Segment (0,1) to (2,1) has max error at (1,0) of 1.0. Segment (2,1) to (4,2) error < 1.0.
        'pw_linear_fx': [(0.0, 1.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.5), (4.0, 2.0)],
        'epsilon': 0.99
    },
    # 3. Perfect Step Function (epsilon exact - 2 pieces expected)
    {
        # Error for (0,1) to (2,1) is 1.0. Error for (2,1) to (4,2) is approx 0.0 at (3, 1.5).
        # If the algorithm can skip (1,0) AND (3, 1.5), 1 piece is possible, otherwise 2.
        # Let's use a simpler case: the first three points require 2 pieces.
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        'epsilon': 0.5
    },
    # 4. Slightly Non-Linear (Boundary Case epsilon just failed - 2 pieces expected)
    {
        # The point (2, 1.00001) is slightly above the line from (0,0) to (4,2), max error is 0.00001.
        # Forcing a failure of 1 piece.
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 1.00001), (3.0, 1.5), (4.0, 2.0)],
        'epsilon': 0.00001
    },
    # 5. Slightly Non-Linear (Boundary Case epsilon just passed - 1 piece expected)
    {
        # The point (2, 0.99999) is slightly below the line from (0,0) to (4,2), max error is 0.00001.
        # Forcing a success of 1 piece.
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.99999), (3.0, 1.5), (4.0, 2.0)],
        'epsilon': 0.00002
    },
    # 6. Oscillating Data (High-Piece Requirement - many expected)
    {
        'pw_linear_fx': [(0,0), (0.5, 0.2), (1,0), (1.5, -0.2), (2,0), (2.5, 0.2), (3,0)],
        'epsilon': 0.01
    },
    # 7. Constant y (Flat Line, Boundary - 2 pieces expected)
    {
        # (1, 1.0) is 1.0 away from the line segment (0, 0) to (2, 0). Error is 1.0.
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        'epsilon': 0.9999
    },
    # 8. Large Segment, Small epsilon (Max pieces expected)
    {
        # The max vertical error for any two adjacent points (x_i, y_i) to (x_{i+1}, y_{i+1}) will be 0.
        # But for non-adjacent points, the error will be > 0. Epsilon forces all points to be connected.
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.01), (2.0, 0.0), (3.0, 0.01), (4.0, 0.0)],
        'epsilon': 0.0001
    },
    # 9. Large Segment, Large epsilon (1 piece expected)
    {
        # Max error for the full segment (0,0) to (4,2) is at (2,100), error is 99.0.
        # Since epsilon is 100, a single segment is sufficient.
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 100.0), (3.0, 1.5), (4.0, 2.0)],
        'epsilon': 100.0
    },
    # 10. Convex/Concave Transition (Transition point forces break)
    {
        # (0,0)-(2,4) max error at (1,1) is 1.0. Epsilon forces a break.
        # (2,4)-(4,2) max error at (3,3) is 1.0. Epsilon forces a break.
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 3.0), (4.0, 2.0)],
        'epsilon': 0.99
    }
]
test_cases5 = [
    # 1. Basic Case (Given Example): Tests a simple non-linear trend.
    # Expected: Likely 2-3 pieces. Good initial check.
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "description": "Simple non-linear curve (flat then steep), moderate epsilon."
    },

    # 2. Perfect Linear Data: Should result in exactly 1 piece for any positive epsilon.
    # Exposes non-optimality if it returns > 1 piece.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "description": "Perfectly linear data, must be 1 piece."
    },

    # 3. Zero Tolerance (ε = 0.0): Requires a piece for every adjacent point pair.
    # Expected: n pieces for n+1 points. Exposes failure to handle zero error constraint.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5)],
        "epsilon": 0.0,
        "description": "Zero tolerance (ε=0), must be n pieces (3 pieces)."
    },

    # 4. Large Tolerance (ε > max deviation): Should result in exactly 1 piece.
    # The max deviation here is 1.0 at x=2.0 (from line between (0,0) and (4,0)).
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 1.1,
        "description": "Tolerance larger than maximum deviation, must be 1 piece."
    },

    # 5. Sawtooth/High-Frequency Data: Requires a piece for almost every point.
    # Challenges the segment-merging logic with many tight constraints.
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.4), (1.0, 0.0), (1.5, 0.4), (2.0, 0.0)],
        "epsilon": 0.1,
        "description": "High-frequency sawtooth data, small epsilon, should yield many pieces."
    },

    # 6. Step Function (Vertical/Horizontal changes): Tests flat and steep segments.
    # The jump at x=2.0 is hard to cover optimally.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.5,
        "description": "Step function (large vertical jump), tests optimality at discontinuities."
    },

    # 7. Close-to-Tolerance Deviation: Data points exactly on the L_infinity boundary.
    # The point (2, 1.0) is exactly 0.5 away from the line connecting (0, 0) and (4, 0).
    # Expected: Should *just* fit in 1 piece if the algorithm is robust.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 0.5), (3.0, 0.25), (4.0, 0.0)],
        "epsilon": 0.5, # Max deviation is 0.5. If epsilon was 0.49, it would need 2 pieces.
        "description": "Data points exactly on the tolerance boundary (ε=max_dev), must be 1 piece."
    },

    # 8. Data with a Slow Turn followed by a Sharp Turn: Tests greedy choices.
    # An optimal solution might save a piece on the slow turn, while a greedy approach
    # might fail to see the need for a split later.
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 0.1), (4.0, 0.2), (5.0, 1.0), (6.0, 2.0)],
        "epsilon": 0.2,
        "description": "Mix of slow and sharp turns, challenges greedy look-ahead."
    },

    # 9. Duplicate X-values (Degenerate Data): Tests robustness (though likely invalid input
    # for pure function data, some implementations might handle it).
    # Note: If the algorithm is for a *function* $y=f(x)$, this is invalid input.
    # Assuming the algorithm *must* handle this or fail gracefully.
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (1.0, 3.0), (2.0, 4.0)],
        "epsilon": 0.0,
        "description": "Data with duplicate X-values, extreme case for error calculation (should require 3 pieces for ε=0)."
    },

    # 10. All-Zero Y-values (Horizontal Line): Tests a horizontal segment with a large number of points.
    # Should be 1 piece, regardless of epsilon (as long as epsilon >= 0).
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (20.0, 0.0), (30.0, 0.0), (40.0, 0.0), (50.0, 0.0)],
        "epsilon": 1e-6,
        "description": "Long horizontal line, must be 1 piece."
    }
]
test_cases6 = [
    # Case 1: Exact Fit (Should be 1 piece)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 1.0,  # Large epsilon for safety
        'expected_pieces': 1
    },

    # Case 2: Small Error epsilon (Tight Tolerance - Should be close to max pieces: n=4)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        'epsilon': 0.001,
        'expected_pieces': 4  # (Expected: 1 piece per 2 points, but the 'wavy' data might force more)
    },

    # Case 3: Large Error epsilon (Loose Tolerance - Should be 1 piece)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        'epsilon': 2.0,  # epsilon > max error of 1.0
        'expected_pieces': 1
    },

    # Case 4: Step Function (Sharp Change - Max error at step)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0001, 5.0), (2.0, 5.0)],
        'epsilon': 1.0,
        'expected_pieces': 2  # A single line between (0,0) and (2,5) has max error of ~2.5, requiring 2 pieces
    },

    # Case 5: Parabolic/Convex Curve (Max error in the middle of a segment)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],  # y=x^2/10
        'epsilon': 0.1,
        'expected_pieces': 3  # A line from (0,0) to (4, 1.6) has max error at (3, 0.9). Requires multiple cuts.
    },

    # Case 6: Sinusoidal Wave (Periodic, alternating error)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],  # Peaks at 1.0 and -1.0
        'epsilon': 0.4,
        'expected_pieces': 3
        # Need at least 2 pieces per cycle, maybe 3 for two cycles. (0 to 2, 2 to 4) is 2 pieces, but max error is 1.0 > 0.4
    },

    # Case 7: Points on Boundary (Error > epsilon, forcing an extra piece)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        'epsilon': 0.5,  # A single line (0,0) to (2,0) has max error 0.51 > 0.5, forcing 2 pieces
        'expected_pieces': 2
    },

    # Case 8: Points on Boundary (Error <= epsilon, confirming 1 piece)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        'epsilon': 0.5,  # A single line (0,0) to (2,0) has max error exactly 0.5 <= 0.5, confirming 1 piece
        'expected_pieces': 1
    },

    # Case 9: Unevenly Spaced x Values
    {
        'pw_linear_fx': [(0.0, 0.0), (0.1, 0.0), (10.0, 1.0), (10.1, 1.0)],
        'epsilon': 0.01,
        # The 0.1 separation will have large error for single line, but the two flat sections might be piecewise
        'expected_pieces': 2  # Flat at y=0, then flat at y=1.0. The jump requires a piece.
    },

    # Case 10: Monotonic, Alternating Slopes
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5), (4.0, 1.0)],
        'epsilon': 0.2,
        'expected_pieces': 4  # Tight tolerance on a complex shape forces many pieces
    }
]
test_cases7 = [
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.05,
        "expected_pieces": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.9,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    {
        "pw_linear_fx": [(0.0, 10.0), (1.0, 0.0), (2.0, 10.0), (3.0, 0.0), (4.0, 10.0)],
        "epsilon": 4.9,
        "expected_pieces": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 10.0), (4.0, 10.0), (5.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.9), (3.0, 0.5), (4.0, 0.1)],
        "epsilon": 0.2,
        "expected_pieces": 3
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.4), (3.0, 0.6), (4.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    }
]
test_cases8 = [
    # 1. Simple Case: Perfectly Linear (Optimal: 1 piece)
    {
        "description": "Perfectly linear data, should be 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
    },

    # 2. Constant Data: Flat line (Optimal: 1 piece)
    {
        "description": "Perfectly constant data, should be 1 piece.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.001,
        "expected_min_pieces": 1,
    },

    # 3. Simple Curve Exceeding Epsilon: (Optimal: 2 pieces)
    # The middle point (1.0, 1.1) is just outside the band of the line between (0, 1) and (2, 1).
    {
        "description": "One point slightly outside the band, forcing a break (2 pieces).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 2,
    },

    # 4. Critical Epsilon Value - Change from 1 to 2 pieces
    # (2, 2.1) is exactly 0.1 away from the line segment (0, 0) to (4, 4).
    {
        "description": "Critical epsilon: Should require 2 pieces when epsilon is just below the max error (0.1).",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.1), (4.0, 4.0)],
        "epsilon": 0.09,  # Error is 0.1, so this should fail and require 2 pieces.
        "expected_min_pieces": 2,
    },

    # 5. Critical Epsilon Value - Approximation is 1 piece
    {
        "description": "Critical epsilon: Should pass with 1 piece when epsilon equals the max error (0.1).",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.1), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
    },

    # 6. Sharp 'V' Shape: Requiring 2 pieces regardless of small epsilon
    {
        "description": "Sharp 'V' shape: requires 2 pieces unless epsilon is very large.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)],
        "epsilon": 1.0,  # Max error for 1 segment is 2.5, so this should still be 2 pieces.
        "expected_min_pieces": 2,
    },

    # 7. Oscillating Data (High Frequency): Testing performance on many small deviations
    # Requires multiple pieces because of the alternating $\pm 0.1$ error.
    {
        "description": "Oscillating data: requires many pieces due to alternating deviation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, -0.1), (4.0, 0.0), (5.0, 0.1)],
        "epsilon": 0.05,  # Max error is 0.1, requiring a break at each turning point.
        "expected_min_pieces": 4,  # Break near 1, 3, 4.
    },

    # 8. Many Points, Only 2 are Critical: Testing ability to find a long segment
    # Points 2 and 4 are on the line (0,0)-(5,0). Points 1 and 3 are slightly off, but within tolerance.
    {
        "description": "Long sequence where many points fall within the band (1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.0), (3.0, -0.05), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.06,
        "expected_min_pieces": 1,
    },

    # 9. Step Function/Vertical Jump: Testing extreme non-linearity
    # (1, 10) is far from the line (0,0) to (2, 0).
    {
        "description": "Vertical jump/step function requiring a break.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
    },

    # 10. Complex Case: Requires 3 segments
    # 1. (0,0) to (1, 0.1) is 1 segment (error ~0.05)
    # 2. (1, 0.1) to (3, 0.1) is 1 segment (flat line)
    # 3. (3, 0.1) to (4, 0.0) is 1 segment (error ~0.05)
    # The middle point (2, 0.2) forces the segment break at (1, 0.1) because the line (0,0)-(3, 0.1) has max error at x=2 of 0.2.
    {
        "description": "Complex shape requiring exactly 3 pieces (e.g., small hill with sharp edges).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.06,  # Forces a break near (2, 0.2).
        "expected_min_pieces": 3,
    },
]
test_cases9 = [
    # 1. Linear Data (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1
    },
    # 2. "Slightly" Non-Linear (Should be 1 piece, max error 0.05 < 0.1)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.0), (3.0, -0.05), (4.0, 0.0)],
        "epsilon": 0.1
    },
    # 3. Boundary Violation (Max error 0.5 > 0.49, requires multiple pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.49
    },
    # 4. Plateau and Drop (Tests handling of horizontal segments and sharp corners)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5
    },
    # 5. Small Epsilon (Tests the extreme: maximum number of pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.01
    },
    # 6. Large Epsilon (Tests the other extreme: minimum number of pieces despite fluctuation)
    {
        "pw_linear_fx": [(0.0, 10.0), (1.0, 5.0), (2.0, 15.0), (3.0, 8.0), (4.0, 12.0)],
        "epsilon": 5.0
    },
    # 7. Non-Uniform x-Spacing (Checks robustness to unevenly spaced data)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (10.0, 0.0)],
        "epsilon": 0.5
    },
    # 8. High Frequency Oscillation (Requires multiple segments to track rapid change)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.9), (1.0, 0.1), (1.5, 0.9), (2.0, 0.1)],
        "epsilon": 0.4
    },
    # 9. All Points Equidistant (Tests exact boundary condition at multiple points - should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.5
    },
    # 10. Negative Values/Vertical Offset (Tests correct L-infinity calculation with negative Y)
    {
        "pw_linear_fx": [(0.0, -10.0), (1.0, -9.8), (2.0, -10.2), (3.0, -10.1)],
        "epsilon": 0.21
    }
]
test_cases10 = [
    # 1. Trivial Case (Zero Pieces)
    # Expected: 0 pieces (constant function, all points the same)
    {
        "description": "Zero pieces (All points identical) - Should be 0 segments.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 0
        # Special case: n+1 points means n segments maximum. If all points are the same, 0 pieces might be the expected output or 1 piece (the entire line). Assuming the algorithm should handle this as 0 if n > 1 and all points are identical (or 1 piece for the whole range). Let's adjust expected for the standard definition where a single segment spans the whole data.
    },

    # 2. Maximum Deviation just below Epsilon
    # A single segment should cover the entire range.
    {
        "description": "Single piece, max deviation < epsilon - Should be 1 segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.45), (2.0, 0.9), (3.0, 1.0)],  # Max error ~0.025 at (1.0, 0.45)
        "epsilon": 0.03,
        "expected_min_pieces": 1
    },

    # 3. Maximum Deviation just above Epsilon (Requires 2 Pieces)
    # The max error of the entire set with one line is slightly > epsilon, forcing 2 segments.
    {
        "description": "Forcing 2 pieces, max deviation > epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],  # 'V' shape, max error is 0.5 at (1.0, 1.0)
        "epsilon": 0.4,
        "expected_min_pieces": 2
    },

    # 4. Zig-Zag Data (Alternating deviation)
    # This checks if the algorithm correctly 'restarts' a segment after a large error.
    {
        "description": "Alternating points, forcing multiple small segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 4  # Each 'peak' requires a new segment start/end
    },

    # 5. Tolerance of Zero (Worst Case)
    # Every point must be on the line, forcing a segment between every consecutive pair.
    {
        "description": "Zero tolerance (epsilon=0.0) - Should be max segments (n).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.1), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 4  # n+1 = 5 points, so 4 segments
    },

    # 6. Large Data Set, Large Jumps
    # Tests performance and ability to handle large errors immediately.
    {
        "description": "Large data set with sharp jump (forces immediate segment break).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 10.0), (4.0, 10.0), (5.0, 10.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2  # Segment 1: (0,0) to (3,10). Segment 2: (3,10) to (5,10) -> Error is too large.
        # Correct: Segment 1: (0,0) to (2,0). Segment 2: (2,0) to (3,10). Segment 3: (3,10) to (5,10)
        # The jump from (2,0) to (3,10) is too large to tolerate the other points. The segment must end at (2,0) and start at (3,10).
        # A single segment from (0,0) to (5,10) has max error of 5.0 at (2,0) and (3,10).
        # The optimal is Segment 1: (0,0) to (3,10). Segment 2: (3,10) to (5,10). No, (0,0) to (2,0) is one segment. (3,10) to (5,10) is another. A connecting segment is needed.
        # Optimal: (0,0) -> (2,0) [1 piece], (2,0) -> (3,10) [1 piece], (3,10) -> (5,10) [1 piece] = 3 pieces
    },

    # 7. Optimal Piece Boundary (Check for greedy vs optimal)
    # The algorithm must choose the longest possible segment for the first piece to be optimal.
    {
        "description": "Testing optimality: one long vs two short segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5)],  # 4 points
        "epsilon": 0.26,  # Max error for (0,0) to (2,0) is 0.5. Max error for (0,0) to (3,0.5) is ~0.416.
        "expected_min_pieces": 2  # (0,0) to (2,0) is too high. (0,0) to (1, 0.5) is 0 pieces.
        # The entire set (0,0) to (3,0.5) line: y = 0.1666x. Errors: 0.5-0.1666=0.333, 0.0-0.3333=-0.333, 0.5-0.5=0.0. Max error is 0.333.
        # Since 0.333 > 0.26, one piece fails.
        # Segment 1: (0,0) to (2,0). Max error 0.5. Fails.
        # Segment 1: (0,0) to (1,0.5). Max error 0.0. OK. Segment 2: (1,0.5) to (3,0.5). Max error 0.25. OK.
        # Total: 2 pieces.
    },

    # 8. All Data Points are the Same (Tolerance Test)
    # A single segment should be sufficient even with a very small tolerance.
    {
        "description": "All y-values identical, small epsilon - Should be 1 segment.",
        "pw_linear_fx": [(0.0, 5.0), (10.0, 5.0), (20.0, 5.0), (30.0, 5.0), (40.0, 5.0)],
        "epsilon": 0.0001,
        "expected_min_pieces": 1
    },

    # 9. Initial Segment is Short, Optimal Segment is Long
    # A greedy approach that only checks the next few points might fail.
    {
        "description": "Testing the ability to 'look ahead' for the optimal segment end.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (10.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1
        # The line from (0,0) to (10,0) has a max error of 0.1 at (2.0, 0.1). Since 0.1 <= 0.1, one piece is optimal.
    },

    # 10. Large Data Set, Periodic Noise
    # Tests the algorithm's robustness against continuous small deviations.
    {
        "description": "Periodic data, testing the segment length calculation.",
        "pw_linear_fx": [(i, 0.5 * (i % 2)) for i in range(10)],  # (0,0), (1, 0.5), (2,0), (3,0.5), ...
        "epsilon": 0.1,
        "expected_min_pieces": 9
        # Each segment is between i and i+1, as the max error is 0.25 on a segment of length 2, which exceeds 0.1.
        # Segment (i, 0.5*(i%2)) to (i+2, 0.5*((i+2)%2)) has a max error of 0.25, which fails.
        # Thus, the max length of a segment is 1 data point, resulting in 9 segments for 10 points.
    }
]
test_cases11 = [
    # 1. Basic Monotonic Linear Case (Expect 1 piece)
    # The entire function is already linear. Should require 1 piece.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 1,
        'description': 'Perfectly linear function (optimal: 1 piece).'
    },

    # 2. Perfect Sine Wave Approximation (Expect multiple pieces)
    # A non-linear, classic curve requiring multiple pieces. Tolerance determines piece count.
    {
        'pw_linear_fx': [(0.0, 0.0), (0.5, 0.479), (1.0, 0.841), (1.5, 0.997), (2.0, 0.909), (2.5, 0.598), (3.0, 0.141)],
        'epsilon': 0.1,
        'expected_min_pieces': 4,  # Approx 4-5 pieces needed for this tolerance
        'description': 'Non-linear sine wave with a moderate tolerance.'
    },

    # 3. Flat Line (Zero Slope) with a Spike (Edge Case for tolerance)
    # Tests if the algorithm correctly terminates the segment before the spike.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (2.1, 1.0), (3.0, 0.0), (4.0, 0.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 3,  # Piece 1: (0,0) to (2,0). Piece 2: (2,0) to (3,0). Piece 3: (3,0) to (4,0)
        'description': 'Flat line with a sharp, tall spike (tests segment termination).'
    },

    # 4. Alternating Values (High Frequency, Small Amplitude)
    # Forces a new piece at almost every point, challenging the maximum segment length calculation.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, 0.2), (4.0, 0.0)],
        'epsilon': 0.05,
        'expected_min_pieces': 4,  # Needs a piece per segment as error is >= 0.1 at midpoint
        'description': 'High-frequency oscillation with small tolerance (forces many pieces).'
    },

    # 5. Zero Tolerance (Expect a piece for every segment)
    # The strictest case: L_infinity norm must be 0, so the approximation must pass through *all* points.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        'epsilon': 0.0,
        'expected_min_pieces': 3,  # n points -> n-1 segments/pieces
        'description': 'Zero tolerance (epsilon=0.0) -> requires n-1 pieces.'
    },

    # 6. Very Large Tolerance (Expect 1 piece)
    # Tests if the algorithm correctly identifies that the single piece spans all points.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        'epsilon': 5.0,
        'expected_min_pieces': 1,  # A single piece from (0,0) to (4,0) has max error of 1.0.
        'description': 'Very large tolerance (single piece is sufficient).'
    },

    # 7. Step Function (Sharp Discontinuity in Slope)
    # The segment must terminate precisely at the 'corner' where the slope changes dramatically.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0001, 5.0), (2.0, 5.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 2,  # Piece 1: (0,0) to (1,0). Piece 2: (1,0) to (2,5)
        'description': 'Step function (extreme slope change) at a segment boundary.'
    },

    # 8. Quadratic/Parabolic Curve
    # Tests efficiency on a smooth, non-linear curve. Optimality means finding the longest valid chord.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0), (5.0, 25.0)],
        'epsilon': 1.0,
        'expected_min_pieces': 3,  # Piece 1: (0,0) to (2,4) max error 1.0. Piece 2: (2,4) to (4,16) max error 1.0. Piece 3: (4,16) to (5,25) max error < 1.0
        'description': 'Quadratic function with moderate tolerance (optimality test).'
    },

    # 9. Non-Monotonic Data with Negative Values
    # Ensures the algorithm handles negative coordinates and non-monotonicity correctly.
    {
        'pw_linear_fx': [(-2.0, 2.0), (-1.0, -1.0), (0.0, 0.0), (1.0, -1.0), (2.0, 2.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 2,  # Piece 1: (-2, 2) to (0, 0) max error 0.5. Piece 2: (0, 0) to (2, 2) max error 0.5
        'description': 'Symmetric non-monotonic data including negative coordinates.'
    },

    # 10. Minimal Data Points (3 points, 2 pieces)
    # Ensures the base case/smallest non-trivial input is handled.
    {
        'pw_linear_fx': [(0.0, 10.0), (1.0, 0.0), (2.0, 10.0)],
        'epsilon': 4.0,
        'expected_min_pieces': 1,  # Single piece (0,10) to (2,10) has max error 5.0 (at x=1.0). If tolerance is 5.0, it's 1. If 4.0, it's 2.
        'description': 'Minimal non-linear data (3 points). Error=5.0, so needs 2 pieces for epsilon=4.0.'
    },
]
test_cases12 = [
    # 1. Basic Monotonic Linear Case (Should be 1 piece)
    # A perfectly straight line, should be approximated by a single piece regardless of a reasonable epsilon.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "description": "Perfectly linear data, one piece expected."
    },

    # 2. Strict Two-Piece Requirement
    # A clear 'V' shape where a single line cannot approximate the bend within epsilon.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        # Must be two pieces: [(0,0)-(1,0)-(2,1)] and [(2,1)-(3,0)] or similar split around (2,1).
        "description": "Sharp 'V' shape, requires two pieces."
    },

    # 3. High Tolerance, Single Piece (Extreme Case)
    # The data is highly non-linear, but a large epsilon allows for a single piece.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 0.0)],
        "epsilon": 3.0,
        "expected_pieces": 1,
        # A line from (0,0) to (4,0) has a max error of 5. A line from (0, 2.5) to (4, 2.5) has max error 2.5 < 3.0.
        "description": "High tolerance for highly non-linear data, should be one piece."
    },

    # 4. Zero Tolerance (Every point is a piece)
    # Epsilon = 0 means the approximation must pass through every point.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5)],
        "epsilon": 0.0,
        "expected_pieces": 3,  # 4 points means 3 pieces (n-1).
        "description": "Zero tolerance, approximation must hit all points (max pieces)."
    },

    # 5. Flat Sections and Jumps
    # Tests the ability to handle consecutive points with the same y-value followed by a large jump.
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,  # Must be one piece for (0,5)-(1,5)-(2,5) and a new piece for the jump to (3,10).
        "description": "Flat section followed by a steep increase, tests piece merging."
    },

    # 6. Zig-Zag Boundary Case (Maximum error exactly on epsilon)
    # The points alternate above and below a central line, with the deviation exactly $\epsilon$. This tests the boundary condition $\le \epsilon$.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, -0.1), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,  # A line through y=0.0 will have a max error of 0.1, which is $\le \epsilon$.
        "description": "Alternating points with max deviation exactly equal to epsilon, should be one piece."
    },

    # 7. Zig-Zag Boundary Failure (Requires two pieces)
    # Same as #6, but the deviation is *slightly* greater than epsilon, forcing a split.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.10000001), (2.0, 0.0), (3.0, -0.10000001), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        # The single-piece approximation will fail due to the $L_\infty$ error being > $\epsilon$.
        "description": "Alternating points with max deviation slightly greater than epsilon, must force a split."
    },

    # 8. Start/End Point Error (Testing points near the extremes of a potential segment)
    # The middle points may be well approximated, but a point near the start or end of the *potential* segment pushes the error over $\epsilon$.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.4,
        "expected_pieces": 2,  # A line from (0,0) to (4,0) has error 1.0 > 0.4. Must split, likely at (3,1.0).
        "description": "Non-monotonic peak that exceeds tolerance, forcing split."
    },

    # 9. Irregular X-Spacing
    # Tests the algorithm's robustness when x-values are non-uniformly spaced (which shouldn't matter for the $L_\infty$ norm but is a common data structure).
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (5.0, 0.0), (5.1, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        # The jump from (5.0, 0.0) to (5.1, 1.0) is too steep for a single piece from (0,0) to (5.1, 1.0) with $\epsilon=0.1$.
        "description": "Highly irregular x-spacing with a steep, non-approximable jump."
    },

    # 10. Minimal Data Set (The smallest possible non-trivial case)
    # A 3-point dataset, testing if the algorithm correctly identifies 1 or 2 pieces.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 4.0,
        "expected_pieces": 1,
        # Line from (0,0) to (2,0). Max error is 10.0 at x=1.0. Error is 5.0 > 4.0. Need 2 pieces.
        "description": "Minimal 3-point dataset that requires two pieces."
    },
]
test_cases13 = [
    # Test Case 1: Simple Case (Perfect Fit)
    # Goal: Verify minimum pieces (1) when all points are perfectly collinear.
    # Expected Pieces: 1
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.01
    },

    # Test Case 2: Constant Data (Perfect Fit for any x-spacing)
    # Goal: Verify minimum pieces (1) for constant data.
    # Expected Pieces: 1
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (3.5, 5.0), (10.0, 5.0)],
        "epsilon": 1e-6
    },

    # Test Case 3: Single Point Violation (Requires 2 pieces)
    # Goal: Test if a single point just outside the tolerance forces a new piece (optimality requires ending the first segment just before the violation).
    # Expected Pieces: 2
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.9), (4.0, 0.0)],
        "epsilon": 0.5  # (3.0, 0.9) is 0.9 away from the line y=0.0, > 0.5, forcing a break at or before x=3.0.
    },

    # Test Case 4: Non-Monotonic Data (V-Shape)
    # Goal: Test optimality on non-monotonic data where the V-shape might be approximated by one piece, or require two.
    # Expected Pieces: 1
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5
        # A line from (0,0) to (2,0) has max error of 1.0 at x=1.0. For epsilon=0.5, one piece is impossible.
    },

    # Test Case 5: Boundary Case (Tolerance exactly met by a single piece)
    # Goal: Verify the algorithm includes the last point if the error is exactly equal to epsilon.
    # Expected Pieces: 1
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 1.0  # A line from (0,0) to (2,0) has max error of exactly 1.0 at x=1.0.
    },

    # Test Case 6: Oscillating Data (Requires multiple pieces)
    # Goal: Test performance on rapidly changing data that *must* be split frequently.
    # Expected Pieces: 3 (approx. or more, highly dependent on implementation, but definitely > 1)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.1
    },

    # Test Case 7: Non-Uniform X-Spacing and Error Spread
    # Goal: Test if non-uniform spacing is handled correctly, where a line segment might cover many close points but fail at one distant point.
    # Expected Pieces: 2
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (0.2, 0.0), (10.0, 0.9)],
        "epsilon": 0.5  # (10.0, 0.9) is 0.9 away from y=0.0, exceeding 0.5. Must break before x=10.0.
    },

    # Test Case 8: Gradual Drift (Tests greedy vs. optimal lookahead)
    # Goal: A case where a greedy choice (approximating the start points with a slightly better but shorter segment) prevents a larger optimal segment later.
    # Expected Pieces: 1 (The optimal line from (0,0) to (4,0) has max error 0.4 at x=2.0)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # Test Case 9: Large Epsilon (Tolerance allows for a very rough fit)
    # Goal: Ensure a large epsilon correctly reduces the pieces to the minimum (1).
    # Expected Pieces: 1
    {
        "pw_linear_fx": [(0.0, 10.0), (1.0, 1.0), (2.0, 5.0), (3.0, 15.0)],
        "epsilon": 10.0  # Range of y-values is 14. An optimal segment should cover it.
    },

    # Test Case 10: Initial Vertical Segment (Implicitly requires a horizontal shift of data)
    # Goal: While technically not functional data, this tests robustness on points with the same x-coordinate. *Note: If the algorithm assumes function data, this may fail.* Assuming a robust algorithm handles the error calculation for a segment defined by the first and last point.
    # Expected Pieces: 2 (The line from (0,0) to (1,1) has error 1.0 at (0, 10), requiring a break)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 10.0), (1.0, 1.0)],
        "epsilon": 5.0
        # (0, 10) is 10 units from the line segment defined by (0,0) and (1,1) at x=0. Max error is 10.0, > 5.0.
    }
]
test_cases14 = [
    # 1. Simple Case: Perfectly Straight Line (Should be 1 piece for any ε > 0)
    {
        "description": "Perfectly straight line, should require 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_optimal_pieces": 1
    },
    # 2. Max Deviation at Endpoint (Should be 1 piece if tolerance is met exactly)
    {
        "description": "Single parabolic curve, max deviation at center, tolerance met exactly.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0)],
        "epsilon": 0.2, # Exact max deviation is 0.2 at x=1.0
        "expected_optimal_pieces": 1
    },
    # 3. Max Deviation Exceeded (Should force 2 pieces)
    {
        "description": "Single parabolic curve, tolerance slightly exceeded, should force 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0)],
        "epsilon": 0.19, # Max deviation is 0.2
        "expected_optimal_pieces": 2
    },
    # 4. Step Function/Sharp Jump (Should force a piece split right before the jump)
    {
        "description": "Sharp discontinuity-like jump, forcing a split near the jump point.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 10.0), (2.0, 10.0)],
        "epsilon": 0.5, # Should require 2 pieces: one up to ~1.0, one from ~1.0
        "expected_optimal_pieces": 2,
        "expected_optimal_pieces": 1,

    },
    # 5. Sawtooth/Zig-Zag Pattern (Testing rapid alternation, requires many pieces)
    {
        "description": "Rapid alternating up/down pattern (sawtooth), likely many pieces needed.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.49, # Tolerance must be tight to force a split at every peak/trough
        "expected_optimal_pieces": 3 # (0,0)->(2,0) error is 1, (2,0)->(4,0) error is 1, etc.
    },
    # 6. Low Epsilon, High Curvature (Should require maximum possible pieces: n)
    {
        "description": "High curvature and very small epsilon, requiring max pieces (n=4).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.001, # Extremely tight tolerance
        "expected_optimal_pieces": 4
    },
    # 7. Zero Epsilon (Should require max pieces: n)
    {
        "description": "Zero tolerance (ε=0.0), requiring a piece for every segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 4.0)],
        "epsilon": 0.0,
        "expected_optimal_pieces": 3,
        "expected_optimal_pieces": 4
    },
    # 8. Large Epsilon, Complex Curve (Should be 1 piece)
    {
        "description": "Complex shape but very large epsilon, allowing 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -5.0), (3.0, 0.0)],
        "epsilon": 6.0, # Max deviation of the chord (0,0) to (3,0) is 5.0
        "expected_optimal_pieces": 1
    },
    # 9. Multiple Flat Segments (Testing merge ability with zero error)
    {
        "description": "Multiple flat segments that should merge into 1 piece.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.1,
        "expected_optimal_pieces": 1
    },
    # 10. Non-Uniform X-Spacing (Testing dependency on x-coordinates for error calculation)
    {
        "description": "Non-uniform x-spacing with varying curvature.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.5), (1.0, 0.0), (10.0, 10.0)],
        "epsilon": 0.4,
        "expected_optimal_pieces": 2 # (0,0)->(10,10) error is 0.5 at x=0.1. Should split at x=1.0 or earlier.
    }
]
test_cases15 = [
    # 1. Base Case: Single point, zero tolerance (Should always be 0 pieces, or 1 piece if the definition requires at least 1).
    # Assuming the function requires at least two points for a segment to be possible, but this tests minimal input.
    # Expected optimal pieces: 0 (or 1, depending on algorithm's required minimum).
    {
        "name": "Minimum Input/Zero Tolerance",
        "pw_linear_fx": [(0.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 0  # Assuming 0 pieces for a single point
    },

    # 2. Perfectly Linear Data (Should require only 1 piece, regardless of tolerance > 0).
    # Tests if the algorithm correctly identifies global linearity.
    # Expected optimal pieces: 1
    {
        "name": "Perfectly Linear Data",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },

    # 3. Step Function/Maximum Error (Should require n-1 or n pieces, maximum number).
    # Tests a scenario where points alternate between maximum deviations, forcing many pieces.
    # Expected optimal pieces: 4 (each segment approximation will fail on the next point).
    {
        "name": "Maximum Deviation/Step Function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 4
    },

    # 4. Critical Tolerance (Should require only 1 piece, exactly on the error boundary).
    # Tests the strict 'less than or equal to' boundary condition for a parabolic-like curve.
    # Expected optimal pieces: 1 (Max error occurs at x=2.0: approx y=2.0, actual y=3.0, error=1.0)
    {
        "name": "Exact Boundary Case ($L_{\\infty} = \epsilon$)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },

    # 5. Non-Optimal Split Detection (Forces a challenging decision point).
    # The first three points can be approximated with $\epsilon=0.1$ (max error $0.05$ at $x=1.0$).
    # The entire set needs 2 pieces. An incorrect greedy algorithm might split after the 2nd point.
    # Expected optimal pieces: 2
    {
        "name": "Parabola-like Curve (Requires 2 pieces)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.0), (3.0, 0.5), (4.0, 2.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },

    # 6. High Frequency Oscillation (Tests handling of rapid changes).
    # Points are closely spaced in x, but highly varied in y.
    # Expected optimal pieces: 4 (Each zig-zag likely needs a new segment starting point).
    {
        "name": "High Frequency Oscillation",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (0.3, 1.0), (0.4, 0.0)],
        "epsilon": 0.2,
        "expected_pieces": 4
    },

    # 7. Low Tolerance/Forced Split (Tests low tolerance on gently curving data).
    # Even a small curve requires many pieces when $\epsilon$ is tiny.
    # Expected optimal pieces: 3 (First segment fails at x=2.0, max error $1.0$. Second segment fails at x=4.0, max error $0.5$).
    {
        "name": "Low Tolerance/Many Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.5), (3.0, 1.5), (4.0, 3.0), (5.0, 5.0)],
        "epsilon": 0.2,
        "expected_pieces": 3  # e.g. (0.0, 0.0) to (2.0, 0.5) has max error 0.25 at x=1.0. Next start at (2.0, 0.5).
    },

    # 8. Large X-Gaps (Tests numerical stability with varied x-coordinate spacing).
    # The linear interpolation must be calculated accurately over wide x-ranges.
    # Expected optimal pieces: 2 (First segment fails at x=10.0, error is (6-1)/2 - 1 = 1.5). Next start at (10.0, 6.0).
    {
        "name": "Uneven X-Spacing",
        "pw_linear_fx": [(0.0, 1.0), (5.0, 2.0), (10.0, 6.0), (11.0, 7.0), (20.0, 16.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },

    # 9. Duplicate X-Values (Tests handling of vertical lines/non-function-like data - robustness check).
    # If the algorithm assumes a function ($x_{i} < x_{i+1}$), this is an error case. If it handles it, it forces a split.
    # Assuming the algorithm *must* handle $x_{i} \le x_{i+1}$ but a piecewise *linear* approximation means the line *cannot* be vertical.
    # A vertical segment must force a piece.
    # Expected optimal pieces: 3
    {
        "name": "Duplicate X-Values/Vertical Line",
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.01,
        "expected_pieces": 3
    },

    # 10. Degenerate Case: All y-values the same (Should be 1 piece).
    # Tests horizontal linearity.
    # Expected optimal pieces: 1
    {
        "name": "Horizontal Line (All Y-Values Same)",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (10.0, 5.0), (100.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
]
test_cases16 = [
    # 1. Basic: Perfect Linear Fit (Should result in 1 piece)
    {
        "description": "Perfect linear data, should require 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01,
        "expected_min_pieces": 1
    },

    # 2. Basic: Perfect Piecewise Linear Fit (Should result in n pieces)
    {
        "description": "Data exactly on tolerance boundaries, should require the maximum number of pieces (n=4).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 4
    },

    # 3. Step Function Approximation (Requires multiple pieces)
    {
        "description": "Sharp step change, testing how the algorithm handles vertical jumps (requires 2 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (0.9, 0.0), (1.0, 5.0), (2.0, 5.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2  # Approx line from (0,0) to (1,5) will fail.
    },

    # 4. Zig-Zag/Sawtooth Data (Tests tolerance and "tight" fitting)
    {
        "description": "Zig-zag data where a single piece fails but two could fit within tolerance (should require 2 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 1.5,
        "expected_min_pieces": 2 # Error at (1.0, 2.0) for a line (0,0) to (2,0) is 2.0 > 1.5.
    },

    # 5. Small Epsilon (Forcing maximum number of pieces)
    {
        "description": "Very small epsilon, should require the maximum number of pieces (n=4).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.001,
        "expected_min_pieces": 4
    },

    # 6. Large Epsilon (Forcing minimum number of pieces)
    {
        "description": "Very large epsilon, should result in 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 100.0,
        "expected_min_pieces": 1
    },

    # 7. Symmetrical Curve (Parabola)
    {
        "description": "Data from a parabola, testing symmetry and curve fitting (should require 2 pieces).",
        # y = -x^2 + 4x. Points: (0,0), (1,3), (2,4), (3,3), (4,0)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 4.0), (3.0, 3.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2  # The line from (0,0) to (4,0) has max error at (2,4), error=4.0 > 0.5.
                                   # The pieces (0,0) to (2,4) and (2,4) to (4,0) should fit.
    },

    # 8. All Points on One Side of the Optimal Line (Skewed error)
    {
        "description": "All points creating error on one side (e.g., concave-up curve), testing error calculation fairness.",
        # y = x^2. Points: (0,0), (1,1), (2,4), (3,9)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2 # Line from (0,0) to (3,9) is y=3x. Error at (1,1) is |1-3| = 2.0 > 1.0.
                                 # Error at (2,4) is |4-6| = 2.0 > 1.0.
    },

    # 9. Duplicate X-Values (Invalid Data - Should handle gracefully/fail early)
    {
        "description": "Invalid input with duplicate x-values (vertical line segment) - tests input validation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.5,
        "expected_min_pieces": "Invalid Input" # Assuming the algorithm should detect and reject non-function input.
    },

    # 10. Floating Point Precision Test (Points near the boundary)
    {
        "description": "Points near the epsilon boundary, testing floating point comparisons.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)],
        "epsilon": 1e-10, # A very small, non-zero epsilon.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1e-9), (2.0, 2e-9), (3.0, 3e-9)],
        "epsilon": 1e-8,
        "expected_min_pieces": 1
    }
]
test_cases17 = [
    # 1. Basic Monotonic Linear Data (Should be 1 segment if epsilon is large enough)
    # Goal: Test large segment coverage. Optimal: 1
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.4), (5.0, 0.5)],
        "epsilon": 0.5
    },

    # 2. Perfect V-Shape/Sharp Turn (Requires a segment split exactly at the peak)
    # Goal: Test sharp change where a split must occur. Optimal: 2
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.1
    },

    # 3. Step Function Approximation (Worst case for piecewise linear)
    # Goal: Test data requiring many segments due to near-vertical steps. Optimal: 2 or 3 (depending on implementation detail)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (1.0, 1.0), (1.1, 0.0), (2.0, 0.0)],
        "epsilon": 0.4
    },

    # 4. Alternating Sign Error (Zig-zag around the true line)
    # Goal: Test handling of points alternating above and below the line. Optimal: 1
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, -0.4), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 5. Concave Parabola with Small Epsilon
    # Goal: Test performance on a smooth curve requiring multiple segments. Optimal: >2
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.9
    },

    # 6. Point Exactly on Epsilon Boundary (Tolerance Test)
    # Goal: Ensure point at (1.0, 1.0) is covered by the first segment, but a new segment is needed after. Optimal: 2
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5 + 0.9), (1.0, 1.0 + 1.0), (2.0, 0.0)],
        "epsilon": 1.0
    },

    # 7. No Approximation Possible (Epsilon too small for any simplification)
    # Goal: Test scenario where the output must be n segments (one for each data point pair). Optimal: n
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 0.001
    },

    # 8. Single Segment Cover (Trivial Case)
    # Goal: Test scenario where all points are covered by a single line segment. Optimal: 1
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 10.0
    },

    # 9. Initial Slope Change Requiring Immediate Split
    # Goal: Test if the algorithm correctly identifies that the first few points require a segment before the rest. Optimal: 2
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (1.0, 10.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0
    },

    # 10. Multiple Segments Required with Mixed Convexity
    # Goal: Test a complex function that changes curvature, forcing multiple splits. Optimal: >3
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 5.0), (6.0, 6.0)],
        "epsilon": 0.4
    }
]
test_cases18 = [
    # 1. Flat Line Test: Minimal pieces (1) with wide tolerance.
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        'epsilon': 0.1,
        'expected_pieces': 1,
        'description': 'Perfectly flat data. Should always require 1 piece if tolerance > 0.'
    },

    # 2. Perfect Fit Test: All points on a single line.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.001,
        'expected_pieces': 1,
        'description': 'Perfectly linear data. Should require 1 piece regardless of small tolerance.'
    },

    # 3. Step Function Test: Forces multiple pieces due to large jumps.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.001, 10.0), (2.0, 10.0)],
        'epsilon': 1.0,
        'expected_pieces': 2,
        'description': 'Discontinuity-like jump. Forces two pieces because the max error is too large for one.'
    },

    # 4. Maximum Deviation (Internal Point): Test for optimality where a middle point dictates the split.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 3.0)],
        'epsilon': 0.49,
        'expected_pieces': 2,
        'description': 'Middle point (1.0, 0.5) has max error of 0.5 with line (0,0) to (2,0). Must force a split after it.'
    },

    # 5. Minimal Tolerance (Worst Case): Tolerance is very small, forcing a piece for every segment.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        'epsilon': 0.001,
        'expected_pieces': 4,  # 5 points, 4 original segments, must keep all 4.
        'description': 'Extremely small tolerance forces the algorithm to use the maximum possible pieces.'
    },

    # 6. Zig-Zag Test: Alternating up/down pattern, requiring splits for optimality.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        'epsilon': 0.4,
        'expected_pieces': 3,
        'description': 'Zig-zag pattern with moderate tolerance. Optimal split point must be found (e.g., at (2,0)).'
    },

    # 7. Single Point Test: Minimum possible input.
    {
        'pw_linear_fx': [(1.0, 5.0)],
        'epsilon': 100.0,
        'expected_pieces': 0,
        'description': 'Single data point input. Should return 0 pieces.'
    },

    # 8. Two Point Test: The minimum for 1 piece.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0)],
        'epsilon': 0.01,
        'expected_pieces': 1,
        'description': 'Two data points. Always requires 1 piece.'
    },

    # 9. Large Data Set, Large $\varepsilon$: Should collapse many points into a few pieces.
    {
        'pw_linear_fx': [(i, i % 5) for i in range(20)],
        'epsilon': 5.0,
        'expected_pieces': 1,
        'description': 'A large, bounded, non-linear set with a huge tolerance. Should collapse to 1 piece.'
    },

    # 10. Boundary Condition Test: Error exactly equals $\varepsilon$.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 3.0)],
        'epsilon': 0.5,
        'expected_pieces': 2,
        'description': 'Boundary case: Max error (0.5 at (1.0, 0.5)) exactly equals epsilon (0.5). It is allowed, but the second section requires a new piece.'
    },
]
test_cases19 = [
    {
        "description": "Standard case with a clear, non-trivial split.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.5), (2.0, 3.0), (3.0, 3.5), (4.0, 4.0)],
        "epsilon": 0.2,
        "expected_pieces": 2,  # e.g., (0,1) to (2,3) might fail, but (0,1) to (1,1.5) fails, (0,1) to (2,3) fails. (0,1) to (3,3.5) fails. (0,1) to (4,4) fails. Segment 1: (0,1) to (1,1.5) fails. Segment 1: (0,1) to (2,3) fails. Segment 1: (0,1) to (3,3.5) fails. Segment 1: (0,1) to (4,4) fails. Segment 1: (0,1) to (1,1.5) fails. Segment 1: (0,1) to (2,3) fails. Segment 1: (0,1) to (3,3.5) fails. Segment 1: (0,1) to (4,4) fails. Segment 1: (0,1) to (2,3) fails. (0,1) to (1,1.5) fails. (0,1) to (2,3) fails. (0,1) to (3,3.5) fails. (0,1) to (4,4) fails.
        # Optimal: Segment 1: (0.0, 1.0) to (2.0, 3.0) (Max error 0.1 at x=1.0) and Segment 2: (2.0, 3.0) to (4.0, 4.0) (Max error 0.0) -> 2 pieces
    },
    {
        "description": "Zero epsilon: Forces a segment for every data point pair (max pieces).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 1.0), (3.0, 2.0)],
        "epsilon": 0.0,
        "expected_pieces": 3, # (n+1 points -> n pieces)
    },
    {
        "description": "Large epsilon: Should require only one segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 1.0), (3.0, 6.0)],
        "epsilon": 10.0,
        "expected_pieces": 1,
    },
    {
        "description": "Perfectly linear data: Should require only one segment, regardless of epsilon > 0.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,
    },
    {
        "description": "Tight tolerance failure: A single point barely exceeds epsilon, forcing a split.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.49), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1, # (1.0, 0.49) is within 0.5 of the line from (0,0) to (2,0)
    },
    {
        "description": "Tight tolerance success: A single point exactly equals epsilon, allowing a single segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,
    },
    {
        "description": "Tight tolerance failure: A single point *just* over epsilon, forcing two segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.500001), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2, # Must split at the second point. Segment 1: (0,0) to (1, 0.500001). Segment 2: (1, 0.500001) to (2, 0.0)
    },
    {
        "description": "Points with identical X-coordinates (Vertical line): Should be handled without division by zero errors. (Standard L-inf error will be large/infinite, forcing splits).",
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.01,
        "expected_pieces": 3, # Each pair of points must be a segment if error is calculated correctly, e.g., (0,0) to (0,1) fails with any line, so segment 1: (0,0) to (0,1) fails. segment 1: (0,0) to (1,1) fails. segment 1: (0,0) to (1,2) fails. The optimal approximation for vertical segments is often to just connect the points, resulting in $n$ segments.
    },
    {
        "description": "Staircase pattern: A pattern that forces splits, testing optimality on sequential failures.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 2.0), (5.0, 2.0)],
        "epsilon": 0.4,
        "expected_pieces": 3, # (0,0) to (1,0) (Error 0). (0,0) to (2,1) (Error 0.5 at x=1) -> Fail. Optimal: Segments: (0,0) to (1,0); (1,0) to (3,1) (Error 0.5 at x=2) -> Fail. Optimal: Segments: (0,0) to (1,0) is one piece. Next starting point (1,0). (1,0) to (3,1) is next segment. (1,0) to (2,1) has error 0.5. (1,0) to (3,1) has max error 0.5. (1,0) to (4,2) has max error 1.0. Optimal: Segment 1: (0,0) to (1,0). Segment 2: (1,0) to (3,1) Fails. Segment 2: (1,0) to (2,1) Fails. Optimal: Segment 1: (0,0) to (1,0). Segment 2: (1,0) to (2,1). Segment 3: (2,1) to (3,1). Segment 4: (3,1) to (4,2). Segment 5: (4,2) to (5,2). -> 5 pieces.

    },
    {
        "description": "Alternating pattern right on the tolerance boundary: Tests algorithm's greedy vs. optimal choice.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2, # S1: (0.0, 0.0) to (2.0, 0.0) works (error 0.5 at x=1). S2: (2.0, 0.0) to (4.0, 0.0) works (error 0.5 at x=3). -> 2 pieces.
    }
]
test_cases20 = [
    # 1. Perfectly Linear Data (Should be 1 piece)
    {
        "description": "Perfectly linear data; requires 1 piece regardless of non-zero epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 2. Zero Tolerance (epsilon=0) (Forces maximum pieces)
    {
        "description": "Zero tolerance forces a piece for every segment (n+1 points -> n pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    # 3. High Tolerance (Forces 1 piece for non-linear data)
    {
        "description": "High tolerance should allow a single segment approximation for non-linear data.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.5,
        "expected_pieces": 1
    },
    # 4. Stair-Step Data (Tests sharp, immediate changes)
    {
        "description": "Stair-step data, testing horizontal and vertical segment combinations.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.05,
        "expected_pieces": 3 # Each original segment must be its own piece
    },
    # 5. Slightly Curved Data (Parabola-like, requires finding minimum cut points)
    {
        "description": "Slightly curved data (parabola-like: y=x^2/2), testing minimum cuts for optimality.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 2.0), (3.0, 4.5), (4.0, 8.0)],
        "epsilon": 0.3,
        "expected_pieces": 3 # Typically splits are (0,2), (2,4), (4,5) (or similar)
    },
    # 6. Sinusoidal Curve Segment (Oscillating data)
    {
        "description": "Oscillating data (sinusoidal) where max error quickly exceeds tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0, 2) has max error 1.0 (fails), (0, 1.5) fails, a split must occur around the peak/trough. e.g., (0,2) and (2,4)
    },
    # 7. Large Gap (Tests if the error calculation correctly handles massive x-intervals)
    {
        "description": "Two distant clusters, testing error calculation across a large x-gap.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (10.0, 10.0), (11.0, 10.0)],
        "epsilon": 0.01,
        "expected_pieces": 3 # The linear line across the gap will have a huge error, forcing 3 pieces.
    },
    # 8. Near-Optimal Cut (Error is exactly epsilon or slightly less)
    {
        "description": "Data that is very close to the tolerance boundary, testing <= epsilon condition.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.1), (3.0, -0.05)],
        "epsilon": 0.1,
        "expected_pieces": 1 # The max error is 0.1, which is <= epsilon, so one piece is optimal.
    },
    # 9. Multiple Optimal Split Points (Ensuring the greedy choice, if any, leads to the global minimum)
    {
        "description": "Data with multiple points where a split *could* occur, testing optimality for minimum pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.6), (2.0, 0.0), (3.0, 0.6), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0, 2) has max error 0.6 (fails), (0, 1) has error 0.3 (passes), (0, 1) and (1, 4) fails, (0, 2) and (2, 4) passes
    },
    # 10. Negative Coordinates (Robustness test)
    {
        "description": "Data using negative x and y coordinates, testing general robustness.",
        "pw_linear_fx": [(-2.0, 2.0), (-1.0, -1.0), (0.0, 0.0), (1.0, 1.0), (2.0, -2.0)],
        "epsilon": 0.5,
        "expected_pieces": 3 # E.g., (-2, 0), (0, 1), (1, 2) or similar split points
    }
]
test_cases21 = [
    # 1. Basic Case: Simple linear segment requiring one piece.
    # Points are collinear. Any positive epsilon should yield 1 piece.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 1,
        'description': "Collinear points, should be 1 piece."
    },

    # 2. Case where no approximation is needed (all points are identical).
    # If the algorithm treats identical points as a zero-length segment, it should be 1 piece.
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        'epsilon': 1e-6,
        'expected_min_pieces': 1,
        'description': "Horizontal line, very small epsilon, should be 1 piece."
    },

    # 3. Step Function: Requires a new piece at every 'step'.
    # Tolerance is too small to cover the 1.0 jump.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0001, 1.0), (2.0, 1.0), (2.0001, 2.0), (3.0, 2.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 3,
        'description': "Step function, requires new piece at each large jump."
    },

    # 4. Alternating Max Error: Points are just barely outside the tolerance.
    # The error (y-value difference) is exactly epsilon + a tiny amount.
    # The middle point (1.0, 1.0 + 2*epsilon) requires two pieces.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.21), (2.0, 0.0)],
        'epsilon': 0.1, # Max L_inf error is |y_i - y_approx|
        'expected_min_pieces': 2, # Line (0,0) to (2,0) has error 0.21 > 0.1, so two pieces needed.
        'description': "Single point requiring a split, where error is 2*epsilon + tiny_amount."
    },

    # 5. Near-Optimal Case: A single piece *just* fails, forcing two pieces.
    # Line from (0,0) to (4,0). Point (2, 0.5) has L_inf error 0.5.
    # If epsilon is 0.49, one piece fails. If it's 0.5, one piece succeeds.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.4), (2.0, 0.51), (3.0, 0.4), (4.0, 0.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 1, # Line (0,0) to (4,0) error max is 0.51. This test ensures the algorithm handles the *first* point just outside. Let's make it fail.
        'expected_min_pieces': 2, # Line (0,0) to (4,0) has error 0.51 > 0.5. A single piece fails. Two are required.
        'description': "Concave function where one piece is barely outside tolerance, forcing two."
    },

    # 6. Zig-Zag requiring multiple pieces.
    # The rapid change in direction should necessitate multiple pieces for small epsilon.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        'epsilon': 0.01,
        'expected_min_pieces': 4, # Each V-shape requires a split unless tolerance is large.
        'description': "High-frequency zig-zag, small epsilon, requires many pieces."
    },

    # 7. Zero Tolerance: Should require n pieces for n segments (all segments).
    # Error must be exactly zero, so any non-linear data needs all segments.
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.1), (2.0, 1.0), (3.0, 1.1), (4.0, 1.0)],
        'epsilon': 0.0,
        'expected_min_pieces': 4, # n+1 points = 4 segments.
        'description': "Zero tolerance, requires one piece per original segment."
    },

    # 8. Large Tolerance: Should require only one piece.
    # The max error of the entire function is < epsilon.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        'epsilon': 1.0,
        'expected_min_pieces': 1, # Max error is 0.5 < 1.0 (Line 0,0 to 4,0).
        'description': "Large tolerance, should compress entire dataset into 1 piece."
    },

    # 9. Boundary Case: The approximation error is exactly equal to epsilon.
    # This point (1.0, 0.2) is exactly epsilon away from the line (0,0) to (2,0).
    # If the check is $L_{\infty} \leq \varepsilon$, it should be 1 piece. If it's $L_{\infty} < \varepsilon$, it should be 2.
    # Assuming $L_{\infty} \leq \varepsilon$ (inclusive):
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0)],
        'epsilon': 0.2,
        'expected_min_pieces': 1,
        'description': "Error is exactly epsilon, should pass and be 1 piece."
    },

    # 10. Data Points with Varying x-Spacing and a Critical Middle Point.
    # A single point (1.0, 5.0) has a large deviation, requiring a split despite the small x-distance.
    # Line (0,0) to (10,0) has max error 5.0. Epsilon 1.0 forces a split.
    # The split should happen at the point requiring the greatest reduction in error.
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (5.0, 0.0), (10.0, 0.0)],
        'epsilon': 1.0,
        'expected_min_pieces': 2, # Split likely from (0,0) to (2,0) and (2,0) to (10,0), or similar.
        'description': "Large deviation over short x-distance, forcing a split."
    }
]
test_cases22 = [
    {
        "description": "Perfectly Linear Data - Should require only 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1
    },
    {
        "description": "Zero Tolerance (epsilon=0) - Should require max pieces to pass through all points.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.5), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 4
    },
    {
        "description": "Small Deviation (Single Point) - Forces 2 pieces due to tight epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.0), (3.0, -0.05), (4.0, 0.0)],
        "epsilon": 0.04,
        "expected_min_pieces": 2
    },
    {
        "description": "Stair-Step Data - Data that forces new segments frequently.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.4,
        "expected_min_pieces": 3
    },
    {
        "description": "Large Tolerance - Should cover the entire dataset with one piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 1
    },
    {
        "description": "Minimal Data (N=3) - Simplest non-linear case requiring one piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },
    {
        "description": "Minimal Data (N=3, Tight epsilon) - Forces two pieces in the simplest non-linear case.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.49,
        "expected_min_pieces": 2
    },
    {
        "description": "High Frequency Oscillations - Tests error accumulation/greedy choice.",
        "pw_linear_fx": [(0, 0), (0.5, 0.5), (1, 0), (1.5, -0.5), (2, 0), (2.5, 0.5), (3, 0)],
        "epsilon": 0.2,
        # Piece 1: (0,0) to (1,0) max error 0.5. Fails.
        # Piece 1: (0,0) to (0.5, 0.5) max error 0.0. Segment 2: (0.5, 0.5) to (1.5, -0.5) max error 0.5. Fails.
        # Piece 1: (0,0) to (2,0) max error 0.5. Fails.
        # Piece 1: (0,0) to (1,0) fails.
        # Piece 1: (0,0) to (1.5, -0.5) fails.
        # Optimal 3 pieces. e.g. (0,0) to (1.5, -0.5) fails.
        # Segment 1: (0,0) to (1,0) fails.
        # 3 pieces is correct. (0,0) to (1,0) fails.
        # Piece 1: (0,0) to (1.5, -0.5) fails.
        # Piece 1: (0,0) to (1,0) fails.
        # Piece 1: (0,0) to (1.5, -0.5) fails.
        "expected_min_pieces": 3
    },
    {
        "description": "Asymmetric Error - Data points on one side of the optimal segment line.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.2), (4.0, 0.1), (5.0, 0.0)],
        "epsilon": 0.15,
        "expected_min_pieces": 1
    },
    {
        "description": "Boundary Condition - Max error of the optimal 1-piece fit is exactly epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5, # Max error for optimal 1-piece fit is 0.5 (at x=1). Should pass.
        "expected_min_pieces": 1
    }
]
test_cases23 = [
    # 1. Simple Straight Line (Zero Pieces)
    # Goal: Test case where all points are already colinear, requiring only 1 segment (0 pieces in the approximation)
    # Expected: 1 segment (connecting (0,0) to (10,10)), 0 approximation pieces.
    {
        "description": "Perfectly colinear points; should require 1 segment (minimum).",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (5.0, 5.0), (10.0, 10.0)],
        "epsilon": 1.0
    },

    # 2. Points within Tolerance (One Piece)
    # Goal: Test case where all points can be approximated by a single line segment within a large tolerance.
    # Expected: 1 segment.
    {
        "description": "Slightly perturbed colinear points; single segment within large tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 0.1), (5.0, 0.0), (10.0, -0.1)],
        "epsilon": 0.5
    },

    # 3. Simple 'V' Shape (Two Pieces)
    # Goal: Test case requiring a split at an obvious vertex to maintain tolerance.
    # Expected: 2 segments.
    {
        "description": "Sharp 'V' shape; split must occur at the vertex (5, 5).",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 5.0), (10.0, 0.0)],
        "epsilon": 0.1
    },

    # 4. Step Function (Maximum Pieces)
    # Goal: Test case where the jump is too large and tolerance is too small, forcing the maximum number of segments (one less than points).
    # Expected: 3 segments.
    {
        "description": "Step function with small tolerance; maximum possible segments required.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.001, 10.0), (2.0, 10.0)],
        "epsilon": 0.5
    },

    # 5. Small Tolerance Forcing Splits
    # Goal: Test with a small $\varepsilon$ to ensure the algorithm doesn't simplify a non-linear curve.
    # Expected: Potentially many segments (depending on algorithm details, likely 3 or 4).
    {
        "description": "Parabola-like curve with small epsilon; forces fine-grained approximation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.1
    },

    # 6. Large Tolerance Allowing Aggressive Simplification
    # Goal: Test with a large $\varepsilon$ to ensure the algorithm finds the single segment solution, proving optimality for simplification.
    # Expected: 1 segment.
    {
        "description": "Parabola-like curve with large epsilon; allows single-segment approximation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 5.0
    },

    # 7. Symmetrical Curve Requiring Central Split
    # Goal: A simple sine-like wave that should require a split at the maximum and minimum.
    # Expected: 2 segments (split around x=1.5 or x=2.0).
    {
        "description": "Symmetrical 'M' shape; should require a split to capture the curve's peak.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, -2.0), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 8. Boundary Case: $\varepsilon$ Equals Maximum Deviation
    # Goal: Test the inclusivity/exclusivity of the tolerance (i.e., is a deviation of exactly $\varepsilon$ allowed?). Assuming it is allowed.
    # The segment (0,0) to (2,0) has a max deviation of 1.0 from (1,1).
    # Expected: 1 segment.
    {
        "description": "Tolerance exactly equal to the max deviation; should be covered by 1 segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 1.0
    },

    # 9. Initial Segment Needs Splitting Immediately
    # Goal: Test the first segment's decision boundary. The point (1, 10) should immediately force a split from (0, 0), and then the next points may be simplified.
    # Expected: At least 2 segments.
    {
        "description": "Immediate large jump forces early split; subsequent points may be colinear.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 10.1), (5.0, 10.2)],
        "epsilon": 0.5
    },

    # 10. Long Section of Simplification Followed by a Sharp Break
    # Goal: Ensure the algorithm doesn't stop after finding a long initial simplification, and correctly identifies the split needed at the end.
    # Expected: 2 segments (one from start to point (9, 0) and one from (9, 0) to (10, 5)).
    {
        "description": "Long initial simplification followed by a sharp deviation.",
        "pw_linear_fx": [(0.0, 0.0), (3.0, 0.1), (6.0, -0.1), (9.0, 0.0), (10.0, 5.0)],
        "epsilon": 0.5
    },
]
test_cases24 = [
    # 1. Perfect Line Fit (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.4)],
        "epsilon": 0.1
    },
    # 2. High Frequency Oscillation (Should be n pieces - 4)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 1.0), (4.0, -1.0)],
        "epsilon": 0.1
    },
    # 3. Zero Tolerance/Constant Function (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.0
    },
    # 4. Large Tolerance (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5), (4.0, 2.0)],
        "epsilon": 1.0
    },
    # 5. Just-Fit Midpoint (Should be 3 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.8), (3.0, 0.9), (4.0, 0.0)],
        "epsilon": 0.1
    },
    # 6. Alternating Deviation at Epsilon (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, -0.2), (4.0, 0.0)],
        "epsilon": 0.2
    },
    # 7. Alternating Deviation >> Epsilon (Should be 4 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.3), (2.0, 0.0), (3.0, 0.3), (4.0, 0.0)],
        "epsilon": 0.1
    },
    # 8. Identical X-Coordinates (Vertical Segment) (Should be 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.1
    },
    # 9. Tiny Epsilon / Numerical Stability (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0000001), (3.0, 0.0)],
        "epsilon": 1e-7 # 10^-7
    },
    # 10. Long Sequence on a Line (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.8), (3.0, 1.2), (4.0, 1.6), (5.0, 2.0)],
        "epsilon": 0.0001
    }
]
test_cases25 = [
    # 1. Straight Line (Zero Error): Should always be 1 piece regardless of epsilon.
    {
        "description": "Perfect straight line: Should require 1 piece for any epsilon > 0.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 2. Maximum Deviation Slightly Above Epsilon: Should require at least 2 pieces.
    # Points: (0,0), (2, 0.51), (4,0). Max error from (0,0) to (4,0) is 0.51.
    {
        "description": "Max deviation slightly above epsilon: Forces a break (2 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 0.51), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # 3. Maximum Deviation Exactly Equal to Epsilon: Should be 1 piece (boundary case).
    # Points: (0,0), (2, 0.5), (4,0). Max error from (0,0) to (4,0) is 0.5.
    {
        "description": "Max deviation exactly equal to epsilon: Should be 1 piece (boundary).",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # 4. Step Function (High Frequency/Low Amplitude): Tests how the algorithm handles frequent small changes.
    {
        "description": "High frequency, small amplitude (step-like): Forces many small pieces.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.6), (0.2, 0.0), (0.3, 0.6), (0.4, 0.0)],
        "epsilon": 0.2,
        "expected_pieces": 4
        # (0,0) to (0.4,0) has max error 0.6 > 0.2. Must break.
        # (0,0) to (0.2,0) has max error 0.6 > 0.2. Must break at (0.2,0).
        # (0.2,0) to (0.4,0) has max error 0.6 > 0.2. Must break at (0.4,0).
        # Optimal: [(0,0)-(0.1,0.6)], [(0.1,0.6)-(0.2,0)], [(0.2,0)-(0.3,0.6)], [(0.3,0.6)-(0.4,0)]
    },
    # 5. Parabola (Uniform Curvature): Tests smooth, non-linear data where error grows quadratically.
    {
        "description": "Parabolic curve: Tests error growth on smooth data.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 2.0,
        "expected_pieces": 2
        # (0,0) to (2,4) max error is 1.0 (at x=1.0) <= 2.0 (OK)
        # (0,0) to (3,9) max error is 2.0 (at x=1.0) and 2.0 (at x=2.0) <= 2.0 (OK)
        # (0,0) to (4,16) max error is 3.0 (at x=1.0, 3.0) > 2.0 (FAIL)
        # Optimal break at (3,9). Pieces: [(0,0)-(3,9)], [(3,9)-(4,16)]
    },
    # 6. Very Loose Tolerance (Large Epsilon): Should always be 1 piece if possible.
    {
        "description": "Very loose tolerance: Should result in 1 piece.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)], # Same as example
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    # 7. Minimum Number of Points (Two): Always 1 piece.
    {
        "description": "Minimum data points (n=2): Always 1 piece.",
        "pw_linear_fx": [(1.0, 5.0), (2.0, 10.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    # 8. Single Point Violating Epsilon: Tests finding the optimal breakpoint.
    # (0,0) to (10,0). Midpoint (5, 1.1). Max error is 1.1.
    {
        "description": "Single point violating epsilon (optimal break in middle).",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 1.1), (10.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
        # Break at (5, 1.1). Pieces: [(0,0)-(5, 1.1)], [(5, 1.1)-(10,0)]
    },
    # 9. Initial Flat Section Followed by Steep Climb: Tests non-uniform error distribution.
    {
        "description": "Flat then steep: First section is 1 piece, forcing a break at the start of the climb.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 5.0), (5.0, 10.0)],
        "epsilon": 0.5,
        "expected_pieces": 3
        # (0,0) to (3,0) max error 0.0 (OK)
        # (0,0) to (4,5) max error 1.25 > 0.5 (FAIL). Break at (3,0).
        # (3,0) to (4,5) max error is 0.0 (OK, points are on the line).
        # (3,0) to (5,10) max error is 0.0 (OK, points are on the line).
        # (4,5) to (5,10) max error is 0.0 (OK).
        # Optimal: [(0,0)-(3,0)], [(3,0)-(4,5)], [(4,5)-(5,10)]
    },
    # 10. Sawtooth Wave (High Frequency/High Amplitude): Requires maximum number of pieces.
    {
        "description": "Sawtooth wave: Requires a piece for every segment due to small epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.01,
        "expected_pieces": 4
        # (0,0) to (2,0) has max error 1.0. Must break at every point due to small epsilon.
    }
]
test_cases26 = [
    # Case 1: Perfect Fit (Zero Error)
    # Rationale: A straight line perfectly fits, requiring the absolute minimum of 1 piece, even with a small epsilon.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01,
        "expected_min_pieces": 1
    },

    # Case 2: Tight Fit (Forcing 3 Pieces)
    # Rationale: The alternating nature and large peaks (relative to epsilon) force a new segment after the slope changes, requiring 3 pieces.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.2,
        "expected_min_pieces": 3
    },

    # Case 3: Stair-Step Function (Testing Discontinuity/Sharp Corners)
    # Rationale: The near-vertical "jump" (e.g., (1.0, 0.0) to (1.1, 1.0)) cannot be covered by a single line with the gentle horizontal sections, forcing 3 pieces.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 1.0), (2.1, 1.0), (2.2, 2.0), (3.2, 2.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 3
    },

    # Case 4: High Frequency Oscillations (Symmetry and Error Maxima)
    # Rationale: The large error (0.6) forces more than one piece. Minimal solution requires 3 pieces to cover the deep dips and high peaks within the 0.5 tolerance.
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.6), (1.0, 0.0), (1.5, -0.6), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3
    },

    # Case 5: Large Epsilon (Testing Coarse Approximation)
    # Rationale: A single line from (0,0) to (3,0) has a maximum error of 10.0 at x=1 and x=2. The large tolerance allows the single piece, proving optimality for loose constraints.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -10.0), (3.0, 0.0)],
        "epsilon": 10.0,
        "expected_min_pieces": 1
    },

    # Case 6: Small Epsilon (Testing Fine Detail)
    # Rationale: The very small epsilon (0.001) forces a piece between nearly every point, as the adjacent point difference (0.01) is greater than epsilon, forcing 4 pieces.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.01), (2.0, 0.0), (3.0, 0.01), (4.0, 0.0)],
        "epsilon": 0.001,
        "expected_min_pieces": 4
    },

    # Case 7: Concave Curvature (Testing non-linear data)
    # Rationale: A single line from (0,0) to (4,1) has an error of approx. 0.3 at x=2, which is > 0.1. Two pieces are necessary to contain the curvature.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 0.9), (4.0, 1.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2
    },

    # Case 8: Convex Curvature (Complementary Curvature Check)
    # Rationale: Similar to the concave case, the convex curvature forces at least two pieces due to the maximum error exceeding 0.1.
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.9), (2.0, 0.8), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2
    },

    # Case 9: Multiple Co-linear Sections (Testing Sequential Co-linearity)
    # Rationale: The three sections have distinct optimal line fits (slope 1, slope 0, slope 1). The approximation must find the three minimum pieces defined by these structural changes.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 2.0), (4.0, 2.0), (5.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3
    },

    # Case 10: Near-Vertical Section (Testing Extreme Slope)
    # Rationale: The steep segment (0,0) to (0.001, 1.0) forces the algorithm to use it as its own piece, as combining it with later, gentle segments would lead to a massive error (much greater than 0.1).
    {
        "pw_linear_fx": [(0.0, 0.0), (0.001, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3
    }
]
test_cases27 = [
    # 1. Simple Case: All points on a line. Optimal segments: 1.
    # Exposes failure if the algorithm uses more than one segment unnecessarily.
    {
        "description": "Perfect Line",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1.0,
        "optimal_segments": 1,
    },
    # 2. Maximum Deviation within Epsilon: All points define a single segment with max error exactly ε.
    # Exposes failure if the algorithm is strictly less than ε or uses two segments.
    {
        "description": "Max Error on Boundary (Single Segment)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "optimal_segments": 1,
    },
    # 3. Requires exactly two segments with the split point clearly defined.
    # Exposes failure if it merges two segments when max error is slightly > ε.
    {
        "description": "Two Segments Required (Sharp Turn)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.0,  # Requires points to be exactly on the line
        "optimal_segments": 4, # (0,0)-(1,1), (1,1)-(2,0), (2,0)-(3,1), (3,1)-(4,0)
    },
    # 4. Long Sequence: An S-Curve that needs to be broken up.
    # Exposes a greedy algorithm that might end the first segment too early.
    {
        "description": "Smooth S-Curve Requiring Multiple Segments",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 0.4), (5.0, 0.1), (6.0, 0.0)],
        "epsilon": 0.2,
        "optimal_segments": 3, # e.g., (0,0)-(3,0.9), (3,0.9)-(4,0.4), (4,0.4)-(6,0.0) is *not* a good approx.
                               # More accurately: (0,0)-(2,0.4), (2,0.4)-(4,0.4), (4,0.4)-(6,0.0) with max dev 0.4 > 0.2
                               # Optimal split points must be found. For ε=0.2, it's likely (0,0)-(2,0.4) is 1 seg, (2,0.4)-(4,0.4) is 1 seg, (4,0.4)-(6,0.0) is 1 seg. Total: 3.
    },
    # 5. Segment Extension Trap: A small deviation early that is within ε, but forcing a break would lead to a longer final segment.
    # A non-optimal algorithm might break at (2, 0.1) leading to 3 segments, while 2 segments is optimal.
    {
        "description": "Segment Extension Trap (2 segments optimal)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.05,
        "optimal_segments": 3, # (0,0)-(2,0.1) max error 0.1/2 = 0.05. (2,0.1)-(5,0.0) max error at 3.0, 4.0 is high.
                               # (0,0)-(3,0.0) max error 0.1. (3,0.0)-(5,0.0) max error 0.0. Total: 2 (Incorrect, max error must be 0.05).
                               # (0,0)-(2,0.1) max error 0.05. (2,0.1)-(5,0.0) max error 0.0667 > 0.05.
                               # Optimal: (0,0)-(2,0.1) $\epsilon=0.05$. (2,0.1)-(5,0.0) $\epsilon=0.05$ (at x=3). Total: 2.
    },
    # 6. Minimal Epsilon: Tests handling of near-zero tolerance (only perfect matches pass).
    {
        "description": "Minimal Epsilon (Almost Zero)",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0001), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.00001,
        "optimal_segments": 2, # (0,1.0)-(1, 1.0001) is 1 seg. (1, 1.0001)-(4, 1.0) is 1 seg. Total: 2.
    },
    # 7. Step Function: Requires a break at every vertical jump.
    {
        "description": "Step Function with High Tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 10.0), (2.0, 10.0)],
        "epsilon": 1.0,
        "optimal_segments": 2, # (0,0)-(1.0, 0.0) $\epsilon=0$. (1.0001, 10.0)-(2.0, 10.0) $\epsilon=0$. The jump is not approximated.
                               # If the approximation must include the point (1.0, 0.0) and (1.0001, 10.0), it should take 2 segments: (0,0)-(1,0) and (1.0001, 10.0)-(2,10.0).
    },
    # 8. High-Frequency Noise within Epsilon.
    # Exposes failure if the algorithm is conservative and breaks segments too often despite small deviations.
    {
        "description": "High-Frequency Noise within Epsilon",
        "pw_linear_fx": [(i, 0.0 + ((-1)**i) * 0.4) for i in range(10)],
        "epsilon": 0.5,
        "optimal_segments": 1,
    },
    # 9. Initial Steep Segment followed by a long, flat segment.
    # Exposes non-optimal behavior if it incorrectly tries to merge the steep part with the flat part.
    {
        "description": "Steep Start, Flat End",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.5,
        "optimal_segments": 2, # (0,0)-(1,5) has max error 2.5 > 0.5. (0,0)-(1,5) must be 1 segment. (1,5)-(4,5) is 1 segment. Total: 2.
    },
    # 10. Small dataset, the general case for testing.
    {
        "description": "General Case (from example)",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "optimal_segments": 2, # (0,1)-(2,3) max error is 0.0. (2,3)-(5,8) max error is 0.0. Total: 2.
    },
]
test_cases28 = [
    # 1. Base Case: Perfectly Linear Data (Should require 1 piece)
    {
        'description': "Perfectly Linear Data (1 piece)",
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.01,
        'expected_min_pieces': 1
    },

    # 2. Zero Tolerance: Should require n pieces (n = number of segments)
    {
        'description': "Zero Tolerance (Max pieces)",
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        'epsilon': 0.0,
        'expected_min_pieces': 3  # (4 points, 3 segments)
    },

    # 3. Large Tolerance: Should require 1 piece (maximum error is within epsilon)
    {
        'description': "Large Tolerance (1 piece)",
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        'epsilon': 0.5,  # Maximum error is 0.1, so one line from (0,0) to (4,0) works.
        'expected_min_pieces': 1
    },

    # 4. Critical Edge Case: Error is exactly equal to epsilon
    # The first segment from (0,0) to (2,0) has max error 0.1, which is <= 0.1.
    {
        'description': "Error Exactly Epsilon (Critical Point)",
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 1.0), (4.0, 1.1), (5.0, 1.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 2  # Segment 1: (0,0) to (2,0). Segment 2: (2,0) to (5,1.0) approx
    },

    # 5. Staircase/Sawtooth Pattern: Requires multiple pieces regardless of segment length
    {
        'description': "Sawtooth Pattern (Must break frequently)",
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        'epsilon': 0.2,  # Max error of 0.5 for 1 piece. Requires 2 pieces: (0,0)->(2,0) and (2,0)->(4,0).
        'expected_min_pieces': 2
    },

    # 6. Minimal Data Points (n=1 segment): Trivial case
    {
        'description': "Minimal Data Points (1 segment)",
        'pw_linear_fx': [(0.0, 1.0), (5.0, 8.0)],
        'epsilon': 100.0,
        'expected_min_pieces': 1
    },

    # 7. Non-Uniform X-Spacing and Y-Change
    {
        'description': "Non-Uniform Spacing (Testing optimality on slope change)",
        'pw_linear_fx': [(0.0, 0.0), (0.1, 0.0), (1.0, 0.5), (10.0, 5.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 2  # Segment 1: (0,0) to (0.1, 0.0). Segment 2: (0.1, 0.0) to (10.0, 5.0)
    },

    # 8. Large Jump/Discontinuity requiring a break
    {
        'description': "Large Jump/Discontinuity (Requires immediate break)",
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (1.1, 10.0), (2.0, 10.1)],
        'epsilon': 1.0,
        'expected_min_pieces': 2
        # Segment 1: (0,0) to (1.0, 0.1) - max error 0.05. Segment 2: (1.0, 0.1) to (2.0, 10.1).
    },

    # 9. Case where the minimum piece length is exactly 2 data points (adjacent points are needed)
    {
        'description': "Minimum Piece Length (Adjacent points required)",
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.1, 1.0), (2.0, 1.0), (3.0, 2.0)],
        'epsilon': 0.05,
        'expected_min_pieces': 3  # Must break after (1.0, 1.0) and include (1.1, 1.0) to keep error low.
    },

    # 10. General Case: Multiple optimal segment choices possible, testing for greediness/optimality
    # Example: (0,0) to (2,0) works with max error 0.1. (2,0) to (4,0) works. Total 2 pieces.
    # The one-piece line (0,0) to (4,0) has max error of 0.5, exceeding 0.2.
    {
        'description': "General Complex Curve (Testing minimum count)",
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        'epsilon': 0.2,
        'expected_min_pieces': 2
    }
]
test_cases29 = [
    {
        # Case 1: Trivial Case (Flat Line, large epsilon). Must return 1 piece.
        "description": "Perfectly linear, large tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0
    },
    {
        # Case 2: Minimal Error Case (Perfect Fit). Must return 1 piece.
        "description": "Perfectly linear diagonal, small tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (4.0, 4.0), (6.0, 6.0)],
        "epsilon": 0.1
    },
    {
        # Case 3: Two Pieces Required (Sharp Corner/V-shape). Must return 2 pieces regardless of large epsilon.
        "description": "V-shape forcing two segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 1.0
    },
    {
        # Case 4: Tolerance-Driven Split (Convex Arc, small epsilon). Tests optimality on a curve.
        "description": "Convex arc requiring multiple splits.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.6), (2.0, 0.8), (3.0, 0.6), (4.0, 0.0)],
        "epsilon": 0.2
    },
    {
        # Case 5: Tolerance-Driven Merge (Same Arc, large epsilon). Tests if the algorithm correctly merges when tolerance allows.
        "description": "Convex arc allowing single segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.6), (2.0, 0.8), (3.0, 0.6), (4.0, 0.0)],
        "epsilon": 0.85
    },
    {
        # Case 6: Stair-Step Function. Tests tight constraints and horizontal segments.
        "description": "Stair-step function, small tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 1.0), (2.1, 1.0), (2.2, 2.0), (3.2, 2.0)],
        "epsilon": 0.05
    },
    {
        # Case 7: Boundary Condition (epsilon = 0.0). Forces the maximum number of pieces (n segments for n+1 points).
        "description": "Zero tolerance, forcing full segmentation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0
    },
    {
        # Case 8: Gradual Deviation/Long Dataset. Tests if a small, cumulative error eventually forces an optimal split.
        "description": "Long dataset with gradual deviation.",
        "pw_linear_fx": [(i, i + 0.1 * (i % 4)) for i in range(10)], # Generates 10 points
        "epsilon": 0.5
    },
    {
        # Case 9: Oscillating Data (High Frequency). Tests $L_{\infty}$ on points far from the line.
        "description": "High frequency oscillation.",
        "pw_linear_fx": [(i, 0.5 * ((-1)**i)) for i in range(8)], # Generates 8 points
        "epsilon": 0.1
    },
    {
        # Case 10: Uneven $\Delta x$ and Steep Slopes. Checks if the variable x-spacing is correctly handled in $L_{\infty}$ (vertical distance).
        "description": "Uneven $\Delta x$ and steep slopes.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (5.0, 0.0), (5.1, 1.0), (10.0, 0.0)],
        "epsilon": 0.5
    }
]
test_cases30 = [
    # Case 1: Perfectly Linear - Should result in 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # Case 2: Zero Tolerance - Forces a piece for every segment (n-1 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    # Case 3: Large Tolerance - Should result in 1 piece despite non-linearity
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    # Case 4: Sharp V-Shape - Forces 2 pieces due to small epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    # Case 5: Minimal Error Fit - Fits in 1 piece using the optimal line y=0.25
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # Case 6: Boundary Case I (Just Fits) - Tests strict inequality (error <= epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # Case 7: Boundary Case II (Just Fails) - Tests strict inequality (error > epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 2
    },
    # Case 8: Staircase (Multiple identical x-values removed as per standard assumption) - Tests horizontal and vertical changes
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    # Case 9: Multiple Segments - Forces multiple segments due to small epsilon and high oscillation
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    # Case 10: Horizontal Line Edge - Checks points slightly above/below the mean line
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.9), (2.0, 1.1), (3.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    }
]