#17Sept 2:55PM
#Iteration1
test_cases1 = [
    # Test Case 1: Simple case with 2 pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2],
            [3, 5],
            [6, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Simple case with 2 pieces that can't be merged"
    },

    # Test Case 2: All pieces within epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 3.0],
            [1, 3.1],
            [2, 2.9],
            [3, 3.05],
            [4, float('inf')]
        ],
        "epsilon": 0.2,
        "description": "All pieces within epsilon, should be merged to one piece"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 2],
            [2, 0],
            [3, 2],
            [4, 0],
            [5, 2],
            [6, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Sawtooth pattern with amplitude 1, should require all pieces"
    },

    # Test Case 4: Single piece
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5],
            [10, float('inf')]
        ],
        "epsilon": 2.0,
        "description": "Single piece, should remain as is"
    },

    # Test Case 5: Alternating high and low values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10],
            [1, 0],
            [2, 10],
            [3, 0],
            [4, 10],
            [5, float('inf')]
        ],
        "epsilon": 4.9,
        "description": "Alternating high and low values, should require all pieces"
    },

    # Test Case 6: Gradually increasing values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4],
            [5, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Gradually increasing values, should be able to merge some pieces"
    },

    # Test Case 7: Large jump in middle
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 1],
            [2, 1],
            [3, 10],
            [4, 1],
            [5, 1],
            [6, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Large jump in middle, should require at least 2 pieces"
    },

    # Test Case 8: Small epsilon with tiny variations
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0],
            [1, 1.0001],
            [2, 0.9999],
            [3, 1.0002],
            [4, float('inf')]
        ],
        "epsilon": 0.00005,
        "description": "Tiny variations with very small epsilon, should require all pieces"
    },

    # Test Case 9: Large epsilon that can merge everything
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, float('inf')]
        ],
        "epsilon": 10.0,
        "description": "Large epsilon that can merge all pieces into one"
    },

    # Test Case 10: Complex pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 2],
            [2, 1],
            [3, 2],
            [4, 0],
            [5, 2],
            [6, 1],
            [7, 2],
            [8, 0],
            [9, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Complex pattern with varying differences"
    }
]
#Iteration2
test_cases2 = [
    # Test Case 1: Simple increasing function
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Simple increasing function with constant slope"
    },

    # Test Case 2: Single piece (should return 1 piece)
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5], [1, 5], [2, 5], [3, 5],
            [4, float('inf')]
        ],
        "epsilon": 0.1,
        "description": "Already constant function"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 3], [2, 1], [3, 3], [4, 1],
            [5, 3], [6, 1], [7, 3], [8, 1], [9, 3],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Sawtooth pattern with amplitude 1"
    },

    # Test Case 4: Step function with varying step sizes
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2], [1, 2], [2, 5], [3, 5], [4, 1],
            [5, 1], [6, 4], [7, 4], [8, 4], [9, 2],
            [10, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Step function with varying step sizes"
    },

    # Test Case 5: Single spike in the middle
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 1], [2, 1], [3, 10], [4, 1],
            [5, 1], [6, 1], [7, 1],
            [8, float('inf')]
        ],
        "epsilon": 2.0,
        "description": "Single spike in the middle"
    },

    # Test Case 6: Very small epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.3], [4, 1.4],
            [5, 1.5], [6, 1.6], [7, 1.7], [8, 1.8], [9, 1.9],
            [10, float('inf')]
        ],
        "epsilon": 0.05,
        "description": "Very small epsilon requiring many pieces"
    },

    # Test Case 7: Large epsilon allowing for few pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 10], [2, 1], [3, 10], [4, 1],
            [5, 10], [6, 1], [7, 10], [8, 1], [9, 10],
            [10, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Large epsilon allowing for few pieces"
    },

    # Test Case 8: Non-uniform x-spacing
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [0.1, 2], [0.2, 3], [1.0, 4], [1.5, 5],
            [2.0, 6], [3.0, 7], [5.0, 8], [8.0, 9], [13.0, 10],
            [21.0, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Non-uniform x-spacing with increasing values"
    },

    # Test Case 9: Alternating high and low values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10], [1, 0], [2, 10], [3, 0], [4, 10],
            [5, 0], [6, 10], [7, 0], [8, 10], [9, 0],
            [10, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Alternating high and low values"
    },

    # Test Case 10: Random-looking function
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 3], [1, 1], [2, 4], [3, 1], [4, 5],
            [5, 9], [6, 2], [7, 6], [8, 5], [9, 3],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Random-looking function (digits of pi)"
    }
]
#Iteration3
test_cases3 = [
    # Test Case 1: Simple case - already optimal
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 3], [4, 5], [6, float('inf')]],
        "epsilon": 0.5,
        "description": "Already optimal - no approximation needed"
    },

    # Test Case 2: Simple merge case
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 0.9], [3, float('inf')]],
        "epsilon": 0.2,
        "description": "Simple merge of similar values"
    },

    # Test Case 3: Alternating pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, 1], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Alternating pattern with epsilon=1.0"
    },

    # Test Case 4: Single spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 5], [3, 0], [4, 0], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Single spike that should be preserved"
    },

    # Test Case 5: Plateau with noise
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 10.1], [2, 9.9], [3, 10.2],
                  [4, 9.8], [5, 10.1], [6, 10.0], [7, float('inf')]],
        "epsilon": 0.3,
        "description": "Plateau with small noise within epsilon"
    },

    # Test Case 6: Step function
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 0], [2, 5], [3, 5],
                  [4, 10], [5, 10], [6, float('inf')]],
        "epsilon": 0.1,
        "description": "Step function with exact steps"
    },

    # Test Case 7: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 1], [3, 2],
                  [4, 1], [5, 2], [6, float('inf')]],
        "epsilon": 0.6,
        "description": "Sawtooth pattern with varying amplitudes"
    },

    # Test Case 8: Single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece - should remain as is"
    },

    # Test Case 9: Large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 5], [2, 2], [3, 6],
                  [4, 3], [5, 7], [6, float('inf')]],
        "epsilon": 4.0,
        "description": "Large epsilon that can merge all pieces"
    },

    # Test Case 10: Complex pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 2], [2, 1], [3, 3],
                  [4, 2], [5, 4], [6, 3], [7, 5],
                  [8, 4], [9, 6], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Complex pattern with varying slopes"
    }
]
#Iteration4
test_cases4 = [
    # Test Case 1: Simple case with exact fit
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2], [1, 2], [2, 2],
            [3, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Constant function should be approximated with 1 piece"
    },

    # Test Case 2: Step function with minimal changes
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 3], [2, 1], [3, 3],
            [4, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Step function with alternating values within epsilon"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 3], [2, 1], [3, 3], [4, 1],
            [5, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Sawtooth pattern that can be approximated with 2 pieces"
    },

    # Test Case 4: Single point requiring multiple pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0], [1, 0], [2, 10], [3, 0], [4, 0],
            [5, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Single spike that requires its own piece"
    },

    # Test Case 5: Monotonically increasing function
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Monotonically increasing function"
    },

    # Test Case 6: Large epsilon that allows single piece
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 3], [2, 5], [3, 7], [4, 9],
            [5, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Large epsilon that allows single piece approximation"
    },

    # Test Case 7: Small epsilon requiring many pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 1.1], [2, 1.2], [3, 1.1], [4, 1.0],
            [5, float('inf')]
        ],
        "epsilon": 0.05,
        "description": "Small epsilon requiring many pieces"
    },

    # Test Case 8: Piece with large jump
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 1], [2, 10], [3, 10],
            [4, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Function with a large jump requiring a new piece"
    },

    # Test Case 9: Multiple jumps with varying distances
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 1], [2, 4], [3, 4],
            [4, 2], [5, 2], [6, 5], [7, 5],
            [8, float('inf')]
        ],
        "epsilon": 1.5,
        "description": "Multiple jumps with varying distances"
    },

    # Test Case 10: Edge case with minimal input
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, float('inf')]
        ],
        "epsilon": 0.1,
        "description": "Minimal input case with just one piece"
    }
]
#Iteration5
test_cases5 = [
    # Test Case 1: Simple case with 3 pieces, should require 2 pieces with epsilon=1.5
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2], [1, 3], [3, 2],
            [4, float('inf')]
        ],
        "epsilon": 1.5,
        "description": "Simple 3-piece function that can be approximated with 2 pieces"
    },

    # Test Case 2: Single piece (already optimal)
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5],
            [10, float('inf')]
        ],
        "epsilon": 2.0,
        "description": "Single piece function (already optimal)"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2], [1, 4], [2, 2], [3, 4], [4, 2],
            [5, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Sawtooth pattern with period 2"
    },

    # Test Case 4: Step function with large jumps
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0], [1, 10], [2, 0], [3, 10], [4, 0],
            [5, float('inf')]
        ],
        "epsilon": 4.5,
        "description": "Step function with large jumps"
    },

    # Test Case 5: Function with a single spike
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 1], [2, 10], [3, 1], [4, 1],
            [5, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Single spike in the middle"
    },

    # Test Case 6: Function with small variations within epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 3.0], [1, 3.2], [2, 2.9], [3, 3.1], [4, 3.0],
            [5, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Small variations within epsilon"
    },

    # Test Case 7: Function with alternating high and low values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10], [1, 0], [2, 10], [3, 0], [4, 10],
            [5, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Alternating high and low values"
    },

    # Test Case 8: Function with a single piece that can't be merged
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5], [1, 6], [2, 5], [3, 6], [4, 5],
            [5, float('inf')]
        ],
        "epsilon": 0.4,
        "description": "No pieces can be merged with given epsilon"
    },

    # Test Case 9: Function with a single point that requires special handling
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5], [1, 10], [1, 10], [2, 5],  # Point at x=1 is duplicated
            [3, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Function with a single point that requires special handling"
    },

    # Test Case 10: Large number of pieces with small variations
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            *[[i, 5 + 0.1 * (i % 3)] for i in range(20)],
            [20, float('inf')]
        ],
        "epsilon": 0.25,
        "description": "Large number of pieces with small variations"
    }
]
#Iteration6
test_cases6 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 2.0,
        "description": "Single piece input should require exactly 1 piece"
    },

    # Test Case 2: Two pieces with same value (can be merged)
    {
        "name": "mergeable_pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 3], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Adjacent pieces with same value should be merged"
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth_pattern",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1], [3, 3],
                  [4, 1], [5, 3], [6, 1], [7, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern with varying amplitudes"
    },

    # Test Case 4: Step function
    {
        "name": "step_function",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 3], [3, 4],
                  [4, 5], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Monotonically increasing step function"
    },

    # Test Case 5: Large epsilon (should merge all pieces)
    {
        "name": "large_epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 3], [3, 4],
                  [4, 5], [5, float('inf')]],
        "epsilon": 10.0,
        "description": "Large epsilon should allow merging all pieces into one"
    },

    # Test Case 6: Small epsilon (should keep all pieces)
    {
        "name": "small_epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.3],
                  [4, 1.4], [5, float('inf')]],
        "epsilon": 0.05,
        "description": "Very small epsilon should prevent any merging"
    },

    # Test Case 7: Single point discontinuity
    {
        "name": "single_point_discontinuity",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 10], [1, 1], [2, 1],
                  [3, float('inf')]],
        "epsilon": 0.5,
        "description": "Single point discontinuity in the middle"
    },

    # Test Case 8: Large range with small variations
    {
        "name": "large_range_small_variations",
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[x, 10 + 0.1 * (x % 3)] for x in range(0, 100)] +
                 [[100, float('inf')]],
        "epsilon": 0.2,
        "description": "Large range with small periodic variations"
    },

    # Test Case 9: Alternating high and low values
    {
        "name": "alternating_values",
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 10 if i % 2 == 0 else 0] for i in range(0, 10)] +
                 [[10, float('inf')]],
        "epsilon": 5.0,
        "description": "Alternating between high and low values"
    },

    # Test Case 10: Your provided example
    {
        "name": "provided_example",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 3], [3, 7], [6, 5],
                  [7, float('inf')]],
        "epsilon": 0.75,
        "description": "Example from the problem statement"
    }
]
#Iteration7
test_cases7 = [
    # Test Case 1: Simple case with 3 pieces, optimal solution should have 2 pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2], [1, 2], [2, 2],  # All y=2
            [3, 5], [4, 5],  # y=5
            [5, 2], [6, 2],  # y=2 again
            [7, float('inf')]
        ],
        "epsilon": 1.5,
        "description": "Simple case with 3 pieces, optimal solution should have 2 pieces"
    },

    # Test Case 2: Single piece input (should return 1 piece)
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 3], [1, 3], [2, 3], [3, 3],
            [4, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Single piece input (should return 1 piece)"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0], [1, 1], [2, 0], [3, 1], [4, 0],
            [5, 1], [6, 0], [7, 1], [8, 0], [9, 1],
            [10, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Sawtooth pattern that can be approximated with 2 pieces"
    },

    # Test Case 4: Strictly increasing function
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9], [9, 10],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Strictly increasing function"
    },

    # Test Case 5: Step function with varying step sizes
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 1], [2, 1],  # y=1
            [3, 4], [4, 4], [5, 4],  # y=4
            [6, 2], [7, 2], [8, 2],  # y=2
            [9, 5], [10, 5],  # y=5
            [11, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Step function with varying step sizes"
    },

    # Test Case 6: Edge case with very small epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.001], [1, 1.002], [2, 1.001], [3, 1.003],
            [4, 1.001], [5, 1.002], [6, 1.001],
            [7, float('inf')]
        ],
        "epsilon": 0.0005,
        "description": "Very small epsilon requiring many pieces"
    },

    # Test Case 7: Large epsilon that can approximate everything to one piece
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10], [1, 15], [2, 5], [3, 20],
            [4, 0], [5, 25], [6, -5], [7, 30],
            [8, float('inf')]
        ],
        "epsilon": 20,
        "description": "Large epsilon that can approximate everything to one piece"
    },

    # Test Case 8: Non-uniform x-spacing
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2], [0.1, 2], [0.5, 5], [1.0, 5],
            [2.0, 8], [5.0, 8], [10.0, 8], [20.0, 2],
            [25.0, float('inf')]
        ],
        "epsilon": 1.5,
        "description": "Non-uniform x-spacing"
    },

    # Test Case 9: Alternating high and low values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10], [1, 0], [2, 10], [3, 0], [4, 10],
            [5, 0], [6, 10], [7, 0], [8, 10], [9, 0],
            [10, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Alternating high and low values"
    },

    # Test Case 10: Random-like pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 3], [2, 2], [3, 4], [4, 1],
            [5, 2], [6, 5], [7, 3], [8, 4], [9, 2],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Random-like pattern"
    }
]
#Iteration8
test_cases8 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece - already optimal"
    },

    # Test Case 2: Two pieces with same value
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [5, 4], [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Two identical pieces - should be merged"
    },

    # Test Case 3: Step function with minimal ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Step function - requires 3 pieces with ε=0.5"
    },

    # Test Case 4: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 1], [3, 2],
                  [4, 1], [5, 2], [6, 1], [7, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern - test piece merging"
    },

    # Test Case 5: Large ε that allows single piece approximation
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 3], [3, 4],
                  [4, 5], [5, 6], [6, float('inf')]],
        "epsilon": 3.0,
        "description": "Large ε - should be approximated by single piece"
    },

    # Test Case 6: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 0], [2, 10], [3, 0],
                  [4, 10], [5, 0], [6, float('inf')]],
        "epsilon": 5.0,
        "description": "Alternating high/low values - requires 4 pieces"
    },

    # Test Case 7: Single outlier point
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1], [2, 10], [3, 1],
                  [4, 1], [5, float('inf')]],
        "epsilon": 2.0,
        "description": "Single outlier point - tests handling of local features"
    },

    # Test Case 8: Gradually increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 1], [2, 2], [3, 3],
                  [4, 4], [5, 5], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Gradually increasing values - requires multiple pieces"
    },

    # Test Case 9: Non-uniform x-spacing
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [0.1, 2], [0.2, 1], [1, 2],
                  [10, 1], [100, 2], [1000, float('inf')]],
        "epsilon": 0.75,
        "description": "Non-uniform x-spacing - tests handling of different scales"
    },

    # Test Case 10: Complex pattern with varying ε
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1], [3, 4],
                  [4, 2], [5, 5], [6, 3], [7, 6],
                  [8, 4], [9, 7], [10, float('inf')]],
        "epsilon": 1.5,
        "description": "Complex pattern - requires careful piece selection"
    }
]
#Iteration9
test_cases9 = [
    # Test Case 1: Simple case with 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 3], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Simple case with 2 pieces, should require 1 piece"
    },

    # Test Case 2: Staircase pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Staircase pattern, each step increases by 1, should require multiple pieces"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, 1], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Sawtooth pattern, tests handling of alternating high and low values"
    },

    # Test Case 4: Single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece, should be returned as is"
    },

    # Test Case 5: Large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 10.0,
        "description": "Large epsilon, should be approximated with 1 piece"
    },

    # Test Case 6: Small variations within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 0.9], [3, 1.05], [4, 0.95], [5, float('inf')]],
        "epsilon": 0.2,
        "description": "Small variations within epsilon, should be approximated with 1 piece"
    },

    # Test Case 7: Step function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 0], [5, 10], [10, 10], [10, 0], [15, float('inf')]],
        "epsilon": 2.0,
        "description": "Step function, tests handling of vertical jumps"
    },

    # Test Case 8: Non-uniform x-spacing
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [10, 2], [15, 1], [30, 2], [31, float('inf')]],
        "epsilon": 0.6,
        "description": "Non-uniform x-spacing, tests handling of varying interval lengths"
    },

    # Test Case 9: Large value range
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1000], [1, 2000], [2, 1000], [3, 2000], [4, float('inf')]],
        "epsilon": 100,
        "description": "Large value range, tests numerical stability"
    },

    # Test Case 10: Boundary test
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1 + 0.75], [2, 1], [3, 1 + 0.75], [4, float('inf')]],
        "epsilon": 0.75,
        "description": "Boundary test, values exactly at epsilon difference"
    }
]
#Iteration10
test_cases10 = [
    # Test Case 1: Simple case with 3 pieces, can be reduced to 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1], [4, 1], [6, 2], [8, float('inf')]],
        "epsilon": 0.5,
        "description": "Simple case with 3 pieces that can be reduced to 2 pieces"
    },

    # Test Case 2: Single piece (should remain as is)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [10, float('inf')]],
        "epsilon": 0.1,
        "description": "Single piece function (should remain unchanged)"
    },

    # Test Case 3: Two pieces with large jump (cannot be merged)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 10], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Two pieces with large jump that cannot be merged"
    },

    # Test Case 4: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1], [3, 3],
                  [4, 1], [5, 3], [6, 1], [7, 3],
                  [8, 1], [9, 3], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern that can be approximated with fewer pieces"
    },

    # Test Case 5: Piece with small deviation within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.1], [2, 4.9],
                  [3, 5.05], [4, 5.15], [5, float('inf')]],
        "epsilon": 0.2,
        "description": "Pieces with small deviations that can be merged"
    },

    # Test Case 6: Varying piece lengths
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 2], [1.1, 3], [1.2, 3],
                  [5, 2], [10, 3], [15, float('inf')]],
        "epsilon": 0.5,
        "description": "Varying piece lengths, some very short"
    },

    # Test Case 7: Large epsilon test
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 10], [2, 20],
                  [3, 30], [4, 40], [5, float('inf')]],
        "epsilon": 15,
        "description": "Large epsilon that should allow significant simplification"
    },

    # Test Case 8: Small epsilon test
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.01], [2, 1.02],
                  [3, 1.03], [4, 1.04], [5, float('inf')]],
        "epsilon": 0.005,
        "description": "Very small epsilon that should prevent most merging"
    },

    # Test Case 9: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 0], [2, 10], [3, 0],
                  [4, 10], [5, 0], [6, 10], [7, 0],
                  [8, 10], [9, 0], [10, float('inf')]],
        "epsilon": 5,
        "description": "Alternating high and low values"
    },

    # Test Case 10: Complex pattern with varying epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.5], [2, 2], [3, 2.5],
                  [4, 3], [5, 2.5], [6, 2], [7, 1.5],
                  [8, 1], [9, 1.5], [10, 2], [11, float('inf')]],
        "epsilon": 0.6,
        "description": "Complex pattern with varying epsilon"
    }
]
#Iteration11
test_cases11 = [
    # Test Case 1: Simple case - single piece already satisfies epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece already satisfies epsilon"
    },

    # Test Case 2: Two pieces needed - step function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 3], [3, 3], [4, float('inf')]],
        "epsilon": 1.0,
        "description": "Two pieces needed for step function"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, 1], [5, 2], [6, float('inf')]],
        "epsilon": 0.6,
        "description": "Sawtooth pattern requiring multiple pieces"
    },

    # Test Case 4: Large epsilon that allows single piece approximation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 2], [4, 3], [5, 4], [6, float('inf')]],
        "epsilon": 2.0,
        "description": "Large epsilon allowing single piece"
    },

    # Test Case 5: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, 10], [5, 0], [6, float('inf')]],
        "epsilon": 5.0,
        "description": "Alternating high and low values"
    },

    # Test Case 6: Single spike in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Single spike in the middle"
    },

    # Test Case 7: Gradually increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Gradually increasing values"
    },

    # Test Case 8: Plateau with varying widths
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1], [3, 2], [6, 2], [7, 3], [10, 3], [11, float('inf')]],
        "epsilon": 0.75,
        "description": "Plateaus with varying widths"
    },

    # Test Case 9: Small epsilon requiring many pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 0.9], [3, 1.2], [4, 0.8], [5, 1.3],
                  [6, float('inf')]],
        "epsilon": 0.2,
        "description": "Small epsilon requiring many pieces"
    },

    # Test Case 10: Large jump in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 100], [4, 1], [5, 1], [6, float('inf')]],
        "epsilon": 2.0,
        "description": "Large jump in the middle"
    }
]
#Iteration12
test_cases12 = [
    # Test Case 1: Simple case - already optimal
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2],
            [2, 4],
            [4, 6],
            [6, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Already optimal with minimum pieces"
    },

    # Test Case 2: Can be reduced
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 1.5],
            [2, 1.8],
            [3, 2.1],
            [4, 2.4],
            [5, 2.7],
            [6, 3.0],
            [7, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Can be reduced to fewer pieces"
    },

    # Test Case 3: Single piece
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5],
            [10, float('inf')]
        ],
        "epsilon": 10.0,
        "description": "Single piece is sufficient"
    },

    # Test Case 4: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 3],
            [2, 1],
            [3, 3],
            [4, 1],
            [5, 3],
            [6, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Sawtooth pattern"
    },

    # Test Case 5: Large epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10],
            [1, 12],
            [2, 8],
            [3, 15],
            [4, 5],
            [5, float('inf')]
        ],
        "epsilon": 10.0,
        "description": "Large epsilon allows significant approximation"
    },

    # Test Case 6: Small epsilon requires more pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0],
            [1, 1.1],
            [2, 0.9],
            [3, 1.2],
            [4, 0.8],
            [5, float('inf')]
        ],
        "epsilon": 0.1,
        "description": "Small epsilon requires more pieces"
    },

    # Test Case 7: Step function
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [5, 2],
            [10, 3],
            [15, 4],
            [20, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Step function with large constant segments"
    },

    # Test Case 8: Alternating high and low values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10],
            [1, 0],
            [2, 10],
            [3, 0],
            [4, 10],
            [5, 0],
            [6, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Alternating high and low values"
    },

    # Test Case 9: Single point with different values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [0.5, 2],
            [1.0, 1],
            [1.5, 2],
            [2.0, float('inf')]
        ],
        "epsilon": 0.6,
        "description": "Rapidly changing values around single points"
    },

    # Test Case 10: Large range with small variations
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 100],
            [1000, 101],
            [2000, 99],
            [3000, 102],
            [4000, 98],
            [5000, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Large range with small relative variations"
    }
]
#Iteration13
import math
test_cases13 = [
        # Test Case 1: Single piece (already optimal)
        {
            'name': 'single_piece',
            'pc_fx': [(-math.inf, 0), (0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0), (5.0, 0), (math.inf, 0)],
            'epsilon': 0.5,
            'expected_pieces': 1
        },

        # Test Case 2: Two pieces with clear separation
        {
            'name': 'two_pieces_clear_separation',
            'pc_fx': [(-math.inf, 0), (0, 1.0), (1, 1.0), (2, 1.0), (3, 2.0), (4, 2.0), (5, 2.0), (6, 0), (math.inf, 0)],
            'epsilon': 0.4,
            'expected_pieces': 2
        },

        # Test Case 3: Sawtooth pattern (can be merged with appropriate epsilon)
        {
            'name': 'sawtooth_pattern',
            'pc_fx': [(-math.inf, 0)] + [(i, 1.0 if i % 2 == 0 else 0.0) for i in range(10)] + [(10, 0), (math.inf, 0)],
            'epsilon': 0.6,  # Should allow merging of all pieces
            'expected_pieces': 1
        },

        # Test Case 4: Gradually increasing values
        {
            'name': 'gradual_increase',
            'pc_fx': [(-math.inf, 0)] + [(i, i*0.1) for i in range(11)] + [(10, 0), (math.inf, 0)],
            'epsilon': 0.25,  # Tests optimal merging
            'expected_pieces': 5  # Should find optimal merging points
        },

        # Test Case 5: Large jump in values
        {
            'name': 'large_jump',
            'pc_fx': [(-math.inf, 0), (0, 1.0), (1, 1.0), (2, 10.0), (3, 10.0), (4, 0), (math.inf, 0)],
            'epsilon': 2.0,  # Should require at least 2 pieces
            'expected_pieces': 2
        },

        # Test Case 6: Single point with epsilon = 0 (should return original function)
        {
            'name': 'single_point_zero_epsilon',
            'pc_fx': [(-math.inf, 0), (0, 1.0), (1, 0), (math.inf, 0)],
            'epsilon': 0.0,
            'expected_pieces': 1
        },

        # Test Case 7: Multiple pieces with varying lengths
        {
            'name': 'varying_length_pieces',
            'pc_fx': [(-math.inf, 0),
                     (0, 1.0), (2, 1.5),  # First piece: length 2
                     (3, 2.0), (3.5, 2.5), # Second piece: length 0.5
                     (5, 3.0), (8, 3.0),   # Third piece: length 3
                     (9, 0), (math.inf, 0)],
            'epsilon': 0.6,
            'expected_pieces': 3
        },

        # Test Case 8: Edge case with very small epsilon
        {
            'name': 'very_small_epsilon',
            'pc_fx': [(-math.inf, 0)] + [(i, 1.0 + (i * 0.0001)) for i in range(100)] + [(100, 0), (math.inf, 0)],
            'epsilon': 0.00001,
            'expected_pieces': 100  # Each piece needs to be preserved
        },

        # Test Case 9: Piece with zero width (should be handled gracefully)
        {
            'name': 'zero_width_piece',
            'pc_fx': [(-math.inf, 0), (0, 1.0), (0, 2.0), (1, 2.0), (2, 1.0), (3, 0), (math.inf, 0)],
            'epsilon': 0.5,
            'expected_pieces': 3  # [0,0)=1.0, [0,1)=2.0, [1,∞)≈1.5
        },

        # Test Case 10: Large number of pieces with random values
        {
            'name': 'large_random_pieces',
            'pc_fx': [(-math.inf, 0)] + [(i, 1.0 + (i % 3)) for i in range(1000)] + [(1000, 0), (math.inf, 0)],
            'epsilon': 1.5,  # Should allow significant reduction in pieces
            'expected_pieces': 3  # One piece for each unique value (1.0, 2.0, 3.0)
        },

        # Test Case 11: Alternating high and low values
        {
            'name': 'alternating_values',
            'pc_fx': [(-math.inf, 0)] + [(i, 2.0 if i % 2 == 0 else 0.0) for i in range(10)] + [(10, 0), (math.inf, 0)],
            'epsilon': 1.0,  # Can be approximated with a single piece at y=1.0
            'expected_pieces': 1
        },

        # Test Case 12: Sinusoidal pattern
        {
            'name': 'sinusoidal_pattern',
            'pc_fx': [(-math.inf, 0)] + [(x, math.sin(x/2)) for x in range(0, 32)] + [(32, 0), (math.inf, 0)],
            'epsilon': 0.3,  # Should find optimal number of pieces to approximate sine wave
            'expected_pieces': 6  # Approximate number of pieces needed
        }
    ]
#Iteration14
test_cases14 = [
        # Test case 1: Single piece function (already optimal)
        {
            'name': 'single_piece',
            'pc_fx': [(-math.inf, 0), (0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0), (4.0, 1.0), (5.0, 0), (math.inf, 0)],
            'epsilon': 0.5,
            'expected_pieces': 1
        },
        # Test case 2: Two pieces required (values differ by more than 2*epsilon)
        {
            'name': 'two_pieces_necessary',
            'pc_fx': [(-math.inf, 0), (0, 0.0), (1, 1.0), (2, 0.0), (3, 1.0), (4, 0.0), (5, 0), (math.inf, 0)],
            'epsilon': 0.4,  # Difference is 1.0, so 2*epsilon = 0.8 < 1.0
            'expected_pieces': 2
        },
        # Test case 3: Sawtooth pattern that can be approximated with fewer pieces
        {
            'name': 'sawtooth_pattern',
            'pc_fx': [(-math.inf, 0)] + [(i, 0.1 * (i % 2)) for i in range(10)] + [(10, 0), (math.inf, 0)],
            'epsilon': 0.15,  # Can be approximated with a single piece of 0.05
            'expected_pieces': 1
        },
        # Test case 4: Plateau with a single spike that needs to be handled
        {
            'name': 'plateau_with_spike',
            'pc_fx': [(-math.inf, 0), (0, 1.0), (1, 1.0), (2, 1.8), (3, 1.0), (4, 1.0), (5, 0), (math.inf, 0)],
            'epsilon': 0.5,
            'expected_pieces': 3  # [0,1.5)≈1.0, [1.5,2.5)≈1.4, [2.5,∞)≈1.0
        },
        # Test case 5: Strictly decreasing sequence
        {
            'name': 'decreasing_sequence',
            'pc_fx': [(-math.inf, 0)] + [(i, 10 - i) for i in range(11)] + [(10, 0), (math.inf, 0)],
            'epsilon': 1.0,
            'expected_pieces': 10  # Each adjacent pair differs by 1.0
        },
        # Test case 6: Alternating high and low values
        {
            'name': 'alternating_high_low',
            'pc_fx': [(-math.inf, 0)] + [(i, 1.0 if i % 2 == 0 else 0.0) for i in range(11)] + [(10, 0), (math.inf, 0)],
            'epsilon': 0.6,  # Can be approximated with a single piece of 0.5
            'expected_pieces': 1
        },
        # Test case 7: Single point anomaly in otherwise constant function
        {
            'name': 'single_point_anomaly',
            'pc_fx': [(-math.inf, 0), (0, 1.0), (1, 1.0), (2, 2.5), (3, 1.0), (4, 1.0), (5, 0), (math.inf, 0)],
            'epsilon': 0.8,
            'expected_pieces': 2  # The anomaly at x=2 is 1.5 away from 1.0
        },
        # Test case 8: Gradual increase that can be approximated with fewer pieces
        {
            'name': 'gradual_increase',
            'pc_fx': [(-math.inf, 0)] + [(i, i * 0.1) for i in range(11)] + [(10, 0), (math.inf, 0)],
            'epsilon': 0.2,
            'expected_pieces': 3  # [0,3.33)≈0.15, [3.33,6.66)≈0.5, [6.66,10)≈0.85
        },
        # Test case 9: Mostly flat with small fluctuations
        {
            'name': 'flat_with_fluctuations',
            'pc_fx': [(-math.inf, 0), (0, 0)] + [(i, 1.0 + (hash(str(i)) % 100 - 50) * 0.002) for i in range(1, 11)] + [(10, 0), (math.inf, 0)],
            'epsilon': 0.15,
            'expected_pieces': 1  # Small random fluctuations should be within epsilon
        },
        # Test case 10: Sawtooth with increasing amplitude
        {
            'name': 'sawtooth_increasing_amplitude',
            'pc_fx': [(-math.inf, 0), (0, 0)] + [(i, (i % 2) * (i * 0.2)) for i in range(11)] + [(10, 0), (math.inf, 0)],
            'epsilon': 0.3,
            'expected_pieces': 4  # The amplitude increases, so we'll need more pieces as we go
        }
    ]
#Iteration15
test_cases15 = [
    # Test Case 1: Simple case with 2 pieces that can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 4], [4, float('inf')]],
        "epsilon": 1.0,
        "description": "Two identical pieces that can be merged with epsilon=1.0"
    },

    # Test Case 2: Step function requiring multiple pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Step function requiring multiple pieces with epsilon=0.5"
    },

    # Test Case 3: Single piece (no approximation needed)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 2.0,
        "description": "Single piece input should return single piece"
    },

    # Test Case 4: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, 2], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern with amplitude 2, epsilon=1.0"
    },

    # Test Case 5: Large epsilon that can approximate everything to one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 2.0,
        "description": "All pieces can be approximated by a single value with large epsilon"
    },

    # Test Case 6: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, 10], [5, float('inf')]],
        "epsilon": 5.0,
        "description": "Alternating high and low values with epsilon=5.0"
    },

    # Test Case 7: Gradually increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 0.6,
        "description": "Gradually increasing values with epsilon=0.6"
    },

    # Test Case 8: Single point with large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 100], [1, float('inf')]],
        "epsilon": 50.0,
        "description": "Single point with large epsilon=50.0"
    },

    # Test Case 9: Multiple pieces with same value
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 0.1,
        "description": "Multiple pieces with same value should be merged"
    },

    # Test Case 10: Complex pattern with varying epsilon requirements
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1], [3, 5], [4, 1],
                  [5, 7], [6, 1], [7, 9], [8, 1], [9, float('inf')]],
        "epsilon": 2.0,
        "description": "Complex pattern testing optimal piece merging with epsilon=2.0"
    }
]
#Iteration16
test_cases16 = [
    # Test Case 1: Simple case with one segment
    {
        'name': 'single_segment',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 1
    },

    # Test Case 2: Two segments that can be merged
    {
        'name': 'two_segments_mergeable',
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [3, 2], [6, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 1
    },

    # Test Case 3: Three segments where only two can be merged
    {
        'name': 'three_segments_partial_merge',
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [2, 4], [4, 6], [6, float('inf')]],
        'epsilon': 1.5,
        'expected_pieces': 2
    },

    # Test Case 4: Sawtooth pattern
    {
        'name': 'sawtooth_pattern',
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 0], [1, 2], [2, 0],
                  [3, 2], [4, 0], [5, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 3
    },

    # Test Case 5: Large epsilon that allows complete merge
    {
        'name': 'large_epsilon_complete_merge',
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1],
                  [3, 3], [4, float('inf')]],
        'epsilon': 2.0,
        'expected_pieces': 1
    },

    # Test Case 6: Small epsilon requiring all original segments
    {
        'name': 'small_epsilon_no_merge',
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1],
                  [3, 3], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 4
    },

    # Test Case 7: Single point with large epsilon
    {
        'name': 'single_point_large_epsilon',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        'epsilon': 2.0,
        'expected_pieces': 1
    },

    # Test Case 8: Staircase pattern
    {
        'name': 'staircase_pattern',
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 3],
                  [3, 4], [4, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 3
    },

    # Test 9: Alternating values
    {
        'name': 'alternating_values',
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1],
                  [3, 3], [4, 1], [5, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 2
    },

    # Test 10: Large number of small segments
    {
        'name': 'many_small_segments',
        'pc_fx': [[-float('inf'), float('inf')]] +
                 [[i, 1 + (i % 2)] for i in range(10)] +
                 [[10, float('inf')]],
        'epsilon': 0.6,
        'expected_pieces': 2
    }
]
#Iteration17
test_cases17 = [
    # Test case 1: Simple case with 2 pieces
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1],
            [2, 3],
            [4, float('inf')]
        ],
        'epsilon': 0.5
    },

    # Test case 2: Single piece (no approximation needed)
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 5],
            [10, float('inf')]
        ],
        'epsilon': 1.0
    },

    # Test case 3: Sawtooth pattern
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 1],
            [2, 0],
            [3, 1],
            [4, 0],
            [5, float('inf')]
        ],
        'epsilon': 0.5
    },

    # Test case 4: Step function with varying step sizes
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 2],
            [3, 0],
            [6, 2],
            [10, 0],
            [15, 2],
            [21, float('inf')]
        ],
        'epsilon': 1.0
    },

    # Test case 5: Flat line with a single spike
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 1],
            [2, 5],  # Spike
            [3, 1],
            [4, 1],
            [5, float('inf')]
        ],
        'epsilon': 1.0
    },

    # Test case 6: Alternating high and low values
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 10],
            [1, 0],
            [2, 10],
            [3, 0],
            [4, 10],
            [5, float('inf')]
        ],
        'epsilon': 5.0
    },

    # Test case 7: Large number of small pieces
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            *[[i, i % 3] for i in range(20)],
            [20, float('inf')]
        ],
        'epsilon': 0.1
    },

    # Test case 8: Gradually increasing values
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            *[[i, i] for i in range(10)],
            [10, float('inf')]
        ],
        'epsilon': 1.5
    },

    # Test case 9: Single point with large epsilon
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, float('inf')]
        ],
        'epsilon': 100.0  # Should be able to approximate with 1 piece
    },

    # Test case 10: Challenging case requiring careful merging
    {
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 2],
            [2, 0],
            [3, 1.5],
            [4, 0.5],
            [5, 2],
            [6, 0],
            [7, float('inf')]
        ],
        'epsilon': 1.0
    }
]

#Iteration18
test_cases18 = [
    # Test Case 1: Simple case - no approximation needed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 3], [4, 5], [6, float('inf')]],
        "epsilon": 0.5,
        "description": "No approximation needed - each piece is already within epsilon"
    },

    # Test Case 2: Simple merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 0], [3, float('inf')]],
        "epsilon": 0.1,
        "description": "All pieces can be merged into one"
    },

    # Test Case 3: Alternating values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Alternating values with epsilon allowing some merging"
    },

    # Test Case 4: Staircase function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Staircase function with epsilon=1.0"
    },

    # Test Case 5: Large jump in middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Large jump in the middle that can't be merged"
    },

    # Test Case 6: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, 2], [6, 0],
                  [7, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern with epsilon=1.0"
    },

    # Test Case 7: Single point spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 0], [3, float('inf')]],
        "epsilon": 0.1,
        "description": "Single point spike that requires its own piece"
    },

    # Test Case 8: Very small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0001], [2, 1.0002], [3, 1.0003], [4, float('inf')]],
        "epsilon": 0.00005,
        "description": "Very small epsilon requiring each piece to be separate"
    },

    # Test Case 9: Large epsilon with many pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.1], [2, 0.9], [3, 1.05],
                  [4, 0.95], [5, 1.01], [6, 0.99], [7, 1.0],
                  [8, float('inf')]],
        "epsilon": 0.2,
        "description": "Many small variations that can be merged with larger epsilon"
    },

    # Test Case 10: Edge case with infinite values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, float('inf')],
                  [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Edge case with infinite values in the middle"
    }
]
#Iteration19
test_cases19 = [
    # Test Case 1: Simple case with 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 4], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Simple case with 2 pieces, should require 1 piece"
    },

    # Test Case 2: Staircase pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Staircase pattern, tests piece merging"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, 1], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern, tests alternating heights"
    },

    # Test Case 4: Single point with epsilon = 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.0,
        "description": "Single point with epsilon=0, should require exactly 1 piece"
    },

    # Test Case 5: Large epsilon that can cover everything
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 4], [3, 3], [5, 5], [7, float('inf')]],
        "epsilon": 10.0,
        "description": "Large epsilon that can cover all points with one piece"
    },

    # Test Case 6: Small epsilon requiring all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 0.9], [3, 1.0], [4, float('inf')]],
        "epsilon": 0.01,
        "description": "Small epsilon requiring all original pieces"
    },

    # Test Case 7: Non-monotonic function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 1], [2, 5], [3, 1], [4, 5], [5, float('inf')]],
        "epsilon": 2.0,
        "description": "Non-monotonic function with peaks and valleys"
    },

    # Test Case 8: Large gaps between x-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [100, 2], [200, 1], [300, 2], [400, float('inf')]],
        "epsilon": 0.5,
        "description": "Large gaps between x-values"
    },

    # Test Case 9: All equal values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 0.1,
        "description": "All equal values, should require only 1 piece"
    },

    # Test Case 10: Random-like pattern
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 2], [3, 5], [4, 3], [5, 6], [6, 4],
                  [7, float('inf')]],
        "epsilon": 1.5,
        "description": "Random-like pattern to test general case"
    }
]
#Iteration20
test_cases20 = [
    # Test Case 1: Simple step function - should require 2 pieces
    {
        "name": "Simple step function",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 1], [3, 0], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },

    # Test Case 2: Single piece within epsilon - should return 1 piece
    {
        "name": "Single piece within epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 0.9], [3, 1.05], [4, float('inf')]],
        "epsilon": 0.2,
        "expected_pieces": 1
    },

    # Test Case 3: Sawtooth pattern - requires multiple pieces
    {
        "name": "Sawtooth pattern",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [6, 0],
                  [7, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 4
    },

    # Test Case 4: Large jump - requires at least 2 pieces
    {
        "name": "Large jump",
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 0], [3, 0], [4, float('inf')]],
        "epsilon": 5,
        "expected_pieces": 2
    },

    # Test Case 5: Empty function (edge case)
    {
        "name": "Empty function",
        "pc_fx": [[-float('inf'), float('inf')], [0, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 0
    },

    # Test Case 6: Single point (edge case)
    {
        "name": "Single point",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },

    # Test Case 7: Piece with exact epsilon difference
    {
        "name": "Exact epsilon difference",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1
    },

    # Test Case 8: Multiple jumps with varying epsilon
    {
        "name": "Multiple jumps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 2], [5, 1], [6, 0],
                  [7, float('inf')]],
        "epsilon": 1.5,
        "expected_pieces": 2
    },

    # Test Case 9: Smallest possible non-trivial case
    {
        "name": "Two pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, float('inf')]],
        "epsilon": 0.6,
        "expected_pieces": 1
    },

    # Test Case 10: Large number of pieces with small variations
    {
        "name": "Many small variations",
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1 + 0.1 * (i % 3)] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 0.2,
        "expected_pieces": 4
    }
]
#Iteration21
test_cases21 = [
    # Test Case 1: Simple case with two pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [2, 3],
            [4, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Two distinct pieces with clear separation"
    },

    # Test Case 2: Single piece (should return original)
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Single piece input"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 3], [2, 1], [3, 3],
            [4, 1], [5, 3], [6, 1], [7, 3],
            [8, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Sawtooth pattern testing alternation"
    },

    # Test Case 4: Staircase pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 2], [2, 3], [3, 4],
            [4, 5], [5, 6], [6, 7], [7, 8],
            [8, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Strictly increasing staircase"
    },

    # Test Case 5: Negative values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [-10, -5], [-5, -3], [0, -1],
            [5, 2], [10, 4], [15, 2],
            [20, float('inf')]
        ],
        "epsilon": 2.0,
        "description": "Negative and positive values"
    },

    # Test Case 6: Large epsilon (should merge all pieces)
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 2], [2, 3], [3, 4],
            [4, float('inf')]
        ],
        "epsilon": 10.0,
        "description": "Large epsilon should merge all pieces"
    },

    # Test Case 7: Small epsilon (should keep most pieces)
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.3],
            [4, 1.4], [5, 1.5], [6, 1.6], [7, 1.7],
            [8, float('inf')]
        ],
        "epsilon": 0.05,
        "description": "Small epsilon should keep most pieces"
    },

    # Test Case 8: Alternating large and small jumps
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 10], [2, 2], [3, 11],
            [4, 3], [5, 12], [6, 4], [7, 13],
            [8, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Alternating large and small jumps"
    },

    # Test Case 9: Plateau with small variations
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5], [1, 5.1], [2, 4.9], [3, 5.2],
            [4, 4.8], [5, 5.3], [6, 4.7], [7, 5.4],
            [10, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Plateau with small variations"
    },

    # Test Case 10: Non-uniform x-intervals
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [0.1, 2], [0.2, 3], [0.5, 2],
            [1.0, 1], [2.0, 4], [3.5, 2], [5.5, 3],
            [10.0, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Non-uniform x-intervals"
    }
]
#Iteration22
test_cases22 = [
    # Test Case 1: Simple case with 3 pieces, should be reducible to 2 pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2],
            [2, 4],
            [4, 2],
            [6, float('inf')]
        ],
        "epsilon": 1.5
    },

    # Test Case 2: All pieces within epsilon, should be reducible to 1 piece
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10],
            [1, 10.5],
            [2, 9.8],
            [3, 10.2],
            [4, float('inf')]
        ],
        "epsilon": 1.0
    },

    # Test Case 3: No possible reduction, each piece is necessary
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 2],
            [2, 0],
            [3, 2],
            [4, float('inf')]
        ],
        "epsilon": 0.5
    },

    # Test Case 4: Staircase pattern with alternating heights
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 3],
            [2, 1],
            [3, 3],
            [4, 1],
            [5, 3],
            [6, float('inf')]
        ],
        "epsilon": 1.0
    },

    # Test Case 5: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 1],
            [2, 0],
            [3, 1],
            [4, 0],
            [5, 1],
            [6, 0],
            [7, float('inf')]
        ],
        "epsilon": 0.6
    },

    # Test Case 6: Large epsilon, should collapse to minimal pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, 5],
            [5, 6],
            [6, float('inf')]
        ],
        "epsilon": 5.0
    },

    # Test Case 7: Small epsilon, no reduction possible
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 0.1],
            [2, 0.2],
            [3, 0.3],
            [4, 0.4],
            [5, float('inf')]
        ],
        "epsilon": 0.05
    },

    # Test Case 8: Large jumps, should require all pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 10],
            [2, 0],
            [3, 10],
            [4, 0],
            [5, 10],
            [6, float('inf')]
        ],
        "epsilon": 4.9
    },

    # Test Case 9: Single piece edge case
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5],
            [10, float('inf')]
        ],
        "epsilon": 1.0
    },

    # Test Case 10: Complex pattern with varying segment lengths
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2],
            [1, 2.5],  # Can be merged with first segment
            [3, 7],  # Large jump, must be new segment
            [5, 7.2],  # Can be merged with previous
            [7, 7.1],  # Can be merged with previous
            [10, 4],  # Large drop, must be new segment
            [12, 4.1],  # Can be merged with previous
            [15, float('inf')]
        ],
        "epsilon": 0.6
    }
]
#Iteration23
test_cases23 = [
    # Test Case 1: Simple case with exact fit
    {
        'name': 'exact_fit',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 2],
            [2, 4],
            [4, 6],
            [6, float('inf')]
        ],
        'epsilon': 2.0,  # Should return original function
        'expected_pieces': 3
    },

    # Test Case 2: Single piece within epsilon
    {
        'name': 'single_piece_within_epsilon',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1.5],
            [1, 2.5],
            [2, 1.8],
            [3, 2.2],
            [4, float('inf')]
        ],
        'epsilon': 1.0,  # All points within 1.0 of 2.0
        'expected_pieces': 1
    },

    # Test Case 3: Step function with varying step heights
    {
        'name': 'varying_step_heights',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 2],
            [2, 4],
            [3, 2],
            [4, 0],
            [5, float('inf')]
        ],
        'epsilon': 1.0,  # Should need at least 3 pieces
        'expected_pieces': 3
    },

    # Test Case 4: Sawtooth pattern
    {
        'name': 'sawtooth_pattern',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 3],
            [2, 1],
            [3, 3],
            [4, 1],
            [5, float('inf')]
        ],
        'epsilon': 1.5,  # Can be approximated with 1 piece
        'expected_pieces': 1
    },

    # Test Case 5: Large jump that requires a new piece
    {
        'name': 'large_jump',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 1],
            [2, 1],
            [3, 5],  # Large jump here
            [4, 5],
            [5, float('inf')]
        ],
        'epsilon': 2.0,  # Needs at least 2 pieces
        'expected_pieces': 2
    },

    # Test Case 6: Small oscillations around a central value
    {
        'name': 'small_oscillations',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1.1],
            [1, 0.9],
            [2, 1.05],
            [3, 0.95],
            [4, 1.01],
            [5, 0.99],
            [6, float('inf')]
        ],
        'epsilon': 0.15,  # Can be approximated with 1 piece
        'expected_pieces': 1
    },

    # Test Case 7: Multiple large jumps
    {
        'name': 'multiple_large_jumps',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 1],  # First segment
            [2, 5],  # First jump
            [3, 5],
            [4, 1],  # Second jump
            [5, 1],
            [6, 4],  # Third jump
            [7, float('inf')]
        ],
        'epsilon': 1.5,  # Needs at least 4 pieces
        'expected_pieces': 4
    },

    # Test Case 8: Edge case with minimum number of pieces
    {
        'name': 'minimal_case',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 2],
            [2, float('inf')]
        ],
        'epsilon': 1.0,  # Can be 1 piece
        'expected_pieces': 1
    },

    # Test Case 9: Large value range
    {
        'name': 'large_value_range',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0, 1000],
            [1, 100],
            [2, 1000],
            [3, 100],
            [4, 1000],
            [5, float('inf')]
        ],
        'epsilon': 500,  # Needs at least 2 pieces
        'expected_pieces': 2
    },

    # Test Case 10: Non-integer x-values
    {
        'name': 'non_integer_x_values',
        'pc_fx': [
            [-float('inf'), float('inf')],
            [0.0, 1.0],
            [0.5, 1.5],
            [1.5, 2.0],
            [2.0, 1.0],
            [2.5, 1.5],
            [3.0, float('inf')]
        ],
        'epsilon': 0.6,  # Needs at least 2 pieces
        'expected_pieces': 2
    }
]
#Iteration24
test_cases24 = [
    # Test case 1
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    },
    # Test case 2
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [10, 1], [20, 1], [30, float('inf')]],
        "epsilon": 0.5
    },
    # Test case 3
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, 1], [5, 3], [6, 1], [7, 3], [8, float('inf')]],
        "epsilon": 1.0
    },
    # Test case 4
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 2], [3, 2], [4, 4], [5, 4], [6, 0], [7, 0], [8, float('inf')]],
        "epsilon": 1.0
    },
    # Test case 5
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 0.9], [3, 1.1], [4, 0.9], [5, 1.1], [6, 0.9], [7, 1.1], [8, float('inf')]],
        "epsilon": 0.05
    },
    # Test case 6
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 4], [3, 2], [4, 0], [5, 2], [6, 4], [7, 2], [8, float('inf')]],
        "epsilon": 2.1
    },
    # Test case 7
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [10, 5], [11, 6], [100, 7], [101, 3], [200, 3], [201, 2], [300, float('inf')]],
        "epsilon": 1.5
    },
    # Test case 8
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, 0], [3, 100], [4, 0], [5, 100], [6, 0], [7, 100], [8, float('inf')]],
        "epsilon": 50.0
    },
    # Test case 9
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0
    },
    # Test case 10
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 5], [4, 0], [5, 2.5], [6, 0], [7, 1.25], [8, float('inf')]],
        "epsilon": 2.0
    }
]
#Iteration25
test_cases25 = [
    # Test Case 1: Simple case with no approximation needed
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1],
                  [2, 3],
                  [4, 5],
                  [6, float('inf')]],
        "epsilon": 1.0,
        "description": "No approximation needed - all pieces can be preserved"
    },

    # Test Case 2: Simple merge of two pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1],
                  [1, 1.5],
                  [2, float('inf')]],
        "epsilon": 1.0,
        "description": "Simple merge of two pieces with small difference"
    },

    # Test Case 3: Edge case with single piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1],
                  [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece - should remain unchanged"
    },

    # Test Case 4: Large jump requiring multiple pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1],
                  [1, 5],
                  [2, 1],
                  [3, 5],
                  [4, float('inf')]],
        "epsilon": 2.0,
        "description": "Large jumps requiring multiple pieces"
    },

    # Test Case 5: Small oscillations within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0],
                  [1, 1.1],
                  [2, 0.9],
                  [3, 1.05],
                  [4, float('inf')]],
        "epsilon": 0.2,
        "description": "Small oscillations within epsilon tolerance"
    },

    # Test Case 6: Large number of pieces with varying differences
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [1, 0.8],
                  [2, 0.2],
                  [3, 0.7],
                  [4, 0.3],
                  [5, 0.6],
                  [6, 0.4],
                  [7, 0.5],
                  [8, float('inf')]],
        "epsilon": 0.5,
        "description": "Many pieces with varying differences"
    },

    # Test Case 7: Edge case with epsilon = 0
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1],
                  [1, 2],
                  [2, 1],
                  [3, float('inf')]],
        "epsilon": 0.0,
        "description": "Epsilon = 0, no approximation allowed"
    },

    # Test Case 8: Large epsilon that allows complete merging
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1],
                  [1, 2],
                  [2, 3],
                  [3, 4],
                  [4, float('inf')]],
        "epsilon": 10.0,
        "description": "Large epsilon allowing complete merging"
    },

    # Test Case 9: Non-integer x-values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.1, 1.5],
                  [1.5, 2.5],
                  [2.5, 1.5],
                  [3.5, float('inf')]],
        "epsilon": 1.0,
        "description": "Non-integer x-values"
    },

    # Test Case 10: Large range of y-values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1000],
                  [1, 10],
                  [2, 2000],
                  [3, 20],
                  [4, float('inf')]],
        "epsilon": 500.0,
        "description": "Large range of y-values"
    }
]
#Iteration26
test_cases26 = [
    # Test Case 1: Simple case with 2 pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2],
            [3, 5],
            [6, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Simple case with 2 pieces, should require 1 piece with epsilon=1.0"
    },

    # Test Case 2: Single piece (already optimal)
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10],
            [10, float('inf')]
        ],
        "epsilon": 2.0,
        "description": "Single piece input, should remain as 1 piece"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 3], [2, 1], [3, 3], [4, 1],
            [5, 3], [6, 1], [7, 3], [8, 1], [9, 3],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Sawtooth pattern, should be able to approximate with 1 piece"
    },

    # Test Case 4: Staircase pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
            [5, 6], [6, 7], [7, 8], [8, 9], [9, 10],
            [10, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Staircase pattern with small epsilon, should require multiple pieces"
    },

    # Test Case 5: Large jump in the middle
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 1], [2, 1], [3, 100], [4, 1],
            [5, 1], [6, 1], [7, 1], [8, 1], [9, 1],
            [10, float('inf')]
        ],
        "epsilon": 2.0,
        "description": "Single large jump in the middle, should require at least 3 pieces"
    },

    # Test Case 6: Very small epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.3], [4, 1.4],
            [5, 1.5], [6, 1.6], [7, 1.7], [8, 1.8], [9, 1.9],
            [10, float('inf')]
        ],
        "epsilon": 0.05,
        "description": "Very small epsilon, should require many pieces or exact representation"
    },

    # Test Case 7: Large epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1], [1, 100], [2, 1], [3, 100], [4, 1],
            [5, 100], [6, 1], [7, 100], [8, 1], [9, 100],
            [10, float('inf')]
        ],
        "epsilon": 50,
        "description": "Large epsilon, should be able to approximate with 1 piece"
    },

    # Test Case 8: Non-uniform x-spacing
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2], [0.1, 3], [0.2, 4], [10, 1], [20, 5],
            [30, 3], [40, 4], [100, 2], [200, 3], [1000, 1],
            [float('inf'), float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Non-uniform x-spacing, tests handling of varying interval lengths"
    },

    # Test Case 9: Edge case with minimum number of pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, float('inf')]
        ],
        "epsilon": 0.0,
        "description": "Minimum non-trivial case, should require 1 piece if epsilon ≥ 0"
    },

    # Test Case 10: Challenge case with varying frequency
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0], [1, 2], [2, 0], [3, 2], [4, 0],  # High frequency
            [5, 0], [6, 0], [7, 0], [8, 0], [9, 0],  # Low frequency
            [10, 10], [11, 0], [12, 10], [13, 0], [14, 10],  # High frequency
            [15, 5], [16, 5], [17, 5], [18, 5], [19, 5],  # Medium frequency
            [20, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Mixed frequency pattern to test algorithm's ability to find optimal segments"
    }
]
#Iteration27
test_cases27 = [
    # Test Case 1: Simple case that requires no approximation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2], [4, 2], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Constant function - should return original function"
    },

    # Test Case 2: Simple case with two pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [3, 5], [6, float('inf')]],
        "epsilon": 2.0,
        "description": "Two pieces within epsilon - can be approximated with one piece"
    },

    # Test Case 3: Example from the problem description
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75,
        "description": "Example from problem description - tests basic functionality"
    },

    # Test Case 4: Requires multiple pieces with varying epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 1], [3, 4], [4, 1], [5, 4], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Oscillating function - tests alternation handling"
    },

    # Test Case 5: Edge case with single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 10.0,
        "description": "Single piece - should return original function"
    },

    # Test Case 6: Large epsilon that can approximate everything to one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, 1], [5, 10], [6, float('inf')]],
        "epsilon": 5.0,
        "description": "Large epsilon - should approximate to one piece"
    },

    # Test Case 7: Small epsilon requiring all original pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1], [3, 1.1], [4, 1], [5, 1.1],
                  [6, float('inf')]],
        "epsilon": 0.01,
        "description": "Tiny epsilon - should keep all original pieces"
    },

    # Test Case 8: Non-uniform x-spacing
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [10, 2], [12, 5], [20, 3], [100, 4], [200, float('inf')]],
        "epsilon": 1.0,
        "description": "Non-uniform x-spacing - tests handling of varying intervals"
    },

    # Test Case 9: Large number of pieces
    {
        "pc_fx": [[-float('inf'), float('inf')]] + [[i, i % 3 + 1] for i in range(100)] + [[100, float('inf')]],
        "epsilon": 1.5,
        "description": "Large number of pieces - tests performance and correctness"
    },

    # Test Case 10: Edge case with negative infinity to infinity
    {
        "pc_fx": [[-float('inf'), float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece from -inf to inf - should return original function"
    }
]
#Iteration28
test_cases28 = [
    # Test Case 1: Simple case with 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 4], [4, float('inf')]],
        "epsilon": 1.0,
        "description": "Simple case with 2 pieces, should be merged with ε=1.0"
    },

    # Test Case 2: No possible merging (already minimal)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 5], [3, 1], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "No possible merging with ε=0.5"
    },

    # Test Case 3: All pieces can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 1.9], [3, float('inf')]],
        "epsilon": 0.2,
        "description": "All pieces can be merged with ε=0.2"
    },

    # Test Case 4: Edge case with single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 2.0,
        "description": "Single piece input (already minimal)"
    },

    # Test Case 5: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1],
                  [3, 3], [4, 1], [5, 3],
                  [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern, should be merged to 2 pieces with ε=1.0"
    },

    # Test Case 6: Large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 10], [2, 1],
                  [3, 10], [4, 1], [5, 10],
                  [6, float('inf')]],
        "epsilon": 5.0,
        "description": "Large epsilon that can merge all pieces"
    },

    # Test Case 7: Small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.05], [2, 0.98],
                  [3, 1.02], [4, 0.99], [5, 1.01],
                  [6, float('inf')]],
        "epsilon": 0.02,
        "description": "Small epsilon, should keep most pieces"
    },

    # Test Case 8: Non-uniform x intervals
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 3], [4, 2],
                  [5, 4], [8, 3], [10, 5],
                  [15, float('inf')]],
        "epsilon": 1.0,
        "description": "Non-uniform x intervals, should merge some pieces"
    },

    # Test Case 9: Large value range
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1000], [1, 1100], [2, 900],
                  [3, 1050], [4, 950], [5, 1025],
                  [6, float('inf')]],
        "epsilon": 100,
        "description": "Large value range, test numerical stability"
    },

    # Test Case 10: Minimal change between pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0 + 1e-10], [2, 1.0 - 1e-10],
                  [3, 1.0 + 2e-10], [4, 1.0 - 2e-10], [5, 1.0 + 3e-10],
                  [6, float('inf')]],
        "epsilon": 1e-9,
        "description": "Minimal changes between pieces, testing floating-point precision"
    }
]
#Iteration29
test_cases29 = [
    # Test Case 1: Simple case with 2 optimal pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 1],
            [2, 3],
            [3, 3],
            [4, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Simple case with 2 optimal pieces"
    },

    # Test Case 2: Single piece is sufficient
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2],
            [1, 2.1],
            [2, 1.9],
            [3, 2.05],
            [4, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Single piece is sufficient within epsilon"
    },

    # Test Case 3: Requires all pieces (no approximation possible)
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 3],
            [2, 1],
            [3, 3],
            [4, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "No approximation possible, requires all pieces"
    },

    # Test Case 4: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 3],
            [2, 1],
            [3, 3],
            [4, 1],
            [5, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Sawtooth pattern with varying epsilon"
    },

    # Test Case 5: Large epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 5],
            [2, 9],
            [3, 5],
            [4, 1],
            [5, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Large epsilon allows single piece approximation"
    },

    # Test Case 6: Small epsilon requires all pieces
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0],
            [1, 1.1],
            [2, 1.05],
            [3, 1.0],
            [4, float('inf')]
        ],
        "epsilon": 0.01,
        "description": "Small epsilon requires all pieces"
    },

    # Test Case 7: Non-integer x values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 1.0],
            [0.5, 2.0],
            [1.5, 2.0],
            [2.0, 1.0],
            [3.0, float('inf')]
        ],
        "epsilon": 0.75,
        "description": "Non-integer x-values"
    },

    # Test Case 8: Single segment input
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Single segment input"
    },

    # Test Case 9: Large number of pieces
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1 + 0.1 * ((-1) ** i)] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 0.2,
        "description": "Oscillating pattern with many pieces"
    },

    # Test Case 10: Your provided example
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2],
            [1, 3],
            [3, 7],
            [6, 5],
            [7, float('inf')]
        ],
        "epsilon": 0.75,
        "description": "Provided example test case"
    }
]

#Iteration30
test_cases30 = [
    # Test Case 1: Simple case with one optimal piece
    {
        "name": "Single optimal piece",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5],
            [5, 5],
            [10, float('inf')]
        ],
        "epsilon": 1.0
    },

    # Test Case 2: Two pieces with clear separation
    {
        "name": "Two clear pieces",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [5, 6],
            [10, float('inf')]
        ],
        "epsilon": 0.5
    },

    # Test Case 3: Alternating values within epsilon
    {
        "name": "Alternating values within epsilon",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0],
            [1, 0.9],
            [2, 1.1],
            [3, 0.95],
            [4, 1.05],
            [5, float('inf')]
        ],
        "epsilon": 0.2
    },

    # Test Case 4: Sawtooth pattern
    {
        "name": "Sawtooth pattern",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0],
            [1, 1],
            [2, 0],
            [3, 1],
            [4, 0],
            [5, 1],
            [6, float('inf')]
        ],
        "epsilon": 1.0
    },

    # Test Case 5: Large jump in values
    {
        "name": "Large jump",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 100],
            [2, 1],
            [3, float('inf')]
        ],
        "epsilon": 0.5
    },

    # Test Case 6: Multiple possible solutions
    {
        "name": "Multiple possible solutions",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1],
            [1, 2],
            [2, 1],
            [3, 2],
            [4, 1],
            [5, 2],
            [6, float('inf')]
        ],
        "epsilon": 1.0
    },

    # Test Case 7: Single point with large epsilon
    {
        "name": "Single point with large epsilon",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 5],
            [1, float('inf')]
        ],
        "epsilon": 10.0
    },

    # Test Case 8: Very small epsilon
    {
        "name": "Very small epsilon",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0],
            [1, 1.0001],
            [2, 0.9999],
            [3, 1.0],
            [4, float('inf')]
        ],
        "epsilon": 0.00001
    },

    # Test Case 9: Large number of pieces
    {
        "name": "Large number of pieces",
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1 + 0.1 * (i % 3)] for i in range(100)] +
                 [[100, float('inf')]],
        "epsilon": 0.25
    },

    # Test Case 10: Given example
    {
        "name": "Provided example",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 2],
            [1, 3],
            [3, 7],
            [6, 5],
            [7, float('inf')]
        ],
        "epsilon": 0.75
    }
]

