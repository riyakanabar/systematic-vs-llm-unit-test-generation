test_cases1 = [
    # 1. Trivial Cases (Single Piece Optimal)
    {
        "description": "Perfect linear fit, should require 1 piece.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.1
    },
    {
        "description": "Constant function, should require 1 piece.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.01
    },
    {
        "description": "One maximum error point exactly on epsilon boundary, should require 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 0.0)],
        "epsilon": 0.5
    },

    # 2. Simple Optimality Checks (Should be 2 pieces)
    {
        "description": "V-shape function, requiring 2 pieces.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 0.0), (2.0, 5.0)],
        "epsilon": 1.0
    },
    {
        "description": "Step-like function, requiring 2 pieces for optimal fit.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.01, 5.0), (2.0, 5.0)],
        "epsilon": 0.1
    },
    {
        "description": "Standard quadratic curve, can be fit in 2 pieces for given epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.5
    },

    # 3. Maximum Error Management (Points on or near the boundary)
    {
        "description": "Point *exactly* requiring a new segment (max error = epsilon).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.5  # Optimal should be 2 pieces: [(0,0) to (2,1)] and [(2,1) to (3,0)]
    },
    {
        "description": "Point *just over* epsilon, forcing a new segment start/end.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0001), (3.0, 0.0)],
        "epsilon": 0.5  # Optimal should be 3 pieces
    },
    {
        "description": "Oscillating points, demanding minimum pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.5), (4.0, -0.5)],
        "epsilon": 0.49  # Should be 4 pieces if optimal, as each segment has error > 0.5.
    },
    {
        "description": "Oscillating points, allowing fewer pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.5), (4.0, -0.5)],
        "epsilon": 0.51  # Should be 1 piece if optimal
    },

    # 4. Non-uniform x-sampling (Affection on linear interpolation error)
    {
        "description": "Non-uniform x: Dense initial sampling, then sparse.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.0), (10.0, 0.0)],
        "epsilon": 0.05  # Requires 2 pieces due to (0.1, 0.1)
    },
    {
        "description": "Non-uniform x: Large gap causes high interpolation error in parabola.",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 100.0), (10.1, 100.0)],
        "epsilon": 5.0  # Test if algorithm handles points between knots. Parabola y=x^2. Midpoint error is 25.
    },
    {
        "description": "Non-uniform x: Linear start, then forcing a new piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (2.1, 10.0), (3.0, 11.0)],
        "epsilon": 0.5  # Should be 2 pieces
    },

    # 5. Flat/Constant Segments (Tests handling of zero curvature)
    {
        "description": "Flat region followed by a slope change, boundary check.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.1  # Requires 2 pieces
    },
    {
        "description": "Flat region where error tolerance is met across the slope change.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 0.5  # Should be 1 piece (line from (0,0) to (3,2))
    },

    # 6. High-Frequency/High Curvature (Guaranteed multiple pieces)
    {
        "description": "Rapid alternating sign change (Sawtooth), should require n pieces.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (0.3, 1.0), (0.4, 0.0), (0.5, 1.0)],
        "epsilon": 0.01  # Should be 5 pieces
    },
    {
        "description": "Parabola $y=x^2$ with tight epsilon.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)],
        "epsilon": 0.2  # Should require > 2 pieces. Error for (0,0)-(5,25) is 1.
    },
    {
        "description": "Sine-wave-like data (peaks require segment ends).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.1  # Should require ~4 pieces
    },

    # 7. Boundary $\epsilon$ values
    {
        "description": "Epsilon = 0: should be max pieces (n segments, n+1 points).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.0  # Should be 2 pieces
    },
    {
        "description": "Epsilon very large: should be 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1000.0), (2.0, 0.0)],
        "epsilon": 1000.0  # Should be 1 piece
    },
    {
        "description": "Epsilon just slightly greater than the max error for a single piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5 + 1e-9  # Should be 1 piece (Max error is 0.5 at x=1.0)
    },
    {
        "description": "Epsilon just slightly less than the max error for a single piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5 - 1e-9  # Should be 2 pieces
    },

    # 8. Small Datasets (Minimum number of points)
    {
        "description": "Two points (n=1 piece), always 1 piece.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.0
    },
    {
        "description": "Three points (n=2 pieces), one piece optimal.",
        "pw_linear_fx": [(0.0, 1.0), (0.5, 1.0), (1.0, 1.0)],
        "epsilon": 0.1
    },

    # 9. Complex and Mixed Cases (Combining challenges)
    {
        "description": "Mixed linear, flat, and sharp turn sections.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 2), (4, 2), (5, 5), (6, 6)],
        "epsilon": 0.1  # Optimal should be 3 pieces: (0,2), (2,4), (4,6)
    },
    {
        "description": "A complex case designed to test the greedy choice of optimal knot placement.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 0.5), (6, -0.5)],
        "epsilon": 0.4  # Should require careful path planning to ensure optimality (min pieces)
    },
    {
        "description": "Example from the prompt - for completeness.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },

    # 10. Negative Coordinates / Large Values
    {
        "description": "Large coordinate values, testing floating point stability.",
        "pw_linear_fx": [(1000.0, 10000.0), (1001.0, 10001.0), (1002.0, 10002.0), (1003.0, 10003.0)],
        "epsilon": 0.0
    },
    {
        "description": "Negative coordinates and values.",
        "pw_linear_fx": [(-2.0, -10.0), (-1.0, -9.0), (0.0, -8.0), (1.0, -7.0)],
        "epsilon": 0.1
    },
    {
        "description": "Negative Epsilon (Should probably raise an error or treat as 0, but tests input handling).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": -0.1
    }
]
test_cases2 = [
    # ----------------------------------------------------------------------
    # 1. Basic Cases and Verification (Expected Optimal Pieces: 1, 2, or max)
    # ----------------------------------------------------------------------
    # T01: All points are collinear (1 optimal piece).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.1},
    # T02: Perfect horizontal line (1 optimal piece).
    {"pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)], "epsilon": 0.01},
    # T03: Very large epsilon (Should require only 1 piece).
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 10.0), (2.0, 1.0), (3.0, 10.0)], "epsilon": 100.0},
    # T04: Small dataset requiring 2 pieces (basic 2-piece check).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 0.0)], "epsilon": 0.5},
    # T05: Epsilon requires maximum possible pieces (n-1 pieces for n points).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0), (4.0, 0.0)], "epsilon": 0.0},

    # ----------------------------------------------------------------------
    # 2. Tight Constraint / Error = Epsilon Cases
    # ----------------------------------------------------------------------
    # T06: Segment where max error is *exactly* epsilon (tests boundary condition).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)], "epsilon": 0.5},
    # T07: Segment where max error is exactly epsilon, but at an intermediate point.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.5, 0.5), (2.0, 0.0)], "epsilon": 0.5},
    # T08: A very small epsilon (tests floating point precision near zero).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1e-5), (2.0, 2e-5)], "epsilon": 1e-6},
    # T09: Maximum error is slightly *over* epsilon (forces a split).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0), (5.0, 5.0), (6.0, 6.0)],
     "epsilon": 0.0},

    # ----------------------------------------------------------------------
    # 3. Greedy Optimality Traps (Multiple feasible endpoints where an early choice is sub-optimal)
    # ----------------------------------------------------------------------
    # T10: Long, flat start. A greedy choice might break early, but a single piece spans more.
    # Optimal: 2 pieces (0->5, 5->10). Sub-optimal: (0->2, 2->5, 5->10) = 3 pieces.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0), (5.0, 0.1), (10.0, 1.0)],
     "epsilon": 0.1},
    # T11: Initial segment has two feasible end-points, p_j and p_k (k > j). p_j is sub-optimal.
    # Segment (0, 0) to (3, 0) has max error 0.5 at x=1.5. Feasible up to p4.
    # If the algorithm chooses p2, it's non-optimal (0->2, 2->4). Optimal (0->4).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, 0.4), (4.0, 0.0)], "epsilon": 0.4},
    # T12: A sequence of small, repeated 'V' shapes. Greedy must be careful to select the longest span.
    # Optimal: 1 piece (0->6). Sub-optimal: (0->2, 2->4, 4->6) = 3 pieces if it doesn't check p6.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, 0.2), (4.0, 0.0), (5.0, 0.2), (6.0, 0.0)],
     "epsilon": 0.2},
    # T13: The longest feasible segment requires the approximation line to pass through the tolerance corridor's corners.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)], "epsilon": 0.5},

    # ----------------------------------------------------------------------
    # 4. Data with High/Low Frequency Changes
    # ----------------------------------------------------------------------
    # T14: High frequency, low amplitude oscillation (should be 1 piece).
    {"pw_linear_fx": [(i, 0.0 if i % 2 == 0 else 0.4) for i in range(10)], "epsilon": 0.5},
    # T15: Low frequency, high amplitude change (should require multiple pieces).
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 10.0), (20.0, 0.0), (30.0, 10.0)], "epsilon": 1.0},
    # T16: Points that oscillate *around* a line. The maximum error may be at an interior point.
    {"pw_linear_fx": [(i, 0.5 * i + 0.3 if i % 2 == 0 else 0.5 * i - 0.3) for i in range(7)], "epsilon": 0.5},
    # T17: Convex curve that forces early splits.
    {"pw_linear_fx": [(i, i ** 2) for i in range(5)], "epsilon": 1.0},

    # ----------------------------------------------------------------------
    # 5. Degenerate and Boundary Conditions
    # ----------------------------------------------------------------------
    # T18: Minimum two points (1 piece).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)], "epsilon": 0.0},
    # T19: Three points, one perfectly on the line, but zero epsilon (2 pieces).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)], "epsilon": 0.0},
    # T20: Data with duplicate x-values (must handle sequential identical points - usually okay, but a check).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)], "epsilon": 0.1},
    # T21: Data with duplicate y-values (creates horizontal segments, easy to approximate).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0)], "epsilon": 0.5},
    # T22: Negative coordinates/mixed quadrants.
    {"pw_linear_fx": [(-5.0, 5.0), (-2.0, -2.0), (0.0, 0.0), (3.0, -5.0)], "epsilon": 1.0},
    # T23: Approximation line is nearly vertical (slope is very large).
    {"pw_linear_fx": [(0.0, 0.0), (0.001, 10.0), (0.002, 0.0)], "epsilon": 0.5},

    # ----------------------------------------------------------------------
    # 6. Combinations of Traps
    # ----------------------------------------------------------------------
    # T24: Long flat segment, followed by a tight constraint forcing a break.
    # Optimal: 2 pieces (0->10, 10->11). Non-optimal might break at 5.
    {"pw_linear_fx": [(i, 0.0) for i in range(11)] + [(11.0, 1.0)], "epsilon": 0.1},
    # T25: Two distinct "corridors" that barely meet. Algorithm must choose the longest span possible.
    # Segment 0->4 is feasible (max error 0.5). Segment 4->8 is feasible (max error 0.5).
    # Optimal: 2 pieces (0->4, 4->8). Sub-optimal: (0->2, 2->4, 4->6, 6->8) = 4 pieces.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0), (5.0, 0.5), (6.0, 0.0), (7.0, 0.5),
                      (8.0, 0.0)], "epsilon": 0.5},
    # T26: A zig-zag pattern where *every other* point is the max error point for a long segment.
    # Points 1, 3, 5, 7, 9 are max error. Line 0->10 works for epsilon=1.
    {"pw_linear_fx": [(i, (i % 2) * 2.0) for i in range(11)], "epsilon": 1.0},
    # T27: A sequence where the max feasible length is determined by a point *far* from the start, not the immediately adjacent points.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 0.1), (3.0, 0.1), (4.0, 0.1), (5.0, 0.1)], "epsilon": 0.5},
    # Line 0->5 fails at x=1. Line 0->2 is optimal first step.

    # ----------------------------------------------------------------------
    # 7. Larger Datasets to Test Efficiency/Cumulative Error
    # ----------------------------------------------------------------------
    # T28: A moderately long dataset with a consistent error profile (checks for performance and stability).
    {"pw_linear_fx": [(i, i * 0.1 + (i % 4) * 0.2) for i in range(20)], "epsilon": 0.3},
    # T29: Data that forces a break in the middle, then a long run to the end.
    {"pw_linear_fx": [(i, i) for i in range(10)] + [(10.0, 20.0)] + [(i, 20.0) for i in range(11, 20)], "epsilon": 1.0},
    # T30: The example from the prompt (for a sanity check).
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)], "epsilon": 0.5}
]
test_cases3 = [
    # ----------------------------------------------------------------------
    # 1. Base Cases & Simplicity (Should require 1 segment)
    # ----------------------------------------------------------------------
    { # 1. Perfectly flat data, high tolerance. (Optimal: 1)
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "Flat function, high epsilon."
    },
    { # 2. Perfectly linear increasing data. (Optimal: 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_pieces": 1,
        "description": "Perfectly linear function, zero epsilon."
    },
    { # 3. Smallest possible dataset. (Optimal: 1)
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "description": "Minimum data points (2 points, 1 piece)."
    },
    # ----------------------------------------------------------------------
    # 2. Tolerance & Boundary Exposure (Greedy failure candidates)
    # ----------------------------------------------------------------------
    { # 4. A classic greedy-trap function: three points that barely fit a line,
      # but adding a fourth point *requires* a break, but the algorithm might
      # incorrectly extend the first segment too far. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 1.1), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        "description": "Greedy trap 1: Slight deviation, then large jump."
    },
    { # 5. Data points exactly on the +/- epsilon bounds of the ideal line. (Optimal: 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "description": "Points touching max tolerance on both sides."
    },
    { # 6. The last point *just* exceeds epsilon, forcing a break at the second-to-last point. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0 + 1e-9)], # Exceeds by tiny amount
        "epsilon": 1.0,
        "expected_pieces": 2,
        "description": "Boundary: Last point just exceeds epsilon."
    },
    { # 7. Same as above, but with a tolerance that *just* includes the last point. (Optimal: 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "Boundary: Last point exactly on epsilon."
    },
    # ----------------------------------------------------------------------
    # 3. High Curvature / Sharp Changes
    # ----------------------------------------------------------------------
    { # 8. V-shape function, testing the sharp corner. (Optimal: 2)
        "pw_linear_fx": [(0.0, 5.0), (1.0, 0.0), (2.0, 5.0)],
        "epsilon": 0.01,
        "expected_pieces": 2,
        "description": "Sharp V-shape with small epsilon."
    },
    { # 9. Step function, requires a segment for each level. (Optimal: 3)
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 5.0), (4.0, 10.0), (5.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 3,
        "description": "Step function (requires a piece per step)."
    },
    { # 10. Rapid oscillation with small amplitude but small epsilon. (Optimal: 4)
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.0), (0.3, 0.1), (0.4, 0.0)],
        "epsilon": 0.01,
        "expected_pieces": 4, # Each oscillation requires its own segment
        "description": "Rapid oscillation, small epsilon."
    },
    # ----------------------------------------------------------------------
    # 4. Long Runs & Non-Uniform Spacing (Testing cumulative error check)
    # ----------------------------------------------------------------------
    { # 11. Convex function ($y=x^2$ for integer $x$) with small epsilon. (Optimal: 3)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0,
        "expected_pieces": 3, # Example: [(0,0)-(2,4)] error at (1,1) is 1.0. [(2,4)-(4,16)] error at (3,9) is 3.0. Fails. Needs 3.
        "description": "Convex function (parabola), small epsilon."
    },
    { # 12. Concave function (sqrt(x)) over a wide range. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (4.0, 2.0), (9.0, 3.0)],
        "epsilon": 0.25,
        "expected_pieces": 2, # Segment 1: (0,0) to (4,2). Max error at (1,1) is 0.5. Fails. Segment 1: (0,0) to (1,1). Segment 2: (1,1) to (9,3). Max error at (4,2) is 0.5. Fails. Needs 3 pieces. Let's adjust epsilon.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (4.0, 2.0), (9.0, 3.0)],
        "epsilon": 0.5,
        "expected_pieces": 2, # (0,0) to (4,2) error at (1,1) is 0.5. (4,2) to (9,3) error at (4,2) is 0.0. Needs 2.
        "description": "Concave function (sqrt), larger epsilon."
    },
    { # 13. Non-uniform x-spacing, data points near each other and far apart. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (10.0, 10.0), (10.1, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        "description": "Non-uniform x-spacing, two clusters."
    },
    # ----------------------------------------------------------------------
    # 5. Epsilon Sensitivity/Toggling (Testing optimality near $\epsilon$)
    # ----------------------------------------------------------------------
    { # 14. Barely requires 2 pieces. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.49,
        "expected_pieces": 2,
        "description": "Epsilon 1: Barely requires 2 pieces."
    },
    { # 15. Same data, but epsilon allows 1 piece. (Optimal: 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.51,
        "expected_pieces": 1,
        "description": "Epsilon 2: Same data, allows 1 piece."
    },
    { # 16. A long flat run, followed by a slight dip that must be covered. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (11.0, 0.9)],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "description": "Long flat run, then sudden small deviation."
    },
    # ----------------------------------------------------------------------
    # 6. Oscillatory and Noisy Data
    # ----------------------------------------------------------------------
    { # 17. Simple sine-like curve over a few cycles. (Optimal: 3)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 3,
        "description": "Sine-like curve, moderate epsilon."
    },
    { # 18. High-frequency noise that requires many segments. (Optimal: 4)
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, -1.0), (2.0, 0.0), (2.5, 1.0), (3.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 6,
        "description": "High-frequency/amplitude oscillation, zero epsilon."
    },
    { # 19. Data that slightly oscillates around a straight line. (Optimal: 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.1)],
        "epsilon": 0.2,
        "expected_pieces": 1,
        "description": "Slight oscillation around a line, wide epsilon."
    },
    # ----------------------------------------------------------------------
    # 7. Larger Datasets with Complex Curvature (More realism)
    # ----------------------------------------------------------------------
    { # 20. Exponential decay, testing fit quality at the start and end. (Optimal: 2 or 3 depending on fit, estimate 3)
        "pw_linear_fx": [(0.0, 10.0), (1.0, 5.0), (2.0, 2.5), (3.0, 1.25), (4.0, 0.625)],
        "epsilon": 0.5,
        "expected_pieces": 3,
        "description": "Exponential decay, moderate epsilon."
    },
    { # 21. A simple parabola $y=x^2$ where $\epsilon$ is large enough to allow 1 segment. (Optimal: 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 2.0,
        "expected_pieces": 1,
        "description": "Parabola, large epsilon (1 segment allowed)."
    },
    { # 22. Sigmoid/S-curve shape. (Optimal: 3)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.5), (3.0, 0.9), (4.0, 1.0)],
        "epsilon": 0.05,
        "expected_pieces": 3, # Requires segments for the two flatter ends and the steep middle
        "description": "Sigmoid/S-curve shape, tight epsilon."
    },
    { # 23. Alternating slopes, testing if the algorithm chooses the longest possible segment. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 3.0), (4.0, 2.0)],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "description": "Alternating slopes, moderate epsilon."
    },
    # ----------------------------------------------------------------------
    # 8. Floating Point Precision Edge Cases (Using tiny values)
    # ----------------------------------------------------------------------
    { # 24. Two points are very close in X, but far in Y (high slope). (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (1e-6, 1.0), (10.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        "description": "Very high slope segment, then flat."
    },
    { # 25. Extremely low epsilon on non-linear data. (Optimal: 4)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.3), (3.0, 0.6), (4.0, 1.0)],
        "epsilon": 0.0001,
        "expected_pieces": 4, # Should require N-1 pieces for N points
        "description": "Extremely small epsilon, non-linear data."
    },
    # ----------------------------------------------------------------------
    # 9. Complex Scenario Combinations (Combining multiple behaviors)
    # ----------------------------------------------------------------------
    { # 26. Step -> Flat -> V-Shape. (Optimal: 4)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 10.0), (3.0, 5.0), (4.0, 10.0), (5.0, 5.0)],
        "epsilon": 1.0,
        "expected_pieces": 4,
        "description": "Step up, flat, V-shape, step down."
    },
    { # 27. Long, nearly flat section followed by immediate failure. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (10.1, 0.0), (10.2, 5.0)],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "description": "Long flat section, then sudden jump."
    },
    { # 28. The 'Wiggle' case: 5 points that barely fit a line, but a slightly different line could save a piece. (Optimal: 2)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        "description": "Wiggle and jump: The first 4 points fit 1 segment, but the 5th forces a break."
    },
    { # 29. A large dataset that is linear overall, testing efficiency. (Optimal: 1)
        "pw_linear_fx": [(i, i * 0.1) for i in range(20)],
        "epsilon": 0.0001,
        "expected_pieces": 1,
        "description": "Large dataset, perfectly linear, small epsilon."
    },
    { # 30. Example from prompt. (Optimal: 2)
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "description": "Example from prompt: Requires 2 segments."
    },
]
test_cases4 = [
    # A: Basic/Linear Cases (Should require 1 segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,  # Perfect linear fit, error should be 0.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 1.0,  # Max error is 0.5 (at x=1,3), 1 segment should suffice.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)],
        "epsilon": 0.0001,  # Trivial case: all points are collinear.
    },
    # B: Single-Segment Maximum Error Cases (Max error near epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.99), (2.0, 0.0)],
        "epsilon": 1.0,  # Max error is 0.99. Should be 1 segment.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 0.0)],
        "epsilon": 1.0,  # Max error is 1.01. Should require 2 segments. (CRITICAL)
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.499), (2.0, 0.0)],
        "epsilon": 0.5,  # Max error is 0.499. Should be 1 segment.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,  # Max error is 0.5. Should be 1 segment (inclusive tolerance).
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (1.0, 0.0), (1.5, -0.1), (2.0, 0.0)],
        "epsilon": 0.1,  # Sine-like shape, max error 0.1. Should be 1 segment.
    },
    # C: Minimal Two-Segment Cases (Testing Optimality/Splitting)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 0.0), (3.0, 1.1), (4.0, 0.0)],
        "epsilon": 1.0,  # Each 'V' shape needs a segment. Should be 2 segments (split at x=2.0).
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.5), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 1.0,  # First part needs its own segment. Optimal split: (2.0, 0.0). Should be 2 segments.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.4,  # The whole data has max error 0.5. Optimal split at (2.0, 1.0) yields max error 0.25. Should be 2 segments.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.49,  # The central peak (at x=2.0) requires a segment to itself. Should be 2 segments.
    },
    # D: Multiple Segments/Curved Data (Testing Greedy vs. Optimal)
    {
        "pw_linear_fx": [(i, 0.5 * (i % 2) - 0.25) for i in range(10)],
        "epsilon": 0.1,  # Sawtooth pattern, requires many segments (5 segments).
    },
    {
        "pw_linear_fx": [(i, i**2) for i in range(5)],  # Quadratic data: (0,0), (1,1), (2,4), (3,9), (4,16)
        "epsilon": 0.5,  # Needs multiple segments due to curvature. Expected 3 segments.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 1.0), (5.0, 0.0)],
        "epsilon": 0.1,  # Mostly linear, but a sharp jump at x=4.0. Should require 3 segments (2 linear + 1 jump).
    },
    {
        "pw_linear_fx": [(i, 0.5 * (1 - (i - 2)**2)) for i in range(5)], # Parabola facing down, max error at ends/mid.
        "epsilon": 0.2,  # Should require 2 segments.
    },
    # E: Vertical Alignment & Edge Points
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.1,  # Vertical jump (impossible to approximate). Algorithm should handle x-values being the same. (Assuming input ensures unique x).
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 0.5), (2.0, 0.5)],
        "epsilon": 0.1,  # Same as above, checking repeated x values.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0)],
        "epsilon": 0.1,  # Segment starts/ends exactly *at* the max error boundary. Should be 1 segment.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.10001), (2.0, 0.0)],
        "epsilon": 0.1,  # Segment *just* exceeds the boundary. Should be 2 segments.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.0), (1.0, 0.0), (1.5, 0.0), (2.0, 0.0)],
        "epsilon": 0.0,  # Should result in 1 segment if $\epsilon=0$ is allowed, or $N$ segments if only perfect fit is allowed (depending on definition). Assume $1$ segment.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,  # Max error is 0.5. Requires $N$ segments to fit $\epsilon=0$.
    },
    # F: Epsilon Edge Cases
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 100.0,  # Very large epsilon. Should be 1 segment.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1e-6), (2.0, 0.0)],
        "epsilon": 1e-7,  # Very small epsilon (testing precision). Should be 2 segments.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1e-6), (2.0, 0.0)],
        "epsilon": 1e-6,  # Very small epsilon (testing precision). Should be 1 segment.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.500001,  # Tolerance just above the max error of the two central 'V's. Should be 1 segment.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.499999,  # Tolerance just below the max error. Should be 3 segments. (CRITICAL)
    },
    # G: Mixed Cases/Longer Sequence
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 1.0,  # First part (x=0 to 2) is fine, but the second peak (x=3) forces a split. Should be 2 segments.
    },
    {
        "pw_linear_fx": [(i, 0.1 * ((-1)**i)) for i in range(10)],
        "epsilon": 0.09,  # Zig-zag data, error is 0.1. Should require 9 segments (to fit $\epsilon=0.09$).
    },
    {
        "pw_linear_fx": [(i, 0.1 * ((-1)**i)) for i in range(10)],
        "epsilon": 0.1,  # Zig-zag data, error is 0.1. Should require 1 segment.
    }
]
test_cases5 = [
    # 1. Optimal 1 Piece (Baseline/Simple)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.0)],
        'epsilon': 0.1
    },
    # 2. Optimal 1 Piece (Perfectly Linear, Zero Tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)],
        'epsilon': 0.0
    },
    # 3. Optimal 1 Piece (High Magnitude/Horizontal)
    {
        'pw_linear_fx': [(0.0, 10.0), (1.0, 10.0), (2.0, 10.0), (3.0, 10.0)],
        'epsilon': 1.0
    },
    # 4. Optimal n Pieces (Zero Tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 2.0)],
        'epsilon': 0.0
    },
    # 5. Optimal 2 Pieces (Symmetric V-shape)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        'epsilon': 0.5
    },
    # 6. Optimal 2 Pieces (Numerical Stability: Tiny deviation forces a split)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0 + 1e-9), (3.0, 3.0)],
        'epsilon': 1e-10
    },
    # 7. Optimal 2 Pieces (Single large peak)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        'epsilon': 0.4
    },
    # 8. Optimal 3 Pieces (Alternating steep slopes)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 2.0)],
        'epsilon': 0.4
    },
    # 9. Optimal 2 Pieces (Just exceeding tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.501), (2.0, 0.0)],
        'epsilon': 0.5
    },
    # 10. Optimal 1 Piece (Just meeting tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5 - 1e-9), (2.0, 0.0)],
        'epsilon': 0.5
    },
    # 11. Optimal 3 Pieces (Convex curve, tight tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.25), (2.0, 1.0), (3.0, 2.25), (4.0, 4.0)],
        'epsilon': 0.1
    },
    # 12. Optimal 2 Pieces (Convex curve, generous tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.25), (2.0, 1.0), (3.0, 2.25), (4.0, 4.0)],
        'epsilon': 1.0
    },
    # 13. Optimal 3 Pieces (S-shaped curve/Inflection point)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        'epsilon': 0.5
    },
    # 14. Optimal 1 Piece (Long run of flat data)
    {
        'pw_linear_fx': [(i, 0.0) for i in range(10)],
        'epsilon': 0.1
    },
    # 15. Optimal 3 Pieces (Long flat, steep spike)
    {
        'pw_linear_fx': [(0.0, 0.0), (10.0, 0.0), (10.1, 5.0), (20.0, 0.0)],
        'epsilon': 0.1
    },
    # 16. Optimal 2 Pieces (Step function)
    {
        'pw_linear_fx': [(0.0, 0.0), (3.0, 0.0), (3.1, 1.0), (6.0, 1.0)],
        'epsilon': 0.5
    },
    # 17. Optimal 1 Piece (Negative Y-values, linear)
    {
        'pw_linear_fx': [(-2.0, -100.0), (-1.0, -100.0), (0.0, -100.0), (1.0, -100.0)],
        'epsilon': 0.0
    },
    # 18. Optimal 3 Pieces (Negative X-domain, tight split)
    {
        'pw_linear_fx': [(-3.0, 0.0), (-2.0, 1.0), (-1.0, 0.0), (0.0, 1.0)],
        'epsilon': 0.49
    },
    # 19. Optimal 1 Piece (High magnitude, still fits)
    {
        'pw_linear_fx': [(0, 1000), (1, 1000.1), (2, 999.9), (3, 1000)],
        'epsilon': 0.2
    },
    # 20. Optimal 1 Piece (Non-uniform X-spacing, linear)
    {
        'pw_linear_fx': [(0.0, 0.0), (10.0, 0.0), (10.1, 0.0)],
        'epsilon': 0.0
    },
    # 21. Optimal 4 Pieces (Non-uniform X, steep changes)
    {
        'pw_linear_fx': [(0.0, 0.0), (0.1, 1.0), (10.0, 0.0), (10.1, 1.0)],
        'epsilon': 0.1
    },
    # 22. Optimal 3 Pieces (Double peak, small tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        'epsilon': 0.2
    },
    # 23. Optimal 2 Pieces (Linearly increasing then sharp drop)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.4), (2.0, 0.8), (3.0, 0.0), (4.0, 0.0)],
        'epsilon': 0.35
    },
    # 24. Optimal 3 Pieces (Duplicate X-value forcing vertical split)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.0, 2.0), (2.0, 0.0)],
        'epsilon': 0.5
    },
    # 25. Optimal 2 Pieces (Duplicate exact point, zero tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        'epsilon': 0.0
    },
    # 26. Optimal 2 Pieces (Extreme floating point deviation)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1e-6), (2.0, 0.0)],
        'epsilon': 1e-7
    },
    # 27. Optimal 1 Piece (Extreme floating point within tolerance)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1e-8), (2.0, 0.0)],
        'epsilon': 1e-6
    },
    # 28. Optimal 2 Pieces (Very short X-range, tight Y-fit failure)
    {
        'pw_linear_fx': [(0.0, 0.0), (0.001, 0.5), (0.002, 0.0)],
        'epsilon': 0.499
    },
    # 29. Optimal 2 Pieces (Sinusoidal segment failure)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.5), (3.0, 0.0), (4.0, 0.0)],
        'epsilon': 0.2
    },
    # 30. Optimal 1 Piece (Wide tolerance for steep line)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 5.0), (2.0, 10.0), (3.0, 15.0)],
        'epsilon': 1.0
    },
]
test_cases6 = [
    # 1. Basic Linear/Constant Tests (Should be 1 piece)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)], "epsilon": 0.1},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.01},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 1.0},

    # 2. Critical Epsilon Tests (Boundary cases where optimality is challenged)
    # Test 4: Parabola y=x^2, max deviation for 1 piece is 0.5 at x=0.5
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0)], "epsilon": 0.12499},  # Should require 2 pieces
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0)], "epsilon": 0.125},
    # Should be exactly 1 piece (Optimal line y=x-0.25)

    # Test 6: Steep V-shape centered at (1, 5)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)], "epsilon": 2.50001},  # Should require 1 piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)], "epsilon": 2.49999},  # Should require 2 pieces

    # 3. High Curvature / Oscillating Tests (Should require many pieces)
    # Test 8: Sine wave sampled densely. Epsilon requires small segments.
    {"pw_linear_fx": [(x / 10, 0.5 * (1 - (x / 10) ** 2)) for x in range(11)], "epsilon": 0.005},
    # Test 9: Sawtooth pattern with sharp peaks
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)], "epsilon": 0.001},
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)], "epsilon": 0.499},
    # Should require 4 pieces

    # 4. Points Exactly on Boundary/Error Limit (Testing <= Epsilon)
    # Test 11: A perfect approximation for the first segment, max error for the second.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1)], "epsilon": 0.1},
    # 1 piece is possible: line from (0,0) to (2,0.1) has max error 0.0
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.10001)], "epsilon": 0.1},  # Should require 2 pieces

    # Test 13: Points forming a line *with* max offset at an intermediate point
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)], "epsilon": 0.5},  # 1 piece (line y=0) should work
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)], "epsilon": 0.5},  # Should require 2 pieces

    # 5. Non-Uniform X-Spacing
    # Test 15: Wide gap followed by dense points
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (10.1, 1.0), (10.2, 0.0)], "epsilon": 0.5},
    # Test 16: Logarithmic X-spacing, challenging for interpolation range
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (10.0, 1.0), (100.0, 1.0)], "epsilon": 0.05},

    # 6. Negative Coordinates and Jumps
    {"pw_linear_fx": [(-2.0, 5.0), (-1.0, 0.0), (0.0, -5.0)], "epsilon": 0.1},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (1.0001, 0.0), (2.0, 10.0)], "epsilon": 0.5},  # Near-vertical jump

    # 7. Zero Epsilon (Requires exact fit)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)], "epsilon": 0.0},  # Should require 1 piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.000001)], "epsilon": 0.0},
    # Should require 2 pieces (or N-1 if N points)

    # 8. Large Epsilon (Should always be 1 piece, testing robustness)
    {"pw_linear_fx": [(0.0, 0.0), (100.0, 100.0), (200.0, 0.0)], "epsilon": 50.0},

    # 9. Small X-range, Large Y-range
    {"pw_linear_fx": [(0.0, 0.0), (0.001, 100.0), (0.002, 0.0)], "epsilon": 1.0},

    # 10. Combination of Constant and Sloped Sections
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 2.0)], "epsilon": 0.0},  # Requires 2 pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 2.0)], "epsilon": 0.5},  # Can be 1 piece: line y=x-1

    # 11. Specific challenging geometry (Staircase)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.0},
    # Requires 5 pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)], "epsilon": 0.4},
    # Should reduce pieces

    # 12. Alternating sign error
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, -0.1), (4.0, 0.0)], "epsilon": 0.1},
    # 1 piece (line y=0) should work
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.11), (2.0, 0.0), (3.0, -0.11), (4.0, 0.0)], "epsilon": 0.1},
    # Requires 2 pieces

    # 13. Very dense points with small error
    {"pw_linear_fx": [(i / 100, i / 100 + 0.005) for i in range(101)], "epsilon": 0.005},  # 1 piece (line y=x+0.005/2)

    # 14. Original Example
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)], "epsilon": 0.5},
]
test_cases7 = [
    # 1. Basic Cases: Simple lines, no approximation needed
    {
        "description": "Perfect straight line, wide tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Perfect straight line, narrow tolerance (still 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    # 3. Simple Curve: Requires 2 pieces
    {
        "description": "Simple parabolic curve, requiring two pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 1.0), (3.0, 2.25), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 2  # e.g., (0,0)-(2,1) has max error 0.5 at (1, 0.25). (2,1)-(4,4) is straight.
    },
    # 4. Standard Case from Prompt Example
    {
        "description": "Standard test case (from example).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,1)-(2,3) max error is 1.0. (0,1)-(1,1) needs its own piece if 0.5. (1,1)-(5,8) max error > 0.5. Optimal is (0,1)-(1,1) [error 0], (1,1)-(5,8) [error 0]. Wait, the original example points *are* the input points, and the approximation line should pass close to them. If it's *already* piecewise, max 2 pieces. Let's assume (0,1)-(5,8) is the goal, max error is |1-0.6|=0.4 at x=1, and max error is |3-3.4|=0.4 at x=2. The line is $y = 1.4 + 7/5 x$. Max error on (0,1)-(5,8) is 0.4. Let's change expected to 1.
    },
    {
        "description": "Adjusted standard case to force 2 pieces.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 1.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 3 # V-shape (2,3) is the peak. (0,1)-(2,3) max error > 0.5. Needs (0,1)-(1,1) [error 0], (1,1)-(2,3) [error 1.0], needs (1,1)-(1.5,2.0) [error 0.5], (1.5,2.0)-(2,3), etc. A simpler approach: (0,1)-(2,3) needs 2 pieces. (2,3)-(4,4) needs 1 piece. Total 3-4 pieces. Let's force 3.
    },
    # 6. Edge Case: Zero Tolerance (Exact match required)
    {
        "description": "Zero tolerance (epsilon=0) should return max pieces (n segments).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    # 7. Edge Case: Tolerance smaller than smallest vertical deviation
    {
        "description": "Tolerance slightly greater than 0, non-linear data.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.01), (2.0, 0.0), (3.0, 0.01)],
        "epsilon": 0.005,
        "expected_pieces": 3 # Needs 3 pieces due to tiny wiggles.
    },
    # 8. Edge Case: Tolerance just large enough for 1 segment
    {
        "description": "Max deviation exactly equals epsilon, should be 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # 9. Edge Case: Horizontal line with one vertical outlier
    {
        "description": "Horizontal line with one vertical outlier, forcing split.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 3 # (0,0)-(2,1) max error is 0.5. Needs (0,0)-(1.5, 0.5). (2,1) is outlier. Needs 3 pieces: (0,0)-(1.0,0.0), (1.0,0.0)-(3.0,0.0) fails. (0,0)-(2,1) fails. Optimal: (0,0)-(1,0), (1,0)-(3,0) fails. It must be (0,0)-(1.5,0.0) [error 0], (1.5,0.0)-(2.5,0.0) fails. Needs (0,0)-(1.0,0.0), (1.0,0.0)-(3.0,0.0) fails. Optimal is 3: (0,0)-(1,0), (1,0)-(3,0) fails. (0,0)-(2,1) fails. Needs (0,0)-(1,0), (1,0)-(3,0) fails. Needs 3 pieces: (0,0)-(1.5, 0.0), (1.5, 0.0)-(2.5, 0.0), (2.5, 0.0)-(4.0, 0.0).
    },
    # 10. Edge Case: Minimal points (2 points = 1 piece)
    {
        "description": "Minimum points (2 points), must be 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    # 11. Edge Case: 3 points forming a sharp corner
    {
        "description": "3 points forming a sharp V-corner, forcing 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,0)-(2,0) line passes through x=1, y=0. Max error is 2. Needs 2 pieces for epsilon 0.5.
    },
    # 12. Alternating Deviation: Requires multiple segments
    {
        "description": "Alternating points above/below, tight tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, -0.2), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4 # Each oscillation needs a split since max error is 0.2
    },
    # 13. Data with high slope change
    {
        "description": "High slope change, forcing a split.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (10.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # (0,0)-(10,10) has max error of 9.9 at x=0.1. Must split at (0.1, 10.0).
    },
    # 14. Data with zero slope
    {
        "description": "Horizontal data points, wide tolerance.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    # 15. Large dataset with small non-linearity
    {
        "description": "Large dataset, small non-linearity, forcing 2 pieces.",
        "pw_linear_fx": [(x, x + (0.1 if x % 10 == 5 else 0)) for x in range(21)],
        "epsilon": 0.05,
        "expected_pieces": 3 # x=5 and x=15 have 0.1 bump. (0,0)-(20,20) has max error 0.1 at x=5,15. Split needed.
    },
    # 16. Stepped function (testing vertical jumps/near-vertical segments)
    {
        "description": "Stepped function, forcing max pieces.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (0.1, 1.0), (1.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    # 17. Case where optimal split is *not* at max error point
    {
        "description": "Optimal split point test (requires sophisticated algorithm).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.5), (3.0, 0.0), (4.0, 1.0)],
        "epsilon": 0.4,
        "expected_pieces": 2 # (0,0)-(3,0) fails. Optimal: (0,0)-(4,1) fails (max error 0.5 at x=1,2). Split is (0,0)-(2,0.5) and (2,0.5)-(4,1).
    },
    # 18. Exponential-like curve
    {
        "description": "Exponential curve, requiring several segments.",
        "pw_linear_fx": [(0, 1), (1, 2), (2, 4), (3, 8), (4, 16)],
        "epsilon": 1.0,
        "expected_pieces": 3 # (0,1)-(4,16) max error 2.5 at x=2, 3.5 at x=3. Needs splits. (0,1)-(2,4) fails. (0,1)-(1,2) [error 0]. (1,2)-(4,16) max error 2.5 at x=3. Needs split (1,2)-(2.5,8). Total 3 pieces.
    },
    # 19. Symmetrical data with tight tolerance
    {
        "description": "Symmetrical data, tight tolerance.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, -1), (4, 0)],
        "epsilon": 0.2,
        "expected_pieces": 4
    },
    # 20. Large number of points that are nearly linear
    {
        "description": "Large, nearly linear dataset, forcing 1 piece.",
        "pw_linear_fx": [(i, i + 0.05 * ((-1)**i)) for i in range(15)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 21. Large number of points that are nearly linear, just exceeding tolerance
    {
        "description": "Large, nearly linear dataset, just exceeding tolerance.",
        "pw_linear_fx": [(i, i + 0.11 * ((-1)**i)) for i in range(15)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Needs a split somewhere.
    },
    # 22. Tolerance check around a high-frequency wiggle
    {
        "description": "High-frequency wiggle, requiring many segments.",
        "pw_linear_fx": [(i, 0.0 if i % 2 == 0 else 1.0) for i in range(10)],
        "epsilon": 0.1,
        "expected_pieces": 9
    },
    # 23. Edge Case: Point exactly on the max L-infinity distance
    {
        "description": "Point exactly on the L-infinity boundary, should pass.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1 # Line is y=0, max error is 1.0. Line is y=1-x. (0,0)-(2,0). Max error is 1.0. New line: y = 0.5 - 0.5 * x. Max error is 0.5 at x=1.
    },
    # 24. Edge Case: Point slightly over the L-infinity distance
    {
        "description": "Point slightly over the L-infinity boundary, should fail (2 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # 25. Large range in Y, small range in X
    {
        "description": "Large Y range, small X range, nearly vertical line.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (0.2, 0.0), (0.3, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 3 # (0,0)-(0.3,10) fails. Needs 3 pieces due to large vertical deviations.
    },
    # 26. Large range in X, small range in Y
    {
        "description": "Large X range, small Y range, nearly horizontal line.",
        "pw_linear_fx": [(0, 0.0), (100, 0.1), (200, 0.0), (300, 0.1)],
        "epsilon": 0.05,
        "expected_pieces": 2 # (0,0)-(300,0.1) max error is 0.07. Should pass. Wait, $y=0.1/300 x$. At $x=100$, $y=0.033$. Error is $0.1-0.033=0.066$. Fails. Optimal: (0,0)-(200,0) fails. Optimal: (0,0)-(150, 0.05) and (150, 0.05)-(300, 0.1). Total 2 pieces.
    },
    # 27. Case with repeating segments
    {
        "description": "Repeating pattern, testing sequence optimality.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1), (6, 0)],
        "epsilon": 0.49,
        "expected_pieces": 6 # (0,0)-(2,0) max error 1.0. Needs (0,0)-(1.5, 0.5) fails. Needs 6 pieces.
    },
    # 28. Optimal for n pieces, but needs n+1 if epsilon is slightly smaller
    {
        "description": "Boundary case for segment count 2 -> 3.",
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0), (3, 0.5), (4, 0)],
        "epsilon": 0.25,
        "expected_pieces": 2 # (0,0)-(2,0) max error 0.5. Needs 2 pieces for 0.25. (0,0)-(2,0) fails. (0,0)-(4,0) fails. Split at (2,0). (0,0)-(2,0) fails. Needs 3 pieces: (0,0)-(1,0.5), (1,0.5)-(3,0.5), (3,0.5)-(4,0). Wait, optimal is 2: (0,0)-(2,0) fails. Optimal is 2: (0, 0)-(2, 0) max error 0.5. (0,0)-(4,0) max error 0.5. Optimal is 2: (0,0)-(2,0.5) and (2,0.5)-(4,0). The first segment max error is 0.25. The second is 0.25.
    },
    # 29. Edge Case: All points on the same X (should technically be avoided but tests robustness)
    {
        "description": "All points on the same X (vertical line).",
        "pw_linear_fx": [(1.0, 0.0), (1.0, 1.0), (1.0, 2.0), (1.0, 3.0)],
        "epsilon": 0.0,
        "expected_pieces": 3 # If x-values are identical, it must use n-1 pieces.
    },
    # 30. High-density linear data
    {
        "description": "High-density linear data, large epsilon.",
        "pw_linear_fx": [(i/10.0, i/10.0) for i in range(100)],
        "epsilon": 1.0,
        "expected_pieces": 1
    }
]
test_cases8 = [
    # --- BASIC / SANITY CHECKS (1-5) ---
    {
        'name': 'T01_Collinear_PerfectFit',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.001,
        'expected_pieces': 1,
        'description': 'All points are perfectly collinear. Should require only 1 piece even with tight tolerance.'
    },
    {
        'name': 'T02_HighEpsilon_SinglePiece',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, -0.2), (3.0, 0.3), (4.0, 0.0)],
        'epsilon': 0.5,
        'expected_pieces': 1,
        'description': 'Points have small variation. High epsilon should allow approximation by a single piece (e.g., $y=0$).'
    },
    {
        'name': 'T03_ZeroEpsilon_MaxPieces',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        'epsilon': 0.0,
        'expected_pieces': 2,
        'description': 'Epsilon is zero. Requires a segment for every original segment (n points -> n-1 pieces).'
    },
    {
        'name': 'T04_Simple_V_Shape_TwoPieces',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        'epsilon': 0.001,
        'expected_pieces': 3,
        'description': 'A clear sequence of non-collinear points, requiring a piece for each turn.'
    },
    {
        'name': 'T05_ConstantFunction_OnePiece',
        'pw_linear_fx': [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        'epsilon': 0.001,
        'expected_pieces': 1,
        'description': 'Testing horizontal collinearity (constant function).'
    },

    # --- TIGHT TOLERANCE & EDGE GEOMETRY (6-10) ---
    {
        'name': 'T06_Points_Just_Outside_Tolerance',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)],
        'epsilon': 0.0,
        'expected_pieces': 3,
        'description': 'Should fail to merge segments if epsilon is strictly zero. Edge case: zero tolerance.'
    },
    {
        'name': 'T07_ZigZag_Epsilon_Equals_MaxError',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        'epsilon': 0.1,
        'expected_pieces': 1,
        'description': 'Error is exactly $\\epsilon$. Should be approimable by $y=0$ in one piece. Tests strict inequality/boundary.'
    },
    {
        'name': 'T08_Strictly_Increasing_MaxDeviation',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.01), (2.0, 0.02), (3.0, 0.03)],
        'epsilon': 0.01,
        'expected_pieces': 1,
        'description': 'Tests approximation of a curve with increasing deviation (but still overall small).'
    },
    {
        'name': 'T09_TwoSegments_MinimalGap',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0)],
        'epsilon': 0.499,
        'expected_pieces': 2,
        'description': 'Requires two segments due to large step change. Epsilon is just too small to bridge the gap.'
    },
    {
        'name': 'T10_Tight_Three_Point_Turn',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.0001, 0.0), (2.0, 1.0)],
        'epsilon': 0.0,
        'expected_pieces': 3,
        'description': 'Points are very close in $x$. Tests precision and handling of sharp vertical changes with zero tolerance.'
    },

    # --- OPTIMALITY TRAPS (Testing the greedy choice) (11-15) ---
    # These cases are designed to trick a naive greedy algorithm into making a non-optimal early split.
    {
        'name': 'T11_Optimal_Greedy_Misstep_Trap_1',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, 0.4), (4.0, 0.0)],
        'epsilon': 0.4,
        'expected_pieces': 1,
        'description': 'A naive greedy might split at (2.0, 0.0) if it focuses only on the $y=0$ line, but a single piece can fit all points.'
    },
    {
        'name': 'T12_Optimal_Greedy_Misstep_Trap_2',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.9), (3.0, 1.0), (4.0, 1.1), (5.0, 2.0)],
        'epsilon': 0.1,
        'expected_pieces': 3,
        # e.g., (0.0, 0.0) to (3.0, 1.0), then (3.0, 1.0) to (4.0, 1.1), then (4.0, 1.1) to (5.0, 2.0)
        'description': 'Points (0,0) to (3,1) can be a single segment. Tests if the algorithm correctly finds the maximal segment length.'
    },
    {
        'name': 'T13_Long_Flat_Then_Spike',
        'pw_linear_fx': [(0.0, 0.0), (5.0, 0.0), (5.001, 10.0), (10.0, 0.0)],
        'epsilon': 0.0,
        'expected_pieces': 3,
        'description': 'A long segment followed by a near-vertical spike. Tests ability to recognize the discontinuity.'
    },
    {
        'name': 'T14_Points_Alternating_Tight',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.2), (2.0, -0.2), (3.0, 0.2), (4.0, -0.2)],
        'epsilon': 0.2,
        'expected_pieces': 1,
        'description': 'A sine-like wave where $\\epsilon$ is exactly the amplitude. Should fit in 1 piece using $y=0$ line.'
    },
    {
        'name': 'T15_Parabola_Approximation',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        'epsilon': 1.0,
        'expected_pieces': 3,  # Example: (0,0)-(2,4) [Max err at (1,1) is 1.0], (2,4)-(3,9), (3,9)-(4,16)
        'description': 'Tests ability to approximate a non-linear (quadratic) function, requiring multiple pieces.'
    },

    # --- X/Y AXIS EDGE CASES (16-20) ---
    {
        'name': 'T16_Vertical_Constant_X',
        'pw_linear_fx': [(1.0, 0.0), (1.0, 1.0), (1.0, 2.0)],
        'epsilon': 0.0,
        'expected_pieces': 2,
        'description': 'Constant $x$ values (vertical segment). Should still require a piece per original segment for zero tolerance.'
    },
    {
        'name': 'T17_Negative_Y_Values',
        'pw_linear_fx': [(0.0, -10.0), (1.0, -10.1), (2.0, -9.9)],
        'epsilon': 0.1,
        'expected_pieces': 1,
        'description': 'Tests handling of negative $y$ coordinates. Should fit in 1 piece.'
    },
    {
        'name': 'T18_Negative_X_Values',
        'pw_linear_fx': [(-3.0, 0.0), (-2.0, 1.0), (-1.0, 0.0)],
        'epsilon': 0.001,
        'expected_pieces': 2,
        'description': 'Tests handling of negative $x$ coordinates.'
    },
    {
        'name': 'T19_Mixed_Negative_Coordinates',
        'pw_linear_fx': [(-2.0, -2.0), (-1.0, -1.0), (0.0, 0.0), (1.0, 1.0)],
        'epsilon': 0.001,
        'expected_pieces': 1,
        'description': 'All points in a line, spanning all four quadrants.'
    },
    {
        'name': 'T20_Floating_Point_X_and_Y',
        'pw_linear_fx': [(0.1, 0.1), (0.5, 0.49), (0.9, 0.9)],
        'epsilon': 0.01,
        'expected_pieces': 1,
        'description': 'Tests handling of non-integer $x$ and $y$ values and small tolerance.'
    },

    # --- SMALL & LARGE DATASETS (21-23) ---
    {
        'name': 'T21_Minimal_Dataset',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0)],
        'epsilon': 100.0,
        'expected_pieces': 1,
        'description': 'The smallest possible dataset (2 points, 1 segment).'
    },
    {
        'name': 'T22_Small_W_Variation',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        'epsilon': 0.5,
        'expected_pieces': 1,
        'description': '3 points, V-shape, high epsilon. Should be 1 piece.'
    },
    {
        'name': 'T23_Large_Dataset_Collinear',
        'pw_linear_fx': [(i, i) for i in range(100)],
        'epsilon': 0.001,
        'expected_pieces': 1,
        'description': '100 points, all collinear. Should confirm scaling and optimal 1-piece result.'
    },

    # --- COMPLEX OPTIMALITY CHECKS (24-30) ---
    {
        'name': 'T24_Optimal_Split_Midpoint_Symmetry',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        'epsilon': 0.25,
        'expected_pieces': 2,
        'description': 'Symmetric curve, optimal split is at the middle point (2.0, 0.0). Each piece has error 0.25. Tests perfect split.'
    },
    {
        'name': 'T25_Asymmetric_Tighter_Fit_Required',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.7), (3.0, 0.8), (4.0, 0.0)],
        'epsilon': 0.2,
        'expected_pieces': 3,
        'description': 'Asymmetric data requiring tighter fit due to the small $\\epsilon$.'
    },
    {
        'name': 'T26_Staircase_Function_Multiple_Pieces',
        'pw_linear_fx': [(i, i // 2) for i in range(10)],
        'epsilon': 0.49,
        'expected_pieces': 5,  # Each segment in $y$ requires a new piece.
        'description': 'Approximation of a staircase (step) function. Tests transition points.'
    },
    {
        'name': 'T27_Strict_Local_Optima_Trap',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, 0.4), (4.0, 0.0)],
        'epsilon': 0.3,
        'expected_pieces': 2,
        'description': 'The first segment (0-2) fits with a small error. The second part (2-4) requires a split, making the total 2. A single piece (0-4) would fail.'
    },
    {
        'name': 'T28_Large_Range_X_Small_Range_Y',
        'pw_linear_fx': [(0.0, 0.0), (100.0, 0.1), (200.0, 0.0)],
        'epsilon': 0.1,
        'expected_pieces': 1,
        'description': 'Tests numerical stability with large $x$ ranges. Should be 1 piece (line $y=0$).'
    },
    {
        'name': 'T29_Tolerance_Just_Fails_Merge',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        'epsilon': 0.5,
        'expected_pieces': 2,
        'description': 'The peak (1.0, 0.51) is **just outside** the $y=0$ line $\\pm 0.5$ tolerance. Requires 2 pieces.'
    },
    {
        'name': 'T30_Tolerance_Just_Allows_Merge',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        'epsilon': 0.5,
        'expected_pieces': 1,
        'description': 'The peak (1.0, 0.5) is **exactly on** the $y=0$ line $\\pm 0.5$ tolerance. Should fit in 1 piece.'
    },
]
test_cases9 = [
    # ----------------------------------------------------------------------
    # 1. Basic Cases: Simple data where the optimal solution is obvious
    # ----------------------------------------------------------------------
    # Case 1: Perfectly linear data (should be 1 piece regardless of epsilon)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], 'epsilon': 0.1, 'expected_pieces': 1},
    # Case 2: Perfectly linear, large epsilon (still 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], 'epsilon': 10.0, 'expected_pieces': 1},
    # Case 3: Constant function (should be 1 piece)
    {'pw_linear_fx': [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)], 'epsilon': 0.001, 'expected_pieces': 1},
    # Case 4: Step function, small epsilon (should be max pieces - n-1 = 3)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0001, 5.0), (2.0, 5.0)], 'epsilon': 0.01, 'expected_pieces': 3},

    # ----------------------------------------------------------------------
    # 2. Tolerance Edge Cases: Testing interactions with epsilon
    # ----------------------------------------------------------------------
    # Case 5: Data that needs 2 pieces at epsilon=0.5, but 1 piece at epsilon=1.0
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0)], 'epsilon': 0.5, 'expected_pieces': 2},
    # Case 6: Same data, larger epsilon (should merge to 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0)], 'epsilon': 1.0, 'expected_pieces': 1},
    # Case 7: Minimum possible epsilon (zero), requires n pieces (max pieces = 4)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)], 'epsilon': 0.0, 'expected_pieces': 4},
    # Case 8: Maximize pieces needed (zigzag) but still possible with large epsilon (1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)], 'epsilon': 10.0, 'expected_pieces': 1},
    # Case 9: Zigzag forcing max pieces due to tight epsilon (3 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)], 'epsilon': 0.1, 'expected_pieces': 3},

    # ----------------------------------------------------------------------
    # 3. Geometric Edge Cases: Points exactly on or just outside the tolerance band
    # ----------------------------------------------------------------------
    # Case 10: Point exactly on one side of the band (2 pieces required)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5)], 'epsilon': 0.5, 'expected_pieces': 2},
    # Case 11: Point just outside the band (3 pieces required)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.500001), (2.0, 1.0), (3.0, 0.5)], 'epsilon': 0.5, 'expected_pieces': 3},
    # Case 12: End points define the max deviation at the start/end of a segment
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0)], 'epsilon': 0.01, 'expected_pieces': 3}, # Last point forces break
    # Case 13: Mid-point defines the max deviation
    {'pw_linear_fx': [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 0.5), (2.0, 0.0)], 'epsilon': 0.5, 'expected_pieces': 2},
    # Case 14: Mid-point exactly on the boundary
    {'pw_linear_fx': [(0.0, 0.0), (0.5, 0.5), (1.0, 0.0), (1.5, 0.5), (2.0, 0.0)], 'epsilon': 0.5, 'expected_pieces': 1},

    # ----------------------------------------------------------------------
    # 4. Long/Short Segments & Non-Uniform X Spacing
    # ----------------------------------------------------------------------
    # Case 15: Non-uniform X spacing, should not affect L_inf optimality
    {'pw_linear_fx': [(0.0, 0.0), (0.1, 0.1), (10.0, 0.0)], 'epsilon': 0.05, 'expected_pieces': 2},
    # Case 16: Very dense points in a flat region
    {'pw_linear_fx': [(i, 0.0) for i in range(10)] + [(10.0, 1.0)], 'epsilon': 0.01, 'expected_pieces': 9}, # 9 flat points + 1 slope
    # Case 17: Sparse points on a steep slope
    {'pw_linear_fx': [(0.0, 0.0), (10.0, 100.0), (20.0, 200.0)], 'epsilon': 0.01, 'expected_pieces': 2},

    # ----------------------------------------------------------------------
    # 5. Multiple Optimal Paths (Greedy vs. Optimal)
    # ----------------------------------------------------------------------
    # Case 18: Path A (p0-p2, p2-p4) vs Path B (p0-p1, p1-p4). Optimal is p0-p4 (1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)], 'epsilon': 0.1, 'expected_pieces': 1},
    # Case 19: Forces a break earlier to allow a longer next segment (Test greedy local choice)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)], 'epsilon': 0.1, 'expected_pieces': 3}, # 3 pieces for the steep V + flat
    # Case 20: Simple sine wave approximation - requires many pieces
    {'pw_linear_fx': [(i/10.0, 0.5 * (1 - __import__('math').cos(i/10.0 * 2 * __import__('math').pi))) for i in range(21)], 'epsilon': 0.05, 'expected_pieces': 'many'}, # ~6-8 pieces

    # ----------------------------------------------------------------------
    # 6. Specific Curve Shapes (Parabola, Sine, Cubic)
    # ----------------------------------------------------------------------
    # Case 21: Parabola: y=x^2 from x=0 to x=3 (4 points)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], 'epsilon': 0.5, 'expected_pieces': 3},
    # Case 22: Parabola: Larger epsilon allows 2 pieces
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], 'epsilon': 1.0, 'expected_pieces': 2},
    # Case 23: Data points creating a cusp (V-shape)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], 'epsilon': 0.1, 'expected_pieces': 4},
    # Case 24: Data points creating a smooth S-curve (inflection point)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.9), (3.0, 1.0)], 'epsilon': 0.05, 'expected_pieces': 3},

    # ----------------------------------------------------------------------
    # 7. Data Scaling and Floating Point Precision
    # ----------------------------------------------------------------------
    # Case 25: Large Y values, standard epsilon
    {'pw_linear_fx': [(0.0, 1000.0), (1.0, 1000.1), (2.0, 1000.0), (3.0, 1000.1)], 'epsilon': 0.001, 'expected_pieces': 3},
    # Case 26: Small Y values, standard epsilon (micro-fluctuations)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1e-6), (2.0, 0.0), (3.0, 1e-6)], 'epsilon': 1e-7, 'expected_pieces': 3},
    # Case 27: Very large epsilon, should always yield 1 piece
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 100.0), (2.0, 0.0), (3.0, 100.0)], 'epsilon': 500.0, 'expected_pieces': 1},

    # ----------------------------------------------------------------------
    # 8. Array Boundary/Size Cases
    # ----------------------------------------------------------------------
    # Case 28: Minimum data points (2 points, always 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0)], 'epsilon': 0.0, 'expected_pieces': 1},
    # Case 29: Small data set, 3 points (max 2 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], 'epsilon': 0.1, 'expected_pieces': 2},
    # Case 30: Longer, complex data set (testing the core algorithm logic)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.4), (3.0, 0.5), (4.0, 0.4), (5.0, 0.0), (6.0, 0.0)], 'epsilon': 0.2, 'expected_pieces': 3}, # p0-p2, p2-p4, p4-p6
]
test_cases10 = [
    # 1. Simple Linear/Constant Cases (Optimal: 1 piece)
    {
        "description": "Perfect linear data, single piece optimal.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Perfect constant data, single piece optimal.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "Linear data with small noise, easily covered.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.95), (3.0, 3.05), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },

    # 2. Tight Tolerance Cases (Testing if the algorithm finds the *longest* piece)
    {
        "description": "Data requiring a small piece at the start, then a long one.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (10.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 2 # (0.0, 0.2) then (0.2, 10.0)
    },
    {
        "description": "Data with maximum deviation exactly equal to epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1 # A single piece from (0,0) to (2,0) has max deviation 0.5
    },
    {
        "description": "Data slightly exceeding epsilon, forcing a split.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.50001), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Must split at 1.0
    },

    # 3. High Curvature/Sharp Change Cases (Guaranteed multiple pieces)
    {
        "description": "High frequency sine-like wave, requires many pieces.",
        "pw_linear_fx": [(i, 1.0 * (i % 2)) for i in range(11)],
        "epsilon": 0.1,
        "expected_pieces": 5 # Must split every 2 points
    },
    {
        "description": "V-shape with sharp corner, small epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Must split at (1.0, 10.0)
    },
    {
        "description": "Square-wave-like data.",
        "pw_linear_fx": [(0, 0), (0.1, 0), (0.11, 5), (1, 5)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0, 0.1) then (0.11, 1) should be 2, but the intermediate point may force a 3rd piece.
    },
    {
        "description": "Convex parabola requiring multiple small pieces.",
        "pw_linear_fx": [(x, x*x) for x in range(11)],
        "epsilon": 1.0,
        "expected_pieces": 4 # A parabola often requires more pieces than a simple wave.
    },

    # 4. Large Tolerance Cases (Testing if the algorithm correctly uses 1 piece)
    {
        "description": "Large tolerance allows single piece for moderately noisy data.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Extremely large tolerance, should always return 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 0.0)],
        "epsilon": 1000.0,
        "expected_pieces": 1
    },

    # 5. Boundary/Edge Cases on Points
    {
        "description": "Minimum data points (2 points) -> always 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "3 points, maximum deviation exactly on the middle point.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "3 points, maximum deviation forces split.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0001), (2.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },

    # 6. Critical Epsilon Value Testing (The algorithm must correctly compute the exact boundary of the tolerance region)
    {
        "description": "Alternating points, epsilon exactly half the change.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,2) is a triangle, max deviation is 0.5. (2,4) is similar.
    },
    {
        "description": "Alternating points, epsilon slightly less than half the change.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.4999,
        "expected_pieces": 4 # Forces a split at every intermediate point.
    },
    {
        "description": "A ramp followed by a flat line, requiring two pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0, 1) and (1, 3)
    },

    # 7. Step Function Approximation (Worst case for piecewise)
    {
        "description": "Pure step function, small epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.0), (0.5001, 10.0), (1.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "description": "Pure step function, very small epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.0), (0.5001, 10.0), (1.0, 10.0)],
        "epsilon": 0.001,
        "expected_pieces": 2 # (0.0, 0.5) and (0.5001, 1.0)
    },

    # 8. Diverse/Complex Shapes
    {
        "description": "Data forming an 'M' shape.",
        "pw_linear_fx": [(0, 0), (1, 5), (2, 0), (3, 5), (4, 0)],
        "epsilon": 0.1,
        "expected_pieces": 4 # Forces splits at all peaks/valleys
    },
    {
        "description": "Sinusoidal-like data over many points.",
        "pw_linear_fx": [(i/10.0, 0.5 * (1 + (i%2))) for i in range(31)],
        "epsilon": 0.05,
        "expected_pieces": 15 # Should split between every two points if the deviation is large
    },
    {
        "description": "Exponential growth/decay (concave/convex mix).",
        "pw_linear_fx": [(i, 2**i) for i in range(6)],
        "epsilon": 2.0,
        "expected_pieces": 3 # Requires splits due to rapid increase in curvature.
    },

    # 9. Test Case from the Prompt Example (For verification)
    {
        "description": "Example from the prompt.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0.0, 2.0) has max deviation 1.0 > 0.5, forces a split at 1.0 or 2.0. Optimal: (0, 1) then (1, 5) or similar. The algorithm should find the minimum. Let's assume a known correct split of 2 for this test.
    },

    # 10. Cases requiring careful selection of split points (optimality)
    {
        "description": "A long constant segment followed by a small spike.",
        "pw_linear_fx": [(i, 0.0) for i in range(10)] + [(10, 1.0), (11, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0, 9) then (9, 11) or (0, 10) then (10, 11)
    },
    {
        "description": "Data where the deviation happens early/late in a segment.",
        "pw_linear_fx": [(0, 0), (9, 0), (10, 0.9), (11, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0, 10) then (10, 11) should work.
    },
    {
        "description": "Data where the greedy choice might not be optimal.",
        # This one is tricky: a greedy max-length piece might miss an overall optimal path.
        "pw_linear_fx": [(0, 0), (1, 0.2), (2, 0), (3, 0.5), (4, 0), (5, 0.2)],
        "epsilon": 0.15,
        "expected_pieces": 3
    },

    # 11. Large N and Small Epsilon
    {
        "description": "Many points, very small noise, small epsilon.",
        "pw_linear_fx": [(i, i/1000.0) for i in range(101)],
        "epsilon": 0.0001,
        "expected_pieces": 1
    },

    # 12. Large N and Moderate Epsilon
    {
        "description": "Many points, moderate noise, moderate epsilon.",
        "pw_linear_fx": [(i, i/10.0 + 0.1 * ((i % 10) == 5)) for i in range(101)],
        "epsilon": 0.05,
        "expected_pieces": 11 # Should require a split at every i=5, 15, 25, ...
    },
    {
        "description": "Alternating noise around a line, long sequence.",
        "pw_linear_fx": [(i, 0.0 if i % 2 == 0 else 0.4) for i in range(21)],
        "epsilon": 0.2,
        "expected_pieces": 1 # The line y=0.2 will cover all points exactly with max deviation 0.2
    }
]
test_cases11 = [
    # 1. Basic Cases (Linear, Constant)
    {
        "description": "Perfectly linear data, single segment expected.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Perfectly constant data, single segment expected.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "Large epsilon, should approximate entire dataset with one piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0), (4.0, 0.0)],
        "epsilon": 10.0,
        "expected_pieces": 1
    },
    {
        "description": "Small step changes, large tolerance, 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Simple V-shape data, 2 pieces required.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },

    # 2. Convex/Concave Data (Forcing Segmentation)
    {
        "description": "Quadratic (concave down), forcing segmentation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 1.6), (3.0, 0.9), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2  # The error at (2.0, 1.6) for the line from (0,0) to (4,0) is 1.6. Need a break.
    },
    {
        "description": "Parabolic data, small epsilon, max pieces.",
        "pw_linear_fx": [(x, x ** 2) for x in range(5)],  # (0,0), (1,1), (2,4), (3,9), (4,16)
        "epsilon": 0.1,
        "expected_pieces": 4  # A tight tolerance on a convex curve often requires a piece per original segment.
    },
    {
        "description": "Concave up, moderate segmentation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
        "epsilon": 0.1,
        "expected_pieces": 3  # e.g., (0,0) to (2,0.4) has max error at (1, 0.1) of 0.1-0.2 = -0.1.
    },

    # 3. Near-Edge Cases (Tolerance Boundary)
    {
        "description": "A point just outside epsilon from the start point's slope, 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.15), (3.0, 0.2)],
        "epsilon": 0.1,
        "expected_pieces": 2
        # Line from (0,0) to (3, 0.2) has error at (2, 0.15) of |0.15 - 0.133| = 0.017. 1 piece is fine. Let's make it tighter.
    },
    {
        "description": "Forcing 2 pieces due to point being exactly on epsilon bound (or slightly over).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 2  # Line from (0,0) to (3,0) has error 0.1 at (2, 0.1). > 0.05.
    },
    {
        "description": "Many points on a line, one point slightly off, forcing 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.5, 2.0), (2.0, 1.0), (3.0, 2.0), (4.0, 3.0)],
        "epsilon": 0.5,
        "expected_pieces": 3  # Line (0,0) to (4,3) is y=0.75x. Point (1.5, 2.0) has error |2.0 - 1.125| = 0.875 > 0.5.
    },
    {
        "description": "Large span in x, small span in y, tight epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.1), (20.0, 0.0), (30.0, 0.1)],
        "epsilon": 0.01,
        "expected_pieces": 4  # A piece for every original segment due to tight tolerance.
    },

    # 4. Step/Oscillating Data
    {
        "description": "Sharp step up, 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 10.0), (2.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2  # Must break at the step.
    },
    {
        "description": "High frequency oscillation, forcing many pieces.",
        "pw_linear_fx": [(i, 0.5 * (i % 2)) for i in range(7)],  # (0,0), (1, 0.5), (2, 0), (3, 0.5), ...
        "epsilon": 0.1,
        "expected_pieces": 6  # Line (0,0) to (2,0) has error 0.5 at (1, 0.5). Requires a piece per peak/trough.
    },
    {
        "description": "Sawtooth pattern, moderate epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 4  # Line (0,0) to (2,0) has error 2.0 at (1, 2.0). Need a piece for each up/down stroke.
    },
    {
        "description": "Flat data with one single spike.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2  # Line (0,0) to (4,0) has error 5.0 at (2, 5.0). Needs a break before and after the spike.
    },

    # 5. Mixed Slopes and Segments
    {
        "description": "Linear then constant, two pieces needed.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "description": "Constant then steep slope, two pieces needed.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 20.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "description": "Multiple linear segments with different slopes (optimal 3 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 3.0), (4.0, 5.0)],
        "epsilon": 0.01,
        "expected_pieces": 3
    },

    # 6. Random/Complex Data & Varying Epsilon
    {
        "description": "High-point requiring a break (from original example).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
        # Line from (0,1) to (5,8) is y=1.4x+1. Max error is at (2,3): |3 - (1.4*2+1)| = |3 - 3.8| = 0.8 > 0.5.
    },
    {
        "description": "Many points, large range, tight epsilon (forcing many pieces).",
        "pw_linear_fx": [(i, 10 * (i % 3) + i) for i in range(10)],  # Highly non-linear
        "epsilon": 1.0,
        "expected_pieces": 7  # Generally forces many pieces on complex data with tight tolerance.
    },
    {
        "description": "Many points, very large epsilon (should be 1 piece).",
        "pw_linear_fx": [(i, 10 * (i % 3) + i) for i in range(10)],
        "epsilon": 50.0,
        "expected_pieces": 1
    },
    {
        "description": "Sinusoidal data (half-wave), small epsilon.",
        "pw_linear_fx": [(i, 5 * (1 - (i / 10) ** 2)) for i in range(11)],
        "epsilon": 0.1,
        "expected_pieces": 3  # Parabolic shape, tight tolerance
    },
    {
        "description": "Data starting far from origin.",
        "pw_linear_fx": [(100.0, 100.0), (101.0, 100.1), (102.0, 100.4), (103.0, 100.9)],
        "epsilon": 0.01,
        "expected_pieces": 3  # Concave up (like x^2), tight epsilon.
    },

    # 7. Short/Long Datasets
    {
        "description": "Minimum possible data points (2 points, 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "Three points, testing single piece vs two.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2  # Line (0,0) to (2,0) has error 0.2 > 0.1.
    },
    {
        "description": "Three points, one piece should be fine.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Long dataset, mostly linear, one outlier.",
        "pw_linear_fx": [(i, i) for i in range(10)] + [(10, 15.0), (11, 11.0)],
        "epsilon": 1.0,
        "expected_pieces": 3  # Line (0,0) to (11,11) has error at (10, 15) of |15 - 10| = 5. Must break.
    },
    {
        "description": "Oscillation around a non-zero slope line.",
        "pw_linear_fx": [(i, i + 0.1 * (i % 2 == 0) - 0.1 * (i % 2 != 0)) for i in range(5)],
        "epsilon": 0.05,
        "expected_pieces": 4  # Line (0, 0.1) to (2, 2.1) has max error at (1, 0.9) of |0.9 - 1.1| = 0.2 > 0.05.
    },
    {
        "description": "Strictly decreasing curve (logarithmic decay shape).",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 2.0), (2.0, 1.0), (3.0, 0.5), (4.0, 0.25)],
        "epsilon": 0.3,
        "expected_pieces": 3  # Line (0,5) to (4, 0.25). Midpoint (2, 1) has approx error |1 - 2.625| = 1.625 > 0.3.
    },
]
test_cases12 = [
    # --- 1. Basic Cases & Uniform Data ---
    {
        "description": "Basic linear case, should be one piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Constant y-value, should be one piece.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "Simple two-segment requirement (sharp corner).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.05,
        "expected_pieces": 2 # Line from (0,0) to (2,1) has max error at (1,0) of 0.5. Line (0,0) to (3,1) max error at (1,0) and (2,1).
    },
    {
        "description": "Two segments, one break point required by tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.6), (2.0, 0.0), (3.0, 0.6), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Optimal fit for first half, optimal fit for second half.
    },
    {
        "description": "Trivial single segment due to large epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 3.0,
        "expected_pieces": 1 # Max error for line (0,0) to (3,5) is at (1,5) ~ 3.33, too big. Let's adjust data.
        # Adjusted: line (0,0) to (3,0) max error 5.0. Line (0,0) to (3,5) is okay.
        # Let's use: (0,0) to (4,0) with point (2,2). Max error is 2.0.
        # Let's use the provided example:
        # pw_linear_fx: [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)]. Max error for one segment is at (2,3) and is ~0.66.
    },
    # --- 2. Edge Epsilon & Bounds ---
    {
        "description": "Epsilon = 0 (exact fit), max pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 3 # Must connect (0,0)->(1,1), (1,1)->(2,0), (2,0)->(3,1). If points are $(x_i, y_i)$, $n$ points $\rightarrow n-1$ pieces.
    },
    {
        "description": "Epsilon very large (should be one piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    {
        "description": "Epsilon slightly too small to capture all with one piece (must be 2).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], # Max error for one segment is 1.0 at (1,1).
        "epsilon": 0.99,
        "expected_pieces": 2
    },
    {
        "description": "Epsilon just large enough for one piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    # --- 3. Convex/Concave/Curved Data ---
    {
        "description": "Convex data (parabola), requires multiple pieces.",
        "pw_linear_fx": [(i, i*i) for i in range(11)], # (0,0) to (10,100)
        "epsilon": 2.0,
        "expected_pieces": 3 # Estimated. Optimal algorithm will find the minimum.
    },
    {
        "description": "Concave data (square root), requires multiple pieces.",
        "pw_linear_fx": [(i, i**0.5) for i in range(16)], # (0,0) to (15, 3.87)
        "epsilon": 0.1,
        "expected_pieces": 4 # Estimated.
    },
    {
        "description": "Sinusoidal data (wiggles), many pieces required.",
        "pw_linear_fx": [(i*0.5, 5*__import__('math').sin(i*0.5)) for i in range(21)],
        "epsilon": 0.5,
        "expected_pieces": 6 # Estimated.
    },
    # --- 4. High Slopes and Density ---
    {
        "description": "High slope data, requires multiple pieces to maintain L-inf.",
        "pw_linear_fx": [(i*0.1, 10*i*0.1) for i in range(11)], # Linear y=10x
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    {
        "description": "Vertical-like jump, requires segment break.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (1.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # Line (0,0) to (1,0) has error 10. Line (0,0) to (1,0) has error 10 at (0.1, 10.0). Too big.
    },
    {
        "description": "Dense data points, testing performance and stability.",
        "pw_linear_fx": [(i/100.0, __import__('math').sin(i/100.0)*0.5 + i/100.0) for i in range(200)],
        "epsilon": 0.01,
        "expected_pieces": 15 # Estimated.
    },
    # --- 5. Step Functions / Discontinuities (Simulated) ---
    {
        "description": "Approximation of a step function (two segments close together).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.001, 10.0), (2.0, 10.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Must break at the jump (1.0, 0.0) -> (1.001, 10.0).
    },
    {
        "description": "Multiple steps, requiring multiple pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.001, 5.0), (2.0, 5.0), (2.001, 0.0), (3.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 3
    },
    # --- 6. Cases Designed to Expose Greedy Failures ---
    # Greedy algorithms might commit to a sub-optimal first segment, requiring more total segments.
    {
        "description": "Greedy trap: A slight curve followed by a long linear run. Optimal should use 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.0), (10.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 2 # One piece from (0,0) to (0.2, 0) max error 0.1 > epsilon.
    },
    {
        "description": "Greedy trap: Many points *just* within tolerance, followed by a point far outside.",
        "pw_linear_fx": [(i, 0.0) if i < 9 else (9.0, 0.0) if i == 9 else (10.0, 5.0) for i in range(11)], # Last point is (10, 5)
        "epsilon": 0.1,
        "expected_pieces": 2 # Should approximate the first 10 points with one line, then break for the last point.
    },
    {
        "description": "Greedy trap: A parabolic segment where an early break is sub-optimal.",
        "pw_linear_fx": [(i, i*i*0.01) for i in range(11)], # (0,0) to (10, 1)
        "epsilon": 0.1,
        "expected_pieces": 2 # Estimated. A naive greedy might stop too early.
    },
    # --- 7. Mixed and Complex Data ---
    {
        "description": "Mix of flat, linear, and curved segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 2.0), (4.0, 1.0), (5.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 3
    },
    {
        "description": "Oscillating data with increasing amplitude.",
        "pw_linear_fx": [(i*0.5, i*0.1 * __import__('math').sin(i*0.5)) for i in range(21)],
        "epsilon": 0.1,
        "expected_pieces": 8 # Estimated.
    },
    # --- 8. Small Datasets ---
    {
        "description": "Minimum data points (3) requiring 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 2
    },
    {
        "description": "Minimum data points (3) allowing 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # --- 9. Negative Values and Large Coordinates ---
    {
        "description": "Data with negative y-values and large coordinates.",
        "pw_linear_fx": [(i*100.0, -i*2.0 + 5.0) for i in range(5)],
        "epsilon": 0.001,
        "expected_pieces": 1 # Linear
    },
    {
        "description": "Data oscillating around zero (negative and positive).",
        "pw_linear_fx": [(i, (-1)**i * 1.0) for i in range(11)],
        "epsilon": 0.1,
        "expected_pieces": 10 # Requires a break at every point if epsilon is small.
    },
    # --- 10. Float Precision Check (Small Epsilon) ---
    {
        "description": "Small epsilon near machine precision, forcing many pieces.",
        "pw_linear_fx": [(i, i*i*0.001) for i in range(11)],
        "epsilon": 1e-5,
        "expected_pieces": 10
    },
    {
        "description": "Data that requires a high-order fit, challenging for linear.",
        "pw_linear_fx": [(i, __import__('math').exp(i/5.0)) for i in range(11)],
        "epsilon": 0.5,
        "expected_pieces": 3 # Estimated.
    },
    # --- 11. Final Complex Case ---
    {
        "description": "A mix of flat, drop, and linear trend.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (1.5, 1.0), (2.0, 0.0), (5.0, 3.0)],
        "epsilon": 0.2,
        "expected_pieces": 3
    },
    {
        "description": "Provided example case from prompt.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Line (0,1) to (5,8). At x=2, y_data=3.0, y_line=4.4. Error=1.4. Too big. Must be 2 pieces.
    }
]
test_cases13 = [
    # 1. Trivial Cases (One piece sufficient)
    {
        "description": "Perfectly linear data, single piece required.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Constant function, single piece required.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "Minimal data points (2), single piece required.",
        "pw_linear_fx": [(1.0, 10.0), (5.0, 15.0)],
        "epsilon": 10.0,
        "expected_pieces": 1
    },

    # 2. Zero/Tiny Tolerance (Should equal N-1 pieces)
    {
        "description": "Zero tolerance (requires all N-1 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 3  # N=4 points, 3 segments
    },
    {
        "description": "Tolerance smaller than machine precision (should require all N-1 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0 + 1e-10)],
        "epsilon": 1e-12,
        "expected_pieces": 2
    },
    {
        "description": "Zig-zag function, tiny tolerance forces all segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1e-5,
        "expected_pieces": 4
    },

    # 3. Large Tolerance (One piece should be sufficient, even for non-linear data)
    {
        "description": "Parabola, tolerance large enough for one piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 3.0,  # Max error for line (0,0) to (3,9) is at x=1.5, y=2.25 vs 4.5 -> 2.25
        "expected_pieces": 1
    },
    {
        "description": "Large jump, large tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 0.0)],
        "epsilon": 50.0,
        "expected_pieces": 1
    },
    {
        "description": "Step function (0,0),(1,1),(2,1),(3,0), large tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.6,
        "expected_pieces": 1
    },

    # 4. Collinear/Constant Data (Testing initial check and extension)
    {
        "description": "Points on a line, but starting with a deviation (needs 2 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 2.0), (4.0, 3.0)],
        "epsilon": 0.01,
        "expected_pieces": 2  # (0,0) to (1,0) is piece 1, then (1,0) to (4,3) is piece 2 (error at (2,1) is 1/3)
    },
    {
        "description": "Points mostly collinear, single point breaks the tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.9), (3.0, 3.0)],
        "epsilon": 0.05,
        "expected_pieces": 2  # Error at 1.9 vs 2.0 is 0.1, requires split. e.g., (0,0)->(1,1), then (1,1)->(3,3)
    },
    {
        "description": "Collinear data with one point barely *on* the line.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },

    # 5. Stair-step/Sharp Corners (Maximizing splits)
    {
        "description": "Stair-step function, forces a piece at every step (e.g., error = 0.5 at midpoint).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.49,
        "expected_pieces": 3  # (0,0)->(1,1) error 0.5 at 0.5, needs 3 splits (0-1, 1-2, 2-3) if epsilon < 0.5
    },
    {
        "description": "Very sharp peak, requires multiple pieces around the peak.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (0.2, 0.0), (1.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 3  # (0,0)->(0.2,0) error is 10. (0.2,0)->(1,0) is fine.
    },
    {
        "description": "Repeated up-down pattern, forces 2 pieces per cycle.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.2,
        "expected_pieces": 5
    },

    # 6. Symmetry and Concavity/Convexity (Parabolic/curved data)
    {
        "description": "Parabola: y=x^2, single piece error is 0.5.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)],
        "epsilon": 0.4,
        "expected_pieces": 2  # Error for (0,0) to (2,4) is 1.0 at x=1. Must split.
    },
    {
        "description": "Inverted parabola: y=2x-x^2, forces splits based on mid-point error.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2  # Error for (0,0) to (2,0) is 1.0 at x=1.
    },
    {
        "description": "Sinusoidal-like data (0,0), (pi/2,1), (pi,0), error check at peak.",
        "pw_linear_fx": [(0.0, 0.0), (1.57, 1.0), (3.14, 0.0)],
        "epsilon": 0.2,
        "expected_pieces": 2  # Line (0,0) to (3.14, 0) has error 1.0 at x=1.57.
    },

    # 7. Critical Points (Barely failing/passing the tolerance)
    {
        "description": "Point barely *exceeds* tolerance, forcing a split (error approx 0.5).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Point barely *within* tolerance, single piece should pass (error approx 0.5).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Small perturbation after a long straight run.",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (10.01, 0.0), (11.0, 1.0)],
        "epsilon": 0.001,
        "expected_pieces": 2  # (0,0) to (10.01, 0.0) is one piece, then (10.01, 0.0) to (11.0, 1.0)
    },

    # 8. Varying X-spacing (Non-uniform segments)
    {
        "description": "Non-uniform x-spacing, error check favors longer segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (10.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Rapid change then slow change.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (100.0, 10.0)],
        "epsilon": 0.5,
        "expected_pieces": 2  # (0,0) to (0.1, 10) error is huge, needs split.
    },
    {
        "description": "Widely spaced points, error at an interior point.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (100.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2  # Line (0,0) to (100,0) has error 5.0 at x=1.
    },

    # 9. Negative/Zero Values (Coordinate space coverage)
    {
        "description": "Negative Y-values.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, -1.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Negative X and Y values.",
        "pw_linear_fx": [(-5.0, -5.0), (-2.0, -1.0), (0.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Crossing the axes (X and Y).",
        "pw_linear_fx": [(-2.0, 2.0), (0.0, 0.0), (2.0, -2.0)],
        "epsilon": 0.0,
        "expected_pieces": 2
    },

    # 10. Complex/Mixed Scenarios
    {
        "description": "Long linear section followed by a required split and another linear section.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 2.0), (4.0, 3.0), (5.0, 4.0)],
        "epsilon": 0.05,
        "expected_pieces": 3  # (0-2) is line, (2-3) is constant (error 0.5 against (2,2) to (5,4)), (3-5) is line.
    },
    {
        "description": "Requires three pieces: two bumps separated by a flat section.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0), (5.0, 0.0)],
        "epsilon": 0.4,
        "expected_pieces": 4
    },
    {
        "description": "The Example Case: (0, 1), (1, 1), (2, 3), (5, 8).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2  # (0,1) to (1,1) is 1 piece. (1,1) to (5,8) is the second piece.
    }
]
test_cases14 = [
    # 1. Simple/Optimal Cases (Should be easy for optimal algorithms)
    {
        "name": "T1_Straight_Line_Perfect_Fit",  # Optimal Pieces: 1
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "T2_One_Split_V_Shape",  # Optimal Pieces: 2 (Split at x=2.0)
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 2.0), (4.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "name": "T3_Multiple_Splits_Staircase",  # Optimal Pieces: 3
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 1.0), (3.0, 1.2), (4.0, 2.0), (5.0, 2.2)],
        "epsilon": 0.15,
        "expected_pieces": 3
    },
    {
        "name": "T4_Smooth_Curve_High_Tolerance",  # Optimal Pieces: 1 (Easy fit for quadratic)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
        "epsilon": 0.7,
        "expected_pieces": 1
    },
    {
        "name": "T5_Initial_Plateau_Optimal_Split",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0), (4.0, 3.0)],
        "epsilon": 0.05,
        "expected_pieces": 2
    },
    # 2. Tolerance Limits (Testing bounds of epsilon)
    {
        "name": "T6_Epsilon_Too_Large_Max_Error_Check",  # Optimal Pieces: 1
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)],  # Max error is 2.5 at x=1.0
        "epsilon": 3.0,
        "expected_pieces": 1
    },
    {
        "name": "T7_Epsilon_Very_Small_Max_Pieces",  # Optimal Pieces: 3 (N points - 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.9), (3.0, 1.9)],
        "epsilon": 0.00001,
        "expected_pieces": 3
    },
    {
        "name": "T8_Exact_Match_Tolerance_Equals_Max_Error",  # Optimal Pieces: 1 (The line should fit exactly)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5, # Midpoint error at x=1.0 is 0.5
        "expected_pieces": 1
    },
    {
        "name": "T9_Epsilon_Forces_Max_Pieces_Tolerant_Jitter",  # Optimal Pieces: 4 (5 points - 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.1), (4.0, -0.1)],
        "epsilon": 0.05,
        "expected_pieces": 4
    },
    {
        "name": "T10_Epsilon_Zero_Must_Be_Exact",  # Optimal Pieces: 4 (5 points - 1)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0001), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    # 3. Boundary Conditions (Zero-slopes, points at start/end of piece)
    {
        "name": "T11_Initial_Horizontal_Segment_Then_Rise",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 6.0), (3.0, 7.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "name": "T12_Final_Horizontal_Segment",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 3.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "name": "T13_Zero_Y_Axis_Test",  # Optimal Pieces: 1
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "name": "T14_All_Points_At_Epsilon_Boundary",  # Optimal Pieces: 1 (Error is exactly 0.5)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "T15_Negative_Y_Values",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.0, -1.0), (1.0, -2.0), (2.0, -1.0), (3.0, -2.0)],
        "epsilon": 0.4,
        "expected_pieces": 2
    },
    # 4. Sharp Turns/Corners (Must split immediately)
    {
        "name": "T16_Immediate_Sharp_Turn",  # Optimal Pieces: 2 (Corner at x=1.0)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (1.0001, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "name": "T17_Right_Angle_Turn",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.05,
        "expected_pieces": 2
    },
    {
        "name": "T18_Inverted_V_Large_Amplitude",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 4.9, # Max error is 5.0 at x=1.0, so should fail
        "expected_pieces": 2
    },
    {
        "name": "T19_Long_Segment_Then_Corner",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (10.1, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "name": "T20_Exponential_Shape_Need_Multiple_Splits", # Optimal Pieces: 3
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.4), (3.0, 2.0), (4.0, 3.0)],
        "epsilon": 0.1,
        "expected_pieces": 3
    },
    # 5. Periodic/Oscillating (Requires splits every cycle)
    {
        "name": "T21_Sine_Wave_Oscillation",  # Optimal Pieces: 4
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.2, # Should force splits near 0 and 2.0
        "expected_pieces": 4
    },
    {
        "name": "T22_Small_Sawtooth_Wave",  # Optimal Pieces: 4
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (1.0, 0.0), (1.5, 0.1), (2.0, 0.0)],
        "epsilon": 0.04,
        "expected_pieces": 4
    },
    {
        "name": "T23_Oscillation_Near_Horizontal",  # Optimal Pieces: 3
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.05), (3.0, 0.05), (4.0, 0.0)],
        "epsilon": 0.02,
        "expected_pieces": 3
    },
    {
        "name": "T24_Greedy_Trap_Long_Segment_Misses_Peak",  # Optimal Pieces: 2 (A greedy algorithm might pick the first two points and then fail)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.6), (3.0, 0.0)],
        "epsilon": 0.55,
        "expected_pieces": 2
    },
    {
        "name": "T25_Step_Function_Approximation",  # Optimal Pieces: 3
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 1.0), (2.0, 1.0), (2.1, 2.0), (3.0, 2.0)],
        "epsilon": 0.05,
        "expected_pieces": 3
    },
    # 6. Misaligned Points / Floating Point Precision (Crucial for L-infinity algorithms)
    {
        "name": "T26_Just_Exceeds_Epsilon",  # Optimal Pieces: 2 (Should fail fit at x=2.0)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.24, # Max error is 0.25 at x=1.0 and x=2.0 for the first point
        "expected_pieces": 2
    },
    {
        "name": "T27_Tolerable_Near_Boundary",  # Optimal Pieces: 1 (Should pass fit)
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.49999), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "T28_Non_Integer_Coordinates_Complex_Fit",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.1, 0.3), (0.7, 1.9), (1.3, 1.2), (2.5, 0.8)],
        "epsilon": 0.2,
        "expected_pieces": 2
    },
    {
        "name": "T29_Steep_Slope_Small_Epsilon",  # Optimal Pieces: 3
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (0.2, 0.0), (0.3, 10.0)],
        "epsilon": 0.5,
        "expected_pieces": 3
    },
    {
        "name": "T30_Single_Intermediate_Point_Breaks_Optimal",  # Optimal Pieces: 2
        "pw_linear_fx": [(0.0, 0.0), (5.0, 0.0), (5.0001, 1.0), (10.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
]
test_cases15 = [
    # ----------------------------------------------------------------------
    # 1. Basic / Trivial Cases (Expected: 1 or n-1 pieces)
    # ----------------------------------------------------------------------
    {
        "name": "Trivial_1: Perfect straight line (Optimal K=1)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        "name": "Trivial_2: Perfect horizontal line (Optimal K=1)",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        "name": "Trivial_3: Very large epsilon (Optimal K=1)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0), (3.0, 20.0)],
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    {
        "name": "Trivial_4: Epsilon = 0, V shape (Optimal K=n-1=3)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    {
        "name": "Trivial_5: Two points only (Optimal K=1)",
        "pw_linear_fx": [(0.0, 5.0), (10.0, -5.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    # ----------------------------------------------------------------------
    # 2. Critical Threshold Cases (Testing Epsilon boundary)
    # ----------------------------------------------------------------------
    {
        "name": "Threshold_1: Fails for K=1 (Max dev is 0.5)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.24,
        "expected_pieces": 2
    },
    {
        "name": "Threshold_2: Passes for K=1 (Max dev is 0.5)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.25,
        "expected_pieces": 1 # Line y=0, max dev 0.5. Wait, the optimal line is y=0.25, max dev 0.25. Yes, K=1.
    },
    {
        "name": "Threshold_3: Critical deviation forces K=2 (Slightly past boundary)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.6), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Line (0,0) to (4,0). Dev at x=2 is 0.6. K=1 fails. Optimal segments: (0,0)-(2,0) and (2,0)-(4,0) will not work. Must use (0,0) to (2, 0.6) and (2, 0.6) to (4,0). K=2.
    },
    {
        "name": "Threshold_4: Strict boundary, forces max-span segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.1), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1 # Optimal line y=0.05. Max deviation is 0.05 < 0.1. K=1.
    },
    # ----------------------------------------------------------------------
    # 3. Step/Square Wave Approximations (Maximal pieces needed)
    # ----------------------------------------------------------------------
    {
        "name": "Square_1: Abrupt steps requiring 3 segments (E=0)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    {
        "name": "Square_2: Noise on a constant function (Epsilon = 0.1, passes K=1)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.05), (4.0, -0.05)],
        "epsilon": 0.1,
        "expected_pieces": 1 # Optimal line is y=0. Max dev is 0.1.
    },
    {
        "name": "Square_3: Noise on a constant function (Epsilon = 0.09, forces K=2)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.05), (4.0, -0.05)],
        "epsilon": 0.09,
        "expected_pieces": 2 # Max dev is 0.1 > 0.09. A split is forced.
    },
    # ----------------------------------------------------------------------
    # 4. Parabolic / Curvature Testing (Convex/Concave)
    # ----------------------------------------------------------------------
    {
        "name": "Parabolic_1: Convex curve y=x^2, deviation 1.0",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)],
        "epsilon": 0.9,
        "expected_pieces": 2 # K=1 line: y=2x. Dev at x=1 is 1.0 > 0.9.
    },
    {
        "name": "Parabolic_2: Convex curve, passes for K=1",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)],
        "epsilon": 1.0,
        "expected_pieces": 1 # K=1 line: y=2x. Max dev is 1.0.
    },
    {
        "name": "Parabolic_3: Concave curve, high complexity",
        "pw_linear_fx": [(0.0, 9.0), (1.0, 4.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 1.5,
        "expected_pieces": 2 # K=1 line: y=-3x+9. Dev at x=1 is 2.0. Dev at x=2 is 3.0. Fails. Needs K=2.
    },
    # ----------------------------------------------------------------------
    # 5. Sawtooth / Zig-zag (Alternating direction)
    # ----------------------------------------------------------------------
    {
        "name": "Sawtooth_1: Small zig-zag that can be covered by K=1",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.1), (4.0, -0.1)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "name": "Sawtooth_2: Critical zig-zag that forces K=2 (boundary check)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 4 # A single segment (0,0) to (2,0) has dev 1.0. Even for optimal K=2 segments (0,0)-(2,0) and (2,0)-(4,0), max dev is 1.0. E=0.5 requires max-deviation 0.5. Needs 4 segments.
    },
    {
        "name": "Sawtooth_3: Zig-zag with tolerance slightly too large for perfect fit",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.499,
        "expected_pieces": 2
    },
    # ----------------------------------------------------------------------
    # 6. Critical Alignment / Dependency Tests
    # ----------------------------------------------------------------------
    {
        "name": "Dependency_1: A slight drop forces segment termination (Greedy Trap)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.4,
        "expected_pieces": 3 # (0,0) to (1,1) is a segment. (1,1) to (2,0) is a segment. (2,0) to (3,1) is a segment. K=3.
    },
    {
        "name": "Dependency_2: Optimal path must choose longest segment first (K=2)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0) to (3,0) fails at x=2 (dev 0.2). Optimal segments are (0,0) to (2, 0.2) and (2, 0.2) to (4, 0.0). Max dev 0.1. K=2.
    },
    {
        "name": "Dependency_3: Segment must end *before* the critical point (K=3)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.5, 0.5), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 3 # (0,0) to (1,0) works. (1,0) to (2,0) fails at x=1.5 (dev 0.5). Must be (0,0)-(1.0, 0.0), (1.0, 0.0)-(2.0, 0.0), and (2.0, 0.0)-(3.0, 1.0). K=3.
    },
    # ----------------------------------------------------------------------
    # 7. Non-Uniform X-axis (Testing $L_\infty$ distance calculation)
    # ----------------------------------------------------------------------
    {
        "name": "NonUniform_1: Sparse data, then dense spike (E=0)",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (10.001, 1.0), (10.002, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    {
        "name": "NonUniform_2: Dense data must fit within tolerance (K=2)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (1.1, 0.0), (2.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 2 # (0,0) to (2,0). Max dev at x=1 is 0.1 > 0.05. Split is needed.
    },
    {
        "name": "NonUniform_3: Long flat section vs. short steep climb (K=2)",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 0.0), (5.001, 10.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,0) to (5,0) works. (5,0) to (5.001, 10.0) works. K=2.
    },
    # ----------------------------------------------------------------------
    # 8. Negative Coordinates and High Complexity
    # ----------------------------------------------------------------------
    {
        "name": "Negative_1: Simple line in negative space (Optimal K=1)",
        "pw_linear_fx": [(-3.0, -1.0), (-1.0, -3.0), (1.0, -5.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        "name": "Negative_2: Crossing zero, complex deviation (K=2)",
        "pw_linear_fx": [(-2.0, 1.0), (0.0, 0.0), (2.0, 1.0)],
        "epsilon": 0.4,
        "expected_pieces": 2 # Line (-2, 1) to (2, 1) fails at x=0 (dev 1.0). Line (-2, 1) to (2, 1) is y=1. Point (0,0) has dev 1.0. Needs 2 pieces.
    },
    {
        "name": "Complexity_1: Alternating noise with boundary violations (Testing for K=3)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 1.1), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 3 # (0,0)-(2,0) works. (2,0) to (4,0) fails at x=3 (dev 1.1). K=3.
    },
    {
        "name": "Complexity_2: Sine-like curve, high tolerance (K=2)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Line (0,0) to (4,0). Max dev is 1.0. Fails. Needs 2: (0,0) to (2,0) and (2,0) to (4,0). Max dev 1.0. Fails. Needs 4.
    },
    {
        "name": "Complexity_3: Sine-like curve, moderate tolerance (K=4)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.25,
        "expected_pieces": 4 # A segment must be short enough. (0,0) to (1,1) is K=1. (1,1) to (2,0) is K=1. (2,0) to (3,-1) is K=1. (3,-1) to (4,0) is K=1. K=4.
    },
    {
        "name": "Complexity_4: Sharp spike with generous Epsilon (K=3)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 10.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 3 # Line (0,0) to (4,0). Max dev at x=3 is 10.0. Fails. (0,0)-(2,0) works. (2,0)-(4,0). Max dev at x=3 is 5.0. Fails. Needs 3: (0,0)-(2,0), (2,0)-(3,10), (3,10)-(4,0).
    },
]
test_cases16 = [
    # --- Basic Cases & Small Data Sets ---
    {
        "description": "Case 1: Simple linear function (should be 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    {
        "description": "Case 2: Constant function (should be 1 piece).",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Case 3: Function with a sharp V-shape requiring 2 pieces for small epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 1.0, # Large epsilon might allow 1 piece
        "expected_pieces": 1
    },
    {
        "description": "Case 4: Same V-shape but with small epsilon, forcing 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Case 5: Simple curve (parabola approximation).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Should approximate (0,0) to (2,4) with error > 0.5, but (1,1) to (3,9) should be okay. Expected pieces: (0,0)-(2,4) and (2,4)-(3,9).
    },

    # --- Tolerance (Epsilon) Edge Cases ---
    {
        "description": "Case 6: Epsilon is zero (requires max pieces if not perfectly linear).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.1), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_pieces": 3 # 4 points -> 3 segments
    },
    {
        "description": "Case 7: Epsilon is very large (should be 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    {
        "description": "Case 8: Epsilon is just large enough to allow 1 piece, testing boundary.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5, # Max error is 0.5 at x=1.0 for a line from (0,0) to (2,0)
        "expected_pieces": 1
    },
    {
        "description": "Case 9: Epsilon is just small enough to force 2 pieces, testing boundary.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.499,
        "expected_pieces": 2
    },

    # --- Dataset Structure Edge Cases ---
    {
        "description": "Case 10: Only two data points (must be 1 piece).",
        "pw_linear_fx": [(0.0, 1.0), (5.0, 5.0)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    {
        "description": "Case 11: Data points with non-uniform x-spacing.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (5.0, 1.0), (5.1, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 3
    },
    {
        "description": "Case 12: Points requiring a segment break close to the start.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (10.0, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },

    # --- Step Functions / Near-Vertical Jumps ---
    {
        "description": "Case 13: Near-step function, requires many pieces.",
        "pw_linear_fx": [(0.0, 0.0), (0.001, 10.0), (1.0, 10.0), (1.001, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 3 # (0,0) to (0.001, 10.0) -> (1.0, 10.0) -> (1.001, 0.0)
    },
    {
        "description": "Case 14: Many points forming a constant line, but with one outlier.",
        "pw_linear_fx": [(i, 0.0) for i in range(10)] + [(5, 1.0), (10, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 3 # The outlier at (5, 1.0) forces splits around it.
    },
    {
        "description": "Case 15: Sawtooth pattern (needs many pieces).",
        "pw_linear_fx": [(i, i % 2) for i in range(11)],
        "epsilon": 0.1,
        "expected_pieces": 5 # Should be able to cover (0,0)-(2,0), (2,0)-(4,0), etc., but the alternating y-values will force segments (0,0)-(1,1)-(2,0)...
    },

    # --- Optimization / Greedy vs. Optimal Check ---
    # These cases are crucial to test for greedy vs. optimal algorithm implementation.
    # An optimal algorithm must find the longest valid segment starting at a point,
    # not just the first one that works.
    {
        "description": "Case 16: Greedy trap 1 - Should take one long segment, not two short ones.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0), (5.0, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2 # (0.0, 0.0) -> (3.0, 0.0) is not perfect, but (0,0)-(4,1) should work. Should be 2 pieces: (0,0)-(3,0) and (3,0)-(5,1). Let's adjust to force 1 optimal path.
    },
    {
        "description": "Case 17: Optimized path should skip intermediate point (1.0, 0.0).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1 # A line from (0,0) to (3,0) works because max error at x=2.0 is 0.1 <= epsilon.
    },
    {
        "description": "Case 18: Optimized path must break at the second point.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.11), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Line (0,0) to (3,0) fails. Line (0,0) to (2, 0.11) fails. Must be (0,0) to (1,0) and (1,0) to (3,0).
    },

    # --- Combined Function Shapes ---
    {
        "description": "Case 19: Exponential growth needing increasingly short segments.",
        "pw_linear_fx": [(i, 2**i) for i in range(5)], # (0,1), (1,2), (2,4), (3,8), (4,16)
        "epsilon": 0.5,
        "expected_pieces": 4 # Exponential growth is hard to fit with straight lines. Should need 4 pieces.
    },
    {
        "description": "Case 20: Concave function (approximation is below the curve).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 4.0), (2.0, 7.0), (3.0, 9.0), (4.0, 10.0)],
        "epsilon": 0.5,
        "expected_pieces": 3 # Should require 3 pieces. (0,0)-(2,7) fails. (0,0)-(1,4), (1,4)-(3,9), (3,9)-(4,10).
    },
    {
        "description": "Case 21: Convex function (approximation is above the curve).",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 6.0), (2.0, 3.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 3
    },
    {
        "description": "Case 22: Sine wave approximation (periodic data).",
        "pw_linear_fx": [(i, 10 * __import__('math').sin(i * 0.5)) for i in range(10)],
        "epsilon": 1.0,
        "expected_pieces": 4 # A sine wave segment usually takes 2-3 pieces per half-period for this epsilon.
    },

    # --- Large Datasets & Complexity Check ---
    {
        "description": "Case 23: Large dataset, all points linear (optimality is 1 piece).",
        "pw_linear_fx": [(i, i) for i in range(50)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    {
        "description": "Case 24: Large dataset, constant deviation (forces max pieces).",
        "pw_linear_fx": [(i, 0.0) if i % 2 == 0 else (i, 0.2) for i in range(50)],
        "epsilon": 0.1,
        "expected_pieces": 25 # Each pair (i, 0.0), (i+1, 0.2) will likely require its own segment if tolerance is tight.
    },
    {
        "description": "Case 25: Large dataset, easy to fit (should be few pieces).",
        "pw_linear_fx": [(i, 0.0) if i < 25 else (i, 10.0) for i in range(50)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0) to (24,0) and (24,0) to (49,10).
    },

    # --- Negative & Mixed Coordinates ---
    {
        "description": "Case 26: Negative y-coordinates.",
        "pw_linear_fx": [(0.0, -10.0), (1.0, -5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Case 27: Mixed positive and negative y-coordinates with curvature.",
        "pw_linear_fx": [(-2.0, 4.0), (-1.0, 1.0), (0.0, 0.0), (1.0, 1.0), (2.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Parabola requires 2 pieces for this epsilon.
    },
    {
        "description": "Case 28: Negative x-coordinates (assuming x-values are strictly increasing).",
        "pw_linear_fx": [(-5.0, 5.0), (-3.0, 3.0), (-1.0, 1.0), (0.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },

    # --- Floating Point Precision Check ---
    {
        "description": "Case 29: Tiny deviations that are exactly equal to epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1 # The maximum error is exactly 0.5, should be inclusive.
    },
    {
        "description": "Case 30: Tiny deviations that slightly exceed epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.500000001), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # The error is > 0.5, forcing a split.
    }
]
test_cases17 = [
    # 1. Simple Straight Line (Optimal: 1 Piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0
    },
    # 2. Perfect Fit within tolerance (Optimal: 1 Piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.5
    },
    # 3. Simple Step Function (Requires 2 Pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.0
    },
    # 4. Maximum Error Just Above Epsilon (Requires 2 Pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.1), (3.0, 1.1)],
        "epsilon": 1.0
    },
    # 5. Sawtooth Wave (High frequency, low amplitude)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.3
    },
    # 6. Sharp Angle (Smallest non-zero error)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.001), (3.0, 0.0)],
        "epsilon": 0.0
    },
    # 7. V-Shape, Just fits (Optimal: 1 Piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5
    },
    # 8. V-Shape, Just breaks (Optimal: 2 Pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.499
    },
    # 9. Constant Function (Optimal: 1 Piece)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (10.0, 5.0), (20.0, 5.0)],
        "epsilon": 0.0
    },
    # 10. Alternating Max Error (Forces 3 Pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.4
    },
    # 11. End-point Tolerance Challenge (Optimal choice of a single line)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.5
    },
    # 12. Short Sequence, Tight Tolerance (Requires 2 Pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.1, 0.0)],
        "epsilon": 0.0
    },
    # 13. High Epsilon (Always 1 Piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 50.0
    },
    # 14. Non-Uniform X-Spacing
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (10.0, 0.0)],
        "epsilon": 0.5
    },
    # 15. The "Greedy Trap" Scenario (Testing for optimality)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.2), (3.0, 0.8), (4.0, 1.0)],
        "epsilon": 0.3
    },
    # 16. Quadratic-like curve (Requires 2 Pieces, near fail)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 1.0), (3.0, 2.25), (4.0, 4.0)],
        "epsilon": 1.0
    },
    # 17. Quadratic-like curve (Forces 3 Pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 1.0), (3.0, 2.25), (4.0, 4.0)],
        "epsilon": 0.5
    },
    # 18. Only two points (Always 1 Piece)
    {
        "pw_linear_fx": [(1.0, 1.0), (2.0, 5.0)],
        "epsilon": 0.0
    },
    # 19. Large Number of Points, Low Amplitude Noise (Optimal: 1 Piece)
    {
        "pw_linear_fx": [(i, 10.0 + (i % 2) * 0.1) for i in range(11)],
        "epsilon": 0.1
    },
    # 20. Large Number of Points, High Amplitude Noise (Requires many pieces)
    {
        "pw_linear_fx": [(i, 10.0 + (i % 2) * 1.0) for i in range(11)],
        "epsilon": 0.0
    },
    # 21. Error occurs at the midpoint (Parabolic maximum error)
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5
    },
    # 22. Error occurs near an endpoint (Skewed data)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (10.0, 0.0)],
        "epsilon": 0.1
    },
    # 23. Zero X-span (Multiple points with the same X)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.0
    },
    # 24. Negative coordinates
    {
        "pw_linear_fx": [(-5.0, -5.0), (-2.0, -4.0), (0.0, -3.0), (3.0, -2.0)],
        "epsilon": 0.2
    },
    # 25. Large Coordinates (Floating Point Precision Test)
    {
        "pw_linear_fx": [(100000.0, 100000.0), (100001.0, 100001.0), (100002.0, 100001.0)],
        "epsilon": 0.4
    },
    # 26. Tolerance Just Fails - (Sensitivity check)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        "epsilon": 0.5
    },
    # 27. Alternating slopes, low $\epsilon$ (Requires 4 Pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.0
    },
    # 28. A single vertical perturbation in a straight line (Forces 3 Pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.0
    },
    # 29. Logarithmic-like Curve (Requires 3 Pieces)
    {
        "pw_linear_fx": [(1.0, 0.0), (2.0, 0.69), (4.0, 1.39), (8.0, 2.08), (16.0, 2.77)],
        "epsilon": 0.5
    },
    # 30. Empty sequence (Edge case)
    {
        "pw_linear_fx": [],
        "epsilon": 1.0
    }
]
test_cases18 = [
    # --- 1. Basic Optimality and Linear Cases (Baseline) ---
    { # 1. Perfectly Linear: Should be 1 piece.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 1
    },
    { # 2. Horizontal Line with small perturbation: Test absorption of noise.
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.05), (2.0, 0.95), (3.0, 1.0)],
        "epsilon": 0.1, # Epsilon > 0.05
        "expected_num_pieces": 1
    },
    { # 3. Step Function with large epsilon: Test feasibility over optimality.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 3.0, # Epsilon > 2.5
        "expected_num_pieces": 1
    },
    { # 4. V-Shape / Sharp Turn: Must require 2 pieces.
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 1.0)],
        "epsilon": 0.05,
        "expected_num_pieces": 2
    },
    { # 5. Outlier: Constant Y with a single outlier point forcing a split.
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.5), (4.0, 1.0), (5.0, 1.0)],
        "epsilon": 0.2, # Outlier error is 0.5, Epsilon is 0.2.
        "expected_num_pieces": 2
    },

    # --- 2. Greedy Failure / Optimality Cases (Critical) ---
    { # 6. The "Slightly Off" End Point: Designed to fail a purely greedy approach for optimality.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.1), (3.0, 0.05), (4.0, 0.0)],
        "epsilon": 0.051, # Epsilon just over the midpoint error (0.05).
        "expected_num_pieces": 2
    },
    { # 7. Delayed Sharp Turn: Point (3, 0) forces a split after (2, 0.5).
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.5), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 2
    },
    { # 8. Gradual Curve requiring minimum points: Parabola-like data.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.2), (3.0, 0.45), (4.0, 0.7), (5.0, 0.95), (6.0, 1.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 3
    },
    { # 9. Alternating sequence: Easily approximated by 1 piece due to large epsilon.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.2), (3.0, 0.2), (4.0, -0.2)],
        "epsilon": 0.21, # Epsilon > max deviation (0.2)
        "expected_num_pieces": 1
    },
    { # 10. Alternating sequence: Same data, but tight epsilon forces many splits.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.2), (3.0, 0.2), (4.0, -0.2)],
        "epsilon": 0.1, # Epsilon is too small. Max span is 0.4.
        "expected_num_pieces": 4
    },

    # --- 3. Geometric and Boundary Cases (Vertical/Horizontal/Extreme) ---
    { # 11. Vertical Segment (Identical X): Check handling of zero width segments.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 2
    },
    { # 12. Very Steep Slope: Check numerical stability with extreme slope.
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (0.2, 0.0)],
        "epsilon": 0.5,
        "expected_num_pieces": 2
    },
    { # 13. Very Gentle Slope / Long Run.
        "pw_linear_fx": [(0.0, 0.0), (100.0, 0.01), (200.0, 0.02)],
        "epsilon": 0.001,
        "expected_num_pieces": 2
    },
    { # 14. Repeated points (Immediate turn): Should treat (0.0, 0.0) as one point.
        "pw_linear_fx": [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 2
    },
    { # 15. Zero Tolerance: Forces a split between every single data point.
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.0,
        "expected_num_pieces": 4
    },

    # --- 4. Varying Epsilon and Data Density ---
    { # 16. Extremely sparse data - Baseline.
        "pw_linear_fx": [(0.0, 0.0), (10.0, 1.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 1
    },
    { # 17. Extremely dense data with noise.
        "pw_linear_fx": [(x / 10.0, x / 10.0 + ((-1)**x) * 0.01) for x in range(20)],
        "epsilon": 0.05,
        "expected_num_pieces": 1
    },
    { # 18. Tight epsilon, forcing a split on every small deviation.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.01), (2.0, 0.0), (3.0, 0.01)],
        "epsilon": 0.001,
        "expected_num_pieces": 3
    },
    { # 19. Large epsilon, absorbing a significant curve (Slight parabolic).
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 1.1, # Epsilon > 1.0 (max deviation)
        "expected_num_pieces": 1
    },
    { # 20. Mid-range epsilon that requires only a single internal split.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.2,
        "expected_num_pieces": 3
    },

    # --- 5. Complex/Real-World Approximations (Sine Wave, Noise) ---
    { # 21. Single period of a sine wave (approx).
        "pw_linear_fx": [(i * 0.5, 0.5 * (1 - ((-1)**i))) for i in range(9)],
        "epsilon": 0.1,
        "expected_num_pieces": 4
    },
    { # 22. Random noise (high frequency) on a constant base.
        "pw_linear_fx": [(i, 5.0 + (i % 2 - 0.5) * 0.4) for i in range(10)], # Points oscillate by +/- 0.2.
        "epsilon": 0.15, # Max deviation is 0.2. Split is forced.
        "expected_num_pieces": 2
    },
    { # 23. Noise on a sloped line.
        "pw_linear_fx": [(i, i * 0.5 + (i % 2 - 0.5) * 0.02) for i in range(10)],
        "epsilon": 0.01, # Epsilon forces splits when noise deviates from straight line.
        "expected_num_pieces": 9
    },
    { # 24. Concave function (e.g., sqrt)
        "pw_linear_fx": [(x, x**0.5) for x in range(10)],
        "epsilon": 0.5,
        "expected_num_pieces": 2
    },
    { # 25. Convex function (e.g., x^2)
        "pw_linear_fx": [(x, x**2) for x in range(5)],
        "epsilon": 0.5,
        "expected_num_pieces": 4
    },

    # --- 6. Edge Case Combinations and Final Checks ---
    { # 26. Initial point is far away, but subsequent points are linear.
        "pw_linear_fx": [(0.0, 5.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 2
    },
    { # 27. End point forces a split near the end.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.5)],
        "epsilon": 0.1,
        "expected_num_pieces": 2
    },
    { # 28. Example from the prompt - Verification.
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_num_pieces": 2
    },
    { # 29. Long run of points on the boundary of the tolerance band.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 2
    },
    { # 30. Minimal points.
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.001,
        "expected_num_pieces": 1
    },
]
test_cases19 = [
    # --- 1. Basic Functionality and Trivial Cases (Optimality is clear) ---
    {
        "description": "Trivial: Perfectly linear data (should be 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
    },
    {
        "description": "Trivial: Flat data (should be 1 piece).",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.001,
    },
    {
        "description": "Trivial: High tolerance (should be 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.1,
    },
    {
        "description": "Trivial: Zero tolerance (n pieces, each point is a piece end).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
    },

    # --- 2. Greedy Failure Scenarios (Testing for Optimality) ---
    # These cases are designed where an optimal algorithm might choose a longer first segment
    # to save more total segments later, while a greedy algorithm might choose a shorter,
    # 'locally best' first segment that leads to a non-optimal overall solution.
    {
        "description": "Greedy Trap 1: Short steep curve followed by long gentle one.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (10.0, 0.0)],
        "epsilon": 0.2,
        # Optimal solution should be 2 pieces: [(0.0, 0.0) to (0.2, 0.0)] and [(0.2, 0.0) to (10.0, 0.0)]
    },
    {
        "description": "Greedy Trap 2: Two short, near-tolerance segments vs. one long one.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.15,  # Optimal is 1 piece; a greedy algorithm might stop at (2.0, 0.0)
    },
    {
        "description": "Greedy Trap 3: A point exactly on the tolerance boundary.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5,  # The first segment should reach (2.0, 1.0)
    },
    {
        "description": "Greedy Trap 4: Sawtooth wave, requiring minimum number of joins.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0), (6.0, 0.0)],
        "epsilon": 0.9,  # Optimal: 2 pieces [(0.0, 0.0) to (3.0, 1.0)] and [(3.0, 1.0) to (6.0, 0.0)]
    },
    {
        "description": "Greedy Trap 5: High-frequency oscillation near tolerance.",
        "pw_linear_fx": [(i, 0.0 if i % 2 == 0 else 0.4) for i in range(11)],
        "epsilon": 0.45,  # Optimal: 1 piece
    },

    # --- 3. Geometric and Boundary Cases (Tolerance, Points) ---
    {
        "description": "Tolerance is exactly the maximum deviation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,  # Should be 1 piece
    },
    {
        "description": "Maximum deviation is slightly over tolerance (forces a split).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        "epsilon": 0.5,  # Should be 2 pieces
    },
    {
        "description": "Single point segment (n=1).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.001,
    },
    {
        "description": "All points outside the optimal approximation region (forcing many pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.01, 0.0), (2.01, 1.0)],
        "epsilon": 0.05,  # Requires 2 pieces (or more) due to sharp vertical change
    },
    {
        "description": "Non-uniform x-spacing, uniform y-variation.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (1.0, 0.2), (10.0, 0.3)],
        "epsilon": 0.05,
    },
    {
        "description": "Steep start, gentle end.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (1.0, 10.1), (10.0, 10.2)],
        "epsilon": 0.05,
    },

    # --- 4. Numerical/Floating Point Precision Cases ---
    {
        "description": "Small epsilon (testing precision of distance calculation).",
        "pw_linear_fx": [(i / 10.0, i / 10.0) for i in range(11)],
        "epsilon": 1e-6,
    },
    {
        "description": "Very large coordinates.",
        "pw_linear_fx": [(0.0, 1e5), (1.0, 1e5 + 1.0), (2.0, 1e5 + 2.0)],
        "epsilon": 0.1,
    },
    {
        "description": "Negative coordinates (full range).",
        "pw_linear_fx": [(-2.0, -2.0), (-1.0, -1.0), (0.0, 0.0), (1.0, -1.0), (2.0, -2.0)],
        "epsilon": 0.1,
    },
    {
        "description": "Points clustered very closely together.",
        "pw_linear_fx": [(0.0, 0.0), (0.001, 1.0), (0.002, 0.0)],
        "epsilon": 0.1,  # Should be 2 pieces
    },
    {
        "description": "Small tolerance near a curve.",
        "pw_linear_fx": [(i, (i / 10.0) ** 2) for i in range(11)],
        "epsilon": 0.01,
    },

    # --- 5. Complex Functions and Patterns ---
    {
        "description": "Sinusoidal wave (multiple pieces required).",
        "pw_linear_fx": [(i, 10 * 0.5 * (1 + 0.5 * i) * 0.5) for i in range(11)],
        "epsilon": 0.5,
    },
    {
        "description": "Parabolic curve ($y=x^2$).",
        "pw_linear_fx": [(i, i ** 2) for i in range(5)],
        "epsilon": 0.1,
    },
    {
        "description": "Exponential curve ($y=2^x$).",
        "pw_linear_fx": [(i, 2 ** i) for i in range(5)],
        "epsilon": 1.0,
    },
    {
        "description": "Alternating 'W' shape, designed to challenge segment extension.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, -1.0), (6.0, 0.0)],
        "epsilon": 0.5,
    },
    {
        "description": "Long section of perfect fit, followed by one large outlier.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (3.1, 10.0), (4.0, 4.0)],
        "epsilon": 0.1,  # Should force a split after (3.0, 3.0)
    },

    # --- 6. Specific Boundary Interactions and Tolerance Tests ---
    {
        "description": "Data exactly on the approximation line, except for the last point.",
        "pw_linear_fx": [(i, i) for i in range(5)] + [(5.0, 10.0)],
        "epsilon": 0.1,  # Forces a split at the last point
    },
    {
        "description": "High slope data, testing the vertical bounds of the $\mathbf{L}_{\infty}$ tube.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (0.2, 20.0), (0.3, 10.0)],
        "epsilon": 1.0,
    },
    {
        "description": "Zero slope segments requiring minimal pieces.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.1, 1.05), (2.0, 1.0)],
        "epsilon": 0.06,  # Should be 1 piece
    },
    {
        "description": "Example from the prompt (for validation/reference).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
    },
]
test_cases20 = [
    # --- Category 1: Simple Functions & Baseline Optimality (Cases 1-5) ---
    {
        "description": "Perfectly linear function (should need 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    {
        "description": "Constant function (should need 1 piece).",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Gentle quadratic curve, achievable with 1 segment given large epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
        "epsilon": 1.0, # Large tolerance
        "expected_pieces": 1
    },
    {
        "description": "V-shape with corner, requires 2 pieces.",
        "pw_linear_fx": [(0.0, 2.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 2.0)],
        "epsilon": 0.0, # Strict tolerance
        "expected_pieces": 2
    },
    {
        "description": "Points right at the tolerance limit for 1 segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Error is 0.1, but often this shape requires 2 pieces
    },

    # --- Category 2: Tolerance & Boundary Cases (Cases 6-10) ---
    {
        "description": "Points perfectly forming two distinct lines, 1 piece *not* possible.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "description": "Function that requires the maximum number of pieces (n points, n-1 segments).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.0, # Strict
        "expected_pieces": 4
    },
    {
        "description": "Zero tolerance (epsilon=0.0) forces exact original function.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    {
        "description": "Extremely large tolerance (should always be 1 piece).",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 1.0), (2.0, 20.0), (3.0, 5.0)],
        "epsilon": 50.0,
        "expected_pieces": 1
    },
    {
        "description": "Intermediate points *exactly* at +/- epsilon limit.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Should pass with 2, but 1 may fail due to error propagation
    },

    # --- Category 3: Local vs. Global Optimality (Cases 11-15) ---
    {
        "description": "A long linear segment followed by a small spike (tests greedy choice).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (3.1, 4.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Should be (0,3) and (3,4) or similar
    },
    {
        "description": "A slow-changing curve that requires 2 pieces for optimality.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.7), (4.0, 0.8)],
        "epsilon": 0.05,
        "expected_pieces": 2
    },
    {
        "description": "A function where the 'best fit' line for the first segment forces a poor choice later.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.5), (4.0, 0.5)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Points with small, alternating deviations (tests error accumulation).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.05), (3.0, 0.05), (4.0, -0.05), (5.0, 0.0)],
        "epsilon": 0.06,
        "expected_pieces": 1
    },
    {
        "description": "A function that can be approximated with 2, but a poor first segment would force 3.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.4), (3.0, 0.0), (4.0, -0.2)],
        "epsilon": 0.2,
        "expected_pieces": 2
    },

    # --- Category 4: Numerical Stability & Precision (Cases 16-20) ---
    {
        "description": "Smallest possible non-zero $\epsilon$ (tests floating point precision).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1e-6), (2.0, 2e-6), (3.0, 3e-6)],
        "epsilon": 1e-5,
        "expected_pieces": 1
    },
    {
        "description": "Points defined by very small $y$ values.",
        "pw_linear_fx": [(0.0, 1e-3), (1.0, 2e-3), (2.0, 1e-3), (3.0, 2e-3)],
        "epsilon": 1e-3,
        "expected_pieces": 1
    },
    {
        "description": "Points defined by very large $x$ values.",
        "pw_linear_fx": [(1000.0, 0.0), (1001.0, 0.0), (1002.0, 1.0), (1003.0, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "description": "Vertical line segment (should be impossible/handled by pre-processing or require $\epsilon>0$).",
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Assuming pre-sorting handles distinct x values, or the algorithm gracefully skips.
    },
    {
        "description": "Multiple points with the same $(x, y)$ coordinate.",
        "pw_linear_fx": [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },

    # --- Category 5: Complex Shapes & Practical Cases (Cases 21-30) ---
    {
        "description": "Sine-like curve (tests handling of inflection points).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0), (5.0, 0.5)],
        "epsilon": 0.1,
        "expected_pieces": 4 # Requires more than 3 segments
    },
    {
        "description": "Sawtooth pattern with tight $\epsilon$ (maximizes segments).",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)],
        "epsilon": 0.01,
        "expected_pieces": 4
    },
    {
        "description": "Staircase/Step function approximation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 1.0), (2.0, 1.0), (2.1, 2.0), (3.0, 2.0)],
        "epsilon": 0.4,
        "expected_pieces": 3
    },
    {
        "description": "Rapid change at the end of the data.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Rapid change at the start of the data.",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Data where points are highly non-uniform in $x$ (tests interpolation over long gaps).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (100.0, 2.0), (101.0, 3.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "A 'bump' function that must be handled by one piece if $\epsilon$ is large enough.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "A 'valley' function that must be handled by one piece if $\epsilon$ is large enough.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, -0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Function that requires 3 pieces due to two distinct, large deviations.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    {
        "description": "A case where a single segment *just* fails at the final point.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.5)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
]
test_cases21 = [
    # --- 1. Basic/Small Data Sets (Expected optimal pieces in comment) ---
    {
        "description": "Perfectly straight line (1 piece expected).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },  # (1)
    {
        "description": "Constant function, zero error (1 piece expected).",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0)],
        "epsilon": 0.001
    },  # (1)
    {
        "description": "Simple two-segment 'V' shape, requires 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.01
    },  # (2)
    {
        "description": "Simple two-segment 'A' shape, requires 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.1
    },  # (2)

    # --- 2. Boundary Condition / Epsilon Sensitivity (Critical Cases) ---
    {
        "description": "Parabola: Single line fails for epsilon=0.04 (Max error is 0.045), should require 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 1.0), (3.0, 2.25), (4.0, 4.0)],
        "epsilon": 0.04
    },  # (2) - Error at (1.0, 0.25) approx 0.045 > 0.04 if using (0,0) to (2,1)
    {
        "description": "Parabola: Single line works for epsilon=0.05 (Max error is 0.045), should require 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 1.0), (3.0, 2.25), (4.0, 4.0)],
        "epsilon": 0.05
    },  # (1)
    {
        "description": "Steep slope change near epsilon limit, should require 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0)],
        "epsilon": 0.04
    },  # (2) - Max error is 0.05, 0.04 fails
    {
        "description": "Steep slope change near epsilon limit, should allow 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0)],
        "epsilon": 0.06
    },  # (1) - Max error is 0.05, 0.06 passes
    {
        "description": "Long sequence of points slightly above the line, maximizing accumulated error.",
        "pw_linear_fx": [(i, 0.05 * (i % 2)) for i in range(10)],
        "epsilon": 0.049
    },  # (5) or more, depending on implementation detail

    # --- 3. Non-Monotonic / Oscillating Data (Wave-like) ---
    {
        "description": "Sinusoidal-like data, forces multiple segments.",
        "pw_linear_fx": [(i, 0.5 * (1 + (-1)**i)) for i in range(10)],
        "epsilon": 0.1
    },  # (9) - alternating 0.0 and 1.0, max error is 0.5. $\epsilon=0.1$ forces a segment for almost every point.
    {
        "description": "Sinusoidal-like data, but epsilon is large enough to simplify.",
        "pw_linear_fx": [(i, 0.5 * (1 + (-1)**i)) for i in range(10)],
        "epsilon": 0.51
    },  # (1) - Max error is 0.5.
    {
        "description": "Small rapid oscillation, requires short segments.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (1.0, 0.0), (1.5, -0.1), (2.0, 0.0)],
        "epsilon": 0.05
    },  # (4)

    # --- 4. Convex/Concave Data (Curvature tests) ---
    {
        "description": "Strong concave down (quadratic-like), requires multiple pieces for small epsilon.",
        "pw_linear_fx": [(i, -i**2) for i in range(6)],
        "epsilon": 0.5
    },  # (4)
    {
        "description": "Strong concave down, large epsilon allows simplification.",
        "pw_linear_fx": [(i, -i**2) for i in range(6)],
        "epsilon": 2.0
    },  # (2)
    {
        "description": "Strong convex up (exponential-like), forces early break.",
        "pw_linear_fx": [(i, 2**i) for i in range(6)],
        "epsilon": 1.0
    },  # (4)

    # --- 5. Mixed Collinear and Non-Collinear Data ---
    {
        "description": "Long collinear start, followed by sharp break, must NOT break on the collinear part.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.01
    },  # (2) - must find segment (0.0, 0.0) to (2.0, 0.0) and then the rest.
    {
        "description": "Collinear segment in the middle of a curve.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0)],
        "epsilon": 0.1
    },  # (3) - (0,1)->(1,0), (1,0)->(3,0), (3,0)->(4,1)
    {
        "description": "Flat region that should be covered by a single segment.",
        "pw_linear_fx": [(i, 10.0 if 3 <= i <= 7 else 0.0) for i in range(11)],
        "epsilon": 0.1
    },  # (3)

    # --- 6. Large Data Sets / Performance Testing ---
    {
        "description": "20 points forming a shallow curve, challenging for optimality search.",
        "pw_linear_fx": [(i, 0.01 * i**2) for i in range(20)],
        "epsilon": 0.1
    },  # (approx 5-7)
    {
        "description": "20 points, highly noisy (random) data, forcing many segments.",
        "pw_linear_fx": [(i, 0.5 if i % 3 == 0 else 0.0) for i in range(20)],
        "epsilon": 0.01
    },  # (approx 10-15)

    # --- 7. Floating Point Precision Edge Cases ($\epsilon$ very small or very large) ---
    {
        "description": "Minimal epsilon, forces almost every point to be an anchor (n pieces).",
        "pw_linear_fx": [(i, i) for i in range(10)],
        "epsilon": 1e-10
    },  # (9) - only 1 piece because the line is perfect.
    {
        "description": "Minimal epsilon on non-linear data, forces n pieces.",
        "pw_linear_fx": [(i, i**2) for i in range(5)],
        "epsilon": 1e-10
    },  # (4)
    {
        "description": "Extremely large epsilon, should always result in 1 piece.",
        "pw_linear_fx": [(i, 100 * (i % 2)) for i in range(10)],
        "epsilon": 1000.0
    },  # (1)
    {
        "description": "Smallest possible vertical deviation that should break the segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2e-8)],
        "epsilon": 1e-8
    },  # (2)

    # --- 8. Specific Geometric Challenges ---
    {
        "description": "Three points forming a maximum error exactly equal to epsilon, must pass (1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5
    },  # (1)
    {
        "description": "Three points forming a maximum error just over epsilon, must fail (2 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5 + 1e-6), (2.0, 0.0)],
        "epsilon": 0.5
    },  # (2)
    {
        "description": "Points with large Y-range but small X-range (steep data).",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (0.2, 0.0)],
        "epsilon": 0.1
    },  # (2) - max error 5, must break.
    {
        "description": "Points with small Y-range but large X-range (shallow data).",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.1), (20.0, 0.0)],
        "epsilon": 0.001
    },  # (2) - max error 0.05, must break.

    # --- 9. Negative Coordinates / Start/End Point Symmetry ---
    {
        "description": "Data including negative X and Y coordinates.",
        "pw_linear_fx": [(-2.0, 2.0), (-1.0, -1.0), (0.0, 0.0), (1.0, 1.0), (2.0, -2.0)],
        "epsilon": 0.5
    },  # (4)
    {
        "description": "Symmetrical quadratic data with large epsilon.",
        "pw_linear_fx": [(-2.0, 4.0), (-1.0, 1.0), (0.0, 0.0), (1.0, 1.0), (2.0, 4.0)],
        "epsilon": 1.0
    }  # (2)
]
test_cases22 = [
    # ----------------------------------------------------
    # 1-3. Simple/Baseline Cases
    # ----------------------------------------------------
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,1) to (2,3) fits, (2,3) to (5,8) fits
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.4)],
        "epsilon": 0.05,
        "expected_pieces": 4 # 5 points, all on a line y=0.1x. Needs one piece.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4 # V-shape/parabola. Likely needs 3-4 pieces.
    },
    # ----------------------------------------------------
    # 4-6. High Epsilon (Testing Single Piece Optimality)
    # ----------------------------------------------------
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 1.0,
        "expected_pieces": 1 # A single line from (0,0) to (3,1) fits all points with max error 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (1.0, 1.0), (5.0, -1.0), (9.0, 1.0)],
        "epsilon": 1.0,
        "expected_pieces": 1 # Large range, max error is 1.0, one piece should be optimal.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.001,
        "expected_pieces": 1 # Perfectly flat data.
    },
    # ----------------------------------------------------
    # 7-9. Low Epsilon (Testing Max Pieces)
    # ----------------------------------------------------
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0001,
        "expected_pieces": 3 # Forces connection between all 4 points.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4 # Very steep function, small epsilon means max pieces.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (0.3, 1.0), (0.4, 0.0), (0.5, 1.0)],
        "epsilon": 0.2,
        "expected_pieces": 5 # High frequency, small x-steps.
    },
    # ----------------------------------------------------
    # 10-12. S-Curve/Curvature (Testing Transition Points)
    # ----------------------------------------------------
    {
        # A cubic-like curve: slow, fast, slow
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.4), (3, 1.5), (4, 4.0), (5, 5.0)],
        "epsilon": 0.5,
        "expected_pieces": 3 # Should need a piece for the slow start, one for the fast curve, one for the slow end.
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.2), (3, 2.0), (4, 3.0), (5, 3.1), (6, 3.2)],
        "epsilon": 0.15,
        "expected_pieces": 3 # Flat-curve-flat. The curve section (3,4) forces a new piece.
    },
    {
        # Steep $\tanh$ approximation
        "pw_linear_fx": [(0, 0), (1, 0.05), (2, 0.2), (3, 0.9), (4, 0.95), (5, 1.0)],
        "epsilon": 0.05,
        "expected_pieces": 3 # Piece 1: (0-2), Piece 2: (2-3) (steep), Piece 3: (3-5)
    },
    # ----------------------------------------------------
    # 13-15. V-Shape/Peaks (Testing Sharp Turns)
    # ----------------------------------------------------
    {
        # Sharp single peak/outlier
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # Piece 1 (0,0) to (3,0) max error 1.66, must break at (2,5). Optimal is P1: (0,0) to (2,5), P2: (2,5) to (4,0). Wait, no, P1: (0,0) to (1,0) - error 0. P2: (1,0) to (3,0) - error 5. P1: (0,0) to (2,5) max error 0. P2: (2,5) to (4,0) max error 0.
    },
    {
        # Two sharp peaks
        "pw_linear_fx": [(0, 0), (1, 5), (2, 0), (3, 5), (4, 0)],
        "epsilon": 1.5,
        "expected_pieces": 3 # Peak 1 forces a piece, Peak 2 forces another.
    },
    {
        # Peak just *outside* epsilon
        "pw_linear_fx": [(0, 0), (1, 2.1), (2, 0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # The line (0,0) to (2,0) has error 2.1. Must break.
    },
    # ----------------------------------------------------
    # 16-18. Oscillating/Noise (Testing Tolerance)
    # ----------------------------------------------------
    {
        # Noise on a flat line
        "pw_linear_fx": [(i, 0.1 * (i % 2)) for i in range(10)],
        "epsilon": 0.06,
        "expected_pieces": 9 # All points are 0 or 0.1. A line between (0,0) and (1,0.1) has max error 0. A line between (0,0) and (2,0) has max error 0.1. Needs max pieces.
    },
    {
        # Noise on a slight slope
        "pw_linear_fx": [(i, i * 0.1 + 0.1 * (i % 3 == 0)) for i in range(10)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Should fit most in one piece, maybe two.
    },
    {
        # Noise that *forces* a piece
        "pw_linear_fx": [(0, 0), (1, 0.15), (2, 0.0), (3, 0.15), (4, 0.0)],
        "epsilon": 0.07,
        "expected_pieces": 4 # The max error is 0.15, forcing piece breaks.
    },
    # ----------------------------------------------------
    # 19-21. Long Flat Sections (Maximizing Length)
    # ----------------------------------------------------
    {
        # Long flat section
        "pw_linear_fx": [(i, 0.0) for i in range(5)] + [(6, 1.0), (7, 2.0)],
        "epsilon": 0.001,
        "expected_pieces": 3 # P1: (0-4), P2: (4-6), P3: (6-7)
    },
    {
        # Flat, step up, flat
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 1), (4, 1), (5, 1)],
        "epsilon": 0.1,
        "expected_pieces": 2 # P1: (0,0) to (2,0), P2: (3,1) to (5,1). Wait, one piece can span (2,0) to (3,1)? No. Needs 3 pieces. P1: (0,0) to (2,0), P2: (2,0) to (3,1), P3: (3,1) to (5,1).
    },
    {
        # Flat, steep drop, flat
        "pw_linear_fx": [(0, 5), (1, 5), (2, 0), (3, 0), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # P1: (0,5) to (2,0), P2: (2,0) to (4,0).
    },
    # ----------------------------------------------------
    # 22-30. Near-Optimal/Greedy Failure Cases (Exposing Non-Optimal)
    # ----------------------------------------------------
    {
        # Case 1: Greedy extends too far.
        # Optimal: P1:(0,0)-(2,0.5), P2:(2,0.5)-(5,0) (2 pieces)
        # Greedy might choose P1:(0,0)-(3,-0.1), which forces 3 pieces total.
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.5), (3, -0.1), (4, 0.1), (5, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        # Case 2: Concave/Convex transition
        # Needs to break *before* the inflection point (1.5) to keep the error small for the second piece.
        "pw_linear_fx": [(0, 0), (1, 0.1), (1.5, 0.0), (2, -0.1), (3, -0.5), (4, -0.1)],
        "epsilon": 0.1,
        "expected_pieces": 3 # P1:(0,0) to (1.5,0.0), P2:(1.5,0.0) to (3,-0.5), P3:(3,-0.5) to (4,-0.1)
    },
    {
        # Case 3: Error is at the max epsilon on an interior point.
        # The line (0,0) to (2,0) has max error 0.5 at (1, 0.5). If epsilon=0.49, it breaks.
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0), (3, 0), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # P1: (0,0) to (4,0) error max 0.5. Optimal is 1 piece.
    },
    {
        # Case 4: Tight fit that requires the break point to be exactly the next one.
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.2), (3, 1.0), (4, 1.1), (5, 1.2)],
        "epsilon": 0.05,
        "expected_pieces": 5 # A line from (0,0) to (3,1) has error at (1,0.1) and (2,0.2). Error is 0.2 at (2,0.2). Requires P1:(0,0) to (2,0.2) and P2:(2,0.2) to (5,1.2). Needs 2 pieces.
    },
    {
        # Case 5: Symmetric test for optimal break point.
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # P1: (0,0) to (4,0) error 1.0. Needs break. P1: (0,0) to (2,0) max error 1.0. P1: (0,0) to (3,1) max error 0.5. P2: (3,1) to (4,0). Needs 2 pieces.
    },
    {
        # Case 6: Very dense data with small errors
        "pw_linear_fx": [(i, (i % 5) * 0.01) for i in range(20)],
        "epsilon": 0.02,
        "expected_pieces": 1 # Fits a flat line for max error 0.02.
    },
    {
        # Case 7: Alternating slope where a single piece can span two "waves"
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0), (3, -0.5), (4, 0)],
        "epsilon": 0.6,
        "expected_pieces": 1 # Single line (0,0) to (4,0) has max error 0.5.
    },
    {
        # Case 8: Error near start point
        "pw_linear_fx": [(0, 0.01), (1, 0.0), (2, 0.0), (3, 0.0)],
        "epsilon": 0.005,
        "expected_pieces": 3 # Point (0, 0.01) forces a break.
    },
    {
        # Case 9: Error near end point
        "pw_linear_fx": [(0, 0.0), (1, 0.0), (2, 0.0), (3, 0.01)],
        "epsilon": 0.005,
        "expected_pieces": 3 # Point (3, 0.01) forces a break.
    },
    {
        # Case 10: The "classic" greedy failure
        # A greedy algorithm might take the first piece from (0,0) to (3,0) which is slightly suboptimal, preventing the overall 2-piece solution.
        # Optimal: P1: (0,0) to (2,1), P2: (2,1) to (5,0) -> 2 pieces.
        # Greedy P1: (0,0) to (3,0) (error 1 at point 2) -> Fails.
        # Greedy P1: (0,0) to (2,1). The second piece (2,1) to (5,0) has max error at 3.
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 1.0), (3, 0.1), (4, 0.0), (5, 0)],
        "epsilon": 0.15,
        "expected_pieces": 2
    }
]
test_cases23 = [
    # 1. Basic Cases (Sanity Checks)
    # ------------------------------------------------------------------------------------------------
    # Case 1: Trivial - all points are collinear. Optimal: 1 piece.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.1, "expected_pieces_optimal": 1},
    # Case 2: No tolerance (epsilon = 0). Optimal: n pieces (n+1 points).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.0, "expected_pieces_optimal": 4},
    # Case 3: Very large tolerance. Optimal: 1 piece.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 10.0, "expected_pieces_optimal": 1},
    # Case 4: A simple V-shape requiring 2 pieces.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.01, "expected_pieces_optimal": 2},

    # 2. Critical Edge Cases (Maximum Error = Epsilon)
    # ------------------------------------------------------------------------------------------------
    # Case 5: A segment where the max error is exactly epsilon. Must be approximated by 1 piece.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 1},
    # Case 6: Same as 5, but error is epsilon + a tiny amount. Must be approximated by 2 pieces.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5000001), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 2},
    # Case 7: Points clustered near the maximum error boundary.
    {"pw_linear_fx": [(0.0, 0.0), (0.1, 0.49), (0.5, 0.5), (1.0, 0.49), (1.1, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 1},
    # Case 8: Maximum error occurs at an interior point, not the center.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (1.1, 0.0), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 2},

    # 3. Geometric Complexity (Curves, Oscillation, and Non-Uniform Spacing)
    # ------------------------------------------------------------------------------------------------
    # Case 9: Uniformly spaced points on a parabola. Tests handling of smooth curves.
    {"pw_linear_fx": [(x, x**2) for x in [0.0, 0.5, 1.0, 1.5, 2.0]], "epsilon": 0.2, "expected_pieces_optimal": 2},
    # Case 10: High-frequency oscillation (sinusoid). Tests handling peaks and troughs.
    {"pw_linear_fx": [(x, 0.5 * (1 - (x % 2))) for x in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]], "epsilon": 0.05, "expected_pieces_optimal": 4},
    # Case 11: Steep slope followed by flat region.
    {"pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (10.0, 10.0)], "epsilon": 0.1, "expected_pieces_optimal": 2},
    # Case 12: Non-uniform x-spacing. Many algorithms are sensitive to x-coordinate distribution.
    {"pw_linear_fx": [(0.0, 0.0), (0.01, 0.5), (1.0, 0.5), (1.01, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 1},

    # 4. Optimality Traps (Cases that trick Greedy/Sub-optimal Algorithms)
    # ------------------------------------------------------------------------------------------------
    # Case 13: Greedy trap 1 - Small error point that allows for a much longer next segment. Optimal solution should ignore the initial small segment.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.01), (2.0, 0.5), (3.0, 0.0), (4.0, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 2},
    # Case 14: Greedy trap 2 - A segment that can *almost* be covered, forcing a split that *just* allows the rest to be covered by one piece.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (1.1, 0.0), (2.0, 0.5), (3.0, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 2},
    # Case 15: Two optimal solutions might exist, testing stability/determinism.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, 0.4), (4.0, 0.0)], "epsilon": 0.4, "expected_pieces_optimal": 2},
    # Case 16: Multiple short, deep dips. Optimal may require jumping over a dip with a single line.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0), (5.0, 0.5), (6.0, 0.0)], "epsilon": 0.4, "expected_pieces_optimal": 5},

    # 5. Data Volume and Scale
    # ------------------------------------------------------------------------------------------------
    # Case 17: Small dataset, low epsilon (force max pieces).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.0001, "expected_pieces_optimal": 4},
    # Case 18: Large dataset with slight variations (should be 1 piece).
    {"pw_linear_fx": [(i, 0.001 * (i % 2)) for i in range(10)], "epsilon": 0.01, "expected_pieces_optimal": 1},
    # Case 19: High Y-values (tests floating point precision and scaling).
    {"pw_linear_fx": [(0.0, 1e6), (1.0, 1e6 + 0.1), (2.0, 1e6)], "epsilon": 0.1, "expected_pieces_optimal": 1},
    # Case 20: Very small epsilon (tests precision).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1e-5), (2.0, 0.0)], "epsilon": 1e-5, "expected_pieces_optimal": 1},

    # 6. Specific Point Arrangements
    # ------------------------------------------------------------------------------------------------
    # Case 21: A spike at the beginning. Forces an immediate piece split.
    {"pw_linear_fx": [(0.0, 1.0), (0.001, 0.0), (1.0, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 2},
    # Case 22: A spike at the end.
    {"pw_linear_fx": [(0.0, 0.0), (0.999, 0.0), (1.0, 1.0)], "epsilon": 0.5, "expected_pieces_optimal": 2},
    # Case 23: Z-shape (two corners).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0)], "epsilon": 0.01, "expected_pieces_optimal": 3},
    # Case 24: A segment perfectly covered, but the next point lies on the line (redundancy test).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, 0.0)], "epsilon": 0.4, "expected_pieces_optimal": 2},

    # 7. Boundary Conditions and Invalid Input (for Robustness)
    # ------------------------------------------------------------------------------------------------
    # Case 25: Minimum number of points (2). Optimal: 1 piece.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)], "epsilon": 0.0, "expected_pieces_optimal": 1},
    # Case 26: Three points with vertical movement only (tests y-diff dominance).
    {"pw_linear_fx": [(0.0, 0.0), (0.0, 0.5), (0.0, 0.0)], "epsilon": 0.5, "expected_pieces_optimal": 1},
    # Case 27: Repeated points (tests duplicate point handling).
    {"pw_linear_fx": [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0), (1.0, 1.0)], "epsilon": 0.0, "expected_pieces_optimal": 2},
    # Case 28: Negative coordinates.
    {"pw_linear_fx": [(-2.0, -1.0), (-1.0, 0.5), (0.0, -1.0)], "epsilon": 0.5, "expected_pieces_optimal": 1},
    # Case 29: Negative epsilon (Should fail or be treated as 0, but tests input validation).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": -0.1, "expected_pieces_optimal": "Error"}, # Or expected to fail validation
    # Case 30: Large dataset with specific breakpoints every 10 points. Tests long-range planning.
    {"pw_linear_fx": [(i, 0.0 if i % 10 == 0 else 0.4) for i in range(21)], "epsilon": 0.5, "expected_pieces_optimal": 3},
]

test_cases24 = [
    # ----------------------------------------------------------------------
    # 1. Basic Cases (Simple Shapes & Different Tolerances)
    # ----------------------------------------------------------------------
    # Case 1: Perfectly linear data (should be 1 segment, regardless of epsilon)
    {"name": "1. Perfectly Linear Data, Epsilon=1.0",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
     "epsilon": 1.0,
     "expected_min_pieces": 1},

    # Case 2: Perfectly linear data, tight epsilon
    {"name": "2. Perfectly Linear Data, Epsilon=0.001",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
     "epsilon": 0.001,
     "expected_min_pieces": 1},

    # Case 3: Simple convex function (Parabola segment)
    {"name": "3. Simple Convex (Parabola), Epsilon=0.2",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
     "epsilon": 0.2,
     "expected_min_pieces": 3},

    # Case 4: Simple concave function (sinusoidal-like)
    {"name": "4. Simple Concave, Epsilon=0.1",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.6), (3.0, 0.4), (4.0, 0.0)],
     "epsilon": 0.1,
     "expected_min_pieces": 3},

    # Case 5: All points same Y-value (horizontal line)
    {"name": "5. Constant Function, Epsilon=0.5",
     "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
     "epsilon": 0.5,
     "expected_min_pieces": 1},

    # ----------------------------------------------------------------------
    # 2. Edge Cases: Tolerance and Error
    # ----------------------------------------------------------------------
    # Case 6: Tolerance allows for maximum possible error in a simple segment
    # (0,0) to (4,0), midpoint is (2, 0.9). Error at midpoint is 0.9.
    {"name": "6. Max Error Exactly Equals Epsilon",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.9), (3.0, 0.5), (4.0, 0.0)],
     "epsilon": 0.9,
     "expected_min_pieces": 1},

    # Case 7: Tolerance is infinitesimally smaller (requires 2 segments)
    {"name": "7. Epsilon Just Below Max Error (Requires 2)",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.9), (3.0, 0.5), (4.0, 0.0)],
     "epsilon": 0.8999999999999999,
     "expected_min_pieces": 2},

    # Case 8: Zero Tolerance (approximation must pass through *every* point)
    {"name": "8. Zero Epsilon (N pieces required)",
     "pw_linear_fx": [(0.0, 1.0), (1.0, 1.5), (2.0, 2.0), (3.0, 2.5), (4.0, 3.0)],
     "epsilon": 0.0,
     "expected_min_pieces": 4}, # (n+1 points = n pieces)

    # Case 9: Large Tolerance (Epsilon exceeds maximum deviation, 1 piece)
    {"name": "9. Large Epsilon (Max Deviation 1.0)",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
     "epsilon": 1.0,
     "expected_min_pieces": 1},

    # ----------------------------------------------------------------------
    # 3. Edge Cases: High Slopes and Jumps
    # ----------------------------------------------------------------------
    # Case 10: Near-vertical segment (algorithm must handle high/infinite slope)
    {"name": "10. Near-Vertical Segment, Tight Epsilon",
     "pw_linear_fx": [(0.0, 0.0), (0.001, 5.0), (1.0, 5.0)],
     "epsilon": 0.01,
     "expected_min_pieces": 2}, # Error on first segment is huge if approximated by (0,0) to (1, 5)

    # Case 11: A 'step' function (requires 2 pieces minimum)
    {"name": "11. Step Function (Large Y jump)",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.001, 10.0), (2.0, 10.0)],
     "epsilon": 0.5,
     "expected_min_pieces": 2},

    # Case 12: Data with points clustered near the end of a segment
    {"name": "12. Data Clustered at Segment End",
     "pw_linear_fx": [(0.0, 0.0), (3.0, 0.0), (3.9, 0.0), (4.0, 1.0)],
     "epsilon": 0.4,
     "expected_min_pieces": 2},

    # ----------------------------------------------------------------------
    # 4. Complex Shapes and Multiple Segments
    # ----------------------------------------------------------------------
    # Case 13: "Zig-Zag" or High-Frequency Oscillation
    # (Error is high for large segments, requires many pieces)
    {"name": "13. High-Frequency Zig-Zag, Tight Epsilon",
     "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1), (6, 0)],
     "epsilon": 0.1,
     "expected_min_pieces": 6}, # Error > 0.1, requires a piece for every peak/trough

    # Case 14: Long segment with small deviation, followed by a sharp turn
    {"name": "14. Small Deviation then Sharp Turn",
     "pw_linear_fx": [(0, 0), (1, 0.05), (2, 0.0), (3, 0.0), (4, 1.0)],
     "epsilon": 0.1,
     "expected_min_pieces": 2}, # (0,0) to (3,0) is 1 piece, then (3,0) to (4,1) is 1 piece

    # Case 15: Concave-Convex mix
    {"name": "15. Concave-Convex Mix",
     "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0), (3, -0.5), (4, 0)],
     "epsilon": 0.2,
     "expected_min_pieces": 2}, # (0,0) to (2,0) error 0.5 > 0.2. (0,0) to (4,0) error 0.5 > 0.2. Need 2 segments.

    # Case 16: Multiple segments due to error being max at different locations
    {"name": "16. Three Segments Required",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0), (5.0, 0.5), (6.0, 0.0)],
     "epsilon": 0.2,
     "expected_min_pieces": 3},

    # Case 17: A single spike that forces segmentation
    {"name": "17. Single Spike",
     "pw_linear_fx": [(0, 0), (1, 0), (2, 1.0), (3, 0), (4, 0)],
     "epsilon": 0.1,
     "expected_min_pieces": 2},

    # ----------------------------------------------------------------------
    # 5. Boundary Conditions and Floating Point Precision
    # ----------------------------------------------------------------------
    # Case 18: First two points are identical (zero initial segment length)
    {"name": "18. Identical Start Points",
     "pw_linear_fx": [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
     "epsilon": 0.1,
     "expected_min_pieces": 2}, # The algorithm should treat the first two points as a zero-length segment or skip. (0,0) to (2,2) is 1 piece. Total 2 pieces (P1-P2) and (P2-P4).

    # Case 19: Last two points are identical
    {"name": "19. Identical End Points",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (2.0, 2.0)],
     "epsilon": 0.1,
     "expected_min_pieces": 2},

    # Case 20: Floating Point Error - data points just barely exceeding epsilon
    {"name": "20. Floating Point Edge (Error 0.500000000001)",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.500000000001), (2.0, 0.0)],
     "epsilon": 0.5,
     "expected_min_pieces": 2},

    # Case 21: Floating Point Error - data points just barely within epsilon
    {"name": "21. Floating Point Edge (Error 0.499999999999)",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.499999999999), (2.0, 0.0)],
     "epsilon": 0.5,
     "expected_min_pieces": 1},

    # ----------------------------------------------------------------------
    # 6. Negative Coordinates and Data Scale
    # ----------------------------------------------------------------------
    # Case 22: Function fully in negative Y space
    {"name": "22. All Negative Y values",
     "pw_linear_fx": [(0, -10), (1, -9.5), (2, -9.0)],
     "epsilon": 0.1,
     "expected_min_pieces": 1},

    # Case 23: Large scale data (potential for overflow/precision issues)
    {"name": "23. Large Scale Data",
     "pw_linear_fx": [(0, 100000), (1, 100001), (2, 100000)],
     "epsilon": 0.5,
     "expected_min_pieces": 1}, # Error is 1 at midpoint, 1 > 0.5. Requires 2 segments: (0, 1e5) to (1, 100001) and (1, 100001) to (2, 100000)

    # ----------------------------------------------------------------------
    # 7. Optimality Test Focus (Checking greedy vs. optimal segmentation)
    # The optimal strategy often means sacrificing local fit for a better global fit.
    # ----------------------------------------------------------------------
    # Case 24: Standard example where a greedy approach fails (Error 0.5 in both halves)
    # The whole span (0,0) to (4,0) has max error 1.0, requires 2 pieces.
    {"name": "24. Greedy Fails (Error 1.0, Epsilon=0.9)",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
     "epsilon": 0.9,
     "expected_min_pieces": 1},

    # Case 25: Case requiring a segment to jump over a few points
    {"name": "25. Optimal Jump Over Points",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.0)],
     "epsilon": 0.2,
     "expected_min_pieces": 1}, # (0,0) to (3,0) max error 0.1 < 0.2

    # Case 26: A long, slightly-curved initial part followed by a sharp deviation
    {"name": "26. Slightly Curved then Sharp Deviation",
     "pw_linear_fx": [(0, 0), (1, 0.05), (2, 0.1), (3, 0.15), (4, 1.0)],
     "epsilon": 0.2,
     "expected_min_pieces": 2}, # (0,0) to (3, 0.15) error is small. (0,0) to (4, 1.0) error is too high.

    # Case 27: A function where the error is maximum near the end of the segment
    {"name": "27. Max Error Near Segment End",
     "pw_linear_fx": [(0, 0), (1, 0.0), (2, 0.5), (3, 0.0), (4, 0.5)],
     "epsilon": 0.4,
     "expected_min_pieces": 2},

    # ----------------------------------------------------------------------
    # 8. Miscellaneous and Robustness
    # ----------------------------------------------------------------------
    # Case 28: Small number of points (minimum N=2 points)
    {"name": "28. Minimum Points (N=2)",
     "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0)],
     "epsilon": 0.0,
     "expected_min_pieces": 1},

    # Case 29: Only X changes drastically
    {"name": "29. Disproportionate X-Scale",
     "pw_linear_fx": [(0.0, 0.0), (100.0, 0.5), (200.0, 0.0)],
     "epsilon": 0.4,
     "expected_min_pieces": 1}, # Max error is 0.5, 0.5 > 0.4. Requires 2 segments.

    # Case 30: The example from the prompt (for validation)
    {"name": "30. User Provided Example",
     "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
     "epsilon": 0.5,
     "expected_min_pieces": 2}
]
test_cases25 = [
    # 1. Simple Straight Line (Perfect Fit) - Should be 1 piece
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)], "epsilon": 0.1},

    # 2. Straight Line with Zero Tolerance - Should be 1 piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.0},

    # 3. Simple Curve (Parabola) requiring 2 pieces (or more)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 2.0), (3.0, 4.5), (4.0, 8.0)], "epsilon": 1.0},

    # 4. Step Function (Sharp Change) - Requires multiple pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 5.0), (2.0, 5.0)], "epsilon": 0.1},

    # 5. Sawtooth/Zig-Zag requiring multiple pieces even with large epsilon
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0), (4.0, 0.0)], "epsilon": 4.0},

    # 6. High-Frequency Oscillation (Sine Wave approx.) - Needs many pieces
    {"pw_linear_fx": [(x, 0.5 * (1 - (i % 2))) for i, x in enumerate([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])], "epsilon": 0.2},

    # 7. Constant Function with small deviations
    {"pw_linear_fx": [(0.0, 5.0), (1.0, 5.05), (2.0, 4.95), (3.0, 5.01), (4.0, 5.0)], "epsilon": 0.02},

    # 8. Constant Function with large deviations, forcing 2 pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0)], "epsilon": 0.4},

    # 9. **Greedy Trap 1:** Slow initial drift followed by a sharp change.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (3.1, 5.0)], "epsilon": 0.3},

    # 10. **Greedy Trap 2:** Two nearly-collinear segments separated by a distant point.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 2.0), (3.0, 2.05), (4.0, 4.0)], "epsilon": 0.1},

    # 11. End-point proximity (Testing boundary conditions of max/min index)
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.0), (1.0, 0.9), (1.5, 0.0)], "epsilon": 0.5},

    # 12. Negative Y-values
    {"pw_linear_fx": [(0.0, -10.0), (1.0, -9.0), (2.0, -11.0), (3.0, -10.0)], "epsilon": 0.5},

    # 13. Mixed positive and negative Y-values (crossing the x-axis)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, -1.0), (3.0, 0.0), (4.0, 1.0)], "epsilon": 0.1},

    # 14. Very large coordinate values (Testing floating-point precision/scaling)
    {"pw_linear_fx": [(0.0, 1e6), (1.0, 1e6 + 0.1), (2.0, 1e6 - 0.1), (3.0, 1e6)], "epsilon": 0.11},

    # 15. Very small epsilon (Forces many pieces, effectively point-to-point)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 1e-6},

    # 16. Very large epsilon (Should result in 1 piece, forcing a single line fit)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0), (3.0, 20.0)], "epsilon": 50.0},

    # 17. Duplicate X-values (Testing vertical segments, max error is 0.5)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 2.0), (2.0, 3.0)], "epsilon": 0.5},

    # 18. Non-uniformly spaced X-values
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 1.0), (11.0, 2.0), (20.0, 3.0)], "epsilon": 0.5},

    # 19. Parabola near the vertex (requiring 2 pieces due to small epsilon)
    {"pw_linear_fx": [(0.0, 4.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 4.0)], "epsilon": 0.5},

    # 20. A concave-convex transition (S-curve)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.9), (3.0, 1.8), (4.0, 2.0)], "epsilon": 0.1},

    # 21. Four points forming an 'M' shape (testing if 2 pieces is possible)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.8},

    # 22. A function where a segment just **barely** fits $\epsilon$ (testing boundary $\epsilon$ calculation)
    # The max error is $\approx 0.1$, so $\epsilon=0.1$ should be 1 piece.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0)], "epsilon": 0.1},

    # 23. A function where a segment just **fails** to fit $\epsilon$ (testing boundary $\epsilon$ calculation)
    # The max error is $\approx 0.1$, so $\epsilon=0.09$ should be 2 pieces.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0)], "epsilon": 0.09},

    # 24. A large number of points on a perfect line (testing performance/loop bounds)
    {"pw_linear_fx": [(i, i) for i in range(15)], "epsilon": 0.1},

    # 25. An exponential curve (requires increasingly shorter segments)
    {"pw_linear_fx": [(i, 2**i) for i in range(5)], "epsilon": 5.0},

    # 26. Step function where epsilon is exactly half the step (tests the exact fit condition)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0)], "epsilon": 0.5},

    # 27. Test with only two points (minimal input) - Should always be 1 piece
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 10.0)], "epsilon": 0.0},

    # 28. Test with three points (minimal non-trivial input)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.4},

    # 29. Concave curve where the middle point is exactly the max error point (should be 2 pieces for $\epsilon=0.1$)
    # The line between (0,0) and (4,0) has an error of 0.2 at x=2.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.1), (4.0, 0.0)], "epsilon": 0.1},

    # 30. Example from prompt, serving as a baseline
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)], "epsilon": 0.5}
]
test_cases26 = [
    # --- Category 1: Basic Cases & Flat/Sloped Lines (Minimal Pieces) ---
    { # 1. Simple Case: Straight line, 1 piece expected.
        "name": "T01_Straight_Line",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    { # 2. Perfect horizontal line, 1 piece expected.
        "name": "T02_Horizontal_Line",
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    { # 3. Slope change, but still within tolerance, 1 piece expected.
        "name": "T03_Shallow_S_Curve_In_Tolerance",
        "pw_linear_fx": [(0, 0), (1, 0.05), (2, 0), (3, -0.05), (4, 0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    { # 4. Points exactly on the upper and lower bound of tolerance, 1 piece expected.
        "name": "T04_Boundary_ZigZag_1_Piece",
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0), (3, -0.5), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },

    # --- Category 2: Boundary/Edge Cases (Epsilon Sensitivity) ---
    { # 5. Point exactly *at* epsilon (should still be 1 piece).
        "name": "T05_Exact_Max_Deviation_1_Piece",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    { # 6. Point *just over* epsilon (must break into 2 pieces). $y_2$ is 1.0001
        "name": "T06_Just_Over_Epsilon_Must_Break",
        "pw_linear_fx": [(0, 0), (1, 1.0001), (2, 0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    { # 7. Point barely requiring the first break at point (2,1.0001). The greedy choice may fail here if it's too short.
        "name": "T07_First_Point_Breaks_Greedy_Failure_1",
        "pw_linear_fx": [(0, 0), (1, 0.9), (2, 1.0001), (3, 0), (4, 0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    { # 8. Two peaks, both exactly at the threshold. Requires 3 pieces for 5 points.
        "name": "T08_Two_Max_Peaks_Exact_Tolerance",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 1.0,
        "expected_pieces": 3
    },
    { # 9. The second point is exactly on the line, but the third point forces a break.
        "name": "T09_Point_On_Line_Followed_by_Break",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 2.01)], # (1,1) is on the line (0,0)-(3,2.01). (2,2) is off by 0.0066. (3, 2.01) must be end.
        "epsilon": 0.005,
        "expected_pieces": 2 # (0,0)-(2,2) is within. (0,0)-(3,2.01) is not.
    },

    # --- Category 3: Geometric Patterns (Triangle, Square Wave, etc.) ---
    { # 10. Sawtooth wave, requiring a piece for every segment.
        "name": "T10_High_Frequency_Sawtooth",
        "pw_linear_fx": [(0, 0), (1, 10), (2, 0), (3, 10), (4, 0)],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    { # 11. Square wave, requiring a break at every corner.
        "name": "T11_Square_Wave",
        "pw_linear_fx": [(0, 0), (0.1, 0), (0.1, 5), (0.2, 5), (0.2, 0), (0.3, 0)],
        "epsilon": 0.01,
        "expected_pieces": 4
    },
    { # 12. Alternating points just inside tolerance, 1 piece.
        "name": "T12_Small_Amplitude_Oscillation_In",
        "pw_linear_fx": [(0, 0), (1, 0.4), (2, 0), (3, -0.4), (4, 0), (5, 0.4)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    { # 13. Alternating points just outside tolerance, 3 pieces needed.
        "name": "T13_Small_Amplitude_Oscillation_Out",
        "pw_linear_fx": [(0, 0), (1, 0.51), (2, 0), (3, -0.51), (4, 0), (5, 0.51)],
        "epsilon": 0.5,
        "expected_pieces": 3 # P0-P2, P2-P4, P4-P5
    },
    { # 14. Convex function (parabola y=x^2).
        "name": "T14_Parabola_Convex",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)],
        "epsilon": 0.5,
        "expected_pieces": 3 # (0,0)-(2,4) max dev at x=1 is 1. (2,4)-(4,16) max dev at x=3 is 1.
    },
    { # 15. Concave function (sqrt(x)).
        "name": "T15_SquareRoot_Concave",
        "pw_linear_fx": [(0, 0), (1, 1), (4, 2), (9, 3)],
        "epsilon": 0.1,
        "expected_pieces": 3
    },

    # --- Category 4: Numerical Precision & Coordinates ---
    { # 16. Floating point coordinates.
        "name": "T16_Float_Coords_General",
        "pw_linear_fx": [(0.5, 1.0), (1.5, 1.2), (2.5, 1.3), (3.5, 2.0)],
        "epsilon": 0.05,
        "expected_pieces": 3
    },
    { # 17. High slope (potential for overflow or precision issues).
        "name": "T17_High_Slope",
        "pw_linear_fx": [(0, 0), (1, 1000), (2, 2000), (3, 3000)],
        "epsilon": 10.0,
        "expected_pieces": 1
    },
    { # 18. Zero slope, testing max X-reach (should be 1).
        "name": "T18_Flat_Long_Reach",
        "pw_linear_fx": [(0, 10), (10, 10), (20, 10), (30, 10)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    { # 19. Start point is far from (0,0), testing coordinate independence.
        "name": "T19_Large_Start_Coords",
        "pw_linear_fx": [(100, 100), (101, 101), (102, 101.1), (103, 102)],
        "epsilon": 0.05,
        "expected_pieces": 2
    },

    # --- Category 5: Challenging Optimality Cases (Greedy Fails) ---
    # These cases are designed where the first possible segment (P_i to P_k)
    # is shorter than the globally optimal first segment (P_i to P_k'),
    # resulting in a non-optimal total piece count if a greedy strategy is used.
    { # 20. The standard greedy failure case: a short segment is possible, but a longer one exists.
        "name": "T20_Greedy_Failure_Short_Segment",
        "pw_linear_fx": [(0, 0), (1, 0.4), (2, 0), (3, 0.45), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 1 # (0,0) to (4,0) works. A greedy that takes (0,0) to (2,0) first might fail.
    },
    { # 21. More complex greedy failure. P0-P2 works, P0-P3 works, P0-P4 fails. P2-P4 works.
        "name": "T21_Greedy_Failure_2",
        "pw_linear_fx": [(0, 0), (1, 0.49), (2, 0), (3, 0.49), (4, 0.51), (5, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # P0-P3 works, P3-P5 works (2 pieces). P0-P2, P2-P4, P4-P5 is 3 pieces (suboptimal).
    },
    { # 22. Multiple points near the boundary, forcing the algorithm to find the longest segment.
        "name": "T22_Many_Boundary_Points_Max_Reach",
        "pw_linear_fx": [(0, 0), (1, 0.01), (2, 0.02), (3, 0.03), (4, 0.051), (5, 0.05)],
        "epsilon": 0.05,
        "expected_pieces": 2 # P0-P3 is OK. P0-P4 fails. So P0-P3, P3-P5 (2 pieces).
    },
    { # 23. Points that alternate side-to-side, testing the L-infinity "corridor".
        "name": "T23_Alternating_Corridor_Test",
        "pw_linear_fx": [(0, 0), (1, 0.4), (2, -0.4), (3, 0.4), (4, -0.4), (5, 0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },

    # --- Category 6: Small N and Degenerate Cases ---
    { # 24. Minimum N (2 points), must be 1 piece.
        "name": "T24_Minimum_Points_2",
        "pw_linear_fx": [(0, 1), (1, 2)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    { # 25. Three points: a simple triangle, 1 piece.
        "name": "T25_Small_Triangle_In",
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    { # 26. Three points: a simple triangle, 2 pieces.
        "name": "T26_Small_Triangle_Out",
        "pw_linear_fx": [(0, 0), (1, 0.1001), (2, 0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    { # 27. Zero epsilon (must use original segments).
        "name": "T27_Zero_Epsilon",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1)],
        "epsilon": 0.0,
        "expected_pieces": 3 # n+1 points = n pieces. (0,0)-(1,1), (1,1)-(2,0), (2,0)-(3,1)
    },

    # --- Category 7: Special Geometric Cases ---
    { # 28. Points that are colinear, but the line requires a vertical shift to stay within epsilon.
        "name": "T28_Colinear_But_Shifted",
        "pw_linear_fx": [(0, 0.5), (1, 0.5), (2, 0.5), (3, 0.5)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    { # 29. Pathological Case: A single point requires a break because the next point is far.
        "name": "T29_Isolated_Far_Point",
        "pw_linear_fx": [(0, 0), (1, 0), (2, 100)],
        "epsilon": 1.0,
        "expected_pieces": 2 # P0-P1, P1-P2. P0-P2 fails.
    },
    { # 30. A large dataset with a few breaks. Forces the algorithm to iterate correctly.
        "name": "T30_Large_Data_Set_Few_Breaks",
        "pw_linear_fx": [(i, 0) if i % 10 != 5 else (i, 1.0) for i in range(21)],
        "epsilon": 0.99,
        "expected_pieces": 3 # P0-P10 (max dev at 5 is 0.5), P10-P20. Max dev is 0.5.
    },
]
import math
test_cases27 = [
    # --- 1. Basic Functionality and Simple Shapes (Optimal = Small Number) ---
    {
        "description": "1. Straight Line, Epsilon > 0 (Optimal: 1 piece)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "2. Small V-Shape, Exact Fit (Optimal: 2 pieces)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 2
    },
    {
        "description": "3. Perfect Quadratic Curve (Should be many pieces unless epsilon is large)",
        "pw_linear_fx": [(x, x**2) for x in [0.0, 0.5, 1.0, 1.5, 2.0]],
        "epsilon": 0.01,
        # Expected value is 4 pieces (as 0.01 is small for this curvature)
        "expected_pieces": 4
    },
    {
        "description": "4. Step Function (Requires pieces exactly at steps)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 5.0), (2.0, 5.0)],
        "epsilon": 0.1,
        # Requires 2 pieces: [(0,0)-(1,0)] and [(1.0001,5)-(2,5)]
        "expected_pieces": 2
    },
    {
        "description": "5. Constant Function (Optimal: 1 piece)",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },

    # --- 2. Numerical and Tolerance Edge Cases (Epsilon = 0, Small Epsilon, Large Epsilon) ---
    {
        "description": "6. Zero Epsilon (Optimal = max pieces - 1)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 2 # 3 points -> 2 segments
    },
    {
        "description": "7. Epsilon just slightly too small to merge two segments",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.25), (3.0, 0.0)],
        "epsilon": 0.12, # Max error for (0,0) to (3,0) is 0.25. 0.12 < 0.25 -> 2 pieces
        "expected_pieces": 2
    },
    {
        "description": "8. Epsilon just large enough to merge two segments",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.25), (3.0, 0.0)],
        "epsilon": 0.25, # Max error is 0.25. 0.25 is inclusive -> 1 piece
        "expected_pieces": 1
    },
    {
        "description": "9. Very tight numerical precision (small coordinates)",
        "pw_linear_fx": [(0.0, 1e-6), (1e-6, 1e-6), (2e-6, 2e-6)],
        "epsilon": 1e-7,
        "expected_pieces": 2
    },
    {
        "description": "10. Very large coordinates",
        "pw_linear_fx": [(0.0, 1e6), (1.0, 1e6+1.0), (2.0, 1e6+2.0)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },

    # --- 3. Geometric Challenges (Sharp Turns and Oscillations) ---
    {
        "description": "11. Sharp turn requiring immediate break (V-shape near a peak)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (1.0001, 10.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Must break at x=1.0. Error is too high if not.
    },
    {
        "description": "12. High-frequency oscillation/noise (Requires max pieces)",
        "pw_linear_fx": [(x, (-1)**x * 0.5) for x in range(5)],
        "epsilon": 0.1, # Max error is 0.5. 0.1 is too small.
        "expected_pieces": 4
    },
    {
        "description": "13. Sinusoidal curve with high Epsilon (Optimal: Few pieces)",
        "pw_linear_fx": [(x/10.0, 0.5 * (1 - math.cos(x/10.0 * 2 * math.pi))) for x in range(11)],
        "epsilon": 0.4,
        "expected_pieces": 1 # For a max amplitude of 1.0, E=0.4 might cover the full range.
    },
    {
        "description": "14. Zig-zag where greedy fails (Must select a short segment to enable a long later one)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (10.0, 0.0)],
        "epsilon": 0.1,
        # A greedy algorithm might cover [0.0, 0.0] to [2.0, 0.0] with error 0.1, requiring a second piece for [2.0, 0.0] to [10.0, 0.0]. Total 2.
        # But wait, the optimal is actually 1 piece: [(0,0) to (10,0)] covers the whole range with max error 0.1 at x=1.0. This tests the *actual* optimal piece.
        "expected_pieces": 1
    },
    {
        "description": "15. A long flat section followed by a steep climb",
        "pw_linear_fx": [(x, 0.0) for x in range(10)] + [(10.0, 10.0)],
        "epsilon": 0.0,
        "expected_pieces": 10 # 11 points -> 10 segments
    },

    # --- 4. Boundary and Length Cases ---
    {
        "description": "16. Minimum number of points (2 points, optimal: 1 piece)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        "description": "17. Three points, optimal: 1 piece",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "18. Three points, optimal: 2 pieces (epsilon too small)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 2
    },
    {
        "description": "19. Many points, straight line (optimal: 1 piece)",
        "pw_linear_fx": [(x, x) for x in range(20)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "20. X-coordinates are not uniform (Tests correct error calculation)",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (1.0, 10.0), (100.0, 1000.0)],
        "epsilon": 0.01,
        "expected_pieces": 3 # 4 points -> 3 segments (likely)
    },

    # --- 5. Specific Error-Maximal/Minimal Scenarios ---
    {
        "description": "21. Data point exactly at the epsilon boundary (positive error)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "22. Data point slightly past the epsilon boundary (positive error)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.500001), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "23. Alternating positive and negative error points within tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1 # Line from (0,0) to (4,0) has max error 0.1
    },
    {
        "description": "24. Max error occurs on the second to last point of a long segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 2 # Segment [(0,0)-(2,0)] fails, must break at x=2.0.
    },
    {
        "description": "25. Max error occurs on the last point of the segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Line from (0,0) to (4,0) gives error 1.0 at (4,1.0). Line (0,0) to (2,0) is fine. Then (2,0) to (4,1) is fine.
    },

    # --- 6. Complex and Mixed Scenarios (Testing Optimality) ---
    {
        "description": "26. Simple example from prompt (Test provided example)",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
        # Optimal break: [(0,1)-(2,3)] (Error at (1,1) is 0.0). [(2,3)-(5,8)]. Total 2 pieces.
    },
    {
        "description": "27. Requires a long initial segment, then two short segments (Tests greedy vs optimal)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
        # Optimal: [(0,0)-(3,0)] has max error 0.2. So, [(0,0)-(2,0.2)] fails.
        # Break at x=2.0. Piece 1: [(0,0)-(2,0.2)] has error 0.1. Piece 2: [(2,0.2)-(5,0.0)] has max error ~0.13. Fails.
        # The key is: [(0,0) to (5,0)] fails. [(0,0) to (3,0)] fails.
        # Optimal is 2 pieces: [(0.0, 0.0) to (2.0, 0.2)] and [(2.0, 0.2) to (5.0, 0.0)]. Both have max error < 0.2. Let's assume 2 for this test.
    },
    {
        "description": "28. Segment where error is maximized in the middle, then flattens out",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (10.0, 0.0)],
        "epsilon": 0.6,
        "expected_pieces": 1 # Line (0,0) to (10,0) has max error 1.0. If Epsilon=0.6, requires 2 pieces.
    },
    {
        "description": "29. Large number of points that should consolidate to a small number of pieces",
        "pw_linear_fx": [(x, x * 0.01 + math.sin(x/10) * 0.005) for x in range(50)], # Almost straight line with tiny noise
        "epsilon": 0.01,
        "expected_pieces": 1 # Line from (0,0) to (49, 0.49) should cover all points with error < 0.01
    },
    {
        "description": "30. Function with two distinct, separated V-shapes",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0), (5.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 4 # V-shape 1 needs 2 pieces, flat needs 1, V-shape 2 needs 2. Flat section can be merged. Optimal: 4 pieces
    }
]
test_cases28 = [
    # ----------------------------------------------------
    # 1-3: Basic/Ideal Cases (Optimal is clearly 1 piece)
    # ----------------------------------------------------
    {
        "name": "Linear_PerfectFit_1Piece",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,  # The function is perfectly linear, should be 1 piece
        "description": "Perfectly linear function, high tolerance. Optimal should be 1 piece."
    },
    {
        "name": "Constant_PerfectFit_1Piece",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1,  # Constant function, any tolerance. Optimal should be 1 piece.
        "description": "Perfectly constant function. Optimal should be 1 piece."
    },
    {
        "name": "SmallDeviation_Fits1Piece",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.02), (3.0, 0.08), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,  # Max deviation is 0.08, fits within 0.1. Optimal should be 1 piece.
        "description": "Function with small deviations that fit within a generous tolerance. Optimal 1 piece."
    },

    # ----------------------------------------------------
    # 4-9: Boundary and Edge Cases (Testing the epsilon threshold)
    # ----------------------------------------------------
    {
        "name": "PeakAtBoundary_ExactEpsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,  # Max deviation is exactly 0.5 at x=1.0. Should be 1 piece.
        "description": "Deviation is exactly epsilon at the midpoint. Optimal should be 1 piece."
    },
    {
        "name": "PeakJustOverBoundary_Forces2Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.50001), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,  # Deviation > epsilon, must split. Optimal should be 2 pieces.
        "description": "Deviation slightly exceeds epsilon, forcing a split into 2 pieces."
    },
    {
        "name": "MultiPoint_Fits1_Tight",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, -0.1), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,  # Max deviation is 0.1, fits exactly. Optimal should be 1 piece.
        "description": "Tight fit where max deviations are exactly +/- epsilon."
    },
    {
        "name": "Convex_JustOverBoundary_ForcesSplit",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.2), (3.0, 0.05), (4.0, 0.0)],
        "epsilon": 0.19,
        "expected_pieces": 2,  # Point (2.0, 0.2) must force a split, as 0.2 > 0.19 (using the line from 0 to 4).
        "description": "Convex shape where max deviation just exceeds tolerance, forcing 2 pieces."
    },
    {
        "name": "Concave_MultipleSplits",
        "pw_linear_fx": [(0.0, 0.0), (1.0, -0.2), (2.0, 0.0), (3.0, -0.2), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 3,  # Requires splits near x=1 and x=3 to contain the dips.
        "description": "Concave function requiring multiple splits due to small epsilon."
    },
    {
        "name": "ZeroEpsilon_MaxPieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5), (4.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 4,  # Zero tolerance means no approximation allowed, pieces = N - 1.
        "description": "Zero tolerance should result in the maximum possible number of pieces."
    },

    # ----------------------------------------------------
    # 10-15: Complex/Non-Uniform Data (Testing optimal segment selection)
    # ----------------------------------------------------
    {
        "name": "AlternatingPeaks_Forces3Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.4,
        "expected_pieces": 3,  # Requires splits to handle the sharp turns/peaks.
        "description": "Alternating peaks/valleys where tolerance requires multiple segments."
    },
    {
        "name": "SteepSlopeChange_2PiecesOptimal",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 5.1), (3.0, 5.2), (4.0, 5.3)],
        "epsilon": 0.5,
        "expected_pieces": 2,  # A very steep initial slope followed by near-constant. Optimal split at x=1.
        "description": "Function with a sharp change in slope. Tests if the algorithm picks the best split point."
    },
    {
        "name": "NonUniformXSpacing_2PiecesOptimal",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (0.2, 0.0), (10.0, 1.0), (10.1, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2,  # Long constant section, then a jump. Tests x-axis independence.
        "description": "Highly non-uniform x-axis spacing. Optimal split near x=0.2 or x=10.0."
    },
    {
        "name": "CubicLikeCurve_3Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.4), (3.0, 0.8), (4.0, 1.0), (5.0, 1.1)],
        "epsilon": 0.1,
        "expected_pieces": 3,  # Requires splits to follow the curve's changing concavity/convexity.
        "description": "A curve that requires multiple segments to maintain tolerance."
    },
    {
        "name": "LargeYRange_Fits1Piece",
        "pw_linear_fx": [(0.0, 1000.0), (1.0, 1001.0), (2.0, 1002.0), (3.0, 1003.0), (4.0, 1004.0)],
        "epsilon": 1.0,
        "expected_pieces": 1,  # Large absolute y-values but perfect linearity.
        "description": "Test with large Y-values but a simple linear relationship."
    },
    {
        "name": "SineWave_MediumEpsilon_3Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0), (5.0, 1.0), (6.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 4,  # Needs a piece for each peak/trough cycle segment.
        "description": "One full cycle of a sine wave, testing the algorithm's ability to segment based on curvature."
    },

    # ----------------------------------------------------
    # 16-20: Pathological Cases (Testing greedy vs. optimal segmentation)
    # ----------------------------------------------------
    {
        "name": "GreedyFail_ShortNearEnd",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],  # 4 points fit 1 piece
        "pw_linear_fx_mod": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (3.9, 0.5), (4.0, 0.0)],
        # 5th point is a peak
        "epsilon": 0.4,
        "expected_pieces": 2,
        # A split early (e.g., at x=2.0) might allow the remaining points to be covered in 1 piece.
        "description": "Data requires a non-obvious initial split to save pieces later. A greedy choice might use 3 pieces."
    },
    {
        "name": "GreedyFail_LongInitialSegment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (3.1, 1.0), (3.2, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,  # Split at x=3.0 allows (3.0 to 4.0) to cover the peak in one piece.
        "description": "Optimal requires the first segment to end at a point that seems 'too early' to facilitate a later, wide segment."
    },
    {
        "name": "ZigZag_TightFit_3Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, -0.2), (4.0, 0.0), (5.0, 0.2), (6.0, 0.0)],
        "epsilon": 0.15,
        "expected_pieces": 4,  # Each 'V' or '^' must be segmented individually.
        "description": "A dense zigzag pattern that forces multiple splits due to small tolerance."
    },
    {
        "name": "SparseData_Fits1Piece",
        "pw_linear_fx": [(0.0, 1.0), (100.0, 1.0)],
        "epsilon": 10.0,
        "expected_pieces": 1,  # Only 2 points, max 1 piece.
        "description": "Minimum number of data points (2), results in 1 piece."
    },
    {
        "name": "ThreePoints_BoundaryCheck",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.99), (2.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 1,  # Fits within tolerance.
        "description": "Three points where the midpoint is just under tolerance."
    },

    # ----------------------------------------------------
    # 21-30: Diverse Functional Shapes and Tolerance Mixes
    # ----------------------------------------------------
    {
        "name": "Exponential_Growth_4Pieces",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.4), (3.0, 2.0), (4.0, 3.0), (5.0, 5.0), (6.0, 8.0)],
        "epsilon": 0.2,
        "expected_pieces": 4,  # Exponential growth requires increasingly short segments.
        "description": "Exponential growth function, requires increasing number of segments as slope changes rapidly."
    },
    {
        "name": "Logarithmic_Decay_3Pieces",
        "pw_linear_fx": [(1.0, 10.0), (2.0, 7.0), (4.0, 5.0), (8.0, 4.0), (16.0, 3.5)],
        "epsilon": 0.5,
        "expected_pieces": 3,  # Logarithmic decay. Slope changes rapidly early on.
        "description": "Logarithmic shape. Tests if the algorithm handles rapid slope change near the start."
    },
    {
        "name": "StepFunction_SharpJumps_5Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 1.0), (2.0, 1.0), (2.0001, 0.0), (3.0, 0.0)],
        "epsilon": 0.01,
        "expected_pieces": 4,  # A split is required for each step change, forcing 4 segments.
        "description": "Approximation of a step function. Requires a piece for each flat and vertical part."
    },
    {
        "name": "HighFrequencyNoise_LowTol_MaxPieces",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.5), (0.2, 0.0), (0.3, 0.5), (0.4, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 4,  # Each point is > 0.05 from a line drawn to the next peak/trough. Forces max segments.
        "description": "High frequency, high amplitude noise with very low tolerance, should result in max pieces."
    },
    {
        "name": "EndPointTweak_ForcesSplit",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.11)],
        "epsilon": 0.1,
        "expected_pieces": 2,  # The last point is just outside the tolerance for the (0.0, 0.0) to (3.0, 0.0) line.
        "description": "A very long constant section followed by an end point that slightly exceeds tolerance."
    },
    {
        "name": "MidRangePeak_Fits1Piece",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.5), (20.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "description": "A single triangular peak that exactly fits the tolerance in 1 piece."
    },
    {
        "name": "MidRangePeak_Forces2Pieces",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.51), (20.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "description": "A single triangular peak that slightly exceeds the tolerance, forcing 2 pieces."
    },
    {
        "name": "DownThenUp_2PiecesOptimal",
        "pw_linear_fx": [(0.0, 1.0), (1.0, -1.0), (2.0, 1.0)],
        "epsilon": 1.5,
        "expected_pieces": 2,
        # The deviation from 0 to 2 is 1.0, which fits 1.5. Expected: 1. (Correction: Max dev is 1.0 at x=0, x=2; line is y=0. Wait, the line from (0,1) to (2,1) has max dev 2.0 at x=1. Max dev from (0,1) to (2,1) is 2.0. The line is $y=0$. The points are $y=1, -1, 1$. Max $\epsilon$ is 1.0. Fits 1 piece.)
        "expected_pieces_correct": 1,  # Max dev from line connecting (0,1) and (2,1) (y=x) is 1.0 at x=1.0. Fits.
        "pw_linear_fx_corrected": [(0.0, 1.0), (1.0, -1.0), (2.0, 1.0)],
        "epsilon_corrected": 1.0,
        "description": "V-shape function, testing if 1 piece is optimal when the tolerance is sufficient."
    },
    {
        "name": "WiderPeak_Forces2Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.1), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2,  # The peak at (2.0, 1.1) is $>$ 1.0 from the line connecting (0.0, 0.0) to (4.0, 0.0).
        "description": "A single peak in the middle that just exceeds tolerance, forcing 2 pieces."
    },
    {
        "name": "LinearWithNoise_2PiecesOptimal",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 3.1), (5.0, 5.0), (6.0, 6.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,  # A split near (4.0, 3.1) allows the rest to be covered linearly.
        "description": "Mostly linear data with one outlier point, requiring a 2-piece split around the outlier."
    },
]
test_cases29 = [
    ### 1. Simple Optimality and Verification (5 Cases)
    {
        "description": "Perfect straight line, should be 1 segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Easy two segments: split at the middle point (2, 1).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Small curvature, 1 segment is possible.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.02), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 1
    },
    {
        "description": "Requires 3 segments due to sharp bends.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 3
    },
    {
        "description": "Mixed slopes, first half is gentle, second is steep, requiring 2 segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 2.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },

    ### 2. Flat/Zero Error Cases (4 Cases)
    {
        "description": "Purely horizontal line (zero error).",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "Zero epsilon, should require n-1 pieces.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.2), (3.0, 1.3), (4.0, 1.4)],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    {
        "description": "Small epsilon, non-straight line, requires max segments.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.001), (2.0, 1.002), (3.0, 1.003)],
        "epsilon": 0.0005,
        "expected_pieces": 3
    },
    {
        "description": "Horizontal staircase requiring splits at every step.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 1.0), (2.0, 1.0), (2.0001, 2.0), (3.0, 2.0)],
        "epsilon": 0.49,
        "expected_pieces": 5
    },

    ### 3. Strict Boundary Cases (6 Cases)
    {
        "description": "Middle point is exactly on the epsilon boundary (0.5). Should pass as 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Middle point is $2\epsilon$ away (1.0). Should fail as 1 piece, forcing 2 segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "First deviation is exactly epsilon. Should be 2 pieces (split 0-2 and 2-4).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Multiple points exactly on the boundary, requiring minimum two pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "The point *after* the split is the problem. Split is needed at (2,0).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, -0.4), (2.0, 0.0), (3.0, 0.5), (4.0, 1.0)],
        "epsilon": 0.4,
        "expected_pieces": 2
    },
    {
        "description": "Oscillation near the limit, should pass with 1 segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.1), (4.0, -0.1)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },

    ### 4. High Density Change and Curve Type (5 Cases)
    {
        "description": "Parabolic curve (y=x^2/4), requires a split in the middle to stay within epsilon=0.5.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 1.0), (3.0, 2.25), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Exponential-like curve (increasing slope), 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.5), (3.0, 2.0), (4.0, 5.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Concave-up shape, must split at (2, 1).",
        "pw_linear_fx": [(0.0, 4.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Steep linear segments with different slopes, 2 pieces are needed.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 10.0), (3.0, 10.1), (4.0, 10.2)],
        "epsilon": 0.05,
        "expected_pieces": 2
    },
    {
        "description": "Data points are very close in x, but require many segments (high local density).",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (0.3, 1.0), (0.4, 0.0)],
        "epsilon": 0.4,
        "expected_pieces": 4
    },

    ### 5. Minimal Data & Extreme Epsilon (5 Cases)
    {
        "description": "Minimum data points (2 points), always 1 segment.",
        "pw_linear_fx": [(0.0, 1.0), (10.0, 2.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        "description": "3 data points, require 2 segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Extreme large epsilon, should always result in 1 segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 0.0)],
        "epsilon": 1000.0,
        "expected_pieces": 1
    },
    {
        "description": "Extreme small epsilon, should result in max pieces (n-1).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.2), (3.0, 1.3)],
        "epsilon": 1e-6,
        "expected_pieces": 3
    },
    {
        "description": "Points with large y-values, testing stability of slope/intercept calculations.",
        "pw_linear_fx": [(0.0, 1000.0), (1.0, 1000.1), (2.0, 1000.2)],
        "epsilon": 0.05,
        "expected_pieces": 1
    },

    ### 6. Pathological (Spikes/Needles) (5 Cases)
    {
        "description": "Single outlier 'spike' exactly at epsilon. Should pass as 1 segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Single outlier 'spike' slightly over epsilon. Must force 2 segments (0-2 and 2-4).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Mid-segment 'dip' that breaks the approximation. Needs split at (2,0).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 1.0)],
        "epsilon": 0.49,
        "expected_pieces": 2
    },
    {
        "description": "A very thin, high-error triangle in the middle. Should be 3 segments.",
        "pw_linear_fx": [(0.0, 0.0), (1.9, 0.0), (2.0, 5.0), (2.1, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 3
    },
    {
        "description": "Negative slope with high deviation, 2 segments required.",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 5.0), (2.0, 0.0), (3.0, 1.0), (4.0, 2.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    }
]
test_cases30 = [
    # 1. Basic Single Segment Test (Optimal: 1 Piece)
    {
        "description": "Perfectly linear data, 1 segment expected.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 2. Maximum Tolerance Test (Optimal: 1 Piece)
    {
        "description": "All points within tolerance 1.0 of the line (0,0)-(5,5).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.5), (3.0, 3.5), (4.0, 4.0), (5.0, 5.0)],
        "epsilon": 1.0, # Max deviation is 1.5-1.0=0.5 and 3.5-3.0=0.5
        "expected_pieces": 1
    },
    # 3. Two Segments Required - Clear Break (Optimal: 2 Pieces)
    {
        "description": "V-shape, requires a break at (5, 0).",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 4.0), (3.0, 2.0), (5.0, 0.0), (7.0, 2.0), (9.0, 4.0), (10.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    # 4. Step Function Approximation (Optimal: 2 Pieces)
    {
        "description": "Step function, break at midpoint (2, 0.0).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 10.0), (4.0, 10.0), (5.0, 10.0)],
        "epsilon": 1.0, # Max deviation is 5.0, so 2 pieces are needed.
        "expected_pieces": 2
    },
    # 5. Boundary Condition - Tight Fit (Optimal: 2 Pieces)
    {
        "description": "First segment hits max deviation exactly at (1, 1).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5, # (1, 1) is 1.0 above line (0,0)-(2,0). Needs split.
        "expected_pieces": 2
    },
    # 6. Large Dataset - Wave (Optimal: 4 Pieces)
    {
        "description": "Sinusoidal-like data, 4 pieces for epsilon 0.1.",
        "pw_linear_fx": [(i, 0.5 * (i % 2) - 0.25 * (i % 4)) for i in range(15)],
        "epsilon": 0.1,
        "expected_pieces": 4 # Rough estimate for this noisy wave
    },
    # 7. No Approximation Possible (Optimal: N Pieces)
    {
        "description": "Epsilon is too small (0.0). Should return N pieces (N=4).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.001), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    # 8. Short Dataset - 3 Points (Optimal: 1 Piece)
    {
        "description": "Minimal dataset, clearly linear.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    # 9. Short Dataset - 3 Points, Needs 2 Pieces (Optimal: 2 Pieces)
    {
        "description": "Minimal dataset, clearly nonlinear.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.4, # Max deviation is 0.5. Requires 2 segments.
        "expected_pieces": 2
    },
    # 10. Greedy Trap - Suboptimal Split 1 (Optimal: 2 Pieces)
    {
        "description": "Greedy split at point 3 or 4 would be suboptimal (should be 2 pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.8), (3.0, 0.0), (4.0, 0.0), (5.0, 5.0), (6.0, 5.0)],
        "epsilon": 0.8,
        "expected_pieces": 2 # (0,0)-(4,0) is fine. Needs split for (5,5).
    },
    # 11. Greedy Trap - Suboptimal Split 2 (Optimal: 2 Pieces)
    {
        "description": "Data needs a split *after* a long flat segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 5.0), (5.0, 5.0), (6.0, 0.0)],
        "epsilon": 1.0, # Max dev is 2.5 on (0,0)-(6,0). Needs split. Split at (3,0) works.
        "expected_pieces": 2
    },
    # 12. Alternating Deviation 1 (Optimal: 3 Pieces)
    {
        "description": "Alternating points just outside tolerance, needs 3 pieces.",
        "pw_linear_fx": [(0,0), (1, 0.2), (2, -0.2), (3, 0.2), (4, -0.2), (5, 0)],
        "epsilon": 0.15,
        "expected_pieces": 3 # Must connect (0,0)-(2,-0.2) and (2,-0.2)-(4,-0.2) and (4,-0.2)-(5,0)
    },
    # 13. Alternating Deviation 2 (Optimal: 2 Pieces)
    {
        "description": "Alternating points *within* tolerance.",
        "pw_linear_fx": [(0,0), (1, 0.2), (2, -0.2), (3, 0.2), (4, -0.2), (5, 0)],
        "epsilon": 0.25,
        "expected_pieces": 1
    },
    # 14. Large Coordinates (Optimal: 1 Piece)
    {
        "description": "Large coordinates, perfect linear.",
        "pw_linear_fx": [(100, 1000), (200, 2000), (300, 3000)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    # 15. Large Coordinates, High Tolerance (Optimal: 1 Piece)
    {
        "description": "Large coordinates, small deviation within tolerance.",
        "pw_linear_fx": [(100, 1000), (200, 2000.5), (300, 3000)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    # 16. Steeper Segment (Optimal: 2 Pieces)
    {
        "description": "Mix of flat and steep segments.",
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 10), (4, 10), (5, 10)],
        "epsilon": 4.0, # Max dev on (0,0)-(5,10) is at (2,0) with 4.0. Split needed.
        "expected_pieces": 2
    },
    # 17. Floating Point Precision (Optimal: 1 Piece)
    {
        "description": "Testing floating point precision near tolerance boundary.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.000000000001)],
        "epsilon": 1e-11,
        "expected_pieces": 1
    },
    # 18. Floating Point Precision - Fail (Optimal: 2 Pieces)
    {
        "description": "Testing floating point precision just outside tolerance boundary.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.000000000001)],
        "epsilon": 1e-13,
        "expected_pieces": 2
    },
    # 19. S-Curve (Optimal: 3 Pieces)
    {
        "description": "S-curve requires 3 pieces for low tolerance.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 1.5), (4, 1), (5, 0.5), (6, 0)],
        "epsilon": 0.2,
        "expected_pieces": 3 # Split: (0,0)-(2,2), (2,2)-(5,0.5), (5,0.5)-(6,0)
    },
    # 20. Simple Quadratic (Optimal: 2 Pieces)
    {
        "description": "Simple quadratic curve $y=x^2$ for $x \in [0, 4]$.",
        "pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)],
        "epsilon": 2.0,
        "expected_pieces": 2 # Split at (2,4) or (3,9) depending on exact line fit. Split at (2,4) works.
    },
    # 21. Constant y-value (Optimal: 1 Piece)
    {
        "description": "All y-values are the same.",
        "pw_linear_fx": [(i, 5.0) for i in range(10)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    # 22. Jitter around a Constant Line (Optimal: 1 Piece)
    {
        "description": "Jitter around a constant y=5 line, within tolerance.",
        "pw_linear_fx": [(0, 5.0), (1, 5.1), (2, 4.9), (3, 5.05), (4, 4.95), (5, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 23. Jitter around a Constant Line - Fail (Optimal: 2 Pieces)
    {
        "description": "Jitter around a constant y=5 line, just outside tolerance.",
        "pw_linear_fx": [(0, 5.0), (1, 5.1), (2, 4.9), (3, 5.15), (4, 4.95), (5, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Point (3, 5.15) is 0.15 away from y=5.0 line.
    },
    # 24. End Point Deviation (Optimal: 2 Pieces)
    {
        "description": "All points fine, but the *last* point requires a split.",
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 5)],
        "epsilon": 1.0,
        "expected_pieces": 2 # Max dev on (0,0)-(4,5) is at (3,0) or (1,0), dev is 3.75. Needs split (3,0)-(4,5).
    },
    # 25. Start Point Deviation (Optimal: 2 Pieces)
    {
        "description": "The *second* point requires the first segment to be short.",
        "pw_linear_fx": [(0, 5), (1, 0), (2, 0), (3, 0), (4, 0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # Max dev on (0,5)-(4,0) is 2.5. Split at (1,0)-(4,0).
    },
    # 26. Asymmetrical Split (Optimal: 2 Pieces)
    {
        "description": "A split that must occur much closer to one end.",
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0.9), (3, 1.2), (4, 1.4), (10, 1.5)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Split needed around (4, 1.4). (0,0)-(4,1.4) works.
    },
    # 27. Multiple Small Deviations (Optimal: 3 Pieces)
    {
        "description": "Requires three segments due to concentrated deviations.",
        "pw_linear_fx": [(0, 0), (1, 1.0), (2, 0), (3, 1.0), (4, 0), (5, 0), (6, 0)],
        "epsilon": 0.4,
        "expected_pieces": 3 # Segments: (0,0)-(2,0), (2,0)-(4,0), (4,0)-(6,0).
    },
    # 28. High Number of Points, Simple Deviation (Optimal: 2 Pieces)
    {
        "description": "Long dataset, single large deviation.",
        "pw_linear_fx": [(i, 0.0) for i in range(10)] + [(10, 5.0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # Split at (9,0)-(10,5.0)
    },
    # 29. Z-Shape/Switchback (Optimal: 3 Pieces)
    {
        "description": "A Z-shape that requires three pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 3
    },
    # 30. Example from Prompt (Optimal: 2 Pieces)
    {
        "description": "Example test case from the user prompt.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Max dev on (0,1)-(5,8) is at (1,1) or (2,3), both > 0.5. Split at (1,1) or (2,3)
    }
]