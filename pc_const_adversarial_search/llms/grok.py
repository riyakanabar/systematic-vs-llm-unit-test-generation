#27 Sept 3:51PM few-shot prompt used to generate 30 test cases (Grok3 Auto mode)(took 1hr)
import math

test_cases1 = [
    {
        "pc_fx": [[-math.inf, math.inf], [0, 2], [1, 3], [3, 7], [6, 5], [7, math.inf]],
        "epsilon": 0.75
    },
    {
        "pc_fx": [[-math.inf, math.inf], [-10, 4.5], [10, math.inf]],
        "epsilon": 0.0
    },
    {
        "pc_fx": [[-math.inf, math.inf], [0, 5], [2, 5], [4, 5], [6, 5], [8, 5], [10, math.inf]],
        "epsilon": 0
    },
    {
        "pc_fx": [[-math.inf, math.inf], [0, 0], [1, 10], [2, 0], [3, 10], [4, math.inf]],
        "epsilon": 4
    },
    {
        "pc_fx": [[-math.inf, math.inf], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, math.inf]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0], [6, math.inf]],
        "epsilon": 2.5
    },
    {
        "pc_fx": [[-math.inf, math.inf], [0, -10], [2, -5], [4, 0], [6, 5], [8, 10], [10, math.inf]],
        "epsilon": 4
    },
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, math.inf]],
        "epsilon": 0
    },
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, math.inf]],
        "epsilon": 100
    },
    {
        "pc_fx": [[-math.inf, math.inf], [0.0, 1.1], [0.5, 1.2], [1.0, 1.3], [1.5, 2.0], [2.0, math.inf]],
        "epsilon": 0.05
    }
]
test_cases2 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-1, 4], [0, 4], [2, 4], [5, 4], [10, float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1], [3, 1.5], [4, 2], [5, float('inf')]],
        "epsilon": 0.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4.9
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 2], [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 2], [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 10
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-5, 3.14], [10, float('inf')]],
        "epsilon": 0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-10, -5], [-5, -4], [0, -8], [5, float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0000000001], [1, 1.0000000002], [2, float('inf')]],
        "epsilon": 1e-10
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 5
    }
]
test_cases3 = [
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,3],[3,7],[6,5],[7,float('inf')]],
        "epsilon": 0.75
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[10,float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[2,2],[4,2],[6,2],[8,float('inf')]],
        "epsilon": 0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,float('inf')]],
        "epsilon": 5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,4],[5,float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,4],[1,3],[2,2],[3,1],[4,0],[5,float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,0],[3,10],[4,0],[5,float('inf')]],
        "epsilon": 4
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[-5,-3],[-3,-2.5],[0,1],[2,3.5],[4,float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,float('inf')]],
        "epsilon": 0
    }
]
inf = float('inf')
test_cases4 = [
    # Test case 1: Example provided
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]], "epsilon": 0.75},

    # Test case 2: Single piece, should remain 1 piece for any epsilon
    {"pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, float('inf')]], "epsilon": 0.5},

    # Test case 3: Multiple pieces with same value, should merge to 1 piece if epsilon allows
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]], "epsilon": 0.1},

    # Test case 4: Pieces with values differing more than 2*epsilon, no merging possible
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]], "epsilon": 4},

    # Test case 5: Epsilon=0, no merging possible, min pieces = number of original pieces
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]], "epsilon": 0},

    # Test case 6: Large epsilon, should merge all to 1 piece
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 2], [3, 9], [4, float('inf')]], "epsilon": 5},

    # Test case 7: Oscillating values, limited merging if differences large
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]], "epsilon": 4.9},

    # Test case 8: Gradually increasing values, partial merging
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, float('inf')]], "epsilon": 1},

    # Test case 9: Gradually decreasing values with negative numbers
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0], [6, -1], [7, float('inf')]], "epsilon": 1.5},

    # Test case 10: Floating point values, precision edge case
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0.1], [1, 0.2], [2, 1.5], [3, 0.3], [4, 0.15], [5, float('inf')]], "epsilon": 0.5}
]
test_cases5 = [
    # Case 1: Single piece, should remain 1 piece
    {"pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, float('inf')]], "epsilon": 1.0},

    # Case 2: Multiple pieces with equal values, epsilon=0, should merge to 1 piece
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, float('inf')]], "epsilon": 0},

    # Case 3: Increasing values within 2*epsilon, should merge to 1 piece
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]], "epsilon": 2.0},

    # Case 4: Increasing values exceeding 2*epsilon at the end, greedy should merge first 4 to 1, last to 1, total 2 pieces
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 5], [5, float('inf')]], "epsilon": 2.0},

    # Case 5: Oscillating values within 2*epsilon, should merge to 1 piece
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]], "epsilon": 5.0},

    # Case 6: Oscillating values slightly exceeding 2*epsilon, cannot merge any adjacent, should remain 5 pieces
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]], "epsilon": 4.9},

    # Case 7: Three groups of close values separated by large jumps, should merge to 3 pieces
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 0.9], [3, 10], [4, 10.2], [5, 9.8], [6, 1], [7, 1.5], [8, 0.5], [9, float('inf')]], "epsilon": 0.5},

    # Case 8: Oscillating with range exactly 2*epsilon, should merge to 1 piece
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, float('inf')]], "epsilon": 1.0},

    # Case 9: Oscillating with range slightly over 2*epsilon, cannot merge any, should remain 3 pieces
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2.0001], [2, 0], [3, float('inf')]], "epsilon": 1.0},

    # Case 10: Different values with epsilon=0, cannot merge any, should remain 4 pieces
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]], "epsilon": 0}
]
test_cases6 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, float('inf')]],
        "epsilon": 5.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, float('inf')]],
        "epsilon": 0.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        "epsilon": 1.1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.5], [2, 1.0], [3, 1.5], [4, 2.0], [5, 2.5], [6, float('inf')]],
        "epsilon": 0.6
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, float('inf')]],
        "epsilon": 0.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2.1], [2, 0], [3, float('inf')]],
        "epsilon": 1.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, float('inf')]],
        "epsilon": 4.4
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 1.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, 0], [2, 1], [3, -1], [4, float('inf')]],
        "epsilon": 1.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0.5, 0], [2.5, 2], [4.5, float('inf')]],
        "epsilon": 1
    }
]
test_cases7 = [
    # Case 1: Single piece, arbitrary epsilon
    {
        "pc_fx": [[-inf, inf], [0, 5], [10, inf]],
        "epsilon": 1.0
    },
    # Case 2: Multiple pieces with identical values, epsilon=0, should merge to 1
    {
        "pc_fx": [[-inf, inf], [0, 3], [1, 3], [2, 3], [3, 3], [4, inf]],
        "epsilon": 0
    },
    # Case 3: Drifting values where adjacent diffs small but cumulative exceeds 2*epsilon, exposes naive consecutive check
    {
        "pc_fx": [[-inf, inf], [0, 0], [1, 0.5], [2, 1.0], [3, 1.5], [4, 2.0], [5, inf]],
        "epsilon": 0.5
    },
    # Case 4: Drifting down with negatives
    {
        "pc_fx": [[-inf, inf], [0, 0], [1, -0.5], [2, -1.0], [3, -1.5], [4, -2.0], [5, inf]],
        "epsilon": 0.5
    },
    # Case 5: Oscillating values with large jumps, cannot merge, epsilon small
    {
        "pc_fx": [[-inf, inf], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, inf]],
        "epsilon": 1.0
    },
    # Case 6: Values exactly at 2*epsilon boundary, should merge
    {
        "pc_fx": [[-inf, inf], [0, 1], [1, 3], [2, inf]],
        "epsilon": 1.0  # |1-3|=2 <= 2*1
    },
    # Case 7: Values just over 2*epsilon, cannot merge
    {
        "pc_fx": [[-inf, inf], [0, 1], [1, 3.1], [2, inf]],
        "epsilon": 1.0  # |1-3.1|=2.1 > 2*1
    },
    # Case 8: Epsilon=0 with different values, must keep all
    {
        "pc_fx": [[-inf, inf], [0, 1], [1, 2], [2, 3], [3, inf]],
        "epsilon": 0
    },
    # Case 9: Large epsilon, merges all even with varied values
    {
        "pc_fx": [[-inf, inf], [0, -10], [1, 0], [2, 10], [3, 20], [4, inf]],
        "epsilon": 15.0  # range 20-(-10)=30 <= 2*15=30
    },
    # Case 10: Clustered groups, multiple mergeable clusters separated by large jump
    {
        "pc_fx": [[-inf, inf], [0, 1.0], [1, 1.1], [2, 1.2], [3, 10.0], [4, 10.1], [5, 10.2], [6, inf]],
        "epsilon": 0.1  # Two groups: [1.0,1.1,1.2] range 0.2<=0.2, [10.0,10.1,10.2] 0.2<=0.2
    }
]
test_cases8 = [
    {'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]], 'epsilon': 1},
    {'pc_fx': [[-float('inf'), float('inf')], [-5, 2.5], [0, 2.5], [5, float('inf')]], 'epsilon': 0},
    {'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, float('inf')]], 'epsilon': 0.6},
    {'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, float('inf')]], 'epsilon': 0.5},
    {'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1.0], [3, 1.5], [4, 2.0], [5, float('inf')]], 'epsilon': 0.75},
    {'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]], 'epsilon': 0.5},
    {'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 3], [2, 0], [3, 3], [4, 0], [5, float('inf')]], 'epsilon': 1},
    {'pc_fx': [[-float('inf'), float('inf')], [-3, -1], [-2, -1], [-1, -1], [0, 10], [1, 10], [2, 10], [3, -1], [4, -1], [5, -1], [6, float('inf')]], 'epsilon': 1},
    {'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]], 'epsilon': 0},
    {'pc_fx': [[-float('inf'), float('inf')], [-10, -5.5], [0, 100], [10, -100], [20, 50], [30, float('inf')]], 'epsilon': 1000}
]
test_cases9 = [
    # Test Case 1: Single piece, should return one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 2: Two pieces with y-values within 2ε, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, float('inf')]],
        "epsilon": 0.3  # |2 - 2.5| = 0.5 < 2 * 0.3 = 0.6
    },
    # Test Case 3: Two pieces with y-values just outside 2ε, should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3.1], [2, float('inf')]],
        "epsilon": 0.5  # |2 - 3.1| = 1.1 > 2 * 0.5 = 1.0
    },
    # Test Case 4: Multiple pieces with identical y-values, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, float('inf')]],
        "epsilon": 0.1
    },
    # Test Case 5: Large ε, should merge all pieces into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 10], [3, float('inf')]],
        "epsilon": 5  # Max difference |1 - 10| = 9 < 2 * 5 = 10
    },
    # Test Case 6: Small ε, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, float('inf')]],
        "epsilon": 0.25  # Differences of 1 > 2 * 0.25 = 0.5
    },
    # Test Case 7: Negative y-values, testing merging with negative differences
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -1.5], [2, -2], [3, float('inf')]],
        "epsilon": 0.3  # |(-1) - (-1.5)| = 0.5 < 2 * 0.3 = 0.6
    },
    # Test Case 8: Consecutive x-values very close, testing numerical stability
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.000001, 1.2], [1, float('inf')]],
        "epsilon": 0.15  # |1 - 1.2| = 0.2 < 2 * 0.15 = 0.3
    },
    # Test Case 9: Alternating y-values, testing optimal merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 0.5  # |0 - 1| = 1 ≤ 2 * 0.5 = 1, should merge optimally
    },
    # Test Case 10: Large y-value differences, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, 0], [3, float('inf')]],
        "epsilon": 10  # |0 - 100| = 100 > 2 * 10 = 20
    }
]
test_cases10 = [
    # Test Case 1: Single piece, should return one piece regardless of ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece, no merging possible"
    },
    # Test Case 2: Adjacent pieces with y-difference exactly ε, should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces with y-difference exactly ε, should remain separate"
    },
    # Test Case 3: Adjacent pieces with y-difference less than ε, should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.4], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces with y-difference less than ε, should merge into one"
    },
    # Test Case 4: Multiple pieces all within ε, should merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 1.4], [3, 1.1], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Multiple pieces with max y-difference ≤ ε, should merge into one"
    },
    # Test Case 5: Large y-value jump exceeding ε, should split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, float('inf')]],
        "epsilon": 1.0,
        "description": "Two pieces with y-difference > ε, should remain separate"
    },
    # Test Case 6: Repeated y-values, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.1,
        "description": "Multiple pieces with identical y-values, should merge into one"
    },
    # Test Case 7: Very small ε, should keep all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.01], [2, 1.02], [3, float('inf')]],
        "epsilon": 0.005,
        "description": "Small ε, differences > ε, should keep all pieces"
    },
    # Test Case 8: Large ε, should merge all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 10], [3, float('inf')]],
        "epsilon": 10.0,
        "description": "Large ε, all y-differences ≤ ε, should merge into one"
    },
    # Test Case 9: Dense x-intervals with alternating y-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0.1, 1], [0.2, 0], [0.3, 1], [0.4, float('inf')]],
        "epsilon": 0.5,
        "description": "Dense x-intervals with alternating y-values, should alternate pieces"
    },
    # Test Case 10: Boundary case with large x-range
    {
        "pc_fx": [[-float('inf'), float('inf')], [-1e308, 0], [0, 1], [1e308, float('inf')]],
        "epsilon": 0.5,
        "description": "Large x-range near infinity boundaries, should handle boundary conditions"
    }
]
test_cases11 = [
    # Test Case 1: Single piece, no merging needed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece, should return one piece."
    },
    # Test Case 2: Two pieces with y-difference ≤ 2ε, should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, float('inf')]],
        "epsilon": 0.25,
        "description": "Two pieces with |y2 - y1| = 0.5 ≤ 2ε = 0.5, should merge into one piece."
    },
    # Test Case 3: Two pieces with y-difference > 2ε, no merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3.1], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces with |y2 - y1| = 1.1 > 2ε = 1.0, should not merge."
    },
    # Test Case 4: Multiple pieces, all y-values equal, should merge to one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 3], [4, float('inf')]],
        "epsilon": 0.1,
        "description": "All y-values equal, should merge into one piece regardless of ε."
    },
    # Test Case 5: Large ε allows merging all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 5], [3, float('inf')]],
        "epsilon": 2.0,
        "description": "Large ε = 2.0, max |y_i - y_j| = 4 ≤ 2ε = 4, should merge into one piece."
    },
    # Test Case 6: Small ε prevents merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, float('inf')]],
        "epsilon": 0.05,
        "description": "Small ε = 0.05, differences > 2ε = 0.1, should keep all pieces."
    },
    # Test Case 7: Non-integer y-values and ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.5], [2, 2.3], [4, 1.7], [6, float('inf')]],
        "epsilon": 0.4,
        "description": "Non-integer values, |2.3 - 1.5| = 0.8 ≤ 2ε = 0.8, |1.7 - 1.5| = 0.2 ≤ 0.8, should merge into one piece."
    },
    # Test Case 8: Repeated x-coordinates with small intervals
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [0.1, 2.2], [0.2, 2.1], [1, float('inf')]],
        "epsilon": 0.15,
        "description": "Small x-intervals, |y_i - y_j| ≤ 0.2 ≤ 2ε = 0.3, should merge into one piece."
    },
    # Test Case 9: Large x-coordinate range
    {
        "pc_fx": [[-float('inf'), float('inf')], [-1e10, 5], [0, 5.5], [1e10, 5.2], [1e10+1, float('inf')]],
        "epsilon": 0.3,
        "description": "Large x-range, |y_i - y_j| ≤ 0.5 ≤ 2ε = 0.6, should merge into one piece."
    },
    # Test Case 10: Example from prompt
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "description": "Example case: Differences |3-2|=1, |7-3|=4, |7-5|=2, |5-2|=3. With ε=0.75, check if merges optimally (e.g., [0,1) and [1,3) may merge since |3-2|=1 ≤ 2ε=1.5)."
    }
]
test_cases12 = [
    # Test Case 1: Single piece, no merging needed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece, should return one piece regardless of epsilon"
    },
    # Test Case 2: Two pieces with y-values within epsilon, should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, float('inf')]],
        "epsilon": 0.75,
        "description": "Two pieces with |y2 - y1| <= 2*epsilon, should merge into one piece"
    },
    # Test Case 3: Two pieces with y-values just outside epsilon, should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3.1], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces with |y2 - y1| > 2*epsilon, should remain two pieces"
    },
    # Test Case 4: Multiple pieces, all equal y-values, should merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 3], [4, float('inf')]],
        "epsilon": 0.1,
        "description": "All pieces have same y-value, should merge into one piece"
    },
    # Test Case 5: Large jumps in y-values, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 10], [3, float('inf')]],
        "epsilon": 0.5,
        "description": "Large y-value differences, should keep all pieces"
    },
    # Test Case 6: Small intervals with alternating y-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 2], [0.2, 1], [0.3, 2], [0.4, float('inf')]],
        "epsilon": 0.5,
        "description": "Small intervals with alternating y-values, tests handling of short segments"
    },
    # Test Case 7: Zero epsilon, no merging allowed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.0,
        "description": "Epsilon = 0, no merging possible, should keep all pieces"
    },
    # Test Case 8: Large epsilon, all pieces mergeable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 10.0,
        "description": "Large epsilon, all pieces should merge into one"
    },
    # Test Case 9: Minimal input (two points)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, float('inf')]],
        "epsilon": 1.0,
        "description": "Minimal input with no actual pieces, should handle gracefully"
    },
    # Test Case 10: Floating-point precision edge case
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0 + 1e-10], [2, float('inf')]],
        "epsilon": 1e-10,
        "description": "y-values differ by epsilon, tests floating-point precision"
    }
]
test_cases13 = [
    # Test Case 1: Single piece, should remain one piece regardless of ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece, should not be split for any ε"
    },
    # Test Case 2: Two pieces with difference exactly equal to ε, should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces with |y2 - y1| = ε, should merge into one piece"
    },
    # Test Case 3: Two pieces with difference just above ε, should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3.01], [2, float('inf')]],
        "epsilon": 1.0,
        "description": "Two pieces with |y2 - y1| slightly > ε, should remain two pieces"
    },
    # Test Case 4: Multiple pieces within ε, should merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 1.4], [3, 1.1], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Multiple pieces all within ε of each other, should merge into one piece"
    },
    # Test Case 5: Large jump exceeding ε, should split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, float('inf')]],
        "epsilon": 2.0,
        "description": "Large jump > ε in middle, should result in at least two pieces"
    },
    # Test Case 6: Zero ε, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.0001], [2, float('inf')]],
        "epsilon": 0.0,
        "description": "ε = 0, no merging allowed, should keep all pieces"
    },
    # Test Case 7: Large ε, merges all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 10], [3, float('inf')]],
        "epsilon": 10.0,
        "description": "Large ε, should merge all pieces into one"
    },
    # Test Case 8: Empty input (only boundaries), should return empty or single piece
    {
        "pc_fx": [[-float('inf'), float('inf')]],
        "epsilon": 1.0,
        "description": "Empty input with only boundaries, should handle gracefully"
    },
    # Test Case 9: Overlapping or same breakpoints, should handle degeneracy
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Overlapping breakpoints, should handle degenerate case"
    },
    # Test Case 10: Example from the problem, mixed values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "description": "Mixed values with varying differences, tests general case"
    }
]
test_cases14 = [
    # Test Case 1: Empty input (no pieces between boundaries)
    {
        "pc_fx": [[-float('inf'), float('inf')], [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # Test Case 2: Single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 3: Multiple pieces with same y-value (should merge into one)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 4: Alternating y-values within 2ε (should merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1.2], [3, float('inf')]],
        "epsilon": 0.3
    },

    # Test Case 5: Alternating y-values exceeding 2ε (should not merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 6: Monotonic increasing y-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.6
    },

    # Test Case 7: Monotonic decreasing y-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4], [2, 3], [3, 2], [4, float('inf')]],
        "epsilon": 0.6
    },

    # Test Case 8: Small ε requiring all pieces to remain distinct
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.1
    },

    # Test Case 9: Large ε allowing merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 5], [3, float('inf')]],
        "epsilon": 2.0
    },

    # Test Case 10: Non-integer y-values and ε, with mixed differences
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.5], [1, 2.7], [2, 2.0], [3, 3.2], [4, float('inf')]],
        "epsilon": 0.75
    }
]
test_cases15 = [
    # Test Case 1: Single segment, should return 1 piece
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, math.inf]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # Test Case 2: Two segments with y-values within 2ε, should merge to 1 piece
    {
        "pc_fx": [[-math.inf, math.inf], [0, 2], [1, 2.5], [2, math.inf]],
        "epsilon": 0.3,  # 2ε = 0.6, |2.5 - 2| = 0.5 ≤ 0.6
        "expected_pieces": 1
    },
    # Test Case 3: Two segments with y-values just beyond 2ε, should return 2 pieces
    {
        "pc_fx": [[-math.inf, math.inf], [0, 2], [1, 3.1], [2, math.inf]],
        "epsilon": 0.5,  # 2ε = 1.0, |3.1 - 2| = 1.1 > 1.0
        "expected_pieces": 2
    },
    # Test Case 4: Multiple segments with identical y-values, should merge to 1 piece
    {
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 5], [2, 5], [3, math.inf]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    # Test Case 5: Alternating high-low values within 2ε, should merge to 1 piece
    {
        "pc_fx": [[-math.inf, math.inf], [0, 0], [1, 1], [2, 0], [3, 1], [4, math.inf]],
        "epsilon": 0.5,  # 2ε = 1.0, all y-values (0 or 1) are within 1.0
        "expected_pieces": 1
    },
    # Test Case 6: Large ε allowing all segments to merge
    {
        "pc_fx": [[-math.inf, math.inf], [0, 0], [1, 10], [2, 5], [3, 15], [4, math.inf]],
        "epsilon": 10.0,  # 2ε = 20.0, max y-diff = 15 - 0 = 15 ≤ 20.0
        "expected_pieces": 1
    },
    # Test Case 7: Small ε preventing any merging
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, math.inf]],
        "epsilon": 0.1,  # 2ε = 0.2, min y-diff = 1 > 0.2
        "expected_pieces": 3
    },
    # Test Case 8: Negative y-values with close segments
    {
        "pc_fx": [[-math.inf, math.inf], [0, -1], [0.1, -1.1], [0.2, -1.05], [0.3, math.inf]],
        "epsilon": 0.1,  # 2ε = 0.2, max y-diff = |-1 - (-1.1)| = 0.1 ≤ 0.2
        "expected_pieces": 1
    },
    # Test Case 9: Long sequence with gradual changes
    {
        "pc_fx": [[-math.inf, math.inf], [0, 0], [1, 0.2], [2, 0.4], [3, 0.6], [4, 0.8], [5, 1.0], [6, math.inf]],
        "epsilon": 0.15,  # 2ε = 0.3, each step = 0.2, can merge pairs
        "expected_pieces": 3  # [0,0.2], [0.4,0.6], [0.8,1.0]
    },
    # Test Case 10: Empty input (edge case with no segments)
    {
        "pc_fx": [[-math.inf, math.inf], [0, math.inf]],
        "epsilon": 1.0,
        "expected_pieces": 0
    }
]
test_cases16 = [
    # Test Case 1: Basic case with distinct values and reasonable epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "description": "Basic case with distinct y-values and moderate epsilon to test merging of close segments."
    },
    # Test Case 2: Single piece, should return one piece regardless of epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece function, tests if algorithm returns minimal (one) piece."
    },
    # Test Case 3: Identical y-values across all pieces, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.1,
        "description": "All y-values identical, should merge into one piece for any positive epsilon."
    },
    # Test Case 4: Large y-value jumps, epsilon too small to merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, float('inf')]],
        "epsilon": 4.0,
        "description": "Large jumps in y-values (10 units), epsilon too small to merge pieces."
    },
    # Test Case 5: Epsilon exactly equals max difference, boundary case
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 4], [2, 2], [3, float('inf')]],
        "epsilon": 2.0,
        "description": "Epsilon equals max y-value difference, tests boundary condition for merging."
    },
    # Test Case 6: Zero epsilon, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.0001], [2, 1], [3, float('inf')]],
        "epsilon": 0.0,
        "description": "Zero epsilon, should return all pieces as no merging is allowed."
    },
    # Test Case 7: Very small intervals with close y-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.0001, 1.1], [0.0002, 1], [0.0003, float('inf')]],
        "epsilon": 0.2,
        "description": "Very small intervals with close y-values, tests handling of near-continuous data."
    },
    # Test Case 8: Negative y-values and large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -5], [1, -4], [2, -6], [3, float('inf')]],
        "epsilon": 10.0,
        "description": "Negative y-values with large epsilon, should merge into one piece."
    },
    # Test Case 9: Single point interval (zero-width piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [0, 4], [1, 4], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Zero-width piece at x=0, tests handling of degenerate intervals."
    },
    # Test Case 10: Large number of pieces with alternating values
    {
        "pc_fx": [[-float('inf'), float('inf')]] + [[i/2, 1 if i % 2 == 0 else 2] for i in range(20)] + [[10, float('inf')]],
        "epsilon": 0.5,
        "description": "Many alternating y-values (1 and 2), tests scalability and merging logic."
    }
]
test_cases17 = [
    # Test Case 1: Single piece, should require only one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece, should return one piece as all points within epsilon"
    },
    # Test Case 2: Adjacent pieces with small difference, mergeable within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, float('inf')]],
        "epsilon": 0.75,
        "description": "Two pieces with |y1 - y2| <= 2*epsilon, should merge into one piece"
    },
    # Test Case 3: Adjacent pieces with large difference, non-mergeable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 4], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces with |y1 - y2| > 2*epsilon, should remain two pieces"
    },
    # Test Case 4: Multiple pieces, some mergeable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "description": "Multiple pieces, some within 2*epsilon, expect partial merging"
    },
    # Test Case 5: Zero tolerance, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.0001], [2, float('inf')]],
        "epsilon": 0.0,
        "description": "Zero epsilon, no pieces can merge, expect original number of pieces"
    },
    # Test Case 6: Large epsilon, all pieces mergeable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 10], [3, float('inf')]],
        "epsilon": 5.0,
        "description": "Large epsilon, all pieces can merge into one"
    },
    # Test Case 7: Empty function (only boundaries)
    {
        "pc_fx": [[-float('inf'), float('inf')]],
        "epsilon": 1.0,
        "description": "Empty function, should return empty or single constant piece"
    },
    # Test Case 8: Single point with infinite intervals
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0, float('inf')]],
        "epsilon": 1.0,
        "description": "Degenerate case with zero-width interval"
    },
    # Test Case 9: Alternating large and small differences
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, 5], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.15,
        "description": "Alternating small and large differences, partial merging expected"
    },
    # Test Case 10: Very small epsilon, near floating-point precision
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1 + 1e-10], [2, float('inf')]],
        "epsilon": 1e-11,
        "description": "Very small epsilon, tests precision handling, expect no merging"
    }
]
test_cases18 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single segment: Should return one piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 2.5], [3, float('inf')]],
        "epsilon": 0.0,
        "description": "Zero tolerance: Should return original function (3 pieces)."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 2.0,
        "description": "Large tolerance: Should merge all segments into one piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 0.1,
        "description": "Equal values: Should merge all segments into one piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 4], [3, float('inf')]],
        "epsilon": 0.5,
        "description": "Small tolerance: No segments merge, expect 3 pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1e308], [1, -1e308], [2, float('inf')]],
        "epsilon": 1.0,
        "description": "Boundary values: Tests handling of near-infinity values."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [0, 3], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single point segment: Tests zero-width segment [0,0)."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 5.0,
        "description": "Alternating values: Tests optimal merging of oscillating values."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [0, 2], [1, 3], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Duplicate points: Tests handling of repeated x-coordinates."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 2], [10, 3], [100, float('inf')]],
        "epsilon": 1.0,
        "description": "Non-uniform intervals: Tests merging with varying interval lengths."
    }
]
test_cases19 = [
    # Test Case 1: Basic case with small differences, should merge some pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.2], [3, float('inf')]],
        "epsilon": 0.4
    },
    # Test Case 2: Single piece, no merging needed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 3: Large value jumps, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 10], [3, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 4: All values equal, should merge to one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 3], [4, float('inf')]],
        "epsilon": 0.1
    },
    # Test Case 5: Values just within 2ε, should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.9], [2, 1.1], [3, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 6: Values just outside 2ε, should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2.1], [2, 1.1], [3, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 7: Negative values with small differences
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -1.2], [2, -0.9], [3, float('inf')]],
        "epsilon": 0.2
    },
    # Test Case 8: Non-integer x-coordinates and values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0.5, 2.3], [1.7, 2.8], [2.9, 2.4], [4.1, float('inf')]],
        "epsilon": 0.3
    },
    # Test Case 9: Very small epsilon, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.01], [2, 1.02], [3, float('inf')]],
        "epsilon": 0.001
    },
    # Test Case 10: Repeated x-coordinates with varying values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0, 1], [1, 1], [1, 0], [2, float('inf')]],
        "epsilon": 0.5
    }
]
test_cases20 = [
    # Test Case 1: Simple case with small changes within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.2], [3, float('inf')]],
        "epsilon": 0.75
    },
    # Test Case 2: Constant function (should reduce to one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 3: Large epsilon allowing full merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 2], [3, float('inf')]],
        "epsilon": 10.0
    },
    # Test Case 4: Small epsilon preventing any merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 5: Single piece (minimal case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [1, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 6: Discontinuous jumps just within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 7: Discontinuous jumps just outside epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1.1], [2, 0], [3, 1.1], [4, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 8: Zero epsilon (no merging possible)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.001], [2, 2], [3, float('inf')]],
        "epsilon": 0.0
    },
    # Test Case 9: Large values with small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1000], [1, 1000.1], [2, 1000], [3, float('inf')]],
        "epsilon": 0.05
    },
    # Test Case 10: Multiple pieces with varying lengths and values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.5, 1.5], [1, 1], [2, 2], [3, 1.8], [4, float('inf')]],
        "epsilon": 0.6
    }
]
test_cases21 = [
    # Test Case 1: Basic case with potential to merge adjacent pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.2], [3, float('inf')]],
        "epsilon": 0.3
    },
    # Test Case 2: Single piece, should return one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 3: y-values exactly 2ε apart, testing merge boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 4: y-values just over 2ε, should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3.01], [2, 1], [3, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 5: Large ε, should merge all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, -5], [3, 7], [4, float('inf')]],
        "epsilon": 10.0
    },
    # Test Case 6: Small ε, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.1
    },
    # Test Case 7: Oscillating y-values within ε, testing multiple merges
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 0.8], [3, 1.1], [4, 0.9], [5, float('inf')]],
        "epsilon": 0.2
    },
    # Test Case 8: Zero-length intervals (repeated x-values)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, 2], [1, 3], [2, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 9: Extreme y-value differences
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1e10], [1, -1e10], [2, 1e10], [3, float('inf')]],
        "epsilon": 1e9
    },
    # Test Case 10: Irregular intervals with small ε, testing precision
    {
        "pc_fx": [[-float('inf'), float('inf')], [0.1, 1.01], [0.5, 1.02], [1.2, 0.99], [2.7, 1.03], [3.0, float('inf')]],
        "epsilon": 0.01
    }
]
test_cases22 = [
    # Test Case 1: Single piece, small ε, should require one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, float('inf')]],
        "epsilon": 0.1,
        "description": "Single piece with constant value, small ε"
    },
    # Test Case 2: Multiple pieces, large ε, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1.2], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "Multiple pieces within ε, should merge"
    },
    # Test Case 3: Values exactly at ε boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "Values at ε boundary, testing merge threshold"
    },
    # Test Case 4: Identical consecutive values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.5,
        "description": "Consecutive identical values, should merge"
    },
    # Test Case 5: Large x-coordinate gaps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [100, 1.5], [200, 1.2], [300, float('inf')]],
        "epsilon": 0.3,
        "description": "Large x gaps, testing piece separation"
    },
    # Test Case 6: Single interval
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Single interval, minimal pieces"
    },
    # Test Case 7: Negative values
    {
        "pc_fx": [[-float('inf'), float('inf')], [-2, -1], [0, -2], [2, -1.5], [4, float('inf')]],
        "epsilon": 0.6,
        "description": "Negative y values, testing L∞ norm"
    },
    # Test Case 8: Small ε, many pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 0.1,
        "description": "Small ε, should require multiple pieces"
    },
    # Test Case 9: Empty input (invalid case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, float('inf')]],
        "epsilon": 0.5,
        "description": "Empty input, testing error handling"
    },
    # Test Case 10: Example from user
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "description": "User-provided example, moderate ε"
    }
]
test_cases23 = [
    # Test Case 1: Basic case with small changes, ε allows some merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    },
    # Test Case 2: Identical y-values, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 3: Large y-value jumps, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, float('inf')]],
        "epsilon": 4.0
    },
    # Test Case 4: Very small ε, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, float('inf')]],
        "epsilon": 0.05
    },
    # Test Case 5: Large ε, should merge all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 10.0
    },
    # Test Case 6: Single piece, should return same piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 7: Negative y-values with small differences
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -1.5], [2, -2], [3, float('inf')]],
        "epsilon": 0.6
    },
    # Test Case 8: Overlapping or zero-width intervals
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, 3], [1, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 9: Very large y-values, testing numerical stability
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1e6], [1, 1e6 + 1], [2, 1e6 - 1], [3, float('inf')]],
        "epsilon": 2.0
    },
    # Test Case 10: Non-uniform x-intervals with varying y-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0.1, 0.5], [5, 1], [10, float('inf')]],
        "epsilon": 0.3
    }
]
test_cases24 = [
    # Test Case 1: Single piece, minimal input
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # Test Case 2: No merging possible, y-values differ by more than 2ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 4], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 3
    },
    # Test Case 3: All pieces mergeable, y-values within 2ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1.2], [3, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    # Test Case 4: Large jump in y-values, partial merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 5], [3, 5.5], [4, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 2
    },
    # Test Case 5: Small intervals, tight ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 1.1], [0.2, 1.2], [0.3, float('inf')]],
        "epsilon": 0.05,
        "expected_pieces": 3
    },
    # Test Case 6: Repeated y-values, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # Test Case 7: Negative y-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -1.5], [2, 0], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    # Test Case 8: Large intervals with large ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [100, 11], [200, 12], [300, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 1
    },
    # Test Case 9: Zero ε, no merging allowed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.001], [2, 1.002], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    # Test Case 10: Example from user input
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 3
    }
]
test_cases25 = [
    {
        "description": "Constant function, should return one piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 1.0
    },
    {
        "description": "Single piece with exact epsilon match",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, float('inf')]],
        "epsilon": 1.0
    },
    {
        "description": "Large jump exceeding epsilon, requires multiple pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 3], [2, float('inf')]],
        "epsilon": 1.0
    },
    {
        "description": "Multiple small jumps within epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1.2], [3, 1.8], [4, float('inf')]],
        "epsilon": 0.6
    },
    {
        "description": "Consecutive equal values, should merge",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.5
    },
    {
        "description": "Empty intervals (same x-coordinates), should handle gracefully",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, 3], [1, float('inf')]],
        "epsilon": 1.0
    },
    {
        "description": "Single-point interval, should handle minimal piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [0, float('inf')]],
        "epsilon": 1.0
    },
    {
        "description": "Negative values with small epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -1.2], [2, -1.5], [3, float('inf')]],
        "epsilon": 0.3
    },
    {
        "description": "Large epsilon allowing full merge",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 10], [3, float('inf')]],
        "epsilon": 10.0
    },
    {
        "description": "Boundary case with tight epsilon and multiple jumps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    }
]
test_cases26 = [
    # Test Case 1: Single piece, should remain one piece regardless of epsilon
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, math.inf]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # Test Case 2: Two pieces with y-difference ≤ ε, should merge into one piece
    {
        "pc_fx": [[-math.inf, math.inf], [0, 2], [1, 2.5], [2, math.inf]],
        "epsilon": 0.75,
        "expected_pieces": 1
    },
    # Test Case 3: Two pieces with y-difference > ε, should remain two pieces
    {
        "pc_fx": [[-math.inf, math.inf], [0, 2], [1, 4], [2, math.inf]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    # Test Case 4: Multiple pieces, some mergeable, from given example
    {
        "pc_fx": [[-math.inf, math.inf], [0, 2], [1, 3], [3, 7], [6, 5], [7, math.inf]],
        "epsilon": 0.75,
        "expected_pieces": 3  # Expected: [0,1) as 2, [1,3) as 3, [3,7) merges 7 and 5
    },
    # Test Case 5: Large epsilon, all pieces merge into one
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 5], [2, 10], [3, math.inf]],
        "epsilon": 10.0,
        "expected_pieces": 1
    },
    # Test Case 6: Zero epsilon, no merging possible
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 1.0001], [2, 1.0002], [3, math.inf]],
        "epsilon": 0.0,
        "expected_pieces": 3
    },
    # Test Case 7: Repeated y-values, should merge into one piece
    {
        "pc_fx": [[-math.inf, math.inf], [0, 3], [1, 3], [2, 3], [3, math.inf]],
        "epsilon": 0.1,
        "expected_pieces": 1
    },
    # Test Case 8: Non-integer y-values and epsilon, partial merging
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1.5], [1, 2.3], [2, 3.2], [3, math.inf]],
        "epsilon": 0.9,
        "expected_pieces": 2  # Expected: [0,2) as 1.5 or 2.3, [2,3) as 3.2
    },
    # Test Case 9: Negative y-values, testing merging with negative differences
    {
        "pc_fx": [[-math.inf, math.inf], [0, -1], [1, -2], [2, -1.5], [3, math.inf]],
        "epsilon": 0.75,
        "expected_pieces": 1  # Expected: All merge as |y_i - y_j| ≤ 1 ≤ 2*0.75
    },
    # Test Case 10: Many pieces with closely spaced x-values, testing precision
    {
        "pc_fx": [[-math.inf, math.inf], [0, 0], [0.1, 0.2], [0.2, 0.4], [0.3, 0.6], [0.4, math.inf]],
        "epsilon": 0.15,
        "expected_pieces": 2  # Expected: [0,0.3) merges 0,0.2,0.4; [0.3,0.4) as 0.6
    }
]
test_cases27 = [
    # Test Case 1: Single piece, should require only one piece
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, math.inf]],
        'epsilon': 0.5,
        'description': 'Single piece, should require one piece'
    },
    # Test Case 2: Multiple pieces with small differences within epsilon
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 1.2], [2, 1.4], [3, math.inf]],
        'epsilon': 0.3,
        'description': 'Values within epsilon, should merge to one piece'
    },
    # Test Case 3: Large jumps exceeding epsilon
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 3], [2, 1], [3, math.inf]],
        'epsilon': 0.5,
        'description': 'Large jumps, should require multiple pieces'
    },
    # Test Case 4: Zero epsilon, no merging possible
    {
        'pc_fx': [[-math.inf, math.inf], [0, 2], [1, 2.00001], [2, math.inf]],
        'epsilon': 0.0,
        'description': 'Zero epsilon, no merging, each piece separate'
    },
    # Test Case 5: Large epsilon, all pieces merge
    {
        'pc_fx': [[-math.inf, math.inf], [0, 0], [1, 5], [2, 10], [3, math.inf]],
        'epsilon': 10.0,
        'description': 'Large epsilon, all pieces should merge into one'
    },
    # Test Case 6: Negative values
    {
        'pc_fx': [[-math.inf, math.inf], [0, -1], [1, -1.5], [2, -2], [3, math.inf]],
        'epsilon': 0.6,
        'description': 'Negative values, some merging expected'
    },
    # Test Case 7: Very small intervals
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [0.0001, 1.1], [0.0002, 1.2], [1, math.inf]],
        'epsilon': 0.15,
        'description': 'Very small intervals, test merging in tight ranges'
    },
    # Test Case 8: Equal consecutive values
    {
        'pc_fx': [[-math.inf, math.inf], [0, 2], [1, 2], [2, 2], [3, math.inf]],
        'epsilon': 0.5,
        'description': 'Equal values, should merge into one piece'
    },
    # Test Case 9: Boundary case with epsilon exactly at difference
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 2], [2, math.inf]],
        'epsilon': 1.0,
        'description': 'Epsilon equals difference, test boundary merging'
    },
    # Test Case 10: Complex case with mixed intervals and values
    {
        'pc_fx': [[-math.inf, math.inf], [0, 2], [1, 3], [3, 7], [6, 5], [7, math.inf]],
        'epsilon': 0.75,
        'description': 'Complex case from example, mixed merging expected'
    }
]
test_cases28 = [
    # Test Case 1: Single piece, all values within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.2], [2, 0.9], [3, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 2: Two pieces, exact epsilon boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 3: Two pieces, just above epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 2.01], [2, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 4: Minimal input (single segment)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 5: Large jumps requiring multiple pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 5.0], [2, 0.0], [3, float('inf')]],
        "epsilon": 2.0
    },
    # Test Case 6: Dense points, values oscillating within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [0.1, 1.1], [0.2, 0.9], [0.3, 1.2], [0.4, float('inf')]],
        "epsilon": 0.3
    },
    # Test Case 7: Negative values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1.0], [1, -1.5], [2, -0.5], [3, float('inf')]],
        "epsilon": 0.75
    },
    # Test Case 8: Zero tolerance (no merging allowed)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.0], [2, 2.1], [3, float('inf')]],
        "epsilon": 0.0
    },
    # Test Case 9: Large tolerance (merge all pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 5.0], [3, float('inf')]],
        "epsilon": 100.0
    },
    # Test Case 10: Floating-point precision edge case
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0000001], [2, 1.0], [3, float('inf')]],
        "epsilon": 0.0000001
    }
]
test_cases29 = [
    # Test Case 1: Single piece, should require exactly one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece, should require one piece regardless of epsilon"
    },
    # Test Case 2: Two pieces with small difference, mergable within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, float('inf')]],
        "epsilon": 0.75,
        "description": "Two pieces with |y1 - y2| <= 2*epsilon, should merge into one piece"
    },
    # Test Case 3: Two pieces with difference just beyond epsilon, non-mergable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3.1], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces with |y1 - y2| > 2*epsilon, should require two pieces"
    },
    # Test Case 4: Multiple pieces, all values equal, should merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "Multiple pieces with equal values, should merge into one piece"
    },
    # Test Case 5: Large epsilon, all pieces mergable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 10], [3, float('inf')]],
        "epsilon": 10.0,
        "description": "Large epsilon allows all pieces to merge into one"
    },
    # Test Case 6: Small epsilon, no pieces mergable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.1,
        "description": "Small epsilon prevents any merging, should keep all pieces"
    },
    # Test Case 7: Empty intervals (zero-length pieces), should ignore
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [0, 3], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Zero-length intervals should be ignored, only one valid piece"
    },
    # Test Case 8: Large gaps in x-coordinates, should not affect merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [100, 2.5], [200, float('inf')]],
        "epsilon": 0.75,
        "description": "Large x-coordinate gaps, mergable due to |y1 - y2| <= 2*epsilon"
    },
    # Test Case 9: Negative y-values, testing sign handling
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -1.5], [2, float('inf')]],
        "epsilon": 0.3,
        "description": "Negative y-values, mergable within epsilon"
    },
    # Test Case 10: Boundary case with epsilon = 0, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.0001], [2, float('inf')]],
        "epsilon": 0.0,
        "description": "Zero epsilon, no merging possible, even for tiny differences"
    }
]
test_cases30 = [
    # Test Case 1: Constant function, should require only one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Constant function with y=5 across all x, should need one piece"
    },
    # Test Case 2: Single piece with small epsilon, should need one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.1,
        "description": "Single piece from x=0 to x=1 with y=1, small epsilon"
    },
    # Test Case 3: Zero epsilon, should require all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 4], [3, float('inf')]],
        "epsilon": 0.0,
        "description": "Zero epsilon, should preserve all pieces"
    },
    # Test Case 4: Large epsilon, should merge all pieces into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, float('inf')]],
        "epsilon": 5.0,
        "description": "Large epsilon, should merge all pieces into one"
    },
    # Test Case 5: Consecutive pieces with values within epsilon, should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.2], [3, float('inf')]],
        "epsilon": 0.75,
        "description": "Consecutive pieces with |y_i - y_{i+1}| <= epsilon, should merge"
    },
    # Test Case 6: Large jumps just beyond epsilon, should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2.01], [2, 1], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "Jumps slightly larger than epsilon, should keep separate pieces"
    },
    # Test Case 7: Empty intervals (consecutive identical x), should handle gracefully
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, 3], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Empty intervals (same x values), should handle degenerate case"
    },
    # Test Case 8: Single point (degenerate interval), should handle as single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, float('inf')]],
        "epsilon": 0.5,
        "description": "Degenerate interval (single point), should treat as single piece"
    },
    # Test Case 9: Large number of pieces with alternating values, tests merging limits
    {
        "pc_fx": [[-float('inf'), float('inf')] ] + [[i, 1 if i % 2 == 0 else 2] for i in range(10)] + [[10, float('inf')]],
        "epsilon": 0.5,
        "description": "Alternating values (1,2,1,2,...), should keep pieces due to |y_i - y_{i+1}| > epsilon"
    },
    # Test Case 10: Closely spaced points with values just within epsilon, tests precision
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 1.4], [0.2, 1.2], [0.3, float('inf')]],
        "epsilon": 0.5,
        "description": "Closely spaced points with values within epsilon, should merge"
    }
]