#7dec 12:38pm 50 testcases - performing it only once for the experiment
test_cases1 = [
    # 1-5: Boundary Conditions and Simple Cases
    # 1. Trivial: Only 2 points. Should always use 1 piece.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0)], "epsilon": 0.1, "expected_pieces": 1},
    # 2. Perfect Line: All points collinear. Should use 1 piece for any epsilon > 0.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], "epsilon": 0.01, "expected_pieces": 1},
    # 3. Maximum Tolerance: Epsilon is very large. Should use 1 piece.
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 5.0), (2.0, 0.0)], "epsilon": 10.0, "expected_pieces": 1},
    # 4. Zero Tolerance: Epsilon = 0. Should use n pieces (n+1 points).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.1)], "epsilon": 0.0, "expected_pieces": 2},
    # 5. Constant Function: Trivial approximation.
    {"pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)], "epsilon": 0.001, "expected_pieces": 1},

    # 6-15: Basic Parabola (to test curvature and mid-point error)
    # y = x^2, points (0,0), (1,1), (2,4), (3,9), (4,16)
    # 6. Epsilon forces 1 segment (large epsilon)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)], "epsilon": 3.0, "expected_pieces": 1},
    # 7. Epsilon forcing 2 segments (e.g., [0,2] then [2,4])
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)], "epsilon": 0.8, "expected_pieces": 2},
    # 8. Epsilon forcing 3 segments (more precise)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)], "epsilon": 0.2, "expected_pieces": 3},
    # 9. Small curvature (shallow parabola)
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.4), (3, 0.9), (4, 1.6)], "epsilon": 0.15, "expected_pieces": 1},
    # 10. Same parabola, tight tolerance (forces max pieces)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)], "epsilon": 0.01, "expected_pieces": 4},
    # 11. Concave down (negative curvature)
    {"pw_linear_fx": [(0, 0), (1, 2), (2, 3), (3, 2), (4, 0)], "epsilon": 0.5, "expected_pieces": 2},
    # 12. Non-symmetric shape
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 1.0), (3, 10.0)], "epsilon": 1.5, "expected_pieces": 2},
    # 13. Case where max error occurs near the start/end
    {"pw_linear_fx": [(0, 0), (0.1, 0.0), (1, 1.0), (2, 2.0)], "epsilon": 0.05, "expected_pieces": 2},
    # 14. Short segment followed by long curve
    {"pw_linear_fx": [(0, 0), (0.1, 0.0), (10, 5.0), (20, 10.0)], "epsilon": 0.1, "expected_pieces": 2},
    # 15. Long curve followed by short segment
    {"pw_linear_fx": [(0, 0), (10, 5.0), (10.1, 5.0), (20, 10.0)], "epsilon": 0.1, "expected_pieces": 2},

    # 16-25: Sharp Turns (Corner Cases)
    # 16. V-shape (Absolute value). Optimal pieces must end at the vertex.
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 1.0)], "epsilon": 0.1, "expected_pieces": 2},
    # 17. The V-shape where a single piece almost fits.
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 1.0)], "epsilon": 0.5, "expected_pieces": 1},
    # 18. Inverted V-shape (Roof).
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.1, "expected_pieces": 2},
    # 19. Extreme angle (almost vertical jump).
    {"pw_linear_fx": [(0.0, 0.0), (0.1, 10.0), (1.0, 10.0)], "epsilon": 0.05, "expected_pieces": 2},
    # 20. Step-like function (forces max pieces unless epsilon is large).
    {"pw_linear_fx": [(0, 0), (1, 0), (1.001, 5), (2, 5)], "epsilon": 0.01, "expected_pieces": 3},
    # 21. Sawtooth function (forces short pieces).
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.1, "expected_pieces": 4},
    # 22. Sawtooth with large epsilon (fits multiple peaks).
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 1.0, "expected_pieces": 1},
    # 23. A single point is an outlier, requiring a piece just for it.
    {"pw_linear_fx": [(0, 0), (1, 0), (1.5, 5), (2, 0), (3, 0)], "epsilon": 0.1, "expected_pieces": 3},
    # 24. A delayed V-shape, where the first piece is long.
    {"pw_linear_fx": [(0, 0), (5, 0), (6, 1), (7, 0)], "epsilon": 0.1, "expected_pieces": 2},
    # 25. Sharp change in slope that requires a new piece.
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 5), (3, 10)], "epsilon": 1.0, "expected_pieces": 2},

    # 26-35: Non-Uniform X-Spacing and Error Placement
    # 26. X-coordinates are powers of 2 (non-uniform).
    {"pw_linear_fx": [(1, 1), (2, 4), (4, 16), (8, 64)], "epsilon": 5.0, "expected_pieces": 2},
    # 27. Error exactly equal to epsilon (must still pass).
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.0)], "epsilon": 0.1, "expected_pieces": 1},
    # 28. Error slightly greater than epsilon (must fail and split).
    {"pw_linear_fx": [(0, 0), (1, 0.1001), (2, 0.0)], "epsilon": 0.1, "expected_pieces": 2},
    # 29. Logarithmic-like curve (decreasing slope).
    {"pw_linear_fx": [(1, 0), (2, 0.7), (4, 1.4), (8, 2.1)], "epsilon": 0.2, "expected_pieces": 2},
    # 30. Exponential-like curve (increasing slope).
    {"pw_linear_fx": [(0, 1), (1, 2), (2, 4), (3, 8)], "epsilon": 1.5, "expected_pieces": 2},
    # 31. Error occurring near the first segment point.
    {"pw_linear_fx": [(0, 0), (0.1, 0.5), (2, 0)], "epsilon": 0.4, "expected_pieces": 1},
    # 32. Error occurring near the last segment point.
    {"pw_linear_fx": [(0, 0), (1.9, 0.5), (2, 0.6)], "epsilon": 0.4, "expected_pieces": 2},
    # 33. All points nearly on a line, but one is a slight bump.
    {"pw_linear_fx": [(0, 0), (1, 1), (1.5, 1.2), (2, 2)], "epsilon": 0.1, "expected_pieces": 1},
    # 34. Points forcing a long segment at the start.
    {"pw_linear_fx": [(0, 0), (5, 0), (6, 5), (7, 0)], "epsilon": 1.0, "expected_pieces": 2},
    # 35. Points forcing a long segment at the end.
    {"pw_linear_fx": [(0, 0), (1, 5), (2, 0), (7, 0)], "epsilon": 1.0, "expected_pieces": 2},

    # 36-40: Oscillatory and Complex Shapes (Sinusoidal approximation)
    # 36. One period of a sine wave (0 to pi).
    {"pw_linear_fx": [(0, 0), (0.785, 0.707), (1.57, 1.0), (2.355, 0.707), (3.14, 0.0)], "epsilon": 0.2, "expected_pieces": 2},
    # 37. One period of a sine wave, tight tolerance (forces multiple pieces).
    {"pw_linear_fx": [(0, 0), (0.785, 0.707), (1.57, 1.0), (2.355, 0.707), (3.14, 0.0)], "epsilon": 0.05, "expected_pieces": 3},
    # 38. High frequency oscillation (many small pieces required).
    {"pw_linear_fx": [(0, 0), (0.1, 0.5), (0.2, 0), (0.3, 0.5), (0.4, 0)], "epsilon": 0.1, "expected_pieces": 4},
    # 39. Damped oscillation (decreasing amplitude).
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0.5), (3, 0.25), (4, 0.1)], "epsilon": 0.1, "expected_pieces": 3},
    # 40. Function with a plateau.
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 1), (3, 1), (4, 0)], "epsilon": 0.1, "expected_pieces": 3},

    # 41-50: Stress and Combined Cases (Larger datasets)
    # 41. Long, simple linear trend.
    {"pw_linear_fx": [(i, i) for i in range(11)], "epsilon": 0.001, "expected_pieces": 1},
    # 42. Long, constant curve with one outlier.
    {"pw_linear_fx": [(i, 5.0) for i in range(11)] + [(5, 7.0)], "epsilon": 1.0, "expected_pieces": 2},
    # 43. A series of small steps (requires n/2 pieces).
    {"pw_linear_fx": [(i, i // 2) for i in range(11)], "epsilon": 0.1, "expected_pieces": 5},
    # 44. Slowly increasing curvature (like 0.1 * x^3).
    {"pw_linear_fx": [(i, 0.1 * i**3) for i in range(5)], "epsilon": 1.0, "expected_pieces": 2},
    # 45. Highly constrained, forcing maximum pieces.
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1), (6, 0)], "epsilon": 0.001, "expected_pieces": 6},
    # 46. Case where the first piece is long, the second is short.
    {"pw_linear_fx": [(0, 0), (10, 0), (11, 1), (12, 0)], "epsilon": 0.1, "expected_pieces": 2},
    # 47. Large x-range, small y-range.
    {"pw_linear_fx": [(i * 10, i * 0.1) for i in range(5)], "epsilon": 0.01, "expected_pieces": 1},
    # 48. Large y-range, small x-range.
    {"pw_linear_fx": [(i * 0.1, i * 10) for i in range(5)], "epsilon": 0.01, "expected_pieces": 1},
    # 49. A 'W' shape that requires 3 pieces.
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], "epsilon": 0.4, "expected_pieces": 3},
    # 50. Mixed shape: Linear start, parabolic middle, linear end.
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 1), (3, 4), (4, 5), (5, 6)], "epsilon": 0.8, "expected_pieces": 2},
]