#24 Nov 4:10 PM --> asking llm to generate 20 testcases x 30 times = 600 test cases
#with Gemini 3 Fast model - few shot prompt
test_cases1 = [
    # 1. Base Case: Perfectly Linear (Expected: 1 segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1
    },

    # 2. Perfect Line, Large Epsilon (Expected: 1 segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0)],
        "epsilon": 5.0
    },

    # 3. Barely Needs 2 Segments (One point exceeds epsilon by a tiny amount)
    # Max deviation for a single line (0,0) to (2,0) is 0.001 at x=1.
    # If epsilon is 0.0009, it should fail and require 2 segments.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.001), (2.0, 0.0)],
        "epsilon": 0.0009
    },

    # 4. Barely Needs 1 Segment (One point is *exactly* at epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5
    },

    # 5. V-Shape: Requires 2 segments regardless of epsilon (for small epsilon)
    {
        "pw_linear_fx": [(0.0, 10.0), (1.0, 0.0), (2.0, 10.0)],
        "epsilon": 1.0
    },

    # 6. Step Function Approximation (Requires 2 segments minimum)
    # The max deviation for a single line from (0,0) to (2,1) is 0.5 at x=0, 1, 2.
    # The data point (1, 1) is 1.0 away from the best fit line (y=0.5).
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.49
    },

    # 7. Rapid Oscillation (Requires many segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1
    },

    # 8. Quadratic Curve (y = x^2, testing uniform curvature)
    # Max error for 1 segment (0,0) to (4,16) is 1.0 at x=2.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.99
    },

    # 9. Small $\varepsilon$ and many points (Forces many segments)
    {
        "pw_linear_fx": [(x, x**2) for x in range(10)],
        "epsilon": 0.05
    },

    # 10. Large $\varepsilon$ (Should result in 1 segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 50.0
    },

    # 11. End-point Tolerance Check 1 (Point exactly at the boundary of 1 segment fit)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 0.0)],
        "epsilon": 0.25 # Best fit line is y=0. Max deviation is 0.25 at x=0.5.
    },

    # 12. End-point Tolerance Check 2 (Point slightly over the boundary, requires 2 segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.501), (1.0, 0.0)],
        "epsilon": 0.25
    },

    # 13. Horizontal line with one outlier (Easy 2 segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.1
    },

    # 14. Non-Uniform X-Spacing (Tests for reliance on x-axis distance)
    # The point (10, 5) makes the line (0,0) to (100,0) fail significantly.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (10.0, 5.0), (100.0, 0.0)],
        "epsilon": 0.5
    },

    # 15. Negative Slope/Y-values
    {
        "pw_linear_fx": [(0.0, -1.0), (1.0, -2.0), (2.0, -1.0)],
        "epsilon": 0.49
    },

    # 16. Case with three segments minimum (e.g., a "W" shape)
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 2.0)],
        "epsilon": 0.1
    },

    # 17. The *Example* Case from the prompt (Needs at least 2 segments)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },

    # 18. Zero Epsilon (Should require N-1 segments if any points are not perfectly collinear)
    # The first three points are collinear. The last point (3,3.001) breaks the collinearity.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.001)],
        "epsilon": 0.0
    },

    # 19. Repeated Points (Tests for handling of redundant data)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0
    },

    # 20. Long Run with small, persistent deviation (Optimal strategy is critical)
    # y = sin(x) style deviation, but with linear segments.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0), (5.0, 0.1), (6.0, 0.0)],
        "epsilon": 0.04
    }
]
test_cases2 = [
    # 1. Basic Linear: Should require 1 piece if endpoints are used.
    {
        "name": "Single Linear Segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "notes": "A truly linear set of points, should be covered by 1 piece."
    },
    # 2. Constant Function: Should require 1 piece, testing y-range.
    {
        "name": "Constant Function",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.001,
        "expected_min_pieces": 1,
        "notes": "All points are co-linear and horizontal."
    },
    # 3. Simple Curve (Parabola): Requires 2 pieces for small epsilon.
    {
        "name": "Parabolic Curve, Small Epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 2.0), (3.0, 4.5)],
        "epsilon": 0.01,
        "expected_min_pieces": 2, # E.g., (0,0) to (2,2) will exceed tolerance.
        "notes": "A curve that requires multiple segments."
    },
    # 4. Same Curve, Large Epsilon: Should require 1 piece.
    {
        "name": "Parabolic Curve, Large Epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 2.0), (3.0, 4.5)],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "notes": "Tolerance is large enough to cover the entire curve with one line."
    },
    # 5. Sawtooth Pattern (Boundary): Tests alternating error signs.
    {
        "name": "Sawtooth Pattern, Points at Epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "notes": "Mid-points are exactly on the line segment, testing L_inf boundary."
    },
    # 6. Sawtooth Pattern (Exceeds): Forces multiple pieces.
    {
        "name": "Sawtooth Pattern, Exceeds Epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0), (3.0, 0.51), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3, # Requires segments (0,0)-(2,0) and (2,0)-(4,0) if done greedily, but optimally (0,0)-(2,0), (2,0)-(4,0)
        "notes": "The points are just outside the tolerance, forcing 3 pieces (e.g., 0-1, 1-2, 2-3, 3-4 is 4, 0-2 and 2-4 is 2. The max deviation for 0-4 is 0.51, so it needs at least 2 pieces). Optimal should be 2: (0,0)-(2,0) and (2,0)-(4,0)."
    },
    # 7. Step Function Approximation: Tests algorithm on abrupt changes.
    {
        "name": "Step Function",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "notes": "The jump from 1.0 to 5.0 must be covered, likely requiring two pieces."
    },
    # 8. Large Data Set, Simple Linear: Performance and single piece check.
    {
        "name": "Large Set, Single Piece Expected",
        "pw_linear_fx": [(i, float(i)) for i in range(100)],
        "epsilon": 0.001,
        "expected_min_pieces": 1,
        "notes": "100 co-linear points to check performance and single-piece handling."
    },
    # 9. Minimal Data Set (3 points, 2 segments): Basic check.
    {
        "name": "Minimal 3 Points",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.4,
        "expected_min_pieces": 1,
        "notes": "Simple V-shape covered by one line (error = 0.5 > 0.4, wait, error is 0.5 if line is 0,0 to 2,0. If line is 0,0 to 2,0, error is 0.5. Needs 2 pieces for 0.4. Let's make error 0.3 for 1 piece)."
    },
    # 10. Minimal Data Set (3 points, force 2 pieces).
    {
        "name": "Minimal 3 Points, Forces 2 Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.2,
        "expected_min_pieces": 2,
        "notes": "V-shape with tight tolerance, forces 2 pieces."
    },
    # 11. Edge Case: Data points already define the minimum pieces (no simplification possible).
    {
        "name": "No Simplification Possible",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3,
        "notes": "Extreme alternating values with low epsilon. Must use all segments."
    },
    # 12. Floating Point Precision Test: Epsilon exactly matching max error.
    {
        "name": "Precision Boundary Test",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 0.0)],
        "epsilon": 0.25,
        "expected_min_pieces": 1,
        "notes": "Max error is exactly epsilon, should pass with 1 piece."
    },
    # 13. Floating Point Precision Test: Epsilon slightly less than max error.
    {
        "name": "Precision Failure Test",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 0.0)],
        "epsilon": 0.249999,
        "expected_min_pieces": 2,
        "notes": "Max error is slightly above epsilon, must fail with 2 pieces."
    },
    # 14. Non-uniform X-spacing: Checks correct use of linear interpolation.
    {
        "name": "Non-Uniform X-Spacing",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (10.0, 0.0)],
        "epsilon": 0.001,
        "expected_min_pieces": 1,
        "notes": "Tests x-coordinates handling in interpolation."
    },
    # 15. Negative Y-values: Checks L-infinity calculation with negative error.
    {
        "name": "Negative Y-Values",
        "pw_linear_fx": [(0.0, -1.0), (1.0, -0.5), (2.0, -1.0)],
        "epsilon": 0.4,
        "expected_min_pieces": 1,
        "notes": "V-shape below the x-axis. Max error is 0.5."
    },
    # 16. Combined Slope and Curve: Tests ability to transition.
    {
        "name": "Slope then Curve",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.5), (4.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3, # (0,0) to (1,1) is needed, (1,1) to (2,1) is 1 piece, (2,1) to (4,3) needs another piece.
        "notes": "Linear section followed by a curved section."
    },
    # 17. Extreme Jitter: Tests if the algorithm incorrectly merges highly erratic data.
    {
        "name": "Extreme Jitter (High Frequency)",
        "pw_linear_fx": [(i, 1.0 if i % 2 == 0 else -1.0) for i in range(10)],
        "epsilon": 0.5,
        "expected_min_pieces": 9,
        "notes": "Alternating points 1.0 and -1.0. Error for one segment is always 1.0, greater than epsilon 0.5."
    },
    # 18. Only Two Points: The simplest case.
    {
        "name": "Only Two Points",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0)],
        "epsilon": 100.0,
        "expected_min_pieces": 1,
        "notes": "Minimal data set, always 1 piece."
    },
    # 19. Large Range of Y: Checks scaling impact.
    {
        "name": "Large Y Range",
        "pw_linear_fx": [(0.0, 1000.0), (1.0, 1000.5), (2.0, 1000.0)],
        "epsilon": 0.49,
        "expected_min_pieces": 2,
        "notes": "Max error 0.5, needs 2 pieces for epsilon 0.49."
    },
    # 20. Linear, but with one point slightly exceeding tolerance in the middle.
    {
        "name": "Forced 2 Pieces via Middle Point",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.501), (2.0, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "notes": "The middle point (1.0, 0.501) is 0.001 above the line from (0,0) to (2,1), forcing two pieces (0-1 and 1-2)."
    },
]
test_cases3 = [
    # 1. Simple Constant Function (Optimal: 1 Piece)
    # Expected: 1 piece. Error is 0.
    {"pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.1, "expected_pieces": 1},

    # 2. Linear Function (Optimal: 1 Piece)
    # Expected: 1 piece. Error is 0.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 1e-6,
     "expected_pieces": 1},

    # 3. Concave Function - Needs 2 Pieces (Exactly Fails 1 Piece)
    # The point (1.0, 0.5) is exactly 0.5 away from the line segment between (0,0) and (2,0).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces": 2},

    # 4. Concave Function - Passes 1 Piece (Tolerance allows 1 piece)
    # The point (1.0, 0.49) is less than 0.5 away from the line segment between (0,0) and (2,0).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.49), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces": 1},

    # 5. Convex Function - Exactly Fails 1 Piece
    # The point (1.0, -0.5) is exactly 0.5 away from the line segment between (0,0) and (2,0).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, -0.5), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces": 2},

    # 6. Sharp 'V' Shape - Fails 1 Piece, Needs 2
    # The point (1, 1) is 0.5 away from the line between (0, 0) and (2, 0) if it was (1, 0.5)
    # Here, (1, 1) is 1.0 away from the line between (0, 0) and (2, 0), so it fails tolerance 0.9.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.9, "expected_pieces": 2},

    # 7. Steep Step Function - Requires 2 Pieces (Minimal x-distance)
    # A single segment between (0,0) and (0.1, 10) is too far from (0.05, 0.0).
    {"pw_linear_fx": [(0.0, 0.0), (0.05, 0.0), (0.1, 10.0)], "epsilon": 0.1, "expected_pieces": 2},

    # 8. Very Gentle Curve - Easily 1 Piece (High tolerance)
    # The max error is small for a gentle slope.
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 0.1), (20.0, 0.2), (30.0, 0.3)], "epsilon": 0.5, "expected_pieces": 1},

    # 9. Multiple Oscillations (Min Max Test)
    # Forces the algorithm to correctly identify the maximum deviation point.
    {"pw_linear_fx": [(0, 0), (0.5, 0.4), (1, 0.0), (1.5, -0.4), (2, 0.0)], "epsilon": 0.39, "expected_pieces": 3},
    # Fails at 0.4 and -0.4.

    # 10. Boundary Case: First Point Deviation
    # The point (1.0, 0.0) is the first point that deviates from the line (0,0) to (5,0).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.5), (5.0, 0.0)], "epsilon": 0.5, "expected_pieces": 2},

    # 11. Boundary Case: Last Point Deviation
    # The point (4.0, 0.5) is the last point that deviates before the end-point (5,0).
    {"pw_linear_fx": [(0.0, 0.0), (3.0, 0.0), (4.0, 0.5), (5.0, 0.0)], "epsilon": 0.49, "expected_pieces": 3},
    # Requires a new segment starting at (3,0)

    # 12. Boundary Case: Small $\varepsilon$ on a Linear Function (Test floating point stability)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)], "epsilon": 1e-10, "expected_pieces": 1},

    # 13. Case requiring 3 segments (W-shape)
    # Segment 1: (0,0) to (2,0) fails at (1, -1). New piece starts at (1, -1).
    # Segment 2: (1,-1) to (4,-1) fails at (3, 0). New piece starts at (3, 0).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, -1.0), (2.0, 0.0), (3.0, 0.0), (4.0, -1.0), (5.0, 0.0)], "epsilon": 0.5,
     "expected_pieces": 3},

    # 14. Non-monotonic X values (Should NOT happen based on problem statement, but robust test)
    # Assuming the algorithm handles $x_i$ non-decreasing, this still tests a high deviation.
    {"pw_linear_fx": [(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (3.0, 0.0)], "epsilon": 0.5, "expected_pieces": 2},

    # 15. Zero $\varepsilon$ (Force a segment for every data point)
    # Optimal should be $n$ pieces for $n+1$ points unless all points are already colinear.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0)], "epsilon": 0.0, "expected_pieces": 3},

    # 16. Identical consecutive points (Test handling of zero-length segments if $x$ values were the same)
    # Assuming $x$ values are distinct based on typical use, but $y$ values can be the same.
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0001), (3.0, 1.0)], "epsilon": 0.00005, "expected_pieces": 2},
    # Fails at 1.0001

    # 17. Extreme Slopes (Vertical lines are approximated by horizontal lines)
    # The max error is 5.0 (at x=1.0, y=5.0). Tolerance 4.9 should fail.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)], "epsilon": 4.9, "expected_pieces": 2},

    # 18. Boundary Case: Exactly meeting the $\varepsilon$ boundary (Should be 2 pieces)
    # The line from (0,0) to (4,0) has a max deviation at x=2. The line value is 0.
    # The deviation is |2.0 - 0.0| = 2.0.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 2.0,
     "expected_pieces": 2},

    # 19. Boundary Case: Just passing the $\varepsilon$ boundary (Should be 1 piece)
    # Max deviation is 2.0. Tolerance 2.00001 should pass.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 2.00001,
     "expected_pieces": 1},

    # 20. Large number of points requiring several pieces (Stress test)
    # A simple parabolic shape that will need multiple cuts for a tight tolerance.
    {"pw_linear_fx": [(i, i ** 2) for i in range(10)], "epsilon": 0.5, "expected_pieces": 4}
    # Example: (0,0) to (3,9) fails at (1,1) with err ~ 2.0.
]
test_cases4 = [
    # 1. Trivial Cases & Single Piece Optimality
    {
        "description": "Perfectly linear data, single piece optimal.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Perfectly constant data, single piece optimal.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (5.0, 5.0), (10.0, 5.0)],
        "epsilon": 0.05,
        "expected_pieces": 1
    },
    {
        "description": "Small deviation from linearity, single piece optimal.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Two points, always one piece optimal (minimum data).",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },

    # 2. Sharp Turns and High Curvature (V-shapes)
    {
        "description": "Sharp V-shape, requires a break at the vertex.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 0.0), (2.0, 5.0)],
        "epsilon": 0.5,
        "expected_pieces": 2  # (0,5)-(1,0) and (1,0)-(2,5)
    },
    {
        "description": "Inverted V-shape, max deviation at the center point.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "A turn followed by a linear segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 2  # (0,0)-(1,5) and (1,5)-(3,5)
    },

    # 3. Quadratic/Parabolic Data - Tests Non-Uniform Point Selection
    {
        "description": "Parabolic $y=x^2$ data, requires multiple pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 0.5,
        "expected_pieces": 2  # Optimal should be (0,0)-(2,4) or (0,0)-(1,1) + (1,1)-(3,9) depending on $L_{\infty}$
    },
    {
        "description": "Shallow parabola $y=0.1x^2$, can be approximated by one piece.",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 2.5), (10.0, 10.0)],
        "epsilon": 3.0,
        "expected_pieces": 1
    },

    # 4. Stair-Step / Vertical-like Jumps (Challenging for Greedy)
    {
        "description": "Stair-step function, forces a break after each 'step'.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.01,
        "expected_pieces": 4  # A piece for (0,0)-(1,0), (1,0)-(1,1) is vertical, (1,1)-(2,1), (2,1)-(2,2) vertical
    },
    {
        "description": "Small jump that exceeds tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (2.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2  # (0,0)-(2,0) and (2,0)-(2,1)
    },

    # 5. Sinusoidal/Oscillating Data
    {
        "description": "Sine wave over one period (approx $\sin(x)$), requires multiple pieces.",
        "pw_linear_fx": [(0, 0), (1.57, 1.0), (3.14, 0), (4.71, -1.0), (6.28, 0)],
        "epsilon": 0.1,
        "expected_pieces": 4  # Requires pieces near peaks/troughs/inflection points
    },
    {
        "description": "High frequency, low amplitude oscillation, one piece if tolerance is large.",
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, -0.1), (3, 0.1), (4, -0.1)],
        "epsilon": 0.2,
        "expected_pieces": 1
    },

    # 6. Critical Tolerance Edge Cases
    {
        "description": "Data point *exactly* on the $\epsilon$ boundary.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.5)],
        "epsilon": 0.5,
        "expected_pieces": 1  # A line from (0,0) to (3,0.5) has max deviation 0.0 for (1,0) and (2,0)
    },
    {
        "description": "A point just *over* the $\epsilon$ boundary, forcing a piece break.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.6), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2  # (0,0)-(1,0.6) and (1,0.6)-(2,0)
    },
    {
        "description": "Long, shallow data that is better approximated by 2 pieces than 1.",
        "pw_linear_fx": [(0, 0), (2, 0.6), (4, 1.0), (6, 0.6), (8, 0)],
        "epsilon": 0.1,
        "expected_pieces": 4  # Testing for optimal segment merging
    },

    # 7. Non-Uniform Spacing and Negative Coordinates
    {
        "description": "Non-uniform X-spacing with a large gap.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (10.0, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "description": "Negative coordinates included.",
        "pw_linear_fx": [(-5.0, 5.0), (0.0, 0.0), (5.0, -5.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },

    # 8. Large Datasets / High Tolerance
    {
        "description": "Many points, high tolerance allows a single piece.",
        "pw_linear_fx": [(i, i * 0.1 + (0.5 if i % 2 == 0 else 0)) for i in range(10)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Complex, forcing small pieces due to very tight tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, -0.1), (4.0, 0.0)],
        "epsilon": 0.01,
        "expected_pieces": 4  # Requires a break at every local extremum
    }
]
test_cases5 = [
    # 1. Basic Monotonic (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0), (5.0, 5.0)],
        "epsilon": 0.1
    },
    # 2. Basic Non-linear (Tight Tolerance, forces max pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.01
    },
    # 3. Step Function Approximation (Tests tolerance across a large jump)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 1.0
    },
    # 4. Zero Tolerance (Forces exact fit, max pieces unless perfectly linear)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0001)],
        "epsilon": 0.0
    },
    # 5. Infinite Tolerance (Forces 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -10.0), (3.0, 0.0)],
        "epsilon": 100.0
    },
    # 6. Critical Point at Max Deviation (Tests algorithm's boundary condition check)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.25
    },
    # 7. Multiple Points on Tolerance Boundary (Optimal 2-piece split)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 1.0
    },
    # 8. Trivial Single Segment Input (Minimum input)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.001
    },
    # 9. Small Perturbation Exceeds Tolerance (Forces a split)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.01), (3.0, 0.0)],
        "epsilon": 0.009
    },
    # 10. Small Perturbation Within Tolerance (Should not split)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.01), (3.0, 0.0)],
        "epsilon": 0.011
    },
    # 11. Concave Function (Parabola section)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.75), (3.0, 2.25), (4.0, 2.5), (5.0, 2.5)],
        "epsilon": 0.1
    },
    # 12. Convex Function
    {
        "pw_linear_fx": [(0.0, 2.5), (1.0, 2.5), (2.0, 2.25), (3.0, 1.75), (4.0, 1.0), (5.0, 0.0)],
        "epsilon": 0.1
    },
    # 13. Very Long Sequence, Max Pieces (Sawtooth)
    {
        "pw_linear_fx": [(x, 10.0 * (x % 2)) for x in range(11)],
        "epsilon": 0.5
    },
    # 14. Very Long Sequence, Minimum Pieces (Perfect Line)
    {
        "pw_linear_fx": [(x, float(x)) for x in range(11)],
        "epsilon": 1.0
    },
    # 15. Oscillating Function, Tight Split (Forces split at every peak/trough)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0), (5.0, 1.0), (6.0, 0.0)],
        "epsilon": 0.49
    },
    # 16. Oscillating Function, Loose Fit (Allows fitting two half-cycles with one piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.51
    },
    # 17. Steep Slope Change (Checks handling of near-vertical lines in approximation)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 10.0), (3.0, 0.0)],
        "epsilon": 0.001
    },
    # 18. Small Non-Zero Epsilon (Floating point stability test)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0001), (2.0, 0.0)],
        "epsilon": 1e-6
    },
    # 19. Start/End Points with Large Vertical Offset (Tests robustness against large coordinates)
    {
        "pw_linear_fx": [(0.0, 100.0), (1.0, 100.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.001
    },
    # 20. Mixed Linear and Non-Linear Sections (Tests ability to efficiently skip the linear parts)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 2.0), (4.0, 2.0), (5.0, 3.0)],
        "epsilon": 0.1
    }
]
test_cases6 = [
    # 1. Base Case: Perfectly Linear Data (Should require 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_optimal_pieces": 1
    },
    # 2. Perfect Fit at epsilon limit: Flat line where one point is just off by epsilon/2
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_optimal_pieces": 1
    },
    # 3. Two-Piece Requirement: V-Shape function with sharp corner exceeding tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.4,
        "expected_optimal_pieces": 2 # Point (1.0, 1.0) is 0.5 away from the line (0,0) to (2,0), which exceeds 0.4
    },
    # 4. Single-Piece Requirement: V-Shape function where tolerance is *just* met
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.51,
        "expected_optimal_pieces": 1 # Max error (0.5) is less than 0.51
    },
    # 5. Stair-step function (Non-monotonic $y$ values) - Zero tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0,
        "expected_optimal_pieces": 4 # Requires perfect fit (N points -> N-1 segments/pieces)
    },
    # 6. Smooth Curve (Parabola): Testing multiple pieces on a curve
    {
        "pw_linear_fx": [(x, x**2) for x in [0.0, 0.5, 1.0, 1.5, 2.0]],
        "epsilon": 0.1,
        "expected_optimal_pieces": 2 # (0,0) to (1.0, 1.0) max error is 0.25. (1.0, 1.0) to (2.0, 4.0) max error is 0.25. Need to split at (1.0, 1.0).
    },
    # 7. Constant Oscillation/Sawtooth: Requires many small pieces due to tight $\epsilon$
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
        "epsilon": 0.49,
        "expected_optimal_pieces": 4 # Error is 0.5 in each 2-unit segment.
    },
    # 8. Wide Peak: Error exactly equals $\epsilon$
    {
        "pw_linear_fx": [(x, 0.5 * (1 - (x-2)**2)) for x in [0.0, 1.0, 2.0, 3.0, 4.0]],
        "epsilon": 0.5,
        "expected_optimal_pieces": 1 # Max deviation for (0,0) to (4,0) is 0.5 (at x=2, y=2.0).
    },
    # 9. Wide Peak: Error just exceeds $\epsilon$
    {
        "pw_linear_fx": [(x, 0.51 * (1 - (x-2)**2)) for x in [0.0, 1.0, 2.0, 3.0, 4.0]],
        "epsilon": 0.5,
        "expected_optimal_pieces": 2 # Max deviation is 0.51, just exceeding the tolerance.
    },
    # 10. High-Frequency Low-Amplitude Noise: Single piece allowed
    {
        "pw_linear_fx": [(i, 0.0 if i % 2 == 0 else 0.05) for i in range(10)],
        "epsilon": 0.1,
        "expected_optimal_pieces": 1 # All points are within 0.05 of the line y=0.0.
    },
    # 11. High-Frequency Low-Amplitude Noise (Just Misses): Forces minimal segments
    {
        "pw_linear_fx": [(i, 0.0 if i % 2 == 0 else 0.051) for i in range(10)],
        "epsilon": 0.05,
        "expected_optimal_pieces": 9 # Max error is 0.051. Requires a piece for almost every segment.
    },
    # 12. Asymmetric Data: Point near the start dictates the split
    {
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0.0), (10, 0.0)],
        "epsilon": 0.4,
        "expected_optimal_pieces": 2 # (0,0) to (10,0) has error 0.5. Optimal split is at (1, 0.5).
    },
    # 13. Short, Steep Segment followed by a long, flat one
    {
        "pw_linear_fx": [(0, 0), (1, 5.0), (2, 5.0), (10, 5.0)],
        "epsilon": 1.0,
        "expected_optimal_pieces": 2 # (0,0) to (10, 5) has max error 4.5 at (1, 5.0). Needs split: (0,0) to (1, 5.0) and (1, 5.0) to (10, 5.0).
    },
    # 14. Long, Flat Data (Testing $x$ range and precision)
    {
        "pw_linear_fx": [(i * 10.0, 5.0) for i in range(5)],
        "epsilon": 1e-6,
        "expected_optimal_pieces": 1
    },
    # 15. Minimal Points (Edge case n=2)
    {
        "pw_linear_fx": [(1.0, 1.0), (2.0, 2.0)],
        "epsilon": 10.0,
        "expected_optimal_pieces": 1
    },
    # 16. Zero Tolerance (Requires piece for every segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.0,
        "expected_optimal_pieces": 3
    },
    # 17. Extreme Tolerance (Always 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 5.0,
        "expected_optimal_pieces": 1
    },
    # 18. Concave-Convex Mixture (S-Curve)
    {
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.5), (3, 0.9), (4, 1.0)],
        "epsilon": 0.1,
        "expected_optimal_pieces": 2 # (0,0) to (4,1) has max error 0.25 at (2, 0.5).
    },
    # 19. Steep initial deviation
    {
        "pw_linear_fx": [(0, 0), (0.5, 2.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.5,
        "expected_optimal_pieces": 2 # (0,0) to (2.0, 2.0) has max error 1.0 at (0.5, 2.0). Needs split at (0.5, 2.0).
    },
    # 20. Simple Case: One point outside tolerance at the end
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.5)],
        "epsilon": 0.1,
        "expected_optimal_pieces": 2 # (0,0) to (3, 0.5) has max error 0.5. Optimal: (0,0) to (2,0) and (2,0) to (3, 0.5).
    }
]
test_cases7 = [
    # 1. Base Case: Perfectly Linear Data (Should always be 1 piece)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.1,
        'expected_optimal_pieces': 1
    },
    # 2. Perfect Fit with Large Epsilon (Should always be 1 piece)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        'epsilon': 2.0,
        'expected_optimal_pieces': 1
    },
    # 3. Sawtooth/V-Shape (Requires 2 pieces for small epsilon)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        'epsilon': 0.5,
        'expected_optimal_pieces': 2
    },
    # 4. Step Function (Requires multiple pieces)
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (1.0001, 3.0), (2.0, 3.0)],
        'epsilon': 0.5,
        'expected_optimal_pieces': 2
    },
    # 5. Quadratic Curve (Increasing curvature requires more pieces)
    {
        'pw_linear_fx': [(x, x**2) for x in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]],
        'epsilon': 0.5,
        'expected_optimal_pieces': 3  # (0,1,2) -> 1, (2,3,4) -> 1, (4,5) -> 1 (approx)
    },
    # 6. Epsilon exactly met by one point (Boundary condition)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        'epsilon': 0.5,
        'expected_optimal_pieces': 1
    },
    # 7. Epsilon slightly exceeded by one point (Should force 2 pieces)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.50001), (2.0, 0.0)],
        'epsilon': 0.5,
        'expected_optimal_pieces': 2
    },
    # 8. Highly Oscillatory Data (Sine wave-like, forcing many pieces)
    {
        'pw_linear_fx': [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, -1.0), (2.0, 0.0)],
        'epsilon': 0.2,
        'expected_optimal_pieces': 4
    },
    # 9. Single Large Spike (Splits data into 3 easy segments)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0001, 10.0), (2.0, 0.0), (3.0, 0.0)],
        'epsilon': 0.5,
        'expected_optimal_pieces': 3
    },
    # 10. Non-Uniform X-Spacing and Y-Change (Ensures reliance on error, not indices)
    {
        'pw_linear_fx': [(0.0, 0.0), (0.1, 0.5), (10.0, 0.5), (10.1, 0.0)],
        'epsilon': 0.1,
        'expected_optimal_pieces': 3
    },
    # 11. Long, Flat, then Sharp Turn (Tests segment termination/start)
    {
        'pw_linear_fx': [(i, 0.0) for i in range(5)] + [(5.0, 5.0)],
        'epsilon': 0.01,
        'expected_optimal_pieces': 2
    },
    # 12. Minimal Data Points (Only 2 points, must be 1 piece)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0)],
        'epsilon': 100.0,
        'expected_optimal_pieces': 1
    },
    # 13. All Points Identical Y-value (Horizontal line, 1 piece)
    {
        'pw_linear_fx': [(i, 5.0) for i in range(10)],
        'epsilon': 0.0001,
        'expected_optimal_pieces': 1
    },
    # 14. Zero Epsilon (Forces $N-1$ pieces, where $N$ is number of points)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.0,
        'expected_optimal_pieces': 3
    },
    # 15. Linear with Noise (Checks robustness against small deviations)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.0)],
        'epsilon': 0.1,
        'expected_optimal_pieces': 1
    },
    # 16. Noise Exceeding Epsilon (Forces splitting)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.5, 0.4), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.5,
        'expected_optimal_pieces': 2 # Segment 1: (0.0, 0.0) to (1.5, 0.4) fails, so (0.0, 0.0) to (1.0, 1.0) is Piece 1, then (1.0, 1.0) to (3.0, 3.0) is Piece 2. (0.0,0.0) to (3.0,3.0) fails with error 0.6.
    },
    # 17. The Example from the Prompt (Verification)
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        'epsilon': 0.5,
        'expected_optimal_pieces': 2 # (0.0, 1.0) to (2.0, 3.0) has max error 0.0. (2.0, 3.0) to (5.0, 8.0) is another line.
    },
    # 18. Large Gap in X-coordinates (Tests scale independence of error calculation)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (1000.0, 0.0), (1001.0, 0.1)],
        'epsilon': 0.01,
        'expected_optimal_pieces': 3
    },
    # 19. Two Tight Bends (Ensures non-greedy local optimal choice)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        'epsilon': 0.4,
        'expected_optimal_pieces': 3
    },
    # 20. Simple Curve (Verifies 2 segments are needed)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
        'epsilon': 0.2,
        'expected_optimal_pieces': 2 # (0.0 to 2.0) is max error 0.1. (2.0 to 4.0) is max error 0.1. (0.0 to 4.0) is max error 0.4.
    }
]
test_cases8 = [
    # 1. Base Case: Flat Line (Should only need 1 piece)
    {
        "description": "Perfectly flat line, tolerance large enough.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 2. Base Case: Perfectly Linear (Should only need 1 piece)
    {
        "description": "Perfectly linear slope, tolerance large enough.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 3. Minimum Pieces: Only 1 Piece (Tolerance is large)
    {
        "description": "All points fit within a single linear segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # 4. Maximum Pieces: Every point requires its own piece (Tolerance is tiny)
    {
        "description": "Maximum pieces (n) needed due to very small epsilon.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], # 5 points, 4 pieces max
        "epsilon": 0.001,
        "expected_pieces": 4
    },
    # 5. Sawtooth Wave (High curvature, requires many pieces)
    {
        "description": "High frequency, high amplitude oscillation (Sawtooth).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.2,
        "expected_pieces": 3 # (0,0)-(2,0) fits, (2,0)-(4,0) fits, (4,0)-(5,1) needs another? No: (0,0)-(2,0) fails. Expected: 3 pieces: (0,0)-(2,0) -> 1.0 max error. (0,0)-(3,1) -> 1.0 max error. (0,0)-(1,1) (2,0)-(3,1) (4,0)-(5,1) - each needs max 2 pieces, but 3 pieces required: (0,0)-(2,0) fails. Try 3: (0,0) to (2,0) error 1.0. 4 needed.
    },
    # 6. Step Function (Vertical jump in slope, forces a break)
    {
        "description": "Abrupt change in slope (Step up), forces a segment break.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # (0,0)-(1,0) is one, (2,10)-(3,10) is one. (0,0)-(3,10) has max error of 5.0 at (1,0)
    },
    # 7. Step Function (Tolerance too tight, forces multiple breaks)
    {
        "description": "Abrupt change in slope, tight tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.001, 10.0), (2.0, 10.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # 8. Concave Curve (Error builds up in the middle)
    {
        "description": "Concave curve (parabola-like), error largest in the middle.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 0.5), (3.0, 0.25), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 3 # (0,0) to (2, 0.5) has max error of 0.25, too high. (0,0) to (1.0, 0.25), (1.0, 0.25) to (3.0, 0.25), (3.0, 0.25) to (4.0, 0.0) -> 3 pieces
    },
    # 9. Convex Curve (Error builds up in the middle)
    {
        "description": "Convex curve (upside-down parabola-like), error largest in the middle.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.75), (2.0, 0.5), (3.0, 0.75), (4.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 3 # Similar to concave, (0,1) to (2, 0.5) has error 0.25. (0,1) to (1, 0.75) and so on.
    },
    # 10. Boundary Case: Exactly meeting epsilon at one point (Should pass as 1 piece)
    {
        "description": "All points fit, one point is exactly at the epsilon boundary.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # 11. Boundary Case: Slightly exceeding epsilon at one point (Should force 2 pieces)
    {
        "description": "One point is slightly past epsilon boundary, forcing 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # 12. Multiple Small Oscillations (Checks the ability to jump small gaps)
    {
        "description": "Small, rapid oscillations, checking segment 'jumping'.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (1.0, 0.0), (1.5, -0.1), (2.0, 0.0)],
        "epsilon": 0.15,
        "expected_pieces": 1 # A single line from (0,0) to (2,0) has max error of 0.1.
    },
    # 13. Wide Gap Test (Checks for optimality over a long stretch)
    {
        "description": "A long, almost-linear section followed by a sharp turn.",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.1), (20.0, 0.2), (21.0, 1.0)],
        "epsilon": 0.3,
        "expected_pieces": 1 # (0,0) to (21, 1.0). Max error at (10, 0.1) is approx 0.1 - 0.047 = 0.053.
    },
    # 14. Edge Case: Start/End Points are the only ones within tolerance
    {
        "description": "Only the start and end points can be connected, forcing maximum break points.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 3 # (0,0) to (1,10) fails. (0,0) to (2,0) fails. 3 pieces: (0,0)-(1,10), (1,10)-(2,0), (2,0)-(3,10)
    },
    # 15. Zero Tolerance (Forces max pieces = n)
    {
        "description": "Zero tolerance (epsilon=0.0), forcing every point to be a piece break.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 2 # 3 points -> 2 segments/pieces
    },
    # 16. Negative Coordinates
    {
        "description": "Test with negative x and y coordinates.",
        "pw_linear_fx": [(-2.0, 5.0), (-1.0, 4.8), (0.0, 5.0), (1.0, 5.2)],
        "epsilon": 0.2,
        "expected_pieces": 1
    },
    # 17. Floating Point Precision Issue Test
    {
        "description": "Tightly spaced points with small deviations, testing floating point stability.",
        "pw_linear_fx": [(0.0, 0.0), (0.001, 0.0001), (0.002, 0.0), (0.003, -0.0001)],
        "epsilon": 0.00005,
        "expected_pieces": 3 # (0,0) to (0.002, 0) error is 0.0001. Too high. (0,0) to (0.001, 0.0001) etc.
    },
    # 18. Non-Uniform X Spacing
    {
        "description": "Large and small x-intervals mixed.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (10.0, 1.0), (11.0, 2.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0) to (1,1) is fine. (1,1) to (11, 2) has max error at (10, 1.0) of 0.0. Max error at (1,1) is 0.0.
    },
    # 19. Initial Flat Section Followed by Sharp Linear Ramp
    {
        "description": "Long flat section, followed by a sharp slope.",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 0.0), (6.0, 5.0), (7.0, 10.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,0) to (5,0) is one. (5,0) to (7,10) has max error of 0.0 at (6,5)
    },
    # 20. Non-Optimal Local Choice Trap (Tests greedy vs. optimal algorithm)
    # The optimal path should skip a nearby point to reach a further, better point.
    {
        "description": "Test if the algorithm avoids a greedy/local optimum trap.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.8), (2.0, 0.0), (3.0, 0.0), (4.0, 0.8), (5.0, 0.0)],
        "epsilon": 0.81,
        "expected_pieces": 1 # (0,0) to (5,0) has max error 0.8. Optimal is 1 piece. A greedy algorithm might break at (2,0) or (3,0).
    }
]
test_cases9 = [
    # 1. Basic Collinear (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "description": "Perfectly linear function, loose epsilon. Should be 1 piece."
    },

    # 2. Perfect Fit (Epsilon = 0, Should be n pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_pieces": 4,  # n+1 points = n segments
        "description": "Zero epsilon requires every segment to be a piece."
    },

    # 3. Simple Step Function (Requires 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 1.0), (2.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        "description": "Sharp discontinuity near x=1.0, forces a piece break."
    },

    # 4. Concave Function (Tight fit required)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 0.9), (4.0, 1.0)],
        "epsilon": 0.15,
        "expected_pieces": 2,
        "description": "Concave curve, large max error at midpoint (1.5, 0.65) if 1 piece. Should be 2 pieces."
    },

    # 5. Convex Function (Tight fit required)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.5), (2.0, 0.2), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.15,
        "expected_pieces": 2,
        "description": "Convex curve, large max error at midpoint. Should be 2 pieces."
    },

    # 6. Zig-Zag / Alternating Error
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 3,
        "description": "Alternating points just outside a single-piece tolerance. Tight epsilon requires multiple pieces."
    },

    # 7. Zig-Zag, Max Epsilon (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "description": "Alternating points that *just* fit within a single-piece tolerance."
    },

    # 8. All Constant (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (5.0, 5.0), (10.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1,
        "description": "Constant function with non-uniform x spacing, loose epsilon. Should be 1 piece."
    },

    # 9. Single Point Off-Line (Forces a break)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "description": "One point (2.0, 1.0) is exactly max-error away from the endpoints. Forces 2 pieces."
    },

    # 10. Single Point Off-Line (Barely fits, 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "One point (2.0, 1.0) is the max error. Fits just inside 1 piece."
    },

    # 11. End-Point Tolerance Test (Backward/Forward look)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 0.0), (3.0, -0.9), (4.0, 0.0)],
        "epsilon": 0.9,
        "expected_pieces": 1,
        "description": "A 'W' shape, points at the exact tolerance limit. Should be 1 piece."
    },

    # 12. End-Point Tolerance Test (Forces 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.9001), (2.0, 0.0), (3.0, -0.9001), (4.0, 0.0)],
        "epsilon": 0.9,
        "expected_pieces": 2,  # Must split at 2.0 to capture the sharp peaks
        "description": "Same as 11, but points are just outside tolerance. Forces multiple pieces."
    },

    # 13. Non-Uniform X Spacing, Convex shape
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.01), (5.0, 0.1), (10.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 2,
        "description": "Non-uniform x spacing, must check max error carefully, forces 2 pieces."
    },

    # 14. Dense Points, Small Tolerance (Should require many pieces)
    {
        "pw_linear_fx": [(i, 0.1 * ((i % 2) - 0.5)) for i in range(11)],  # x=0 to 10, y= -0.05, 0.05, -0.05...
        "epsilon": 0.01,
        "expected_pieces": 5,  # Every other point likely forces a break
        "description": "Dense, slightly noisy data, very tight tolerance. Expect many pieces."
    },

    # 15. Sinusoidal Approximation (Tests curve fitting)
    {
        "pw_linear_fx": [(i / 4.0, 1.0 * (i / 4.0)) for i in range(17)],  # A linear function, should be 1 piece
        "epsilon": 0.0001,
        "expected_pieces": 1,
        "description": "Test with points generated programmatically for a simple line."
    },

    # 16. Sinusoidal Approximation (Forces multiple breaks)
    {
        "pw_linear_fx": [(i / 4.0, 0.5 * (1.0 - (i / 16.0)) * (1.0 - (i / 16.0)) * (i / 16.0)) for i in range(17)],
        "epsilon": 0.01,
        "expected_pieces": 3,  # Example of a complex cubic function requiring multiple fits.
        "description": "Complex curve (cubic) with non-obvious optimal breakpoints. Must find minimal pieces."
    },

    # 17. The 'Stuck' Problem (Need to ensure the piece break is optimal)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        "description": "Initial points (0,1,2) barely fit. The optimal solution should break at (2.0, 0.0) and use the minimum remaining pieces."
    },

    # 18. Large Data Range (Tests floating point stability)
    {
        "pw_linear_fx": [(i * 1000.0, i * 1000.0) for i in range(5)],
        "epsilon": 10.0,
        "expected_pieces": 1,
        "description": "Large coordinate values, should still result in 1 piece."
    },

    # 19. Two Consecutive Large Errors (Forces small pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (1.5, -0.5), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.2,
        "expected_pieces": 3,
        "description": "Two consecutive, high-error points close to each other, forces two very small pieces at the start."
    },

    # 20. Non-Monotonic X (Ensures robust input handling - should ideally fail or be handled by the function)
    # Assuming the algorithm requires X to be monotonic, but testing the edge case anyway.
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (1.0, 1.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_pieces": 3,  # If algorithm processes points in order, it will be 3 pieces
        "description": "Non-monotonic x-values, testing robust input handling. (If X must be monotonic, this is an invalid test)."
    },
]
test_cases10 = [
    # 1. Baseline - Simple linear increase (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1
    },

    # 2. Perfect alignment (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5), (4.0, 2.0)],
        "epsilon": 0.0
    },

    # 3. Flat data (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.0
    },

    # 4. Large deviation (V-shape) - Forces a split (Expected: 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.1
    },

    # 5. Sawtooth pattern - Small epsilon forces many pieces (Expected: 3 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.4
    },

    # 6. Sawtooth pattern - Large epsilon reduces to 1 piece (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 7. Step function - Forces a split (Expected: 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 0.1
    },

    # 8. Point exactly on the edge of tolerance (y=0.5) - Should be 1 piece if optimal
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.5), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 9. Point just outside the tolerance (y=0.51) - Forces a split (Expected: 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.51), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 10. Non-uniform x-spacing with linear increase (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (1.0, 10.0), (10.0, 100.0)],
        "epsilon": 0.01
    },

    # 11. Non-uniform x-spacing with sharp peak (Expected: 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (5.0, 10.0), (5.1, 0.0), (10.0, 0.0)],
        "epsilon": 0.1
    },

    # 12. Alternating points slightly off a straight line (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.05), (3.0, 0.05), (4.0, -0.05), (5.0, 0.0)],
        "epsilon": 0.1
    },

    # 13. Data requiring exactly 3 pieces (Expected: 3 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (4.0, 4.0), (5.0, 1.0)],
        "epsilon": 0.5
    },

    # 14. Data requiring exactly 2 pieces (Expected: 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0), (5.0, 1.0)],
        "epsilon": 0.1
    },

    # 15. Minimal points (3 points) - Linear (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.0
    },

    # 16. Minimal points (3 points) - V-shape (Expected: 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)],
        "epsilon": 0.1
    },

    # 17. Extreme coordinates/scaling test (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1000.0, 0.0), (2000.0, 0.0)],
        "epsilon": 1.0
    },

    # 18. Tightest possible fit requiring 2 pieces (Expected: 2 pieces)
    # The midpoint (1.5, 1.1) is off by 1.1 from the line y=0. Epsilon is 1.0.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.5, 1.1), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 1.0
    },

    # 19. Same data, but epsilon allows 1 piece (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.5, 1.1), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 1.1
    },

    # 20. Data testing greedy vs. optimal segmentation (Expected: 2 pieces)
    # A single segment from (0,0) to (4,1) has a max error around 0.25, which exceeds epsilon=0.1.
    # Optimal segmentation is (0,0) to (3,0) and (3,0) to (4,1).
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0)],
        "epsilon": 0.1
    },
]
test_cases11 = [
    # ----------------------------------------------------------------------
    # 1. Base Case: Trivial approximation (1 piece)
    # ----------------------------------------------------------------------
    {
        "name": "Single segment, all points on it",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 1.0,  # Large tolerance, should result in 1 piece
        "expected_pieces": 1
    },
    # ----------------------------------------------------------------------
    # 2. Perfect Fit Case (1 piece)
    # ----------------------------------------------------------------------
    {
        "name": "All points within epsilon of first-to-last segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.2), (3.0, 0.3), (4.0, -0.4)],
        "epsilon": 0.5, # Max deviation is 0.4 at x=4.0
        "expected_pieces": 1
    },
    # ----------------------------------------------------------------------
    # 3. Minimum Two Pieces Case (Threshold test)
    # ----------------------------------------------------------------------
    {
        "name": "Requires two pieces: max error exactly equals epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.6), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.5, # First segment (0,0) to (2,0) has max error 0.6 > 0.5. Must break.
        "expected_pieces": 2 # (0,0) to (1, 0.6) is invalid, must be (0,0) to (1, 0.6) and (1, 0.6) to (3, 0)
    },
    # ----------------------------------------------------------------------
    # 4. Constant Function (1 piece)
    # ----------------------------------------------------------------------
    {
        "name": "Constant function, should be 1 piece",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    # ----------------------------------------------------------------------
    # 5. Sawtooth/V-shape (Forces many pieces)
    # ----------------------------------------------------------------------
    {
        "name": "Sharp V-shape, forcing many segments (epsilon = 0.0)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.0, # Forces point-to-point segments
        "expected_pieces": 4
    },
    # ----------------------------------------------------------------------
    # 6. Critical Point: Error *just* exceeds epsilon
    # ----------------------------------------------------------------------
    {
        "name": "Critical error: requires a split at point 3",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, 0.6), (4.0, 0.0)],
        "epsilon": 0.5, # Segment (0,0) to (4,0) has error 0.6. Optimal break is after (2,0).
        "expected_pieces": 2 # (0,0) to (3, 0.6) error > 0.5 (must break before 3)
    },
    # ----------------------------------------------------------------------
    # 7. Long Span, then a sharp change (Testing 'look ahead')
    # ----------------------------------------------------------------------
    {
        "name": "Long flat run followed by a spike that needs a break",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (11.0, 1.0), (12.0, 0.0)],
        "epsilon": 0.5, # Segment (0,0) to (12,0) has error 1.0. Optimal break is at (10,0).
        "expected_pieces": 2 # (0,0) to (10.0, 0.0) [Error 0], then (10.0, 0.0) to (12.0, 0.0) [Error 1.0 > 0.5] -> must break
    },
    # ----------------------------------------------------------------------
    # 8. All points on one side of the optimal line
    # ----------------------------------------------------------------------
    {
        "name": "Parabola-like shape, points only above",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.5, # Max error is 0.4, covered by 1 segment
        "expected_pieces": 1
    },
    # ----------------------------------------------------------------------
    # 9. Optimal choice is NOT the full segment
    # ----------------------------------------------------------------------
    {
        "name": "Optimal segment choice (mid-run split)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.6), (3.0, 0.1), (4.0, 0.0), (5.0, 0.1)],
        "epsilon": 0.5, # Segment (0,0) to (4,0) has error 0.6 (fails). Must break at (2, 0.6).
        "expected_pieces": 3 # (0,0) to (2.0, 0.6), (2.0, 0.6) to (4.0, 0.0), (4.0, 0.0) to (5.0, 0.1)
    },
    # ----------------------------------------------------------------------
    # 10. Large Number of Points
    # ----------------------------------------------------------------------
    {
        "name": "Large set, all fit in 1 piece",
        "pw_linear_fx": [(i, 0.5 * (i % 2) - 0.25) for i in range(11)], # Alternating small y-value
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # ----------------------------------------------------------------------
    # 11. Large Number of Points - Forces many pieces
    # ----------------------------------------------------------------------
    {
        "name": "Large set, forcing max pieces (epsilon = 0.0)",
        "pw_linear_fx": [(i, i % 2) for i in range(11)],
        "epsilon": 0.0,
        "expected_pieces": 10
    },
    # ----------------------------------------------------------------------
    # 12. Segment Error at the start/end points
    # ----------------------------------------------------------------------
    {
        "name": "Error near start/end of the segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.5, # Segment (0,0) to (3,1) has error 1.0 > 0.5. Optimal break at (2,0).
        "expected_pieces": 2
    },
    # ----------------------------------------------------------------------
    # 13. Negative Y-values
    # ----------------------------------------------------------------------
    {
        "name": "Negative Y-values test",
        "pw_linear_fx": [(0.0, -1.0), (1.0, -0.5), (2.0, -1.0), (3.0, -1.5)],
        "epsilon": 0.4, # Segment (0,-1) to (3,-1.5) has max error 0.5 (at x=1). Fails.
        "expected_pieces": 2
    },
    # ----------------------------------------------------------------------
    # 14. Very Small Epsilon
    # ----------------------------------------------------------------------
    {
        "name": "Very small epsilon, forcing many pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.01), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.005, # Max error 0.01 > 0.005. Fails.
        "expected_pieces": 2
    },
    # ----------------------------------------------------------------------
    # 15. The 'Staircase' Function (Testing step changes)
    # ----------------------------------------------------------------------
    {
        "name": "Step function (staircase)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 1.0), (2.0, 1.0)],
        "epsilon": 0.5, # Segment (0,0) to (2,1) has max error 0.5 at x=1.0001
        "expected_pieces": 2 # (0,0) to (1,0) and (1.0001, 1.0) to (2, 1.0)
    },
    # ----------------------------------------------------------------------
    # 16. Multiple critical points within a segment
    # ----------------------------------------------------------------------
    {
        "name": "Multiple error points, error is from first one",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.6), (2.0, 0.7), (3.0, 0.0)],
        "epsilon": 0.5, # Segment (0,0) to (3,0) max error 0.7. Optimal break at (1, 0.6)
        "expected_pieces": 2
    },
    # ----------------------------------------------------------------------
    # 17. The 'Slope Change' Case
    # ----------------------------------------------------------------------
    {
        "name": "Slope change that requires a split",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.4, # Segment (0,0) to (3,0) has max error 1.0. Optimal break at (1, 1.0) or (2, 1.0).
        "expected_pieces": 3 # (0,0) to (1, 1.0), (1, 1.0) to (2, 1.0), (2, 1.0) to (3, 0.0)
    },
    # ----------------------------------------------------------------------
    # 18. Non-Uniform X-spacing
    # ----------------------------------------------------------------------
    {
        "name": "Non-uniform x-spacing with a required split",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (10.0, 0.0), (11.0, 0.6), (12.0, 0.0)],
        "epsilon": 0.5, # Segment (0,0) to (12,0) has error 0.6. Optimal break at (10,0).
        "expected_pieces": 2
    },
    # ----------------------------------------------------------------------
    # 19. Segmenting from a mid-point
    # ----------------------------------------------------------------------
    {
        "name": "Starting a segment from an already elevated point",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0)],
        "epsilon": 0.0, # Forces max pieces
        "expected_pieces": 3
    },
    # ----------------------------------------------------------------------
    # 20. Example from prompt
    # ----------------------------------------------------------------------
    {
        "name": "Prompt example",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5, # Segment (0,1) to (5,8) has max error 1.5 at (2,3). Fails.
        "expected_pieces": 2 # (0,1) to (2,3) max error 0.0. (2,3) to (5,8) max error 0.0.
    }
]
test_cases12 = [
    # 1. Base Case: Trivial approximation (perfectly linear, N_min=1)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_n_min": 1,
        "description": "Perfectly linear data. Should require 1 piece."
    },
    # 2. Perfect Fit: N_min=1, even with larger tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1.0,
        "expected_n_min": 1,
        "description": "Perfectly linear data with large epsilon."
    },
    # 3. Maximum Tolerance: N_min=1 (all points fit in one piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.0)],
        "epsilon": 0.2,
        "expected_n_min": 1,
        "description": "All points fit within a single linear piece."
    },
    # 4. Zero Tolerance: N_min = n (each segment is a piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_n_min": 4, # 4 segments, 5 points -> 4 pieces required
        "description": "Zero tolerance forces every segment to be a piece."
    },
    # 5. Tight Fit, N_min=2: Point barely exceeds tolerance, forcing a split
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.5)],
        "epsilon": 0.1,
        "expected_n_min": 2, # (0,0) to (3,0) fits, (4,0.5) must start a new piece.
        "description": "One point barely exceeds epsilon, forcing two pieces."
    },
    # 6. Step Function: Requires many pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (0.3, 1.0), (0.4, 0.0)],
        "epsilon": 0.1,
        "expected_n_min": 4, # Max error is 0.5 in each segment. Requires 4 pieces.
        "description": "Highly oscillatory/step data, small epsilon. N_min=4."
    },
    # 7. Step Function (Larger Epsilon): Requires fewer pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (0.3, 1.0), (0.4, 0.0)],
        "epsilon": 0.51,
        "expected_n_min": 1, # The max error is 0.5 (at 0.1, 0.3)
        "description": "Highly oscillatory/step data with large enough epsilon. N_min=1."
    },
    # 8. Convex Curve (Parabola): Requires splitting
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.01), (2.0, 0.04), (3.0, 0.09), (4.0, 0.16)],
        "epsilon": 0.02,
        "expected_n_min": 3, # (0,0) to (2,0.04) has max error 0.02. Next point (3,0.09) is too far.
        "description": "Convex curve, max error should occur at interior point(s)."
    },
    # 9. Non-Uniform X-Spacing: Should not affect optimality based on Y-error
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.1), (11.0, -0.1), (20.0, 0.0)],
        "epsilon": 0.1,
        "expected_n_min": 1,
        "description": "Non-uniform x-spacing, all points fit within tolerance."
    },
    # 10. Negative Coordinates (Y): Should be handled correctly
    {
        "pw_linear_fx": [(0.0, -10.0), (1.0, -9.9), (2.0, -9.8), (3.0, -9.7)],
        "epsilon": 0.05,
        "expected_n_min": 1,
        "description": "Negative Y-coordinates, perfectly linear."
    },
    # 11. Negative Coordinates (X): Should be handled correctly
    {
        "pw_linear_fx": [(-3.0, 0.0), (-2.0, 1.0), (-1.0, 0.0), (0.0, 1.0)],
        "epsilon": 0.4,
        "expected_n_min": 2, # (-3,0) to (-1,0) fits (error 0.5 at x=-2). Split needed.
        "description": "Negative X-coordinates, requires 2 pieces."
    },
    # 12. Minimal Input: Two points (N_min=1)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_n_min": 1,
        "description": "Minimal input: two points, always 1 piece."
    },
    # 13. Minimal Input: Three collinear points (N_min=1)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0,
        "expected_n_min": 1,
        "description": "Minimal non-trivial collinear input."
    },
    # 14. Large Dataset & Low Tolerance: Expect many pieces
    {
        "pw_linear_fx": [(i, i % 2) for i in range(11)], # 0,1,0,1,0,1...
        "epsilon": 0.01,
        "expected_n_min": 10, # 10 segments, 11 points -> each segment must be a piece.
        "description": "Large highly-oscillating dataset, very low tolerance."
    },
    # 15. Horizontal Line: Should require N_min=1
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0)],
        "epsilon": 0.0,
        "expected_n_min": 1,
        "description": "Perfectly horizontal line with zero tolerance."
    },
    # 16. Vertical-like segment (but strictly monotonic X): N_min=2
    {
        "pw_linear_fx": [(0.0, 0.0), (0.001, 10.0), (1.0, 10.0)],
        "epsilon": 0.01,
        "expected_n_min": 2,
        "description": "Very steep initial slope forces two pieces."
    },
    # 17. Convex to Concave transition
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_n_min": 3, # (0,0) to (2,0) has error 0.5. (2,0) to (4,0) has error 0.5. Requires 3 pieces.
        "description": "Change in curvature, testing the internal error checks."
    },
    # 18. Floating point precision issue (tolerance barely fails)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.10000000000000001), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_n_min": 2, # Should be N_min=2 if the error is > epsilon, due to float precision
        "description": "Floating point value slightly exceeding epsilon, testing strict inequality handling."
    },
    # 19. Floating point precision issue (tolerance barely succeeds)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.09999999999999999), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_n_min": 1, # Should be N_min=1 if the error is <= epsilon
        "description": "Floating point value slightly under epsilon, testing inequality handling."
    },
    # 20. Mixed Slopes and Uniform X: Example from problem description variation
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 5.0), (4.0, 6.0)],
        "epsilon": 0.5,
        "expected_n_min": 2, # (0,1) to (3,5) fits with error 0.5 (at x=2). Next point (4,6) requires split.
        "description": "Mixed slopes, forcing a split on the third segment."
    }
]
test_cases13 = [
    # 1. Base Case: Perfectly Linear Data (Expected: 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
     'epsilon': 0.1,
     'expected_pieces_optimal': 1},

    # 2. Perfect Fit with Zero Tolerance (Expected: N-1 pieces for N points)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
     'epsilon': 0.0,
     'expected_pieces_optimal': 4},

    # 3. Simple Concave-Up Curve: Parabola (Expected: 3 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
     'epsilon': 0.05,
     'expected_pieces_optimal': 3},

    # 4. Simple Convex-Down Curve: Sine Wave Peak (Expected: 2 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.9), (2.0, 1.0), (3.0, 0.9), (4.0, 0.0)],
     'epsilon': 0.1,
     'expected_pieces_optimal': 2},

    # 5. Sawtooth/Alternating Max Error: Error-Driving Points (Expected: 3 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, 0.2), (4.0, 0.0)],
     'epsilon': 0.1,
     'expected_pieces_optimal': 3},

    # 6. High Tolerance: All Points Covered (Expected: 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
     'epsilon': 1.0,
     'expected_pieces_optimal': 1},

    # 7. Step Function (Sharp Jumps) - Tolerance must be inclusive of the jump point (Expected: 2 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.1, 10.0), (2.0, 10.0), (2.1, 0.0)],
     'epsilon': 1.0,
     'expected_pieces_optimal': 2},

    # 8. Trivial Case: Only Two Points (Expected: 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (10.0, 10.0)],
     'epsilon': 0.001,
     'expected_pieces_optimal': 1},

    # 9. Non-Uniform X-Spacing (Expected: 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (0.1, 0.0), (10.0, 1.0), (10.1, 1.0)],
     'epsilon': 0.05,
     'expected_pieces_optimal': 1},

    # 10. Horizontal Line with Small Perturbations (Expected: 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.01), (2.0, -0.01), (3.0, 0.0)],
     'epsilon': 0.02,
     'expected_pieces_optimal': 1},

    # 11. Maximum Error at the Beginning (Expected: 2 pieces)
    {'pw_linear_fx': [(0.0, 1.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
     'epsilon': 0.1,
     'expected_pieces_optimal': 2},

    # 12. Maximum Error at the End (Expected: 2 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0)],
     'epsilon': 0.1,
     'expected_pieces_optimal': 2},

    # 13. Case Where Splitting One Segment Works (Expected: 2 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, -0.2), (4.0, 0.0)],
     'epsilon': 0.1,
     'expected_pieces_optimal': 2},

    # 14. Dense Data with Slight Curvature (y=0.01*x^2) (Expected: 4 pieces)
    {'pw_linear_fx': [(i, i ** 2 * 0.01) for i in range(11)],
     'epsilon': 0.02,
     'expected_pieces_optimal': 4},

    # 15. Negative Y Values (Ensure absolute error calculation is correct) (Expected: 3 pieces)
    {'pw_linear_fx': [(0.0, -1.0), (1.0, -0.9), (2.0, -0.6), (3.0, -0.1), (4.0, 0.0)],
     'epsilon': 0.05,
     'expected_pieces_optimal': 3},

    # 16. Error Driven by a Single Interior Point (Midpoint Error > epsilon) (Expected: 2 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
     'epsilon': 0.4,
     'expected_pieces_optimal': 2},

    # 17. Single Interior Point BARELY within Tolerance (Max error = epsilon) (Expected: 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
     'epsilon': 0.5,
     'expected_pieces_optimal': 1},

    # 18. Large Data Span/Scale (Expected: 1 piece)
    {'pw_linear_fx': [(0.0, 1000.0), (1.0, 1000.0), (2.0, 1000.0), (3.0, 1000.1)],
     'epsilon': 0.05,
     'expected_pieces_optimal': 1},

    # 19. Repeated Points (Expected: 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
     'epsilon': 0.1,
     'expected_pieces_optimal': 1},

    # 20. Mixed Curvature: Concave then Convex (Expected: 3 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 0.5), (4.0, 0.0)],
     'epsilon': 0.1,
     'expected_pieces_optimal': 3},
]
test_cases14 = [
    # 1. Uniformly Spaced, Flat (Baseline)
    {"pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)], "epsilon": 1.0},

    # 2. Uniformly Spaced, Linear (Baseline)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.1},

    # 3. Maximum Deviation (Boundary Hit)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)], "epsilon": 0.499},

    # 4. Maximum Deviation (Boundary Miss)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)], "epsilon": 0.501},

    # 5. Small Epsilon (Many Segments)
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.5), (3, 0.9), (4, 1.0), (5, 0.9), (6, 0.5), (7, 0.1), (8, 0)],
     "epsilon": 0.01},

    # 6. Large Epsilon (Single Segment)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0), (4.0, 0.0)], "epsilon": 5.0},

    # 7. Greedy Failure Case (Critical for Optimality Test)
    {"pw_linear_fx": [(0, 0), (1, 0.8), (2, 0.9), (3, 0.2), (4, 1.0)], "epsilon": 0.3},

    # 8. Zig-Zag Path (Alternating Slopes)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1), (6, 0)], "epsilon": 0.05},

    # 9. Vertical Jumps (Steep Sections)
    {"pw_linear_fx": [(0.0, 0.0), (0.1, 5.0), (0.2, 0.0), (1.0, 1.0)], "epsilon": 0.5},

    # 10. Only Two Points (Minimum Input)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)], "epsilon": 0.001},

    # 11. Negative Coordinates/Values
    {"pw_linear_fx": [(-5.0, -5.0), (-3.0, -4.0), (-1.0, -3.0), (0.0, -2.5)], "epsilon": 0.1},

    # 12. Flat Followed by Steep Change (Knee Point)
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 5.0), (4.0, 6.0)], "epsilon": 0.5},

    # 13. Floating Point Epsilon Boundary (Precision)
    {"pw_linear_fx": [(0, 0), (1, 0.125), (2, 0.25), (3, 0.375), (4, 0.5)], "epsilon": 0.124999},

    # 14. Smallest Possible Epsilon (Maximum Segments)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.0},

    # 15. Convex Shape (Parabola)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)], "epsilon": 3.0},

    # 16. Concave Shape (Parabola Reflected)
    {"pw_linear_fx": [(0, 16), (1, 9), (2, 4), (3, 1), (4, 0)], "epsilon": 3.0},

    # 17. Dense Sampling in one area
    {"pw_linear_fx": [(0, 0), (0.1, 0), (0.2, 0), (0.5, 0), (1.0, 5.0), (1.1, 5.0)], "epsilon": 0.1},

    # 18. Points Far from x=0
    {"pw_linear_fx": [(100.0, 5.0), (101.0, 5.1), (102.0, 5.2), (103.0, 5.3)], "epsilon": 0.2},

    # 19. Large Dataset, Optimal Greedy (Long Linear)
    {"pw_linear_fx": [(i, 2 * i) for i in range(10)], "epsilon": 0.01},

    # 20. Large Dataset, Minimal Epsilon (Max segments for a long curve)
    {"pw_linear_fx": [(i, i ** 2) for i in range(10)], "epsilon": 0.001},
]
test_cases15 = [
    # 1. Basic Cases: Simple, smooth, or constant data
    {
        "description": "Constant function, should be 1 piece.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Perfect linear function, should be 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "Small, gentle quadratic curve within tolerance, should be 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.15), (3.0, 0.3), (4.0, 0.5)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Two clearly defined linear segments, minimum 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0001, 1.0), (2.0, 0.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },

    # 2. Critical Edge Cases for Tolerance (ε)
    {
        "description": "Data point exactly at epsilon limit (vertical offset).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 1.0,  # L_inf error at x=3 is 1.0. This should pass as 1 piece.
        "expected_pieces": 1
    },
    {
        "description": "Data point slightly exceeds epsilon, forcing a split (1 piece fails).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0001)],
        "epsilon": 1.0,
        "expected_pieces": 2  # Must split, likely at x=2 or x=1
    },
    {
        "description": "Tolerance of zero (0.0): Requires exact fit, N pieces for N+1 points.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },

    # 3. Concavity and Convexity (Smooth Curves)
    {
        "description": "Smooth convex curve (parabola), requires multiple pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.5,
        "expected_pieces": None  # Hard to predict, tests optimality (should be > 1)
    },
    {
        "description": "Smooth concave curve (sqrt), requires multiple pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (4.0, 2.0), (9.0, 3.0), (16.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": None  # Tests correct error calculation in low-slope regions
    },

    # 4. High-Frequency / Oscillating Data
    {
        "description": "High-frequency sine wave, demanding many small pieces.",
        "pw_linear_fx": [(i, 0.5 * (-1) ** i) for i in range(10)],  # Alternating +/- 0.5
        "epsilon": 0.1,
        "expected_pieces": 9
    },
    {
        "description": "Low-frequency sine wave, should pass with few pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.866), (3.0, 1.0), (4.0, 0.866), (5.0, 0.5), (6.0, 0.0)],
        "epsilon": 0.3,
        "expected_pieces": None  # Should be around 3 or 4
    },

    # 5. Spiky/Zigzag and Non-Uniformly Spaced Data
    {
        "description": "Sharp V-shape (absolute value function), testing the corner.",
        "pw_linear_fx": [(0.0, 4.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 2  # Optimal split is at x=2.0
    },
    {
        "description": "Single narrow spike/outlier, forcing a split.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 3  # Must isolate the spike
    },
    {
        "description": "Non-uniform X-spacing (dense then sparse).",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.01), (0.2, 0.04), (10.0, 0.0), (10.1, -0.01)],
        "epsilon": 0.1,
        "expected_pieces": 2  # Small curve then a large linear segment
    },
    {
        "description": "Multiple segments in close proximity, testing merge prevention.",
        "pw_linear_fx": [(0, 0), (1, 1), (1.01, 0), (2, 1), (2.01, 0), (3, 1)],
        "epsilon": 0.01,
        "expected_pieces": 5
    },

    # 6. Degenerate/Extreme Cases
    {
        "description": "Only 2 data points, must be 1 piece.",
        "pw_linear_fx": [(0.0, 10.0), (5.0, -10.0)],
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    {
        "description": "Large Y-values, testing precision/floating point stability.",
        "pw_linear_fx": [(0.0, 10000.0), (1.0, 10001.0), (2.0, 10004.0), (3.0, 10009.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "description": "Large X-range, testing slope calculation precision.",
        "pw_linear_fx": [(0.0, 0.0), (1000.0, 1.0), (2000.0, 2.0)],
        "epsilon": 0.001,
        "expected_pieces": 1
    },
    {
        "description": "Negative coordinates.",
        "pw_linear_fx": [(-2.0, 3.0), (-1.0, 1.0), (0.0, -1.0), (1.0, -3.0), (2.0, -5.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },

    # 7. A challenging case for optimality (where a greedy choice might fail)
    {
        "description": "Segment 1 can cover 3 points, but only if Segment 2 is shorter.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 1.0), (4.0, 1.5), (5.0, 1.0)],
        "epsilon": 0.51,
        "expected_pieces": 2  # Optimal: [(0,0) to (3,1)], then [(3,1) to (5,1)]
    }
]
test_cases16 = [
    # 1. Basic Monotonic (Straight Line) - Should use 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "description": "Perfect straight line, high tolerance. Should be 1 piece."
    },

    # 2. Step Function (Max Discontinuity) - Tests tolerance vs large jumps
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 10.0), (2.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 2,  # Must use 2 pieces due to the large jump
        "description": "Vertical jump/step function. Must use 2 pieces."
    },

    # 3. V-Shape (Sharp Corner) - Optimal pieces often meet at the corner
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "description": "Sharp V-shape. Needs 2 pieces, meeting at the minimum."
    },

    # 4. Parabola (Smooth Curve) - Tests approximation of a continuous curve
    {
        "pw_linear_fx": [(x / 10.0, (x / 10.0) ** 2) for x in range(21)],  # y=x^2 from 0 to 2
        "epsilon": 0.05,
        "expected_pieces_min": 3,  # Requires several pieces for good fit
        "description": "Smooth quadratic curve. Tests multi-segment optimization."
    },

    # 5. Sawtooth Wave (High Frequency) - Must use many small pieces
    {
        "pw_linear_fx": [(i, (i % 2) * 2.0) for i in range(11)],  # (0,0), (1,2), (2,0), (3,2), ...
        "epsilon": 0.01,
        "expected_pieces": 10,  # Must use a piece for every segment due to high oscillation
        "description": "High-frequency sawtooth wave, low tolerance. Should be maximum pieces."
    },

    # 6. Noise on a Line (Max error is one point)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0 + 0.9), (3.0, 3.0)],
        "epsilon": 1.0,
        "expected_pieces": 1,  # The noise point (0.9 error) is just within tolerance 1.0
        "description": "Single point of large noise, just within tolerance."
    },

    # 7. Zero Tolerance (Extreme Edge Case) - Should use maximum pieces (n)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 3,
        "description": "Zero tolerance (epsilon=0). Must use 3 pieces."
    },

    # 8. Infinite Tolerance (Extreme Edge Case) - Should use 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0)],
        "epsilon": 100.0,
        "expected_pieces": 1,
        "description": "Extremely high tolerance. Should be 1 piece."
    },

    # 9. Horizontal Line with Tiny Error - Tests alignment with the tolerance
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0.501), (3, 0), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2,  # Point at x=2 exceeds the envelope, forcing a split.
        "description": "Horizontal line where one point just exceeds epsilon (0.501 > 0.5)."
    },

    # 10. Horizontal Line with Error *Exactly* on Tolerance Boundary
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0.5), (3, 0), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 1,  # Point at x=2 is exactly on the envelope, so 1 piece is optimal.
        "description": "Horizontal line where one point is exactly on epsilon (0.5 = 0.5)."
    },

    # 11. Large Dataset, Simple Shape - Tests performance/scaling
    {
        "pw_linear_fx": [(i, i % 2) for i in range(101)],  # 100 segments
        "epsilon": 0.6,
        "expected_pieces_max": 51,
        # The line y=0.5 can approximate two points (i, 0) and (i+1, 1), requiring roughly N/2 pieces.
        "description": "Large oscillating dataset. Tests efficiency of segment combining."
    },

    # 12. Segment Start/End Points are the Max Error Points
    {
        "pw_linear_fx": [(0, 0), (1, 1.0), (2, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "description": "Error points at segment boundaries. A single piece (0,0) to (2,0) has error 1.0 > 0.5."
    },

    # 13. Data already in optimal two pieces
    {
        "pw_linear_fx": [(0, 0), (1, 0.4), (2, 0), (3, 0), (4, 0.4), (5, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2,  # (0,0)->(3,0) max error 0.4. (3,0)->(5,0) max error 0.4.
        "description": "Data already optimally split into two pieces."
    },

    # 14. Concave-up curve that requires many pieces
    {
        "pw_linear_fx": [(i, i ** 3) for i in range(11)],  # x^3 from 0 to 10
        "epsilon": 50.0,
        "expected_pieces_min": 2,  # Will require a split near the origin and then again later.
        "description": "Highly non-linear cubic curve."
    },

    # 15. Minimal data set (2 points) - Should use 1 piece regardless of epsilon
    {
        "pw_linear_fx": [(0.0, 10.0), (5.0, -5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1,
        "description": "Minimum data points (2 points, 1 piece)."
    },

    # 16. Minimal data set (3 points) - Max error is the middle point
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 2,  # Error is 1.0, requires 2 pieces
        "description": "3 points, max error in the middle, epsilon is just too small."
    },

    # 17. Constant Function (Should always be 1 piece if epsilon > 0)
    {
        "pw_linear_fx": [(i, 5.0) for i in range(10)],
        "epsilon": 0.001,
        "expected_pieces": 1,
        "description": "Constant function. Should be 1 piece."
    },

    # 18. Floating Point Precision Edge Case (small epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1e-7), (2.0, 0.0)],
        "epsilon": 1e-6,
        "expected_pieces": 1,  # Max error 1e-7 < 1e-6
        "description": "Very small epsilon, testing floating point stability."
    },

    # 19. Floating Point Precision Edge Case (error > epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1e-5), (2.0, 0.0)],
        "epsilon": 1e-6,
        "expected_pieces": 2,  # Max error 1e-5 > 1e-6, forcing a split
        "description": "Very small epsilon, error slightly exceeds, forcing 2 pieces."
    },

    # 20. Segment combination (4 points, optimal 2 pieces)
    {
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.0), (3, 2.0), (4, 1.9), (5, 2.0)],
        "epsilon": 0.2,
        "expected_pieces": 2,  # (0,0) to (2,0) is max error 0.1. (2,0) to (5,2) is approx. 2.0 max error 0.1.
        "description": "Two distinct low-error segments combined."
    }
]
test_cases17 = [
    # 1. Simple Straight Line (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.1,
        "description": "Perfect linear data, high tolerance. Should be 1 piece."
    },
    # 2. Perfect Fit (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.001,
        "description": "Perfect horizontal line, very low tolerance. Should be 1 piece."
    },
    # 3. Maximum Deviation = Epsilon (Boundary Condition) (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "description": "Triangle wave where max deviation is exactly epsilon. Should be 1 piece."
    },
    # 4. Maximum Deviation > Epsilon (Minimum 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        "epsilon": 0.5,
        "description": "Minimum 2 pieces needed due to a single large deviation."
    },
    # 5. Sawtooth Wave - Small Epsilon (Expected: n/2 pieces if deviation is 2*epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "description": "Highly oscillatory data, small epsilon. Tests if local minima are found correctly. Needs multiple pieces."
    },
    # 6. Sharp Turn - Needs two pieces immediately
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "description": "An acute angle. The segment (0, 2) has a deviation of 10. Needs two pieces."
    },
    # 7. Step Function Approximation (Expected: 2 pieces, end-to-end)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.1,
        "description": "Approximation of a step function. Should be (0, 2) and (2, 3) or similar split."
    },
    # 8. Quadratic Curve - Tests non-linear fit
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.01), (2.0, 0.04), (3.0, 0.09), (4.0, 0.16)],
        "epsilon": 0.05,
        "description": "Quadratic data, moderate epsilon. Checks if long segments are used."
    },
    # 9. Large, Complex Dataset with Local Maxima/Minima (Optimality Test)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.1), (4.0, 0.0), (5.0, 0.2), (6.0, 0.4), (7.0, 0.2), (8.0, 0.0)],
        "epsilon": 0.15,
        "description": "Two connected 'W' shapes. Should optimally fit the first W, then the second."
    },
    # 10. Zero Tolerance (Expected: n pieces, one for each segment)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.0,
        "description": "Zero tolerance forces every original segment to be a piece (n pieces)."
    },
    # 11. Infinite Tolerance (Expected: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 0.0), (3.0, 100.0)],
        "epsilon": 1000.0,
        "description": "Effectively infinite tolerance. Should be 1 piece, connecting first and last points."
    },
    # 12. Oscillating around a line (Boundary Case)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.05), (3.0, 0.05), (4.0, -0.05)],
        "epsilon": 0.05,
        "description": "Points oscillating with max deviation exactly epsilon."
    },
    # 13. Very Dense Data, Linear (Efficiency Test)
    {
        "pw_linear_fx": [(i, i * 0.1) for i in range(11)], # (0,0), (1, 0.1), ..., (10, 1.0)
        "epsilon": 0.5,
        "description": "Many points on a line, large tolerance. Should be 1 piece (testing efficiency/n-points)."
    },
    # 14. Very Dense Data, Non-Linear (Optimality on Long Segment)
    {
        "pw_linear_fx": [(i, 0.0) if i % 2 == 0 else (i, 0.01) for i in range(11)],
        "epsilon": 0.009,
        "description": "Oscillating slightly, epsilon just small enough to force multiple segments."
    },
    # 15. Negative Y-values and X-values
    {
        "pw_linear_fx": [(-2.0, -1.0), (-1.0, -0.9), (0.0, -1.0), (1.0, -0.9)],
        "epsilon": 0.05,
        "description": "Test with negative coordinates. Should fit in 1 piece."
    },
    # 16. Single point violation at the end of a potential segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0)],
        "epsilon": 0.5,
        "description": "Need one piece for (0, 3) and another for (3, 4)."
    },
    # 17. Single point violation at the start of a potential segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "description": "Need one piece for (0, 1) and another for (1, 4)."
    },
    # 18. Points on both sides of the approximation line (S-curve)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, -0.1), (4.0, 0.0)],
        "epsilon": 0.1,
        "description": "S-curve shape with max deviation exactly epsilon. Should be 1 piece."
    },
    # 19. Repeated Points (Degenerate Case)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.01,
        "description": "Test with duplicate points. Should still be 1 piece."
    },
    # 20. The Example Case from the Prompt
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "description": "User example. Needs 2 pieces (e.g., (0, 2) fails, so (0, 1) and (1, 5))."
    },
]
test_cases18 = [
    {
        "description": "1. Baseline: Perfect horizontal line (1 segment)",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1
    },
    {
        "description": "2. Baseline: Perfect diagonal line (1 segment)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },
    {
        "description": "3. Simple V-shape requiring 2 segments (low tolerance)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 2
    },
    {
        "description": "4. Prompt example forcing 3 segments due to high error at (1,1)",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3
    },
    {
        "description": "5. Single large deviation slightly exceeding epsilon (forces split)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.9,
        "expected_min_pieces": 3
    },
    {
        "description": "6. Boundary check: Max error exactly equals epsilon (1 segment)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 1
    },
    {
        "description": "7. Boundary check: Max error just exceeds epsilon (forces 2 segments)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.99,
        "expected_min_pieces": 2
    },
    {
        "description": "8. Testing optimality: Long almost-line with a bend (2 segments)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 3.0), (4.0, 3.1)],
        "epsilon": 0.2,
        "expected_min_pieces": 2
    },
    {
        "description": "9. High frequency low amplitude noise (1 segment)",
        "pw_linear_fx": [(i, 0.01 * ((-1)**i)) for i in range(10)],
        "epsilon": 0.011,
        "expected_min_pieces": 1
    },
    {
        "description": "10. Sharp jump, testing the latest possible split point (2 segments)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2
    },
    {
        "description": "11. Zig-zag pattern, tolerance allows optimal 2 segments",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 1.1,
        "expected_min_pieces": 2
    },
    {
        "description": "12. Minimum data points (2 points is 1 segment)",
        "pw_linear_fx": [(10.0, 5.0), (20.0, 10.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 1
    },
    {
        "description": "13. Zero epsilon (forces N-1 segments)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 4
    },
    {
        "description": "14. Very large epsilon (should always be 1 segment)",
        "pw_linear_fx": [(0.0, 100.0), (1.0, -50.0), (2.0, 200.0), (3.0, 0.0)],
        "epsilon": 500.0,
        "expected_min_pieces": 1
    },
    {
        "description": "15. Parabola (y=x^2) requiring 3 segments",
        "pw_linear_fx": [(i, i**2) for i in range(7)],
        "epsilon": 2.0,
        "expected_min_pieces": 3
    },
    {
        "description": "16. Points tightly clustered near optimal line (1 segment)",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.01), (1.0, 0.0), (1.5, -0.01), (2.0, 0.0)],
        "epsilon": 0.015,
        "expected_min_pieces": 1
    },
    {
        "description": "17. Stair-step function (forces split at every step change)",
        "pw_linear_fx": [(i, i // 2) for i in range(10)],
        "epsilon": 0.1,
        "expected_min_pieces": 9
    },
    {
        "description": "18. Alternating slopes, testing local optima (4 segments)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 4
    },
    {
        "description": "19. Wide x-range, narrow y-range (testing scale and 1 segment solution)",
        "pw_linear_fx": [(0.0, 1.0), (100.0, 1.05), (200.0, 1.1)],
        "epsilon": 0.06,
        "expected_min_pieces": 1
    },
    {
        "description": "20. A single outlier point forcing a split for an otherwise flat function (3 segments)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 3
    },
]
test_cases19 = [
    # 1. Baseline - Perfectly Linear (Optimal: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1
    },

    # 2. Perfectly Linear (Larger dataset, very strict tolerance)
    {
        "pw_linear_fx": [(i, i) for i in range(10)],
        "epsilon": 0.001,
        "expected_min_pieces": 1
    },

    # 3. Perfectly Horizontal (Should use 1 piece)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 1
    },

    # 4. Zero Tolerance (Must use n pieces / n+1 points)
    # 5 points, 4 segments.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 4
    },

    # 5. High Tolerance (Allowing large error, should use 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 5.1,
        "expected_min_pieces": 1
    },

    # 6. Minimal Non-linearity - Just Under Epsilon (Optimal: 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.49), (2.0, 0.0), (3.0, -0.49)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },

    # 7. Minimal Non-linearity - Just Over Epsilon (Forces 2 pieces)
    # (0,0) to (2,0) has max error at (1, 0.51). Must break.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },

    # 8. Step-like Function Approximation - Must Break
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 1.0), (2.0, 1.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2
    },

    # 9. Alternating Error - Pushing the Boundary (Optimal: 2 pieces)
    # (0,0) to (4,0) approximation. Max error is 1.0. Needs 2 pieces for epsilon 0.99.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.99,
        "expected_min_pieces": 2
    },

    # 10. Alternating Error - Boundary Case (Optimal: 1 piece)
    # Same as above, but epsilon 1.0 allows for 1 piece.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 1
    },

    # 11. Quadratic Function - Requires multiple breaks
    # y = x^2. Tolerance 0.2 requires 3 breaks for 5 points.
    {
        "pw_linear_fx": [(i, i * i) for i in range(5)],
        "epsilon": 0.2,
        "expected_min_pieces": 3
    },

    # 12. V-shape (Symmetric, Forces 2 pieces)
    # (0,0) to (2,0) approx. Max error is 1.0. Needs 2 pieces for epsilon 0.5.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },

    # 13. V-shape - Optimal: 1 piece (Boundary test)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 1
    },

    # 14. Dataset with repeated X-coordinates (Vertical segment handling)
    # Small epsilon forces a break around the vertical change.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.01,
        "expected_min_pieces": 2
    },

    # 15. Long Run with Small, Consistent Error (Test range extension)
    # The whole set (0,0) to (10,0) approx. Max error is 0.4. Can use 1 piece.
    {
        "pw_linear_fx": [(i, 0.0 if i % 2 == 0 else 0.4) for i in range(11)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },

    # 16. A Breakpoint that Just Misses the Next Point
    # The segment from (0,0) must end at (3, 0.5) to capture the boundary, forcing 2 pieces.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.5), (4.0, -0.5), (5.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },

    # 17. Extreme Steep Slope Change - Forces a break
    # Segment (0,0) to (10,0) approx. Max error at (5,50) is 50. Needs 2 pieces for epsilon 49.9.
    {
        "pw_linear_fx": [(0.0, 0.0), (5.0, 50.0), (10.0, 0.0)],
        "epsilon": 49.9,
        "expected_min_pieces": 2
    },

    # 18. Extreme Steep Slope Change - Boundary Pass
    {
        "pw_linear_fx": [(0.0, 0.0), (5.0, 50.0), (10.0, 0.0)],
        "epsilon": 50.0,
        "expected_min_pieces": 1
    },

    # 19. Two Distinct Flat Sections (Should use 2 pieces)
    # (0,0) to (4,0) and (5,10) to (9,10). The jump forces a break.
    {
        "pw_linear_fx": [(i, 0.0) for i in range(5)] + [(i, 10.0) for i in range(5, 10)],
        "epsilon": 1.0,
        "expected_min_pieces": 2
    },

    # 20. High-Frequency Oscillation (Needs many pieces)
    # Rapid oscillation with amplitude 1. Epsilon 0.1 forces a new segment almost every point.
    {
        "pw_linear_fx": [(i, (-1) ** i) for i in range(10)],  # Points: (0,1), (1,-1), (2,1), ...
        "epsilon": 0.1,
        "expected_min_pieces": 5
    }
]
test_cases20 = [
    # 1. Perfectly Linear Data (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "description": "Linear data, one piece should suffice for high tolerance."
    },

    # 2. Perfectly Linear Data, Tight Tolerance (Should still be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0001,
        "expected_pieces": 1,
        "description": "Linear data with very tight tolerance."
    },

    # 3. Two distinct linear segments, tight tolerance (Should be 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 2.0)],
        "epsilon": 0.001,
        "expected_pieces": 2,
        "description": "Two segments meeting at a sharp corner (2.0, 1.0)."
    },

    # 4. Two distinct linear segments, loose tolerance (Should be 1 piece if endpoints allow)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 2.0)],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "Two segments, large epsilon allows approximation with one piece (max error is 1.0)."
    },

    # 5. Sawtooth pattern (Many pieces needed)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4,  # Each V shape requires a separate piece for small epsilon
        "description": "Sawtooth pattern, requiring many pieces."
    },

    # 6. Step function (Minimum of 2 pieces for each step)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.9, 0.0), (1.0, 5.0), (2.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,  # A piece for the flat start, and a piece for the flat end.
        "description": "Large vertical jump (step function) at x=1.0."
    },

    # 7. Parabolic curve $y = x^2$ (Error grows quadratically, multiple pieces needed)
    {
        "pw_linear_fx": [(x, x ** 2) for x in [0.0, 1.0, 2.0, 3.0, 4.0]],
        "epsilon": 0.5,
        "expected_pieces": 2,
        # Points: (0,0), (1,1), (2,4), (3,9), (4,16). (0,0) to (2,4) has max error 1.0 (too large). (0,0) to (1,1) is ok. (1,1) to (4,16) is ok. Try (0,0) to (3,9): max error is 2.25. (0,0) to (2,4): max error is 1.0. Must break earlier. (0,0) to (1,1) is fine. (1,1) to (4,16) is fine.
        "description": "Concave curve $y=x^2$, challenging for error tolerance."
    },

    # 8. Parabolic curve $y = x^2$, tighter tolerance
    {
        "pw_linear_fx": [(x, x ** 2) for x in [0.0, 0.5, 1.0, 1.5, 2.0]],
        "epsilon": 0.05,
        "expected_pieces": 3,  # Requires more pieces for tighter fit.
        "description": "Concave curve $y=x^2$ with tighter tolerance."
    },

    # 9. Single point deviation (Should be 2 pieces if deviation > epsilon, or 1 piece if <= epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.5, 0.6), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,  # Max error is 0.6 at (1.5, 0.6). 0.6 is > 0.5. So 2 pieces.
        "description": "Single point spike/dip, where max error is slightly greater than epsilon."
    },

    # 10. Single point deviation where max error = epsilon (Crucial boundary check)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.5, 0.5), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,
        # If the error is exactly epsilon, it *must* fail if the point is interior, requiring a break.
        "description": "Single point spike/dip where max error is exactly epsilon."
    },

    # 11. Single point deviation where max error < epsilon (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.5, 0.49), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "description": "Single point spike/dip where max error is slightly less than epsilon."
    },

    # 12. Constant function, small deviation (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.01), (2.0, 4.99), (3.0, 5.0)],
        "epsilon": 0.02,
        "expected_pieces": 1,
        "description": "Data points close to a horizontal line."
    },

    # 13. High-frequency noise on a straight line
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.1), (4.0, -0.1), (5.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 5,  # Requires many small pieces if noise exceeds tolerance
        "description": "High-frequency oscillation around a straight line."
    },

    # 14. Data with only 2 points (Trivial case, must be 1 piece)
    {
        "pw_linear_fx": [(0.0, 1.0), (5.0, 10.0)],
        "epsilon": 100.0,
        "expected_pieces": 1,
        "description": "Minimum number of points (2), must return 1 piece."
    },

    # 15. Data with 3 points that are co-linear (Should be 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.001,
        "expected_pieces": 1,
        "description": "3 co-linear points."
    },

    # 16. Data with 3 points that are NOT co-linear (Should be 2 pieces if tight epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.01,
        "expected_pieces": 2,
        "description": "A 'V' shape, tight epsilon requires 2 pieces."
    },

    # 17. Extreme epsilon (Should force 1 piece regardless of data shape)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 0.0), (3.0, 100.0)],
        "epsilon": 200.0,
        "expected_pieces": 1,
        "description": "Extremely loose epsilon, should always result in 1 piece."
    },

    # 18. Zero epsilon (Should force N-1 pieces for N points, unless co-linear)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 3,  # N=4 points, must use N-1=3 pieces.
        "description": "Zero epsilon, forcing interpolation through every point."
    },

    # 19. Repeated points (Should be handled gracefully, likely ignored or treated as a single point in the approximation)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.01,
        "expected_pieces": 1,
        "description": "Repeated identical points, should simplify to 1 piece."
    },

    # 20. Non-uniform x-spacing
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.5), (1.0, 0.0), (10.0, 0.0)],
        "epsilon": 0.4,
        "expected_pieces": 2,
        # (0.0, 0.0) to (1.0, 0.0) has max error 0.5 > 0.4. Needs to break. (0.0, 0.0) to (0.1, 0.5) is 1st piece. (0.1, 0.5) to (10.0, 0.0) is 2nd.
        "description": "Extreme non-uniform x-spacing with an initial spike."
    },
]
test_cases21 = [
    # 1. Basic Monotonic (Expected: Greedy optimal)
    {
        "name": "Basic Monotonic Ramp",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_n_pieces": 4  # All points must be connected (N+1 points = N pieces)
    },

    # 2. Perfect Linear Fit (Expected: 1 piece)
    {
        "name": "Perfect Linear Fit",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 4.0), (4.0, 8.0), (6.0, 12.0)],
        "epsilon": 0.1,
        "expected_n_pieces": 1  # All points lie on a single line y=2x.
    },

    # 3. Step Function (Small epsilon) (Expected: N pieces - no compression)
    {
        "name": "Sharp Step Function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 10.0), (2.0, 10.0)],
        "epsilon": 0.5,
        "expected_n_pieces": 3  # The sharp vertical jump needs its own segment.
    },

    # 4. Large Tolerance - Single Piece Allowed
    {
        "name": "High Tolerance Fit",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 0.0)],
        "epsilon": 1.0,
        "expected_n_pieces": 1  # Max deviation is 1.0 at (2.0, -1.0) using the line y=0.
    },

    # 5. Greedy Fail Potential (Example from literature - A smaller max segment allows more total compression)
    {
        "name": "Greedy Non-Optimal Trap",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0), (5.0, 1.0), (6.0, 0.0),
                         (7.0, 0.0)],
        "epsilon": 0.6,
        "expected_n_pieces": 2
        # Optimal can skip (2,1) and (5,1) with two large segments (0,0)->(7,0). A greedy choice (0,0)->(3,0) might use 3 pieces.
    },

    # 6. Sharp Peak / V-Shape (Needs 2 pieces minimum)
    {
        "name": "V-Shape Peak",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 4.0,
        "expected_n_pieces": 2
        # The peak at (1, 10) is too high for a single segment (0,0)->(2,0) which has an error of 5.0.
    },

    # 7. Horizontal Line with Single Outlier (Needs 2 pieces)
    {
        "name": "Single Outlier Point",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_n_pieces": 3
        # Points (0,0)->(2,1) needs 2 segments. (2,1)->(4,0) needs 2 segments. Total 3 segments minimum (e.g., (0,0)->(1,0), (1,0)->(3,0), (3,0)->(4,0)).
    },

    # 8. All Zeros / Coincident Points (Expected: 1 piece)
    {
        "name": "All Coincident Points",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.001,
        "expected_n_pieces": 1
    },

    # 9. Small Epsilon on a Curve (Forces N pieces)
    {
        "name": "Small Epsilon on Sine Wave",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (1.0, 0.0), (1.5, -0.1), (2.0, 0.0)],
        "epsilon": 0.01,
        "expected_n_pieces": 4  # The error will exceed 0.01 on any segment longer than 1 point.
    },

    # 10. Floating Point Data and Tolerance Edge
    {
        "name": "Float Edge Case (Tolerance met exactly)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.25,
        "expected_n_pieces": 1
        # Line (0,0)->(2,0) has max error of 0.5 at x=1. Line (0,0)->(2,0) has max error of 0.5 at x=1. If we choose a line through (0,0) and (2,0), the error is $0.5$. With an epsilon of 0.25, 2 pieces are needed. Let's adjust this for 1 piece.
    },

    # 11. Concave/Convex alternating
    {
        "name": "Concave/Convex Alternating",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.4,
        "expected_n_pieces": 2
        # A single line (0,0)->(3,1) has error of $\approx 0.66$ at x=1 and x=2. Need 2 segments minimum.
    },

    # 12. Non-uniformly spaced X (Checks line calculation dependency on X)
    {
        "name": "Non-Uniform X-Spacing",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.5), (10.0, 0.0)],
        "epsilon": 0.49,
        "expected_n_pieces": 2  # Single segment (0,0)->(10,0) has error 0.5 at x=0.1.
    },

    # 13. Horizontal Compression Test
    {
        "name": "Horizontal Compression Test",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (20.0, 0.1), (30.0, 0.0)],
        "epsilon": 0.09,
        "expected_n_pieces": 3
        # (0,0)->(30,0) has error 0.1 > 0.09. Need 3 pieces. (0,0)->(20,0.1) has max error 0.1. (0,0)->(10,0) (10,0)->(30,0) fails.
    },

    # 14. Minimum Two Pieces Required (High error in middle)
    {
        "name": "Minimum Two Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0), (4.0, 0.0)],
        "epsilon": 5.0,
        "expected_n_pieces": 2  # Optimal can be (0,0)->(2,0) and (2,0)->(4,0) with max error 5.0.
    },

    # 15. All points are the same (Expected: 1 piece)
    {
        "name": "All Identical Points",
        "pw_linear_fx": [(1.0, 2.0), (1.0, 2.0), (1.0, 2.0), (1.0, 2.0)],
        "epsilon": 0.01,
        "expected_n_pieces": 1
        # Note: A robust algorithm should handle this degeneracy or pre-filter. If treated literally, 1 piece.
    },

    # 16. Negative Y values
    {
        "name": "Negative Y Values",
        "pw_linear_fx": [(0.0, -1.0), (1.0, 0.0), (2.0, -1.0)],
        "epsilon": 0.4,
        "expected_n_pieces": 2  # (0,-1)->(2,-1) has error 1.0. Needs 2 segments.
    },

    # 17. Zig-Zag that allows high compression
    {
        "name": "Compressible Zig-Zag",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, 0.0), (3.0, -0.2), (4.0, 0.0)],
        "epsilon": 0.2,
        "expected_n_pieces": 1  # Line (0,0)->(4,0) has max error of exactly 0.2.
    },

    # 18. Zero Tolerance on Non-Linear Data (Forces N pieces)
    {
        "name": "Zero Tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0)],
        "epsilon": 0.0,
        "expected_n_pieces": 2
    },

    # 19. Long Sequence with Minor Deviation (Testing span/range of algorithm)
    {
        "name": "Long Sequence Minor Dev",
        "pw_linear_fx": [(i, 0.0 if i % 10 != 5 else 0.001) for i in range(21)],
        "epsilon": 0.0001,
        "expected_n_pieces": 20  # Requires all original segments since error is 0.001 > 0.0001
    },

    # 20. The "Optimal is Not Greedy" Classic Setup
    # An optimal solution might choose a segment that is slightly shorter than the maximum possible but results in a better fit for the subsequent points.
    {
        "name": "Classic Greedy Fail",
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0.8), (3, 0.8), (4, 0), (5, 0)],
        "epsilon": 0.2,
        "expected_n_pieces": 3
    }
]
test_cases22 = [
    # 1. Basic Cases & Uniform Data
    {
        "description": "Perfectly flat line, large epsilon. Expect 1 piece.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Perfectly flat line, epsilon=0. Expect 4 pieces (n-1).",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    {
        "description": "Perfectly linear slope, large epsilon. Expect 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (4.0, 8.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },

    # 2. Tolerance Boundary Testing
    {
        "description": "Single point slightly above a line segment. Requires 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.0, # All points on the line, but epsilon is 0
        "expected_pieces": 5 # Must use one segment per point, min_points = 2 -> n-1 pieces
    },
    {
        "description": "Minimum deviation to force a split. Requires 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.99, # Can cover (0,0) to (4,0) with one line if 1.0 tolerance
        "expected_pieces": 2 # Should fail the single segment test, splitting at (2, 1.0)
    },
    {
        "description": "Deviation exactly equals epsilon. Should be 1 piece (<=).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Deviation slightly exceeds epsilon. Requires 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.999,
        "expected_pieces": 2
    },

    # 3. Shape Tests: Sharp Corners & V-Shapes
    {
        "description": "A sharp 'V' shape requiring 2 pieces for any small epsilon.",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 0.0), (2.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "A 'W' shape, forces 4 pieces for small epsilon.",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 0.0), (2.0, 10.0), (3.0, 0.0), (4.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    {
        "description": "A 'W' shape, very large epsilon. Expect 1 piece.",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 0.0), (2.0, 10.0), (3.0, 0.0), (4.0, 10.0)],
        "epsilon": 10.0,
        "expected_pieces": 1
    },

    # 4. Curvature Tests (Non-linear data)
    {
        "description": "Parabola (y=x^2). Small epsilon requires multiple pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,0) to (3,9) has max error 1.0 at x=2. Need 0.5 error.
                            # (0,0) to (2,4) has error 1.0 at x=1. Need 0.5 error.
                            # Optimal split: [(0,0), (1,1), (4,16)] -> 2 pieces.
    },
    {
        "description": "Parabola (y=x^2). Smaller epsilon forces more pieces.",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 3 # Estimated
    },
    {
        "description": "Sine wave-like data, forces segmentation.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    {
        "description": "Sine wave-like data, large epsilon. Expect 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 1.1,
        "expected_pieces": 1
    },

    # 5. Greedy vs. Optimal Test Cases
    # These cases distinguish between a simple greedy algorithm (e.g., Ramer–Douglas–Peucker)
    # and a provably optimal algorithm (e.g., Dynamic Programming).
    {
        "description": "Greedy trap 1: A long, shallow segment followed by a sharp turn. Optimal algorithms look ahead.",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 0.0), (5.1, 10.0), (10.0, 10.0)],
        "epsilon": 0.01,
        "expected_pieces": 2 # (0,0) to (5,0) and (5.1, 10.0) to (10.0, 10.0)
    },
    {
        "description": "Greedy trap 2: An early split is forced, but a later longer segment could be covered.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.5), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.4,
        "expected_pieces": 2 # Optimal: (0,0) to (3,0) and (3,0) to (5,0). Greedy might split at (2,0.5).
    },

    # 6. Minimal Data & Edge Coordinates
    {
        "description": "Minimal data (2 points). Expect 1 piece.",
        "pw_linear_fx": [(1.0, 1.0), (2.0, 2.0)],
        "epsilon": 10.0,
        "expected_pieces": 1
    },
    {
        "description": "Minimal data (3 points). Should always be 1 piece if epsilon is large.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 10.0,
        "expected_pieces": 1
    },
    {
        "description": "Negative coordinates and float epsilon.",
        "pw_linear_fx": [(-5.0, 1.0), (-2.5, 0.0), (0.0, 1.0), (2.5, 0.0), (5.0, 1.0)],
        "epsilon": 0.15,
        "expected_pieces": 4 # A series of 'W' points, requires 4 segments for small epsilon.
    },
    {
        "description": "Non-monotonic X coordinates (Should not happen but tests robustness of data parsing).",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (1.0, 10.0), (3.0, 3.0)],
        "epsilon": 5.0,
        "expected_pieces": 2 # Assuming the algorithm internally sorts or handles this by connecting the given points sequentially.
    }
]
test_cases23 = [
    # 1. Basic Convex Function (Should require 2 pieces if epsilon is small enough, 1 if large)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,  # Should ideally use (0,0)-(2,1) and (2,1)-(4,0)
        "description": "Convex shape, moderate epsilon. Tests two-piece optimality."
    },
    # 2. Straight Line (Must be 1 piece, regardless of epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01,
        "expected_pieces": 1,
        "description": "Perfect straight line. Must be 1 piece."
    },
    # 3. Constant Function (Must be 1 piece)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.001,
        "expected_pieces": 1,
        "description": "Perfect constant line. Must be 1 piece."
    },
    # 4. Zero Tolerance ($\varepsilon=0$) - Each segment is a piece
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.0,
        "expected_pieces": 2, # n+1 points -> n segments/pieces
        "description": "Zero epsilon, non-linear. Should result in max pieces (n segments)."
    },
    # 5. Very Large Tolerance ($\varepsilon$ allows 1 piece for non-linear data)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 5.0,
        "expected_pieces": 1,
        "description": "Very large epsilon. Should be approximated by 1 piece."
    },
    # 6. Sharp Turn (Requires 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0001, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        "description": "Very sharp turn close to (1.0, 1.0). Requires 2 pieces."
    },
    # 7. Step Function (Staircase - Requires 3 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.01,
        "expected_pieces": 3,
        "description": "Staircase function. Tests vertical segments implicitly."
    },
    # 8. Single Segment Approximation Failure (Need 2 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 0.0)],
        "epsilon": 0.2,
        "expected_pieces": 2, # Max error is 0.25 on single piece (0,0)-(1,0). Epsilon is 0.2
        "description": "Non-linear data, single piece error exceeds epsilon."
    },
    # 9. Minimal Data Set (Two points, always 1 piece)
    {
        "pw_linear_fx": [(1.0, 5.0), (5.0, 1.0)],
        "epsilon": 10.0,
        "expected_pieces": 1,
        "description": "Minimal dataset (2 points). Must be 1 piece."
    },
    # 10. Minimal Data Set (Three points, non-collinear, always 2 pieces if epsilon=0)
    {
        "pw_linear_fx": [(1.0, 1.0), (2.0, 5.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 2,
        "description": "Three points, epsilon=0. Should be 2 pieces."
    },
    # 11. Noise on a Line (1 piece should be enough)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.05), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "description": "Small noise on a constant line, large enough epsilon."
    },
    # 12. Noise on a Line (Epsilon too small, requires multiple pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.05), (3.0, 0.0)],
        "epsilon": 0.04,
        "expected_pieces": 2, # Single piece approx error is 0.05. Need 2 pieces.
        "description": "Small noise, very small epsilon. Requires multiple pieces."
    },
    # 13. High-Frequency Oscillation (Requires many pieces)
    {
        "pw_linear_fx": [(i, (-1)**i * 0.5) for i in range(11)],
        "epsilon": 0.1,
        "expected_pieces": 10, # Max pieces (11 points = 10 segments)
        "description": "High-frequency, high-amplitude oscillation. Requires max pieces."
    },
    # 14. Gradual Curve (Optimality test for greedy approaches)
    {
        "pw_linear_fx": [(i, i**2) for i in range(5)], # (0,0), (1,1), (2,4), (3,9), (4,16)
        "epsilon": 1.0,
        "expected_pieces": 3, # (0,0)-(2,4) has max error 1. (2,4)-(4,16) max error 4. (0,0)-(1,1)-(2,4), (2,4)-(3,9), (3,9)-(4,16)
        "description": "Parabola, moderate epsilon. Test for 3-piece optimality."
    },
    # 15. Near-Vertical/Steep Slope (Ensure approximation handles steepness)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.001, 10.0), (1.0, 10.001)],
        "epsilon": 0.1,
        "expected_pieces": 2,
        "description": "Very steep initial slope. Tests robustness near vertical."
    },
    # 16. Identical Points (Should be treated as a single point, but depends on implementation)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.01,
        "expected_pieces": 2, # If algorithm skips duplicates, otherwise 3 max segments.
        "description": "Dataset with duplicate points. Test for duplicate handling."
    },
    # 17. Zig-Zag, 3 Points Per Piece (Tests multi-point piece fitting)
    {
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0), (3, 1), (4, 1.5), (5, 1)],
        "epsilon": 0.51, # Max error for the first zig-zag (0, 0.5, 0) is 0.25 (line 0-2).
        "expected_pieces": 2, # (0,0)-(2,0) max error 0.5. (2,0)-(5,1) max error 0.5. Total 2 pieces.
        "description": "Zig-zag pattern, large epsilon allows 2 pieces."
    },
    # 18. Zig-Zag, Must use 3 pieces (Epsilon slightly too small)
    {
        "pw_linear_fx": [(0, 0), (1, 0.5), (2, 0), (3, 1), (4, 1.5), (5, 1)],
        "epsilon": 0.49,
        "expected_pieces": 3, # Single piece cannot cover (0,0)-(2,0)
        "description": "Zig-zag pattern, small epsilon forces 3 pieces."
    },
    # 19. Long Constant/Flat Section followed by a sharp change
    {
        "pw_linear_fx": [(i, 1.0) for i in range(5)] + [(6.0, 10.0)],
        "epsilon": 0.01,
        "expected_pieces": 2, # (0,1) to (4,1) is 1 piece. (4,1) to (6,10) is 1 piece.
        "description": "Long flat section followed by a sharp jump."
    },
    # 20. Non-Uniform X-Spacing (Ensure error calculation is based on Y-deviation)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (10.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2, # Max error is 0.9 on single piece (0,0)-(10,0). Need 2 pieces.
        "description": "Non-uniform x-spacing, non-linear data. Requires 2 pieces."
    },
]
test_cases24 = [
    # Category 1: Basic & Trivial Cases (Establishing Baseline)
    {
        "description": "Trivial: All points are collinear (y=x). Should require 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1
    },
    {
        "description": "Trivial: All points within tolerance of the first point (y=0). Should require 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, -0.05), (3.0, 0.1)],
        "epsilon": 0.2,
        "expected_min_pieces": 1
    },
    {
        "description": "Step function: Large gap, forcing multiple pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },
    {
        "description": "Maximum tolerance: Should always require 1 piece if tolerance is >= half the total y-range.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -5.0), (3.0, 0.0)],
        "epsilon": 5.0,
        "expected_min_pieces": 1
    },

    # Category 2: Boundary/Exact Tolerance Edge Cases (Testing optimality)
    {
        "description": "Boundary Case 1: Point exactly at epsilon threshold, forcing the segment to end.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },
    {
        "description": "Boundary Case 2: Point just *under* epsilon threshold, allowing 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.49), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },
    {
        "description": "Boundary Case 3: Point just *over* epsilon threshold, forcing 2 pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.51), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },
    {
        "description": "Symmetry Test: Alternating points exactly on the boundary, requiring multiple pieces.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, -1.0), (5.0, 0.0)],
        "epsilon": 1.0,  # The approximation should pass through (0,0) and (3,0). It hits 1.0 at x=2 and -1.0 at x=4.
        "expected_min_pieces": 2  # (0,0) to (3,0) fits 0, 1, 2. (3,0) to (5,0) fits 4.
    },

    # Category 3: High Frequency/Oscillation (Testing rapid change detection)
    {
        "description": "High Frequency/Sine-like: Rapid, small oscillations, should require many pieces.",
        "pw_linear_fx": [(i, 0.5 * (1 if i % 2 == 0 else -1)) for i in range(11)],
        "epsilon": 0.1,
        "expected_min_pieces": 5  # Each oscillation is 1.0 peak-to-peak. Must split every 2-3 points.
    },
    {
        "description": "High Frequency, Tight Tolerance: Forces every two points to be a piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.49,
        "expected_min_pieces": 5  # Must fit [(0,0),(1,1)], [(1,1),(2,0)], etc.
    },

    # Category 4: Varying Slopes and Long/Short Segments
    {
        "description": "Long near-linear run followed by a sharp turn.",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 0.1), (10.0, 0.2), (10.1, 5.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },
    {
        "description": "Sharp initial slope, then a flat section.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 10.1), (5.0, 10.2)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },
    {
        "description": "Convex curve (Parabola y=x^2) requiring multiple splits.",
        "pw_linear_fx": [(i, i ** 2) for i in range(6)],  # Points: (0,0), (1,1), (2,4), (3,9), (4,16), (5,25)
        "epsilon": 1.0,
        "expected_min_pieces": 4  # Example fit: [(0,0),(2,4)], [(2,4),(3,9)], [(3,9),(4,16)], [(4,16),(5,25)]
    },
    {
        "description": "Concave curve (Square root y=sqrt(x)) requiring more pieces at the start.",
        "pw_linear_fx": [(i, i ** 0.5) for i in range(10)],  # Points: (0,0), (1,1), (2,1.41), (3,1.73), (9,3)
        "epsilon": 0.1,
        "expected_min_pieces": 5
    },

    # Category 5: End-Point Sensitivity (Testing start/end of approximation)
    {
        "description": "Minimum pieces requires a segment *not* starting/ending at the local min/max.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
        # Segment (0,0) to (4,0) has max error of 1.0. (0,0) to (2,1) works. (2,1) to (4,0) works.
    },
    {
        "description": "Only the very last point forces a split.",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 0.1), (10.0, 0.2), (10.5, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },

    # Category 6: Floating Point Precision / Zero Epsilon
    {
        "description": "Zero tolerance (Exact fit): Should always require n pieces for n+1 points unless collinear.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 2.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 3
    },
    {
        "description": "Zero tolerance (Exact fit) for collinear data: Should require 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 1
    },
    {
        "description": "Small epsilon, non-integer coordinates: Requires precision in L-inf calculation.",
        "pw_linear_fx": [(0.5, 1.1), (1.5, 1.2), (2.5, 1.0), (3.5, 1.3)],
        "epsilon": 0.05,
        "expected_min_pieces": 3  # (0.5, 1.1) to (1.5, 1.2) fails to include (2.5, 1.0).
    },
    {
        "description": "Example from prompt (Sanity check)",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3  # (0,1) to (1,1) is 1 piece. (1,1) to (2,3) fails on x=2. (2,3) to (5,8) fails on x=2.
    }
]
test_cases25 = [
    # 1. Basic Convex Function (Should require 2 pieces for small epsilon)
    {
        "description": "Simple quadratic-like curve, moderate error. Tests general performance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
        "epsilon": 0.01,
        "expected_pieces_min": 2  # (0.0, 0.0) -> (2.0, 0.4) and (2.0, 0.4) -> (4.0, 1.6) roughly
    },
    # 2. Perfectly Linear Data (Must return 1 piece for any epsilon > 0)
    {
        "description": "Perfectly linear data. Must return 1 piece (the original segment).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.001,
        "expected_pieces_min": 1
    },
    # 3. Perfectly Linear Data with Epsilon = 0 (Must return n pieces)
    {
        "description": "Perfectly linear data with epsilon = 0. Requires preserving all original points.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_pieces_min": 4
    },
    # 4. Constant Function (Must return 1 piece)
    {
        "description": "Data is a constant line. Must return 1 piece.",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces_min": 1
    },
    # 5. Steep Change / Corner Case 1 (Should require a split near the corner)
    {
        "description": "Sharp V-shape corner, small epsilon forces a split at (2.0, 0.0).",
        "pw_linear_fx": [(0.0, 2.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 2.0)],
        "epsilon": 0.1,
        "expected_pieces_min": 2
    },
    # 6. Corner Case 2 (Large epsilon allows the corner to be covered in 1 piece)
    {
        "description": "Same V-shape, large epsilon allows 1 piece.",
        "pw_linear_fx": [(0.0, 2.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 2.0)],
        "epsilon": 1.5,
        "expected_pieces_min": 1
    },
    # 7. Step Function (Requires splits at both steps)
    {
        "description": "Approximating a step function (discontinuous-like shape). Forces multiple pieces.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.001, 5.0), (2.0, 5.0), (2.001, 1.0), (3.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces_min": 4 # A piece for each near-vertical segment
    },
    # 8. Sinusoidal Curve - Max Error Check (Small epsilon should require many pieces)
    {
        "description": "Sinusoidal data. Very small epsilon tests maximum local error tolerance.",
        "pw_linear_fx": [(i, 5.0 * (1 - (i % 4) / 4.0)) for i in range(11)], # Sawtooth-like
        "epsilon": 0.1,
        "expected_pieces_min": 5 # Should split roughly every 2 segments
    },
    # 9. Sinusoidal Curve - Over-Tolerance (Large epsilon should allow 1 piece)
    {
        "description": "Sinusoidal data. Large epsilon should allow 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)],
        "epsilon": 1.1,
        "expected_pieces_min": 1
    },
    # 10. Data Points Barely Outside Epsilon (Critical Point)
    {
        "description": "One point is barely outside the tolerance of a single piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, -0.4), (4.0, 0.0)],
        "epsilon": 0.4,
        "expected_pieces_min": 2 # Error at x=1 and x=3 is exactly 0.4. Should fail to cover (0,4) with 1 piece if endpoints are (0,0) and (4,0)
    },
    # 11. Data Points Barely Inside Epsilon (Critical Point)
    {
        "description": "One point is barely inside the tolerance of a single piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.399), (2.0, 0.0), (3.0, -0.399), (4.0, 0.0)],
        "epsilon": 0.4,
        "expected_pieces_min": 1 # Should pass with 1 piece if error is < 0.4
    },
    # 12. Multiple Segments of Varying Difficulty (Tests greedy vs optimal)
    {
        "description": "Initial segment is easy (linear), followed by a difficult curve.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 2.5), (4.0, 2.8), (5.0, 3.0)],
        "epsilon": 0.05,
        "expected_pieces_min": 3 # (0,0) to (2,2) -> linear, then splits needed for the curve
    },
    # 13. Back-and-Forth Oscillations (Maximum error points alternating side of line)
    {
        "description": "Oscillating data, max error points alternate sides of the segment.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.5), (4.0, -0.5), (5.0, 0.0)],
        "epsilon": 0.4,
        "expected_pieces_min": 2 # Should require 2 pieces
    },
    # 14. Short, Sharp Deviation
    {
        "description": "A single point is a significant outlier.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.01, 10.0), (2.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces_min": 2 # (0,0) to (1.01, 10.0) -> (2.0, 0.0) or similar
    },
    # 15. Exponential-like Growth (Error increases rapidly)
    {
        "description": "Exponential growth - error accumulates quickly, forcing early splits.",
        "pw_linear_fx": [(i, 2**i) for i in range(5)], # (0,1), (1,2), (2,4), (3,8), (4,16)
        "epsilon": 1.0,
        "expected_pieces_min": 3 # Roughly (0,1)->(2,4) and then more splits
    },
    # 16. Identical Points (Zero length segment)
    {
        "description": "Two adjacent identical points (zero-length segment). Must handle gracefully.",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.1,
        "expected_pieces_min": 2 # Should treat the (1.0, 2.0) to (1.0, 2.0) as a single point
    },
    # 17. Extreme Slopes (Large Y-range, small X-range)
    {
        "description": "Data with extreme slopes/large y-range.",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 100.0), (0.2, 0.0)],
        "epsilon": 10.0,
        "expected_pieces_min": 1
    },
    # 18. Boundary Case - Error exactly Epsilon at all points in a segment
    {
        "description": "Error exactly at epsilon for all intermediate points in a potential segment. Must fail (L-inf strict inequality on non-endpoints).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces_min": 3 # The middle points (1, 0.1), (2, 0.2), (3, 0.1) have max error 0.1 vs line (0,0) to (4,0). A split is needed.
    },
    # 19. Boundary Case - Error slightly less than Epsilon
    {
        "description": "Error slightly less than epsilon for all intermediate points. Must pass.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.099), (2.0, 0.0), (3.0, -0.099), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces_min": 1
    },
    # 20. Long series of nearly linear data points
    {
        "description": "A long sequence of points that are nearly linear, testing the algorithm's greedy step size.",
        "pw_linear_fx": [(i, 1.0 + i * 0.001) for i in range(100)],
        "epsilon": 0.01,
        "expected_pieces_min": 1
    },
]
test_cases26 = [
    # 1. Perfectly Linear, 1 Piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 1.0
    },
    # 2. Perfectly Linear, Tight Fit (Expected 1 piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01
    },
    # 3. Small Deviation, Still 1 Piece (Line from (0,0) to (3, 0.08) has max error < 0.1)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.02), (3.0, 0.08)],
        "epsilon": 0.1
    },
    # 4. Just Exceeds epsilon, Forces 2 Pieces. Error at (1, 0.51) is 0.51 for line (0,0)-(2,0).
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        "epsilon": 0.5
    },
    # 5. Alternating Deviation. Forces 3 pieces (0.4 epsilon).
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.4
    },
    # 6. "Sawtooth" Pattern, Maximum Pieces (Almost zero error tolerance)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.01
    },
    # 7. Step Function/Vertical Jumps. Must break due to vertical displacement.
    {
        "pw_linear_fx": [(0.0, 0.0), (0.01, 1.0), (1.0, 1.0), (1.01, 0.0)],
        "epsilon": 0.1
    },
    # 8. Exponential/Curve (Concave Up). Line (0,0)-(4,16) error at (2,4) is 4. > 1.0.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0
    },
    # 9. High Density, Small epsilon (forces frequent breaks for a quadratic curve)
    {
        "pw_linear_fx": [(float(i), float(i**2)) for i in range(10)],
        "epsilon": 0.5
    },
    # 10. Horizontal Line Segment (Trivial case, expected 1 piece)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.0
    },
    # 11. Points on Boundary (Upper epsilon - testing inclusivity of bounds)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 0.5
    },
    # 12. Points on Boundary (Lower epsilon - testing inclusivity of bounds)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5), (4.0, 1.0)],
        "epsilon": 0.5
    },
    # 13. Two Distinct Lines (Sharp Corner, forces break)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.1
    },
    # 14. Minimal Set (3 Points, Max Deviation for 1 Piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5
    },
    # 15. Minimal Set (3 Points, Just Forces 2)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        "epsilon": 0.5
    },
    # 16. Points Clustered Near Start (Challenges look-ahead for optimal segment length)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.01), (0.2, 0.0), (5.0, 5.0)],
        "epsilon": 0.1
    },
    # 17. Points Clustered Near End (Similar to 16, testing greedy vs optimal choice)
    {
        "pw_linear_fx": [(0.0, 0.0), (4.8, 4.9), (4.9, 5.01), (5.0, 5.0)],
        "epsilon": 0.1
    },
    # 18. Zero Epsilon ($\varepsilon=0$) (Forces one segment per original piece, i.e., n points $\rightarrow$ n-1 pieces)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0
    },
    # 19. Large Epsilon (Always 1 Piece, even for extreme data)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 0.0)],
        "epsilon": 50.0
    },
    # 20. Example from Prompt (A complex slope change)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    }
]
test_cases27 = [
    # 1. Base Case: Minimum two points (one segment).
    {
        "name": "Single Segment - Trivial",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,  # (0,0) to (1,1) is one piece
    },

    # 2. Perfect Line: All points are collinear (should be 1 piece regardless of epsilon > 0).
    {
        "name": "Perfect Collinearity",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.001,
        "expected_pieces": 1,
    },

    # 3. Large Epsilon: Epsilon exceeds max deviation from endpoints (should be 1 piece).
    # Max deviation for this set is at (2.0, 0.0) with deviation of 1.0 from the line (0,1) to (4,-1).
    {
        "name": "Tolerance Covers All (Single Piece)",
        "pw_linear_fx": [(0.0, 1.0), (2.0, 0.0), (4.0, -1.0)],
        "epsilon": 1.0,
        "expected_pieces": 1,
    },

    # 4. Zero Epsilon: Requires a piece for every adjacent pair (n data points -> n-1 pieces).
    {
        "name": "Zero Tolerance (Max Pieces)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.4)],
        "epsilon": 0.0,
        "expected_pieces": 4,  # 5 points -> 4 pieces
    },

    # 5. Sawtooth Pattern: Requires a new piece at every peak/trough (2 pieces per cycle).
    # Deviation at peaks is 0.5. Epsilon slightly less than 0.5 forces 3 pieces.
    {
        "name": "Sawtooth Pattern (Forces Breaks)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 4,  # Break at (1.0, 0.5), (2.0, 0.0), (3.0, 0.5)
    },

    # 6. Sharp Angle (Corner Case): A single point widely off the line between its neighbors.
    # Deviation of (1, 1.0) from line (0,0) to (2,0) is 1.0. Epsilon=0.99 forces a break.
    {
        "name": "Single Outlier Point (Sharp Turn)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.99,
        "expected_pieces": 2,  # [(0,0) to (1,1)] and [(1,1) to (4,0)] or [(0,0) to (2,0)] -> WRONG!
        # The optimal path is (0,0) to (1,1) (or (2,0)) and then the rest. Optimal is (0,0) to (2,0) fails.
        # Optimal is: [(0,0) to (1,1)] then [(1,1) to (4,0)]. This is 2 pieces.
    },

    # 7. Step Function Approximation: Testing vertical changes.
    {
        "name": "Step Function Approximation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 1.0), (2.0, 1.0)],
        "epsilon": 0.49,
        "expected_pieces": 2,  # Must break at the step change (1.0, 0.0) to (1.0001, 1.0)
    },

    # 8. Optimal Merge (Greedy Failure Example): A case where a non-greedy choice leads to optimality.
    # The segment (0,0) to (2,0) has max deviation 1.0 at (1,1). Epsilon=1.0 allows it.
    # The segment (0,0) to (3,1) has max deviation > 1.0. Must break at 2.
    {
        "name": "Greedy Non-Optimal (Optimal 2 pieces)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 1.0,
        "expected_pieces": 2,  # (0,0) to (2,0) is valid. Then (2,0) to (3,1) is valid.
    },

    # 9. Minimal Data, Strict Epsilon: Only 3 points, forces two pieces.
    {
        "name": "Three Points, Strict Two Pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 2,  # Deviation from (0,0) to (2,0) is 1.0 at (1,1).
    },

    # 10. Floating Point Precision Test: Coordinates near epsilon limit.
    {
        "name": "Floating Point Edge 1",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.500001), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,  # (1.0, 0.500001) is just outside the tolerance
    },

    # 11. Floating Point Precision Test 2: Coordinates *at* epsilon limit (should pass with 1 piece).
    {
        "name": "Floating Point Edge 2",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1,
    },

    # 12. Non-Monotonic X values: Invalid input (The algorithm should typically assume sorted X).
    # If the algorithm handles it, it should still calculate the max deviation correctly.
    {
        "name": "Unsorted X (Should Fail or Handle)",
        "pw_linear_fx": [(0.0, 0.0), (3.0, 3.0), (1.0, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2,  # If sorted: 1. If unsorted, should be 2: (0,0) to (3,3) fails at (1,1).
        # Assuming the algorithm requires sorted input, but test for robustness.
    },

    # 13. Very Long, Smooth Curve: Should find the optimal long segment.
    {
        "name": "Long Smooth Curve (Optimal Long Segments)",
        "pw_linear_fx": [(i, 0.05 * (i % 2)) for i in range(11)],
        "epsilon": 0.06,
        "expected_pieces": 1,  # Deviation is max 0.05, so 1 segment is possible.
    },

    # 14. Very Long, Highly Deviating Curve: Forces many small pieces.
    {
        "name": "Long Highly Deviating Curve",
        "pw_linear_fx": [(i, i % 2) for i in range(11)],
        "epsilon": 0.4,
        "expected_pieces": 5,  # Must break at every other point. (0-2), (2-4), (4-6), (6-8), (8-10)
    },

    # 15. Negative Coordinates: Ensure handling of negative y-values and x-values.
    {
        "name": "Negative Coordinates",
        "pw_linear_fx": [(-5.0, -1.0), (0.0, 0.0), (5.0, -1.0)],
        "epsilon": 0.9,
        "expected_pieces": 2,  # Deviation is 1.0 at (0,0) from line (-5,-1) to (5,-1).
    },

    # 16. Epsilon near Zero, Deviation near Zero: Tests for stability when numbers are very small.
    {
        "name": "Small Numbers (Near Zero)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1e-6), (2.0, 0.0)],
        "epsilon": 1e-7,
        "expected_pieces": 2,  # Deviation 1e-6 is > 1e-7
    },

    # 17. Constant Function (Horizontal Line): All points on the line.
    {
        "name": "Constant Function",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.001,
        "expected_pieces": 1,
    },

    # 18. Linear Trend with Small Noise (Should be 1 piece if epsilon is generous).
    {
        "name": "Linear Trend with Small Noise (1 Piece)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 1.99), (3.0, 3.0)],
        "epsilon": 0.01,
        "expected_pieces": 1,  # Max deviation is 0.01 at (1.0, 1.01) from line (0,0) to (3,3).
    },

    # 19. Two Clear Approximation Regions: Forces exactly 2 segments.
    # (0,0) to (2,2) with a perturbation at (1, 1.5). Deviation 0.5.
    # (2,2) to (4,4) with a perturbation at (3, 3.5). Deviation 0.5.
    {
        "name": "Two Clear Regions",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.5), (2.0, 2.0), (3.0, 3.5), (4.0, 4.0)],
        "epsilon": 0.4
    },

    # 20. Example from prompt:
    {
        "name": "Prompt Example",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "expected_pieces": 2,  # (0,1) to (2,3) fails at (1,1) (dev 0.0). Oh wait...
        # The line between (0,1) and (5,8) is y = 1.4x + 1.0.
        # At x=1.0, y_line = 2.4. Error is |1.0 - 2.4| = 1.4. (Fails epsilon=0.5).
        # Optimal break is at (1.0, 1.0).
        # Seg 1: (0.0, 1.0) to (1.0, 1.0). Valid (1 piece).
        # Seg 2: (1.0, 1.0) to (5.0, 8.0). Line is y = 1.75x - 0.75.
        # At x=2.0, y_data=3.0. y_line = 2.75. Error |3.0-2.75| = 0.25. (Passes epsilon=0.5).
        # Total pieces: 2
    },
]
test_cases28 = [
    # 1. Basic Linear/Simple Cases (Should require 1 or 2 pieces)
    {
        "description": "Perfectly linear data, should require 1 piece.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01,
        "expected_pieces_optimal": 1 # For algorithms that find the minimum.
    },
    {
        "description": "Two distinct linear segments with a clear break.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces_optimal": 2
    },
    {
        "description": "Minimal 3-point dataset, perfectly linear.",
        "pw_linear_fx": [(0.0, 5.0), (5.0, 5.0), (10.0, 5.0)],
        "epsilon": 0.5,
        "expected_pieces_optimal": 1
    },
    {
        "description": "Perfectly linear, high tolerance (should be 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 1.0), (20.0, 2.0)],
        "epsilon": 5.0,
        "expected_pieces_optimal": 1
    },

    # 2. Step and Sharp Angle Cases (Expose L-infinity check complexity)
    {
        "description": "Sharp 90-degree bend, high points, low tolerance.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 100.0), (2.0, 100.0)],
        "epsilon": 0.1,
        "expected_pieces_optimal": 2
    },
    {
        "description": "Near-vertical jump followed by a segment (tests $L_{\infty}$ on steep slopes).",
        "pw_linear_fx": [(0.0, 0.0), (0.001, 5.0), (1.0, 5.0), (2.0, 6.0)],
        "epsilon": 0.5,
        "expected_pieces_optimal": 2
    },
    {
        "description": "Staircase pattern (each step requires a new piece if epsilon is small).",
        "pw_linear_fx": [(0,0), (1,0), (1,1), (2,1), (2,2), (3,2), (3,3)],
        "epsilon": 0.05,
        "expected_pieces_optimal": 4
    },
    {
        "description": "A deep valley that might be approximated by one line if epsilon is large.",
        "pw_linear_fx": [(0.0, 1.0), (0.5, -5.0), (1.0, 1.0)],
        "epsilon": 2.0,
        "expected_pieces_optimal": 1 # Max error is 5.0, 1 piece fits if E > 5.0
    },

    # 3. Curved Data (Expose non-linearity and greedy flaws)
    {
        "description": "Simple parabola y=x^2, low tolerance.",
        "pw_linear_fx": [(x, x**2) for x in range(0, 5)],
        "epsilon": 0.1,
        "expected_pieces_optimal": 3 # Estimated
    },
    {
        "description": "Sine wave segment, challenging for greedy algorithms.",
        "pw_linear_fx": [(i/10.0, 0.5 * (1 - (i/10.0))) for i in range(11)] + [(i/10.0, 0.5 * (i/10.0)) for i in range(11, 21)], # V-shape
        "epsilon": 0.05,
        "expected_pieces_optimal": 2
    },
    {
        "description": "Data resembling y=sqrt(x), steepest at the start.",
        "pw_linear_fx": [(i, i**0.5) for i in range(0, 10)],
        "epsilon": 0.2,
        "expected_pieces_optimal": 3 # Estimated
    },
    {
        "description": "Exaggerated 'M' shape requiring multiple pieces.",
        "pw_linear_fx": [(0,0), (1,10), (2,0), (3,10), (4,0)],
        "epsilon": 1.0,
        "expected_pieces_optimal": 4
    },

    # 4. Critical Tolerance Cases (Edge cases for epsilon)
    {
        "description": "Tolerance just below a segment's max error (forces a split).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.5), (3.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces_optimal": 2
    },
    {
        "description": "Tolerance just above a segment's max error (allows a single piece).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.5), (3.0, 0.0)],
        "epsilon": 0.51,
        "expected_pieces_optimal": 1
    },
    {
        "description": "Zero tolerance (should require N pieces).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces_optimal": 3
    },
    {
        "description": "Very large tolerance (should require 1 piece).",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0), (20.0, 0.0), (30.0, 10.0)],
        "epsilon": 100.0,
        "expected_pieces_optimal": 1
    },

    # 5. Long and Noisy Data (Stress test for efficiency/accuracy)
    {
        "description": "Long, perfectly linear dataset (test for efficiency and initial fit).",
        "pw_linear_fx": [(i, i * 0.1) for i in range(21)],
        "epsilon": 0.01,
        "expected_pieces_optimal": 1
    },
    {
        "description": "High-frequency noise (should require many pieces).",
        "pw_linear_fx": [(i, (i % 2) * 2.0) for i in range(10)], # Zeros and Twos alternating
        "epsilon": 0.5,
        "expected_pieces_optimal": 5 # Each pair (0,2) or (2,0) needs its own piece
    },
    {
        "description": "Random noise around a center line (tests averaging/max deviation).",
        "pw_linear_fx": [(i, 5.0 + (-1)**i * 0.4) for i in range(11)],
        "epsilon": 0.35,
        "expected_pieces_optimal": 6 # Max error is 0.4, so 0.35 forces splits
    },
    {
        "description": "The 'classic' non-optimal case: a flat line then a gentle curve, where a greedy start could fail.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.1), (4.0, 0.5), (5.0, 1.0)],
        "epsilon": 0.2,
        "expected_pieces_optimal": 2 # Optimal might be (0,0)->(3, 0.1) and (3,0.1)->(5,1.0)
    },
]
test_cases29 = [
    # 1. Basic Case: Perfectly linear data, should require 1 segment.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,  # Expected minimum segments: 1
    },
    # 2. Perfect Fit: Zero tolerance for a perfectly linear function. Should require 1 segment.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0,  # Expected minimum segments: 1
    },
    # 3. Constant Data: Horizontal line, should require 1 segment regardless of epsilon > 0.
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 1e-6,  # Expected minimum segments: 1
    },
    # 4. Zero Tolerance on Non-linear Data: Should require n segments (n+1 points).
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.5), (3.0, 1.0)],
        "epsilon": 0.0,  # Expected minimum segments: 3
    },
    # 5. Parabola (Convex): Standard test for non-linearity. epsilon forces multiple segments.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0), (5.0, 25.0)],
        "epsilon": 0.5,  # Expected minimum segments: 3 (approx.)
    },
    # 6. Sharp Turn (V-shape): Tests ability to break at critical change points.
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 0.0), (2.0, 5.0)],
        "epsilon": 0.1,  # The maximum error is 2.5 (at x=0.5 and x=1.5). Should require 2 segments.
    },
    # 7. Step Function (Almost Discontinuous): Requires many segments with small epsilon.
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.0), (0.5001, 10.0), (1.0, 10.0)],
        "epsilon": 1.0,  # Max error is 5. Should require 2 segments.
    },
    # 8. Large Epsilon: Tolerance is greater than the maximum deviation, should require 1 segment.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)],
        "epsilon": 1.0,  # Max deviation is 0.5. Expected minimum segments: 1
    },
    # 9. Just Below Max Deviation: Smallest epsilon that still allows 1 segment.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0)],
        "epsilon": 0.21,  # Max deviation from line (0,0)-(2,0) is 0.4. Should require 1 segment.
    },
    # 10. Just Above Max Deviation: Smallest epsilon that forces 2 segments.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0)],
        "epsilon": 0.19,  # Should require 2 segments.
    },
    # 11. Oscillating Data (Sine-like): Tests performance on a smooth, repetitive curve.
    {
        "pw_linear_fx": [(x, 2.0 * ((x % 2 == 0) - (x % 2 != 0)) * (x / 5.0)) for x in range(6)],
        "epsilon": 0.5,  # Expected minimum segments: 3 (approx.)
    },
    # 12. Tightly Spaced Points, Small Deviation: Tests handling of high point density.
    {
        "pw_linear_fx": [(i * 0.1, 0.1 * i + 0.01 * (i % 2)) for i in range(11)],
        "epsilon": 0.005,  # Max deviation is 0.005 from line, but is slightly over. Should force 2 segments.
    },
    # 13. End Point Coincidence: Two pieces where the endpoints are very close in Y but far in X.
    {
        "pw_linear_fx": [(0.0, 0.0), (5.0, 0.0), (5.1, 1.0), (10.0, 1.0)],
        "epsilon": 0.5,  # The first 3 points may be approximated by 1 segment. Expected minimum segments: 2
    },
    # 14. Concave Function: Tests algorithm on a curve bending down.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.41), (3.0, 1.73), (4.0, 2.0)],  # y = sqrt(x)
        "epsilon": 0.1,  # Expected minimum segments: 2
    },
    # 15. Minimal Points (2 points): Should always require 1 segment.
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0)],
        "epsilon": 0.0,  # Expected minimum segments: 1
    },
    # 16. Minimal Points (3 points): Linearly increasing, requires 1 segment.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0,  # Expected minimum segments: 1
    },
    # 17. Minimal Points (3 points): Triangle peak, requires 2 segments with small epsilon.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.49,  # Max deviation is 0.5. Forces 2 segments.
    },
    # 18. Large Data Set, Large Deviation: Should require many segments.
    {
        "pw_linear_fx": [(i, (i % 2) * 10 + (i % 3) * 5) for i in range(20)],
        "epsilon": 1.0,  # Highly variable data. Expected minimum segments: > 5
    },
    # 19. Noisy Linear Data: Tests robustness against small, random noise.
    {
        "pw_linear_fx": [(i, i + (0.1 if i % 3 == 0 else -0.1)) for i in range(6)],
        "epsilon": 0.1,  # Max deviation from y=x is 0.1. Should require 1 segment.
    },
    # 20. Noisy Linear Data (Forces Break): Tests the limit of noise tolerance.
    {
        "pw_linear_fx": [(i, i + (0.1 if i % 3 == 0 else -0.1)) for i in range(6)],
        "epsilon": 0.09,  # Max deviation is 0.1. Forces 2 segments.
    },
]
test_cases30 = [
    # 1. Basic Straight Line (Optimal 1 Segment)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.1
    },

    # 2. Simple Deviation (Optimal 1 Segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.1), (3.0, 0.3)],
        "epsilon": 0.5
    },

    # 3. Step Function (Optimal 4 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 4. Small Epsilon, Forcing Many Segments (Optimal 4 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
        "epsilon": 0.05
    },

    # 5. Large Epsilon, Reducing Segments (Optimal 1 Segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)],
        "epsilon": 1.0
    },

    # 6. Zig-Zag/Oscillation Close to Boundary (Optimal 4 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.49
    },

    # 7. Zig-Zag Epsilon Covers All (Optimal 1 Segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 8. Point Exactly on Epsilon Boundary (Optimal 1 Segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 0.5), (3.0, 0.25), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 9. Point Just Exceeding Epsilon (Forces Optimal 2 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.25), (2.0, 0.51), (3.0, 0.25), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 10. Horizontal Line With Mid-Point Deviation (Optimal 2 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5
    },

    # 11. Concave/Convex Curve (Optimal 3 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.2
    },

    # 12. Non-Uniform X Spacing (Optimal 2 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.5), (10.0, 0.0), (10.1, 0.5)],
        "epsilon": 0.4
    },

    # 13. High Y-Offset, Low Slope (Optimal 1 Segment)
    {
        "pw_linear_fx": [(0.0, 100.0), (1.0, 100.2), (2.0, 100.0), (3.0, 100.2)],
        "epsilon": 0.5
    },

    # 14. Repeated Points/Segments (Optimal 1 Segment - Testing Degeneracy)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.1
    },

    # 15. The "W" Function (Optimal 3 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.25
    },

    # 16. The "W" Function, Wide Epsilon (Optimal 1 Segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 1.0
    },

    # 17. Floating Point Precision Test (Optimal 1 Segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.001), (2.0, 0.002), (3.0, 0.003)],
        "epsilon": 0.005
    },

    # 18. Zero Epsilon (Forces Max Segments - Optimal 3 Segments for 4 points)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.0
    },

    # 19. Long Sequence, Mostly Flat (Optimal 2 Segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0), (5.0, 1.0), (6.0, 0.0)],
        "epsilon": 0.5
    },

    # 20. Negative Y-Values (Optimal 4 Segments)
    {
        "pw_linear_fx": [(0.0, -1.0), (1.0, -0.5), (2.0, -1.0), (3.0, -0.5), (4.0, -1.0)],
        "epsilon": 0.4
    }
]
