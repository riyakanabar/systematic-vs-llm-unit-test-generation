#16 Sept 5:47 PM
#Iteration1
test_cases1 = [
    {
        "name": "1. Simple Monotone Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 4
    },
    {
        "name": "2. Zero Tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    {
        "name": "3. All-Merging Tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, 5], [4, float('inf')]],
        "epsilon": 2.5,
        "expected_pieces": 1
    },
    {
        "name": "4. Non-Mergeable Segments",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 3
    },
    {
        "name": "5. Step Function with a Plateau",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "name": "6. Small Oscillations",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.1], [1, 1.2], [2, 1.0], [3, 1.3], [4, 1.2], [5, float('inf')]],
        "epsilon": 0.2,
        "expected_pieces": 1
    },
    {
        "name": "7. Repeated Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 10], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "name": "8. Negative Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -5], [2, -1], [3, -5], [4, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 4
    },
    {
        "name": "9. Boundary Effects",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 0], [3, 0], [4, 10], [5, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 3
    },
    {
        "name": "10. Complex Merging Pattern",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 4], [3, 1], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 3
    }
]
#Iteration2
test_cases2 = [
    {
        'description': 'Test Case 1: Simple Monotonic Increase - No Merging',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 4,
        'reasoning': 'The absolute difference between adjacent pieces is 1, which is > 2 * epsilon (0.5). No pieces can be merged.'
    },
    {
        'description': 'Test Case 2: All Pieces Merged',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 1.4], [3, 1.6], [4, float('inf')]],
        'epsilon': 0.4,
        'expected_pieces': 1,
        'reasoning': 'The total range of values is [1, 1.6]. The L-infinity error for a single constant piece (e.g., 1.3) is 0.3, which is <= epsilon. All pieces can be merged.'
    },
    {
        'description': 'Test Case 3: Alternating Values - No Merging',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, float('inf')]],
        'epsilon': 0.9,
        'expected_pieces': 4,
        'reasoning': 'The difference between adjacent piece values is 2, which is > 2 * epsilon. No pieces can be merged.'
    },
    {
        'description': 'Test Case 4: Partial Merging',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2.8], [2, 3], [3, 1.2], [4, float('inf')]],
        'epsilon': 0.9,
        'expected_pieces': 3,
        'reasoning': 'Only the middle two pieces [1, 2.8) and [2, 3) can be merged, as their value range is [2.8, 3] and the error (0.1) is <= epsilon.'
    },
    {
        'description': 'Test Case 5: Merging Distinct Blocks',
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 1], [3, 1], [4, float('inf')]],
        'epsilon': 2.0,
        'expected_pieces': 2,
        'reasoning': 'The first two and last two pieces have zero difference, so they can be merged. The middle jump from 10 to 1 is too large to merge the resulting blocks.'
    },
    {
        'description': 'Test Case 6: Narrow Pieces with Large Differences - No Merging',
        'pc_fx': [[-float('inf'), float('inf')], [0, 100], [0.1, 10], [0.2, 100], [0.3, 10], [0.4, float('inf')]],
        'epsilon': 5.0,
        'expected_pieces': 4,
        'reasoning': 'The value difference between all adjacent pieces is 90, which is >> 2 * epsilon, so no merging is possible.'
    },
    {
        'description': 'Test Case 7: Wide Pieces with Small Differences - All Merged',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [100, 1.5], [200, 2], [300, 2.5], [400, float('inf')]],
        'epsilon': 0.8,
        'expected_pieces': 1,
        'reasoning': 'The entire range of values is [1, 2.5], and the max error of 0.75 from a constant value is <= epsilon.'
    },
    {
        'description': 'Test Case 8: Zero Epsilon - Only Exact Matches Merged',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 2], [3, 2], [4, float('inf')]],
        'epsilon': 0.0,
        'expected_pieces': 2,
        'reasoning': 'With epsilon=0, only pieces with identical values can be merged. The jump from 1 to 2 is not allowed.'
    },
    {
        'description': 'Test Case 9: Negative Values - Partial Merging',
        'pc_fx': [[-float('inf'), float('inf')], [0, -1], [1, -1.5], [2, -2], [3, -1.5], [4, float('inf')]],
        'epsilon': 0.4,
        'expected_pieces': 2,
        'reasoning': 'The pieces from [1, -1.5) to [3, -1.5) have a value range of [-2, -1.5], with a max error of 0.25 from a constant value of -1.75, which is <= epsilon. The first piece cannot be merged.'
    },
    {
        'description': 'Test Case 10: Single Piece Input',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [10, float('inf')]],
        'epsilon': 100.0,
        'expected_pieces': 1,
        'reasoning': 'The input is already a single piece, so no changes should be made.'
    }
]
#Iteration3
test_cases3 = [
    # Test Case 1: Basic Monotonic Increasing Function
    # The algorithm should not merge any pieces as the difference is > epsilon.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 4
    },

    # Test Case 2: Basic Monotonic Decreasing Function
    # Similar to above, no merges should occur.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 4], [2, 3], [3, 2], [4, float('inf')]],
        'epsilon': 0.9,
        'expected_pieces': 4
    },

    # Test Case 3: All Pieces within Tolerance
    # All pieces should be merged into a single one.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 1.1], [3, 0.9], [4, float('inf')]],
        'epsilon': 0.3,
        'expected_pieces': 1
    },

    # Test Case 4: Edge Case: Merging is Exactly at the Boundary epsilon
    # The algorithm should handle the inclusive boundary condition.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 1
    },

    # Test Case 5: Stair-Step Function
    # An alternating pattern that can be fully merged.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, 1], [5, float('inf')]],
        'epsilon': 2.0,
        'expected_pieces': 1
    },

    # Test Case 6: Multiple Plateaus (Constant Sections)
    # Merges should occur within plateaus but not between them.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 10], [3, 20], [4, 20], [5, 20],
                  [6, float('inf')]],
        'epsilon': 0.1,
        'expected_pieces': 2
    },

    # Test Case 7: Large Number of Pieces, Small epsilon
    # Challenges performance and correct grouping on a larger dataset.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1], [3, 1.5], [4, 2], [5, 2.5], [6, 3], [7, 3.5],
                  [8, 4], [9, 4.5], [10, float('inf')]],
        'epsilon': 0.4,
        'expected_pieces': 5
    },

    # Test Case 8: Alternating Values that Can be Merged
    # Similar to the stair-step but with smaller differences.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 4.9], [3, 5.2], [4, float('inf')]],
        'epsilon': 0.3,
        'expected_pieces': 1
    },

    # Test Case 9: Piece Values Differing by a Small Amount
    # Tests precision and non-trivial merges.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.01], [2, 1.02], [3, 1.03], [4, float('inf')]],
        'epsilon': 0.01,
        'expected_pieces': 2
    },

    # Test Case 10: Trivial Input
    # Checks for correct handling of a single piece.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [float('inf'), float('inf')]],
        'epsilon': 10.0,
        'expected_pieces': 1
    }
]
#Iteration4
test_cases4 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, float('inf')]],
        "epsilon": 0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, float('inf')]],
        "epsilon": 2
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1], [3, 1.5], [4, float('inf')]],
        "epsilon": 0.75
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 0.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 100
    },
    {
        "pc_fx": [[-float('inf'), float('inf')]] + [[i, i % 2] for i in range(1, 101)] + [[101, float('inf')]],
        "epsilon": 0.25
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 2], [4, 0], [5, float('inf')]],
        "epsilon": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, 0], [2, 1], [3, float('inf')]],
        "epsilon": 1
    }
]
#Iteration5
test_cases5 = [
    {
        "description": "Uniformly Spaced, Identical Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Simple Step Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 4
    },
    {
        "description": "Tolerance Greater Than All Value Differences",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 11], [2, 12], [3, 11], [4, float('inf')]],
        "epsilon": 5.0,
        "expected_pieces": 1
    },
    {
        "description": "Tolerance Exactly Equal to a Difference",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 6], [2, 7], [3, 8], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Alternating, Symmetrical Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 11], [2, 10], [3, 11], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 4
    },
    {
        "description": "Alternating, Mergable Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 11], [2, 10], [3, 11], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Single Piece, Zero Epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 6], [2, 7], [3, 8], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 4
    },
    {
        "description": "Large Number of Pieces, Small Changes",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.1], [2, 10.2], [3, 10.3], [4, 10.4], [5, 10.5], [6, float('inf')]],
        "epsilon": 0.2,
        "expected_pieces": 3
    },
    {
        "description": "Decreasing Function, Constant Slope",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 9], [2, 8], [3, 7], [4, float('inf')]],
        "epsilon": 1.5,
        "expected_pieces": 2
    },
    {
        "description": "A U-Shaped Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 4
    }
]
#Iteration6
test_cases6 = [
    {
        "description": "Single piece function. Should return one piece, the original.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0
    },
    {
        "description": "Two disjoint pieces, separated. No merging possible.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 6], [10, float('inf')]],
        "epsilon": 1.0
    },
    {
        "description": "Merge two pieces. Their values are within epsilon.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.5], [5, 3.0], [10, float('inf')]],
        "epsilon": 0.6
    },
    {
        "description": "Merge three pieces. All three are within epsilon.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.5], [3, 2.8], [6, 2.6], [9, float('inf')]],
        "epsilon": 0.4
    },
    {
        "description": "Zero tolerance. No merging should occur.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [3, 5], [6, 2], [9, float('inf')]],
        "epsilon": 0.0
    },
    {
        "description": "Large tolerance. Should merge all pieces into one.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [3, 5], [6, 2], [9, float('inf')]],
        "epsilon": 2.0
    },
    {
        "description": "Oscillating data. Merging should be difficult.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, 5], [4, float('inf')]],
        "epsilon": 1.5
    },
    {
        "description": "Step function. Jumps are larger than epsilon, preventing merging.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 3], [4, 5], [6, float('inf')]],
        "epsilon": 0.5
    },
    {
        "description": "Multiple consecutive merges. A series of merges possible.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.5], [2, 10.2], [3, 10.6], [4, float('inf')]],
        "epsilon": 0.8
    },
    {
        "description": "Mixed merging and non-merging. Some pieces merge, some don't.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 5], [3, 5.2], [4, 2], [5, 2.4], [6, float('inf')]],
        "epsilon": 0.6
    }
]
#Iteration7
test_cases7 = [
    # 1. Simple Monotonic Function
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Tests a simple monotonic function. Each piece should remain separate as the value change (1) is greater than epsilon (0.5).',
        'expected_pieces': 4
    },
    # 2. Zero Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        'epsilon': 0.0,
        'description': 'Tests for zero tolerance. No approximation is allowed, so the number of pieces should be the same as the input.',
        'expected_pieces': 3
    },
    # 3. Perfectly Constant Function
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [6, 5], [8, float('inf')]],
        'epsilon': 1.0,
        'description': 'Tests if a constant function can be reduced to a single piece.',
        'expected_pieces': 1
    },
    # 4. Large Jumps, Small Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Small tolerance with large jumps. Should result in many pieces.',
        'expected_pieces': 4
    },
    # 5. Large Jumps, Large Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        'epsilon': 6.0,
        'description': 'Large tolerance, should be able to approximate the entire function with a single piece.',
        'expected_pieces': 1
    },
    # 6. "Near Miss" Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, float('inf')]],
        'epsilon': 0.5,
        'description': 'A critical case for optimality. The segments [0,1) and [1,2) can be merged with deviation 0.5.',
        'expected_pieces': 2
    },
    # 7. Tolerance Aligned with Step Values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'Tests if the algorithm correctly handles a tolerance exactly equal to the maximum deviation, allowing for maximum merging.',
        'expected_pieces': 1
    },
    # 8. Alternating Values with Varying Widths
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [3, 0], [4, 10], [6, 0], [7, float('inf')]],
        'epsilon': 6.0,
        'description': 'Tests if a non-greedy approach can find the optimal solution by merging non-adjacent values.',
        'expected_pieces': 1
    },
    # 9. Negative Values and Mixed Signs
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, -5], [2, 5], [3, -5], [4, float('inf')]],
        'epsilon': 5.0,
        'description': 'Ensures the algorithm correctly handles negative values and mixed signs.',
        'expected_pieces': 1
    },
    # 10. Asymmetric Jumps and Complex Merging
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 5], [3, 0], [4, float('inf')]],
        'epsilon': 2.5,
        'description': 'A complex case to expose non-greedy algorithm failures. The optimal solution is not obvious and requires careful merging decisions.',
        'expected_pieces': 3
    }
]
#Iteration8
test_cases8 = [
    {
        "description": "Uniform Function: A single piece should approximate the entire function.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    {
        "description": "Step Function with Large Gaps: Large jumps require a new piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2], [5, 8], [10, 8], [10, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "description": "Step Function with Small Gaps: Small jumps can be merged.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2.4], [5, 2.6], [10, 2.6], [10, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 1
    },
    {
        "description": "Monotonically Increasing Function: Multiple pieces required to stay within tolerance.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 2], [4, 3], [6, 4], [8, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 4
    },
    {
        "description": "Monotonically Decreasing Function: Multiple pieces required to stay within tolerance.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 4], [4, 3], [6, 2], [8, 1], [10, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 4
    },
    {
        "description": "Oscillating Function within Tolerance: Oscillation within tolerance can be merged into one piece.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, 4.5], [3, 5.2], [4, 4.8], [5, 5], [5, float('inf')]],
        "epsilon": 0.6,
        "expected_pieces": 1
    },
    {
        "description": "Oscillating Function Exceeding Tolerance: Oscillation exceeds tolerance, requiring multiple pieces.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 6], [2, 4], [3, 6], [4, 4], [5, 5], [5, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 4
    },
    {
        "description": "Single Point Function: A single piece with two points should be approximated by itself.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [5, 10], [5, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 1
    },
    {
        "description": "Function with a 'Peak' or 'Spike': A sharp change cannot be merged.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [2, 10], [3, 5], [5, 5], [5, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 3
    },
    {
        "description": "Long Flat Segment Followed by Monotonic Change: Combines flat and monotonic regions.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2], [5, 3], [6, 4], [7, 5], [8, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 3
    }
]
#Iteration9
test_cases9 = [
    # 1. Basic Case with Clear Solution
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        'epsilon': 0.75,
        'description': 'A standard case with clear jumps, requiring multiple pieces.'
    },
    # 2. Zero Epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 2], [3, 4], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Tests the extreme case where no approximation is allowed. Should return the original number of pieces.'
    },
    # 3. Large Epsilon (Single Piece Solution)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 1], [2, 5], [3, 12], [4, float('inf')]],
        'epsilon': 100.0,
        'description': 'When epsilon is very large, the entire function should be approximable by a single piece.'
    },
    # 4. Step Function with All Pieces Mergable
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        'epsilon': 0.1,
        'description': 'A step function where all pieces have the same value. The algorithm should merge all pieces into one.'
    },
    # 5. Piecewise Linear-like Function
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Values are linearly increasing. Tests if the algorithm can find the minimum number of pieces for this gradual change.'
    },
    # 6. Small Oscillations within Epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.1], [1, 0.9], [2, 1.2], [3, 0.8], [4, float('inf')]],
        'epsilon': 0.2,
        'description': 'All values are within the tolerance range of a single piece. Should result in one piece.'
    },
    # 7. Tightly Bounded Jumps
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2.0], [2, 1], [3, 2.0], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Value jumps by exactly 2*epsilon. Tests boundary conditions for merging pieces.'
    },
    # 8. Single Interior Piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 1], [3, 5], [4, 5], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'A single piece with a different value that is close enough to be approximated with surrounding pieces.'
    },
    # 9. Alternating Values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 0], [2, 1], [3, 0], [4, 1], [5, float('inf')]],
        'epsilon': 0.4,
        'description': 'Alternating values. The algorithm must pair adjacent pieces to find the optimal solution.'
    },
    # 10. Long Plateau with a Single Jump
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 1], [4, 5], [5, 5], [6, 5], [7, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two long plateaus separated by a jump. The algorithm should merge within each plateau but not across the jump.'
    }
]
#Iteration10
test_cases10 = [
    # 1. Single piece function.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 2.0,
        'description': "Already a single constant piece",
        'expected_pieces': 1
    },

    # 2. Zero tolerance.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        'epsilon': 0.0,
        'description': "No approximation allowed",
        'expected_pieces': 4
    },

    # 3. Large tolerance.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        'epsilon': 5.0,
        'description': "Large epsilon reduces to a single piece",
        'expected_pieces': 1
    },

    # 4. Oscillating function.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, 10], [5, float('inf')]],
        'epsilon': 4.0,
        'description': "Alternating high and low values",
        'expected_pieces': 3
    },

    # 5. Gradually increasing function.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        'epsilon': 0.5,
        'description': "Gradual changes requiring new pieces",
        'expected_pieces': 5
    },

    # 6. All-or-nothing case.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, 1], [5, float('inf')]],
        'epsilon': 0.6,
        'description': "One piece can be absorbed if within range",
        'expected_pieces': 3
    },

    # 7. Function with zero-width intervals (simulated).
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, 3], [2, float('inf')]],
        'epsilon': 1.0,
        'description': "Simulated zero-width interval",
        'expected_pieces': 2
    },

    # 8. Sparse function with large jumps.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [10, 2], [20, 15], [30, 1], [40, float('inf')]],
        'epsilon': 3.0,
        'description': "Large value differences between pieces",
        'expected_pieces': 4
    },

    # 9. Staircase function.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, 2.5], [4, 100], [5, float('inf')]],
        'epsilon': 0.4,
        'description': "Each step just above the threshold",
        'expected_pieces': 5
    },

    # 10. Repeated values.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 8], [4, 8], [5, float('inf')]],
        'epsilon': 0.01,
        'description': "Series of repeating values can be merged",
        'expected_pieces': 2
    }
]
#Iteration11
test_cases11 = [
    {
        "name": "1. Basic Function with Uniform Jumps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "2. A Single Large Jump",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "name": "3. Jumps Exceeding and Equaling the Tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2.5], [2, 3], [3, 4.5], [4, float('inf')]],
        "epsilon": 1.5,
        "expected_pieces": 2
    },
    {
        "name": "4. Narrow Pieces with Small Jumps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0.1, 0.1], [0.2, 0.05], [0.3, float('inf')]],
        "epsilon": 0.15,
        "expected_pieces": 1
    },
    {
        "name": "5. Zig-Zagging Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0.5], [3, 1.5], [4, float('inf')]],
        "epsilon": 1,
        "expected_pieces": 2
    },
    {
        "name": "6. Large Gaps in X-Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [100, 10.5], [101, 10], [200, float('inf')]],
        "epsilon": 0.6,
        "expected_pieces": 1
    },
    {
        "name": "7. Function with Values Far from Zero",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1000], [1, 1000.5], [2, 1001], [3, 1000.8], [4, float('inf')]],
        "epsilon": 0.8,
        "expected_pieces": 2
    },
    {
        "name": "8. All Jumps Exactly at Tolerance Limit",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 1,
        "expected_pieces": 2
    },
    {
        "name": "9. A Single Piece with Varying Widths",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.2], [5, 5.3], [6, float('inf')]],
        "epsilon": 0.3,
        "expected_pieces": 1
    },
    {
        "name": "10. Empty or Trivial Input",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 1,
        "expected_pieces": 1
    }
]
#Iteration12
test_cases12 = [
    {
        "name": "1. Constant Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 1.0,
        "description": "Tests if the algorithm correctly identifies a single-piece constant function and returns the optimal single piece.",
    },
    {
        "name": "2. Small ε for a Staircase Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.1,
        "description": "Tests for a small tolerance on a staircase function with large jumps. Expects a large number of pieces.",
    },
    {
        "name": "3. Large ε for a Staircase Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 5.0,
        "description": "Tests if the algorithm correctly merges many pieces into one when the tolerance is large. Expects a single piece.",
    },
    {
        "name": "4. 'V' Shape Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 3], [2, 1], [3, 3], [4, 5], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Tests the algorithm's ability to handle functions that decrease and then increase.",
    },
    {
        "name": "5. Spiky Function (Alternating High and Low Values)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 1], [2, 10], [3, 1], [4, 10], [5, float('inf')]],
        "epsilon": 2.0,
        "description": "Tests the algorithm on a function with rapid, alternating changes. Should approximate each peak and valley.",
    },
    {
        "name": "6. Single Piece That Can Be Approximated by a Different Value",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Tests if the algorithm can approximate a single piece with a different value if it's within tolerance.",
    },
    {
        "name": "7. Long Constant Section Followed by a Jump",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 1], [4, 5], [5, float('inf')]],
        "epsilon": 0.2,
        "description": "Tests if a long constant section is correctly approximated by one piece before a sudden jump requires a new one.",
    },
    {
        "name": "8. Negative Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, -5], [1, -2], [2, -8], [3, -5], [4, float('inf')]],
        "epsilon": 1.0,
        "description": "Tests if the algorithm correctly handles negative function values.",
    },
    {
        "name": "9. Large Number of Pieces",
        "pc_fx": [[-float('inf'), float('inf')]] + [[i, i % 5] for i in range(100)] + [[100, float('inf')]],
        "epsilon": 0.5,
        "description": "Tests the algorithm's performance and optimality on a large dataset.",
    },
    {
        "name": "10. Zero-Width Pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, 3], [2, float('inf')]],
        "epsilon": 0.5,
        "description": "Tests the algorithm's robustness to zero-width intervals, which it should handle gracefully, likely by ignoring them.",
    },
]
#Iteration13
test_cases13 = [
    # 1. Simple Case: All Points Approximated by a Single Piece 🎯
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 4.9], [3, float('inf')]],
        'epsilon': 0.15,
        'expected_output': 1
    },
    # 2. Staircase Function 📈
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 3
    },
    # 3. V-Shaped Function ⛰️
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 8], [2, 6], [3, 8], [4, 10], [5, float('inf')]],
        'epsilon': 2.0,
        'expected_output': 2
    },
    # 4. Zero-Tolerance Case 📏
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 6], [3, 6], [4, 5], [5, float('inf')]],
        'epsilon': 0.0,
        'expected_output': 3
    },
    # 5. Large Tolerance: Single Piece Approximation ☁️
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 100], [1, 1], [2, 10], [3, 50], [4, float('inf')]],
        'epsilon': 100.0,
        'expected_output': 1
    },
    # 6. Small Tolerance: No Approximation 🤏
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.001], [2, 1.002], [3, float('inf')]],
        'epsilon': 0.0001,
        'expected_output': 3
    },
    # 7. Repeated Values 🔄
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 6], [4, 6], [5, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 2
    },
    # 8. Mixed Tolerance Scenarios ⚖️
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 3], [3, 10], [4, 10.2], [5, 10.4], [6, float('inf')]],
        'epsilon': 1.0,
        'expected_output': 2
    },
    # 9. Boundary Case: First and Last Pieces 🚧
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.5], [1, 1], [2, 0.5], [3, 1], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 2
    },
    # 10. W-Shaped Function 🌊
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 1], [2, 5], [3, 1], [4, 5], [5, float('inf')]],
        'epsilon': 2.0,
        'expected_output': 3
    }
]
#Iteration14
test_cases14 = [
    {
        "description": "Uniformly Spaced, Small Epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.1,
        "expected_result": 4
    },
    {
        "description": "Uniformly Spaced, Large Epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 2.0,
        "expected_result": 1
    },
    {
        "description": "Zig-Zag Pattern",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, 10], [5, 0], [6, float('inf')]],
        "epsilon": 4.0,
        "expected_result": 3
    },
    {
        "description": "Constant Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_result": 1
    },
    {
        "description": "Single Piece Input",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [5, float('inf')]],
        "epsilon": 0.5,
        "expected_result": 1
    },
    {
        "description": "Edge Case: Epsilon is a perfect 'fit'",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_result": 3
    },
    {
        "description": "Negative Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, -5], [1, -4], [2, -6], [3, -5], [4, float('inf')]],
        "epsilon": 0.75,
        "expected_result": 3
    },
    {
        "description": "Varying Piece Lengths",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 1], [5, 12], [6, 2], [10, float('inf')]],
        "epsilon": 4.0,
        "expected_result": 3
    },
    {
        "description": "Sharp Spike",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 15], [3, 5], [4, 5], [5, float('inf')]],
        "epsilon": 2.0,
        "expected_result": 3
    },
    {
        "description": "Complex Pattern with Optimal Merge Points",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 12], [2, 10], [3, 5], [4, 7], [5, 5], [6, 1], [7, 3], [8, float('inf')]],
        "epsilon": 1.5,
        "expected_result": 4
    }
]
#Iteration15
test_cases15 = [
    {
        "name": "Uniformly Spaced, Monotonic Step Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 2], [4, 2], [5, 3], [6, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 3,
        "notes": "Tests basic merging of consecutive, identical-valued pieces."
    },
    {
        "name": "Identical Function and Approximation",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [2, 12], [4, 10], [6, 12], [8, float('inf')]],
        "epsilon": 3.0,
        "expected_pieces": 1,
        "notes": "Tolerance is large enough to merge the entire function into a single piece."
    },
    {
        "name": "Large Epsilon, Single Piece Approximation",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 12], [2, 15], [3, 11], [4, 8], [5, float('inf')]],
        "epsilon": 5.0,
        "expected_pieces": 1,
        "notes": "With a large epsilon, the algorithm should return a single piece for the whole interval."
    },
    {
        "name": "Zero Epsilon, No Merging",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 4,
        "notes": "Zero tolerance means no merging is possible, so the original pieces are returned."
    },
    {
        "name": "Small Epsilon, Minimal Merging",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.05], [2, 2], [3, 2.05], [4, 3], [5, 3.05], [6, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 3,
        "notes": "Small tolerance allows merging of very similar adjacent pieces only."
    },
    {
        "name": "Alternating High and Low Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 4.0,
        "expected_pieces": 5,
        "notes": "Large, frequent jumps in value prevent any merging."
    },
    {
        "name": "Symmetry around a Single Point",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, float('inf')]],
        "epsilon": 5.0,
        "expected_pieces": 1,
        "notes": "The function is symmetric, allowing for a single-piece approximation."
    },
    {
        "name": "Single Piece Input",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "notes": "Base case: The input is already a single piece and should not be modified."
    },
    {
        "name": "Steep Slopes (Large Jumps)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, 0], [3, 100], [4, float('inf')]],
        "epsilon": 10.0,
        "expected_pieces": 4,
        "notes": "Very large value changes test if the algorithm correctly identifies that no merging is possible."
    },
    {
        "name": "Example from the Prompt",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 4,
        "notes": "The provided example is re-tested to ensure consistency and correctness."
    }
]
#Iteration16
test_cases16 = [
    {
        "name": "1. Linear Function with Simple Approximation",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 4], [3, 5], [4, float('inf')]],
        "epsilon": 1.5,
        "expected_pieces": 1,
        "notes": "A linear sequence of values (2, 3, 4, 5) can be approximated by a single piece with a value of 3.5. The max deviation from 2 and 5 is 1.5."
    },
    {
        "name": "2. Approximation with No Combination Possible",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 20], [2, 30], [3, 40], [4, float('inf')]],
        "epsilon": 5.0,
        "expected_pieces": 4,
        "notes": "Values are spaced too far apart. The difference between any two adjacent values is 10, which is greater than the epsilon of 5.0."
    },
    {
        "name": "3. Zig-Zag Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 2], [3, 6], [4, 3], [5, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 3,
        "notes": "The function's non-monotonic behavior requires careful grouping. For an epsilon of 2.0, pieces (1, 5) can be combined (e.g., approximated by 3), and (2, 6) can be combined (e.g., approximated by 4). The last piece must stand alone."
    },
    {
        "name": "4. Approximation of a Step Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 2,
        "notes": "Adjacent pieces with the same value can always be combined, even with zero tolerance. This tests for correct handling of discrete jumps."
    },
    {
        "name": "5. Small Epsilon Close to an Edge Case",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 2.5], [2, 1.5], [3, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 3,
        "notes": "The difference between 1.0 and 2.5 is 1.5, and between 2.5 and 1.5 is 1.0. An epsilon of 0.75 is too small to combine these pieces, forcing the algorithm to retain all of them."
    },
    {
        "name": "6. Zero Epsilon Tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 20], [3, 30], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 3,
        "notes": "With epsilon=0, the approximation must be exact. Only adjacent pieces with identical values can be merged. Thus, the first two pieces merge, but the others must be kept separate."
    },
    {
        "name": "7. Floating Point Numbers with Small Differences",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.01], [1, 1.05], [2, 1.02], [3, 1.04], [4, float('inf')]],
        "epsilon": 0.05,
        "expected_pieces": 1,
        "notes": "All values are within the range [1.01, 1.05]. The maximum deviation from the mean (1.03) is 0.02, which is less than the epsilon of 0.05. This confirms correct handling of floating-point values."
    },
    {
        "name": "8. Large Values with Small Relative Differences",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1000], [1, 1001], [2, 1002], [3, 1003], [4, float('inf')]],
        "epsilon": 1.5,
        "expected_pieces": 1,
        "notes": "The range of values is [1000, 1003]. The maximum deviation from the mean (1001.5) is 1.5, which is exactly the epsilon. This tests for an inclusive tolerance."
    },
    {
        "name": "9. A Long Sequence with a Mix of Combinable and Non-Combinable Sections",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 11], [2, 15], [3, 16], [4, 20], [5, 21], [6, float('inf')]],
        "epsilon": 1.2,
        "expected_pieces": 3,
        "notes": "This long sequence requires the algorithm to find optimal combinations. The values (10, 11) can be grouped, as can (15, 16) and (20, 21). The jumps between these groups (e.g., 11 to 15) are too large for the given epsilon."
    },
    {
        "name": "10. Constant Function Approximation",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 100.0,
        "expected_pieces": 1,
        "notes": "A sanity check for a function that is already a single constant piece. The algorithm should combine all pieces into one, regardless of the large epsilon value."
    }
]
#Iteration17
test_cases17 = [
    # Test Case 1: Simple Monotonic Increase
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_outcome': 4  # Cannot combine any pieces because the max error would be >= 0.5.
    },

    # Test Case 2: Constant Sections
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 2], [4, 2], [5, 1], [6, float('inf')]],
        'epsilon': 0.1,
        'expected_outcome': 3  # Combines [0, 3) with value 5, [3, 5) with value 2, and [5, 6) with value 1.
    },

    # Test Case 3: Sharp Jump
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 11], [3, 1], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_outcome': 4  # Jumps are too large to be approximated. All pieces must remain separate.
    },

    # Test Case 4: Zero Tolerance (epsilon=0)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 2], [3, 2], [4, float('inf')]],
        'epsilon': 0.0,
        'expected_outcome': 2  # Only merges pieces that are already equal.
    },

    # Test Case 5: Large Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        'epsilon': 2.0,
        'expected_outcome': 1  # The entire function can be approximated by a single constant value (e.g., 3).
    },

    # Test Case 6: Alternating Values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        'epsilon': 0.4,
        'expected_outcome': 4
        # The error between any two consecutive pieces is at least 0.5. So no two pieces can be combined.
    },

    # Test Case 7: Non-integer Values and Tolerance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.25], [1, 1.5], [2, 2.75], [3, 3.0], [4, float('inf')]],
        'epsilon': 0.25,
        'expected_outcome': 2  # Can combine [0, 2) with value 1.375 and [2, 4) with value 2.875.
    },

    # Test Case 8: Only Two Pieces
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, float('inf')]],
        'epsilon': 1.0,
        'expected_outcome': 2  # Error is 2 > 1, so the pieces cannot be combined.
    },

    # Test Case 9: All Pieces Can Be Combined
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 1.5,
        'expected_outcome': 1  # The entire function can be approximated by a single constant value (e.g., 2.5).
    },

    # Test Case 10: Empty Piece List
    {
        'pc_fx': [[-float('inf'), float('inf')]],
        'epsilon': 1.0,
        'expected_outcome': 0  # Should return 0 pieces for an empty function.
    }
]
#Iteration18
test_cases18 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "expected_output": 1,
        "reasoning": "A single constant segment requires only one piece, regardless of the tolerance."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 10], [10, float('inf')]],
        "epsilon": 2.0,
        "expected_output": 2,
        "reasoning": "The jump from y=1 to y=10 is an error of 9.0, which exceeds the tolerance of 2.0, so at least two pieces are required."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 2], [4, 3], [6, float('inf')]],
        "epsilon": 0.5,
        "expected_output": 3,
        "reasoning": "This is a step function. Each constant segment requires its own piece since a single piece covering multiple segments would have an error larger than the tolerance."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 2], [10, float('inf')]],
        "epsilon": 1.0,
        "expected_output": 1,
        "reasoning": "The total variation of the function is from y=1 to y=2. The optimal constant approximation is 1.5, with an L-infinity error of 0.5. Since 0.5 <= 1.0, a single piece is sufficient."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 2], [10, float('inf')]],
        "epsilon": 0.25,
        "expected_output": 2,
        "reasoning": "The total variation is from y=1 to y=2, with an optimal single-piece error of 0.5. Since 0.5 > 0.25, more than one piece is needed."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.0,
        "expected_output": 4,
        "reasoning": "A zero tolerance means no approximation is allowed. The algorithm must return the original number of piecewise constant segments."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [5, 1], [10, 8], [15, 3], [20, float('inf')]],
        "epsilon": 5.0,
        "expected_output": 1,
        "reasoning": "The total range of y values is from 1 to 10. The optimal constant approximation is 5.5, with a max error of 4.5. Since 4.5 <= 5.0, one piece is sufficient."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 1], [4, 0], [6, 1], [8, 0], [10, float('inf')]],
        "epsilon": 0.25,
        "expected_output": 3,
        "reasoning": "The function oscillates between y=0 and y=1. An approximation over a segment of this function would have a max error of 0.5, which is greater than 0.25. The function must be split at least once every time it crosses its midpoint (y=0.5)."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1], [6, 10], [10, 10], [11, float('inf')]],
        "epsilon": 1.0,
        "expected_output": 2,
        "reasoning": "The first segment is flat and can be a single piece. The jump from y=1 to y=10 is larger than the tolerance, requiring a new piece. The second flat segment can also be a single piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "expected_output": 3,
        "reasoning": "The first two segments ([0, 1) and [1, 3)) can be merged as the range of y values is [2, 3], with an L-infinity error of 0.5, which is less than 0.75. The subsequent values of 7 and 5 cannot be included in a single piece with the previous values. The pieces must be split at x=3 and x=6."
    }
]
#Iteration19
test_cases19 = [
    {
        "description": "Simple Monotonic Increase",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_outcome": "The approximation should require more than one piece. For example, approximating [0,4) with a single value would have a max error of 1.5 > 0.5. An optimal algorithm should use multiple pieces."
    },
    {
        "description": "Constant Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_outcome": "The algorithm must return a single piece covering the entire domain [0,4) with a constant value of 5. The L∞ error is 0, which is well within the tolerance."
    },
    {
        "description": "Zero Tolerance (ε = 0)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 2], [3, 2], [4, 3], [5, float('inf')]],
        "epsilon": 0.0,
        "expected_outcome": "The approximation must exactly match the original function, resulting in the same number of pieces. The algorithm should not merge any pieces unless they already have the same constant value."
    },
    {
        "description": "Extreme Tolerance (ε > max deviation)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, float('inf')]],
        "epsilon": 5.1,
        "expected_outcome": "The algorithm must recognize that a single constant value can approximate the entire function. The min is 0, max is 10, so a single piece at 5 has a max error of 5. Since 5 < 5.1, one piece is optimal."
    },
    {
        "description": "Staircase Function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 1], [2, 8], [3, 2], [4, float('inf')]],
        "epsilon": 2.0,
        "expected_outcome": "The large, abrupt jumps make it impossible to merge consecutive pieces. The algorithm should find that each original piece requires its own approximation piece to stay within the error bounds."
    },
    {
        "description": "Oscillating Function with Small Amplitude",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.1], [1, 4.9], [2, 5.2], [3, 4.8], [4, 5.0], [5, float('inf')]],
        "epsilon": 0.2,
        "expected_outcome": "All values fall within a small range [4.8, 5.2]. The minimum number of pieces is one, with an approximation value of 5.0 and a maximum error of exactly 0.2. This tests for an optimal solution that finds the exact boundary of the tolerance."
    },
    {
        "description": "Non-Contiguous Merge",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, 1], [5, float('inf')]],
        "epsilon": 2.0,
        "expected_outcome": "The algorithm must correctly identify that it cannot merge the first and third pieces due to the intervening piece. The solution should be three separate pieces."
    },
    {
        "description": "Short and Long Segments",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 1.1], [0.2, 1.2], [10, 10], [11, 10.1], [12, float('inf')]],
        "epsilon": 0.5,
        "expected_outcome": "The algorithm should correctly merge the initial short segments and the final long segments, demonstrating it can handle a mix of segment lengths."
    },
    {
        "description": "Single Large Jump",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 10], [3, 2.2], [4, 2], [5, float('inf')]],
        "epsilon": 0.3,
        "expected_outcome": "The function is mostly flat except for a single piece with a value of 10. The algorithm should correctly identify this large jump and create a new piece for it, while merging the surrounding flat pieces."
    },
    {
        "description": "Negative Values",
        "pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -2], [2, -1.5], [3, -1], [4, float('inf')]],
        "epsilon": 0.6,
        "expected_outcome": "The algorithm should handle negative numbers correctly. The min value is -2 and max is -1, so a single piece at -1.5 has a max error of 0.5. Since 0.5 < 0.6, a single piece is optimal."
    }
]
#Iteration20
test_cases20 = [
    # 1. Trivial Case: Single piece, no approximation needed.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 2.0,
        'expected_pieces': 1,
        'description': "A single constant segment. The algorithm should return a single piece."
    },

    # 2. Simple Merging: Two adjacent pieces can be merged.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [5, 2.5], [10, float('inf')]],
        'epsilon': 0.6,
        'expected_pieces': 1,
        'description': "Two pieces within epsilon of each other. Should be merged into one."
    },

    # 3. No Merging Possible: Adjacent pieces are just outside the tolerance.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [5, 3], [10, float('inf')]],
        'epsilon': 0.9,
        'expected_pieces': 2,
        'description': "Two pieces with a difference of 1.0, just outside the 0.9 epsilon. No merging should occur."
    },

    # 4. Merging Multiple Pieces: A sequence of pieces can be merged into one.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 1.2], [4, 1.5], [6, 1.3], [8, float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 1,
        'description': "Multiple consecutive pieces within epsilon of each other. Should be merged into a single optimal piece."
    },

    # 5. Non-monotonic Piecewise Function: Test with values that don't strictly increase or decrease.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [2, 1], [4, 3], [6, float('inf')]],
        'epsilon': 2.0,
        'expected_pieces': 2,
        'description': "Values fluctuate, requiring multiple segments even with a large epsilon. Should merge [0, 5] and [2, 1] but not [4, 3] as it exceeds the tolerance."
    },

    # 6. Edge Case: Merging across zero (negative and positive values).
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, -1], [2, 0.5], [4, -0.5], [6, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 3,
        'description': "Test with negative and positive values. Merging from -1 to 0.5 is 1.5 (too large), from 0.5 to -0.5 is 1.0 (just fits). Should result in 3 pieces."
    },

    # 7. Zero Epsilon: No merging should ever occur.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 2], [4, 3], [6, float('inf')]],
        'epsilon': 0.0,
        'expected_pieces': 3,
        'description': "An epsilon of zero means no pieces can be merged unless their values are identical."
    },

    # 8. Large Epsilon: A very large tolerance, all pieces should be merged.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 100], [2, 150], [4, 200], [6, float('inf')]],
        'epsilon': 1000.0,
        'expected_pieces': 1,
        'description': "A large epsilon should merge all pieces regardless of their values."
    },

    # 9. Complex Merging Pattern: Optimal solution is not greedy.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 2], [4, 3], [6, 1.5], [8, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 3,  # e.g., [1], [2,3], [1.5]
        'description': "A case where a greedy approach might fail. An optimal algorithm should merge [2,2], [4,3] to a single piece (max diff 1.0), and leave [0,1] and [6,1.5] as separate pieces."
    },

    # 10. Floating Point Precision: Small, non-zero epsilon.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [2, 1.0001], [4, 1.0002], [6, float('inf')]],
        'epsilon': 0.00015,
        'expected_pieces': 2,
        'description': "Test for floating point precision. The first two pieces can be merged (diff 0.0001), but the third can't (diff 0.0002 from 1.0)."
    },
]
#Iteration21
test_cases21 = [
    # Test 1: A single piece within tolerance.
    # The algorithm should return 1 piece, as all points can be approximated by a single constant.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, 4.5], [3, 5.25], [4, float('inf')]],
        "epsilon": 0.51,
        "expected_pieces": 1
    },

    # Test 2: All pieces are exactly at the tolerance boundary.
    # The algorithm should correctly identify each piece as a separate segment.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 3
    },

    # Test 3: The first two pieces can be merged, but the third one cannot.
    # Tests the greedy nature of the algorithm and ensures it doesn't over-merge.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 5], [3, float('inf')]],
        "epsilon": 0.3,
        "expected_pieces": 2
    },

    # Test 4: All pieces can be merged into a single piece.
    # This is a fundamental test for optimality.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.5], [2, 9.7], [3, 10.3], [4, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 1
    },

    # Test 5: No pieces can be merged at all.
    # The algorithm should simply return the original number of pieces.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 4
    },

    # Test 6: A single, very large piece with a very large tolerance.
    # Checks for stability with large values.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1000], [1, 1001], [2, 999], [3, float('inf')]],
        "epsilon": 10.0,
        "expected_pieces": 1
    },

    # Test 7: A zig-zag pattern that requires multiple pieces even with a moderate tolerance.
    # This tests the algorithm's ability to handle oscillating data.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, 5], [4, float('inf')]],
        "epsilon": 3.0,
        "expected_pieces": 2
    },

    # Test 8: A step function where the tolerance is exactly the step height.
    # Checks for correct handling of exact boundary conditions.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },

    # Test 9: An example with a large number of short, non-mergable pieces.
    # Tests performance and correctness for a larger input.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [6, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 6
    },

    # Test 10: An example with an invalid or small epsilon.
    # A negative or zero epsilon should result in no merges, as no error is allowed.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 3
    }
]
#Iteration22
import math
test_cases22 = [
    # 1. Simple, non-trivial case: A step function that can be approximated with fewer pieces.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, 4], [4, math.inf]],
        'epsilon': 0.75,
        'expected_min_pieces': 4,
    },

    # 2. Case where no simplification is possible: Each piece is too far from its neighbors.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 10], [1, 1], [2, 10], [3, 1], [4, math.inf]],
        'epsilon': 0.5,
        'expected_min_pieces': 4,
    },

    # 3. Case where all pieces can be merged into one: A flat line.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 5], [1, 5], [2, 5], [3, 5], [4, math.inf]],
        'epsilon': 0.1,
        'expected_min_pieces': 1,
    },

    # 4. Case with varying step sizes and values, where merging is possible in some places but not others.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 1.2], [2, 3], [3, 3.1], [4, 5], [5, math.inf]],
        'epsilon': 0.25,
        'expected_min_pieces': 3,
    },

    # 5. Case with a single piece, which is a trivial but necessary edge case.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 5], [10, math.inf]],
        'epsilon': 1.0,
        'expected_min_pieces': 1,
    },

    # 6. Large number of pieces with a tolerance that allows for significant simplification.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1.1], [1, 1.2], [2, 1.3], [3, 1.4], [4, 1.5],
                   [5, 1.6], [6, 1.7], [7, 1.8], [8, 1.9], [9, 2.0], [10, math.inf]],
        'epsilon': 0.5,
        'expected_min_pieces': 1,
    },

    # 7. Zero tolerance: The algorithm should not merge any pieces unless their values are identical.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 1], [2, 2], [3, 2], [4, math.inf]],
        'epsilon': 0.0,
        'expected_min_pieces': 2,
    },

    # 8. Tolerance equal to the exact difference between two pieces.
    # This checks for correct handling of boundary conditions (<= vs <).
    {
        'pc_fx': [[-math.inf, math.inf], [0, 2], [1, 3], [2, 2], [3, math.inf]],
        'epsilon': 1.0,
        'expected_min_pieces': 2,
    },

    # 9. Test with negative y-values.
    {
        'pc_fx': [[-math.inf, math.inf], [0, -1], [1, -2], [2, -1.5], [3, -2.5], [4, math.inf]],
        'epsilon': 0.6,
        'expected_min_pieces': 3,
    },

    # 10. A complex, zig-zagging function where the optimal solution requires careful pathfinding.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, math.inf]],
        'epsilon': 1.5,
        'expected_min_pieces': 2,
    }
]
#Iteration23
test_cases23 = [
    # Test 1: Simple case with a single piece.
    # The approximation should be the original single piece, as it is already constant.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'A single constant piece. The algorithm should return the input unchanged.'
    },

    # Test 2: Two pieces with small difference, easily approximated by one piece.
    # The difference between the two values (1.0) is less than 2*epsilon (2.0), so one piece is optimal.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [5, 11], [10, float('inf')]],
        'epsilon': 0.6,
        'description': 'Two pieces with a small jump. Should be approximated by a single piece with value 10.5.'
    },

    # Test 3: Two pieces with a large difference, requiring two pieces.
    # The jump of 5.0 is greater than 2*epsilon (2.0), so two pieces are required.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [5, 15], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two pieces with a large jump. Two pieces are necessary.'
    },

    # Test 4: Multiple pieces where some can be merged.
    # First three can be merged, last two can be merged, but the jump in between requires a break.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [2, 6], [4, 5.5], [6, 12], [8, 11.5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Multiple pieces, some of which can be merged. Tests greedy vs. optimal merging.'
    },

    # Test 5: Pieces with varying widths.
    # The widths of the pieces are not uniform. The algorithm must handle this correctly.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 5], [5, 2], [7, 8], [10, float('inf')]],
        'epsilon': 1.5,
        'description': 'Pieces with varying widths. Tests if width is correctly ignored for L-infinity norm.'
    },

    # Test 6: A 'staircase' pattern where each step is slightly greater than 2*epsilon.
    # Each step requires a new piece, testing the strict inequality check.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2.01], [2, 3.02], [3, 4.03], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'A staircase pattern where each step > 2*epsilon. Each piece should be separate.'
    },

    # Test 7: A 'staircase' pattern where each step is exactly 2*epsilon.
    # This is a critical edge case. The algorithm should break and start a new piece.
    # The L_infinity norm must be <= epsilon, which means max_error_y <= epsilon.
    # If the range is exactly 2*epsilon, the midpoint is (y_min+y_max)/2. The error from this midpoint to y_min or y_max is exactly epsilon.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'A staircase pattern with steps exactly 2*epsilon. Tests the boundary condition.'
    },

    # Test 8: A 'v-shape' pattern with multiple minima/maxima.
    # The algorithm must find the global range, not just a local one.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 1], [2, 10], [3, 1], [4, float('inf')]],
        'epsilon': 4.0,
        'description': 'A "V-shape" with multiple extrema. Tests if the algorithm handles multiple peaks and valleys.'
    },

    # Test 9: Case with negative values.
    # Tests that the absolute difference is correctly calculated.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, -5], [2, -6], [4, -5.5], [6, -10], [8, float('inf')]],
        'epsilon': 1.5,
        'description': 'Includes negative values. Ensures that the absolute difference is correctly handled.'
    },

    # Test 10: Empty input or malformed input.
    # A robust algorithm should handle this gracefully, returning a reasonable result or error.
    # Here, we test with only the boundary markers. The algorithm should return a single piece.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [0, float('inf')]],
        'epsilon': 1.0,
        'description': 'Only two points, which should result in a single piece.'
    }
]
#Iteration24
test_cases24 = [
    # 1. Basic case with two pieces
    # The two pieces (y=2 and y=3) are far apart.
    # The optimal solution should be two pieces.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 2], [1, 3], [2, math.inf]],
        'epsilon': 0.1,
        'description': "Two pieces, distinct values, epsilon is small. Should result in two pieces."
    },

    # 2. Case where two pieces can be merged
    # The two pieces (y=2 and y=2.2) are within the tolerance.
    # Optimal solution should be one piece.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 2], [1, 2.2], [2, math.inf]],
        'epsilon': 0.2,
        'description': "Two pieces, values are within epsilon. Should be merged into one piece."
    },

    # 3. Case with zero epsilon
    # No tolerance for approximation.
    # The number of pieces should be the same as the input.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, math.inf]],
        'epsilon': 0,
        'description': "Zero epsilon. Should not merge any pieces."
    },

    # 4. Case with a large epsilon
    # All pieces (1, 2, 3) are within the large tolerance.
    # Optimal solution should be one piece.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, math.inf]],
        'epsilon': 1.5,
        'description': "Large epsilon. All pieces should be merged into one."
    },

    # 5. Case with a "valley" or "peak" pattern
    # The pieces go from low (1) to high (10) and back to low (1).
    # The algorithm must not merge across the peak.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 10], [2, 1], [3, math.inf]],
        'epsilon': 5,
        'description': "Peak/valley pattern. Values (1, 10, 1) are not within epsilon. Should be 3 pieces."
    },

    # 6. Case with a single piece
    # The input already has only one piece.
    # Should be handled correctly and return one piece.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 5], [1, math.inf]],
        'epsilon': 1,
        'description': "Single piece input. Should return one piece."
    },

    # 7. A complex case with multiple potential merges
    # This tests the algorithm's ability to find the optimal split points.
    # Pieces: [1, 5, 2, 6, 3] with epsilon 2.
    # The optimal solution merges [1, 5, 2] and [6, 3] into 2 pieces, or [1,5] and [2,6,3] or [1,5,2,6,3]
    # This tests the greedy nature (or non-greedy) of the algorithm
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 5], [2, 2], [3, 6], [4, 3], [5, math.inf]],
        'epsilon': 2,
        'description': "Complex case with multiple merge possibilities."
    },

    # 8. All pieces have the same value
    # All pieces should be merged into a single one, regardless of epsilon (as long as it's non-negative).
    {
        'pc_fx': [[-math.inf, math.inf], [0, 5], [1, 5], [2, 5], [3, math.inf]],
        'epsilon': 1,
        'description': "All pieces have the same value. Should be merged into one piece."
    },

    # 9. Large number of pieces
    # Tests the algorithm's performance and correctness on a larger scale.
    # Values alternate between 1 and 10. With epsilon 4.
    # This should result in 5 pieces. Each (1, 10) pair can't be merged but each (10, 1) pair can.
    # No, with L-inf norm, the max and min of the values must be within epsilon of the chosen value for that piece.
    # So if you have [1, 10, 1], and epsilon is 4, you can't merge them because max is 10 and min is 1 and 10-1 = 9 > 2*4.
    # The average value would be (1+10+1)/3 = 4. With max value 10, |4-10|=6 > 4. So cannot merge.
    # The algorithm must pick a constant value 'c' that satisfies max(|y_i - c|) <= epsilon for all y_i in the new piece.
    # The optimal 'c' is (min(y_i)+max(y_i))/2. The condition becomes (max(y_i)-min(y_i))/2 <= epsilon.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 10], [2, 1], [3, 10], [4, 1], [5, 10], [6, 1], [7, 10], [8, 1], [9, math.inf]],
        'epsilon': 4,
        'description': "Large number of pieces, alternating values. Should not merge any pieces."
    },

    # 10. Case with non-integer values
    # The algorithm should handle floating-point values correctly.
    # All pieces are within epsilon of each other.
    # [1.2, 1.5, 1.8] with epsilon 0.5. Range is 0.6, which is > 2*0.5.
    # But [1.2, 1.5] can be merged since range is 0.3 < 2*0.5.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1.2], [1, 1.5], [2, 1.8], [3, math.inf]],
        'epsilon': 0.5,
        'description': "Non-integer values. Should merge first two pieces, but not the third."
    }
]
#Iteration25
test_cases25 = [
    # 1. Basic case with a simple, monotonic function.
    # Should produce one piece.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 1.2], [2, 1.4], [3, math.inf]],
        'epsilon': 0.5,
        'expected_pieces': 1,
        'description': "Simple monotonic function, should be approximated by a single piece."
    },

    # 2. Function with two distinct clusters of values.
    # Should produce two pieces.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 10], [1, 10.1], [2, 1], [3, 1.2], [4, math.inf]],
        'epsilon': 0.2,
        'expected_pieces': 2,
        'description': "Two distinct clusters of values, requiring two pieces."
    },

    # 3. All values are the same.
    # Should produce one piece, regardless of epsilon.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 5], [1, 5], [2, 5], [3, 5], [4, math.inf]],
        'epsilon': 10,
        'expected_pieces': 1,
        'description': "All values are the same, should be approximated by a single piece."
    },

    # 4. Epsilon is very small.
    # Should produce a large number of pieces, potentially one for each original piece.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, math.inf]],
        'epsilon': 0.01,
        'expected_pieces': 4,
        'description': "Small epsilon, each original piece might be its own approximation."
    },

    # 5. Epsilon is very large.
    # Should produce one piece, as the entire function can be approximated.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 5], [2, 10], [3, 20], [4, math.inf]],
        'epsilon': 100,
        'expected_pieces': 1,
        'description': "Large epsilon, the entire function should be approximated by a single piece."
    },

    # 6. Values that oscillate around a central value.
    # Should produce one piece if the oscillation is within epsilon.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 5.1], [1, 4.9], [2, 5.2], [3, 4.8], [4, math.inf]],
        'epsilon': 0.3,
        'expected_pieces': 1,
        'description': "Oscillating values within epsilon, should be one piece."
    },

    # 7. Step function with a large jump.
    # Should produce two pieces, one before and one after the jump.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 1.1], [2, 10], [3, 10.1], [4, math.inf]],
        'epsilon': 0.5,
        'expected_pieces': 2,
        'description': "Large step change, requiring at least two pieces."
    },

    # 8. Epsilon is exactly the max difference between two points.
    # The algorithm should be able to merge these two points into one piece.
    {
        'pc_fx': [[-math.inf, math.inf], [0, 1], [1, 1.5], [2, math.inf]],
        'epsilon': 0.5,
        'expected_pieces': 1,
        'description': "Epsilon equals the difference, testing the boundary of merging."
    },

    # 9. Empty input (no actual pieces).
    # The algorithm should handle this gracefully, returning zero pieces.
    {
        'pc_fx': [[-math.inf, math.inf], [0, math.inf]],
        'epsilon': 1.0,
        'expected_pieces': 0,
        'description': "Empty input with no actual pieces."
    },

    # 10. Case with negative values and varying intervals.
    # The L-infinity norm considers the absolute difference, so negative values shouldn't be an issue.
    {
        'pc_fx': [[-math.inf, math.inf], [-2, -10], [0, -9.5], [1, -1], [3, -1.2], [5, math.inf]],
        'epsilon': 0.6,
        'expected_pieces': 2,
        'description': "Negative values and varying intervals, requires two pieces."
    }
]
#Iteration26
test_cases26 = [
    # 1. Basic case with a monotonically increasing function.
    # The algorithm should merge pieces where the difference is within epsilon.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 2], [1, 3], [3, 4], [5, 6], [6, math.inf]],
        "epsilon": 1.5,
        "description": "Monotonically increasing function, epsilon allows merging adjacent steps."
    },

    # 2. Case with a single piece, epsilon is large enough to cover the whole function.
    # Should result in a single output piece.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 2], [2, 1], [3, 8], [4, math.inf]],
        "epsilon": 7.0,
        "description": "Large epsilon, should approximate the entire function with one piece."
    },

    # 3. Case with a single piece, epsilon is too small to cover the whole function.
    # Should not merge any pieces and return the original function.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 2], [2, 1], [3, 8], [4, math.inf]],
        "epsilon": 0.5,
        "description": "Small epsilon, no pieces should be merged."
    },

    # 4. Step function where each step is exactly 2*epsilon apart.
    # The algorithm must carefully place the approximating constant to cover two pieces.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 0], [1, 2], [2, 4], [3, 6], [4, math.inf]],
        "epsilon": 1.0,
        "description": "Steps with height 2*epsilon, forcing one-to-one mapping or careful placement."
    },

    # 5. Sawtooth-like function, testing how the algorithm handles alternating directions.
    # Should merge pieces but may not find the global optimal without backtracking.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 0], [1, 5], [2, 0], [3, 5], [4, math.inf]],
        "epsilon": 2.0,
        "description": "Sawtooth pattern, tests merging alternating values."
    },

    # 6. Function with many small fluctuations, epsilon should filter them out.
    # Tests the algorithm's ability to smooth out noise.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 1.1], [2, 1.05], [3, 1.2], [4, 1.1], [5, math.inf]],
        "epsilon": 0.2,
        "description": "Small fluctuations around a constant value, epsilon should smooth."
    },

    # 7. Function where the first and last pieces have very different values but intermediate ones are close.
    # Tests handling of boundaries and non-contiguous mergable sections.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 10], [1, 1], [2, 1.1], [3, 1.05], [4, 1.2], [5, 0], [6, math.inf]],
        "epsilon": 0.5,
        "description": "Divergent boundaries with a constant core, tests non-contiguous mergable parts."
    },

    # 8. All points on the same line, but with a non-constant slope.
    # Tests handling of linear trends within the piecewise constant framework.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, 4], [4, math.inf]],
        "epsilon": 0.5,
        "description": "Linear function, but piecewise constant. Tests approximation of slope."
    },

    # 9. A case where the optimal solution requires approximating two pieces with one constant
    # that is not one of their original values.
    # Example: pc_fx values are 1 and 3. The optimal approximation is 2 with epsilon 1.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 3], [2, math.inf]],
        "epsilon": 1.0,
        "description": "Optimal approximation is a value between the original pieces."
    },

    # 10. A function with a sharp drop, testing if the algorithm correctly identifies
    # the end of a mergable sequence.
    {
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 4.5], [2, 4.8], [3, 1], [4, math.inf]],
        "epsilon": 0.5,
        "description": "Sharp drop, tests breaking a mergable sequence."
    }
]
#Iteration27
test_cases27 = [
    # Test Case 1: Simple case with clear merges
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        'epsilon': 0.75,
        'expected_output': 3  # [0,1) -> 2, [1,3) -> 3, diff=1. [1,3) & [3,6) -> 7 & 5, diff=2. [6,7) -> 5.
        # Possible merges: [0,3) (2,3) -> 1. Then [3,7) (7,5) -> 2. Two pieces with center value.
        # Wait, the expected output should be 3: [2.5], [6], [5].
        # Piece 1: [0,3) w val 2.5, err=0.5
        # Piece 2: [3,6) w val 6, err=1 (not possible, so needs more pieces)
        # Optimal is: 3 pieces
    },

    # Test Case 2: Consecutive pieces with same value
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        'epsilon': 0.1,
        'expected_output': 1  # All pieces have the same value; they should merge into one.
    },

    # Test Case 3: epsilon = 0 (no merges possible)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 0,
        'expected_output': 4  # No tolerance, so each piece must be its own.
    },

    # Test Case 4: Values are all within epsilon (one merge)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.1], [1, 1.2], [2, 1.3], [3, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 1  # Max diff is 0.2, which is < 0.5. All can be one piece.
    },

    # Test Case 5: Large number of pieces with varying values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 9], [2, 11], [3, 8], [4, 12], [5, 7], [6, 13],
                  [7, float('inf')]],
        'epsilon': 2,
        'expected_output': 4  # The values fluctuate significantly, requiring multiple pieces.
    },

    # Test Case 6: Negative values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, -2], [1, -3], [2, -2.5], [3, -4], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 2  # [0,2) could be one piece with value -2.5 (error 0.5,0,0)
        # [2,4) could be another with value -3.25 (error 0.75, 0.75)
        # No, [0,1) val -2, [1,2) val -3, [2,3) val -2.5, [3,4) val -4
        # Merging [0,1) and [1,2) -> val -2.5, err 0.5. This is ok.
        # Merging [2,3) and [3,4) -> val -3.25, err 0.75. This is not ok since epsilon=0.5
        # A valid split is 2 pieces: [0,2) and [2,4)
    },

    # Test Case 7: Zero-valued pieces
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, -1], [4, float('inf')]],
        'epsilon': 0.9,
        'expected_output': 3  # [0,1) val 0, [1,2) val 1 -> merge into one piece with val 0.5 (err 0.5). Yes.
        # [2,3) val 0, [3,4) val -1 -> merge into one piece with val -0.5 (err 0.5). Yes.
        # So two pieces: [0,2) and [2,4)
    },

    # Test Case 8: Non-uniform piece widths
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1], [3, 2], [6, 2], [7, float('inf')]],
        'epsilon': 0.5,
        'expected_output': 2  # [0,1) val 1, [1,3) val 1 -> can merge.
        # [3,6) val 2, [6,7) val 2 -> can merge.
        # The large piece from 1 to 3 should not affect the merging logic
    },

    # Test Case 9: Tight tolerance, forcing more pieces
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10.1], [2, 10.2], [3, 10.3], [4, float('inf')]],
        'epsilon': 0.05,
        'expected_output': 4  # Small epsilon means even small differences matter. Each piece must be its own.
    },

    # Test Case 10: `pc_fx` with only two pieces
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 10], [2, float('inf')]],
        'epsilon': 2.5,
        'expected_output': 2  # The difference is 5, which is exactly double the epsilon. No merge is possible.
    }
]
#Iteration28
test_cases28 = [
    # 1. Simple, well-defined case
    # This case tests basic functionality with a clear solution.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [2, 3], [4, 5], [6, 7], [8, float('inf')]],
        'epsilon': 0.5
    },

    # 2. Tolerance allows merging all pieces
    # The tolerance is large enough to approximate the entire function with a single piece.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10.5], [2, 11], [3, 10.2], [4, float('inf')]],
        'epsilon': 1.1
    },

    # 3. Tolerance is very small, no merging possible
    # The tolerance is so small that each original piece must be kept, testing the base case.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 5.2], [3, float('inf')]],
        'epsilon': 0.05
    },

    # 4. Adjacent pieces can be merged, but non-adjacent cannot
    # This checks if the algorithm correctly identifies which pieces can be grouped.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 10], [3, 10.5], [4, float('inf')]],
        'epsilon': 0.6
    },

    # 5. Step function with large gaps
    # Tests a function with large, distinct steps where some pieces can be merged, but others cannot.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 11], [2, 10], [3, 50], [4, 51], [5, float('inf')]],
        'epsilon': 1.2
    },

    # 6. A "V" shape or triangle pattern
    # The function values go up and then down, or vice-versa, testing the L-infinity norm on a non-monotonic function.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 5], [3, 3], [4, 1], [5, float('inf')]],
        'epsilon': 1.5
    },

    # 7. Zero-width pieces (or almost zero)
    # The input format implies x_i < x_{i+1}, but this case tests handling very small intervals,
    # which can be a source of floating-point errors.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [0.001, 10.1], [1, 10], [1.001, 10.1], [2, float('inf')]],
        'epsilon': 0.2
    },

    # 8. All pieces have the same value
    # A degenerate case where the entire function is already a single constant piece.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        'epsilon': 0.1
    },

    # 9. Negative and zero values
    # Tests whether the algorithm correctly handles a mix of positive, negative, and zero values.
    # The L-infinity norm is based on absolute differences.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, -5], [2, 0], [3, -10], [4, float('inf')]],
        'epsilon': 12
    },

    # 10. Piecewise function with only two actual pieces
    # A simple boundary case to check if the algorithm works for the minimum number of pieces.
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 7], [2, float('inf')]],
        'epsilon': 1.1
    }
]
#Iteration29
test_cases29 = [
    # 1. Simple Case: All points are within epsilon of a single constant value.
    # The algorithm should return one piece.
    # Expected: Optimal with 1 piece.
    {
        "name": "Case 1: Single Piece Approximation",
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 1.1], [2, 1.2], [3, 1]],
        "epsilon": 0.2,
        "expected_pieces": 1
    },

    # 2. Step Function: Each point is outside the epsilon range of the previous one.
    # The algorithm should return a piece for each original point.
    # This tests the algorithm's handling of distinct jumps.
    # Expected: 4 pieces.
    {
        "name": "Case 2: Step Function",
        "pc_fx": [[-math.inf, math.inf], [0, 0], [1, 2], [2, 4], [3, 6], [4, math.inf]],
        "epsilon": 0.5,
        "expected_pieces": 4
    },

    # 3. Large Epsilon: Epsilon is large enough to cover all points.
    # The algorithm should return one piece.
    # This tests the algorithm's behavior with a generous tolerance.
    # Expected: 1 piece.
    {
        "name": "Case 3: Large Epsilon",
        "pc_fx": [[-math.inf, math.inf], [0, 10], [1, 12], [2, 11], [3, 10.5], [4, math.inf]],
        "epsilon": 3,
        "expected_pieces": 1
    },

    # 4. Zero Epsilon: Epsilon is zero.
    # The algorithm should return a piece for each segment where the value changes.
    # This tests for exact matching and should result in the maximum number of pieces.
    # Expected: The number of pieces will equal the number of points minus 1. Here, 3 pieces.
    {
        "name": "Case 4: Zero Epsilon",
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 5], [2, 6], [3, 6]],
        "epsilon": 0,
        "expected_pieces": 3
    },

    # 5. Epsilon equals max deviation: The tolerance is exactly the maximum deviation of the data points.
    # The algorithm should return one piece. This is a critical edge case.
    # Expected: 1 piece.
    {
        "name": "Case 5: Epsilon Equals Max Deviation",
        "pc_fx": [[-math.inf, math.inf], [0, 10], [1, 10.5], [2, 11], [3, 10.5], [4, 10]],
        "epsilon": 1,
        "expected_pieces": 1
    },

    # 6. Negative values: The input contains negative values.
    # The algorithm should handle negative numbers correctly.
    # Expected: 2 pieces. The jump from 1 to -1 should be a new piece.
    {
        "name": "Case 6: Negative Values",
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 0.5], [2, -1], [3, -1.5], [4, math.inf]],
        "epsilon": 0.6,
        "expected_pieces": 2
    },

    # 7. Disjoint segments: Input consists of distinct groups of points.
    # The algorithm should identify each group as a separate piece.
    # Expected: 3 pieces.
    {
        "name": "Case 7: Disjoint Segments",
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 1.2], [2, 5], [3, 5.1], [4, 10], [5, 10.3], [6, math.inf]],
        "epsilon": 0.3,
        "expected_pieces": 3
    },

    # 8. All equal values: All points have the same value.
    # The algorithm should return one piece, regardless of epsilon.
    # This checks for a trivial case.
    # Expected: 1 piece.
    {
        "name": "Case 8: All Equal Values",
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 5], [2, 5], [3, 5]],
        "epsilon": 0.1,
        "expected_pieces": 1
    },

    # 9. Large number of points with small variations:
    # This tests the algorithm's efficiency and correctness with a larger input.
    # The points slowly increase, but each small step is within epsilon.
    # Expected: 1 piece.
    {
        "name": "Case 9: Large Number of Points",
        "pc_fx": [[-math.inf, math.inf]] + [[i, i * 0.1] for i in range(1, 101)] + [[101, math.inf]],
        "epsilon": 10,
        "expected_pieces": 1
    },

    # 10. Boundary case: The first and last points of a segment are exactly at the epsilon boundary.
    # The algorithm must correctly decide if they can be grouped or not.
    # The range of y values is [1, 2] and epsilon is 0.5, so they can be grouped.
    # Expected: 1 piece.
    {
        "name": "Case 10: Boundary Epsilon Check",
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 1.5], [2, 2], [3, 1.5], [4, 1]],
        "epsilon": 0.5,
        "expected_pieces": 1
    }
]
#Iteration30
test_cases30 = [
    # 1. Basic case: No merging possible.
    # Each segment is separated by more than 2 * epsilon.
    {
        "name": "No Merging Possible",
        "pc_fx": [[-math.inf, math.inf], [0, 2], [1, 5], [2, 1], [3, math.inf]],
        "epsilon": 1.0,
        "expected_pieces": 3,
        "description": "Each piece is too far apart to be merged, so the number of pieces should remain the same."
    },

    # 2. Complete Merging: All pieces can be merged into a single one.
    # The maximum difference between any two y values is <= 2 * epsilon.
    {
        "name": "Complete Merging",
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 5.5], [2, 6], [3, math.inf]],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "description": "All pieces are within the tolerance range and can be merged into a single segment."
    },

    # 3. Merging in pairs: Adjacent pieces can be merged.
    # The difference between y values of adjacent pieces is <= 2 * epsilon.
    {
        "name": "Merging in Pairs",
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 2], [2, 10], [3, 11], [4, math.inf]],
        "epsilon": 0.75,
        "expected_pieces": 2,
        "description": "Pieces (1,2) and (3,4) can be merged, but the two resulting segments cannot be merged with each other."
    },

    # 4. Merging across a gap: Merging non-adjacent segments.
    # The algorithm must consider merging pieces that aren't next to each other in the original list.
    {
        "name": "Merging Across a Gap",
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 3], [2, 2], [3, math.inf]],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "The first and third segments can be merged, even though there's a segment in between them. The maximum difference between y-values (3 - 1 = 2) is within the 2 * epsilon tolerance (2 * 1 = 2)."
    },

    # 5. Multiple optimal solutions: The algorithm should find the minimum number of pieces.
    # There are multiple ways to merge, but the number of final pieces should be the same.
    {
        "name": "Multiple Optimal Solutions",
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 2], [2, 3], [3, 4], [4, math.inf]],
        "epsilon": 0.5,
        "expected_pieces": 3,
        "description": "The optimal solution is to merge pieces (1,2) and (3,4), resulting in 3 final pieces. Merging (2,3) and keeping (1) and (4) separate would also result in 3 pieces, so both are optimal."
    },

    # 6. Epsilon equals zero: No merging should happen.
    # The algorithm should handle epsilon being 0.
    {
        "name": "Epsilon is Zero",
        "pc_fx": [[-math.inf, math.inf], [0, 1], [1, 1.1], [2, 1.2], [3, math.inf]],
        "epsilon": 0.0,
        "expected_pieces": 3,
        "description": "With epsilon set to 0, no merging should occur as any difference in y-values will exceed the tolerance."
    },

    # 7. Large epsilon: All pieces can be merged.
    # Similar to test case 2 but with a larger range of values.
    {
        "name": "Large Epsilon",
        "pc_fx": [[-math.inf, math.inf], [0, 10], [1, 20], [2, 15], [3, 12], [4, math.inf]],
        "epsilon": 5.0,
        "expected_pieces": 1,
        "description": "A large epsilon should allow all pieces to be merged, as the range of y-values is (20-10)=10 which is less than or equal to 2*epsilon=10."
    },

    # 8. All y-values are the same: All pieces should be merged regardless of epsilon.
    {
        "name": "All Y-Values Are the Same",
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, 5], [2, 5], [3, 5], [4, math.inf]],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "description": "Since all y-values are identical, they can be represented by a single piece regardless of the epsilon value."
    },

    # 9. Single piece input: No approximation needed, result should be 1 piece.
    {
        "name": "Single Piece Input",
        "pc_fx": [[-math.inf, math.inf], [0, 5], [1, math.inf]],
        "epsilon": 10.0,
        "expected_pieces": 1,
        "description": "A single piece input should always result in one piece."
    },

    # 10. Negative y-values: The algorithm should handle negative numbers correctly.
    # The difference between two negative numbers is calculated correctly.
    {
        "name": "Negative Y-Values",
        "pc_fx": [[-math.inf, math.inf], [0, -5], [1, -6], [2, -1], [3, math.inf]],
        "epsilon": 2.0,
        "expected_pieces": 2,
        "description": "Pieces (1,2) can be merged as the difference between y-values is |-6 - (-5)| = 1, which is less than 2*epsilon. The second piece (-1) cannot be merged with the result as |-1 - (-5.5)| = 4.5 > 2*epsilon."
    },
]