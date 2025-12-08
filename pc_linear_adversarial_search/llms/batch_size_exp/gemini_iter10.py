#7dec 12:38pm 100 testcases - performing it only once for the experiment
test_cases1 = [
    # 1-10: Basic & Uniformly Spaced
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], "epsilon": 0.1}, # 1. Perfectly Linear (1 piece expected)
    {"pw_linear_fx": [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)], "epsilon": 0.001}, # 2. Perfectly Constant (1 piece expected)
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.4), (3, 0.9), (4, 1.6), (5, 2.5)], "epsilon": 0.05}, # 3. Parabola, tight epsilon (Multiple pieces)
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.4), (3, 0.9), (4, 1.6), (5, 2.5)], "epsilon": 0.5}, # 4. Parabola, loose epsilon (Few pieces)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1)], "epsilon": 0.01}, # 5. Sawtooth, tight (Many pieces)
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1)], "epsilon": 0.5}, # 6. Sawtooth, loose (Few pieces)
    {"pw_linear_fx": [(0, 1), (1, 1), (1.001, 5), (2, 5), (2.001, 1), (3, 1)], "epsilon": 0.1}, # 7. Step function (Tests vertical gaps)
    {"pw_linear_fx": [(0, 0), (1, 0.05), (2, 0), (3, -0.05), (4, 0)], "epsilon": 0.1}, # 8. Minor Deviation (1 piece expected)
    {"pw_linear_fx": [(0, 0), (1, 0.11), (2, 0)], "epsilon": 0.1}, # 9. Just Exceeds Epsilon (2 pieces required)
    {"pw_linear_fx": [(0, 1), (5, 10)], "epsilon": 0.001}, # 10. Minimal Points (2 points, 1 piece expected)

    # 11-20: Non-Uniform X Spacing
    {"pw_linear_fx": [(0, 0), (0.1, 0), (0.2, 0), (5, 5)], "epsilon": 0.01}, # 11. X-Clustered at start
    {"pw_linear_fx": [(0, 0), (4.8, 5), (4.9, 5), (5, 5)], "epsilon": 0.01}, # 12. X-Clustered at end
    {"pw_linear_fx": [(0, 0), (0.01, 0.01), (1, 1), (10, 10)], "epsilon": 0.01}, # 13. Highly non-uniform linear
    {"pw_linear_fx": [(0, 0), (0.01, 0.0001), (1, 1), (10, 100)], "epsilon": 0.5}, # 14. Highly non-uniform parabolic
    {"pw_linear_fx": [(0, 1), (1, 1), (100, 1)], "epsilon": 0.01}, # 15. Large X jump, constant Y
    {"pw_linear_fx": [(0, 0), (0.1, 1), (0.2, 0), (0.3, 1)], "epsilon": 0.1}, # 16. Small X-range, high Y-variance
    {"pw_linear_fx": [(0, 0), (0.001, 10), (1, 10), (1.001, 0)], "epsilon": 0.1}, # 17. Steep slope segments
    {"pw_linear_fx": [(0, 0), (1, 0.1), (1.5, 0.15), (2, 0)], "epsilon": 0.01}, # 18. Points close to the max error line
    {"pw_linear_fx": [(0, 0), (1, 1), (100, 100), (101, 101)], "epsilon": 0.1}, # 19. Linear with large central gap
    {"pw_linear_fx": [(-5, -5), (-1, -1), (0, 0), (1, 1), (5, 5)], "epsilon": 0.1}, # 20. Negative X and Y values

    # 21-30: Zero, Negative & Epsilon Boundaries
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1)], "epsilon": 0.0}, # 21. Zero Epsilon (N pieces expected)
    {"pw_linear_fx": [(0, 0), (1, 0.00001), (2, 0)], "epsilon": 0.000001}, # 22. Tiny Epsilon
    {"pw_linear_fx": [(0, 0), (1, 100), (2, 0)], "epsilon": 1000.0}, # 23. Extremely Large Epsilon (1 piece expected)
    {"pw_linear_fx": [(0, -1), (1, -2), (2, -1.5), (3, -3)], "epsilon": 0.1}, # 24. All Negative Y
    {"pw_linear_fx": [(0, -100), (1, -1), (2, -100)], "epsilon": 50.0}, # 25. Large Negative Y, loose epsilon
    {"pw_linear_fx": [(0, 5), (1, -5), (2, 5), (3, -5)], "epsilon": 1.0}, # 26. Y values straddling X-axis
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0)], "epsilon": 0.1}, # 27. Perfectly fits Epsilon (Max deviation = Epsilon)
    {"pw_linear_fx": [(0, 0.1), (1, 0), (2, 0)], "epsilon": 0.05}, # 28. First point is max error
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 0.1)], "epsilon": 0.05}, # 29. Last point is max error
    {"pw_linear_fx": [(0, 0), (1, 1)], "epsilon": 0.1}, # 30. Minimal valid input

    # 31-40: Oscillating Functions
    {"pw_linear_fx": [(x, 10 * (0.5 - 0.5 * (1 + 0.1 * x) * (1 - 0.1 * x))) for x in range(11)], "epsilon": 0.01}, # 31. Low-frequency sine-like, tight
    {"pw_linear_fx": [(x, 10 * (0.5 - 0.5 * (1 + 0.1 * x) * (1 - 0.1 * x))) for x in range(11)], "epsilon": 1.0}, # 32. Low-frequency sine-like, loose
    {"pw_linear_fx": [(x, (-1)**x * 0.5) for x in range(11)], "epsilon": 0.05}, # 33. High-frequency oscillation
    {"pw_linear_fx": [(x, (-1)**x * (x/10)) for x in range(11)], "epsilon": 0.05}, # 34. Non-uniform amplitude oscillation
    {"pw_linear_fx": [(0, 1), (1, 1), (1.01, -1), (2, -1), (2.01, 1), (3, 1)], "epsilon": 0.1}, # 35. Square Wave
    {"pw_linear_fx": [(0, 0), (1, 0.05), (2, 0), (3, -0.05), (4, 0), (5, 5)], "epsilon": 0.1}, # 36. Oscillation followed by a steep slope
    {"pw_linear_fx": [(x, x/10 + (-1)**x * 0.1) for x in range(11)], "epsilon": 0.05}, # 37. Oscillation with linear trend
    {"pw_linear_fx": [(x, x * 0.01 + (-1)**x * 0.001) for x in range(11)], "epsilon": 0.005}, # 38. Very small steps
    {"pw_linear_fx": [(x, (-1)**x * 10) for x in range(11)], "epsilon": 5.0}, # 39. Large Amplitude Oscillation, medium epsilon
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (5, 1)], "epsilon": 0.01}, # 40. Long zero segment followed by jump

    # 41-50: Convex/Concave Functions
    {"pw_linear_fx": [(x, x**2) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], "epsilon": 0.5}, # 41. Convex (Parabola)
    {"pw_linear_fx": [(x, -x**2) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], "epsilon": 0.5}, # 42. Concave (Inverted Parabola)
    {"pw_linear_fx": [(x, (x-5)**3 / 25) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], "epsilon": 0.1}, # 43. S-curve (Inflection point)
    {"pw_linear_fx": [(x, 5 * (x + 1)**0.5) for x in range(11)], "epsilon": 0.2}, # 44. Logarithmic curve
    {"pw_linear_fx": [(x, 0.1 * 2**x) for x in range(11)], "epsilon": 0.5}, # 45. Exponential curve
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.4), (3, 0.9)], "epsilon": 0.09}, # 46. Convex, tight fit (Max error forces break)
    {"pw_linear_fx": [(0, 0), (1, -0.1), (2, -0.4), (3, -0.9)], "epsilon": 0.09}, # 47. Concave, tight fit
    {"pw_linear_fx": [(0, 0), (1, 0.5), (2, 0.4), (3, 0.5), (4, 1)], "epsilon": 0.1}, # 48. Inflection point near start
    {"pw_linear_fx": [(0, 1), (1, 0.5), (2, 0.4), (3, 0.5), (4, 1)], "epsilon": 0.1}, # 49. Inflection point near middle
    {"pw_linear_fx": [(x, (x-5)**4 / 100) for x in range(11)], "epsilon": 0.1}, # 50. High-degree polynomial

    # 51-60: Critical Epsilon Boundary Cases
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0), (3, 0.1001), (4, 0)], "epsilon": 0.1}, # 51. Just OUT of tolerance
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0), (3, 0.0999), (4, 0)], "epsilon": 0.1}, # 52. Just IN tolerance
    {"pw_linear_fx": [(0, 0), (1, 0.1001), (2, 0), (3, 0)], "epsilon": 0.1}, # 53. Second point immediately fails
    {"pw_linear_fx": [(x, 0.1 * ((-1)**x)) for x in range(11)], "epsilon": 0.10001}, # 54. Many points, one piece (just above max error)
    {"pw_linear_fx": [(x, 0.1 * ((-1)**x)) for x in range(11)], "epsilon": 0.09999}, # 55. Many points, many pieces (just below max error)
    {"pw_linear_fx": [(0, 0), (100, 0.1)], "epsilon": 0.01}, # 56. Very shallow slope, far-apart points
    {"pw_linear_fx": [(0, 0), (1, 0.5), (2, 0.1), (3, 0.5), (4, 0)], "epsilon": 0.5}, # 57. The optimal path must skip an intermediate point
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 1), (4, 2)], "epsilon": 0.05}, # 58. Zero slope followed by steep slope
    {"pw_linear_fx": [(0, 0), (1, 0.01), (2, 0.005), (3, 0)], "epsilon": 0.009}, # 59. Tolerance close to minimum non-zero difference
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.05), (3, 0.0), (4, 0.05), (5, 0.1), (6, 0)], "epsilon": 0.1}, # 60. Non-monotonic deviation within a segment

    # 61-70: Multi-Segment Scenarios (Testing optimization)
    {"pw_linear_fx": [(0, 0), (1, 1), (1.1, 0), (2, 1)], "epsilon": 0.01}, # 61. Two distinct short linear segments
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.4), (3, 0.4), (4, 0.1), (5, 0)], "epsilon": 0.1}, # 62. Two parabolic segments
    {"pw_linear_fx": [(0, 0), (1, 1), (2, 1), (3, 0)], "epsilon": 0.1}, # 63. Mixed slopes (positive, zero, negative)
    {"pw_linear_fx": [(0, 0), (1, 0.5), (2, 0.1), (3, 0.5), (4, 0)], "epsilon": 0.5}, # 64. Data where optimal path skips intermediate points
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (5, 2)], "epsilon": 0.1}, # 65. Long stretch exactly on the line
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0), (3, 0), (4, 0)], "epsilon": 0.09}, # 66. Segment boundary MUST be the end point
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.1), (3, 0.1), (4, 0)], "epsilon": 0.1}, # 67. Optimal segment endpoint is the last possible point
    {"pw_linear_fx": [(x, x**2/10) for x in range(5)] + [(x, 2.5 + 0.1 * (x - 5)) for x in range(5, 10)], "epsilon": 0.1}, # 68. High curvature to low curvature
    {"pw_linear_fx": [(x, 0.1 * x) for x in range(5)] + [(x, 0.5 + (x - 5)**2/10) for x in range(5, 10)], "epsilon": 0.1}, # 69. Low curvature to high curvature
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.0), (3, 0.05), (4, 0.0), (5, 0.1), (6, 0)], "epsilon": 0.05}, # 70. Forces DP/optimal choice over simple greedy

    # 71-80: High-Density & Large Data Sets
    {"pw_linear_fx": [(x, x) for x in range(51)], "epsilon": 0.1}, # 71. N=50, perfectly linear
    {"pw_linear_fx": [(x, x**2/100) for x in range(51)], "epsilon": 0.1}, # 72. N=50, uniform parabola
    {"pw_linear_fx": [(x, (-1)**x * 0.1) for x in range(51)], "epsilon": 0.05}, # 73. N=50, high-frequency oscillation
    {"pw_linear_fx": [(x, x**2/100) for x in range(51)], "epsilon": 0.0001}, # 74. N=50, extremely tight epsilon (tests performance)
    {"pw_linear_fx": [(x, x**2/100) for x in range(51)], "epsilon": 10.0}, # 75. N=50, very loose epsilon (1 piece)
    {"pw_linear_fx": [(x, 0) for x in range(25)] + [(25, 0.11), (26, 0), (27, 0)], "epsilon": 0.1}, # 76. N=50, mix, fails early on one segment
    {"pw_linear_fx": [(x / 10, x / 10) for x in range(10)] + [(x, x) for x in range(11, 40)], "epsilon": 0.1}, # 77. N=50, X-clustered near start
    {"pw_linear_fx": [(x, x) for x in range(30)] + [(31, 30), (32, 30), (33, 30)], "epsilon": 0.1}, # 78. N=50, Y-clustered near end
    {"pw_linear_fx": [(x, x/10 + (x % 5) / 100) for x in range(51)], "epsilon": 0.05}, # 79. N=50, random noise around a line
    {"pw_linear_fx": [(x, 50 * ((-1)**x)) for x in range(51)], "epsilon": 20.0}, # 80. N=50, large amplitude oscillation, medium epsilon

    # 81-90: Advanced Edge Cases & Geometric Traps
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0001), (2.0, 0.0), (3.0, 0.0002)], "epsilon": 0.0001}, # 81. Precision 1: Exactly on boundary or slightly over
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0001), (2.0, 0.0), (3.0, 0.00019)], "epsilon": 0.0002}, # 82. Precision 2: Exactly on boundary or slightly under
    {"pw_linear_fx": [(0.0, 0.0), (0.001, 10.0), (0.002, 0.0)], "epsilon": 5.0}, # 83. Near-Vertical Line (Test slope stability)
    {"pw_linear_fx": [(0.0, 0.0), (1000.0, 0.1), (2000.0, 0.0)], "epsilon": 0.05}, # 84. Near-Horizontal Line (Test error sensitivity to X-range)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.49}, # 85. Sharp Peak Mid-Segment (Just fails 1 piece)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)], "epsilon": 0.5}, # 86. Sharp Peak Mid-Segment (Just passes 1 piece)
    {"pw_linear_fx": [(0.0, 0.0), (5.0, 5.0), (10.0, 0.0)], "epsilon": 1.0}, # 87. Perfect V-shape, tests 2 pieces vs 1
    {"pw_linear_fx": [(0.0, 1.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0), (4.0, 1.0)], "epsilon": 0.1}, # 88. 'W' shape (Two sharp concavities)
    {"pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.1), (4.0, 0.0), (5.0, 0.1)], "epsilon": 0.05}, # 89. Tangent start, then fails
    {"pw_linear_fx": [(0.0, 0.1), (1.0, 0.0), (2.0, 0.1), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0)], "epsilon": 0.05}, # 90. Tangent end, then fails

    # 91-100: Greedy Traps & Specific Optimality Checks
    {"pw_linear_fx": [(0, 0), (1, 0.01), (2, 0.0), (3, 0.1), (4, 0.05)], "epsilon": 0.05}, # 91. A longer (optimal) segment exists, but a shorter, less greedy one is also valid.
    {"pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.11), (3, 0.0), (4, 0.0)], "epsilon": 0.1}, # 92. Immediate failure forces break, must verify the next piece starts optimally.
    {"pw_linear_fx": [(0, 0), (1, 0.001), (2, 0.002), (3, 0.003), (4, 0.004), (5, 0.05)], "epsilon": 0.005}, # 93. Long, shallow slope, with final point failure
    {"pw_linear_fx": [(0, 0), (1, 10), (2, 0), (3, 10), (4, 0), (5, 10)], "epsilon": 1.0}, # 94. High variance, small epsilon, many pieces needed.
    {"pw_linear_fx": [(x, (x-5)**2) for x in range(11)], "epsilon": 0.1}, # 95. N=10, Parabola, very tight fit.
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 0.1), (3, 0), (4, -0.1), (5, 0)], "epsilon": 0.0999}, # 96. Zig-zag, just misses tolerance (many pieces)
    {"pw_linear_fx": [(0, 0), (1, 0), (2, 0.1), (3, 0), (4, -0.1), (5, 0)], "epsilon": 0.1}, # 97. Zig-zag, just passes tolerance (fewer pieces)
    {"pw_linear_fx": [(x, 0) for x in range(10)] + [(11, 1), (12, 1)], "epsilon": 0.01}, # 98. Long flat segment followed by a large jump.
    {"pw_linear_fx": [(0, 0), (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.0)], "epsilon": 0.0}, # 99. Constant, zero epsilon (test zero division/N-1 pieces)
    {"pw_linear_fx": [(x, x + (-1)**x * 0.5) for x in range(11)], "epsilon": 0.25} # 100. Linear trend with high-frequency noise, medium epsilon
]