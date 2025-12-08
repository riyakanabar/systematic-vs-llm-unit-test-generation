#7dec 12:38pm 90 testcases - performing it only once for the experiment
import math
test_cases1 = [
    # ----------------------------------------------------------------------
    # 1. Basic Cases (Collinear, Steps, Simple Slopes) - (1-10)
    # ----------------------------------------------------------------------
    # 1. All points collinear, error 0, should be 1 piece for large epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 2. All points collinear, but a single point slightly off (0.1 error)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.1), (3.0, 3.0), (4.0, 4.0)],
        "epsilon": 0.05, # < 0.1, so two pieces needed: (0,0)-(1,1) and (2,2.1)-(4,4) or similar
        "expected_pieces": 2
    },
    # 3. Simple step function
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.001, 1.0), (2.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0)-(1,0) and (1.001,1.0)-(2,1.0)
    },
    # 4. Simple 'V' shape, peak is far, requires two pieces
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 2.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # The line (0,0)-(2,0) has error 2.0, so needs 2 pieces
    },
    # 5. Simple 'V' shape, peak is close, requires one piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)],
        "epsilon": 0.51,
        "expected_pieces": 1 # The line (0,0)-(2,0) has error 0.5. With 0.51 tolerance, 1 piece is enough
    },
    # 6. Flat line, small tolerance (testing floating point equality)
    {
        "pw_linear_fx": [(0.0, 5.0), (1.0, 5.0), (2.0, 5.0), (3.0, 5.0)],
        "epsilon": 0.0,
        "expected_pieces": 1 # Collinear, error is 0.0
    },
    # 7. Constant deviation: sine-like, 4 cycles
    {
        "pw_linear_fx": [(x, 0.5 * (-1)**x) for x in range(9)],
        "epsilon": 0.49,
        "expected_pieces": 8 # Every point is separated by 1.0 vert diff. Greedy ensures 1 piece per two points
    },
    # 8. Same as 7, but very large epsilon
    {
        "pw_linear_fx": [(x, 0.5 * (-1)**x) for x in range(9)],
        "epsilon": 100.0,
        "expected_pieces": 1 # All points within a segment error of 0.5
    },
    # 9. Simple parabola y=x^2 (0,0), (1,1), (2,4), (3,9). Line (0,0)-(3,9) error max at x=1.5 (approx 1.5)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # (0,0)-(2,4) has error 1.0 at x=1.0. (2,4)-(3,9) has max error < 1.0. Needs two.
    },
    # 10. Horizontal segment with one high point exactly at epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (1.5, 0.999)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },

    # ----------------------------------------------------------------------
    # 2. Boundary Cases (Points Exactly on the Epsilon Limit) - (11-20)
    # ----------------------------------------------------------------------
    # 11. Point exactly at epsilon, forcing the segment to end
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Line (0,0)-(3,0) max error is 1.0. Epsilon 0.5 will force 2 pieces.
    },
    # 12. Segment (0,0) to (4,0). Intermediate point (2, 1.0). Error is 1.0. Epsilon is 1.0.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    # 13. Same as 12, but epsilon is 1.0 - $10^{-9}$, should still be 1 piece (floating point check)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 0.5), (4.0, 0.0)],
        "epsilon": 0.999999999,
        "expected_pieces": 2
    },
    # 14. Collinear for the first half, second point exactly on boundary, forces 2 segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 2.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,0)-(3,2) has error 1.0 at x=2.0. Needs 2 segments.
    },
    # 15. Zig-zag pattern with points exactly $2\varepsilon$ apart vertically (alternating $\pm \varepsilon$ from a center line)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 4 # Segment (0,0)-(2,0) has error 1.0 > 0.5. Must break at every peak/trough.
    },
    # 16. Two segments, one short and one long. Testing decision point at the join
    {
        "pw_linear_fx": [(0.0, 0.0), (0.1, 0.0), (0.2, 0.1), (10.0, 0.0)],
        "epsilon": 0.05,
        "expected_pieces": 2 # Segment (0,0)-(10,0) has error 0.1. Needs 2 segments.
    },
    # 17. The intermediate point that causes the failure is not the next one
    # Segment (0,0)-(4,0). Intermediate points: (1, 0.1), (2, 0.5), (3, 0.1).
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.5), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.49,
        "expected_pieces": 2 # Error is 0.5 at x=2.0. Tolerance 0.49. Forces 2 segments.
    },
    # 18. Points below the line: Segment (0,0)-(2,2). Intermediate point (1, -1.0).
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, -1.0), (2.0, 2.0)],
        "epsilon": 1.0,
        "expected_pieces": 1 # Line y=x. Error at x=1 is |-1 - 1| = 2.0.
    },
    # 19. Points below the line: Corrected to force two segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, -1.0), (2.0, 2.0)],
        "epsilon": 1.99,
        "expected_pieces": 2
    },
    # 20. Exactly $\varepsilon$ away case, segment must end (classic optimality check)
    # (0,0)-(2,0) error 0.1 at (1, 0.1). Epsilon 0.1.
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Must end at (2,0). Next segment (2,0)-(3,1) error 0.
    },

    # ----------------------------------------------------------------------
    # 3. Floating Point Precision & Small/Zero Epsilon - (21-30)
    # ----------------------------------------------------------------------
    # 21. Zero tolerance on a non-linear set
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.001), (2.0, 0.0), (3.0, 0.0)],
        "epsilon": 0.0,
        "expected_pieces": 2 # Must break at (1.0, 0.001)
    },
    # 22. Zero tolerance on a collinear set
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    # 23. Extremely small but non-zero tolerance
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1e-8), (2.0, 0.0)],
        "epsilon": 1e-9,
        "expected_pieces": 2
    },
    # 24. Large number of collinear points, small perturbation near the end
    {
        "pw_linear_fx": [(i, i) for i in range(10)] + [(10.0, 10.001)],
        "epsilon": 0.0005,
        "expected_pieces": 2
    },
    # 25. Large number of points that should all fit in 1 segment
    {
        "pw_linear_fx": [(i, i + 0.01 * (i % 2)) for i in range(20)],
        "epsilon": 0.01,
        "expected_pieces": 1
    },
    # 26. Large number of points that force many tiny segments
    {
        "pw_linear_fx": [(i, 0.1 * (-1)**i) for i in range(20)],
        "epsilon": 0.05,
        "expected_pieces": 19 # Max error is 0.1. 0.05 < 0.1. Must break at every point.
    },
    # 27. Same as 26, but just over epsilon to force 1 piece
    {
        "pw_linear_fx": [(i, 0.1 * (-1)**i) for i in range(20)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 28. Tiny X-intervals, large Y-difference (testing vertical lines)
    {
        "pw_linear_fx": [(1.0, 0.0), (1.0001, 1.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # The points are too steep, line (1,0)-(2,0) misses (1.0001, 1.0) by almost 1.0
    },
    # 29. Very sparse points (long segments)
    {
        "pw_linear_fx": [(0.0, 0.0), (100.0, 1.0), (200.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    # 30. Sparse points, one intermediate point far away
    {
        "pw_linear_fx": [(0.0, 0.0), (100.0, 50.0), (200.0, 0.0)],
        "epsilon": 10.0,
        "expected_pieces": 2 # Line (0,0)-(200,0) error is 50.0. Needs 2 segments.
    },

    # ----------------------------------------------------------------------
    # 4. Alternating Errors (Above and Below the Segment) - (31-40)
    # ----------------------------------------------------------------------
    # 31. Alternating positive/negative errors within epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1 # The line (0,0)-(3,0) contains all points exactly.
    },
    # 32. Alternating positive/negative errors exceeding epsilon
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.2), (2.0, -0.2), (3.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Must break at (2, -0.2). Error is 0.2 > 0.1.
    },
    # 33. Points forming an 'S' curve, which is hard to approximate
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.4,
        "expected_pieces": 3 # (0,0)-(1,1), (1,1)-(2,0), (2,0)-(3,1) - each segment has max error 0.5 with center line.
    },
    # 34. S-curve that fits perfectly with 2 segments
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Segment (0,0)-(2,0) has error 1.0. Segment (0,0)-(3,1) has error 1.0. Needs 2 pieces (e.g., (0,0)-(1,1) and (1,1)-(3,1) (error 0.5 at x=2)).
    },
    # 35. Increasing density of points
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (1.5, 0.0), (1.75, 0.0), (2.0, 1.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,0)-(2,1) has error 0.5 at x=1.5 and x=1.75. If error <= 0.5, it's 1 piece.
    },
    # 36. Decreasing density of points
    {
        "pw_linear_fx": [(0.0, 1.0), (0.25, 0.0), (0.5, 0.0), (1.0, 0.0), (2.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 1 # All points within the range
    },
    # 37. Points forming a 'Z' shape
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 2.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0)-(1,1) and (1,1)-(3,2). Max error is 0.5 at x=2.0. Needs 2 segments.
    },
    # 38. Sine wave approximation (testing continuous curvature)
    {
        "pw_linear_fx": [(i * 0.1, 0.5 * math.sin(i * 0.1)) for i in range(30)],
        "epsilon": 0.01,
        "expected_pieces": "High Number (Approx 7-10)" # Depends on $\sin(x)$ curvature, should be many
    },
    # 39. Concave down (e.g., negative parabola)
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 1.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Line (0,0)-(3,0) has max error 1.0 at x=1,2.
    },
    # 40. Concave up
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, -1.0), (2.0, -1.0), (3.0, 0.0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Line (0,0)-(3,0) has max error 1.0 at x=1,2.
    },

    # ----------------------------------------------------------------------
    # 5. Greedy Trap Scenarios (Shouldn't happen with L-inf but good check) - (41-50)
    # ----------------------------------------------------------------------
    # Note: The greedy strategy is *proven* optimal for $L_{\infty}$ with increasing $x$.
    # These tests ensure the *geometric* core logic is robust.
    # 41. Long flat line with a spike near the beginning
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.5), (2.0, 0.0)] + [(i, 0.0) for i in range(3, 10)],
        "epsilon": 0.1,
        "expected_pieces": 2 # Segment (0,0)-(2,0) fails. Must be (0,0)-(1, 0.5) (error 0.5) and (1, 0.5)-(10, 0.0) (error < 0.1)
    },
    # 42. Long flat line with a spike near the end
    {
        "pw_linear_fx": [(i, 0.0) for i in range(7)] + [(7.0, 0.5), (8.0, 0.0), (9.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0)-(6,0) and (6,0)-(9,0). Segment (0,0)-(8,0) fails.
    },
    # 43. Steep segment followed by a flat segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (2.0, 10.0), (3.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0)-(1,10) and (1,10)-(3,10)
    },
    # 44. Flat segment followed by a steep segment
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.0), (2.0, 10.0), (3.0, 11.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0)-(1,0) and (1,0)-(3,11)
    },
    # 45. Segment that barely fails, forcing a short piece
    # (0,0)-(4,0). Points (1, 0.1), (2, 0.1), (3, 0.1). Epsilon 0.1 - 1e-9
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.1), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.099999999,
        "expected_pieces": 4 # Must break at every point (1, 0.1), (2, 0.1), (3, 0.1)
    },
    # 46. Segment that barely passes, forcing one long piece
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, 0.1), (3.0, 0.1), (4.0, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 47. Sawtooth pattern (high number of segments)
    {
        "pw_linear_fx": [(i, i % 2) for i in range(10)],
        "epsilon": 0.49,
        "expected_pieces": 9
    },
    # 48. Sawtooth pattern with large x-spacing
    {
        "pw_linear_fx": [(i * 10.0, i % 2) for i in range(10)],
        "epsilon": 0.49,
        "expected_pieces": 9
    },
    # 49. Segment where the error is maximal at an x-coordinate *between* data points
    # y = x^2, (0,0), (1,1), (2,4). Line (0,0)-(2,4) is y=2x. Error at x=1 is 1. Epsilon 1.
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0)],
        "epsilon": 1.0,
        "expected_pieces": 1 # Max error for (0,0)-(2,4) is 1.0 at x=1.0. Fits with 1 segment.
    },
    # 50. Same as 49, but epsilon slightly lower
    {
        "pw_linear_fx": [(0.0, 0.0), (0.5, 0.25), (1.0, 1.0), (1.5, 2.25), (2.0, 4.0)],
        "epsilon": 0.99,
        "expected_pieces": 2
    },

    # ----------------------------------------------------------------------
    # 6. Random/Mixed Data (A total of 40 more cases, filling out the 90) - (51-90)
    # ----------------------------------------------------------------------

    # 51-55: Medium size data set with varying epsilons
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.2), (4.0, 0.0), (5.0, 0.1)],
        "epsilon": 0.05,
        "expected_pieces": 4 # Forces many breaks
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.2), (4.0, 0.0), (5.0, 0.1)],
        "epsilon": 0.11,
        "expected_pieces": 2 # (0,0)-(4,0) error 0.2. (0,0)-(3,0.2) error 0.2. (0,0)-(5,0.1) max error 0.2 at x=3.0. Two pieces: (0,0)-(3,0.2) and (3,0.2)-(5,0.1)
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 0.1), (2.0, -0.1), (3.0, 0.2), (4.0, 0.0), (5.0, 0.1)],
        "epsilon": 0.2,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 3.0), (4.0, 0.0)],
        "epsilon": 1.0,
        "expected_pieces": 2 # (0,0)-(2,0) error 1.0. (2,0)-(4,0) error 3.0. Needs (2,0)-(3,3) and (3,3)-(4,0). Total 3 pieces.
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 3.0), (4.0, 0.0)],
        "epsilon": 1.5,
        "expected_pieces": 2 # (0,0)-(4,0) error 3.0. (0,0)-(2,0) error 1.0. (2,0)-(4,0) error 3.0. Needs 2 pieces (e.g., (0,0)-(2,0) and (2,0)-(4,0)).
    },
    # 56-60: Large, random-like data set
    {
        "pw_linear_fx": [(i, 0.25 * ((i % 4) - 2) + 0.01 * i) for i in range(20)],
        "epsilon": 0.2,
        "expected_pieces": "Medium Number (approx 5-10)"
    },
    {
        "pw_linear_fx": [(i, 0.25 * ((i % 4) - 2) + 0.01 * i) for i in range(20)],
        "epsilon": 0.51,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(i, 0.25 * ((i % 4) - 2) + 0.01 * i) for i in range(20)],
        "epsilon": 0.001,
        "expected_pieces": "Many (approx 19)"
    },
    {
        "pw_linear_fx": [(i, 0.01 * i * i) for i in range(10)], # Slow curve
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "pw_linear_fx": [(i, 0.01 * i * i) for i in range(10)],
        "epsilon": 0.001,
        "expected_pieces": 4
    },
    # 61-70: Sequences with large slopes and small errors
    {
        "pw_linear_fx": [(0, 0), (1, 10), (2, 20), (3, 30), (4, 40.1)],
        "epsilon": 0.05,
        "expected_pieces": 2 # (0,0)-(4,40.1) has error 0.1. Needs two: (0,0)-(3,30) and (3,30)-(4,40.1).
    },
    {
        "pw_linear_fx": [(0, 0), (1, 10), (2, 19.9), (3, 30)],
        "epsilon": 0.09,
        "expected_pieces": 2 # (0,0)-(3,30) has error 0.1 at x=2. Needs 2 segments.
    },
    {
        "pw_linear_fx": [(0, 0), (1, 10), (2, 19.9), (3, 30)],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(0, 0), (1, 10), (1.1, 10), (2, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # Steep ascent, small flat, steep descent
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (1.0, 10.0), (1.0001, 0.0), (2.0, 10.0)],
        "epsilon": 1.0,
        "expected_pieces": 3 # Must break at the tiny x-gap
    },
    {
        "pw_linear_fx": [(0.0, 0.0), (10.0, 0.0), (10.001, 10.0), (20.0, 10.0)],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 1), (3, 0), (4, -1), (5, 0)],
        "epsilon": 0.4,
        "expected_pieces": 4
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 1), (3, 0), (4, -1), (5, 0)],
        "epsilon": 0.5,
        "expected_pieces": 3 # (0,0)-(2,1) error 0.5. (2,1)-(4,-1) error 1.0. (2,1)-(5,0) error 1.0. Needs 3: (0,0)-(2,1), (2,1)-(3,0), (3,0)-(5,0).
    },
    {
        "pw_linear_fx": [(i, 100.0) for i in range(10)],
        "epsilon": 10.0,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(i, 100.0) for i in range(10)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    # 71-80: Focusing on the optimal point selection after a break
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 0), (3, 1.1), (4, 0)],
        "epsilon": 0.5,
        "expected_pieces": 3 # (0,0)-(2,0) error 1.0. (0,0)-(1,1) (1 piece). Then (1,1)-(3,1.1) (error 0.5 at x=2). Then (3,1.1)-(4,0).
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 1), (3, 0), (4, 1)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,0)-(2,1) has error 0.5 at x=1. (2,1)-(4,1) has error 0.5 at x=3.
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0.1), (2, 0.2), (3, 0.0), (4, 0.0), (5, 0.0)],
        "epsilon": 0.1,
        "expected_pieces": 2 # (0,0)-(3,0) error 0.2 at x=2. (0,0)-(2,0.2) error 0.1. (2,0.2)-(5,0.0) error 0.13.
    },
    {
        "pw_linear_fx": [(i, 0.0) for i in range(10)] + [(10, 1.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1.0), (5, 0), (6, 0)],
        "epsilon": 0.5,
        "expected_pieces": 2 # (0,0)-(6,0) error 1.0. Break at (4, 1.0). Two pieces: (0,0)-(4,1) and (4,1)-(6,0)
    },
    {
        "pw_linear_fx": [(0, 0), (1, 1), (2, 2), (3, 2.001), (4, 4)],
        "epsilon": 0.00000001,
        "expected_pieces": 3
    },
    {
        "pw_linear_fx": [(i, 0.0) for i in range(5)],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(i, i) for i in range(5)] + [(5.0, 4.0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(i, i) for i in range(5)] + [(5.0, 4.0)],
        "epsilon": 0.01,
        "expected_pieces": 2
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 1.0)],
        "epsilon": 0.99999,
        "expected_pieces": 2
    },
    # 81-90: Complex, long-range dependencies
    {
        "pw_linear_fx": [(0, 0), (10, 0.9), (20, 0), (30, 0.9), (40, 0)],
        "epsilon": 0.5,
        "expected_pieces": 3 # (0,0)-(20,0) error 0.9. (0,0)-(10,0.9) (1 piece). (10,0.9)-(30,0.9) (error 0.9). Needs 3 segments.
    },
    {
        "pw_linear_fx": [(0, 0), (10, 0.9), (20, 0), (30, 0.9), (40, 0)],
        "epsilon": 0.9,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(i, 1.0 if i % 10 == 0 else 0.0) for i in range(50)],
        "epsilon": 0.1,
        "expected_pieces": 5 # Should break at 10, 20, 30, 40
    },
    {
        "pw_linear_fx": [(i, 1.0 if i % 10 == 0 else 0.0) for i in range(50)],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 1), (6, 0), (7, 0), (8, 0)],
        "epsilon": 0.49,
        "expected_pieces": 2 # Must break at (5,1)
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 1), (6, 0), (7, 0), (8, 0)],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (10, 1), (11, 0), (20, 1)],
        "epsilon": 0.5,
        "expected_pieces": 3 # (0,0)-(10,1) error 0.9 at x=1. Needs to be (0,0)-(1,0), (1,0)-(11,0), (11,0)-(20,1) -> 3 pieces.
    },
    {
        "pw_linear_fx": [(0, 0), (1, 0), (10, 1), (11, 0), (20, 1)],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "pw_linear_fx": [(i, i * 0.1) for i in range(10)], # Simple upward slope
        "epsilon": 0.0001,
        "expected_pieces": 1
    },
    {
        "pw_linear_fx": [(i, i * 0.1 + 0.01 * (-1)**i) for i in range(10)], # Slope with oscillation
        "epsilon": 0.005,
        "expected_pieces": 9 # Max error 0.01. Requires 9 segments.
    },
]