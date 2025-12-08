#7dec 12:38pm 40 testcases - performing it only once for the experiment

test_cases1 = [
    # --- BASIC & CONSTANT FUNCTION TESTS (Optimal: 1 Piece) ---
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)], "epsilon": 0.1},
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)], "epsilon": 0.0},  # Zero tolerance on constant
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.001), (2.0, -0.001), (3.0, 0.0)], "epsilon": 0.001},  # Barely fits one piece
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 0.0)], "epsilon": 0.0},  # Two points, zero tolerance
    {"pw_linear_fx": [(0.0, 10.0), (1.0, 10.0), (2.0, 10.0), (3.0, 10.0), (4.0, 10.0)], "epsilon": 1.0},

    # --- LINEAR & NEAR-LINEAR FUNCTION TESTS (Optimal: 1 Piece) ---
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.0},  # Perfect line, zero tolerance
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.1},
    # Perfect line, non-zero tolerance
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.9), (3.0, 3.1)], "epsilon": 0.1},  # Line with small noise
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.95), (2.0, 2.05), (3.0, 2.95), (4.0, 4.0)], "epsilon": 0.06},
    # Noise at max tolerance limit
    {"pw_linear_fx": [(0.0, 10.0), (1.0, 9.0), (2.0, 8.0), (3.0, 7.0), (4.0, 6.0)], "epsilon": 0.0},
    # Negative slope perfect line

    # --- SINGLE PEAK/VALLEY TESTS (Optimal: 2 Pieces minimum) ---
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.4},  # Simple V-shape, fits 2 pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.5},
    # Simple V-shape, *just* fits 1 piece (critical error check)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, -1.0), (2.0, 0.0)], "epsilon": 0.4},  # Simple Inverted V-shape
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 2.0), (1.0, 0.0)], "epsilon": 0.5},
    # Sharp V-shape (0.5, 2.0) is the max deviation (2.0)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.001, 10.0), (2.0, 0.0)], "epsilon": 1.0},
    # Near-vertical step up and down, large peak

    # --- STEP FUNCTION / DISCONTINUOUS-LIKE TESTS (Require many pieces) ---
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.001, 1.0), (2.0, 1.0)], "epsilon": 0.1},
    # Single large jump (step function)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)], "epsilon": 0.4},
    # Alternating points (sawtooth-like)
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0)], "epsilon": 0.0},
    # Alternating, zero tolerance (5 pieces)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.1, 0.0), (2.1, 1.0), (2.2, 0.0)], "epsilon": 0.05},  # Tight peaks
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.1, 1.0), (2.0, 1.0), (2.1, 0.0), (3.0, 0.0), (3.1, 1.0)],
     "epsilon": 0.4},  # Block/Stair step

    # --- CONVEX (Parabola) TESTS (Error increases quadratically) ---
    # Points on y = x^2: (0,0), (1,1), (2,4), (3,9), (4,16)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], "epsilon": 1.0},
    # Tolerance large enough for one piece? (Max error is at 2.0, error is (4-3)=1)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], "epsilon": 0.99},
    # Error must exceed tolerance, requiring 2 pieces
    {"pw_linear_fx": [(0.0, 0.0), (2.0, 4.0), (4.0, 16.0)], "epsilon": 0.5},
    # Deviation at 2.0 is 0 (endpoints). Deviation at 1.0: (1.0-2.0)=-1.0. Error needs refinement.
    # Refined Convex Test: Max deviation for line (0,0) to (4,16) is at x=2.0 (y=4). Line passes through (2, 8). Error |4-8|=4.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)], "epsilon": 4.1},
    # Should take 1 piece
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)], "epsilon": 3.9},
    # Must take >1 piece

    # --- CONCAVE (Negative Parabola) TESTS ---
    # Points on y = 4x - x^2: (0,0), (1,3), (2,4), (3,3), (4,0)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 4.0), (3.0, 3.0), (4.0, 0.0)], "epsilon": 1.1},
    # Max error is at (2,4) with line (0,0) to (4,0). Error |4-0|=4.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 4.0), (3.0, 3.0), (4.0, 0.0)], "epsilon": 0.5},
    # Requires multiple pieces due to peak
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 3.0), (2.0, 4.0), (3.0, 3.0), (4.0, 0.0)], "epsilon": 4.0},
    # Boundary case for 1 piece

    # --- SINUSOIDAL / OSCILLATION TESTS ---
    # Points on y = sin(pi*x): (0,0), (0.5, 1), (1,0), (1.5, -1), (2,0)
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, -1.0), (2.0, 0.0)], "epsilon": 0.1},
    # Multiple oscillations, small tolerance
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, -1.0), (2.0, 0.0)], "epsilon": 0.5},
    # Tolerance allows spanning a half-cycle
    {"pw_linear_fx": [(0.0, 0.0), (0.25, 0.7), (0.5, 1.0), (0.75, 0.7), (1.0, 0.0)], "epsilon": 0.1},
    # Higher resolution on a single hump

    # --- MIXED SLOPES & ZIG-ZAG TESTS ---
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 1.0), (4.0, 3.0)], "epsilon": 0.5},
    # Mixed slopes, checking for optimal split
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.001, -1.0), (2.0, 0.0), (3.0, 0.0)], "epsilon": 0.1},
    # Acute turn followed by a constant segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 1.0), (3.0, 10.0)], "epsilon": 2.0},  # Large 'M' shape
    {"pw_linear_fx": [(0.0, 0.0), (0.5, 0.1), (1.0, 0.0), (1.5, 0.1), (2.0, 0.0)], "epsilon": 0.05},
    # Small, rapid oscillations

    # --- ENDPOINT & CRITICAL TOLERANCE TESTS ---
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)], "epsilon": 0.001},
    # Perfect line, tiny tolerance (should still be 1 piece)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.5, 0.0), (2.0, 1.0)], "epsilon": 0.5},
    # Tolerance boundary (error at 1.5 is 0.5)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.5, 0.0), (2.0, 1.0)], "epsilon": 0.49999},
    # Should fail, requiring 2 pieces
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)], "epsilon": 0.0},
    # Minimal case, perfect fit, zero tolerance
    {"pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (20.0, 0.0), (30.0, 0.0), (40.0, 0.0)], "epsilon": 100.0},
    # Very large domain, large tolerance
]
