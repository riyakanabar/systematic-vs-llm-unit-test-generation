# Zero-shot prompt on Gemini 2.5 Pro model
# 9 Sept 2025 6:48PM
import math

# For clarity, let's define a representation of infinity.
inf = float('inf')

# The test cases are stored in a list of dictionaries.
# Each dictionary contains a descriptive name, the input function (pc_fx),
# the tolerance (epsilon), and the expected minimum number of pieces.

test_cases = [
    {
        "name": "Test Case 1: Basic Sanity Check",
        "pc_fx": [[-inf, inf], [0, 1], [1, 2], [2, 1.5], [3, 8], [4, 9], [5, inf]],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "reason": "A standard case. The first three pieces ([0,3)) can be merged since max(1, 2, 1.5) - min(1, 2, 1.5) = 1 <= 2*0.5. The last two pieces ([3,5)) can also be merged."
    },
    {
        "name": "Test Case 2: Zero Epsilon",
        "pc_fx": [[-inf, inf], [0, 5], [1, 5.1], [2, 5], [3, inf]],
        "epsilon": 0,
        "expected_pieces": 3,
        "reason": "With ε=0, no simplification is possible unless adjacent pieces have identical values. The output should be identical to the input."
    },
    {
        "name": "Test Case 3: Large Epsilon",
        "pc_fx": [[-inf, inf], [0, 10], [1, -10], [2, 100], [3, 0], [4, inf]],
        "epsilon": 1000,
        "expected_pieces": 1,
        "reason": "When ε is very large, the entire function should be approximated by a single piece. Here, max-min = 100 - (-10) = 110, which is far less than 2*1000."
    },
    {
        "name": "Test Case 4: 'On the Edge' Merging",
        "pc_fx": [[-inf, inf], [0, 2], [1, 0], [2, 1], [3, 4], [4, inf]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "reason": "Tests the boundary condition of the merging rule. The first three pieces ([0,3)) have max-min = 2-0 = 2, which is exactly 2*ε. They should merge."
    },
    {
        "name": "Test Case 5: 'Just Over the Edge' Precision",
        "pc_fx": [[-inf, inf], [0, 2.0], [1, 0.0], [2, 4.0001], [3, 5.0], [4, inf]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "reason": "Tests floating-point precision. The first two pieces merge. When considering the third piece, max-min = 4.0001 - 0.0 = 4.0001, which is just over 2*ε. The greedy algorithm should correctly create a piece for [0,2) and then start a new one."
    },
    {
        "name": "Test Case 6: Oscillating Function",
        "pc_fx": [[-inf, inf], [0, 10], [1, 0], [2, 10], [3, 0], [4, 10], [5, inf]],
        "epsilon": 4,
        "expected_pieces": 4,
        "reason": "In this highly oscillating function, the range of any two adjacent pieces is 10, which is greater than 2*ε = 8. No merging should occur."
    },
    {
        "name": "Test Case 7: Monotonically Increasing Function",
        "pc_fx": [[-inf, inf], [0, 1], [1, 2], [2, 3], [3, 4], [4, 10], [5, 12], [6, inf]],
        "epsilon": 1.2,
        "expected_pieces": 3,
        "reason": "Tests the greedy extension on a monotonic sequence. The first three pieces ([0,3)) merge as max-min=2 <= 2*1.2. The fourth piece (value 4) breaks the condition. The fifth and sixth pieces merge as max-min=2 <= 2*1.2."
    },
    {
        "name": "Test Case 8: Function with Plateaus",
        "pc_fx": [[-inf, inf], [0, 5], [1, 5], [2, 5], [3, 10], [4, 10], [5, inf]],
        "epsilon": 1,
        "expected_pieces": 2,
        "reason": "An algorithm should always merge adjacent pieces with identical values (since max-min=0). This tests if it correctly groups the '5's and the '10's."
    },
    {
        "name": "Test Case 9: Greedy Choice 'Dip and Rise'",
        "pc_fx": [[-inf, inf], [0, 10], [1, 9], [2, 12], [3, 11], [4, inf]],
        "epsilon": 1,
        "expected_pieces": 2,
        "reason": "This tests the greedy choice. Merging [0,1) and [1,2) is valid (max-min=1). Adding [2,3) is not (max-min=3 > 2*ε). A correct greedy algorithm finalizes the first piece over [0,2) and then merges the last two."
    },
    {
        "name": "Test Case 10: Single Piece Input",
        "pc_fx": [[-inf, inf], [0, 100], [10, inf]],
        "epsilon": 0.001,
        "expected_pieces": 1,
        "reason": "The simplest edge case. An input with only one effective piece should always return one piece, regardless of ε (assuming ε >= 0)."
    }
]

# Example of how you might use these test cases with a hypothetical function
# `approximate(pc_fx, epsilon)` that returns the number of pieces.

# def approximate(pc_fx, epsilon):
#     # ... implementation of the algorithm ...
#     # return number_of_pieces
#
# for i, case in enumerate(test_cases):
#     result = approximate(case["pc_fx"], case["epsilon"])
#     print(f"--- Running {case['name']} ---")
#     print(f"Input: {case['pc_fx']}, Epsilon: {case['epsilon']}")
#     print(f"Expected: {case['expected_pieces']}, Got: {result}")
#     print(f"Pass: {result == case['expected_pieces']}")
#     print(f"Reasoning: {case['reason']}\n")