#2 Oct 8:11AM Claude Sonnet 4.5
test_cases1 = [
    {
        "name": "Test 1: Perfect Line - Should Return 1 Piece",
        "description": "All points lie exactly on a line. Optimal is 1 piece (original line).",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (4.0, 8.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "rationale": "Tests if algorithm recognizes collinear points don't need segmentation"
    },

    {
        "name": "Test 2: Near-Line Within Epsilon - Should Return 1 Piece",
        "description": "Points deviate from line but stay within epsilon band.",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.05), (4.0, 3.95)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "rationale": "Tests if algorithm finds global linear approximation when possible"
    },

    {
        "name": "Test 3: Step Function - Requires Multiple Pieces",
        "description": "Sharp step requiring minimum 2 pieces with epsilon=0.5",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "rationale": "Tests handling of discontinuity and greedy vs optimal choice"
    },

    {
        "name": "Test 4: Alternating Pattern - Exposes Greedy Suboptimality",
        "description": "Zigzag pattern where greedy may use 3 pieces but optimal is 2",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.6,
        "expected_min_pieces": 2,
        "rationale": "A greedy algorithm might break early; optimal connects (0,0)→(2,0)→(4,0)"
    },

    {
        "name": "Test 5: Single Outlier Point",
        "description": "One point deviates significantly, forcing a split decision",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3,
        "rationale": "Tests if algorithm handles isolated spikes optimally"
    },

    {
        "name": "Test 6: Convex Curve - Parabolic Arc",
        "description": "Smooth convex curve requiring precise segment count",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "rationale": "Tests approximation of quadratic curve; optimal may use (0,0)→(2,4)→(4,16)"
    },

    {
        "name": "Test 7: Very Tight Epsilon - Forces Many Pieces",
        "description": "Epsilon so small that almost every segment needs to be kept",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.5), (3.0, 2.0), (4.0, 3.0)],
        "epsilon": 0.01,
        "expected_min_pieces": 4,
        "rationale": "Tests behavior with minimal tolerance; may need original segmentation"
    },

    {
        "name": "Test 8: Large Epsilon - Should Return 1 Piece",
        "description": "Epsilon large enough to cover all deviations",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 2.0), (3.0, 7.0), (4.0, 4.0)],
        "epsilon": 10.0,
        "expected_min_pieces": 1,
        "rationale": "Tests if algorithm takes advantage of large tolerance"
    },

    {
        "name": "Test 9: Non-Uniform Spacing with Inflection",
        "description": "Non-uniform x-spacing with curve changing concavity",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 2.0), (1.0, 3.0), (2.0, 3.5), (5.0, 2.0)],
        "epsilon": 0.8,
        "expected_min_pieces": 2,
        "rationale": "Tests handling of varying densities and inflection points"
    },

    {
        "name": "Test 10: Boundary Case - Epsilon Exactly at Threshold",
        "description": "Points where max deviation equals epsilon exactly",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "rationale": "Tests tie-breaking when deviation exactly equals tolerance"
    }
]
test_cases2 = [
    # Test 1: Exact fit - all points collinear, should return 1 piece (2 points)
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.0,
        'description': 'Collinear points with zero tolerance',
        'expected_min_pieces': 1
    },

    # Test 2: Just within tolerance - tests boundary condition
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0 + 0.5), (3.0, 3.0)],
        'epsilon': 0.5,
        'description': 'Middle point exactly at epsilon boundary',
        'expected_min_pieces': 1
    },

    # Test 3: Just outside tolerance - forces split
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0 + 0.51), (3.0, 3.0)],
        'epsilon': 0.5,
        'description': 'Middle point just exceeds epsilon, requires split',
        'expected_min_pieces': 2
    },

    # Test 4: Sine-like oscillation - multiple pieces needed
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        'epsilon': 0.3,
        'description': 'Oscillating function requiring multiple pieces',
        'expected_min_pieces': 4
    },

    # Test 5: Step function - sharp discontinuity
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0)],
        'epsilon': 0.1,
        'description': 'Step function with vertical jump',
        'expected_min_pieces': 3
    },

    # Test 6: Parabola-like curve - tests convex shape
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        'epsilon': 2.0,
        'description': 'Quadratic-like growth pattern',
        'expected_min_pieces': 2
    },

    # Test 7: Large epsilon - everything fits in one piece
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 5.0), (2.0, 3.0), (3.0, 8.0), (4.0, 2.0)],
        'epsilon': 10.0,
        'description': 'Large tolerance allowing single piece',
        'expected_min_pieces': 1
    },

    # Test 8: Minimum case - two points
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0)],
        'epsilon': 0.5,
        'description': 'Minimal input with two points',
        'expected_min_pieces': 1
    },

    # Test 9: Alternating deviation - tests greedy vs optimal
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, 0.4), (4.0, 0.0), (5.0, 0.4)],
        'epsilon': 0.5,
        'description': 'Alternating small deviations that might trap greedy algorithm',
        'expected_min_pieces': 1
    },

    # Test 10: Sharp corner - tests curvature sensitivity
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 10.0), (3.0, 10.1), (4.0, 10.2)],
        'epsilon': 0.5,
        'description': 'Sharp corner with flat regions on both sides',
        'expected_min_pieces': 2
    }
]
test_cases3 = [
    # Test Case 1: Simple linear function - should need only 1 piece
    # All points lie on a line, so one segment should suffice for any reasonable epsilon
    {
        "name": "Perfect linear function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "All points collinear - optimal should be 1 piece"
    },

    # Test Case 2: Two distinct linear segments with sharp transition
    # Forces algorithm to decide optimal breakpoint
    {
        "name": "Two linear segments with different slopes",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 5.0), (4.0, 10.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Sharp slope change - tests if algorithm finds optimal split point"
    },

    # Test Case 3: Convex parabolic shape
    # Tests whether algorithm can skip intermediate points optimally
    {
        "name": "Convex parabola",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 2.0,
        "expected_min_pieces": 2,
        "description": "Parabola with small epsilon - tests greedy vs optimal segment selection"
    },

    # Test Case 4: Oscillating function (sine-like)
    # High frequency changes test if algorithm uses minimal breakpoints
    {
        "name": "Oscillating pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0), (5.0, 1.0), (6.0, 0.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 4,
        "description": "Tests optimal placement for oscillating data"
    },

    # Test Case 5: Single outlier point
    # Tests if algorithm handles outliers optimally vs. creating extra segments
    {
        "name": "Outlier detection",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3,
        "description": "Single outlier - tests if algorithm minimizes segments around anomaly"
    },

    # Test Case 6: Very tight epsilon with small deviations
    # Tests precision and whether algorithm is greedy or truly optimal
    {
        "name": "Tight tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.01), (2.0, 2.02), (3.0, 2.98), (4.0, 4.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 2,
        "description": "Small deviations with tight epsilon - reveals greedy vs optimal behavior"
    },

    # Test Case 7: Step function
    # Multiple horizontal segments - tests optimal merging
    {
        "name": "Step function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0), (4.0, 2.0), (5.0, 5.0), (6.0, 5.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 3,
        "description": "Step function - tests if algorithm optimally groups plateaus"
    },

    # Test Case 8: Logarithmic-like curve
    # Decreasing rate of change tests adaptive segment length
    {
        "name": "Logarithmic curve",
        "pw_linear_fx": [(1.0, 0.0), (2.0, 1.0), (3.0, 1.58), (4.0, 2.0), (5.0, 2.32), (6.0, 2.58), (7.0, 2.81)],
        "epsilon": 0.3,
        "expected_min_pieces": 2,
        "description": "Logarithmic shape - longer segments should work for later points"
    },

    # Test Case 9: V-shape (sharp corner)
    # Tests optimal handling of sharp directional change
    {
        "name": "V-shape with sharp corner",
        "pw_linear_fx": [(0.0, 4.0), (1.0, 3.0), (2.0, 2.0), (3.0, 1.0), (4.0, 2.0), (5.0, 3.0), (6.0, 4.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Symmetric V-shape - should need exactly 2 pieces optimally"
    },

    # Test Case 10: Dense points with gradual curve
    # Many points test if algorithm avoids unnecessary segments
    {
        "name": "Dense sampling of smooth curve",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0),
                         (2.5, 6.25), (3.0, 9.0), (3.5, 12.25), (4.0, 16.0)],
        "epsilon": 1.5,
        "expected_min_pieces": 2,
        "description": "Dense points on parabola - tests if algorithm skips unnecessary intermediate points"
    }
]
test_cases4 = [
    # Test Case 1: Simple horizontal line - should return 1 piece (optimal is entire segment)
    {
        "name": "Horizontal line",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "All points collinear and horizontal, should use 1 piece"
    },

    # Test Case 2: Monotonic convex function - tests if algorithm minimizes pieces
    {
        "name": "Monotonic convex (parabolic)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.5,
        "expected_min_pieces": 2,
        "description": "Convex quadratic curve, optimal should be 2 pieces with epsilon=1.5"
    },

    # Test Case 3: Monotonic concave function - tests opposite curvature
    {
        "name": "Monotonic concave (sqrt-like)",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (4.0, 2.0), (9.0, 3.0), (16.0, 4.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Concave function, tests if algorithm handles opposite curvature optimally"
    },

    # Test Case 4: Alternating curvature - exposes greedy algorithm failures
    {
        "name": "Sine-like alternating curvature",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, -2.0), (4.0, 0.0), (5.0, 2.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 3,
        "description": "Oscillating function - greedy might use 4-5 pieces, optimal is 3"
    },

    # Test Case 5: Sharp corner/discontinuity in derivative
    {
        "name": "V-shape with sharp corner",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 10.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "V-shape requires break at vertex, tests handling of sharp directional change"
    },

    # Test Case 6: Tight epsilon forcing many pieces
    {
        "name": "Tight tolerance on curved function",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0), (2.5, 6.25), (3.0, 9.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 5,
        "description": "Small epsilon on quadratic, tests if algorithm finds minimal segmentation"
    },

    # Test Case 7: Nearly collinear points with outlier
    {
        "name": "Near-collinear with one outlier",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 4.0), (4.0, 4.0), (5.0, 5.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Mostly linear with one outlier point, tests outlier handling"
    },

    # Test Case 8: Large epsilon that should allow single piece
    {
        "name": "Large epsilon allows single approximation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 4.0), (3.0, 5.0), (4.0, 10.0)],
        "epsilon": 5.0,
        "expected_min_pieces": 1,
        "description": "Large tolerance should allow entire function in 1 piece"
    },

    # Test Case 9: Step function - multiple horizontal segments at different levels
    {
        "name": "Step function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3,
        "description": "Vertical jumps require separate pieces, tests handling of discontinuities"
    },

    # Test Case 10: High-frequency oscillation (worst case)
    {
        "name": "High-frequency sawtooth",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0), (2.5, 1.0), (3.0, 0.0)],
        "epsilon": 0.2,
        "expected_min_pieces": 6,
        "description": "Rapid oscillation forces many pieces, tests worst-case behavior"
    }
]
test_cases5 = [
    # Test Case 1: Single segment (trivial case - should return 1 piece)
    {
        "name": "Single segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Trivial case with only one segment"
    },

    # Test Case 2: Two collinear segments (should merge into 1 piece)
    {
        "name": "Collinear segments",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.01,
        "expected_min_pieces": 1,
        "description": "Three points on same line should use 1 piece"
    },

    # Test Case 3: Sharp corner requiring split
    {
        "name": "Sharp corner",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2,
        "description": "90-degree corner forces at least 2 pieces"
    },

    # Test Case 4: Nearly collinear with tight tolerance
    {
        "name": "Nearly collinear - tight epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.01)],
        "epsilon": 0.005,
        "expected_min_pieces": 2,
        "description": "Slight deviation from collinear with tight tolerance"
    },

    # Test Case 5: Nearly collinear with loose tolerance
    {
        "name": "Nearly collinear - loose epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.01)],
        "epsilon": 0.02,
        "expected_min_pieces": 1,
        "description": "Slight deviation tolerable with loose epsilon"
    },

    # Test Case 6: Zigzag pattern
    {
        "name": "Zigzag pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 4,
        "description": "Alternating slopes require multiple pieces"
    },

    # Test Case 7: Step function
    {
        "name": "Step function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 3,
        "description": "Horizontal segments with vertical jumps"
    },

    # Test Case 8: Convex curve (parabola-like)
    {
        "name": "Convex curve",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Quadratic curve with epsilon=1 tests optimal splitting"
    },

    # Test Case 9: High-frequency oscillation
    {
        "name": "High-frequency sine-like",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, -1.0), (2.0, 0.0), (2.5, 1.0), (3.0, 0.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 6,
        "description": "Rapid oscillations with moderate tolerance"
    },

    # Test Case 10: Critical epsilon boundary
    {
        "name": "Epsilon boundary case",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Tests if algorithm correctly handles epsilon exactly at boundary where approximation changes from 2 to 3 pieces"
    }
]
test_cases6 = [
    # Test Case 1: Simple linear function - should return 1 piece (optimal)
    # All points lie on a line y = x, any approximation should use 1 piece
    {
        "name": "Perfect line - should be 1 piece",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1
    },

    # Test Case 2: Two segments that can be merged within tolerance
    # Tests if algorithm recognizes mergeable segments
    {
        "name": "Two near-linear segments mergeable within epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },

    # Test Case 3: Sharp corner that requires split
    # Tests if algorithm correctly identifies when split is necessary
    {
        "name": "Sharp corner exceeding epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3
    },

    # Test Case 4: Staircase function
    # Tests handling of multiple discontinuities
    {
        "name": "Staircase with vertical jumps",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 5
    },

    # Test Case 5: Parabolic-like curve requiring multiple pieces
    # Tests if algorithm finds optimal segmentation for curved data
    {
        "name": "Quadratic curve requiring multiple segments",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0), (5.0, 25.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 3
    },

    # Test Case 6: Oscillating function
    # Tests if algorithm handles alternating slopes optimally
    {
        "name": "Zigzag pattern with tight tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0), (5.0, 2.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 5
    },

    # Test Case 7: Nearly flat with small perturbation
    # Tests if algorithm avoids over-segmentation for noise within tolerance
    {
        "name": "Nearly flat with noise within epsilon",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.95), (3.0, 1.05), (4.0, 1.0), (5.0, 0.98)],
        "epsilon": 0.2,
        "expected_min_pieces": 1
    },

    # Test Case 8: V-shape with minimum point
    # Tests optimal breakpoint selection at valley
    {
        "name": "V-shape requiring split at minimum",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 3.0), (2.0, 1.0), (3.0, 3.0), (4.0, 5.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },

    # Test Case 9: Three segments with middle one nearly flat
    # Tests if algorithm can skip unnecessary breakpoints
    {
        "name": "Three segments with flat middle - tests greedy vs optimal",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 2.1), (3.0, 2.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },

    # Test Case 10: Exponential-like growth with varying curvature
    # Tests if algorithm adapts segment length to local curvature
    {
        "name": "Exponential-like with varying curvature",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0),
                         (5.0, 32.0), (6.0, 64.0)],
        "epsilon": 2.0,
        "expected_min_pieces": 4
    }
]
test_cases7 = [
    # Test 1: Already optimal - single linear segment within tolerance
    {
        "name": "Single linear segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "All points lie on a line, should return 1 piece"
    },

    # Test 2: Epsilon boundary test - point exactly at epsilon distance
    {
        "name": "Point at exact epsilon boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Middle point at exactly epsilon distance from approximating line"
    },

    # Test 3: Point just over epsilon - requires split
    {
        "name": "Point exceeds epsilon by small margin",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.51), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Middle point exceeds epsilon, must split into 2 pieces"
    },

    # Test 4: Convex function - tests greedy vs optimal
    {
        "name": "Convex parabola-like shape",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Quadratic growth pattern, greedy might not be optimal"
    },

    # Test 5: Alternating high-low pattern
    {
        "name": "Zigzag pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 4,
        "description": "Oscillating values, tests if algorithm handles non-monotonic data"
    },

    # Test 6: Plateau with sudden jump
    {
        "name": "Flat region then jump",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 10.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Flat segment followed by jump, tests handling of constant regions"
    },

    # Test 7: Dense clustering near discontinuity
    {
        "name": "Dense points with abrupt change",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (0.31, 5.0), (1.0, 5.0)],
        "epsilon": 0.2,
        "expected_min_pieces": 2,
        "description": "Many close points then sudden jump, exposes greedy inefficiency"
    },

    # Test 8: Concave then convex (inflection point)
    {
        "name": "S-curve with inflection",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 2.5), (3.0, 3.0), (4.0, 5.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 2,
        "description": "Curvature changes direction, tests inflection point handling"
    },

    # Test 9: Minimum case - only 2 points
    {
        "name": "Minimal input - two points",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Edge case: minimum possible input, must return 1 piece"
    },

    # Test 10: Multiple intermediate points all violating epsilon
    {
        "name": "All intermediate points exceed tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 10.0), (3.0, 15.0), (4.0, 4.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 3,
        "description": "Non-linear with large deviations, exposes suboptimal greedy choices"
    }
]
test_cases8 = [
    # Test 1: Triangle inequality edge case - three collinear points with slight deviation
    # Tests if algorithm correctly identifies when middle point can be removed
    {
        "name": "collinear_with_noise",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "description": "Perfectly collinear points - optimal should merge all into 1 piece"
    },

    # Test 2: Alternating pattern that tests greedy vs optimal
    # A greedy algorithm might make suboptimal choices here
    {
        "name": "zigzag_pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, 0.4), (4.0, 0.0), (5.0, 0.4)],
        "epsilon": 0.5,
        "description": "Zigzag where optimal solution requires look-ahead, not greedy choices"
    },

    # Test 3: Step function with epsilon at boundary
    # Tests whether algorithm handles exact epsilon boundary correctly
    {
        "name": "step_function_boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.5,
        "description": "Step function where error exactly equals epsilon at corners"
    },

    # Test 4: Parabolic curve that tests convexity
    # Optimal solution depends on understanding the curvature
    {
        "name": "parabolic_curve",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0), (2.5, 6.25), (3.0, 9.0)],
        "epsilon": 0.3,
        "description": "Quadratic function y=x^2 - tests handling of curved segments"
    },

    # Test 5: Single sharp spike
    # Tests if algorithm can efficiently handle a local anomaly
    {
        "name": "single_spike",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.2,
        "description": "Sharp spike requires separate piece or optimal merging strategy"
    },

    # Test 6: Gradually increasing error
    # Tests if algorithm recognizes when cumulative error exceeds epsilon
    {
        "name": "cumulative_error",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.3), (3.0, 0.6), (4.0, 1.0), (5.0, 1.5)],
        "epsilon": 0.5,
        "description": "Gradual curve where error accumulates - tests error tracking"
    },

    # Test 7: Two distinct linear segments with different slopes
    # Tests if algorithm correctly identifies the breakpoint
    {
        "name": "two_slopes",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 4.5), (4.0, 5.0), (5.0, 5.5)],
        "epsilon": 0.3,
        "description": "Two clear linear regions - optimal must find the transition point"
    },

    # Test 8: Dense sampling with small epsilon
    # Tests scalability and precision with many points
    {
        "name": "dense_sampling",
        "pw_linear_fx": [(i * 0.1, (i * 0.1) ** 1.5) for i in range(21)],
        "epsilon": 0.05,
        "description": "Dense points on y=x^1.5 curve - tests fine-grained optimization"
    },

    # Test 9: Epsilon larger than all deviations
    # Edge case where single piece should be optimal
    {
        "name": "large_epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.2), (4.0, -0.15), (5.0, 0.0)],
        "epsilon": 1.0,
        "description": "Large epsilon should allow single piece for entire function"
    },

    # Test 10: Sine-like oscillation
    # Tests periodic behavior where optimal solution requires understanding pattern
    {
        "name": "oscillating_function",
        "pw_linear_fx": [
            (0.0, 0.0), (0.5, 0.5), (1.0, 0.866), (1.5, 1.0),
            (2.0, 0.866), (2.5, 0.5), (3.0, 0.0), (3.5, -0.5),
            (4.0, -0.866), (4.5, -1.0), (5.0, -0.866), (5.5, -0.5), (6.0, 0.0)
        ],
        "epsilon": 0.4,
        "description": "Sine-like curve - tests symmetric oscillating patterns"
    }
]
test_cases9 = [
    # Test 1: Single segment - should return 1 piece (trivial case)
    {
        "name": "Single segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Simplest case - any algorithm should return 1 piece"
    },

    # Test 2: Collinear points - should return 1 piece
    {
        "name": "Collinear points",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01,
        "description": "All points lie on same line - optimal is 1 piece"
    },

    # Test 3: Near-collinear with tight tolerance - greedy might fail
    {
        "name": "Near-collinear trap",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.05,
        "description": "Greedy might split at point 2, but optimal can fit in 1 piece with proper positioning"
    },

    # Test 4: Step function - tests L∞ norm specifically
    {
        "name": "Step function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (2.0, 2.0), (2.0, 4.0), (3.0, 4.0)],
        "epsilon": 0.5,
        "description": "Vertical jumps expose algorithms that don't handle L∞ correctly"
    },

    # Test 5: Oscillating with amplitude exactly at epsilon
    {
        "name": "Epsilon boundary oscillation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 1.0,
        "description": "Oscillations with amplitude exactly at tolerance - tests boundary conditions"
    },

    # Test 6: Convex then concave - tests lookahead
    {
        "name": "Convex-concave transition",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 3.0), (3.0, 3.5), (4.0, 3.0), (5.0, 2.0), (6.0, 0.0)],
        "epsilon": 0.5,
        "description": "Shape change requires algorithm to look ahead - greedy may create unnecessary splits"
    },

    # Test 7: Long flat region with small perturbation
    {
        "name": "Flat with perturbation",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.3), (4.0, 5.0), (5.0, 5.0), (6.0, 5.0),
                         (7.0, 5.0)],
        "epsilon": 0.2,
        "description": "Single outlier in flat region - optimal uses 1 or 2 pieces depending on epsilon positioning"
    },

    # Test 8: Exponential-like growth - tests non-uniform spacing
    {
        "name": "Exponential growth pattern",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0), (5.0, 32.0)],
        "epsilon": 2.0,
        "description": "Rapid growth with non-uniform curvature - exposes suboptimal early termination"
    },

    # Test 9: Alternating slopes - maximum difficulty for greedy
    {
        "name": "Alternating slopes",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 2.5), (3.0, 4.5), (4.0, 5.0), (5.0, 7.0), (6.0, 7.5)],
        "epsilon": 0.3,
        "description": "Alternating steep and shallow slopes - greedy may split too early"
    },

    # Test 10: High-frequency sine-like pattern
    {
        "name": "High-frequency oscillation",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 0.0), (1.5, -0.5), (2.0, 0.0),
                         (2.5, 0.5), (3.0, 0.0), (3.5, -0.5), (4.0, 0.0)],
        "epsilon": 0.25,
        "description": "High-frequency oscillation - tests if algorithm can balance multiple peaks within tolerance"
    }
]
test_cases10 = [
    # Test Case 1: Single segment that fits within tolerance
    # Should return 1 piece (optimal)
    {
        "name": "single_segment_within_tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Collinear points should be approximated by single segment"
    },

    # Test Case 2: Sharp turn requiring split
    # Should return 2 pieces (optimal)
    {
        "name": "sharp_corner",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2,
        "description": "90-degree turn requires at least 2 pieces for small epsilon"
    },

    # Test Case 3: Alternating pattern (zigzag)
    # Should reveal if algorithm uses greedy approach incorrectly
    {
        "name": "zigzag_pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 3,
        "description": "Alternating pattern tests greedy vs optimal splitting"
    },

    # Test Case 4: Large epsilon allowing full compression
    # Should return 1 piece (optimal)
    {
        "name": "large_epsilon_full_compression",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.5), (2.0, 3.0), (3.0, 4.0), (4.0, 5.5)],
        "epsilon": 2.0,
        "expected_min_pieces": 1,
        "description": "Large epsilon should allow single segment approximation"
    },

    # Test Case 5: Exact boundary case (L∞ norm at exactly epsilon)
    # Tests if algorithm handles equality correctly
    {
        "name": "boundary_at_epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Middle point deviation exactly at epsilon boundary"
    },

    # Test Case 6: Multiple points slightly over tolerance
    # Tests if algorithm finds optimal split point
    {
        "name": "multiple_violations",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.6), (2.0, 1.2), (3.0, 1.8), (4.0, 2.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 2,
        "description": "Multiple points exceed tolerance, tests optimal breakpoint selection"
    },

    # Test Case 7: Dense points with small epsilon
    # Exposes greedy vs dynamic programming approaches
    {
        "name": "dense_sampling",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.3), (1.0, 1.0), (1.5, 2.2), (2.0, 4.0), (2.5, 4.5), (3.0, 4.8)],
        "epsilon": 0.2,
        "expected_min_pieces": 3,
        "description": "Dense sampling with varying slopes tests look-ahead capability"
    },

    # Test Case 8: Flat regions followed by steep change
    # Tests if algorithm handles heterogeneous data
    {
        "name": "flat_then_steep",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 5.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Flat region followed by steep jump"
    },

    # Test Case 9: Near-linear with small perturbations
    # Tests sensitivity to noise-like variations
    {
        "name": "near_linear_perturbations",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.1), (4.0, 3.9), (5.0, 5.0)],
        "epsilon": 0.15,
        "expected_min_pieces": 1,
        "description": "Nearly linear with small noise should compress to 1 piece"
    },

    # Test Case 10: Adversarial case - requires careful split placement
    # Exposes suboptimal greedy algorithms
    {
        "name": "adversarial_split",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.8), (2.0, 0.0), (3.0, 0.8), (4.0, 0.0), (5.0, 0.8), (6.0, 0.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 4,
        "description": "Regular oscillation exposes greedy vs optimal splitting strategies"
    }
]
test_cases11 = [
    # Test Case 1: Straight line - should return 1 piece (optimal is entire line)
    {
        "name": "Straight line",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "All points are collinear, optimal is 1 piece"
    },

    # Test Case 2: Epsilon exactly at boundary - tests if algorithm handles equality correctly
    {
        "name": "Epsilon boundary case",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.5), (3.0, 3.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Middle point deviates exactly epsilon from linear interpolation"
    },

    # Test Case 3: Alternating oscillation - greedy may fail
    {
        "name": "Alternating oscillation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 3,
        "description": "Sawtooth pattern where greedy might not find optimal split points"
    },

    # Test Case 4: Single sharp peak - tests handling of local extrema
    {
        "name": "Sharp peak",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 5.0), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Sharp spike in middle requires splitting"
    },

    # Test Case 5: Multiple points within tolerance - tests greedy vs optimal extension
    {
        "name": "Clustered deviations",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.2), (2.0, 1.8), (3.0, 3.2), (4.0, 3.8), (5.0, 5.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 3,
        "description": "Multiple small deviations that accumulate, greedy may split too early"
    },

    # Test Case 6: Zero epsilon - no tolerance allowed
    {
        "name": "Zero tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "description": "Any deviation requires new piece with zero tolerance"
    },

    # Test Case 7: Large epsilon - should fit everything in one piece
    {
        "name": "Large epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0), (3.0, 3.0), (4.0, 2.0)],
        "epsilon": 5.0,
        "expected_min_pieces": 1,
        "description": "Large tolerance should allow single piece for entire function"
    },

    # Test Case 8: Convex then concave - tests handling of curvature changes
    {
        "name": "Inflection point",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 1.0), (4.0, 1.5), (5.0, 2.5)],
        "epsilon": 0.15,
        "expected_min_pieces": 2,
        "description": "Change in curvature direction may cause greedy to split suboptimally"
    },

    # Test Case 9: Dense then sparse points - tests point distribution sensitivity
    {
        "name": "Non-uniform point distribution",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (5.0, 5.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Dense cluster followed by large gap, tests if algorithm handles varying density"
    },

    # Test Case 10: Staircase pattern - critical for L∞ norm
    {
        "name": "Staircase with overshoot",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3,
        "description": "Vertical steps with horizontal segments test L∞ distance calculation at discontinuities"
    }
]
test_cases12 = [
    # Test Case 1: Triangle wave - tests if algorithm finds optimal split points
    # Optimal: 2 pieces (split at peak), but greedy might use 3
    {
        'name': 'Triangle wave with peak',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 2
    },

    # Test Case 2: Staircase pattern - tests handling of alternating slopes
    # Should require multiple pieces, tests if algorithm uses minimum
    {
        'name': 'Staircase pattern',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0), (4.0, 2.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 4
    },

    # Test Case 3: Sine-like oscillation - classical test for greedy vs optimal
    # Greedy algorithms often fail on smooth oscillations
    {
        'name': 'Smooth oscillation',
        'pw_linear_fx': [(0.0, 0.0), (0.5, 0.5), (1.0, 0.8), (1.5, 0.5), (2.0, 0.0)],
        'epsilon': 0.2,
        'expected_min_pieces': 2
    },

    # Test Case 4: Sharp corner that barely exceeds epsilon
    # Tests boundary condition where error is just above tolerance
    {
        'name': 'Sharp corner at epsilon boundary',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.01), (3.0, 3.0)],
        'epsilon': 0.01,
        'expected_min_pieces': 2
    },

    # Test Case 5: Flat line with single spike
    # Tests if algorithm unnecessarily splits flat regions
    {
        'name': 'Flat with single spike',
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 3.0), (4.0, 1.0), (5.0, 1.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 3
    },

    # Test Case 6: W-shape - tests double valley pattern
    # Optimal solution might merge outer segments
    {
        'name': 'W-shape double valley',
        'pw_linear_fx': [(0.0, 2.0), (1.0, 0.0), (2.0, 2.0), (3.0, 0.0), (4.0, 2.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 4
    },

    # Test Case 7: Nearly collinear points with small deviations
    # Tests if algorithm avoids over-segmentation
    {
        'name': 'Nearly collinear with noise',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.05), (4.0, 4.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 1
    },

    # Test Case 8: Exponential-like growth approximation
    # Tests handling of increasing curvature
    {
        'name': 'Exponential-like growth',
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.5), (2.0, 2.5), (3.0, 4.0), (4.0, 6.5)],
        'epsilon': 0.5,
        'expected_min_pieces': 2
    },

    # Test Case 9: Tight tolerance on curved segment
    # Small epsilon forces more pieces, tests optimality under constraint
    {
        'name': 'Tight tolerance curve',
        'pw_linear_fx': [(0.0, 0.0), (0.25, 0.5), (0.5, 0.75), (0.75, 0.9), (1.0, 1.0)],
        'epsilon': 0.05,
        'expected_min_pieces': 2
    },

    # Test Case 10: Sawtooth pattern with varying amplitudes
    # Tests if algorithm handles non-uniform oscillations optimally
    {
        'name': 'Sawtooth with varying amplitude',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 2.0), (4.0, 0.8), (5.0, 2.5)],
        'epsilon': 0.3,
        'expected_min_pieces': 5
    }
]
test_cases13 = [
    # Test 1: Straight line - optimal is 1 piece (2 points)
    # All points collinear, should reduce to just endpoints
    {
        'name': 'collinear_points',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 1,
        'description': 'All points on a line, optimal should be 2 endpoints (1 piece)'
    },

    # Test 2: Points almost collinear within epsilon
    # Tests if algorithm correctly identifies near-collinear points
    {
        'name': 'near_collinear_within_epsilon',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.1), (4.0, 3.9)],
        'epsilon': 0.15,
        'expected_min_pieces': 1,
        'description': 'Points deviate from line by less than epsilon, should be 1 piece'
    },

    # Test 3: Sharp corner requiring break
    # Single point that forces a break
    {
        'name': 'sharp_corner',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 3,
        'description': 'Sharp vertical jump requires minimum 3 pieces'
    },

    # Test 4: Oscillating function (sine-like)
    # Tests handling of alternating peaks and valleys
    {
        'name': 'oscillating_peaks',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        'epsilon': 0.3,
        'expected_min_pieces': 4,
        'description': 'Oscillating pattern should require multiple pieces'
    },

    # Test 5: Parabolic curve
    # Tests convex curve approximation
    {
        'name': 'parabolic_curve',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 3,
        'description': 'Convex parabola y=x^2 with tight tolerance'
    },

    # Test 6: Step function
    # Tests handling of horizontal segments with jumps
    {
        'name': 'step_function',
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (1.0, 3.0), (2.0, 3.0), (2.0, 5.0), (3.0, 5.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 5,
        'description': 'Vertical jumps at same x-coordinate'
    },

    # Test 7: Single outlier point
    # One point deviates, rest are collinear
    {
        'name': 'single_outlier',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.2,
        'expected_min_pieces': 3,
        'description': 'Single outlier forces segmentation'
    },

    # Test 8: Boundary case - epsilon exactly matches deviation
    # Tests numerical precision at boundary
    {
        'name': 'epsilon_boundary',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.5), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 1,
        'description': 'Maximum deviation exactly equals epsilon'
    },

    # Test 9: Dense sampling of smooth curve
    # Many points on a curve - tests greedy vs optimal
    {
        'name': 'dense_smooth_curve',
        'pw_linear_fx': [(i * 0.5, (i * 0.5) ** 2) for i in range(11)],
        'epsilon': 1.0,
        'expected_min_pieces': 2,
        'description': 'Dense sampling of parabola, tests if algorithm is greedy or optimal'
    },

    # Test 10: Exponential-like growth
    # Tests rapidly changing slope
    {
        'name': 'exponential_growth',
        'pw_linear_fx': [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0), (5.0, 32.0)],
        'epsilon': 1.5,
        'expected_min_pieces': 4,
        'description': 'Exponential growth with increasing slope changes'
    }
]
test_cases14 = [
    # Test Case 1: Simple linear function - should return 1 piece
    # All points are collinear, any epsilon > 0 should allow 1 piece
    {
        'name': 'Collinear points',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 1
    },

    # Test Case 2: Step function with tight tolerance
    # Forces algorithm to use exact segments due to vertical jump
    {
        'name': 'Step function - tight tolerance',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0)],
        'epsilon': 0.01,
        'expected_min_pieces': 3
    },

    # Test Case 3: Parabola approximation
    # Tests greedy vs optimal - y = x^2, greedy might not be optimal
    {
        'name': 'Parabola - exposes greedy suboptimality',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        'epsilon': 2.0,
        'expected_min_pieces': 2
    },

    # Test Case 4: Sine wave sample
    # Non-monotonic function with oscillation
    {
        'name': 'Oscillating function',
        'pw_linear_fx': [(0.0, 0.0), (0.5, 0.48), (1.0, 0.84), (1.5, 1.0), (2.0, 0.91), (2.5, 0.6), (3.0, 0.14)],
        'epsilon': 0.15,
        'expected_min_pieces': 3
    },

    # Test Case 5: Sharp corner that fits within epsilon
    # Tests whether algorithm correctly merges segments when error is within tolerance
    {
        'name': 'Sharp corner within tolerance',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.5, 1.4), (2.0, 2.0)],
        'epsilon': 0.2,
        'expected_min_pieces': 1
    },

    # Test Case 6: Almost collinear with one outlier
    # Tests boundary case where one point barely exceeds epsilon
    {
        'name': 'One point exceeds epsilon',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.5), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.4,
        'expected_min_pieces': 2
    },

    # Test Case 7: Symmetric V-shape
    # Tests handling of symmetry and minimum point
    {
        'name': 'V-shape symmetric',
        'pw_linear_fx': [(0.0, 4.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 4.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 2
    },

    # Test Case 8: High frequency variation
    # Many small oscillations - tests if algorithm avoids oversegmentation
    {
        'name': 'High frequency alternating',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0), (5.0, 0.5)],
        'epsilon': 0.6,
        'expected_min_pieces': 1
    },

    # Test Case 9: Exponential-like growth
    # Increasing curvature - tests adaptive segmentation
    {
        'name': 'Exponential growth pattern',
        'pw_linear_fx': [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0), (5.0, 32.0)],
        'epsilon': 3.0,
        'expected_min_pieces': 3
    },

    # Test Case 10: Plateau with transitions
    # Flat regions with sharp transitions - tests segment boundary detection
    {
        'name': 'Plateau with sharp transitions',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 5.0), (4.0, 10.0), (5.0, 10.0), (6.0, 10.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 2
    }
]
test_cases15 = [
    # Test Case 1: Single segment - should return 1 piece (trivial case)
    {
        "name": "Single segment",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Trivial case with only one segment"
    },

    # Test Case 2: Horizontal line - all points collinear, should return 1 piece
    {
        "name": "Horizontal collinear points",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "All points lie on horizontal line, optimal is 1 piece"
    },

    # Test Case 3: Exactly at epsilon boundary - tests whether algorithm handles boundary correctly
    {
        "name": "Boundary case - exactly at epsilon",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0 + 1.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Last point deviates exactly epsilon from linear approximation"
    },

    # Test Case 4: Zigzag pattern - tests if algorithm minimizes pieces vs greedy approach
    {
        "name": "Zigzag alternating pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 5,
        "description": "Alternating pattern where greedy might not be optimal"
    },

    # Test Case 5: Quadratic-like curve - tests approximation of nonlinear function
    {
        "name": "Quadratic curve approximation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0), (5.0, 25.0)],
        "epsilon": 2.0,
        "expected_min_pieces": 3,
        "description": "y=x^2 curve requiring multiple pieces"
    },

    # Test Case 6: Near-collinear with one outlier - tests if algorithm handles outliers optimally
    {
        "name": "Near-collinear with single outlier",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 5.0), (4.0, 4.0), (5.0, 5.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3,
        "description": "One point deviates significantly, testing optimal split point"
    },

    # Test Case 7: Very tight epsilon - forces many pieces
    {
        "name": "Tight epsilon tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 4.0), (4.0, 6.0)],
        "epsilon": 0.01,
        "expected_min_pieces": 4,
        "description": "Very small epsilon requiring nearly all original segments"
    },

    # Test Case 8: Steep then flat - tests transition handling
    {
        "name": "Steep-to-flat transition",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 11.0), (3.0, 11.5), (4.0, 11.75), (5.0, 11.875)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Steep initial segment followed by gradual flattening"
    },

    # Test Case 9: V-shape - tests sharp corner handling
    {
        "name": "V-shaped function",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 10.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Sharp corner at minimum, tests if algorithm finds optimal split"
    },

    # Test Case 10: Dense sampling of sine-like curve - tests L∞ norm behavior
    {
        "name": "Dense sine-like curve",
        "pw_linear_fx": [
            (0.0, 0.0), (0.5, 0.479), (1.0, 0.841), (1.5, 0.997),
            (2.0, 0.909), (2.5, 0.598), (3.0, 0.141), (3.5, -0.35),
            (4.0, -0.757), (4.5, -0.977), (5.0, -0.959)
        ],
        "epsilon": 0.5,
        "expected_min_pieces": 4,
        "description": "Approximating sin(x) with L∞ norm constraints"
    }
]
test_cases16 = [
    # Test 1: Straight line - should return 1 piece (optimal is always achievable)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "description": "Collinear points - should need only 1 piece",
        "expected_min_pieces": 1
    },

    # Test 2: Almost collinear with epsilon tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.05), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "description": "Nearly collinear within epsilon - tests if algorithm finds optimal 1 piece",
        "expected_min_pieces": 1
    },

    # Test 3: Sharp corner requiring split
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (2.0, 2.0)],
        "epsilon": 0.1,
        "description": "Right angle turn - must use at least 2 pieces",
        "expected_min_pieces": 2
    },

    # Test 4: Sawtooth pattern - critical for greedy vs optimal
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)],
        "epsilon": 0.3,
        "description": "Oscillating pattern - greedy may use more pieces than optimal",
        "expected_min_pieces": 2
    },

    # Test 5: Convex shape testing L∞ norm specifically
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 1.6), (3.0, 2.1), (4.0, 2.4), (5.0, 2.5)],
        "epsilon": 0.5,
        "description": "Diminishing slope (sqrt-like) - tests max vertical deviation",
        "expected_min_pieces": 1
    },

    # Test 6: Tight epsilon exposing suboptimality
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.5), (3.0, 2.0), (4.0, 2.5), (5.0, 4.0)],
        "epsilon": 0.2,
        "description": "Mixed slopes with tight tolerance - exposes greedy early commitment",
        "expected_min_pieces": 2
    },

    # Test 7: Alternating high-low with strategic epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0), (3.0, 3.0), (4.0, 2.0), (5.0, 4.0), (6.0, 3.0)],
        "epsilon": 1.0,
        "description": "Zigzag that could fit in 2 pieces optimally but greedy might use 3+",
        "expected_min_pieces": 2
    },

    # Test 8: Parabola-like curve
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 2.0,
        "description": "Quadratic growth - L∞ deviation grows differently than L2",
        "expected_min_pieces": 2
    },

    # Test 9: Plateau with spike
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 5.0), (4.0, 1.0), (5.0, 1.0), (6.0, 1.0)],
        "epsilon": 0.5,
        "description": "Flat segments with sharp spike - tests handling of outliers",
        "expected_min_pieces": 3
    },

    # Test 10: Dense points with subtle curve
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.24), (1.0, 0.45), (1.5, 0.63), (2.0, 0.78),
                         (2.5, 0.90), (3.0, 0.99), (3.5, 1.05), (4.0, 1.08)],
        "epsilon": 0.15,
        "description": "Many points with gradual curvature - optimal may lookahead vs greedy",
        "expected_min_pieces": 2
    }
]
test_cases17 = [
    # Test Case 1: Already optimal - single segment within tolerance
    {
        "name": "Single segment sufficient",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Straight line - should need only 1 piece"
    },

    # Test Case 2: Epsilon exactly at boundary
    {
        "name": "Epsilon at exact error boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 1.0,
        "description": "Triangle peak at exactly epsilon - tests boundary condition"
    },

    # Test Case 3: Greedy fails - requires look-ahead
    {
        "name": "Greedy trap - requires optimal planning",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0), (5.0, 0.5), (6.0, 0.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 3,
        "description": "Oscillating pattern where greedy spanning creates suboptimal solution"
    },

    # Test Case 4: Very tight tolerance
    {
        "name": "Tight tolerance forces many pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0), (3.0, 3.0), (4.0, 0.0)],
        "epsilon": 0.01,
        "description": "Highly variable function with minimal tolerance"
    },

    # Test Case 5: Zero tolerance
    {
        "name": "Zero tolerance - exact representation",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 3.0), (2.0, 2.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "description": "Must preserve all original segments"
    },

    # Test Case 6: Large tolerance - everything collapses
    {
        "name": "Large tolerance collapses to one piece",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.5), (3.0, 2.0), (4.0, 3.0), (5.0, 4.0)],
        "epsilon": 10.0,
        "expected_min_pieces": 1,
        "description": "Tolerance so large that single segment suffices"
    },

    # Test Case 7: Sawtooth pattern
    {
        "name": "Sawtooth wave",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0), (6.0, 0.0)],
        "epsilon": 0.25,
        "expected_min_pieces": 6,
        "description": "Regular sawtooth requires careful piece placement"
    },

    # Test Case 8: Non-uniform spacing with sharp changes
    {
        "name": "Non-uniform spacing with discontinuities",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 5.0), (0.2, 5.1), (5.0, 5.2), (5.1, 0.0), (10.0, 0.1)],
        "epsilon": 0.5,
        "description": "Sharp jumps mixed with flat regions - tests non-uniform x-spacing"
    },

    # Test Case 9: Convex then concave curvature
    {
        "name": "Mixed curvature segments",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.9), (2.0, 1.6), (3.0, 2.1), (4.0, 2.4), (5.0, 2.5), (6.0, 2.4),
                         (7.0, 2.1)],
        "epsilon": 0.2,
        "description": "Tests algorithm on changing curvature where local decisions matter"
    },

    # Test Case 10: Step function approximation
    {
        "name": "Near step function",
        "pw_linear_fx": [(0.0, 0.0), (0.99, 0.0), (1.0, 10.0), (1.01, 10.0), (2.0, 10.0), (2.99, 10.0), (3.0, 0.0),
                         (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 4,
        "description": "Near-vertical transitions test handling of large slope changes"
    }
]
test_cases18 = [
    # Test Case 1: Simple monotonic function - should be approximated by single segment
    {
        "name": "Monotonic line within tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Perfect line y=x, should need only 1 piece"
    },

    # Test Case 2: Exactly at tolerance boundary
    {
        "name": "Points exactly at epsilon boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Middle points exactly at ±ε from connecting line, tests boundary condition"
    },

    # Test Case 3: Single point exceeds tolerance
    {
        "name": "One point just exceeds tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.51), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Single spike forces split, tests if algorithm minimizes pieces"
    },

    # Test Case 4: Sawtooth pattern
    {
        "name": "Alternating peaks and valleys",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 4,
        "description": "High frequency oscillations, tests greedy vs optimal splitting"
    },

    # Test Case 5: Flat segments with transition
    {
        "name": "Piecewise constant with step",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 3.0), (4.0, 3.0), (5.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2,
        "description": "Two flat regions, tests handling of zero-slope segments"
    },

    # Test Case 6: Quadratic-like curve
    {
        "name": "Parabolic curve approximation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.5,
        "expected_min_pieces": 2,
        "description": "y=x², tests optimal segmentation of convex curve"
    },

    # Test Case 7: Tight cluster then gap
    {
        "name": "Dense points followed by sparse",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (5.0, 5.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 1,
        "description": "Tests if algorithm handles non-uniform point spacing optimally"
    },

    # Test Case 8: V-shape (direction change)
    {
        "name": "Sharp direction reversal",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 10.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "V-shape with minimum at center, tests vertex handling"
    },

    # Test Case 9: Nearly collinear with outlier
    {
        "name": "Mostly linear with single outlier",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 5.0), (4.0, 4.0), (5.0, 5.0)],
        "epsilon": 0.8,
        "expected_min_pieces": 2,
        "description": "Tests if single outlier causes suboptimal multi-segment split"
    },

    # Test Case 10: Exponential-like growth
    {
        "name": "Rapid exponential growth",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0), (5.0, 32.0)],
        "epsilon": 2.0,
        "expected_min_pieces": 3,
        "description": "Tests optimal splitting of exponentially increasing curve"
    }
]
test_cases19 = [
    # Test Case 1: Simple linear function - should return 1 piece (optimal)
    # All points lie on a straight line, so one segment should suffice
    {
        "name": "Perfectly linear function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "All points collinear - tests if algorithm recognizes optimality"
    },

    # Test Case 2: Single sharp corner - requires exactly 2 pieces
    # Tests if algorithm uses minimum pieces at a discontinuity in slope
    {
        "name": "Sharp corner requiring split",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 10.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Sharp angle at x=1 - tests minimum piece detection at corners"
    },

    # Test Case 3: Alternating high-low pattern - worst case for greedy algorithms
    # A greedy algorithm might create many pieces, but optimal is fewer
    {
        "name": "Oscillating pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0), (5.0, 2.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Zigzag pattern - greedy may use 5 pieces, optimal is 2-3"
    },

    # Test Case 4: Convex then concave curve
    # Tests if algorithm handles curvature changes optimally
    {
        "name": "Curvature change",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.5), (2.0, 2.0), (3.0, 2.5), (4.0, 3.5), (5.0, 5.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 2,
        "description": "Change from convex to concave - tests curvature handling"
    },

    # Test Case 5: Clustered points followed by sparse points
    # Tests how algorithm handles non-uniform point distribution
    {
        "name": "Non-uniform spacing",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (10.0, 10.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Dense then sparse points - tests spacing sensitivity"
    },

    # Test Case 6: Minimal points with tight tolerance
    # Edge case with exactly 3 points and very small epsilon
    {
        "name": "Minimal dataset tight tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1)],
        "epsilon": 0.05,
        "expected_min_pieces": 2,
        "description": "3 points, small deviation - tests boundary detection"
    },

    # Test Case 7: Staircase function
    # Multiple flat segments at different levels
    {
        "name": "Staircase pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3,
        "description": "Vertical jumps - tests handling of steep transitions"
    },

    # Test Case 8: Parabolic-like curve
    # Smooth curve that needs strategic breakpoints
    {
        "name": "Smooth parabolic curve",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0), (5.0, 25.0)],
        "epsilon": 2.0,
        "expected_min_pieces": 2,
        "description": "Quadratic growth - tests optimal segmentation of curves"
    },

    # Test Case 9: Nearly flat with one outlier
    # Tests if algorithm wastes pieces on the flat section
    {
        "name": "Flat with outlier",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 5.0), (4.0, 1.0), (5.0, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3,
        "description": "Single spike in flat region - tests outlier handling"
    },

    # Test Case 10: Exponential-like growth with large epsilon
    # Tests if algorithm can use very few pieces when tolerance is generous
    {
        "name": "Exponential growth generous tolerance",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0), (5.0, 32.0), (6.0, 64.0)],
        "epsilon": 10.0,
        "expected_min_pieces": 2,
        "description": "Large epsilon on exponential - tests if algorithm exploits tolerance"
    }
]
test_cases20 = [
    # Test Case 1: Single segment (trivial case - should return 1 piece)
    {
        'name': 'Single segment',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 1,
        'description': 'Trivial case with only one segment'
    },

    # Test Case 2: Collinear points (should compress to 1 piece)
    {
        'name': 'Collinear points',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.0,
        'expected_min_pieces': 1,
        'description': 'All points are collinear, optimal should use single piece'
    },

    # Test Case 3: Nearly collinear with tight epsilon
    {
        'name': 'Nearly collinear - tight epsilon',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.01), (3.0, 3.0)],
        'epsilon': 0.005,
        'expected_min_pieces': 2,
        'description': 'Small deviation requires split; tests if algorithm is greedy vs optimal'
    },

    # Test Case 4: Zigzag pattern (tests greedy failure)
    {
        'name': 'Zigzag pattern',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5), (4.0, 1.0)],
        'epsilon': 0.3,
        'expected_min_pieces': 3,
        'description': 'Oscillating function exposes greedy vs optimal approach'
    },

    # Test Case 5: Sharp corner that forces split
    {
        'name': 'Sharp corner',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0)],
        'epsilon': 0.1,
        'expected_min_pieces': 3,
        'description': 'Vertical-like transition tests handling of extreme slopes'
    },

    # Test Case 6: Convex curve approximation (parabola-like)
    {
        'name': 'Convex parabolic',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        'epsilon': 1.0,
        'expected_min_pieces': 2,
        'description': 'Convex curve tests optimal split point selection'
    },

    # Test Case 7: Alternating slopes (tests lookahead)
    {
        'name': 'Alternating slopes',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 2.5), (3.0, 4.5), (4.0, 5.0), (5.0, 7.0)],
        'epsilon': 0.3,
        'expected_min_pieces': 3,
        'description': 'Slope changes test if algorithm considers future segments'
    },

    # Test Case 8: Zero epsilon (exact representation required)
    {
        'name': 'Zero epsilon',
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        'epsilon': 0.0,
        'expected_min_pieces': 3,
        'description': 'No tolerance allowed, tests if algorithm preserves all segments'
    },

    # Test Case 9: Large epsilon (should compress maximally)
    {
        'name': 'Large epsilon',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.5), (2.0, 2.0), (3.0, 3.5), (4.0, 4.0)],
        'epsilon': 2.0,
        'expected_min_pieces': 1,
        'description': 'Large tolerance should allow maximum compression to single piece'
    },

    # Test Case 10: Critical epsilon boundary (tests exact threshold)
    {
        'name': 'Epsilon boundary case',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 4.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 2,
        'description': 'Epsilon exactly at boundary where one vs two pieces needed; tests L∞ distance calculation accuracy'
    }
]
test_cases21 = [
    # Test Case 1: Simple linear function - should need only 1 piece
    # A perfectly linear segment should be approximable with just 2 points
    {
        "name": "Perfect linear - optimal is 1 piece",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Perfectly linear data should require only 1 piece (2 points)"
    },

    # Test Case 2: Convex arc - tests greedy vs optimal choice
    # A convex arc where greedy might overshoot but optimal waits
    {
        "name": "Convex arc - greedy may fail",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.9), (3.0, 2.7), (4.0, 3.4), (5.0, 4.0)],
        "epsilon": 0.15,
        "expected_min_pieces": 2,
        "description": "Convex curve where greedy extending might miss optimal split point"
    },

    # Test Case 3: Concave then convex - tests segment boundary decisions
    {
        "name": "Concave-convex transition",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 3.0), (3.0, 3.5), (4.0, 4.0), (5.0, 6.0)],
        "epsilon": 0.6,
        "expected_min_pieces": 2,
        "description": "Shape change tests if algorithm recognizes optimal inflection points"
    },

    # Test Case 4: Tight alternating deviations
    # Tests whether algorithm handles oscillations near tolerance boundary
    {
        "name": "Oscillating near epsilon boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0), (5.0, 0.5)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Oscillations exactly at tolerance - optimal should use 1 piece"
    },

    # Test Case 5: Single outlier point
    # Tests if algorithm handles isolated deviations optimally
    {
        "name": "Single outlier in linear data",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.5), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 3,
        "description": "One outlier point should require 3 pieces if handled optimally"
    },

    # Test Case 6: Quadratic-like curve with small epsilon
    # Tests approximation quality vs piece count tradeoff
    {
        "name": "Quadratic curve - tight tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3,
        "description": "Quadratic shape with tight epsilon tests optimal segmentation"
    },

    # Test Case 7: Plateau with endpoints
    # Tests handling of flat regions with non-flat boundaries
    {
        "name": "Plateau with sloped ends",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 3.0), (3.0, 3.0), (4.0, 3.0), (5.0, 5.0), (6.0, 7.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 3,
        "description": "Flat middle section with slopes - tests segment merging decisions"
    },

    # Test Case 8: Exponential-like growth
    # Tests rapidly changing slopes
    {
        "name": "Exponential-like growth curve",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.5), (2.0, 2.5), (3.0, 4.5), (4.0, 8.5), (5.0, 16.5)],
        "epsilon": 1.0,
        "expected_min_pieces": 3,
        "description": "Increasing rate of change tests adaptive segmentation"
    },

    # Test Case 9: Nearly collinear with slight curve
    # Edge case where points are almost but not quite linear
    {
        "name": "Nearly collinear points",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.01), (3.0, 3.0), (4.0, 4.01), (5.0, 5.0)],
        "epsilon": 0.02,
        "expected_min_pieces": 1,
        "description": "Very slight deviations from linearity at tolerance boundary"
    },

    # Test Case 10: Sharp corner/kink
    # Tests handling of discontinuous derivatives
    {
        "name": "Sharp direction change",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (2.5, 2.5), (3.0, 2.0), (4.0, 1.0), (5.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2,
        "description": "Sharp kink at midpoint tests minimum piece detection at corners"
    }
]
test_cases22 = [
    # Test Case 1: Already optimal - single segment within tolerance
    {
        "name": "Single segment sufficient",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Collinear points should need only 1 piece"
    },

    # Test Case 2: Exact boundary case - point lies exactly at epsilon distance
    {
        "name": "Epsilon boundary precision",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.5), (3.0, 3.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Middle point at exactly epsilon=0.5 from line, tests boundary handling"
    },

    # Test Case 3: Just beyond epsilon - requires split
    {
        "name": "Just beyond epsilon threshold",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.501), (3.0, 3.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Point barely exceeds epsilon, must split into 2 pieces"
    },

    # Test Case 4: Greedy vs optimal distinction
    {
        "name": "Greedy trap - requires look-ahead",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.4), (2.0, 0.0), (3.0, 0.4), (4.0, 0.0), (5.0, 0.4), (6.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Greedy might split early; optimal can cover all in 1 piece with epsilon=0.5"
    },

    # Test Case 5: Oscillating function requiring minimum splits
    {
        "name": "High frequency oscillation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 4,
        "description": "Sharp oscillations require many pieces with tight tolerance"
    },

    # Test Case 6: Step function with tight tolerance
    {
        "name": "Step function discontinuity",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 5,
        "description": "Vertical jumps in piecewise function test edge case handling"
    },

    # Test Case 7: Very large epsilon (everything fits in one piece)
    {
        "name": "Large tolerance collapses all",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -3.0), (3.0, 8.0), (4.0, 2.0)],
        "epsilon": 10.0,
        "expected_min_pieces": 1,
        "description": "Large epsilon should allow single piece approximation"
    },

    # Test Case 8: Near-zero epsilon (requires maximum pieces)
    {
        "name": "Near-zero tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.5), (3.0, 2.0), (4.0, 3.0)],
        "epsilon": 0.01,
        "expected_min_pieces": 4,
        "description": "Very tight tolerance forces original piecewise structure"
    },

    # Test Case 9: Non-uniform spacing with hidden simplification
    {
        "name": "Non-uniform x-spacing optimization",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.2), (5.0, 5.0), (10.0, 10.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Wide spacing allows single piece despite multiple points"
    },

    # Test Case 10: Convex/concave segments requiring strategic splits
    {
        "name": "Parabolic arc approximation",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0), (5.0, 25.0)],
        "epsilon": 2.0,
        "expected_min_pieces": 2,
        "description": "Quadratic-like curve tests optimal split point selection for convex functions"
    }
]
test_cases23 = [
    # Test Case 1: Simple linear function - should return 1 piece
    # All points lie on a straight line, so optimal is 1 piece regardless of epsilon
    {
        "name": "Perfect linear - optimal is 1 piece",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1
    },

    # Test Case 2: Two linear segments with exact breakpoint
    # Tests if algorithm correctly identifies necessary breakpoint
    {
        "name": "Two distinct linear segments - needs 2 pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2
    },

    # Test Case 3: Small epsilon forcing more pieces
    # Tests if algorithm handles tight tolerance correctly
    {
        "name": "Tight epsilon on curved data",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.5), (3.0, 1.8), (4.0, 2.0)],
        "epsilon": 0.05,
        "expected_min_pieces": 3
    },

    # Test Case 4: Large epsilon allowing single piece
    # Same data as Test 3 but with relaxed tolerance
    {
        "name": "Relaxed epsilon allows fewer pieces",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.5), (3.0, 1.8), (4.0, 2.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },

    # Test Case 5: Critical epsilon boundary
    # Epsilon exactly at the maximum deviation - tests boundary condition
    {
        "name": "Epsilon at exact boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0), (3.0, 3.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2
    },

    # Test Case 6: Outlier point in middle
    # Single point deviates significantly, tests if algorithm handles spike
    {
        "name": "Single outlier spike",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 1.0), (4.0, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3
    },

    # Test Case 7: Monotonic but non-linear
    # Tests concave function approximation
    {
        "name": "Concave curve - square root like",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (4.0, 2.0), (9.0, 3.0), (16.0, 4.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 2
    },

    # Test Case 8: Alternating direction changes
    # Tests zig-zag pattern requiring multiple pieces
    {
        "name": "Zig-zag pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5), (4.0, 1.0), (5.0, 2.0)],
        "epsilon": 0.2,
        "expected_min_pieces": 4
    },

    # Test Case 9: Dense clustering at boundaries
    # Tests if algorithm handles non-uniform point distribution
    {
        "name": "Non-uniform spacing with clusters",
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (0.2, 0.2), (5.0, 5.0), (5.1, 5.1), (5.2, 5.2)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },

    # Test Case 10: Near-optimal greedy trap
    # Designed to expose greedy vs optimal algorithms
    # Greedy might take 3 pieces, but optimal is 2
    {
        "name": "Greedy algorithm trap",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.9), (3.0, 3.0), (4.0, 3.9), (5.0, 5.0)],
        "epsilon": 0.15,
        "expected_min_pieces": 2
    }
]
test_cases24 = [
    # Test 1: Perfectly collinear points - should collapse to 1 piece
    (
        [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        0.5,
        1,
        "Perfectly collinear points - optimal is 1 piece"
    ),

    # Test 2: Near-collinear within epsilon - should collapse to 1 piece
    (
        [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.05), (4.0, 3.95)],
        0.1,
        1,
        "Near-collinear within epsilon - tests if algorithm exploits full epsilon budget"
    ),

    # Test 3: Sharp corner exceeding epsilon - requires at least 2 pieces
    (
        [(0.0, 0.0), (1.0, 0.0), (1.0, 2.0), (2.0, 2.0)],
        0.5,
        2,
        "90-degree corner - cannot be approximated with 1 piece under given epsilon"
    ),

    # Test 4: Oscillating data - tests greedy vs optimal
    (
        [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        0.3,
        3,
        "Zigzag pattern - greedy might use 4 pieces, optimal uses 3"
    ),

    # Test 5: Boundary case - epsilon exactly at threshold
    (
        [(0.0, 0.0), (1.0, 1.0), (2.0, 2.5), (3.0, 3.0)],
        0.5,
        1,
        "Maximum deviation exactly at epsilon - tests boundary handling"
    ),

    # Test 6: Convex curve approximation
    (
        [(0.0, 0.0), (1.0, 0.5), (2.0, 1.5), (3.0, 3.0), (4.0, 5.0)],
        0.4,
        2,
        "Convex quadratic-like curve - tests if algorithm finds optimal split point"
    ),

    # Test 7: Very small epsilon requiring many pieces
    (
        [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        0.05,
        3,
        "Small epsilon on oscillating data - tests precision handling"
    ),

    # Test 8: Large epsilon allowing single piece despite variation
    (
        [(0.0, 0.0), (1.0, 3.0), (2.0, 1.0), (3.0, 4.0), (4.0, 2.0)],
        5.0,
        1,
        "Large epsilon - all variations within tolerance"
    ),

    # Test 9: Three linear segments with different slopes
    (
        [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 4.0), (4.0, 6.0), (5.0, 6.0), (6.0, 6.0)],
        0.3,
        3,
        "Three distinct linear segments - tests segment detection"
    ),

    # Test 10: Dense points with subtle curvature
    (
        [(0.0, 0.0), (0.5, 0.3), (1.0, 0.8), (1.5, 1.5), (2.0, 2.4), (2.5, 3.5), (3.0, 4.8)],
        0.2,
        2,
        "Parabolic-like curve with dense sampling - tests if algorithm finds global optimum vs local greedy choice"
    )
]
test_cases25 = [
    # Test Case 1: Already optimal - single piece suffices
    # A straight line should need only 1 piece regardless of epsilon
    {
        'name': 'Straight line - optimal is 1 piece',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 1,
        'description': 'Collinear points should be approximated by a single piece'
    },

    # Test Case 2: Sharp turn forcing split
    # Tests if algorithm detects when a point forces a new piece
    {
        'name': 'Sharp V-shape requiring 2 pieces',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 2,
        'description': 'V-shape with apex exceeding epsilon from single line'
    },

    # Test Case 3: Boundary case - point exactly at epsilon
    # Tests whether algorithm handles boundary correctly
    {
        'name': 'Point exactly at epsilon boundary',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.1)],
        'epsilon': 0.1,
        'expected_min_pieces': 1,
        'description': 'Last point is exactly at epsilon tolerance from the line'
    },

    # Test Case 4: Greedy vs optimal tradeoff
    # A greedy algorithm might split early when a later split is more optimal
    {
        'name': 'Greedy trap - early vs late split decision',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.9), (2.0, 2.0), (3.0, 2.9), (4.0, 4.0), (5.0, 5.1)],
        'epsilon': 1.0,
        'expected_min_pieces': 2,
        'description': 'Tests if algorithm greedily splits too early instead of finding optimal split points'
    },

    # Test Case 5: Alternating oscillations
    # Tests handling of oscillating data that might confuse segment selection
    {
        'name': 'Oscillating sawtooth pattern',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5), (4.0, 1.0), (5.0, 2.0)],
        'epsilon': 0.3,
        'expected_min_pieces': 3,
        'description': 'Oscillating pattern tests optimal piece placement'
    },

    # Test Case 6: Dense clustering with outlier
    # Tests if algorithm handles clusters efficiently
    {
        'name': 'Clustered points with distant outlier',
        'pw_linear_fx': [(0.0, 0.0), (0.1, 0.05), (0.2, 0.1), (0.3, 0.15), (5.0, 5.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 2,
        'description': 'Tests handling of dense cluster followed by distant point'
    },

    # Test Case 7: Staircase pattern
    # Tests optimal segmentation of piecewise constant sections
    {
        'name': 'Staircase with plateaus',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0), (4.0, 4.0), (5.0, 4.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 3,
        'description': 'Horizontal segments connected by vertical jumps'
    },

    # Test Case 8: Very tight epsilon exposing sub-optimality
    # Small epsilon might expose whether algorithm finds truly minimal pieces
    {
        'name': 'Tight epsilon on curved approximation',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 1.414), (3.0, 1.732), (4.0, 2.0)],
        'epsilon': 0.01,
        'expected_min_pieces': 3,
        'description': 'Approximating sqrt(x) with very tight tolerance'
    },

    # Test Case 9: Single sharp spike
    # Tests if algorithm optimally handles one anomalous point
    {
        'name': 'Single spike in otherwise flat line',
        'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 5.0), (3.0, 1.0), (4.0, 1.0)],
        'epsilon': 0.5,
        'expected_min_pieces': 3,
        'description': 'One spike point requires 2 additional pieces for optimal coverage'
    },

    # Test Case 10: Long gradual curve
    # Tests whether algorithm uses minimum pieces for smooth transitions
    {
        'name': 'Parabolic curve requiring multiple pieces',
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0), (5.0, 25.0)],
        'epsilon': 2.0,
        'expected_min_pieces': 3,
        'description': 'Quadratic function y=x^2 with moderate epsilon'
    }
]
test_cases26 = [
    # Test 1: Straight line - should return 1 piece (optimal = 2 points)
    # All points are collinear, single segment should suffice
    {
        "name": "Straight line",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "optimal_pieces": 1,
        "description": "Collinear points should require only 1 piece"
    },

    # Test 2: Two distinct slopes - requires at least 2 pieces
    # Sharp transition at x=2 that cannot be smoothed within epsilon
    {
        "name": "Two distinct slopes",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 5.0), (4.0, 8.0)],
        "epsilon": 0.5,
        "optimal_pieces": 2,
        "description": "Sharp slope change requires 2 pieces"
    },

    # Test 3: Oscillating function - tests greedy vs optimal
    # This exposes whether algorithm is greedy or truly optimal
    {
        "name": "Oscillating pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0), (5.0, 2.0)],
        "epsilon": 0.3,
        "optimal_pieces": 5,
        "description": "Oscillations test if algorithm handles periodic patterns optimally"
    },

    # Test 4: Single spike - tests if algorithm splits correctly
    # Middle point creates deviation that may require strategic splitting
    {
        "name": "Single spike",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "optimal_pieces": 2,
        "description": "Isolated spike should require 2 pieces minimum"
    },

    # Test 5: Gradual curve - tests approximation quality
    # Parabolic-like shape tests if algorithm finds minimum pieces for smooth curves
    {
        "name": "Parabolic curve",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0), (5.0, 25.0)],
        "epsilon": 2.0,
        "optimal_pieces": 2,
        "description": "Smooth curve tests approximation with larger epsilon"
    },

    # Test 6: Very tight epsilon - should need many pieces
    # Tests behavior with strict tolerance
    {
        "name": "Tight tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.1,
        "optimal_pieces": 4,
        "description": "Tight epsilon should require piece per segment or near it"
    },

    # Test 7: Flat then steep - tests transition handling
    # Exposes if algorithm looks ahead or is purely greedy
    {
        "name": "Flat to steep transition",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 10.0), (5.0, 19.0)],
        "epsilon": 1.0,
        "optimal_pieces": 2,
        "description": "Long flat followed by steep change tests look-ahead capability"
    },

    # Test 8: Three-segment zigzag - classic optimality test
    # Tests if algorithm can find that 2 pieces work when greedy might use 3
    {
        "name": "Zigzag optimality test",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5), (4.0, 1.0)],
        "epsilon": 0.6,
        "optimal_pieces": 2,
        "description": "Tests if algorithm finds optimal split vs greedy approach"
    },

    # Test 9: Near-collinear with outlier - boundary case
    # Tests L∞ norm specifically - one point slightly outside tolerance
    {
        "name": "Near-collinear with outlier",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.05), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.04,
        "optimal_pieces": 2,
        "description": "Single outlier just beyond epsilon tests L∞ norm sensitivity"
    },

    # Test 10: Symmetric V-shape - tests splitting symmetry
    # Tests if algorithm handles symmetric patterns optimally
    {
        "name": "Symmetric V-shape",
        "pw_linear_fx": [(0.0, 10.0), (1.0, 7.0), (2.0, 4.0), (3.0, 1.0), (4.0, 4.0), (5.0, 7.0), (6.0, 10.0)],
        "epsilon": 0.5,
        "optimal_pieces": 2,
        "description": "Symmetric pattern should be handled with 2 pieces optimally"
    }
]
test_cases27 = [
    # Test 1: Simple linear function - should need only 1 piece
    # All points lie on same line y = x
    {
        "name": "perfect_linear",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Collinear points should collapse to single segment"
    },

    # Test 2: Step function - exposes if algorithm handles discontinuous slopes
    {
        "name": "step_function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 5,
        "description": "Vertical-like jumps require separate pieces"
    },

    # Test 3: Convex curve approximation - tests greedy vs optimal
    # Points on y = x^2, scaled down
    {
        "name": "convex_parabola",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6), (5.0, 2.5)],
        "epsilon": 0.15,
        "expected_min_pieces": 2,
        "description": "Convex curve - greedy might use 3+ pieces, optimal uses 2"
    },

    # Test 4: Alternating high-low - exposes look-ahead failures
    {
        "name": "zigzag_pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.5), (3.0, 2.5), (4.0, 1.0), (5.0, 3.0)],
        "epsilon": 0.6,
        "expected_min_pieces": 3,
        "description": "Zigzag pattern tests if algorithm considers future points"
    },

    # Test 5: Boundary case - point exactly at epsilon distance
    {
        "name": "epsilon_boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.5), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Middle point at exactly epsilon distance from line"
    },

    # Test 6: Narrow spike - tests if algorithm handles sharp local deviations
    {
        "name": "narrow_spike",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.1), (2.5, 5.0), (3.0, 1.2), (4.0, 2.0), (5.0, 3.0)],
        "epsilon": 0.3,
        "expected_min_pieces": 3,
        "description": "Sharp spike in middle - tests local vs global optimization"
    },

    # Test 7: Dense then sparse points - tests adaptation to point density
    {
        "name": "varying_density",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (5.0, 5.0), (10.0, 10.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Non-uniform spacing shouldn't affect linear segments"
    },

    # Test 8: S-curve (inflection point) - critical for optimal piece selection
    {
        "name": "s_curve_inflection",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 4.5), (3.0, 5.0), (4.0, 5.5), (5.0, 6.5), (6.0, 10.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "S-curve with inflection point - greedy may split prematurely"
    },

    # Test 9: Multiple small deviations vs one large deviation
    {
        "name": "many_small_vs_one_large",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.2), (2.0, 1.8), (3.0, 3.2), (4.0, 3.8), (5.0, 5.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Multiple small errors accumulating - tests error measurement"
    },

    # Test 10: Minimal dataset with tight tolerance
    {
        "name": "minimal_three_points",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 1.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Triangle shape - middle point far from line through endpoints"
    }
]
test_cases28 = [
    # Test Case 1: Triangle wave - tests if algorithm can skip intermediate points
    # Optimal: 2 pieces (start to peak to end), Greedy might use 3
    {
        "name": "Triangle wave",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "description": "Simple triangle - optimal skips the peak if epsilon allows"
    },

    # Test Case 2: Staircase with small steps
    # Tests if algorithm can bridge multiple small steps with one segment
    {
        "name": "Staircase pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "description": "Linear staircase - should reduce to single segment if epsilon permits"
    },

    # Test Case 3: Saddle point (concave then convex)
    # Critical for testing lookahead - can we skip the middle inflection point?
    {
        "name": "Saddle/inflection point",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 2.0), (3.0, 4.0)],
        "epsilon": 0.6,
        "description": "Flat section in middle - tests if algorithm looks ahead past inflection"
    },

    # Test Case 4: Oscillating wave
    # Tests ability to capture multiple peaks with minimal segments
    {
        "name": "Oscillating wave",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.3,
        "description": "Multiple oscillations - greedy might stop too early"
    },

    # Test Case 5: Nearly collinear points
    # Tests numerical stability and whether algorithm recognizes near-linearity
    {
        "name": "Nearly collinear",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.01), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.05,
        "description": "Small deviation from linearity - should use 2 pieces optimally"
    },

    # Test Case 6: Sharp corner followed by gentle curve
    # Tests if algorithm prioritizes based on error magnitude
    {
        "name": "Mixed curvature",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.5, 5.0), (2.0, 5.5), (3.0, 6.0)],
        "epsilon": 1.0,
        "description": "Sharp corner then gentle - tests error distribution strategy"
    },

    # Test Case 7: Parabolic arc
    # Classic test for piecewise linear approximation optimality
    {
        "name": "Parabolic arc",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 2.0,
        "description": "Quadratic function - tests optimal chord placement"
    },

    # Test Case 8: Plateau with endpoints
    # Tests handling of flat regions
    {
        "name": "Plateau boundaries",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0), (5.0, 0.0)],
        "epsilon": 0.8,
        "description": "Flat plateau - can algorithm skip all middle points?"
    },

    # Test Case 9: Exponential-like growth
    # Tests with increasing slope magnitude
    {
        "name": "Exponential growth",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0), (5.0, 32.0)],
        "epsilon": 3.0,
        "description": "Accelerating growth - tests adaptive segmentation"
    },

    # Test Case 10: Zig-zag with precise epsilon boundary
    # Critical edge case: epsilon is exactly at the threshold
    {
        "name": "Epsilon boundary case",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.5,
        "description": "Maximum deviation equals epsilon - tests boundary conditions"
    }
]
test_cases29 = [
    # Test case 1: Simple linear function - should return 1 piece (optimal)
    # All points lie on a line, so single segment should suffice
    {
        "name": "Simple linear function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Perfectly linear data - optimal is 1 piece"
    },

    # Test case 2: Two clear segments - requires exactly 2 pieces
    # Sharp corner at (2.0, 2.0) forces a break
    {
        "name": "Two distinct linear segments",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 0.0), (4.0, -2.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 2,
        "description": "Sharp direction change requires 2 pieces minimum"
    },

    # Test case 3: Epsilon boundary test - point exactly at epsilon distance
    # Tests whether algorithm handles boundary correctly (≤ε vs <ε)
    {
        "name": "Epsilon boundary case",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.5)],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Middle point deviation exactly at epsilon - tests boundary handling"
    },

    # Test case 4: Oscillating function - greedy vs optimal challenge
    # Greedy might break too early, optimal waits for better breakpoint
    {
        "name": "Oscillating sawtooth pattern",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.5), (3.0, 1.5), (4.0, 1.0), (5.0, 2.0)],
        "epsilon": 0.6,
        "expected_min_pieces": 2,
        "description": "Oscillations test greedy vs optimal segmentation"
    },

    # Test case 5: Single peak/valley - tests look-ahead capability
    # Optimal algorithm should recognize symmetry and minimize pieces
    {
        "name": "Symmetric peak",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Symmetric peak tests if algorithm finds optimal break point"
    },

    # Test case 6: Nearly flat with small perturbations
    # Tests numerical stability and whether small deviations are handled correctly
    {
        "name": "Nearly flat with noise",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.1), (2.0, 0.95), (3.0, 1.05), (4.0, 1.0)],
        "epsilon": 0.2,
        "expected_min_pieces": 1,
        "description": "Small perturbations within epsilon - should use 1 piece"
    },

    # Test case 7: Increasing curvature - exposes greedy early termination
    # Later points deviate more, greedy might segment too early
    {
        "name": "Quadratic-like curvature",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 2.0,
        "expected_min_pieces": 2,
        "description": "Increasing curvature tests optimal breakpoint selection"
    },

    # Test case 8: Multiple tight epsilon violations
    # Tests whether algorithm correctly handles multiple constraint violations
    {
        "name": "Dense violations",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_min_pieces": 4,
        "description": "Rapid oscillations require many pieces"
    },

    # Test case 9: Zero epsilon - strictest case
    # Every non-collinear point must start a new segment
    {
        "name": "Zero tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.5), (3.0, 2.0)],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "description": "Zero epsilon requires exact piecewise linear representation"
    },

    # Test case 10: Large epsilon - everything fits in one piece
    # Tests if algorithm correctly identifies when no segmentation needed
    {
        "name": "Large epsilon - single piece sufficient",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, -3.0), (3.0, 7.0), (4.0, 2.0)],
        "epsilon": 10.0,
        "expected_min_pieces": 1,
        "description": "Large epsilon allows all points in single segment"
    }
]
test_cases30 = [
    # Test 1: Collinear points - should return 1 piece (optimal is single segment)
    {
        "name": "Collinear points",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.01,
        "expected_min_pieces": 1,
        "description": "All points lie on same line y=x, should use 1 piece"
    },

    # Test 2: Almost collinear with small epsilon - tests precision
    {
        "name": "Almost collinear with tight tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.001), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0005,
        "expected_min_pieces": 2,
        "description": "Middle point deviates by 0.001, epsilon=0.0005 requires split"
    },

    # Test 3: Step function - each segment needs separate piece
    {
        "name": "Step function",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.0, 5.0), (2.0, 5.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 0.1,
        "description": "Vertical jumps force multiple pieces"
    },

    # Test 4: Greedy vs optimal - triangle wave where greedy fails
    {
        "name": "Triangle wave - greedy trap",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0), (5.0, 2.0), (6.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3,
        "description": "Greedy might use more pieces than optimal dynamic programming"
    },

    # Test 5: Epsilon at critical boundary
    {
        "name": "Epsilon at exact boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "description": "Max deviation is exactly 1.0, should fit in 1 piece with epsilon=1.0"
    },

    # Test 6: Epsilon just below critical boundary
    {
        "name": "Epsilon below boundary",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 4.0)],
        "epsilon": 0.999,
        "expected_min_pieces": 2,
        "description": "Max deviation is 1.0, epsilon=0.999 requires split"
    },

    # Test 7: Single hump - tests optimal segment selection
    {
        "name": "Parabolic hump",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.5), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.25,
        "expected_min_pieces": 2,
        "description": "Symmetric curve tests if algorithm finds optimal split point"
    },

    # Test 8: Sawtooth pattern - repeating structure
    {
        "name": "Sawtooth wave",
        "pw_linear_fx": [(0.0, 0.0), (0.5, 3.0), (1.0, 0.0), (1.5, 3.0), (2.0, 0.0), (2.5, 3.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_min_pieces": 6,
        "description": "High frequency changes force many pieces"
    },

    # Test 9: Long flat segment followed by sudden change
    {
        "name": "Flat then spike",
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0), (5.0, 15.0), (6.0, 15.0)],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Tests if algorithm handles long segments optimally"
    },

    # Test 10: Exponential-like growth - tests non-uniform spacing
    {
        "name": "Exponential growth pattern",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0), (5.0, 32.0)],
        "epsilon": 2.0,
        "expected_min_pieces": 3,
        "description": "Increasing slopes test adaptive approximation"
    }
]