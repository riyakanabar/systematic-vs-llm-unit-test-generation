#30 Sept 5:41PM few-shot prompt used to generate 30 test cases (Grok3 Auto mode)
test_cases1 = [
    # Test Case 1: Collinear points, should require only one segment regardless of ε
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "description": "Collinear points; expects single segment for any reasonable ε."
    },
    # Test Case 2: Zigzag pattern, tests handling of sharp changes
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2,
        "description": "Zigzag pattern; tests if algorithm handles alternating points efficiently."
    },
    # Test Case 3: Flat line with one outlier, tests sensitivity to single deviation
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.3,
        "description": "Mostly flat with one peak; tests if outlier forces additional segments."
    },
    # Test Case 4: Large ε, should allow single segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 2.0,
        "description": "Large ε; expects single segment as all points are within tolerance."
    },
    # Test Case 5: Small ε, forces more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.1,
        "description": "Small ε; tests if algorithm uses multiple segments for small tolerance."
    },
    # Test Case 6: Single segment, trivial case
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0)],
        "epsilon": 0.5,
        "description": "Two points; expects single segment (trivial case)."
    },
    # Test Case 7: Non-uniform x-spacing, tests robustness to irregular intervals
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.2), (2.0, 0.5), (10.0, 1.0)],
        "epsilon": 0.3,
        "description": "Non-uniform x-spacing; tests handling of irregular intervals."
    },
    # Test Case 8: Step function, tests abrupt changes
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.2,
        "description": "Step function; tests handling of discontinuities in y."
    },
    # Test Case 9: Dense points, nearly linear, tests efficiency
    {
        "pw_linear_fx": [(0.0, 0.0), (0.2, 0.21), (0.4, 0.39), (0.6, 0.61), (0.8, 0.79), (1.0, 1.0)],
        "epsilon": 0.1,
        "description": "Dense, nearly linear points; tests if algorithm minimizes segments."
    },
    # Test Case 10: Zero ε, should reproduce all segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "description": "Zero ε; expects all original segments to be preserved."
    }
]
test_cases2 = [
    # Test Case 1: Basic case with small number of points, should require 2 segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: All points collinear, should require 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Points requiring exactly one segment within epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.2
    },
    # Test Case 4: Large epsilon, all points fit in one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 2.0
    },
    # Test Case 5: Small epsilon, each segment needs its own piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.1
    },
    # Test Case 6: Duplicate x-coordinates (degenerate case, same x should be handled)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 0.1), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.05
    },
    # Test Case 7: Large number of points, zig-zag pattern
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.2
    },
    # Test Case 8: Single segment with two points
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0
    },
    # Test Case 9: Points with maximum deviation at endpoints
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 1.0)],
        "epsilon": 0.5
    },
    # Test Case 10: High precision case with very small epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.001), (2.0, 0.002), (3.0, 0.003)],
        "epsilon": 0.0001
    }
]
test_cases3 = [
    # Test Case 1: Collinear Points
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.5,
        "expected_segments": 1
    },
    # Test Case 2: Single Segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "expected_segments": 1
    },
    # Test Case 3: Steep Slope
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 20.0)],
        "epsilon": 0.5,
        "expected_segments": 2
    },
    # Test Case 4: Oscillating Function
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.25,
        "expected_segments": 4
    },
    # Test Case 5: Zero Epsilon
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.0,
        "expected_segments": 3
    },
    # Test Case 6: Large Epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 10.0,
        "expected_segments": 1
    },
    # Test Case 7: Duplicate Points
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.5,
        "expected_segments": 1
    },
    # Test Case 8: Single Point
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.5,
        "expected_segments": 0
    },
    # Test Case 9: Monotonic Function
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 6.0)],
        "epsilon": 0.5,
        "expected_segments": 2
    },
    # Test Case 10: Flat Function with Noise
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.9), (3.0, 1.05)],
        "epsilon": 0.2,
        "expected_segments": 1
    }
]
test_cases4 = [
    # Test Case 1: Basic case with small number of points and moderate epsilon
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Collinear points (should require only one piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Large epsilon (should allow fewer pieces, possibly one)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 5.0
    },
    # Test Case 4: Small epsilon (forces more pieces, tests precision)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.01
    },
    # Test Case 5: Sharp change in y-values (tests handling of abrupt transitions)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 10.0), (2.0, 10.0)],
        "epsilon": 0.5
    },
    # Test Case 6: Duplicate x-values (degenerate case, should handle or reject)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.5
    },
    # Test Case 7: Single segment (minimal case with two points)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.1
    },
    # Test Case 8: Oscillating data (tests ability to handle frequent changes)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2
    },
    # Test Case 9: Large number of points (tests scalability)
    {
        "pw_linear_fx": [(i, i % 2) for i in range(100)],  # Alternating 0,1 pattern
        "epsilon": 0.1
    },
    # Test Case 10: Zero epsilon (exact fit, should use all segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 4.0)],
        "epsilon": 0.0
    }
]
test_cases5 = [
    # Test Case 1: Basic case with small number of points and reasonable epsilon
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Collinear points (should require only one segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Sharp jump in y-values (tests handling of large slope changes)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 10.0), (2.0, 10.0)],
        "epsilon": 0.2
    },
    # Test Case 4: Zero epsilon (exact fit, should require n segments)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 1.5), (3.0, 3.0)],
        "epsilon": 0.0
    },
    # Test Case 5: Large epsilon (should allow single segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 10.0
    },
    # Test Case 6: Duplicate x-coordinates (invalid case, tests robustness)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0), (2.0, 4.0)],
        "epsilon": 0.5
    },
    # Test Case 7: Single segment (minimum points, n=1)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.1
    },
    # Test Case 8: Dense points with small fluctuations
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.05), (0.3, 0.15), (0.4, 0.1)],
        "epsilon": 0.05
    },
    # Test Case 9: Negative y-values and large x-range
    {
        "pw_linear_fx": [(0.0, -5.0), (10.0, -4.0), (20.0, -6.0), (30.0, -5.5)],
        "epsilon": 0.5
    },
    # Test Case 10: Non-uniform x-spacing with oscillations
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (3.0, -1.0), (3.1, 1.0), (5.0, 0.0)],
        "epsilon": 0.3
    }
]
test_cases6 = [
    # Test Case 1: Basic case with small epsilon, requiring multiple segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Collinear points, should require only one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Single segment, should fit within large epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 1.0
    },
    # Test Case 4: Sharp change in y-values, testing small epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 0.1
    },
    # Test Case 5: Large epsilon, should allow single segment for varied points
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 10.0
    },
    # Test Case 6: Identical points, should require one segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.5
    },
    # Test Case 7: Very small epsilon, forcing one segment per point
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.1), (3.0, 1.2)],
        "epsilon": 0.01
    },
    # Test Case 8: Negative coordinates and values
    {
        "pw_linear_fx": [(-2.0, -2.0), (-1.0, -1.0), (0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5
    },
    # Test Case 9: Non-uniform x-spacing, testing robustness
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (5.0, 2.0), (10.0, 3.0)],
        "epsilon": 0.5
    },
    # Test Case 10: Large number of points with gradual change
    {
        "pw_linear_fx": [(i, i + 0.2 * (-1)**i) for i in range(10)],
        "epsilon": 0.3
    }
]
test_cases7 = [
    # Test Case 1: Basic case with small deviation, should require minimal pieces
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Collinear points, should require one piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Points with sharp change, tests handling of abrupt slope change
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 10.0), (2.0, 10.0)],
        "epsilon": 0.5
    },
    # Test Case 4: Small epsilon, forces more pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.5)],
        "epsilon": 0.05
    },
    # Test Case 5: Large epsilon, allows fewer pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 3.0
    },
    # Test Case 6: Single segment, should require one piece
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 1.0
    },
    # Test Case 7: Points at epsilon boundary, tests precision
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5)],
        "epsilon": 0.5
    },
    # Test Case 8: Non-uniform x-spacing, tests robustness
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.2), (5.0, 0.4), (10.0, 0.6)],
        "epsilon": 0.3
    },
    # Test Case 9: Oscillating points, tests handling of frequent changes
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2
    },
    # Test Case 10: Large number of points, tests scalability
    {
        "pw_linear_fx": [(i, 0.1 * (i % 2)) for i in range(100)],
        "epsilon": 0.05
    }
]
test_cases8 = [
    # Test Case 1: Linear points - All points on a straight line y=x, should require one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Sharp change - Sharp y-value change at x=1.0, requires at least two segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.1, 5.0), (2.0, 5.0)],
        "epsilon": 0.5
    },
    # Test Case 3: Flat line - All y-values are 2.0, should require one segment
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0), (4.0, 2.0)],
        "epsilon": 1.0
    },
    # Test Case 4: Single segment - Two points forming one segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5
    },
    # Test Case 5: Small epsilon - Forces more segments due to tight tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.01
    },
    # Test Case 6: Duplicate points - Duplicate points at x=1.0, should collapse duplicates
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.5
    },
    # Test Case 7: Collinear points - Should merge into one segment with larger epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1.0
    },
    # Test Case 8: Large dataset - 20 points with small oscillations, tests scalability
    {
        "pw_linear_fx": [(x, x + 0.2 * (-1)**x) for x in range(20)],
        "epsilon": 0.5
    },
    # Test Case 9: Empty input - Should handle gracefully (e.g., raise error or return empty)
    {
        "pw_linear_fx": [],
        "epsilon": 0.5
    },
    # Test Case 10: Single point - No segments possible, tests edge case handling
    {
        "pw_linear_fx": [(0.0, 1.0)],
        "epsilon": 0.5
    }
]
test_cases9 = [
    # Test Case 1: Collinear points (should require one segment)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.1
    },

    # Test Case 2: Points requiring multiple segments due to sharp slope change
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 3.0), (4.0, 1.0)],
        "epsilon": 0.5
    },

    # Test Case 3: Single segment possible with small epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2)],
        "epsilon": 0.15
    },

    # Test Case 4: Large epsilon allowing all points to be approximated by one segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 0.0), (3.0, 3.0)],
        "epsilon": 2.0
    },

    # Test Case 5: Zero epsilon (exact fit, likely requires n segments)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.0
    },

    # Test Case 6: Large dataset with oscillatory behavior
    {
        "pw_linear_fx": [(float(x), float((-1) ** x)) for x in range(10)],
        "epsilon": 0.5
    },

    # Test Case 7: Points with very close x-coordinates (numerical precision test)
    {
        "pw_linear_fx": [(1.0, 1.0), (1.0001, 1.1), (1.0002, 1.0), (1.0003, 1.2)],
        "epsilon": 0.05
    },

    # Test Case 8: Monotonic increasing points (gradual slope change)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.2
    },

    # Test Case 9: Single segment boundary case (points just within epsilon)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5)],
        "epsilon": 0.5
    },

    # Test Case 10: Non-uniform x-spacing with high deviation
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 1.0), (10.1, 5.0), (20.0, 2.0)],
        "epsilon": 0.5
    }
]
test_cases10 = [
    # Test Case 1: Collinear points, should require one segment for any ε ≥ 0
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.5
    },

    # Test Case 2: Step function, requires multiple segments for small ε
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.1
    },

    # Test Case 3: Large ε, all points can be approximated with one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 2.0
    },

    # Test Case 4: ε = 0, requires a segment for each pair of points
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 3.0)],
        "epsilon": 0.0
    },

    # Test Case 5: High-frequency oscillation, tests handling of rapid changes
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)],
        "epsilon": 0.2
    },

    # Test Case 6: Single segment, minimal case with two points
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5
    },

    # Test Case 7: Near-collinear points, tests sensitivity to small deviations
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.05
    },

    # Test Case 8: Duplicate x-coordinates, testing robustness
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0)],
        "epsilon": 0.5
    },

    # Test Case 9: Many points with noise, tests scalability
    {
        "pw_linear_fx": [(i / 10.0, i / 10.0 + 0.1 * (-1) ** i) for i in range(11)],
        "epsilon": 0.15
    },

    # Test Case 10: Sharp peak, requires multiple segments for small ε
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 0.5
    }
]
test_cases11 = [
    {
        "description": "Basic case with small epsilon, requiring multiple segments",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    {
        "description": "Collinear points, should require one segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    {
        "description": "Sharp change in y-values, testing tight epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 10.0), (2.0, 10.0)],
        "epsilon": 0.5
    },
    {
        "description": "Large epsilon, should allow single segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 10.0
    },
    {
        "description": "Two points, minimal case requiring one segment",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5
    },
    {
        "description": "Dense points with small oscillations, testing optimization",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.0), (0.3, 0.1), (0.4, 0.0), (0.5, 0.1)],
        "epsilon": 0.05
    },
    {
        "description": "Points requiring exact fit due to zero epsilon",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 1.0)],
        "epsilon": 0.0
    },
    {
        "description": "Large y-range, testing numerical stability",
        "pw_linear_fx": [(0.0, 1000.0), (1.0, 1000.0), (2.0, -1000.0), (3.0, -1000.0)],
        "epsilon": 1.0
    },
    {
        "description": "Nearly collinear points, testing epsilon boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.01), (2.0, 0.02), (3.0, 0.03)],
        "epsilon": 0.015
    },
    {
        "description": "Sparse points with alternating pattern, testing segment reduction",
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0), (20.0, 0.0), (30.0, 10.0), (40.0, 0.0)],
        "epsilon": 5.0
    }
]
test_cases12 = [
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "description": "Basic case: four points with moderate slope changes, ε=0.5, testing if algorithm can reduce segments while maintaining L∞ norm."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.1,
        "description": "Collinear points: all y=0, small ε, should return one segment as all points are exactly on a line."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2,
        "description": "Zigzag pattern: alternating y-values, small ε, likely requires multiple segments to stay within tolerance."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "description": "Sharp peak: large y-change at middle point, small ε, tests handling of abrupt changes."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0)],
        "epsilon": 1.0,
        "description": "Minimal case: two points (one segment), should return one segment regardless of ε."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "description": "Invalid input: duplicate x-coordinates at x=0, tests error handling for non-strictly increasing x."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 1.0), (1.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.5,
        "description": "Invalid input: non-increasing x-coordinates (2.0 to 1.0), tests error handling."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.4)],
        "epsilon": 0.5,
        "description": "Nearly collinear: points slightly deviating from a line, large ε, should approximate with one segment."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.01,
        "description": "Strictly linear: points on y=x, very small ε, tests if algorithm preserves exact fit or over-segments."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 2.1), (3.0, 2.2), (4.0, 4.0)],
        "epsilon": 2.0,
        "description": "Large ε: allows significant deviation, tests if algorithm merges segments effectively to minimize count."
    }
]
test_cases13 = [
    # Test Case 1: Simple linear function, should reduce to one segment
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.1
    },
    # Test Case 2: Points requiring multiple segments due to sharp change
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.1, 2.0), (2.0, 2.0)],
        'epsilon': 0.5
    },
    # Test Case 3: Collinear points with small noise, should reduce to one segment
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.01), (2.0, 2.02), (3.0, 2.99)],
        'epsilon': 0.03
    },
    # Test Case 4: Single segment, exact fit within epsilon
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0)],
        'epsilon': 0.0
    },
    # Test Case 5: Large epsilon, should allow single segment
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        'epsilon': 2.0
    },
    # Test Case 6: Small epsilon, forces more segments
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        'epsilon': 0.1
    },
    # Test Case 7: Duplicate x-values (edge case, assuming algorithm handles as discontinuity)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.0, 2.0), (2.0, 2.0)],
        'epsilon': 0.5
    },
    # Test Case 8: Oscillatory pattern, tests handling of frequent changes
    {
        'pw_linear_fx': [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)],
        'epsilon': 0.2
    },
    # Test Case 9: Unevenly spaced points, tests interpolation
    {
        'pw_linear_fx': [(0.0, 0.0), (0.1, 0.1), (2.0, 2.0), (10.0, 2.0)],
        'epsilon': 0.5
    },
    # Test Case 10: Flat segment with outlier, tests single point deviation
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 1.0)],
        'epsilon': 0.5
    }
]
test_cases14 = [
    # Test Case 1: Basic case with small deviation, should require fewer segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Collinear points, should reduce to one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Sharp change in slope, may require more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0)],
        "epsilon": 0.2
    },
    # Test Case 4: Single segment, should always return one segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 1.0
    },
    # Test Case 5: Large epsilon, should reduce to minimal segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 5.0
    },
    # Test Case 6: Duplicate points, testing handling of identical points
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 1.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.5
    },
    # Test Case 7: Small epsilon, forces more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.01
    },
    # Test Case 8: Negative coordinates, testing robustness
    {
        "pw_linear_fx": [(-2.0, -2.0), (-1.0, -1.0), (0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5
    },
    # Test Case 9: Large number of points with oscillation
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.25
    },
    # Test Case 10: Extreme values, testing numerical stability
    {
        "pw_linear_fx": [(0.0, 1e6), (1.0, 1e6 + 1), (2.0, 1e6 + 2), (3.0, 1e6)],
        "epsilon": 1.0
    }
]
test_cases15 = [
    # Test Case 1: Basic case with small changes, should require minimal pieces
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.5), (3.0, 2.0)],
        "epsilon": 0.5,
        "description": "Small changes within epsilon, should need 1 piece"
    },
    # Test Case 2: Collinear points, should require 1 piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "description": "Collinear points, should be approximated by 1 piece"
    },
    # Test Case 3: Sharp change exceeding epsilon, should require multiple pieces
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 3.0)],
        "epsilon": 0.5,
        "description": "Sharp change at x=2, should need at least 2 pieces"
    },
    # Test Case 4: Single segment, trivial case
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5,
        "description": "Single segment, should need exactly 1 piece"
    },
    # Test Case 5: Duplicate points, testing robustness
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 1.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.1,
        "description": "Duplicate points at x=0, should handle gracefully and need 1 piece"
    },
    # Test Case 6: Large epsilon, should allow fewer pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 3.0,
        "description": "Large epsilon, should approximate zigzag with fewer pieces"
    },
    # Test Case 7: Points exactly at epsilon boundary
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5)],
        "epsilon": 0.5,
        "description": "Points at epsilon boundary, tests boundary condition handling"
    },
    # Test Case 8: Empty or invalid input, edge case
    {
        "pw_linear_fx": [(0.0, 1.0)],
        "epsilon": 0.5,
        "description": "Single point, should handle as invalid or return empty"
    },
    # Test Case 9: High-frequency oscillations within epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.2), (1.0, 0.0), (1.5, 0.2), (2.0, 0.0)],
        "epsilon": 0.3,
        "description": "High-frequency small oscillations, should need 1 piece"
    },
    # Test Case 10: Non-uniform x-spacing with sharp change
    {
        "pw_linear_fx": [(0.0, 1.0), (0.1, 1.0), (2.0, 10.0), (10.0, 10.0)],
        "epsilon": 1.0,
        "description": "Non-uniform x-spacing with sharp change, should need at least 2 pieces"
    }
]
test_cases16= [
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_segments": 1,
        "description": "Linear points, should require exactly one segment as all points lie on y=x."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.05), (3.0, 0.15)],
        "epsilon": 0.2,
        "expected_segments": 1,
        "description": "Points nearly colinear within epsilon, testing if algorithm avoids unnecessary segments."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.5,
        "expected_segments": 2,
        "description": "Sharp jump at x=1, should require two segments to handle discontinuity-like behavior."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.01), (0.2, 0.02), (0.3, 0.01), (0.4, 0.0)],
        "epsilon": 0.05,
        "expected_segments": 1,
        "description": "Dense points with small variations, testing if algorithm merges into one segment."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0)],
        "epsilon": 0.5,
        "expected_segments": 1,
        "description": "Points just within epsilon of a single line, testing boundary of tolerance."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.1,
        "expected_segments": 3,
        "description": "Zigzag pattern, should require a segment for each pair due to tight epsilon."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 10.0,
        "expected_segments": 1,
        "description": "Large epsilon allowing a single segment (e.g., y=5), testing loose tolerance."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 0.0)],
        "epsilon": 0.01,
        "expected_segments": 3,
        "description": "Small epsilon forcing a segment per point pair, testing precision."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "expected_segments": None,
        "description": "Duplicate x-coordinates, should raise an error due to invalid input."
    },
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.5,
        "expected_segments": 0,
        "description": "Single point, degenerate case, should return no segments."
    }
]
test_cases17 = [
    # Test Case 1: Basic case with small ε, requiring multiple segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "description": "Basic case with small ε, expecting multiple segments due to significant y-changes."
    },
    # Test Case 2: Collinear points, should require one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "description": "Collinear points, should be approximated with one segment regardless of small ε."
    },
    # Test Case 3: Single segment, large ε, should require one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 10.0,
        "description": "Single segment with large ε, should require exactly one segment."
    },
    # Test Case 4: Sharp spike, small ε, tests handling of abrupt changes
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 10.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "description": "Sharp spike in data, small ε, should require multiple segments."
    },
    # Test Case 5: Duplicate points, tests robustness to repeated x-values
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.5,
        "description": "Duplicate points at x=0, tests handling of non-unique x-coordinates."
    },
    # Test Case 6: Large ε, should allow fewer segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 5.0,
        "description": "Large ε, should approximate with fewer segments, possibly one."
    },
    # Test Case 7: Non-uniform x-spacing, tests generalization
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (10.0, 2.0), (100.0, 3.0)],
        "epsilon": 0.5,
        "description": "Non-uniform x-spacing, tests handling of unevenly spaced points."
    },
    # Test Case 8: Zero ε, should require n segments (exact fit)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 1.0), (3.0, 2.0)],
        "epsilon": 0.0,
        "description": "Zero ε, should require one segment per pair of points (exact fit)."
    },
    # Test Case 9: Flat line with noise, tests robustness to small variations
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.9), (3.0, 1.05)],
        "epsilon": 0.2,
        "description": "Nearly flat line with small noise, should require one segment."
    },
    # Test Case 10: Large number of points, tests scalability
    {
        "pw_linear_fx": [(i, 2.0 + (-1)**i * 0.5) for i in range(100)],
        "epsilon": 0.6,
        "description": "Large number of points with alternating pattern, tests scalability and pattern handling."
    }
]
test_cases18 = [
    # Test Case 1: Collinear points, should require 1 segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # Test Case 2: Sharp change, requires multiple segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.1, 3.0), (2.0, 3.0)],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # Test Case 3: Small epsilon, forces more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.05,
        "expected_pieces": 3
    },
    # Test Case 4: Large epsilon, allows single segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 4.0)],
        "epsilon": 2.0,
        "expected_pieces": 1
    },
    # Test Case 5: Single segment (two points)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # Test Case 6: Duplicate x-coordinates (invalid input, should raise error)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0)],
        "epsilon": 0.5,
        "expected_pieces": None  # Expect algorithm to handle invalid input
    },
    # Test Case 7: Single point (degenerate case, no segments)
    {
        "pw_linear_fx": [(0.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces": 0
    },
    # Test Case 8: Oscillating points, requires multiple segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2,
        "expected_pieces": 4
    },
    # Test Case 9: Zero epsilon, requires exact fit (one segment per point pair)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    # Test Case 10: Large dataset with gradual changes
    {
        "pw_linear_fx": [(x, x + 0.1 * (x % 2)) for x in range(10)],
        "epsilon": 0.2,
        "expected_pieces": 5
    }
]
test_cases19 = [
    # Test Case 1: Collinear points, should require one segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.1
    },
    # Test Case 2: Sharp change, requires multiple segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.01, 10.0), (2.0, 10.0)],
        "epsilon": 0.5
    },
    # Test Case 3: Minimal points (2 points, always one segment)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5
    },
    # Test Case 4: Large epsilon, allows single segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 10.0
    },
    # Test Case 5: Small epsilon, forces more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.01
    },
    # Test Case 6: Irregular x-spacing
    {
        "pw_linear_fx": [(0.0, 1.0), (0.1, 1.1), (2.0, 1.2), (10.0, 1.3)],
        "epsilon": 0.2
    },
    # Test Case 7: Flat region with slight noise
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.1), (2.0, 1.9), (3.0, 2.05)],
        "epsilon": 0.15
    },
    # Test Case 8: Oscillating data
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 1.0), (4.0, -1.0)],
        "epsilon": 0.5
    },
    # Test Case 9: Single segment feasible within epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.2
    },
    # Test Case 10: Zero epsilon, forces exact fit (one segment per pair)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.0
    }
]
test_cases20 = [
    # Test Case 1: Linear function, should need only 1 segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.1,
        "expected_segments": 1
    },
    # Test Case 2: Near-linear with small deviations, testing tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.4)],
        "epsilon": 0.2,
        "expected_segments": 1
    },
    # Test Case 3: Sharp change, requiring multiple segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.0, 3.0), (2.0, 3.0)],
        "epsilon": 0.5,
        "expected_segments": 2
    },
    # Test Case 4: Collinear points, should collapse to 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    # Test Case 5: Large epsilon, allowing single segment for varied points
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 2.0,
        "expected_segments": 1
    },
    # Test Case 6: Small epsilon, forcing more segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.1,
        "expected_segments": 3
    },
    # Test Case 7: Single segment (two points)
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5,
        "expected_segments": 1
    },
    # Test Case 8: Oscillatory pattern, testing frequent changes
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.25,
        "expected_segments": 4
    },
    # Test Case 9: Non-uniform x-spacing, testing robustness
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.5), (2.0, 0.4), (10.0, 1.0)],
        "epsilon": 0.3,
        "expected_segments": 2
    },
    # Test Case 10: Duplicate x-coordinates, testing edge case
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.5,
        "expected_segments": 2
    }
]
test_cases21 = [
    # Test Case 1: Basic case with small changes
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Collinear points (should require only one piece)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Sharp spike in data
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 10.0), (2.0, 0.0)],
        "epsilon": 0.5
    },
    # Test Case 4: Large epsilon allowing single piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 5.0
    },
    # Test Case 5: Small epsilon requiring many pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 10.0)],
        "epsilon": 0.01
    },
    # Test Case 6: Duplicate points
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 1.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.5
    },
    # Test Case 7: Single segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.1
    },
    # Test Case 8: Zigzag pattern
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2
    },
    # Test Case 9: Negative coordinates
    {
        "pw_linear_fx": [(-2.0, -2.0), (-1.0, -1.0), (0.0, 0.0), (1.0, -1.0)],
        "epsilon": 0.3
    },
    # Test Case 10: Non-uniform x-spacing
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (10.0, 1.0), (100.0, 2.0)],
        "epsilon": 0.5
    }
]
test_cases22 = [
    # Test Case 1: Basic case with small epsilon, requiring multiple segments
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Collinear points, should require only one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Large epsilon, should allow a single segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 2.0
    },
    # Test Case 4: Duplicate points, testing handling of zero-length segments
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 1.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.5
    },
    # Test Case 5: Single segment possible with tight epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2)],
        "epsilon": 0.15
    },
    # Test Case 6: Sharp change in y, requiring multiple segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0001, 5.0), (2.0, 5.0)],
        "epsilon": 0.1
    },
    # Test Case 7: Negative coordinates and epsilon
    {
        "pw_linear_fx": [(0.0, -1.0), (1.0, -2.0), (2.0, -1.0), (3.0, -3.0)],
        "epsilon": 0.5
    },
    # Test Case 8: Very small epsilon, forcing many segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.3), (3.0, 0.6)],
        "epsilon": 0.01
    },
    # Test Case 9: Non-uniform x spacing, testing interpolation
    {
        "pw_linear_fx": [(0.0, 1.0), (0.5, 1.5), (2.0, 2.0), (10.0, 3.0)],
        "epsilon": 0.2
    },
    # Test Case 10: Single point pair, minimal case
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5
    }
]
test_cases23 = [
    # Test Case 1: Linear Data
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 2: Colinear Points
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.5
    },
    # Test Case 3: Sharp Change
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.1, 5.0), (2.0, 5.0)],
        "epsilon": 0.5
    },
    # Test Case 4: Repeated Points
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 2.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.2
    },
    # Test Case 5: Single Segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.2)],
        "epsilon": 0.3
    },
    # Test Case 6: Large Epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 10.0
    },
    # Test Case 7: Small Epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.01
    },
    # Test Case 8: Empty Input
    {
        "pw_linear_fx": [],
        "epsilon": 0.5
    },
    # Test Case 9: Single Point
    {
        "pw_linear_fx": [(0.0, 1.0)],
        "epsilon": 0.5
    },
    # Test Case 10: Large Dataset
    {
        "pw_linear_fx": [(i, (i % 2) + 0.1 * (i % 3)) for i in range(20)],
        "epsilon": 0.2
    }
]
test_cases24 = [
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "description": "Basic case with non-collinear points, moderate epsilon. Tests if algorithm can handle points requiring multiple segments.",
        "expected_segments": 3  # Likely needs at least 3 segments due to varying slopes and epsilon=0.5.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "description": "Collinear points with small epsilon. Should require one segment as points are perfectly linear.",
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)],
        "epsilon": 0.0,
        "description": "Collinear points with zero epsilon. Tests if algorithm enforces exact fit (one segment).",
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "description": "Sharp peak with small epsilon. Should require multiple segments due to large deviation.",
        "expected_segments": 2  # Likely needs two segments: (0,0) to (1,10), (1,10) to (2,0).
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 1.0,
        "description": "Constant function with large epsilon. Should require one segment.",
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5), (4.0, 2.0)],
        "epsilon": 0.25,
        "description": "Nearly collinear points with tight epsilon. Tests sensitivity to small deviations.",
        "expected_segments": 2  # May need two segments if deviations exceed 0.25.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "description": "Invalid input with repeated x-coordinates. Should raise an error.",
        "expected_segments": None  # Algorithm should reject due to non-strictly increasing x.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1e-10, 0.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "description": "Points with very close x-coordinates. Tests numerical stability.",
        "expected_segments": 1  # Should treat as nearly collinear.
    },
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.5,
        "description": "Single point. Should require no segments or handle gracefully.",
        "expected_segments": 0  # No segments possible with one point.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.01), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.005,
        "description": "Small perturbation in one point. Tests if algorithm detects need for extra segment.",
        "expected_segments": 2  # Likely needs two segments due to 0.01 deviation exceeding 0.005.
    }
]
test_cases25 = [
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5,
        "description": "Basic case with increasing x and varying y, moderate ε, testing general approximation."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.1,
        "description": "All points collinear (y=0), should require only one segment for any ε > 0."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 2.0,
        "description": "Zigzag pattern with large y-deviations, testing ability to merge segments within ε."
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0), (2.0, 4.0)],
        "epsilon": 0.5,
        "description": "Two points with same x (vertical segment), should handle undefined slope or reject invalid input."
    },
    {
        "pw_linear_fx": [(0.0, 1.0)],
        "epsilon": 0.0,
        "description": "Single point, should return zero segments or handle as edge case."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "description": "Two points (single segment), should return one segment for any ε ≥ 0."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.05,
        "description": "Nearly collinear points, small ε, testing precision in approximation."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 0.0), (3.0, 100.0)],
        "epsilon": 50.0,
        "description": "Large y-deviations, large ε, testing if algorithm minimizes segments effectively."
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.0,
        "description": "Zero ε with same x-coordinates, should preserve all segments or handle error."
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.01), (4.0, 0.0)],
        "epsilon": 0.005,
        "description": "Mostly flat with small perturbation, testing sensitivity to small changes."
    }
]
test_cases26 = [
    # Test Case 1: Basic case with small deviation, should require minimal pieces
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 1.1), (3.0, 1.2)],
        'epsilon': 0.2
    },
    # Test Case 2: Collinear points, should require only one piece
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.1
    },
    # Test Case 3: Sharp change in middle, may require multiple pieces
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0)],
        'epsilon': 0.5
    },
    # Test Case 4: Single segment, should require one piece
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 2.0)],
        'epsilon': 0.5
    },
    # Test Case 5: Large epsilon, should allow fewer pieces
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0)],
        'epsilon': 5.0
    },
    # Test Case 6: Small epsilon, may require more pieces
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 1.01), (3.0, 1.02)],
        'epsilon': 0.001
    },
    # Test Case 7: Duplicate x-coordinates, should handle vertical jumps
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.0, 2.0), (2.0, 2.0)],
        'epsilon': 0.5
    },
    # Test Case 8: Large number of points with oscillation
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 1.0), (4.0, -1.0), (5.0, 0.0)],
        'epsilon': 0.5
    },
    # Test Case 9: Extreme values, testing numerical stability
    {
        'pw_linear_fx': [(0.0, 1e6), (1.0, 1e6 + 1), (2.0, 1e6 - 1), (3.0, 1e6)],
        'epsilon': 2.0
    },
    # Test Case 10: Nearly flat with small perturbations
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.01), (2.0, 0.99), (3.0, 1.02), (4.0, 0.98)],
        'epsilon': 0.05
    }
]
test_cases27 = [
    # Test Case 1: Basic case with small number of points
    {
        "points": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    # Test Case 2: Collinear points (should require one segment)
    {
        "points": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    # Test Case 3: Points just within epsilon (should require one segment)
    {
        "points": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.3
    },
    # Test Case 4: Points just outside epsilon (should require multiple segments)
    {
        "points": [(0.0, 0.0), (1.0, 0.6), (2.0, 0.0), (3.0, 0.6)],
        "epsilon": 0.5
    },
    # Test Case 5: Two points (minimum possible, one segment)
    {
        "points": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.5
    },
    # Test Case 6: High-frequency oscillations
    {
        "points": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)],
        "epsilon": 0.2
    },
    # Test Case 7: Repeated x-coordinates (degenerate case)
    {
        "points": [(0.0, 1.0), (0.0, 1.1), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.05
    },
    # Test Case 8: Large dataset with gradual change
    {
        "points": [(x, x + 0.2 * (-1)**x) for x in range(10)],
        "epsilon": 0.3
    },
    # Test Case 9: Extreme y-values
    {
        "points": [(0.0, 1e6), (1.0, 1e6 + 0.1), (2.0, 1e6 - 0.1), (3.0, 1e6)],
        "epsilon": 0.2
    },
    # Test Case 10: Points exactly at epsilon boundary
    {
        "points": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.5
    }
]
test_cases28 = [
    # Test Case 1: Collinear points, should require one piece
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.1
    },
    # Test Case 2: Sharp change, requires multiple pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.5
    },
    # Test Case 3: Small epsilon, forces more pieces
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.2), (3.0, 1.3)],
        "epsilon": 0.05
    },
    # Test Case 4: Large epsilon, allows single piece
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.5), (2.0, 2.0), (3.0, 2.5)],
        "epsilon": 1.0
    },
    # Test Case 5: Single segment (minimum points)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5
    },
    # Test Case 6: Large dataset with gradual changes
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3), (4.0, 0.4), (5.0, 0.5), (6.0, 0.6), (7.0, 0.7), (8.0, 0.8), (9.0, 0.9)],
        "epsilon": 0.1
    },
    # Test Case 7: Negative coordinates
    {
        "pw_linear_fx": [(-2.0, -1.0), (-1.0, -0.5), (0.0, 0.0), (1.0, 0.5)],
        "epsilon": 0.2
    },
    # Test Case 8: Duplicate x-coordinates (invalid input)
    {
        "pw_linear_fx": [(0.0, 1.0), (0.0, 2.0), (1.0, 3.0)],
        "epsilon": 0.5
    },
    # Test Case 9: Non-increasing x-coordinates (invalid input)
    {
        "pw_linear_fx": [(0.0, 1.0), (2.0, 2.0), (1.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.5
    },
    # Test Case 10: High-frequency oscillations
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)],
        "epsilon": 0.2
    }
]
test_cases29 = [
    # Test Case 1: Linear data, should require minimal segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "description": "Perfectly linear data, should be approximated with one segment"
    },
    # Test Case 2: Small oscillations within epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.0)],
        "epsilon": 0.2,
        "description": "Small oscillations within epsilon, should use one segment"
    },
    # Test Case 3: Large deviation requiring multiple segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.5,
        "description": "Step function, should require at least two segments"
    },
    # Test Case 4: Single segment just within epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0)],
        "epsilon": 0.5,
        "description": "Parabolic shape just within epsilon, should use one segment"
    },
    # Test Case 5: Single point far outside epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.5,
        "description": "One point far outside epsilon, should require two segments"
    },
    # Test Case 6: Empty input
    {
        "pw_linear_fx": [],
        "epsilon": 0.5,
        "description": "Empty input, should handle gracefully (e.g., return empty or error)"
    },
    # Test Case 7: Single point
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.5,
        "description": "Single point, should return empty or single point"
    },
    # Test Case 8: Two points
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "description": "Two points, should return one segment"
    },
    # Test Case 9: High-frequency oscillations
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.3), (0.2, -0.3), (0.3, 0.3), (0.4, 0.0)],
        "epsilon": 0.2,
        "description": "High-frequency oscillations, may require multiple segments"
    },
    # Test Case 10: Large epsilon allowing single segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0)],
        "epsilon": 2.0,
        "description": "Large epsilon, should allow single segment for varied data"
    }
]
test_cases30 = [
    {
        "description": "Basic collinear points, should require one segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1
    },
    {
        "description": "Points requiring multiple segments due to large y-deviation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0)],
        "epsilon": 1.0
    },
    {
        "description": "Zero epsilon, should require n segments (no approximation)",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 1.2)],
        "epsilon": 0.0
    },
    {
        "description": "Large epsilon, should allow single segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 10.0
    },
    {
        "description": "Single segment with small deviations",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.3)],
        "epsilon": 0.5
    },
    {
        "description": "Sharp changes, testing oscillation handling",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (1.1, 0.0), (2.0, 5.0), (2.1, 0.0)],
        "epsilon": 1.0
    },
    {
        "description": "Duplicate x-coordinates, should handle gracefully",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 2.0), (2.0, 3.0)],
        "epsilon": 0.5
    },
    {
        "description": "Large dataset with gradual changes",
        "pw_linear_fx": [(float(i), float(i) + 0.2 * (-1)**i) for i in range(10)],
        "epsilon": 0.3
    },
    {
        "description": "Non-uniform x-spacing with significant y-changes",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 2.0), (10.0, 3.0), (10.1, 0.0)],
        "epsilon": 1.0
    },
    {
        "description": "Negative coordinates and boundary epsilon",
        "pw_linear_fx": [(0.0, -1.0), (1.0, -2.0), (2.0, -1.0), (3.0, -3.0)],
        "epsilon": 0.99
    }
]