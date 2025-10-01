#30 Sept few-shot prompt with Copilot Think Deeper mode 4:38PM
test_cases1 = [
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 2.1), (3.0, 2.95)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 4.5)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 1.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 1.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.3
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 4.0), (3.0, 8.0), (4.0, 16.0)],
        "epsilon": 2.0
    },
]
test_cases2 = [
    # 1. Minimal case: exactly two points ⇒ always one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_segments": 1,
    },

    # 2. Three perfectly colinear points ⇒ one segment at zero tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0,
        "expected_segments": 1,
    },

    # 3. Small noise within ε ⇒ still one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.0)],
        "epsilon": 0.2,
        "expected_segments": 1,
    },

    # 4. Noise just outside ε ⇒ must split into two segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.0)],
        "epsilon": 0.05,
        "expected_segments": 2,
    },

    # 5. Flat horizontal line (many points) ⇒ one segment even at zero tolerance
    {
        "pw_linear_fx": [
            (0.0, 5.0), (1.0, 5.0), (2.0, 5.0),
            (3.0, 5.0), (4.0, 5.0), (5.0, 5.0)
        ],
        "epsilon": 0.0,
        "expected_segments": 1,
    },

    # 6. Sharp “V” shape ⇒ middle point forces two segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_segments": 2,
    },

    # 7. Single outlier at end ⇒ should isolate that region
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 5.0)],
        "epsilon": 1.0,
        "expected_segments": 2,
    },

    # 8. Concave shape requiring exactly two pieces
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 1.0), (2.0, 2.0),
            (3.0, 1.0), (4.0, 0.0)
        ],
        "epsilon": 0.5,
        "expected_segments": 2,
    },

    # 9. Duplicate consecutive points ⇒ duplicates should be ignored
    {
        "pw_linear_fx": [
            (0.0, 0.0), (0.0, 0.0),
            (1.0, 1.0), (2.0, 2.0)
        ],
        "epsilon": 0.0,
        "expected_segments": 1,
    },

    # 10. Unsorted x‐values ⇒ algorithm should sort or handle gracefully
    {
        "pw_linear_fx": [(3.0, 3.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0,
        "expected_segments": 1,
    },
]
test_cases3 = [
    {
        # perfectly collinear, zero tolerance → 1 segment
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        # collinear but uneven x‐spacing, small epsilon → 1 segment
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (3.0, 3.0), (6.0, 6.0)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    {
        # slight noisy deviations within epsilon → 1 segment
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.05), (3.0, 2.95)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        # very large epsilon swallows any shape → 1 segment
        "pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)],
        "epsilon": 5.0,
        "expected_pieces": 1
    },
    {
        # zero tolerance on a simple “V” shape forces two segments
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 2
    },
    {
        # rapid zigzag with small epsilon → max one‐per‐interval
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    {
        # step function (flat, jump, flat) with zero tolerance → 2 segments
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0),
                         (3.0, 5.0), (4.0, 5.0), (5.0, 5.0)],
        "epsilon": 0.0,
        "expected_pieces": 2
    },
    {
        # small plateau within epsilon then big jump → 2 segments
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.05), (2.0, 0.0), (3.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        # valley shape with moderate epsilon allows two pieces
        "pw_linear_fx": [(0.0, 10.0), (1.0, 8.0), (2.0, 6.0),
                         (3.0, 8.0), (4.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        # three true linear pieces (up, flat, down) with zero tolerance → 3 segments
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0),
                         (2.0, 1.0), (3.0, 1.0),
                         (4.0, 0.0), (5.0, -1.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    }
]
test_cases4 = [
    # 1. Constant function: all y-values identical → one segment for any ε ≥ 0
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },

    # 2. Perfect linear function: exactly on y = 2x → one segment at ε = 0
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },

    # 3. Small noise within tolerance: noisy around y = 2x but max deviation 0.1
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.1), (2.0, 3.9), (3.0, 6.05)],
        "epsilon": 0.2,
        "expected_pieces": 1
    },

    # 4. Same noisy data but tighter tolerance → must break at each small segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.1), (2.0, 3.9), (3.0, 6.05)],
        "epsilon": 0.05,
        "expected_pieces": 3
    },

    # 5. Quadratic growth with small ε → no long straight approximation possible
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 0.5,
        "expected_pieces": 3
    },

    # 6. Same quadratic data but huge ε → one segment covers entire curve
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 10.0,
        "expected_pieces": 1
    },

    # 7. Step function (plateaus and a jump) → one piece per flat region
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 10.0), (3.0, 10.0), (4.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces": 3
    },

    # 8. Only two points → always a single segment regardless of ε
    {
        "pw_linear_fx": [(0.0, 0.0), (100.0, 100.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },

    # 9. Rapid oscillation (sin-like) → cannot merge across peaks with small ε
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, -1.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 4
    },

    # 10. Non-uniform x-spacing requiring a break under tight ε
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.1, 1.2), (5.0, 5.0), (10.0, 10.0)],
        "epsilon": 0.05,
        "expected_pieces": 2
    }
]
test_cases5 = [
    # Case 1: Single point should require 0 segments
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.1,
        "expected_segments": 0
    },

    # Case 2: Two points always form exactly one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # Case 3: Three perfectly colinear points, zero tolerance → one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # Case 4: Colinear with small noise, within epsilon → one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.1)],
        "epsilon": 0.15,
        "expected_segments": 1
    },

    # Case 5: Colinear with noise exceeding epsilon → splits into 2 pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.2), (2.0, 1.9), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_segments": 2
    },

    # Case 6: V-shape (kink) requiring exactly two segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.0,
        "expected_segments": 2
    },

    # Case 7: Parabola sampled, coarse tolerance → two segments suffice
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0,
        "expected_segments": 2
    },

    # Case 8: Parabola sampled, tight tolerance → each interval needed (4 segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.2,
        "expected_segments": 4
    },

    # Case 9: Zigzag oscillation, small epsilon → one segment per jump (4 segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_segments": 4
    },

    # Case 10: Zigzag oscillation, large epsilon absorbs all → one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 2.5,
        "expected_segments": 1
    }
]
test_cases6 = [
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0), (3.0, 7.0), (4.0, 9.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (2.0, 5.0), (4.0, 5.0), (6.0, 5.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 1.05), (1.0, 3.10), (2.0, 4.90), (3.0, 7.00), (4.0, 9.10)],
        "epsilon": 0.2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 6.0), (4.0, 8.0), (5.0, 10.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0), (4.0, 0.0), (5.0, 0.0)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -5.0), (3.0, 8.0), (4.0, 2.0)],
        "epsilon": 10.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 8.0), (3.0, 27.0), (4.0, 64.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 1.0), (2.5, 0.5), (3.0, 1.5), (5.0, 1.0)],
        "epsilon": 0.4
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0)],
        "epsilon": 5.0
    }
]
test_cases7 = [
    # 1. Minimal input: exactly two points → always one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
     "epsilon":    0.0,
     "expected":   1},

    # 2. Constant function: any ε ≥ 0 → one flat segment
    {"pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
     "epsilon":    0.0,
     "expected":   1},

    # 3. Perfectly linear multi-point: exact line → one segment even at ε = 0
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
     "epsilon":    0.0,
     "expected":   1},

    # 4. Small noise within ε: all deviations < 0.1 → still one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.02), (4.0, 4.00)],
     "epsilon":    0.10,
     "expected":   1},

    # 5. Noise exactly on the ε boundary: max deviation = 0.1 → OK as one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.10), (2.0, 2.00), (3.0, 3.00), (4.0, 4.00)],
     "epsilon":    0.10,
     "expected":   1},

    # 6. Single “break” point exceeds ε → must split into 2 segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 6.0)],
     "epsilon":    0.50,
     "expected":   2},

    # 7. Plateau then incline: two distinct slopes → 2 segments at tight ε
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 3.0), (4.0, 6.0)],
     "epsilon":    0.10,
     "expected":   2},

    # 8. Single large outlier in the middle → three segments around the spike
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 3.0), (4.0, 4.0)],
     "epsilon":    1.00,
     "expected":   3},

    # 9. Oscillating “peaks and valleys”: no two consecutive points are collinear → n segments
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
     "epsilon":    0.50,
     "expected":   4},

    # 10. Same oscillation but huge ε → everything collapses into one segment
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
     "epsilon":    2.00,
     "expected":   1},
]
test_cases8 = [
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0)],
        "epsilon": 0.0,
        "expected_num_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_num_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0), (3.0, 7.0)],
        "epsilon": 0.0,
        "expected_num_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.4), (1.0, 1.2), (2.0, 2.1), (3.0, 2.8)],
        "epsilon": 0.5,
        "expected_num_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_num_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_num_segments": 4
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 2.0,
        "expected_num_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 0.1,
        "expected_num_segments": 4
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0),
                         (3.0, 6.0), (4.0, 8.0), (5.0, 10.0)],
        "epsilon": 0.1,
        "expected_num_segments": 2
    },
    {
        "pw_linear_fx": [(3.0, 3.0), (1.0, 1.0), (2.0, 2.0), (0.0, 0.0)],
        "epsilon": 0.0,
        "expected_num_segments": 1
    }
]
test_cases9 = [
    # 1. Perfectly colinear points, zero tolerance → 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0),
                         (1.0, 1.0),
                         (2.0, 2.0),
                         (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 2. Linear with tiny noise all within ε → still 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0),
                         (1.0, 1.1),
                         (2.0, 1.9),
                         (3.0, 3.05)],
        "epsilon": 0.1,
        "expected_segments": 1
    },

    # 3. One point exactly at the ε boundary → 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0),
                         (1.0, 1.0),
                         (2.0, 2.2),
                         (3.0, 3.0)],
        "epsilon": 0.2,
        "expected_segments": 1
    },

    # 4. One point slightly above ε → forces a split into 2 segments
    {
        "pw_linear_fx": [(0.0, 0.0),
                         (1.0, 1.0),
                         (2.0, 2.3),
                         (3.0, 3.0)],
        "epsilon": 0.2,
        "expected_segments": 2
    },

    # 5. Quadratic points (0→16) with ε=1 → can do in 2 optimal segments
    {
        "pw_linear_fx": [(0.0, 0.0),
                         (1.0, 1.0),
                         (2.0, 4.0),
                         (3.0, 9.0),
                         (4.0, 16.0)],
        "epsilon": 1.0,
        "expected_segments": 2
    },

    # 6. Same quadratic but tighter ε=0.5 → needs 3 segments
    {
        "pw_linear_fx": [(0.0, 0.0),
                         (1.0, 1.0),
                         (2.0, 4.0),
                         (3.0, 9.0),
                         (4.0, 16.0)],
        "epsilon": 0.5,
        "expected_segments": 3
    },

    # 7. Constant function, zero tolerance → trivially 1 segment
    {
        "pw_linear_fx": [(0.0, 5.0),
                         (2.0, 5.0),
                         (4.0, 5.0),
                         (6.0, 5.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 8. Two-point curve → always exactly 1 segment
    {
        "pw_linear_fx": [(0.0, 1.0),
                         (10.0, 10.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 9. Zig-zag data with moderate ε → still needs a segment per jump
    {
        "pw_linear_fx": [(0.0, 0.0),
                         (1.0, 5.0),
                         (2.0, 0.0),
                         (3.0, 5.0),
                         (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_segments": 4
    },

    # 10. Degenerate: duplicate x-values → should raise an error
    {
        "pw_linear_fx": [(0.0, 0.0),
                         (0.0, 1.0),  # duplicate x
                         (1.0, 1.0),
                         (2.0, 0.0)],
        "epsilon": 0.5,
        "expect_exception": ValueError
    }
]
test_cases10 = [
    # 1. Perfect straight line, uniform spacing → one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.1,
        "expected_segments": 1
    },

    # 2. Perfect straight line, non-uniform x spacing → still one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (0.2, 0.2), (1.5, 1.5), (4.0, 4.0)],
        "epsilon": 0.01,
        "expected_segments": 1
    },

    # 3. Tiny vertical noise around y=x → one segment when ε covers noise
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.04)],
        "epsilon": 0.1,
        "expected_segments": 1
    },

    # 4. Zero tolerance must reproduce every original piece
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.0,
        "expected_segments": 3
    },

    # 5. Sharp “V” shape forces two pieces even for moderate ε
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_segments": 2
    },

    # 6. Zig-zag alternation can’t be consolidated → all original pieces
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1), (6, 0)],
        "epsilon": 0.1,
        "expected_segments": 6
    },

    # 7. Duplicate points shouldn’t break optimal merging
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.05,
        "expected_segments": 1
    },

    # 8. Single extreme outlier reintroduces every piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.5,
        "expected_segments": 4
    },

    # 9. Plateau then ramp can collapse for large ε
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.5), (4.0, 4.0)],
        "epsilon": 0.6,
        "expected_segments": 1
    },

    # 10. Plateau then ramp with small ε must split at slope change
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 3.0), (4.0, 6.0)],
        "epsilon": 0.1,
        "expected_segments": 2
    }
]


test_cases11 = [
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.05), (3.0, 3.0)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, -0.5), (3.0, 0.4), (4.0, 0.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.1), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 2.0), (3.0, 2.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.0
    }
]
test_cases12 = [
    # 1. Exactly two points → always one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 2. Single point → zero segments needed
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.0,
        "expected_segments": 0
    },

    # 3. Perfectly linear (no error) → can collapse to one segment
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 4.0), (2.0, 6.0), (3.0, 8.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 4. Linear + small jitter within ε → still one segment
    {
        "pw_linear_fx": [(0.0, 1.1), (1.0, 2.0), (2.0, 2.9), (3.0, 4.1)],
        "epsilon": 0.2,
        "expected_segments": 1
    },

    # 5. Same jitter but ε slightly too small → forces at least two pieces
    {
        "pw_linear_fx": [(0.0, 1.1), (1.0, 2.0), (2.0, 2.9), (3.0, 4.1)],
        "epsilon": 0.05,
        "expected_segments": 2
    },

    # 6. V-shape → cannot approximate with one line unless ε ≥ 2
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 1.0,
        "expected_segments": 2
    },

    # 7. Step function with small ε → two flat pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 1.0,
        "expected_segments": 2
    },

    # 8. Same step but large ε → one sloping line suffices
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 5.0,
        "expected_segments": 1
    },

    # 9. Single extreme outlier in the middle → splits into four pieces at ε=1
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 50.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1.0,
        "expected_segments": 4
    },

    # 10. Plateau → slope → plateau
    #   Should yield three segments: flat, rising, flat
    {
        "pw_linear_fx": [
            (0.0, 5.0), (1.0, 5.0), (2.0, 5.0),
            (3.0, 10.0), (4.0, 15.0),
            (5.0, 15.0), (6.0, 15.0)
        ],
        "epsilon": 0.5,
        "expected_segments": 3
    }
]
test_cases13 = [
    # 1. Perfectly linear (y = 2x + 1), zero tolerance → just 1 segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0), (3.0, 7.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 2. Perfectly linear with slack → still 1 segment even for ε > 0
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 4.0), (4.0, 8.0)],
        "epsilon": 10.0,
        "expected_segments": 1
    },

    # 3. Constant function, zero tolerance → 1 segment
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 4. Single big outlier in the middle forces two segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 0.0)],
        "epsilon": 5.0,
        "expected_segments": 2
    },

    # 5. Noisy line: deviations within ε → collapses to one segment
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.05), (4.0, 4.0)
        ],
        "epsilon": 0.2,
        "expected_segments": 1
    },

    # 6. Noise just above ε at one point → splits into two optimal pieces
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 1.2), (2.0, 1.8), (3.0, 3.5)
        ],
        "epsilon": 0.25,
        "expected_segments": 2
    },

    # 7. Plateau then jump: two flat regions → 2 segments at ε = 1
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 0.0), (2.0, 0.0),
            (3.0, 10.0), (4.0, 10.0), (5.0, 10.0)
        ],
        "epsilon": 1.0,
        "expected_segments": 2
    },

    # 8. Two distinct slopes, exact boundary at x=3, zero tolerance → 2 segments
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0),
            (4.0, 9.0), (5.0, 12.0)
        ],
        "epsilon": 0.0,
        "expected_segments": 2
    },

    # 9. Duplicate points should be ignored; whole is linear → 1 segment
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 1.0), (1.0, 1.0),
            (2.0, 2.0), (3.0, 3.0)
        ],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 10. Single data point: no segments needed → 0 segments
    {
        "pw_linear_fx": [(42.0, 7.0)],
        "epsilon": 0.5,
        "expected_segments": 0
    }
]
# 10 edge-case test inputs for a piecewise-linear approximation under the L∞ norm.
# Each case is a dict with keys "pw_linear_fx", "epsilon", and "expected_segments".

test_cases14 = [
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (4.0, 4.0), (6.0, 6.0)],
        "epsilon": 1e-6,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.5), (4.0, 1.0)],
        "epsilon": 0.2,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.05), (4.0, 0.0)],
        "epsilon": 0.2,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 100.0), (4.0, 0.0)],
        "epsilon": 5.0,
        "expected_segments": 3
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 4.0), (4.0, 4.0)],
        "epsilon": 1.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0001), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_segments": 3
    },
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (2.5, 2.4),
            (5.0, 5.0),
            (7.5, 2.6),
            (10.0, 0.0)
        ],
        "epsilon": 0.5,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, -1.0), (2.0, -2.0), (3.0, 1.0), (4.0, 2.0)],
        "epsilon": 0.5,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 5.0), (2.0, -3.0), (3.0, 4.0), (4.0, 0.0)],
        "epsilon": 100.0,
        "expected_segments": 1
    },
]
# Test cases for piecewise linear approximation under the L∞ norm.
# Each dict has keys 'pw_linear_fx', 'epsilon' and the expected minimum number of segments.

test_cases15 = [
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 3.0), (1.0, 3.0), (2.0, 3.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1e-6,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0)],
        "epsilon": 0.0,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.2), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.2,
        "expected_segments": 4
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 4.0), (2.0, 3.0), (3.0, 2.0), (4.0, 1.0)],
        "epsilon": 0.01,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 1.0000001),
            (2.0, 1.9999999),
            (3.0, 3.0000001),
            (4.0, 6.0)
        ],
        "epsilon": 1e-6,
        "expected_segments": 2
    }
]

test_cases16 = [
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 1.9), (3.0, 3.05)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.2), (2.0, 2.3), (3.0, 3.5)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 0.0),
            (2.0, 5.0), (3.0, 5.0),
            (4.0,10.0), (5.0,10.0)
        ],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [
            (0.0,  0.0),
            (0.1,  1.0),
            (1.5,  1.0),
            (2.5,  2.5),
            (10.0,10.0)
        ],
        "epsilon": 5.0
    },
    {
        "pw_linear_fx": [
            (0.0,  0.0),
            (1.0,  1.0),
            (2.0,  4.0),
            (3.0,  9.0),
            (4.0, 16.0)
        ],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 2.0),
            (2.0, 3.0),
            (3.0, 2.0),
            (4.0, 0.0)
        ],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 42.0)],
        "epsilon": 1.0
    }
]
test_cases17 = [
    # 1. Minimal input: just two points → always one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    # 2. Perfectly linear but epsilon zero → merge to one
    {
        "pw_linear_fx": [(0.0, 2.0), (1.0, 3.0), (2.0, 4.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    # 3. Constant function with zero tolerance → one flat segment
    {
        "pw_linear_fx": [(0.0, 10.0), (2.0, 10.0), (5.0, 10.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    # 4. Small outlier within epsilon → still one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0)],
        "epsilon": 0.15,
        "expected_segments": 1
    },
    # 5. Single “kink” too sharp → must split into two
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.5,
        "expected_segments": 2
    },
    # 6. V-shape: valley depth just below tolerance → one segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, -1.9), (2.0, 0.0)],
        "epsilon": 2.0,
        "expected_segments": 1
    },
    # 7. V-shape: valley depth just above tolerance → two segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, -2.1), (2.0, 0.0)],
        "epsilon": 2.0,
        "expected_segments": 2
    },
    # 8. Oscillation around zero, epsilon small → many pieces
    {
        "pw_linear_fx": [(i, (-1)**i * 0.5) for i in range(6)],
        "epsilon": 0.1,
        "expected_segments": 5
    },
    # 9. Large epsilon swallows all noise → one segment
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0), (2.0, 0.0), (3.0, 3.0), (4.0, 1.0)],
        "epsilon": 5.0,
        "expected_segments": 1
    },
    # 10. Monotonic but non-linear curve, zero tolerance → every original piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.2), (2.0, 2.8), (3.0, 4.5), (4.0, 7.0)],
        "epsilon": 0.0,
        "expected_segments": 4
    }
]
test_cases18 = [
    # 1. Minimal input: just 1 segment → always 1 piece
    {
        "name": "two_points_trivial",
        "pw_linear_fx": [(0.0, 0.0), (5.0, 5.0)],
        "epsilon": 0.1,
        "expected_pieces": 1,
    },

    # 2. Perfectly collinear, zero tolerance → still 1 piece
    {
        "name": "collinear_zero_eps",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_pieces": 1,
    },

    # 3. Slight noise within epsilon → should collapse to 1 piece
    {
        "name": "noisy_within_tolerance",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.05), (3.0, 3.0)],
        "epsilon": 0.15,
        "expected_pieces": 1,
    },

    # 4. Midpoint out‐of‐tolerance → requires split into 2 pieces
    {
        "name": "one_outlier_requires_split",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.2), (2.0, 2.5)],
        "epsilon": 0.1,
        "expected_pieces": 2,
    },

    # 5. Constant function, zero tolerance → 1 piece no matter how many points
    {
        "name": "constant_function",
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 1,
    },

    # 6. Step function with zero tolerance → every change of slope is a new piece
    {
        "name": "step_function_zero_eps",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0),
                         (2.0, 5.0), (3.0, 5.0),
                         (4.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 4,
    },

    # 7. Unsorted x input – algorithm must sort or error
    {
        "name": "unsorted_input",
        "pw_linear_fx": [(0.0, 0.0), (2.0, 0.1), (1.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.2,
        "expected_pieces": 2,
    },

    # 8. Very large epsilon → collapse entire curve into 1 piece
    {
        "name": "high_tolerance_single_piece",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, -10.0), (3.0, 0.0)],
        "epsilon": 20.0,
        "expected_pieces": 1,
    },

    # 9. Exact parabola, zero tolerance → no three are collinear, so n-1 pieces
    {
        "name": "parabola_zero_eps",
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 0.0,
        "expected_pieces": 3,
    },

    # 10. Floating‐point precision edge: tiny jitter around a line
    {
        "name": "precision_boundary",
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 1.0 + 1e-10),
            (2.0, 2.0 - 1e-10),
            (3.0, 3.0 + 5e-10)
        ],
        "epsilon": 1e-9,
        "expected_pieces": 1,
    },
]
test_cases19 = [
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.52), (1.0, 0.98), (1.5, 1.48)],
        "epsilon": 0.05
    },
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (0.5, 0.5),
            (1.0, 1.0),
            (1.5, 3.0),    # outlier
            (2.0, 2.0)
        ],
        "epsilon": 0.2
    },
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.9
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 1.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.5708, 1.0), (3.1416, 0.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [
            (-2.0, 4.0),
            (-1.0, 1.0),
            ( 0.0, 0.0),
            ( 1.0, 1.0),
            ( 2.0, 4.0)
        ],
        "epsilon": 1.0
    }
]
test_cases20 = [
    # 1. Trivial 2‐point line, zero tolerance → always 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },

    # 2. Constant function, multiple points, zero tolerance → 1 segment
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },

    # 3. Noisy but almost linear (error ≤0.1) → should compress to a single segment
    {
        "pw_linear_fx": [(0.0, 0.1), (1.0, 1.05), (2.0, 2.00), (3.0, 3.02)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },

    # 4. Quadratic curve y=x^2 sampled at [0,…,4], ε=1 → needs exactly 2 segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },

    # 5. Zigzag alternating peaks, tight ε=0.5 → no merging, uses max segments (n−1)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 4
    },

    # 6. Two flat clusters with a jump in between, small ε → exactly 2 segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0), (4.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },

    # 7. Invalid input: duplicate x‐values (should raise or return error)
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.5,
        "expected_pieces": None    # expecting the implementation to detect/raise error
    },

    # 8. Strictly decreasing line with slight ε → still exactly 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, -1.0), (2.0, -2.0), (3.0, -3.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },

    # 9. Zero tolerance but tiny noise → forces a new segment at every step
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.001), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_pieces": 3
    },

    # 10. Wildly varying y but huge ε → everything in one big segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 5.0), (3.0, 15.0), (4.0, 7.0)],
        "epsilon": 20.0,
        "expected_pieces": 1
    },
]
test_cases21 = [
    # 1. Minimal case: exactly two points → always one piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_num_pieces": 1
    },

    # 2. Perfectly colinear, zero tolerance → still one piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.0,
        "expected_num_pieces": 1
    },

    # 3. Slight noise under ε → should collapse to one piece
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 1.05),
            (2.0, 2.02),
            (3.0, 3.08),
            (4.0, 3.95)
        ],
        "epsilon": 0.1,
        "expected_num_pieces": 1
    },

    # 4. Single “corner” just outside ε → forces two pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0)],
        "epsilon": 0.1,
        "expected_num_pieces": 2
    },

    # 5. Two flat plateaus with a vertical jump in between → three natural pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0),
                         (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.0,
        "expected_num_pieces": 3
    },

    # 6. Zig-zag alternating ±1 around zero, zero tolerance → one piece per interval
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 0.0),
            (3.0, 1.0),
            (4.0, 0.0)
        ],
        "epsilon": 0.0,
        "expected_num_pieces": 4
    },

    # 7. One period of sin(x) sampled at integers, moderate ε → should fit in three segments
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 0.84),
            (2.0, 0.91),
            (3.0, 0.14),
            (4.0, -0.76),
            (5.0, -0.96),
            (6.0, -0.28)
        ],
        "epsilon": 0.5,
        "expected_num_pieces": 3
    },

    # 8. Duplicate-x entry → invalid; algorithm should raise an error / reject
    {
        "pw_linear_fx": [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        "epsilon": 0.1,
        "expected_num_pieces": "error"
    },

    # 9. Non-monotonic x → invalid ordering; expect rejection
    {
        "pw_linear_fx": [(1.0, 1.0), (0.0, 0.0), (2.0, 2.0)],
        "epsilon": 0.1,
        "expected_num_pieces": "error"
    },

    # 10. Large random noise around y=x, ε just above the noise bound → one piece
    {
        "pw_linear_fx": [
            (i, i + offset) for i, offset in enumerate(
                [0.05, -0.08, 0.03, -0.07, 0.02, -0.09, 0.01, -0.04, 0.06, -0.05]
            )
        ],
        "epsilon": 0.1,
        "expected_num_pieces": 1
    }
]
test_cases22 = [
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.95), (3.0, 3.02), (4.0, 4.00)],
        "epsilon": 0.10,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.10), (2.0, 1.90), (3.0, 3.10), (4.0, 3.90)],
        "epsilon": 0.10,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 5.0), (4.0, 5.0)],
        "epsilon": 0.10,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)],
        "epsilon": 1.0,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.999,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.02), (2.0, 1.97), (3.0, 3.01),
                         (4.0, 3.98), (5.0, 5.03), (6.0, 5.99)],
        "epsilon": 0.05,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 3.0), (3.0, 2.0), (4.0, 0.0)],
        "epsilon": 0.50,
        "expected_segments": 2
    },
]
# Each test case is a dict with keys 'pw_linear_fx', 'epsilon', and 'expected_pieces'
test_cases23 = [
    {
        'pw_linear_fx': [(0.0, 0.0)],
        'epsilon': 0.0,
        'expected_pieces': 0
    },
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0)],
        'epsilon': 0.0,
        'expected_pieces': 1
    },
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        'epsilon': 0.0,
        'expected_pieces': 1
    },
    {
        'pw_linear_fx': [(0.0, 5.1), (1.0, 4.9), (2.0, 5.0), (3.0, 4.95), (4.0, 5.05)],
        'epsilon': 0.1,
        'expected_pieces': 1
    },
    {
        'pw_linear_fx': [
            (0.0, 0.0), (1.0, 1.0), (2.0, 2.0),
            (3.0, 5.0), (4.0, 8.0), (5.0, 11.0)
        ],
        'epsilon': 0.0,
        'expected_pieces': 2
    },
    {
        'pw_linear_fx': [
            (0.0, 0.0), (1.0, 1.0), (2.0, 2.0),
            (3.0, 5.0), (4.0, 8.0), (5.0, 11.0)
        ],
        'epsilon': 3.0,
        'expected_pieces': 1
    },
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 10.0)],
        'epsilon': 0.0,
        'expected_pieces': 2
    },
    {
        'pw_linear_fx': [
            (0.0, 0.0), (1.0, 10.0), (2.0, -10.0),
            (3.0, 10.0), (4.0, -10.0), (5.0, 0.0)
        ],
        'epsilon': 3.0,
        'expected_pieces': 5
    },
    {
        'pw_linear_fx': [
            (0.0, 0.0), (1.0, 0.5), (2.0, 1.1),
            (3.0, 1.6), (4.0, 2.1)
        ],
        'epsilon': 0.05,
        'expected_pieces': 2
    },
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0), (4.0, 4.0)],
        'epsilon': 0.0,
        'expected_pieces': 3
    },
]
test_cases24 = [
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (2.0, 2.0), (4.0, 4.0), (6.0, 6.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.05), (2.0, 1.98), (3.0, 3.02), (4.0, 4.10)],
        "epsilon": 0.1,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)],
        "epsilon": 0.1,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 100.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1.0,
        "expected_segments": 4
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 5.0), (4.0, 5.0), (5.0, 5.0)],
        "epsilon": 0.1,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 10.0), (1.0, 5.0), (2.0, 0.0), (3.0, 5.0), (4.0, 10.0)],
        "epsilon": 1.0,
        "expected_segments": 2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.5), (2.5, 2.5), (10.0, 10.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.2), (3.0, 3.0)],
        "epsilon": 0.2,
        "expected_segments": 1
    },
    {
        "pw_linear_fx": [
            (0.0,    0.0),
            (1.5708, 1.0),
            (3.1416, 0.0),
            (4.7124,-1.0),
            (6.2832, 0.0)
        ],
        "epsilon": 0.1,
        "expected_segments": 4
    }
]
test_cases25 = [
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 1.0), (2.0, 3.0), (5.0, 8.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.05), (3.0, 2.9)],
        "epsilon": 0.2
    },
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 0.0), (2.0, 10.0),
            (3.0, 10.0), (4.0, 0.0), (5.0, 0.0)
        ],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.57, 1.0), (3.14, 0.0),
            (4.71, -1.0), (6.28, 0.0)
        ],
        "epsilon": 0.2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 100.0), (2.0, 200.0), (3.0, 300.0)],
        "epsilon": 1000.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [
            (0.0, 0.0), (1.0, 1.0), (4.0, 2.0),
            (9.0, 3.0), (16.0, 4.0)
        ],
        "epsilon": 0.1
    }
]
test_cases26 = [
    # 1. Trivial two points — always one segment
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0)],
        'epsilon': 0.0,
        'expected_segments': 1
    },
    # 2. Perfectly linear (y = 2x + 1), zero tolerance — one segment
    {
        'pw_linear_fx': [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0), (3.0, 7.0)],
        'epsilon': 0.0,
        'expected_segments': 1
    },
    # 3. Constant function, zero tolerance — one segment
    {
        'pw_linear_fx': [(0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0)],
        'epsilon': 0.0,
        'expected_segments': 1
    },
    # 4. Zig‐zag within tolerance — should collapse to one segment
    {
        'pw_linear_fx': [
            (0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)
        ],
        'epsilon': 1.0,
        'expected_segments': 1
    },
    # 5. Single outlier forcing breaks at each neighborhood
    {
        'pw_linear_fx': [
            (0.0, 0.0), (1.0, 1.0), (2.0, 5.0), (3.0, 3.0), (4.0, 4.0)
        ],
        'epsilon': 0.5,
        'expected_segments': 4
    },
    # 6. Small random noise around line y = x, within epsilon — one segment
    {
        'pw_linear_fx': [
            (i, i + delta)
            for i, delta in zip(
                range(11),
                [0.03, -0.05, 0.02, -0.04, 0.01, -0.02, 0.04, -0.03, 0.05, -0.01, 0.00]
            )
        ],
        'epsilon': 0.1,
        'expected_segments': 1
    },
    # 7. Same noisy line with zero tolerance — must break between every pair
    {
        'pw_linear_fx': [
            (i, i + delta)
            for i, delta in zip(
                range(11),
                [0.03, -0.05, 0.02, -0.04, 0.01, -0.02, 0.04, -0.03, 0.05, -0.01, 0.00]
            )
        ],
        'epsilon': 0.0,
        'expected_segments': 10
    },
    # 8. Two‐phase slope: slope=1 then slope=2, zero tolerance — two segments
    {
        'pw_linear_fx': [
            (0.0, 0.0), (1.0, 1.0), (2.0, 2.0),
            (3.0, 5.0), (4.0, 8.0), (5.0, 11.0)
        ],
        'epsilon': 0.0,
        'expected_segments': 2
    },
    # 9. V‐shape (triangle) with just enough tolerance to fail single‐segment
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        'epsilon': 1.0,
        'expected_segments': 2
    },
    # 10. Same V‐shape but epsilon exactly equals max deviation — one segment
    {
        'pw_linear_fx': [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        'epsilon': 2.0,
        'expected_segments': 1
    }
]
test_cases27 = [
    # 1. Minimal two‐point case → always 1 segment
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0)],
        "epsilon": 0.1,
        "expected_segments": 1
    },
    # 2. Single‐point boundary → no segments can be formed
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.5,
        "expected_segments": 0
    },
    # 3. Perfectly constant y → one flat segment even with zero tolerance
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    # 4. Exactly linear growth → one segment at zero tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (4.0, 8.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },
    # 5. Small random noise all within ε → still one segment
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 2.05),
            (2.0, 4.02),
            (3.0, 5.98),
            (4.0, 8.03)
        ],
        "epsilon": 0.05,
        "expected_segments": 1
    },
    # 6. Noise at exactly the ε boundary → should still merge into one
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 2.025),
            (2.0, 4.05),
            (3.0, 6.075),
            (4.0, 8.1)
        ],
        "epsilon": 0.05,
        "expected_segments": 1
    },
    # 7. One point deviates beyond ε → must split into two pieces
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 2.0),
            (2.0, 5.0),   # jumps too far from y=4.0
            (3.0, 6.0),
            (4.0, 8.0)
        ],
        "epsilon": 0.5,
        "expected_segments": 2
    },
    # 8. Zig-zag pattern → each interval must be its own piece
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 0.0),
            (3.0, 1.0),
            (4.0, 0.0)
        ],
        "epsilon": 0.1,
        "expected_segments": 4
    },
    # 9. True piecewise ground-truth: flat → slope → flat
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 0.0),
            (2.0, 2.0),
            (3.0, 4.0),
            (4.0, 4.0),
            (5.0, 4.0)
        ],
        "epsilon": 0.01,
        "expected_segments": 3
    },
    # 10. Unsorted x-values input → algorithm should handle or sort internally
    {
        "pw_linear_fx": [
            (1.0, 2.0),
            (0.0, 0.0),
            (2.0, 4.0),
            (3.0, 6.0)
        ],
        "epsilon": 0.0,
        "expected_segments": 1
    }
]
test_cases28 = [
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.1), (2.0, 2.2), (3.0, 3.3)],
        "epsilon": 0.3
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.1), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.2
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 10.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 1.0
    },
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 3.0), (2.0, 1.0), (3.0, 2.0), (4.0, 4.0)],
        "epsilon": 0.5
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (4.0, 8.0)],
        "epsilon": 0.1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 1.0), (11.0, 2.0), (20.0, 3.0)],
        "epsilon": 0.5
    }
]
# Ten edge‐case inputs for L∞ piecewise linear approximation
test_cases29 = [
    # 1. Minimal data: only two points (always optimal as one segment)
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 10.0)],
        "epsilon": 5.0
    },

    # 2. Exact colinear with intermediate points, zero tolerance:
    # should collapse to one segment only if epsilon>0; here epsilon=0 so must keep breakpoints
    {
        "pw_linear_fx": [(0.0, 0.0), (5.0, 5.0), (10.0, 10.0)],
        "epsilon": 0.0
    },

    # 3. Noisy nearly‐linear data: small vertical deviations
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 1.1),
            (2.0, 2.05),
            (3.0, 2.95),
            (4.0, 4.2)
        ],
        "epsilon": 0.2
    },

    # 4. Step‐function shape: two plateaus separated by spike
    {
        "pw_linear_fx": [
            (0.0, 1.0),
            (1.0, 1.0),
            (2.0, 3.0),
            (3.0, 3.0),
            (4.0, 1.0),
            (5.0, 1.0)
        ],
        "epsilon": 0.5
    },

    # 5. Zigzag oscillation: high‐frequency changes
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 2.0),
            (2.0, 0.0),
            (3.0, 2.0),
            (4.0, 0.0)
        ],
        "epsilon": 1.0
    },

    # 6. Perfectly constant line: zero tolerance should still merge to one piece
    {
        "pw_linear_fx": [
            (0.0, 5.0),
            (1.0, 5.0),
            (2.0, 5.0),
            (3.0, 5.0),
            (4.0, 5.0)
        ],
        "epsilon": 0.0
    },

    # 7. Duplicate consecutive points (zero x‐span)
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 2.0)
        ],
        "epsilon": 0.1
    },

    # 8. U‐shaped convex curve: should test interior point removal
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.0, 2.0),
            (2.0, 4.0),
            (3.0, 2.0),
            (4.0, 0.0)
        ],
        "epsilon": 1.0
    },

    # 9. Non‐uniform x‐spacing on a straight‐line trend
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (0.1, 0.1),
            (5.0, 5.0),
            (9.9, 9.9),
            (10.0, 10.0)
        ],
        "epsilon": 0.05
    },

    # 10. Coarse sampling of a sine wave (challenging for L∞)
    {
        "pw_linear_fx": [
            (0.0, 0.0),
            (1.5708, 1.0),
            (3.1416, 0.0),
            (4.7124, -1.0),
            (6.2832, 0.0)
        ],
        "epsilon": 0.2
    }
]
test_cases30 = [
    # 1. Single point → no segments at all
    {
        "pw_linear_fx": [(0.0, 0.0)],
        "epsilon": 0.0,
        "expected_segments": 0
    },

    # 2. Exactly two points → always 1 segment, even if epsilon=0
    {
        "pw_linear_fx": [(0.0, 1.0), (1.0, 2.0)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 3. Constant function (many points, same y) → 1 segment suffices
    {
        "pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5)],
        "epsilon": 0.1,
        "expected_segments": 1
    },

    # 4. Perfectly collinear points → 1 segment regardless of epsilon=0
    {
        "pw_linear_fx": [(0, 0), (2, 4), (4, 8), (6, 12)],
        "epsilon": 0.0,
        "expected_segments": 1
    },

    # 5. One sharp “V” corner → needs 2 segments if ε < corner‐height/2
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0)],
        "epsilon": 0.1,
        "expected_segments": 2
    },

    # 6. Step–function with large jumps, small ε → no compression possible
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 10), (3, 10), (4, 0)],
        "epsilon": 1.0,
        "expected_segments": 4
    },

    # 7. Same step–function but ε large enough to bridge jump → 2 segments
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 10), (3, 10), (4, 0)],
        "epsilon": 5.0,
        "expected_segments": 2
    },

    # 8. Small random noise around zero, all within ε → 1 segment
    {
        "pw_linear_fx": [
            (0, 0.00),
            (1, 0.05),
            (2, 0.02),
            (3, 0.08),
            (4, -0.03),
            (5, 0.04)
        ],
        "epsilon": 0.10,
        "expected_segments": 1
    },

    # 9. Same noisy pattern but noise exceeds ε at a couple of points → 3 segments
    {
        "pw_linear_fx": [
            (0, 0.00),
            (1, 0.20),
            (2, 0.15),
            (3, 0.18),
            (4, 0.22),
            (5, 0.10)
        ],
        "epsilon": 0.10,
        "expected_segments": 3
    },

    # 10. Far apart x’s but flat y except one mid‐point bump → forces 2 segments
    {
        "pw_linear_fx": [(0, 0), (10, 0), (20, 5), (30, 0), (40, 0)],
        "epsilon": 2.0,
        "expected_segments": 2
    }
]
























