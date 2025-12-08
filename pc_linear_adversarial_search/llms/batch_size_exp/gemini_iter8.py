#7dec 12:38pm 80 testcases - performing it only once for the experiment
test_cases1 = [
    # ----------------------------------------------------------------------
    # 1. Basic / Simple Linear/Constant Data (1-8)
    # ----------------------------------------------------------------------
    # TC 1-4: Perfectly linear data (should always result in 1 piece).
    # Test for exact fit (ε=0), loose fit, tight fit, and moderate fit.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.0,
     "expected_pieces": 1},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.01,
     "expected_pieces": 1},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 1.0,
     "expected_pieces": 1},
    {"pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)], "epsilon": 0.001,
     "expected_pieces": 1},
    # TC 5-8: Simple concave/convex curve that can be covered by one piece with a large enough ε.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)], "epsilon": 0.5,
     "expected_pieces": 1},  # Single piece fit
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)], "epsilon": 0.0,
     "expected_pieces": 4},  # Requires 4 pieces for ε=0
    {"pw_linear_fx": [(0.0, 4.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 4.0)], "epsilon": 1.0,
     "expected_pieces": 2},  # Symmetric, wide V-shape
    {"pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (0.2, 0.0), (1.0, 10.0), (1.1, 10.0)], "epsilon": 1.0,
     "expected_pieces": 2},  # Steep rise, then flat

    # ----------------------------------------------------------------------
    # 2. Critical Points and ε Alignment (9-16)
    # ----------------------------------------------------------------------
    # TC 9-12: Data where the maximum deviation is exactly ε at a single point (critical for optimality).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces": 1},  # Max deviation = ε
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5 + 1e-9), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces": 2},
    # Max deviation > ε (Test boundary)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5 - 1e-9), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces": 1},
    # Max deviation < ε (Test boundary)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.1), (3.0, 0.0)], "epsilon": 0.1, "expected_pieces": 1},
    # Multiple points on ε boundary
    # TC 13-16: Zig-zag/sawtooth pattern where each peak requires a new segment unless ε is large.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.49,
     "expected_pieces": 4},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.5,
     "expected_pieces": 2},  # Optimal 2-piece fit
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 0.0), (1.5, 0.5), (2.0, 0.0)], "epsilon": 0.1,
     "expected_pieces": 4},
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 0.0), (1.5, 0.5), (2.0, 0.0)], "epsilon": 0.25,
     "expected_pieces": 2},

    # ----------------------------------------------------------------------
    # 3. Vertical (x-coordinate) Variations (17-24)
    # ----------------------------------------------------------------------
    # TC 17-20: Unevenly spaced x-coordinates, which affects the slope and linear interpolation.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (10.0, 1.0), (11.0, 2.0)], "epsilon": 0.1, "expected_pieces": 2},
    # Long flat segment
    {"pw_linear_fx": [(0.0, 0.0), (0.01, 0.0), (1.0, 1.0), (2.0, 2.0)], "epsilon": 0.0, "expected_pieces": 3},
    # Small x-step
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (10.1, 10.0), (10.2, 10.0)], "epsilon": 1.0, "expected_pieces": 2},
    # Steep vertical jump
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (100.0, 1.0)], "epsilon": 0.05,
     "expected_pieces": 4},  # Mix of rapid change and long flat.
    # TC 21-24: Points with repeated x-values (non-function), assuming the input format guarantees unique x. If not, these are invalid.
    # Assuming valid function input (unique x_i, x_{i+1} > x_i) for the standard definition of the problem.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.4},
    # Optimal 2-piece (0,0) to (3,1), then (3,1) to (4,0) - NO! (0,0) to (4,0) with max dev 1.0.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.5,
     "expected_pieces": 2},  # Max deviation 0.5 at (2,1) and (3,1) with line (0,0) to (4,0)
    {"pw_linear_fx": [(0.0, 10.0), (1.0, 0.0), (2.0, 10.0), (3.0, 0.0), (4.0, 10.0)], "epsilon": 2.0,
     "expected_pieces": 2},  # Large amplitude V-shapes
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 20.0), (3.0, 30.0), (4.0, 40.0)], "epsilon": 0.001,
     "expected_pieces": 1},

    # ----------------------------------------------------------------------
    # 4. Floating Point Precision and Numerical Stability (25-32)
    # ----------------------------------------------------------------------
    # TC 25-28: Using small/large numbers and near-zero differences.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1e-9), (2.0, 0.0)], "epsilon": 1e-10, "expected_pieces": 2},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1e-9), (2.0, 0.0)], "epsilon": 1e-9, "expected_pieces": 1},
    {"pw_linear_fx": [(0.0, 1e5), (1.0, 1e5 + 0.1), (2.0, 1e5)], "epsilon": 0.05, "expected_pieces": 2},
    # Large y-offsets, small diff
    {"pw_linear_fx": [(0.0, 1e5), (1.0, 1e5 + 0.1), (2.0, 1e5)], "epsilon": 0.1, "expected_pieces": 1},
    # TC 29-32: Irrational or messy coordinates.
    {"pw_linear_fx": [(0.0, 0.0), (1.0 / 3.0, 0.0), (2.0 / 3.0, 0.0), (1.0, 0.0)], "epsilon": 0.0,
     "expected_pieces": 1},
    {"pw_linear_fx": [(0.0, 0.0), (0.707, 0.1), (1.414, 0.0)], "epsilon": 0.05, "expected_pieces": 2},
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.01), (1.0, 0.0)], "epsilon": 0.01 + 1e-9, "expected_pieces": 1},
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.01), (1.0, 0.0)], "epsilon": 0.01 - 1e-9, "expected_pieces": 2},

    # ----------------------------------------------------------------------
    # 5. Piece Count Transition (33-40)
    # ----------------------------------------------------------------------
    # TC 33-36: Data that requires an exact number of pieces (N) for a small change in ε.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)], "epsilon": 0.4,
     "expected_pieces": 4},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, -1.0), (4.0, 0.0)], "epsilon": 0.5,
     "expected_pieces": 2},  # Transition from 4 to 2 pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)], "epsilon": 0.1},
    # Should be 4 pieces if ε is small enough
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)], "epsilon": 0.25,
     "expected_pieces": 2},  # Transition from 4 to 2
    # TC 37-40: Long sequence of points that could be covered by a single segment except for one outlier.
    {"pw_linear_fx": [(i, 0.0) for i in range(10)] + [(10, 1.0), (11, 0.0)], "epsilon": 0.01, "expected_pieces": 11},
    {"pw_linear_fx": [(i, 0.0) for i in range(10)] + [(5.0, 1.0)] + [(i, 0.0) for i in range(11, 21)], "epsilon": 0.49,
     "expected_pieces": 20},  # Single outlier requiring two pieces
    {"pw_linear_fx": [(i, 0.0) for i in range(10)] + [(5.0, 1.0)] + [(i, 0.0) for i in range(11, 21)], "epsilon": 0.5,
     "expected_pieces": 1},  # Single outlier covered by one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0)], "epsilon": 0.09,
     "expected_pieces": 3},

    # ----------------------------------------------------------------------
    # 6. Step Functions / Discontinuities (41-48)
    # ----------------------------------------------------------------------
    # TC 41-44: Points that form a sharp step, requiring a segment change right before/after the step.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.01, 10.0), (2.0, 10.0)], "epsilon": 0.0, "expected_pieces": 3},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.01, 10.0), (2.0, 10.0)], "epsilon": 1.0, "expected_pieces": 2},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (1.01, 0.0), (2.0, 0.0)], "epsilon": 5.0, "expected_pieces": 2},
    # Large step covered
    {"pw_linear_fx": [(0.0, 0.0), (0.9, 0.0), (1.0, 1.0), (1.1, 0.0), (2.0, 0.0)], "epsilon": 0.1},  # Sharp impulse
    # TC 45-48: Square wave / alternating flat segments.
    {"pw_linear_fx": [(i, i % 2 * 10.0) for i in range(6)], "epsilon": 1.0, "expected_pieces": 5},
    # Requires 5 pieces if ε is small
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 0.0), (5.0, 0.0)], "epsilon": 0.1,
     "expected_pieces": 4},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 0.0), (5.0, 0.0)], "epsilon": 0.5,
     "expected_pieces": 3},
    {"pw_linear_fx": [(i, 10.0) if i % 2 == 0 else (i, 0.0) for i in range(11)], "epsilon": 2.0},
    # Alternating high/low

    # ----------------------------------------------------------------------
    # 7. Concave/Convex Curves (49-56)
    # ----------------------------------------------------------------------
    # TC 49-52: Quadratic data (parabola) that requires multiple pieces for optimality.
    {"pw_linear_fx": [(i, i ** 2) for i in [0, 1, 2, 3, 4]], "epsilon": 0.5},  # Needs at least 2 pieces
    {"pw_linear_fx": [(i, i ** 2) for i in [0, 1, 2, 3, 4, 5]], "epsilon": 0.1},  # Needs many pieces
    {"pw_linear_fx": [(i, -i ** 2) for i in [0, 1, 2, 3, 4]], "epsilon": 0.5},  # Concave down
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.1), (4.0, 0.0)], "epsilon": 0.05,
     "expected_pieces": 2},  # Low amplitude bump
    # TC 53-56: Exponential and other non-polynomial curves.
    {"pw_linear_fx": [(i, 2 ** i) for i in [0.0, 1.0, 1.5, 2.0, 2.5, 3.0]], "epsilon": 0.1},
    {"pw_linear_fx": [(i, 1.0 / i) for i in [1.0, 2.0, 3.0, 4.0, 5.0]], "epsilon": 0.05},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 0.9), (4.0, 1.0)], "epsilon": 0.1,
     "expected_pieces": 2},  # Logarithmic shape
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, -1.0), (3.0, 0.0), (4.0, 1.0)], "epsilon": 0.5,
     "expected_pieces": 2},  # Cosine-like shape

    # ----------------------------------------------------------------------
    # 8. Large Data Sets and Scalability (57-64)
    # ----------------------------------------------------------------------
    # TC 57-60: Long sequence of points (N>10) that can be approximated by one piece.
    {"pw_linear_fx": [(i, i) for i in range(20)], "epsilon": 1e-9, "expected_pieces": 1},
    {"pw_linear_fx": [(i, 0.0) for i in range(20)], "epsilon": 0.0, "expected_pieces": 1},
    {"pw_linear_fx": [(i, 0.0) if i % 2 == 0 else (i, 0.1) for i in range(20)], "epsilon": 0.05 + 1e-9,
     "expected_pieces": 1},
    {"pw_linear_fx": [(i, 0.0) if i % 2 == 0 else (i, 0.1) for i in range(20)], "epsilon": 0.05 - 1e-9,
     "expected_pieces": 10},  # Tight check for optimality
    # TC 61-64: Data that clearly requires a large number of pieces (N/2 or more).
    {"pw_linear_fx": [(i, 1.0 if i % 2 == 0 else -1.0) for i in range(10)], "epsilon": 0.5, "expected_pieces": 5},
    {"pw_linear_fx": [(i, 1.0 if i % 2 == 0 else -1.0) for i in range(10)], "epsilon": 0.99, "expected_pieces": 5},
    {"pw_linear_fx": [(i, 1.0 if i % 2 == 0 else -1.0) for i in range(10)], "epsilon": 1.0, "expected_pieces": 1},
    # Transition from 5 to 1 piece
    {"pw_linear_fx": [(i, (i % 3) / 3.0) for i in range(15)], "epsilon": 0.05},

    # ----------------------------------------------------------------------
    # 9. Initial/Final Segment Edge Cases (65-72)
    # ----------------------------------------------------------------------
    # TC 65-68: Scenarios where the first or last few points define the deviation.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)], "epsilon": 0.1},
    # Deviation at start
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.1},  # Deviation at end
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0)], "epsilon": 0.49},
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 1.0)], "epsilon": 0.5},
    # Optimal fit covers the first peak/trough
    # TC 69-72: Cases with only two or three points.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)], "epsilon": 0.0, "expected_pieces": 1},  # Trivial 2-point case
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.0, "expected_pieces": 2},
    # Trivial 3-point case with no fit for ε=0
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.5, "expected_pieces": 1},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.1, 0.0)], "epsilon": 0.001, "expected_pieces": 2},
    # Very sharp 3-point

    # ----------------------------------------------------------------------
    # 10. Complex / Nested Fits (73-80)
    # ----------------------------------------------------------------------
    # TC 73-76: Data that requires a small segment followed by a large segment for optimality.
    {"pw_linear_fx": [(0.0, 0.0), (0.1, 1.0), (0.2, 0.0), (10.0, 0.0)], "epsilon": 0.01, "expected_pieces": 2},
    # Short V, then long flat
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (100.0, 0.0)], "epsilon": 0.01,
     "expected_pieces": 3},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 10.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 1.0,
     "expected_pieces": 2},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0)], "epsilon": 0.49},
    # Tight fit requiring 3 pieces (0,0) to (2,1) and (2,1) to (5,0) with max deviation 0.4
    # TC 77-80: Complex combination of sharp changes, gentle curves, and flat regions.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.5), (3.0, 1.0), (4.0, 0.0), (5.0, 0.0), (6.0, -1.0)],
     "epsilon": 0.1},
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (10.1, 1.0), (20.0, 1.0), (20.1, 0.0), (30.0, 0.0)], "epsilon": 0.49},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0), (4.0, 0.0), (5.0, -0.1), (6.0, 0.0)],
     "epsilon": 0.05, "expected_pieces": 4},
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0), (4.0, 0.0), (5.0, -0.1), (6.0, 0.0)],
     "epsilon": 0.1, "expected_pieces": 2}  # The entire set can be covered by two segments for this tolerance.
]
