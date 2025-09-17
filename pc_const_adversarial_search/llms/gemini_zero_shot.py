
#15 Sept Gemini 2.5 flash 4.22pm
import math
#Iteration1
test_cases1 = [
    {
        "name": "Simple Constant Function",
        "pc_fx": [[-float('inf'), 5.0], [0.0, 5.0], [10.0, 5.0], [float('inf'), 5.0]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "name": "Simple Monotonic Increasing Function",
        "pc_fx": [[-float('inf'), 0.0], [0.0, 0.0], [1.0, 0.1], [2.0, 0.2], [3.0, 0.3], [float('inf'), 0.3]],
        "epsilon": 0.05,
        "expected_pieces": 3  # For example, [0,1), [1,2), [2,3)
    },
    {
        "name": "Simple Monotonic Decreasing Function",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [1.0, 0.9], [2.0, 0.8], [3.0, 0.7], [float('inf'), 0.7]],
        "epsilon": 0.05,
        "expected_pieces": 3  # For example, [0,1), [1,2), [2,3)
    },
    {
        "name": "Step Function with Large Jumps",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [1.0, 1.0], [1.0001, 10.0], [2.0, 10.0], [float('inf'), 10.0]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "name": "Oscillating Function within Tolerance",
        "pc_fx": [[-float('inf'), 0.0], [0.0, 0.0], [1.0, 0.5], [2.0, -0.5], [3.0, 0.5], [4.0, 0.0], [float('inf'), 0.0]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "Optimal Piece Value not at Endpoint",
        "pc_fx": [[-float('inf'), 0.0], [0.0, 0.0], [1.0, 0.1], [2.0, -0.1], [3.0, 0.0], [float('inf'), 0.0]],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "name": "Flat Function with a Single Outlier",
        "pc_fx": [[-float('inf'), 5.0], [0.0, 5.0], [1.0, 5.0], [2.0, 10.0], [3.0, 5.0], [4.0, 5.0], [float('inf'), 5.0]],
        "epsilon": 1.0,
        "expected_pieces": 3
    },
    {
        "name": "Large Epsilon for a Single Piece",
        "pc_fx": [[-float('inf'), 0.0], [0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [float('inf'), 3.0]],
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    {
        "name": "Zero Tolerance (epsilon=0.0)",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [1.0, 2.0], [2.0, 3.0], [3.0, 3.0], [float('inf'), 3.0]],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    {
        "name": "Staircase Function",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [1.0, 2.0], [2.0, 2.0], [3.0, 3.0], [4.0, 3.0], [5.0, 4.0], [float('inf'), 4.0]],
        "epsilon": 0.5,
        "expected_pieces": 3
    }
]
#Iteration2
test_cases2 = [
    # 1. Simple Step Function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 0], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 3,
        "description": "A basic step function with jumps larger than epsilon. Each jump requires a new piece."
    },

    # 2. Function with Jumps and Plateaus
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 1], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 3,
        "description": "A function with jumps and flat sections that can be merged. The jumps at x=2 and x=4 are large, requiring new pieces."
    },

    # 3. Tolerance Greater Than All Jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, 1.5], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "A function where the entire range of values is within 2*epsilon, allowing a single piece."
    },

    # 4. Tolerance Exactly Equal to Half the Range
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "A function whose total value range is exactly 2*epsilon. A single piece is optimal as the max error (half the range) is <= epsilon."
    },

    # 5. Tolerance Slightly Less Than Half the Range
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2.1], [2, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "description": "A function where the total value range is slightly greater than 2*epsilon. A new piece must be created because a single piece approximation fails."
    },

    # 6. Function with a Single Point Jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 3,
        "description": "A single interval of different value, requiring new pieces at both ends. Jumps at x=1 and x=2 are > epsilon, creating three pieces."
    },

    # 7. Negative Function Values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -0.5], [2, -2], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "description": "Testing handling of negative numbers. The range of values on [0,2) is within 2*epsilon, but the jump to the final segment is too large."
    },

    # 8. Constant Function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 1.0e-6,
        "expected_pieces": 1,
        "description": "A trivial case where the function is already constant. A single piece is always sufficient."
    },

    # 9. Fluctuating Function within Tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.2], [2, 0], [3, 0.2], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "description": "The function oscillates, but the total range of values is small, so the entire function can be approximated by a single piece."
    },

    # 10. Complex Merging Scenario
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 10.1], [3, 10.2], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "description": "A large jump followed by a series of small changes that can be merged. The first jump at x=1 requires a new piece, but the subsequent pieces can be merged into one."
    }
]
#Iteration3
test_cases3 = [
    {
        "description": "1. Constant Function. The algorithm should use only one piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 5.0], [10.0, float('inf')]],
        "epsilon": 1.0,
        "expected_output": 1,
    },
    {
        "description": "2. Step Function. This tests if the algorithm correctly identifies the need for two pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 1.0], [5.0, 6.0], [10.0, float('inf')]],
        "epsilon": 0.5,
        "expected_output": 2,
    },
    {
        "description": "3. Small Epsilon, Small Jumps. This tests the algorithm's ability to handle fine-grained approximations.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 1.0], [1.0, 1.1], [2.0, 1.0], [3.0, 1.1], [4.0, 1.0], [5.0, float('inf')]],
        "epsilon": 0.05,
        "expected_output": 4,
    },
    {
        "description": "4. Epsilon Equal to the Jump Size. The algorithm should be able to cover the entire function with a single piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [5.0, 10.0], [10.0, float('inf')]],
        "epsilon": 10.0,
        "expected_output": 1,
    },
    {
        "description": "5. Epsilon Slightly Less Than the Jump Size. The algorithm should correctly identify that two pieces are needed.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [5.0, 10.0], [10.0, float('inf')]],
        "epsilon": 9.999,
        "expected_output": 2,
    },
    {
        "description": "6. Long, Flat Segments with a Single Spike. The algorithm should approximate the constant parts with a few pieces and the spike with more.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [10.0, 0.0], [10.1, 10.0], [10.2, 0.0], [20.0, 0.0], [20.0, float('inf')]],
        "epsilon": 0.5,
        "expected_output": 3,
    },
    {
        "description": "7. Alternating, Large Jumps. This tests if the algorithm can efficiently handle a large number of necessary pieces without being greedy.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [1.0, 10.0], [2.0, 0.0], [3.0, 10.0], [4.0, 0.0], [5.0, float('inf')]],
        "epsilon": 1.0,
        "expected_output": 4,
    },
    {
        "description": "8. Function with Overlapping Intervals. This tests if the algorithm correctly merges adjacent intervals when possible.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [1.0, 1.0], [2.0, 0.0], [3.0, 1.0], [4.0, 0.0], [5.0, float('inf')]],
        "epsilon": 1.0,
        "expected_output": 2,
    },
    {
        "description": "9. Zero Epsilon. A strict tolerance that requires an exact match. The algorithm should return the number of pieces in the original function.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 1.0], [5.0, 2.0], [10.0, float('inf')]],
        "epsilon": 0.0,
        "expected_output": 2,
    },
    {
        "description": "10. Very Large Epsilon. The tolerance is so large that the entire function can be approximated by a single piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [1.0, 100.0], [2.0, 0.0], [3.0, 100.0], [4.0, 0.0], [5.0, float('inf')]],
        "epsilon": 1000.0,
        "expected_output": 1,
    },
]
#Iteration4
test_cases4 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [-5, 5], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Uniform function, expected 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-10, 1], [-5, 3], [0, 5], [5, 7], [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Step function with small epsilon, expected 4 pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-10, 1], [-5, 3], [0, 5], [5, 7], [10, float('inf')]],
        "epsilon": 2.0,
        "description": "Step function with large epsilon, expected 2 pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Monotonically increasing function, expected 2 pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4], [2, 3], [3, 2], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Monotonically decreasing function, expected 2 pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-10, 2], [0, 10], [1, 2], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Function with a single spike, expected 3 pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-4, 4], [-2, 2], [0, 0], [2, 2], [4, 4], [6, float('inf')]],
        "epsilon": 1.5,
        "description": "Symmetrical V-shaped function, expected 3 pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-10, 0], [10, 0], [20, 0], [30, 0], [40, float('inf')]],
        "epsilon": 0.1,
        "description": "Constant at zero, expected 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-10, 1], [-5, 2], [0, 3], [5, 4], [10, float('inf')]],
        "epsilon": 2.0,
        "description": "Tolerance exceeds max variation, expected 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, 1.4], [5, 1.5], [6, float('inf')]],
        "epsilon": 0.5,
        "description": "Dense pieces with single approximation, expected 1 piece."
    }
]
#Iteration5
test_cases5 = [
    # 1. Simple linear function with a small slope
    {
        "pc_fx": [[-float('inf'), 0], [0, 0], [1, 0.5], [2, 1], [3, 1.5], [4, 2], [float('inf'), 2]],
        "epsilon": 0.2,
        "expected_pieces": 2,  # Example: One piece [0, 2) and another [2, 4)
    },

    # 2. Function with a large jump, requiring a new piece
    {
        "pc_fx": [[-float('inf'), 0], [0, 0], [1, 10], [2, 10], [3, 0], [4, 0], [float('inf'), 0]],
        "epsilon": 1.0,
        "expected_pieces": 3,  # A piece for the first interval, a piece for the jump, and a piece for the last part.
    },

    # 3. A constant function: should be approximated by a single piece
    {
        "pc_fx": [[-float('inf'), 5], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [float('inf'), 5]],
        "epsilon": 0.1,
        "expected_pieces": 1,
    },

    # 4. Zero tolerance: should return the original number of pieces
    {
        "pc_fx": [[-float('inf'), 0], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [float('inf'), 5]],
        "epsilon": 0.0,
        "expected_pieces": 4,  # The number of actual pieces in the input
    },

    # 5. Tolerance larger than any jump: should be a single piece
    {
        "pc_fx": [[-float('inf'), 0], [0, 0], [1, 10], [2, 5], [3, 15], [4, 20], [float('inf'), 20]],
        "epsilon": 100.0,
        "expected_pieces": 1,
    },

    # 6. Step function where tolerance is exactly the size of the steps
    {
        "pc_fx": [[-float('inf'), 0], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [float('inf'), 5]],
        "epsilon": 1.0,
        "expected_pieces": 1,
    },

    # 7. Step function where tolerance is less than the steps
    {
        "pc_fx": [[-float('inf'), 0], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [float('inf'), 5]],
        "epsilon": 0.9,
        "expected_pieces": 4,
    },

    # 8. Oscillating function with small amplitude
    {
        "pc_fx": [[-float('inf'), 0], [0, 0], [1, 0.1], [2, 0], [3, 0.1], [4, 0], [float('inf'), 0]],
        "epsilon": 0.05,
        "expected_pieces": 3,
    },

    # 9. Function with large negative values
    {
        "pc_fx": [[-float('inf'), -10], [0, -10], [1, -12], [2, -8], [3, -9], [4, -11], [float('inf'), -11]],
        "epsilon": 1.5,
        "expected_pieces": 2,
    },

    # 10. A function with many tiny steps that can be merged
    {
        "pc_fx": [[-float('inf'), 0], [0, 0.1], [1, 0.2], [2, 0.3], [3, 0.4], [4, 0.5], [5, 0.6], [6, 0.7], [7, 0.8],
                  [8, 0.9], [9, 1.0], [10, 1.1], [float('inf'), 1.1]],
        "epsilon": 0.5,
        "expected_pieces": 2,  # The first 5 pieces can be approximated by one, and the next 5 by another.
    },
]
#Iteration6
test_cases6 = [
    {
        "description": "Constant function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [10, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    {
        "description": "Step function, large epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, float('inf')]],
        "epsilon": 1.5,
        "expected_pieces": 1
    },
    {
        "description": "Linear function, requires multiple pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, 0.2], [3, 0.3], [4, float('inf')]],
        "epsilon": 0.05,
        "expected_pieces": 3
    },
    {
        "description": "Two distinct steps, small epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Step function, epsilon equal to step range",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Piecewise function with multiple segments",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1.2], [3, 2], [4, 1.5], [5, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Sawtooth function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.4,
        "expected_pieces": 3
    },
    {
        "description": "Large number of points, small tolerance",
        "pc_fx": [[-float('inf'), float('inf')]] + [[i, i/100] for i in range(101)] + [[100, float('inf')]],
        "epsilon": 0.005,
        "expected_pieces": 100
    },
    {
        "description": "Monotonic increasing function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4], [5, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Randomly generated, small epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.5], [1, 0.1], [2, 0.8], [3, 0.2], [4, 0.9], [5, float('inf')]],
        "epsilon": 0.01,
        "expected_pieces": 4
    }
]
#Iteration7
test_cases7 = [
    {
        "description": "Simple Flat Function: A constant function should be approximated by a single piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, 5], [30, 5], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Step Function with Tolerance: A simple step function where epsilon is large enough to cover the jump, so one piece is optimal.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 5], [10, 1], [float('inf'), float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 1
    },
    {
        "description": "Step Function at Tolerance Boundary: The jump is exactly at epsilon, so the algorithm should correctly require two pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 3], [10, 1], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "description": "Multiple Steps Within Tolerance: Multiple small steps within the tolerance, one piece is optimal.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1.1], [10, 1.2], [15, 1.3], [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Alternating Steps: Alternating up/down steps, all within tolerance, one piece is optimal.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [5, 1.5], [10, 0.5], [15, 1.2], [float('inf'), float('inf')]],
        "epsilon": 0.6,
        "expected_pieces": 1
    },
    {
        "description": "Small Variations Requiring Multiple Pieces: The range of values is slightly greater than 2*epsilon, forcing two pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [5, 2.1], [10, 3.0], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "description": "Complex Function with Multiple Sub-ranges: A more complex function with multiple jumps, should require multiple pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [5, 12], [10, 10], [15, 20], [20, 22], [25, 20], [30, 5], [35, 7], [40, 5], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 3
    },
    {
        "description": "Function with Smallest Possible Change: A change of 2*epsilon + a small delta, forcing a new piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [10, 2.0001], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "description": "Very Steep 'Staircase' Function: A staircase function where each step requires a new piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 2], [20, 4], [30, 6], [40, 8], [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 4
    },
    {
        "description": "Large Number of Pieces, Low Tolerance: Many pieces, low tolerance, forces the algorithm to use many pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.2], [2, 0], [3, 0.2], [4, 0], [5, 0.2], [6, 0], [7, 0.2], [8, 0], [9, 0.2], [10, 0], [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 6
    }
]
#Iteration8
test_cases8 = [
    # 1. Simple Horizontal Line
    {'pc_fx': [['-inf', 'inf'], [0, 5], [10, 5], [20, 5]], 'epsilon': 1.0, 'expected_pieces': 1},
    # 2. Step Function (Perfect Fit)
    {'pc_fx': [['-inf', 'inf'], [0, 1], [1, 2], [2, 3], [3, 4]], 'epsilon': 0.0, 'expected_pieces': 3},
    # 3. Step Function (Single Piece Approximation)
    {'pc_fx': [['-inf', 'inf'], [0, 1], [1, 1.5], [2, 1], [3, 1.5]], 'epsilon': 0.5, 'expected_pieces': 1},
    # 4. Alternating Values (High Frequency)
    {'pc_fx': [['-inf', 'inf'], [0, 1], [1, 2], [2, 1], [3, 2], [4, 1], [5, 2]], 'epsilon': 0.4, 'expected_pieces': 5},
    # 5. Alternating Values (Low Frequency)
    {'pc_fx': [['-inf', 'inf'], [0, 1], [1, 2], [2, 1], [3, 2], [4, 1], [5, 2]], 'epsilon': 0.6, 'expected_pieces': 1},
    # 6. Zero Tolerance
    {'pc_fx': [['-inf', 'inf'], [0, 0], [1, 1], [2, 2], [3, 3]], 'epsilon': 0.0, 'expected_pieces': 3},
    # 7. Monotonically Increasing Function
    {'pc_fx': [['-inf', 'inf'], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]], 'epsilon': 1.0, 'expected_pieces': 3},
    # 8. Monotonically Decreasing Function
    {'pc_fx': [['-inf', 'inf'], [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0]], 'epsilon': 1.0, 'expected_pieces': 3},
    # 9. Sawtooth Wave
    {'pc_fx': [['-inf', 'inf'], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0]], 'epsilon': 0.8, 'expected_pieces': 2},
    # 10. Large Data Set with Variable Spacing
    {'pc_fx': [['-inf', 'inf'], [0, 10], [1, 12], [2.5, 11], [3, 10.5], [4.5, 13], [5, 14], [8, 12], [9, 11.5]], 'epsilon': 1.5, 'expected_pieces': 3}
]
#Iteration9
test_cases9 = [
    {
        "description": "Uniformly Increasing Data. An optimal algorithm should use a single piece if the tolerance is large enough.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1], [3, 1.5], [4, 2], [5, 2.5], [6, 3]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Step Function. Requires a new piece at each discontinuity, regardless of tolerance.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0]],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    {
        "description": "Perfectly Flat Data. The function is already constant and should only need one piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Narrow Peaks. Tests sensitivity to localized fluctuations that require new pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0.5, 1], [1, 0], [1.5, 1], [2, 0]],
        "epsilon": 0.1,
        "expected_pieces": 4
    },
    {
        "description": "Large Tolerance. A large tolerance allows a complex function to be approximated by a single piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, -2], [4, 0]],
        "epsilon": 2.0,
        "expected_pieces": 1
    },
    {
        "description": "Alternating Values. A classic test for greedy algorithms that might get stuck in local minima.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [6, 0]],
        "epsilon": 0.4,
        "expected_pieces": 6
    },
    {
        "description": "Data Outside Tolerance Range. Tests for the strictness of the L-infinity norm check.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2.01]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "description": "Varying Slopes. Requires finding optimal breakpoints for a function with varying linear slopes.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.2], [2, 1], [3, 1.2], [4, 1.4]],
        "epsilon": 0.3,
        "expected_pieces": 2
    },
    {
        "description": "No Solution. The first data point itself violates tolerance, an edge case.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "description": "Exponential Growth. The spacing of pieces should increase as the function's slope steepens.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 4], [3, 8], [4, 16], [5, 32]],
        "epsilon": 2.0,
        "expected_pieces": 3
    }
]
#Iteration10
test_cases10 = [
    {
        "test_name": "Identical adjacent pieces",
        "pc_fx": [[0.0, 1.0], [1.0, 1.0]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "test_name": "Two steps within tolerance",
        "pc_fx": [[0.0, 1.0], [1.0, 1.5]],
        "epsilon": 0.26,
        "expected_pieces": 1
    },
    {
        "test_name": "Two steps outside tolerance",
        "pc_fx": [[0.0, 1.0], [1.0, 1.5]],
        "epsilon": 0.24,
        "expected_pieces": 2
    },
    {
        "test_name": "Alternating values, mergeable",
        "pc_fx": [[0.0, 1.0], [1.0, 3.0], [2.0, 1.0], [3.0, 3.0]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "test_name": "Monotonically increasing steps",
        "pc_fx": [[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]],
        "epsilon": 0.25,
        "expected_pieces": 3
    },
    {
        "test_name": "Multiple merges and splits",
        "pc_fx": [[0.0, 1.0], [1.0, 1.2], [2.0, 2.0], [3.0, 2.2], [4.0, 2.1]],
        "epsilon": 0.15,
        "expected_pieces": 2
    },
    {
        "test_name": "Already a single piece",
        "pc_fx": [[0.0, 5.0]],
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    {
        "test_name": "Zero epsilon, exact match",
        "pc_fx": [[0.0, 1.0], [1.0, 1.0], [2.0, 2.0]],
        "epsilon": 0.0,
        "expected_pieces": 2
    },
    {
        "test_name": "Empty input",
        "pc_fx": [],
        "epsilon": 1.0,
        "expected_pieces": 0
    },
    {
        "test_name": "Large jump after small change",
        "pc_fx": [[0.0, 1.0], [1.0, 1.1], [2.0, 100.0]],
        "epsilon": 1.0,
        "expected_pieces": 2
    }
]
#Iteration11
test_cases11 = [
    # Test Case 1: Simple Constant Function (Baseline)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 0.5,
    },

    # Test Case 2: Step Function, High Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [5, 6], [10, float('inf')]],
        'epsilon': 2.5,
    },

    # Test Case 3: Multiple Pieces, High Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 5], [4, 1], [6, 5], [8, 1], [10, float('inf')]],
        'epsilon': 2.0,
    },

    # Test Case 4: Multiple Pieces, Low Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 5], [4, 1], [6, 5], [8, 1], [10, float('inf')]],
        'epsilon': 0.5,
    },

    # Test Case 5: Staircase Function
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 2], [4, 3], [6, 4], [8, 5], [10, float('inf')]],
        'epsilon': 0.5,
    },

    # Test Case 6: Narrow "Spike"
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [4.9, 10], [5.1, 0], [10, float('inf')]],
        'epsilon': 1.0,
    },

    # Test Case 7: Minimal Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 20], [2, 30], [3, float('inf')]],
        'epsilon': 1e-9,
    },

    # Test Case 8: Zero Epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 2], [4, 3], [6, float('inf')]],
        'epsilon': 0.0,
    },

    # Test Case 9: Single-Piece Function, Zero Epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 0.0,
    },

    # Test Case 10: Piecewise Function with No Merges Possible
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 3], [4, 5], [6, 7], [8, float('inf')]],
        'epsilon': 0.5,
    }
]
#Iteration12
test_cases12 = [
    # Test Case 1: Simple Constant Function
    {
        'description': 'A function that is already a single constant piece.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'expected_output': 1
    },
    # Test Case 2: Two Pieces with Merging
    {
        'description': 'Two adjacent pieces can be merged because the difference is within epsilon.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [5, 11], [10, float('inf')]],
        'epsilon': 1.5,
        'expected_output': 1
    },
    # Test Case 3: Two Pieces, No Merging
    {
        'description': 'Two adjacent pieces cannot be merged as the difference exceeds epsilon.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [5, 12], [10, float('inf')]],
        'epsilon': 1.5,
        'expected_output': 2
    },
    # Test Case 4: Step Function with Varying Jumps
    {
        'description': 'A function with multiple steps, some can be merged, others cannot.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 3], [4, 5], [6, 1], [8, float('inf')]],
        'epsilon': 2.0,
        'expected_output': 2
    },
    # Test Case 5: Single Piece Approximation
    {
        'description': 'Multiple pieces that can all be approximated by a single constant.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [5, 1.5], [10, 2], [15, float('inf')]],
        'epsilon': 1.0,
        'expected_output': 1
    },
    # Test Case 6: Zero Tolerance
    {
        'description': 'Epsilon of zero means no approximation is allowed.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [5, 20], [10, 30], [15, float('inf')]],
        'epsilon': 0.0,
        'expected_output': 3
    },
    # Test Case 7: Large Tolerance
    {
        'description': 'A very large epsilon should always result in a single piece approximation.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 100], [5, -100], [10, 50], [15, float('inf')]],
        'epsilon': 1000.0,
        'expected_output': 1
    },
    # Test Case 8: Negative Values
    {
        'description': 'The algorithm should handle negative values correctly.',
        'pc_fx': [[-float('inf'), float('inf')], [0, -5], [5, -7], [10, -1], [15, float('inf')]],
        'epsilon': 2.5,
        'expected_output': 2
    },
    # Test Case 9: Boundary Case - Exactly Equal to Epsilon
    {
        'description': 'The difference is exactly equal to epsilon. Merging should be allowed.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [5, 10], [10, float('inf')]],
        'epsilon': 5.0,
        'expected_output': 1
    },
    # Test Case 10: Zig-Zag Function
    {
        'description': 'A function that alternates between two values.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [2, 1], [4, 10], [6, 1], [8, 10], [10, float('inf')]],
        'epsilon': 5.0,
        'expected_output': 3
    }
]
#Iteration13
test_cases13 = [
    {
        'name': '1. Merging Identical Pieces',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 1.0], [3, float('inf')]],
        'epsilon': 0.5,
        'expected_num_pieces': 1,
        'description': 'A basic sanity check to ensure the algorithm merges pieces with identical values.'
    },
    {
        'name': '2. No Merges Possible',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 3.0], [3, float('inf')]],
        'epsilon': 0.4,
        'expected_num_pieces': 3,
        'description': 'Tests that the algorithm does not merge pieces when the value differences exceed the tolerance.'
    },
    {
        'name': '3. Multiple Disjoint Merges',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.1], [1, 1.2], [2, 2.3], [3, 2.4], [4, float('inf')]],
        'epsilon': 0.2,
        'expected_num_pieces': 2,
        'description': 'Verifies the ability to find and perform multiple, non-contiguous merges for an optimal solution.'
    },
    {
        'name': '4. Staircase Function',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 2.0], [3, 2.5], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_num_pieces': 2,
        'description': 'Checks if the algorithm can find the largest possible contiguous merge block in a staircase-like function.'
    },
    {
        'name': '5. Small Spike',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 5.0], [2, 1.0], [3, float('inf')]],
        'epsilon': 0.5,
        'expected_num_pieces': 3,
        'description': 'Ensures a significant, isolated spike is preserved when the tolerance is too small to smooth it out.'
    },
    {
        'name': '6. Large Spike',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 5.0], [2, 1.0], [3, float('inf')]],
        'epsilon': 2.5,
        'expected_num_pieces': 1,
        'description': 'Tests that a large enough tolerance correctly allows the entire function to be simplified to a single piece.'
    },
    {
        'name': '7. Alternating Values, No Merge',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, -1.0], [2, 1.0], [3, -1.0], [4, float('inf')]],
        'epsilon': 0.9,
        'expected_num_pieces': 4,
        'description': 'Validates that the algorithm handles oscillatory data correctly, preventing merges when the tolerance is insufficient.'
    },
    {
        'name': '8. Alternating Values, Full Merge',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, -1.0], [2, 1.0], [3, -1.0], [4, float('inf')]],
        'epsilon': 1.0,
        'expected_num_pieces': 1,
        'description': 'Confirms that the algorithm can optimally simplify an oscillatory function into a single piece when the tolerance is exactly sufficient.'
    },
    {
        'name': '9. Zero Tolerance',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.1], [1, 1.2], [2, 2.3], [3, float('inf')]],
        'epsilon': 0.0,
        'expected_num_pieces': 2,
        'description': 'A boundary case that ensures no merges occur unless the piece values are exactly identical.'
    },
    {
        'name': '10. Complex Multi-Stage Merge',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 2.1], [3, 2.2], [4, 2.3], [5, 5.0], [6, float('inf')]],
        'epsilon': 0.5,
        'expected_num_pieces': 3,
        'description': 'A comprehensive test requiring the algorithm to find multiple optimal sub-merges within a complex function.'
    }
]
#Iteration14
test_cases14 = [
    {
        'description': 'Test Case 1: Constant Function',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 5.0], [10.0, float('inf')]],
        'epsilon': 1.0,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 5.0], [10.0, float('inf')]]
    },
    {
        'description': 'Test Case 2: Simple Merge',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 10.0], [10.0, 20.0], [20.0, float('inf')]],
        'epsilon': 5.0,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 15.0], [20.0, float('inf')]]
    },
    {
        'description': 'Test Case 3: Simple No-Merge',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 10.0], [10.0, 20.0], [20.0, float('inf')]],
        'epsilon': 4.9,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 10.0], [10.0, 20.0], [20.0, float('inf')]]
    },
    {
        'description': 'Test Case 4: Greedy Algorithm Failure Case',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 10.0], [10.0, 1.0], [20.0, 10.0], [30.0, 1.0], [40.0, float('inf')]],
        'epsilon': 4.5,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 5.5], [40.0, float('inf')]]
    },
    {
        'description': 'Test Case 5: Zero Tolerance',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 10.0], [10.0, 20.0], [20.0, 20.0], [30.0, float('inf')]],
        'epsilon': 0.0,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 10.0], [10.0, 20.0], [30.0, float('inf')]]
    },
    {
        'description': 'Test Case 6: Large Number of Pieces',
        'pc_fx': [[-float('inf'), float('inf')]] + [[float(i), 10.0] for i in range(51)] + [[float(i+50), 20.0] for i in range(51, 101)] + [[100.0, float('inf')]],
        'epsilon': 4.9,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 10.0], [50.0, 20.0], [100.0, float('inf')]]
    },
    {
        'description': 'Test Case 7: Alternating Values (No Merge Possible)',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [10.0, 10.0], [20.0, 1.0], [30.0, 10.0], [40.0, float('inf')]],
        'epsilon': 1.0,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 1.0], [10.0, 10.0], [20.0, 1.0], [30.0, 10.0], [40.0, float('inf')]]
    },
    {
        'description': 'Test Case 8: Large Tolerance',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [10.0, 10.0], [20.0, 1.0], [30.0, 10.0], [40.0, float('inf')]],
        'epsilon': 5.0,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 5.5], [40.0, float('inf')]]
    },
    {
        'description': 'Test Case 9: Non-integer Values',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.1], [10.0, 1.2], [20.0, 1.3], [30.0, 1.4], [40.0, float('inf')]],
        'epsilon': 0.2,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, 1.3], [40.0, float('inf')]]
    },
    {
        'description': 'Test Case 10: Mixed Positive and Negative Values',
        'pc_fx': [[-float('inf'), float('inf')], [0.0, -10.0], [10.0, -5.0], [20.0, 5.0], [30.0, float('inf')]],
        'epsilon': 2.5,
        'pc_fx_expected': [[-float('inf'), float('inf')], [0.0, -7.5], [20.0, 5.0], [30.0, float('inf')]]
    }
]
#Iteration15
test_cases15 = [
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [10, 10], [20, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 1,
        'description': 'A simple linear function. Approximated by one piece with a large epsilon.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [5, 2], [10, 3], [15, float('inf')]],
        'epsilon': 0.1,
        'expected_pieces': 3,
        'description': 'An already piecewise constant function. Should return the original number of pieces.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [5, 100], [10, 0], [15, float('inf')]],
        'epsilon': 10.0,
        'expected_pieces': 3,
        'description': 'A large vertical jump. The algorithm must split the piece.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [5, 0.5], [10, 0], [15, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 1,
        'description': 'A small jump within tolerance. The algorithm should combine the pieces.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [10, 5], [20, 0], [30, float('inf')]],
        'epsilon': 10.0,
        'expected_pieces': 1,
        'description': 'A large tolerance allowing a single-piece approximation.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [5, 2], [10, 3], [15, float('inf')]],
        'epsilon': 0.0,
        'expected_pieces': 3,
        'description': 'Zero tolerance. Requires an exact approximation.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, -0.5], [3, 0.5], [4, -0.5], [5, float('inf')]],
        'epsilon': 0.75,
        'expected_pieces': 1,
        'description': 'A function with small variations. Should be grouped into a single piece.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 4,
        'description': 'A function with steps of size 1. An epsilon of 0.5 is too small to combine steps.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [5, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 1,
        'description': 'A single-piece function. Should simply return one piece.'
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 1], [3, 3], [4, 2], [5, 4], [6, 3], [7, 5], [8, 4], [9, float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 4,
        'description': 'A complex function with varying slopes. Should find the minimal number of pieces.'
    }
]
#Iteration16
test_cases16 = [
    {
        "name": "1. Simple Monotonic Function ↗️",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "expected_optimal_pc_fx": [[-float('inf'), float('inf')], [0, 0.5], [1, 1.5], [2, 2.5], [3, 3.5], [4, 4.5], [5, float('inf')]]
    },
    {
        "name": "2. Discontinuous Function ⚡️",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [1, 10], [2, 10], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_optimal_pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, float('inf')]]
    },
    {
        "name": "3. Flat Function ➖",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_optimal_pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [10, float('inf')]]
    },
    {
        "name": "4. Zero Tolerance (ε = 0) 🎯",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [float('inf'), float('inf')]],
        "epsilon": 0.0,
        "expected_optimal_pc_fx": None  # Expecting a failure or no-solution state
    },
    {
        "name": "5. Oscillating Function 🌊",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.5], [1, -0.5], [2, 0.5], [3, -0.5], [4, 0.5], [float('inf'), float('inf')]],
        "epsilon": 0.4,
        "expected_optimal_pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [float('inf'), float('inf')]]
    },
    {
        "name": "6. Function with Varying Slope 📉📈",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 1], [6, 2], [7, 4], [float('inf'), float('inf')]],
        "epsilon": 0.2,
        "expected_optimal_pc_fx": "dynamically determined, multiple pieces for steep sections"
    },
    {
        "name": "7. Large Tolerance (ε > max deviation) ⬆️",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_optimal_pc_fx": [[-float('inf'), float('inf')], [0, 0.5], [2, float('inf')]]
    },
    {
        "name": "8. Perfectly Approximable Function ✅",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [float('inf'), float('inf')]],
        "epsilon": 0.0,
        "expected_optimal_pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]]
    },
    {
        "name": "9. Step-and-Ramp Combination 🚶‍♂️",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 0], [6, 1], [float('inf'), float('inf')]],
        "epsilon": 0.2,
        "expected_optimal_pc_fx": "dynamically determined, one piece for flat, multiple for ramp"
    },
    {
        "name": "10. Large Number of Pieces and Varying Density 🧩",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [1.1, 0.1], [2, 0.2], [2.1, 0.2], [10, 0.3], [10.1, 0.3], [11, 0.4], [float('inf'), float('inf')]],
        "epsilon": 0.05,
        "expected_optimal_pc_fx": "dynamically determined, few pieces for flat, more for dense data"
    }
]
#Iteration17
test_cases17 = [
    {
        "description": "Simple linear function (10 pieces) with a tolerance requiring 5 pieces.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.5], [1, 1.5], [2, 2.5], [3, 3.5], [4, 4.5],
            [5, 5.5], [6, 6.5], [7, 7.5], [8, 8.5], [9, 9.5],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "expected_pieces": 5
    },
    {
        "description": "Already optimal approximation (2 pieces). Tolerance is too small to merge.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [5, 2.0], [10, float('inf')]
        ],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Constant function. Should always be 1 piece.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5.0], [10, float('inf')]
        ],
        "epsilon": 10.0,
        "expected_pieces": 1
    },
    {
        "description": "Zero tolerance. No approximation allowed; original pieces must be kept.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [5, 2.0], [10, float('inf')]
        ],
        "epsilon": 0.0,
        "expected_pieces": 2
    },
    {
        "description": "Very large tolerance. The entire function should be approximated by a single piece.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.5], [1, 1.5], [2, 2.5], [3, 3.5], [4, 4.5],
            [5, 5.5], [6, 6.5], [7, 7.5], [8, 8.5], [9, 9.5],
            [10, float('inf')]
        ],
        "epsilon": 5.0,
        "expected_pieces": 1
    },
    {
        "description": "Oscillating function. A small tolerance forces a large number of pieces.",
        "pc_fx": (lambda: [
            [-float('inf'), float('inf')]
        ] + [[i * 0.314159265, math.sin(i * 0.314159265 + 0.1570796325)] for i in range(20)] + [
            [2 * 3.14159265, float('inf')]
        ])(),
        "epsilon": 0.1,
        "expected_pieces": "large number (> 20)"
    },
    {
        "description": "Large discontinuity. A huge jump prevents merging even with high tolerance.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.0], [5, 100.0], [10, float('inf')]
        ],
        "epsilon": 10.0,
        "expected_pieces": 2
    },
    {
        "description": "Mixed monotonic segments. Checks that the algorithm respects multiple jumps.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 2.0], [3, 3.0], [6, 4.0], [10, float('inf')]
        ],
        "epsilon": 0.5,
        "expected_pieces": 4
    },
    {
        "description": "'V' shape function. Tests handling of sharp corners, requiring many pieces.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 4.5], [1, 3.5], [2, 2.5], [3, 1.5], [4, 0.5],
            [5, 0.5], [6, 1.5], [7, 2.5], [8, 3.5], [9, 4.5],
            [10, float('inf')]
        ],
        "epsilon": 0.2,
        "expected_pieces": "large number (> 10)"
    },
    {
        "description": "Combined behaviors. Constant, linear, and jump segments.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [3, 2.0], [6, 3.0], [10, 5.0], [12, float('inf')]
        ],
        "epsilon": 0.6,
        "expected_pieces": 4
    }
]
#Iteration18
test_cases18 = [
    # 1. Simple Horizontal Line
    {
        "pc_fx": [[0.0, 5.0], [1.0, 5.0], [2.0, 5.0], [3.0, 5.0]],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # 2. Simple Linear Function
    {
        "pc_fx": [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # 3. Step Function with Jumps Exceeding Epsilon
    {
        "pc_fx": [[0.0, 1.0], [1.0, 1.0], [1.0001, 3.0], [2.0, 3.0]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # 4. Step Function with Jumps within Epsilon
    {
        "pc_fx": [[0.0, 1.0], [1.0, 1.0], [1.0001, 1.4], [2.0, 1.4]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # 5. Oscillating Function
    {
        "pc_fx": [[0.0, 0.0], [0.5, 1.0], [1.0, 0.0], [1.5, 1.0], [2.0, 0.0]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # 6. Empty Input
    {
        "pc_fx": [],
        "epsilon": 0.1,
        "expected_pieces": 0
    },
    # 7. Single Point
    {
        "pc_fx": [[5.0, 10.0]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    # 8. Disconnected Point (Extreme Tolerance)
    {
        "pc_fx": [[0.0, 1.0], [1.0, 1.0], [2.0, 100.0], [3.0, 1.0]],
        "epsilon": 100.0,
        "expected_pieces": 1
    },
    # 9. Disconnected Point (Tight Tolerance)
    {
        "pc_fx": [[0.0, 1.0], [1.0, 1.0], [2.0, 100.0], [3.0, 1.0]],
        "epsilon": 1.0,
        "expected_pieces": 3
    },
    # 10. Function with Multiple Loci of Change
    {
        "pc_fx": [[0.0, 0.0], [1.0, 1.0], [2.0, 0.0], [3.0, -1.0], [4.0, 0.0]],
        "epsilon": 0.5,
        "expected_pieces": 3
    }
]
#Iteration19
test_cases19 = [
    {
        'pc_fx': [[-float('inf'), float('inf')], [1.0, 5.0], [10.0, 5.0], [20.0, float('inf')]],
        'epsilon': 1.0,
        'expected_output': 1
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 2.0], [5.0, 2.0], [10.0, float('inf')]],
        'epsilon': 0.001,
        'expected_output': 1
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [5.0, 3.0], [10.0, float('inf')]],
        'epsilon': 1.5,
        'expected_output': 1
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [5.0, 3.0], [10.0, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 2
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [5.0, 2.0], [10.0, 3.0], [15.0, float('inf')]],
        'epsilon': 0.001,
        'expected_output': 2
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [5.0, 2.0], [10.0, 3.0], [15.0, float('inf')]],
        'epsilon': 1.0,
        'expected_output': 1
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [2.0, 3.0], [5.0, -1.0], [8.0, 2.0], [10.0, float('inf')]],
        'epsilon': 1.5,
        'expected_output': 3
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [0.5, 10.0], [5.0, 1.0], [10.0, float('inf')]],
        'epsilon': 2.0,
        'expected_output': 3
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [5.0, 2.0], [5.0, 3.0], [10.0, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 2
    },
    {
        'pc_fx': [[-float('inf'), float('inf')], [0.0, 1.0], [1.0, 2.0], [2.0, 1.0], [3.0, 3.0], [4.0, 4.0], [5.0, 2.0], [6.0, 1.0], [7.0, 0.0], [8.0, 1.0], [9.0, 2.0], [10.0, 3.0], [11.0, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 6
    }
]
#Iteration20
test_cases20 = [
    {
        "description": "1. Simple, flat function: Should require only one piece as it is already constant.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 1.0], [10.0, 1.0], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },
    {
        "description": "2. Single step function: The jump exceeds the tolerance, so it should require two pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 1.0], [5.0, 2.0], [10.0, 1.0], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },
    {
        "description": "3. Linear function within tolerance: The total range of y-values is less than 2*epsilon, allowing a single piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [10.0, 0.4], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },
    {
        "description": "4. Linear function at tolerance boundary: The range of y-values is exactly 2*epsilon, which should still be covered by a single piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [10.0, 1.0], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },
    {
        "description": "5. Function with multiple directional changes: Should require multiple pieces to handle the 'sawtooth' pattern.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [1.0, 1.0], [2.0, 0.0], [3.0, 1.0], [4.0, 0.0], [float('inf'), float('inf')]],
        "epsilon": 0.2
    },
    {
        "description": "6. Function with a single spike: A sharp, brief deviation that forces an additional piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [5.0, 1.0], [5.1, 0.0], [10.0, 0.0], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },
    {
        "description": "7. Function with many small steps: The small, frequent oscillations might tempt a non-optimal algorithm to use many pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [1.0, 0.2], [2.0, 0.0], [3.0, 0.2], [4.0, 0.0], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },
    {
        "description": "8. Long flat section followed by a jump: Tests the algorithm's ability to transition from a long, simple piece to a more complex section.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [10.0, 0.0], [10.1, 1.0], [15.0, 1.0], [float('inf'), float('inf')]],
        "epsilon": 0.2
    },
    {
        "description": "9. Multiple jumps: Tests the algorithm's ability to find separate optimal pieces for widely separated discontinuities.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [2.0, 1.0], [4.0, 0.0], [6.0, 1.0], [8.0, 0.0], [float('inf'), float('inf')]],
        "epsilon": 0.2
    },
    {
        "description": "10. An extreme case where a single piece spans a wide range: The algorithm must find an optimal piece that covers a larger segment, not just the obvious ones.",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [1.0, 0.1], [2.0, 0.1], [3.0, 0.3], [4.0, 0.3], [float('inf'), float('inf')]],
        "epsilon": 0.1
    }
]
#Iteration21
test_cases21 = [
    {
        "name": "Uniformly Spaced Points",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]],
        "epsilon": 0.5,
        "expected_pieces": 5,
        "rationale": "A small tolerance should merge points that are close, but not all of them."
    },
    {
        "name": "Highly Oscillating Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, -1], [2, 1], [3, -1], [4, 1], [5, -1]],
        "epsilon": 0.1,
        "expected_pieces": 6,
        "rationale": "The function values oscillate by 2, so a small epsilon will force a new piece for almost every interval."
    },
    {
        "name": "Step Function with Large Jumps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 10], [3, 10], [4, 0], [5, 0]],
        "epsilon": 1.0,
        "expected_pieces": 3,
        "rationale": "The large jumps from 0 to 10 and back to 0 cannot be absorbed into a single piece with epsilon=1."
    },
    {
        "name": "All Points Within Tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3]],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "rationale": "All values (1, 1.1, 1.2, 1.3) fall within a range of 0.3, which is less than 2*epsilon=1.0."
    },
    {
        "name": "Large Tolerance (epsilon)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 100], [1, 200], [2, 300], [3, 400]],
        "epsilon": 1000,
        "expected_pieces": 1,
        "rationale": "Any function can be approximated by a single piece if the tolerance is large enough."
    },
    {
        "name": "Zero Tolerance (epsilon=0)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4]],
        "epsilon": 0.0,
        "expected_pieces": 4,
        "rationale": "With zero tolerance, the algorithm must return the original number of pieces since any change would introduce error."
    },
    {
        "name": "Constant Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5]],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "rationale": "The function is already constant, so the approximation should be a single piece regardless of a non-zero epsilon."
    },
    {
        "name": "Strictly Increasing Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4]],
        "epsilon": 0.5,
        "expected_pieces": 3,
        "rationale": "The algorithm should group points [0,1,2] and [2,3,4] (or similar groupings) as the values increase, but a small tolerance will still require multiple pieces. For example, a single piece covering [0,4] would have a range of 4, much larger than 2*epsilon=1.0."
    },
    {
        "name": "Strictly Decreasing Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [1, 3], [2, 2], [3, 1], [4, 0]],
        "epsilon": 0.5,
        "expected_pieces": 3,
        "rationale": "Similar to the increasing function, the algorithm should group points, but the negative slope requires new pieces for the approximation to remain within tolerance."
    },
    {
        "name": "Combination of Constant and Changing Segments",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 10], [4, 10], [5, 10]],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "rationale": "The first three points are constant and should be merged into one piece. The next three points are also constant but at a different value, which requires a new piece."
    }
]
#Iteration22
test_cases22 = [
    {
        "description": "Uniformly Rising Function: f(x) = x. Total variation requires multiple pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 10], [10, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 3,
        "notes": "Range of [0,10] is 10. Half-range (L-infinity error) is 5.0. Since 5.0 > epsilon (2.0), more than one piece is needed. Each piece can span a range of 2*epsilon=4. The function `f(x)=x` on [0,10] has a range of 10. Thus, at least ceil(10/4)=3 pieces are needed. For example, [0,4), [4,8), [8,10). The last piece has a range of 2 which is fine."
    },
    {
        "description": "Step Function: A large jump that forces a breakpoint.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 10], [10, 1], [10, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 2,
        "notes": "A single piece cannot span the discontinuity at x=5, as the range of the function is [1,10], so the error would be (10-1)/2 = 4.5, which exceeds epsilon. An optimal algorithm should place a breakpoint at x=5, resulting in two pieces."
    },
    {
        "description": "Flat Function: A single piece with zero error.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [10, float('inf')]],
        "epsilon": 0.001,
        "expected_pieces": 1,
        "notes": "The function is constant, so the range is 0. The error is 0, which is less than epsilon, so one piece is sufficient."
    },
    {
        "description": "Alternating Peaks and Valleys: Multiple extrema requiring multiple pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 10], [4, 0], [6, 10], [8, 0], [10, 10], [10, float('inf')]],
        "epsilon": 4.0,
        "expected_pieces": 3,
        "notes": "The function's range for any interval containing both a peak (10) and a valley (0) is 10. The L-infinity error is half the range, 5, which is greater than epsilon (4). The optimal solution will place breakpoints at local extrema to minimize the number of pieces. In this case, three pieces are needed to cover the range while respecting the error bound."
    },
    {
        "description": "High-Frequency Data: Small epsilon forces many small pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [10, 0], [10, float('inf')]],
        "epsilon": 0.2,
        "expected_pieces": 5,
        "notes": "The function value alternates between 0 and 1. The range is 1. The error for any single piece covering a jump is 0.5, which is greater than epsilon (0.2). A new piece must be created for each jump. The number of pieces will be the number of segments in the input `pc_fx` representation, which is 5."
    },
    {
        "description": "Single Local Extremum: V-shaped function requires a breakpoint at the vertex.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [5, 0], [10, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 3,
        "notes": "The function f(x)=|x-5| has a range of 5 over the interval [0,10]. Half of this is 2.5, which exceeds epsilon. To be within the error bound, the range of each piece must be at most 2*epsilon=2. The first piece can span [0,3), with a range of 3, so error of 1.5, exceeding epsilon. A better solution would be to place breakpoints to cut the function into segments of range at most 2. For f(x)=|x-5|, a piece can cover [3,7) with a range of 2. The remaining sections [0,3) and [7,10) each have a range of 3, so each needs one piece. Thus, 3 pieces are required."
    },
    {
        "description": "Gentle Slope: A function where the total variation is within tolerance.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 1], [10, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "notes": "The function's range over [0,10] is 1. The L-infinity error is 0.5, which is exactly equal to epsilon. Therefore, a single piece is a valid and optimal approximation."
    },
    {
        "description": "Large Jump Followed by Flat Section: Mixed behavior.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 100], [2, 100], [10, 100], [10, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "notes": "The large jump at x=1 forces a breakpoint. The first segment, [0, 1), has a large range. The optimal solution will cut it into one piece. The second segment, [1, 10), is constant and can be covered by a single piece. Thus, two pieces are optimal."
    },
    {
        "description": "Random Noisy Data: Tests algorithm's robustness.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.2], [1, 3.5], [2, 2.1], [3, 4.8], [4, 1.9], [5, 3.2], [6, 2.5], [7, 4.0], [8, 3.3], [9, 1.5], [10, 2.8], [10, float('inf')]],
        "epsilon": 0.8,
        "expected_pieces": "Variable",
        "notes": "The number of pieces will depend on the optimal partitioning of the intervals. The algorithm must find the longest possible sub-intervals where the range is at most 2*epsilon=1.6. A naive approach would create 10 pieces. An optimal algorithm should produce a smaller number."
    },
    {
        "description": "Function with Inflection Point: tests handling of a smooth curve.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 125], [10, 1000], [10, float('inf')]],
        "epsilon": 100,
        "expected_pieces": 2,
        "notes": "The function f(x) = x^3 has a smooth, increasing slope. Over [0,10], the range is 1000. Half-range is 500, which exceeds epsilon. An optimal solution will find a balance, likely resulting in two pieces, e.g., one on [0,6) and the other on [6,10), where the range on each subinterval is within the tolerance."
    }
]
#Iteration23
test_cases23 = [
    # 1. Linear Function with Small ε
    {
        'pc_fx': [[-float('inf'), 0], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [float('inf'), float('inf')]],
        'epsilon': 0.01,
        'description': 'Tests many small pieces needed for a linear function with small tolerance.'
    },
    # 2. Linear Function with Large ε
    {
        'pc_fx': [[-float('inf'), 0], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [float('inf'), float('inf')]],
        'epsilon': 1.0,
        'description': 'Tests if the algorithm correctly merges all segments into a single piece.'
    },
    # 3. Step Function with a Single Large Jump
    {
        'pc_fx': [[-float('inf'), 0], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 100], [float('inf'), float('inf')]],
        'epsilon': 10.0,
        'description': 'Tests handling of a sharp discontinuity that exceeds the tolerance.'
    },
    # 4. Constant Function
    {
        'pc_fx': [[-float('inf'), 0], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [float('inf'), float('inf')]],
        'epsilon': 0.5,
        'description': 'Tests if the algorithm recognizes a constant function and uses only one piece.'
    },
    # 5. Sine Wave (Periodic Function)
    {
        'pc_fx': [[-float('inf'), 0], [0, 0], [1, 0.84], [2, 0.91], [3, 0.14], [4, -0.76], [5, -0.96], [6, -0.28], [6.28, 0], [float('inf'), float('inf')]],
        'epsilon': 0.1,
        'description': 'Tests handling of non-monotonic, oscillating functions.'
    },
    # 6. Sawtooth Wave
    {
        'pc_fx': [[-float('inf'), 0], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [float('inf'), float('inf')]],
        'epsilon': 0.2,
        'description': 'Tests handling of repeating linear patterns with sharp drops.'
    },
    # 7. Piecewise Constant with Changes Below ε
    {
        'pc_fx': [[-float('inf'), 0], [0, 5], [1, 5.1], [2, 4.9], [3, 5.2], [4, 5.0], [5, 5.3], [float('inf'), float('inf')]],
        'epsilon': 0.5,
        'description': 'Tests if small variations are ignored and a single piece is used.'
    },
    # 8. Sharp V-Shape (Absolute Value Function)
    {
        'pc_fx': [[-float('inf'), 0], [0, 5], [1, 4], [2, 3], [3, 2], [4, 3], [5, 4], [6, 5], [float('inf'), float('inf')]],
        'epsilon': 0.5,
        'description': 'Tests handling of a sharp turning point, requiring a new piece at the vertex.'
    },
    # 9. Monotonic, Slowly Changing Function
    {
        'pc_fx': [[-float('inf'), 0], [0, 0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4], [5, 0.5], [float('inf'), float('inf')]],
        'epsilon': 0.2,
        'description': 'Tests merging of multiple segments when the function changes slowly.'
    },
    # 10. A Function with a Single Outlier Point
    {
        'pc_fx': [[-float('inf'), 0], [0, 5], [1, 5], [2, 5], [3, 10], [4, 5], [5, 5], [float('inf'), float('inf')]],
        'epsilon': 1.0,
        'description': 'Tests ability to isolate and handle a single, significant deviation from a constant.'
    }
]
#Iteration24
test_cases24 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 2.0,
        "expected_optimal_pieces": 1,
        "explanation": "Simple case: a single constant piece. The approximation should use one piece, as the tolerance is large enough."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_optimal_pieces": 4,
        "explanation": "Staircase function with exact tolerance. Each step requires its own piece; no adjacent pieces can be merged."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        "epsilon": 0.2,
        "expected_optimal_pieces": 1,
        "explanation": "Merging multiple small steps. All pieces can be merged into a single piece as the total deviation from a central value is within the tolerance."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [1.1, 0], [2, 0], [3, float('inf')]],
        "epsilon": 2.0,
        "expected_optimal_pieces": 2,
        "explanation": "Narrow spikes. The single spike at value 5 is too large to be merged with the surrounding 0-valued pieces. It must form its own piece, while the surrounding pieces can be merged."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [5, 11], [6, 10], [10, 10.5], [12, float('inf')]],
        "epsilon": 0.8,
        "expected_optimal_pieces": 2,
        "explanation": "Unevenly spaced steps. The first two pieces can be merged into one, and the last two can be merged into another, resulting in two optimal pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.4,
        "expected_optimal_pieces": 5,
        "explanation": "Zig-zag pattern. The '0' and '1' values are too far apart for the given tolerance, so each step requires its own piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 10.1], [3, 10.2], [4, float('inf')]],
        "epsilon": 0.1,
        "expected_optimal_pieces": 2,
        "explanation": "Large step followed by small steps. The first jump from 0 to 10 must form a separate piece, but the subsequent small steps can be merged into one."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 5.01], [2, 5.02], [3, 5.03], [4, 5.04], [5, float('inf')]],
        "epsilon": 0.05,
        "expected_optimal_pieces": 1,
        "explanation": "All values within a narrow band. The range of all values is less than the tolerance, so a single piece is optimal."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 10], [3, 0], [4, 0], [5, float('inf')]],
        "epsilon": 4.0,
        "expected_optimal_pieces": 1,
        "explanation": "Single large piece in the middle. The entire function can be represented by a single piece with an average value since the maximum deviation is within the tolerance."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, float('inf')]],
        "epsilon": 0.5,
        "expected_optimal_pieces": 2,
        "explanation": "Zero-width pieces (discontinuity). The jump from value 1 to 2 at x=0 is a discontinuity that cannot be merged. This requires two separate pieces."
    }
]
#Iteration25
test_cases25 = [
    {
        "description": "Simple Monotonic Function: tests basic functionality and single-piece solution.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "description": "Constant Function: tests if a function already constant is identified as one piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Step Function: handles discontinuities and adds a new piece at the jump point.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [1.000001, 10], [2, 10], [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 2
    },
    {
        "description": "Zero Tolerance (ε=0): approximation must be exact, returning the number of original pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [float('inf'), float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    {
        "description": "Large Tolerance: a large epsilon allows the entire function to be approximated by a single piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [float('inf'), float('inf')]],
        "epsilon": 10.0,
        "expected_pieces": 1
    },
    {
        "description": "Oscillating Function: tests finding a minimal number of pieces for rapid changes.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, 10], [float('inf'), float('inf')]],
        "epsilon": 5.0,
        "expected_pieces": 1
    },
    {
        "description": "Non-Monotonic with Flat Segments: handles varying behaviors without adding unnecessary pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 1], [3, 0], [4, -1], [5, -1], [float('inf'), float('inf')]],
        "epsilon": 0.2,
        "expected_pieces": 4
    },
    {
        "description": "Small ε leading to many pieces: high fidelity requires many pieces, testing performance and accuracy.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4], [5, 0.5], [float('inf'), float('inf')]],
        "epsilon": 0.01,
        "expected_pieces": 5
    },
    {
        "description": "Inaccessible Middle Values: tests recognition that a segment cannot be merged.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, 101], [3, 0], [float('inf'), float('inf')]],
        "epsilon": 10.0,
        "expected_pieces": 2
    },
    {
        "description": "Piecewise function that can be simplified: a direct test of the optimality goal.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 2], [4, 2.1], [float('inf'), float('inf')]],
        "epsilon": 0.3,
        "expected_pieces": 2
    }
]
#Iteration26
test_cases26 = [
    {
        "description": "Uniform, flat function",
        "f": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1]],
        "epsilon": 0.1,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 1], [4, float('inf')]],
        "expected_pieces": 1
    },
    {
        "description": "Step function with large gaps",
        "f": [[0, 1], [1, 1], [1, 2], [2, 2], [2, 1], [3, 1]],
        "epsilon": 0.05,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, float('inf')]],
        "expected_pieces": 3
    },
    {
        "description": "Linear increasing function",
        "f": [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]],
        "epsilon": 0.5,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 0.5], [1, 1.5], [2, 2.5], [3, 3.5], [4, float('inf')]],
        "expected_pieces": 4
    },
    {
        "description": "No-op case (high epsilon)",
        "f": [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]],
        "epsilon": 2.0,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 2], [4, float('inf')]],
        "expected_pieces": 1
    },
    {
        "description": "Strict tolerance (low epsilon)",
        "f": [[0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, 1.4]],
        "epsilon": 0.01,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        "expected_pieces": 4
    },
    {
        "description": "Sine wave-like function",
        "f": [[0, 0], [1, 0.5], [2, 0.8], [3, 0.5], [4, 0], [5, -0.5], [6, 0]],
        "epsilon": 0.2,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 0.25], [1, 0.65], [2, 0.65], [3, 0.25], [4, -0.25], [5, -0.25], [6, float('inf')]],
        "expected_pieces": 6
    },
    {
        "description": "Symmetry around a horizontal axis",
        "f": [[0, 0], [1, 1], [2, 0], [3, 1], [4, 0]],
        "epsilon": 0.25,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 0.5], [1, 0.5], [2, 0.5], [3, 0.5], [4, float('inf')]],
        "expected_pieces": 4
    },
    {
        "description": "Single point function",
        "f": [[0, 5]],
        "epsilon": 1.0,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 5], [0, float('inf')]],
        "expected_pieces": 1
    },
    {
        "description": "Random noise",
        "f": [[0, 1.0], [1, 1.2], [2, 0.9], [3, 1.1], [4, 0.8]],
        "epsilon": 0.3,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [4, float('inf')]],
        "expected_pieces": 1
    },
    {
        "description": "Constant segments with different values",
        "f": [[0, 5], [1, 5], [2, 5], [2.1, 8], [3, 8], [4, 8], [4.1, 2], [5, 2]],
        "epsilon": 0.05,
        "expected_pc_fx": [[-float('inf'), float('inf')], [0, 5], [2.1, 8], [4.1, 2], [5, float('inf')]],
        "expected_pieces": 3
    }
]
#Iteration27
test_cases27 = [
    # 1. Simple Linear Function
    {
        'description': 'Simple linear function approximated within tolerance.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [float('inf'), float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 1
    },
    # 2. Flat Function (No Change)
    {
        'description': 'Perfectly flat function should require only one piece.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [float('inf'), float('inf')]],
        'epsilon': 0.1,
        'expected_pieces': 1
    },
    # 3. Step Function
    {
        'description': 'Sharp jump requires a new piece.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [0, 1], [1, 1], [float('inf'), float('inf')]],
        'epsilon': 0.1,
        'expected_pieces': 2
    },
    # 4. Step Function with Large Epsilon
    {
        'description': 'Large epsilon allows a single piece to bridge a jump.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [0, 1], [1, 1], [float('inf'), float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 1
    },
    # 5. Quadratic Function
    {
        'description': 'A non-linear function requiring multiple pieces.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [0.5, 0.25], [1, 1], [float('inf'), float('inf')]],
        'epsilon': 0.1,
        'expected_pieces': 2
    },
    # 6. Sinusoidal Oscillation
    {
        'description': 'Oscillating function requiring multiple pieces for peaks and troughs.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [0.5, 1], [1, 0], [1.5, -1], [2, 0], [float('inf'), float('inf')]],
        'epsilon': 0.1,
        'expected_pieces': 4
    },
    # 7. Function with a Plateau
    {
        'description': 'Function with a flat segment that should be one piece.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [0.5, 0.5], [1, 0.5], [1.5, 0.5], [2, 1], [float('inf'), float('inf')]],
        'epsilon': 0.1,
        'expected_pieces': 3
    },
    # 8. Function with Small, Rapid Changes
    {
        'description': 'Rapid changes contained within the epsilon, requiring only one piece.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [0.1, 0.05], [0.2, 0.01], [0.3, 0], [float('inf'), float('inf')]],
        'epsilon': 0.05,
        'expected_pieces': 1
    },
    # 9. Sawtooth Function
    {
        'description': 'A repetitive pattern of linear segments.',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [0.5, 1], [1, 0], [1.5, 1], [2, 0], [float('inf'), float('inf')]],
        'epsilon': 0.2,
        'expected_pieces': 4
    },
    # 10. Large Data Set
    {
        'description': 'A larger set of data points to test performance.',
        'pc_fx': [[-float('inf'), float('inf')]] + [[i, 0.1 * i] for i in range(11)] + [[float('inf'), float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 1
    }
]
#Iteration28
test_cases28 = [
    {
        "description": "Flat function",
        "pc_fx": [[float('-inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_output": 1
    },
    {
        "description": "Stair-step function",
        "pc_fx": [[float('-inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "expected_output": 5
    },
    {
        "description": "Single-point piece",
        "pc_fx": [[float('-inf'), float('inf')], [0, 1], [0.0001, 5], [1, 1], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_output": 3
    },
    {
        "description": "Tolerance greater than max jump",
        "pc_fx": [[float('-inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [float('inf'), float('inf')]],
        "epsilon": 3.0,
        "expected_output": 2
    },
    {
        "description": "Zig-zag function",
        "pc_fx": [[float('-inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, 5], [4, 1], [5, 5], [float('inf'), float('inf')]],
        "epsilon": 2.0,
        "expected_output": 2
    },
    {
        "description": "No-change in value",
        "pc_fx": [[float('-inf'), float('inf')], [0, 10], [1, 10], [2, 10], [3, 10], [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "expected_output": 1
    },
    {
        "description": "Smallest possible tolerance",
        "pc_fx": [[float('-inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, 1], [float('inf'), float('inf')]],
        "epsilon": 0.000001,
        "expected_output": 5
    },
    {
        "description": "Large tolerance",
        "pc_fx": [[float('-inf'), float('inf')], [0, 1], [1, 10], [2, 2], [3, 15], [float('inf'), float('inf')]],
        "epsilon": 10.0,
        "expected_output": 1
    },
    {
        "description": "Symmetrical jumps",
        "pc_fx": [[float('-inf'), float('inf')], [0, 5], [1, 6], [2, 5], [3, 4], [4, 5], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_output": 3
    },
    {
        "description": "Combination of small and large jumps",
        "pc_fx": [[float('-inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 10], [4, 10.1], [5, 10.2], [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "expected_output": 2
    }
]
#Iteration29
test_cases29 = [
    {
        "description": "Simple Step Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "notes": "A single piece with a value of 3 would have an L-infinity error of 2, which exceeds the tolerance. Therefore, at least two pieces are required."
    },
    {
        "description": "Slowly Changing Slope",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, 0.2], [3, 0.3], [4, float('inf')]],
        "epsilon": 0.2,
        "expected_pieces": 1,
        "notes": "A single piece from [0, 4) with a value of 0.15 would have a maximum error of 0.15, which is within the tolerance. An optimal algorithm should return one piece."
    },
    {
        "description": "All Zeros",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 0], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "notes": "A constant function requires only a single piece. This is a baseline test for a trivial case."
    },
    {
        "description": "Zero Tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 3,
        "notes": "An L-infinity tolerance of zero means the approximation must be exact. The number of pieces must equal the number of original steps."
    },
    {
        "description": "Infinite Tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 100], [1, -50], [2, 200], [3, float('inf')]],
        "epsilon": 1000.0,
        "expected_pieces": 1,
        "notes": "With a very large tolerance, the entire function can be approximated by a single constant value, as the maximum error will be well within the limit."
    },
    {
        "description": "Alternating Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, -1], [2, 1], [3, -1], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "notes": "An optimal solution should combine pairs of segments. For example, [0, 2) can be approximated by a constant of 0, with a maximum error of 1, which meets the tolerance."
    },
    {
        "description": "Narrow Peaks",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [1.1, 0], [2, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 3,
        "notes": "The sharp peak from [1, 1.1) must be isolated into its own piece to satisfy the tight tolerance."
    },
    {
        "description": "Single Jump",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 10], [2, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "notes": "A single piece would have a mean value of 7.5 and a maximum error of 2.5, which exceeds the tolerance of 1.0. Two pieces are necessary."
    },
    {
        "description": "Large Gaps in Domain",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [10, 1], [20, 2], [30, 2], [40, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "notes": "The algorithm should combine the long constant segments. The function can be represented by two pieces: one for [0, 20) with value 1 and another for [20, 40) with value 2."
    },
    {
        "description": "Staircase Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.8,
        "expected_pieces": 2,
        "notes": "The algorithm should be able to group the steps. For example, the first two segments ([0, 1) and [1, 2)) can be combined into one piece with value 0.5 and a maximum error of 0.5, which is within the tolerance."
    }
]
#Iteration30
test_cases30 = [
    {
        "description": "Simple Monotonic Function: Checks for optimal pieces on a linear, increasing function with a small epsilon.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 10]],
        "epsilon": 2.0,
        "expected_pieces": 3  # Based on the function and epsilon
    },
    {
        "description": "Discontinuous Function: Verifies that a new piece is created at a discontinuity.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 3], [10, 3]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "All Points within Tolerance: Tests the trivial case where one piece is sufficient.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.1], [2 * 3.14159, 0.1]],
        "epsilon": 1.5,
        "expected_pieces": 1
    },
    {
        "description": "Zero Tolerance: Examines the edge case of epsilon = 0.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 10]],
        "epsilon": 0.0,
        "expected_pieces": float('inf') # Or a very large number, representing the function itself.
    },
    {
        "description": "Oscillating Function: Assesses the handling of a rapidly changing function.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2 * 3.14159, 0]],
        "epsilon": 0.5,
        "expected_pieces": 20 # Approximation based on the function and epsilon.
    },
    {
        "description": "Function with a Flat Section: Checks if the algorithm can efficiently use a single piece for a flat region.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 5], [10, 5]],
        "epsilon": 0.5,
        "expected_pieces": 3 # 2 for the slope, 1 for the flat part.
    },
    {
        "description": "Function with a Single Outlier Point: Tests isolation of a single outlier point.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 10], [5.000001, 1], [10, 1]],
        "epsilon": 0.5,
        "expected_pieces": 3
    },
    {
        "description": "Multiple Local Minima/Maxima: Verifies adaptation to non-uniform oscillations.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 10 * 3.14159]],
        "epsilon": 1.0,
        "expected_pieces": 7 # Based on the function and epsilon.
    },
    {
        "description": "Step Function with Varying Widths: Checks handling of unevenly spaced discontinuities.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [5, 3], [6, 3]],
        "epsilon": 0.5,
        "expected_pieces": 3
    },
    {
        "description": "Large Tolerance: Ensures a single piece is returned when the tolerance is generous.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2 * 3.14159, 1]],
        "epsilon": 5.0,
        "expected_pieces": 1
    }
]