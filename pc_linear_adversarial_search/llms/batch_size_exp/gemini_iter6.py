#7dec 12:38pm 60 testcases - performing it only once for the experiment
test_cases1 = [
    # 1. Uniform Slopes (Baseline & Simple Linear)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], 'epsilon': 0.01},  # Perfect line, N=5, tight epsilon
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.1), (4.0, 3.9)], 'epsilon': 0.2},   # Slightly perturbed line, should be 1 piece
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)], 'epsilon': 0.0},   # Constant function, epsilon=0 (must be 1 piece)
    {'pw_linear_fx': [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)], 'epsilon': 0.5},             # Example case
    {'pw_linear_fx': [(0.0, 5.0), (1.0, 4.0), (2.0, 3.0), (3.0, 2.0), (4.0, 1.0)], 'epsilon': 1.0},   # Negative slope, large epsilon (should be 1 piece)

    # 2. Abrupt Changes (Sharp Turns - forcing new segments)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 0.0)], 'epsilon': 0.5},   # V-shape sequence (expect many pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.01, 10.0), (2.0, 10.0)], 'epsilon': 0.1},            # Near vertical jump (must be 2 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0, 0.0), (1.0, 0.0), (2.0, 0.0)], 'epsilon': 0.01},  # Duplicate points (should be 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)], 'epsilon': 0.01},  # Duplicate at start of turn
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 10.0), (1.001, 0.0)], 'epsilon': 1.0},                        # Very sharp V-shape, relaxed epsilon

    # 3. Step Functions/Vertical Jumps (High Difficulty)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0)], 'epsilon': 0.49},             # Classic step, tight to 0.5 (must be 2 pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (2.0, 1.0)], 'epsilon': 0.51},             # Classic step, loose (could be 1 piece if algo is aggressive)
    {'pw_linear_fx': [(0.0, 0.0), (0.1, 0.0), (0.2, 1.0), (0.3, 1.0), (0.4, 0.0)], 'epsilon': 0.4},  # Small steps
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0, 10.0), (2.0, 10.0), (2.0, 0.0)], 'epsilon': 4.9}, # Double step, large epsilon
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.1, 10.0), (1.2, 0.0), (2.0, 0.0)], 'epsilon': 1.0}, # Spike

    # 4. Convex/Concave Shapes (Curvature)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.4), (3.0, 0.9), (4.0, 1.6)], 'epsilon': 0.1},  # $y = x^2 / 10$ (convex), tight epsilon
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.8), (3.0, 0.95), (4.0, 1.0)], 'epsilon': 0.05},# $y = \sqrt{x}/2$ (concave), very tight
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, 0.5), (4.0, 0.0)], 'epsilon': 0.2},  # W-shape
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], 'epsilon': 10.0}, # W-shape, very loose epsilon (should be 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.1), (4.0, 0.0)], 'epsilon': 0.01}, # Gentle bump, tight epsilon

    # 5. Small Tolerance (Maximizing Pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0)], 'epsilon': 0.001},# Tiny epsilon, should require max pieces
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], 'epsilon': 1e-10}, # Zero epsilon equivalent (max pieces)
    {'pw_linear_fx': [(0.0, 0.0), (0.1, 0.1), (0.2, 0.0), (0.3, 0.1), (0.4, 0.0)], 'epsilon': 0.005},# Many points, tiny epsilon
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)], 'epsilon': 1e-10}, # Constant function, tiny epsilon (should be 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.001), (2.0, 0.002), (3.0, 0.003)], 'epsilon': 0.0001},    # Points just outside a perfect line

    # 6. Large Tolerance (Minimizing Pieces)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0), (3.0, 10.0), (4.0, 0.0)], 'epsilon': 100.0},# Huge epsilon (should be 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)], 'epsilon': 100.0}, # Constant, huge epsilon (should be 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], 'epsilon': 100.0}, # Perfect line, huge epsilon (should be 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 2.0)], 'epsilon': 2.0},             # V-shape, epsilon large enough
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)], 'epsilon': 4.9},                          # Simple triangle, epsilon close to max deviation

    # 7. Data near Epsilon Boundaries (Critical Edge Cases)
    # A point that is exactly epsilon away from the line (L-infinity error = epsilon)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0)], 'epsilon': 1.0},                          # Midpoint (1.0, 0.0) has max error 1.0. Should be 1 piece.
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.01), (2.0, 0.0)], 'epsilon': 0.5},                         # Midpoint error 1.01. Must force new segment.
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 3.0)], 'epsilon': 0.99},             # First segment fails, forces break.
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)], 'epsilon': 0.5},              # Plateau, max error 0.5 from (0,0)-(3,0) line (should be 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)], 'epsilon': 0.49},             # Plateau, fails 0.5 test, must break.

    # 8. Sequences Designed to Test Optimality (Greedy vs. Optimal)
    # A sequence where a sub-optimal greedy choice fails to cover the maximum possible range.
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0), (5.0, 0.1), (6.0, 0.0)], 'epsilon': 0.06}, # Should be 2 pieces max
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0), (4.0, 1.0), (5.0, 0.0)], 'epsilon': 0.4}, # Two humps, needs 3 pieces if optimal
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)], 'epsilon': 0.5},             # Should be 1 piece, max error 0.5
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)], 'epsilon': 0.49},            # Must be 2 pieces
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.2), (3.0, 0.1), (4.0, 0.0), (5.0, -0.1), (6.0, -0.2)], 'epsilon': 0.15}, # Gentle Sine wave

    # 9. Additional Complex/Boundary Cases (Completion to 60)
    # Negative Y values
    {'pw_linear_fx': [(0.0, 0.0), (1.0, -1.0), (2.0, -2.0), (3.0, -3.0)], 'epsilon': 0.01},          # Negative slope and Y values
    {'pw_linear_fx': [(0.0, 1.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 1.0)], 'epsilon': 0.99}, # Oscillation, almost 1 piece
    {'pw_linear_fx': [(0.0, 1.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 1.0)], 'epsilon': 0.49}, # Oscillation, must be 3 pieces
    {'pw_linear_fx': [(0.0, 0.0), (0.5, 0.0), (1.0, 1.0), (1.5, 1.0), (2.0, 2.0)], 'epsilon': 0.51}, # Horizontal and diagonal segments
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.0001, 0.0), (2.0, 0.0)], 'epsilon': 0.0},           # Coincident points, zero tolerance

    # Extreme Data Range
    {'pw_linear_fx': [(0.0, 1000.0), (1.0, 1000.0), (2.0, 1000.0)], 'epsilon': 0.0},                # Large Y values, constant
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1000.0), (2.0, 2000.0)], 'epsilon': 50.0},                  # Steep slope, large epsilon
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1000.0), (2.0, 0.0)], 'epsilon': 499.0},                     # Spike, almost 1 piece
    {'pw_linear_fx': [(0.0, 0.0), (100.0, 0.0), (200.0, 0.0), (300.0, 1.0)], 'epsilon': 0.1},       # Sparse X, small Y change
    {'pw_linear_fx': [(0.0, 0.0), (10.0, 1.0), (10.1, 0.0), (20.0, 1.0)], 'epsilon': 0.05},          # Small X segment in a large X range

    # High N (Many Points) - Testing efficiency and complexity
    {'pw_linear_fx': [(i, i/10.0 + (i%3)*0.1) for i in range(15)], 'epsilon': 0.1},                   # N=15, varied small perturbation
    {'pw_linear_fx': [(i, 0.0) for i in range(15)] + [(15, 5.0)], 'epsilon': 0.01},                  # Long horizontal followed by a jump
    {'pw_linear_fx': [(i, i**2/100.0) for i in range(15)], 'epsilon': 0.1},                         # $y=x^2$ with many points
    {'pw_linear_fx': [(i, i**2/100.0) for i in range(15)], 'epsilon': 1.0},                         # $y=x^2$ with many points, large epsilon

    # More Boundary & Optimality Checks (Fine-tuning $L_{\infty}$ error)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)], 'epsilon': 0.26},# Should be 2 pieces
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0), (3.0, -0.5), (4.0, 0.0)], 'epsilon': 0.24},# Should be 3 pieces
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)], 'epsilon': 0.5},             # Sharp point at midpoint, max error 0.5 (should be 1 piece)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)], 'epsilon': 0.49},            # Sharp point, fails (must be 2 pieces)

    # Miscellaneous Cases (Ensuring Coverage)
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0), (5.0, 1.0)], 'epsilon': 0.33}, # Extended zig-zag
    {'pw_linear_fx': [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, -0.1), (4.0, 0.0)], 'epsilon': 0.05}, # Small sine, tight fit
]