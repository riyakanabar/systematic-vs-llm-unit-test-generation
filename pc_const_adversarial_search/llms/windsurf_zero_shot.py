#17 Sept 2:02 PM
#Iteration1
test_cases1 = [
    # Test Case 1: Single piece (minimum case)
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [10, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Single piece function should require exactly 1 piece for any epsilon >= 0"
    },

    # Test Case 2: Two pieces with exact fit
    {
        "name": "two_pieces_exact",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0],
            [5, 2.0],
            [10, float('inf')]
        ],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Two pieces with exact fit should require exactly 2 pieces"
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth_pattern",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 3.0], [2, 1.0], [3, 3.0], [4, 1.0],
            [5, 3.0], [6, 1.0], [7, 3.0], [8, 1.0], [9, 3.0],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "expected_min_pieces": 5,
        "description": "Sawtooth pattern with alternating heights"
    },

    # Test Case 4: Single spike
    {
        "name": "single_spike",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [4, 10.0], [6, 1.0],
            [10, float('inf')]
        ],
        "epsilon": 2.0,
        "expected_min_pieces": 3,
        "description": "Single spike that requires 3 pieces to approximate within epsilon"
    },

    # Test Case 5: Staircase function
    {
        "name": "staircase",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 2.0], [2, 3.0], [3, 4.0], [4, 5.0],
            [5, 6.0], [6, 7.0], [7, 8.0], [8, 9.0], [9, 10.0],
            [10, float('inf')]
        ],
        "epsilon": 0.6,
        "expected_min_pieces": 5,
        "description": "Staircase function with unit steps"
    },

    # Test Case 6: High frequency oscillation
    {
        "name": "high_freq_oscillation",
        "pc_fx": [
            [-float('inf'), float('inf')],
            *[[i, 1.0 + 0.1 * (i % 2)] for i in range(21)],
            [20, float('inf')]
        ],
        "epsilon": 0.05,
        "expected_min_pieces": 11,
        "description": "High frequency oscillation requiring many pieces"
    },

    # Test Case 7: Large epsilon
    {
        "name": "large_epsilon",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 1.5], [2, 2.0], [3, 2.5], [4, 3.0],
            [5, 3.5], [6, 4.0], [7, 4.5], [8, 5.0], [9, 5.5],
            [10, float('inf')]
        ],
        "epsilon": 10.0,
        "expected_min_pieces": 1,
        "description": "Large epsilon should allow single piece approximation"
    },

    # Test Case 8: Non-uniform intervals
    {
        "name": "non_uniform_intervals",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [0.1, 2.0], [0.3, 1.0], [1.0, 3.0], [10.0, 1.0],
            [10.5, 3.0], [10.6, 1.0], [11.0, 3.0], [20.0, 1.0],
            [100.0, float('inf')]
        ],
        "epsilon": 0.5,
        "expected_min_pieces": 4,
        "description": "Non-uniform x-intervals with varying piece lengths"
    },

    # Test Case 9: Edge case with minimal epsilon
    {
        "name": "minimal_epsilon",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 1.0 + 1e-10], [2, 1.0], [3, 1.0 + 1e-10], [4, 1.0],
            [5, float('inf')]
        ],
        "epsilon": 1e-11,
        "expected_min_pieces": 3,
        "description": "Minimal epsilon requiring exact approximation"
    },

    # Test Case 10: Random-like pattern
    {
        "name": "random_pattern",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0], [1, 1.8], [2, 0.9], [3, 1.6], [4, 1.1],
            [5, 1.9], [6, 0.8], [7, 1.7], [8, 1.0], [9, 1.5],
            [10, float('inf')]
        ],
        "epsilon": 0.4,
        "expected_min_pieces": 4,
        "description": "Random-like pattern testing general case"
    }
]
#Iteration2
import math
test_cases2 = [
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
        'pc_fx': [(-math.inf, 0), (0, 0)] + [(i, 1.0 + (hash(str(i)) % 100 - 50) * 0.002) for i in range(1, 11)] + [
            (10, 0), (math.inf, 0)],
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
#Iteration3
test_cases3 = [
    {
        "name": "single_piece_constant",
        "pc_fx": [(-float('inf'), 0), (0, 1.0), (1.0, 0)],
        "epsilon": 0.1,
        "expected_min_pieces": 1
    },
    {
        "name": "two_pieces_exact_fit",
        "pc_fx": [(-float('inf'), 0), (0, 1.0), (1.0, 2.0), (2.0, 0)],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },
    {
        "name": "sawtooth_pattern",
        "pc_fx": [(-float('inf'), 0),
                 (0, 1.0), (1.0, 0.5), (2.0, 1.0),
                 (3.0, 0.5), (4.0, 1.0), (5.0, 0)],
        "epsilon": 0.6,
        "expected_min_pieces": 3
    },
    {
        "name": "step_function_with_noise",
        "pc_fx": [(-float('inf'), 0)] +
                [(i, 1.0 + 0.1 * (i % 3)) for i in range(10)] +
                [(10, 0)],
        "epsilon": 0.15,
        "expected_min_pieces": 1
    },
    {
        "name": "large_gap_requiring_multiple_pieces",
        "pc_fx": [(-float('inf'), 0),
                 (0, 0), (1, 10), (2, 0),
                 (3, 10), (4, 0), (5, 0)],
        "epsilon": 5.0,
        "expected_min_pieces": 2
    },
    {
        "name": "empty_function",
        "pc_fx": [(-float('inf'), 0), (0, 0)],
        "epsilon": 1.0,
        "expected_min_pieces": 0
    },
    {
        "name": "single_point",
        "pc_fx": [(-float('inf'), 0), (0, 1.0), (1.0, 0)],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },
    {
        "name": "large_epsilon",
        "pc_fx": [(-float('inf'), 0)] +
                [(i, i % 5) for i in range(20)] +
                [(20, 0)],
        "epsilon": 4.0,
        "expected_min_pieces": 1
    },
    {
        "name": "small_epsilon_requiring_many_pieces",
        "pc_fx": [(-float('inf'), 0)] +
                [(i, 1.0 if i % 2 == 0 else 0.0) for i in range(10)] +
                [(10, 0)],
        "epsilon": 0.1,
        "expected_min_pieces": 10
    },
    {
        "name": "non_uniform_x_spacing",
        "pc_fx": [(-float('inf'), 0),
                 (0, 1.0), (0.1, 1.0), (0.2, 1.0),  # Dense region
                 (1.0, 2.0), (2.0, 2.0),            # Sparse region
                 (10.0, 1.0), (10.1, 1.0),          # Dense region
                 (11.0, 0)],
        "epsilon": 0.5,
        "expected_min_pieces": 3
    }
]
#Iteration4
test_cases4 = [
    # Test Case 1: Simple single piece
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [1.0, 5.0], [2.0, 5.0], [3.0, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 2: Two pieces with exact fit
    {
        "name": "two_pieces_exact",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [1.0, 1.0], [2.0, 1.0],  # First piece
            [2.0, 2.0], [3.0, float('inf')]  # Second piece
        ],
        "epsilon": 0.0
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 0.0], [1.0, 1.0],  # Up
            [1.0, 0.0], [2.0, 1.0],  # Down
            [2.0, 0.0], [3.0, 1.0],  # Up
            [3.0, 0.0], [4.0, float('inf')]  # Down
        ],
        "epsilon": 0.5
    },

    # Test Case 4: Step function with varying step sizes
    {
        "name": "varying_step_sizes",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 1.0], [1.0, 1.0],  # Step 1
            [1.0, 2.0], [1.5, 2.0],  # Step 2
            [1.5, 3.0], [2.0, 3.0],  # Step 3
            [2.0, 1.0], [3.0, float('inf')]  # Step 4
        ],
        "epsilon": 0.25
    },

    # Test Case 5: Small epsilon requiring many pieces
    {
        "name": "small_epsilon",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 0.0], [0.5, 0.1], [1.0, 0.2], [1.5, 0.3],
            [2.0, 0.4], [2.5, 0.5], [3.0, 0.4], [3.5, 0.3],
            [4.0, 0.2], [4.5, 0.1], [5.0, 0.0], [5.5, float('inf')]
        ],
        "epsilon": 0.05
    },

    # Test Case 6: Large epsilon allowing few pieces
    {
        "name": "large_epsilon",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 0.0], [0.5, 0.9], [1.0, 0.1], [1.5, 0.8],
            [2.0, 0.2], [2.5, 0.7], [3.0, 0.3], [3.5, 0.6],
            [4.0, 0.4], [4.5, 0.5], [5.0, 0.0], [5.5, float('inf')]
        ],
        "epsilon": 1.0
    },

    # Test Case 7: Empty function (edge case)
    {
        "name": "empty_function",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [0.0, float('inf')]],
        "epsilon": 0.1
    },

    # Test Case 8: Single point (edge case)
    {
        "name": "single_point",
        "pc_fx": [[-float('inf'), float('inf')], [1.0, 1.0], [1.0, float('inf')]],
        "epsilon": 0.1
    },

    # Test Case 9: Piece with zero width (should be handled gracefully)
    {
        "name": "zero_width_piece",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [1.0, 1.0], [1.0, 2.0],  # Zero-width piece
            [1.0, 3.0], [2.0, 3.0],  # Normal piece
            [2.0, float('inf')]
        ],
        "epsilon": 0.5
    },

    # Test Case 10: Large numbers and floating point precision
    {
        "name": "large_numbers",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [1e6, 1.0], [1e6 + 1, 1.0],  # First piece
            [1e6 + 1, 2.0], [1e6 + 2, 2.0],  # Second piece
            [1e6 + 2, 3.0], [1e6 + 3, 3.0],  # Third piece
            [1e6 + 3, float('inf')]
        ],
        "epsilon": 0.1
    }
]
#Iteration5
test_cases5 = [
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
#Iteration6
test_cases6 = [
    # Test Case 1: Single piece (minimum case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece function should always be optimal"
    },

    # Test Case 2: Two pieces with clear separation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, float('inf')]],
        "epsilon": 0.4,
        "description": "Two clearly separated pieces that can't be merged"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 0.0],
                  [2, 1.0], [3, 0.0],
                  [4, 1.0], [5, float('inf')]],
        "epsilon": 0.6,
        "description": "Sawtooth pattern testing alternation"
    },

    # Test Case 4: Plateau with small perturbations
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.1], [2, 0.9],
                  [3, 1.0], [4, 1.1], [5, 0.9],
                  [6, 1.0], [7, float('inf')]],
        "epsilon": 0.15,
        "description": "Plateau with small perturbations within epsilon"
    },

    # Test Case 5: Step function
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 2.0],
                  [3, 3.0], [4, 4.0], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Step function with equal intervals"
    },

    # Test Case 6: Large jump in middle
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0], [2, 1.0],
                  [3, 10.0], [4, 1.0], [5, 1.0],
                  [6, 1.0], [7, float('inf')]],
        "epsilon": 1.0,
        "description": "Single large jump in middle of constant regions"
    },

    # Test Case 7: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10.0], [1, 0.0], [2, 10.0],
                  [3, 0.0], [4, 10.0], [5, 0.0],
                  [6, 10.0], [7, float('inf')]],
        "epsilon": 5.0,
        "description": "Alternating high and low values"
    },

    # Test Case 8: Single outlier
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0], [2, 1.0],
                  [3, 5.0],  # Single outlier
                  [4, 1.0], [5, 1.0], [6, 1.0],
                  [7, float('inf')]],
        "epsilon": 1.0,
        "description": "Single outlier in otherwise constant function"
    },

    # Test Case 9: Gradually increasing function
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.2], [2, 0.4],
                  [3, 0.6], [4, 0.8], [5, 1.0],
                  [6, 1.2], [7, float('inf')]],
        "epsilon": 0.3,
        "description": "Gradually increasing function"
    },

    # Test Case 10: Random-looking pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.2], [1, 0.8], [2, 1.5],
                  [3, 0.5], [4, 1.8], [5, 0.2],
                  [6, 2.0], [7, float('inf')]],
        "epsilon": 0.6,
        "description": "Random-looking pattern testing general case"
    }
]
#Iteration7
test_cases7 = [
    # Test Case 1: Single piece (already optimal)
    {
        'pc_fx': [[-float('inf'), 0], [1, 2, 3, 4], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece - already optimal'
    },

    # Test Case 2: Two pieces with clear separation
    {
        'pc_fx': [[-float('inf'), 0], [1, 2, 3, 4, 5, 6], [7, float('inf')]],
        'epsilon': 0.5,
        'description': 'Two clearly separated pieces'
    },

    # Test Case 3: Multiple pieces with varying heights
    {
        'pc_fx': [[-float('inf'), 0],
                  [1, 5, 2, 4, 3, 5, 4, 6, 5, 7],
                  [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Multiple pieces with varying heights'
    },

    # Test Case 4: Sawtooth pattern
    {
        'pc_fx': [[-float('inf'), 0],
                  [1, 1, 2, 3, 3, 1, 4, 3, 5, 1, 6, 3],
                  [7, float('inf')]],
        'epsilon': 1.0,
        'description': 'Sawtooth pattern with period 2'
    },

    # Test Case 5: Large jump in the middle
    {
        'pc_fx': [[-float('inf'), 0],
                  [1, 1, 2, 1, 3, 1, 4, 10, 5, 1, 6, 1],
                  [7, float('inf')]],
        'epsilon': 0.5,
        'description': 'Large jump in the middle of the function'
    },

    # Test Case 6: Very small epsilon
    {
        'pc_fx': [[-float('inf'), 0],
                  [1, 1.0, 2, 1.01, 3, 1.02, 4, 1.01, 5, 1.0],
                  [6, float('inf')]],
        'epsilon': 0.005,
        'description': 'Very small epsilon requiring many pieces'
    },

    # Test Case 7: Non-monotonic function
    {
        'pc_fx': [[-float('inf'), 0],
                  [1, 1, 2, 3, 3, 2, 4, 4, 5, 3, 6, 5],
                  [7, float('inf')]],
        'epsilon': 0.75,
        'description': 'Non-monotonic function with local extrema'
    },

    # Test Case 8: Large number of pieces
    {
        'pc_fx': [[-float('inf'), 0]] +
                 [[i, i % 3] for i in range(1, 21)] +
                 [[21, float('inf')]],
        'epsilon': 0.5,
        'description': 'Large number of pieces with repeating pattern'
    },

    # Test Case 9: Piece with zero width (should be handled gracefully)
    {
        'pc_fx': [[-float('inf'), 0],
                  [1, 2, 1, 3, 2, 4, 3, 4],  # Note: x=1 appears twice
                  [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Piece with zero width (x coordinates equal)'
    },

    # Test Case 10: Large epsilon that allows single-piece approximation
    {
        'pc_fx': [[-float('inf'), 0],
                  [1, 1, 2, 5, 3, 2, 4, 6, 5, 3],
                  [6, float('inf')]],
        'epsilon': 3.0,
        'description': 'Large epsilon allowing single-piece approximation'
    }
]
#Iteration8
test_cases8 = [
    # Test Case 1: Simple single piece (should require exactly 1 piece)
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 1.0], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },

    # Test Case 2: Two clearly distinct steps
    {
        "name": "two_steps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.0], [2, 2.0], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0],
                  [4, 0.0], [5, 1.0], [6, 0.0], [7, 1.0],
                  [8, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 4
    },

    # Test Case 4: Single outlier point
    {
        "name": "single_outlier",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.0], [2, 5.0], [3, 0.0],
                  [4, 0.0], [5, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 3
    },

    # Test Case 5: Gradually increasing values
    {
        "name": "gradual_increase",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.5], [2, 1.0], [3, 1.5],
                  [4, 2.0], [5, 2.5], [6, 3.0], [7, 3.5],
                  [8, 4.0], [9, 4.5], [10, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 4
    },

    # Test Case 6: Large jump in the middle
    {
        "name": "large_jump",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [4, 0.0], [5, 10.0], [9, 10.0],
                  [10, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2
    },

    # Test Case 7: Alternating between three values
    {
        "name": "three_value_alternation",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0],
                  [4, 4.0], [5, 2.0], [6, 4.0], [7, 2.0],
                  [8, 0.0], [9, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 3
    },

    # Test Case 8: Small fluctuations around zero
    {
        "name": "small_fluctuations",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -0.1], [1, 0.1], [2, -0.1], [3, 0.1],
                  [4, -0.1], [5, 0.1], [6, -0.1], [7, 0.1],
                  [8, -0.1], [9, 0.1], [10, float('inf')]],
        "epsilon": 0.2,
        "expected_min_pieces": 1
    },

    # Test Case 9: Step function with varying step sizes
    {
        "name": "varying_step_sizes",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.0], [2, 1.0], [4, 1.0],
                  [5, 0.0], [7, 0.0], [8, 1.0], [11, 1.0],
                  [12, 0.0], [16, 0.0], [17, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 3
    },

    # Test Case 10: Challenging case requiring careful piece placement
    {
        "name": "challenging_placement",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 1.0], [3, 0.0],
                  [4, 1.0], [5, 2.0], [6, 2.0], [7, 1.0],
                  [8, 0.0], [9, 1.0], [10, 0.0], [11, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 3
    }
]
#Iteration9
test_cases9 = [
    # Test Case 1: Simple horizontal line
    {
        "name": "horizontal_line",
        "pc_fx": [[-float('inf'), 0], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5],
                  [10, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1,  # Can be represented by a single piece
        "description": "Horizontal line should be representable by a single piece"
    },

    # Test Case 2: Step function with minimal changes
    {
        "name": "step_function",
        "pc_fx": [[-float('inf'), 0], [0, 1], [1, 1], [2, 2], [3, 2], [4, 3], [5, 3], [5, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 3,  # Each step needs its own piece
        "description": "Step function with minimal changes should require one piece per step"
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth",
        "pc_fx": [[-float('inf'), 0]] + [[x, x % 3] for x in range(0, 20, 1)] + [[20, float('inf')]],
        "epsilon": 1.5,
        "expected_pieces": 2,  # Can alternate between two values within tolerance
        "description": "Sawtooth pattern that can be approximated with 2 pieces"
    },

    # Test Case 4: Single spike
    {
        "name": "single_spike",
        "pc_fx": [[-float('inf'), 0]] + [[x, 0] for x in range(0, 10)] + [[10, 10], [11, 0]] + [[x, 0] for x in
                                                                                                range(12, 22)] + [
                     [22, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 3,  # One for the baseline, one for the spike, one to return to baseline
        "description": "Single spike requires 3 pieces"
    },

    # Test Case 5: Alternating values
    {
        "name": "alternating_values",
        "pc_fx": [[-float('inf'), 0]] + [[i, 1.0 if i % 2 == 0 else 0.0] for i in range(10)] + [[10, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1,  # Can be within epsilon using a single piece at y=0.5
        "description": "Alternating values can be approximated by their average"
    },

    # Test Case 6: Large jump
    {
        "name": "large_jump",
        "pc_fx": [[-float('inf'), 0], [0, 0], [1, 0], [2, 10], [3, 10], [4, 10], [5, 10], [5, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,  # Need at least 2 pieces for the jump
        "description": "Large jump requires at least 2 pieces"
    },

    # Test Case 7: Gradual increase
    {
        "name": "gradual_increase",
        "pc_fx": [[-float('inf'), 0]] + [[x, x] for x in range(0, 11)] + [[11, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 2,  # Can be approximated with 2 pieces
        "description": "Gradual increase can be approximated with 2 pieces"
    },

    # Test Case 8: Plateau with noise
    {
        "name": "noisy_plateau",
        "pc_fx": [[-float('inf'), 0]] +
                 [[x, 5.0 + (0.5 if x % 2 == 0 else -0.5)] for x in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1,  # All points within 0.5 of 5.0, so one piece suffices
        "description": "Noisy plateau can be one piece within tolerance"
    },

    # Test Case 9: Multiple plateaus
    {
        "name": "multiple_plateaus",
        "pc_fx": [[-float('inf'), 0]] +
                 [[x, 1.0] for x in range(0, 3)] +
                 [[3, 3.0], [4, 3.0], [5, 3.0]] +
                 [[x, 1.0] for x in range(6, 10)] +
                 [[10, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 3,  # Need 3 pieces for the two plateaus and the middle section
        "description": "Multiple plateaus require multiple pieces"
    },

    # Test Case 10: Edge case with minimal points
    {
        "name": "minimal_points",
        "pc_fx": [[-float('inf'), 0], [0, 1], [1, 0], [1, float('inf')]],
        "epsilon": 0.9,
        "expected_pieces": 1,  # Can be approximated with one piece at y=0.5
        "description": "Minimal points test case"
    }
]
#Iteration10
test_cases10 = [
    # Test case 1
    {
        "pc_fx": [(-float('inf'), 0), (0, 1), (1, 1), (2, 1), (3, float('inf'))],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    # Test case 2
    {
        "pc_fx": [(-float('inf'), 0), (0, 1), (1, 1), (2, 1.9), (3, 1.9), (4, float('inf'))],
        "epsilon": 1.0,
        "expected_pieces": 1
    },
    # Test case 3
    {
        "pc_fx": [(-float('inf'), 0), (0, 1), (1, 1), (2, 2.1), (3, 2.1), (4, float('inf'))],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    # Test case 4
    {
        "pc_fx": [(-float('inf'), 0)] + [(i, 1 if i % 2 == 0 else 0) for i in range(10)] + [(10, float('inf'))],
        "epsilon": 0.5,
        "expected_pieces": 5
    },
    # Test case 5
    {
        "pc_fx": [(-float('inf'), 0), (0, 1), (2, 2), (5, 3), (6, 4), (10, 5), (11, float('inf'))],
        "epsilon": 0.8,
        "expected_pieces": 3
    },
    # Test case 6
    {
        "pc_fx": [(-float('inf'), 0), (0, 1), (1, 1), (2, 100), (3, 100), (4, float('inf'))],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    # Test case 7
    {
        "pc_fx": [(-float('inf'), 0)] + [(i, 10 + 0.5 * (-1)**i) for i in range(20)] + [(20, float('inf'))],
        "epsilon": 0.6,
        "expected_pieces": 1
    },
    # Test case 8
    {
        "pc_fx": [(-float('inf'), 0), (0, 10), (1, 0), (2, 10), (3, 0), (4, 10), (5, float('inf'))],
        "epsilon": 5.0,
        "expected_pieces": 3
    },
    # Test case 9
    {
        "pc_fx": [(-float('inf'), 0), (0, 1), (1, 1), (2, 1), (3, 10), (4, 1), (5, 1), (6, float('inf'))],
        "epsilon": 1.0,
        "expected_pieces": 3
    },
    # Test case 10
    {
        "pc_fx": [(-float('inf'), 0)] + [(i, i*0.1) for i in range(20)] + [(20, float('inf'))],
        "epsilon": 0.2,
        "expected_pieces": 5
    }
]
#Iteration11
test_cases11 = [
    # Test Case 1: Simple single piece (should require 1 piece)
    {
        "pc_fx": [[-float('inf'), 0], [1, 1], [2, 1], [3, 1], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2],
                  [9, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1,  # Can be approximated by a single constant value
        "description": "Single piece approximation"
    },

    # Test Case 2: Two clear segments
    {
        "pc_fx": [[-float('inf'), 0], [1, 1], [2, 1], [3, 1], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5],
                  [9, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2,  # Clearly two different constant segments
        "description": "Two distinct segments"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 3], [3, 1],
                  [4, 3], [5, 1], [6, 3],
                  [7, 1], [8, 3], [9, float('inf')]],
        "epsilon": 1.5,  # Can be approximated with 2 pieces
        "expected_pieces": 2,
        "description": "Sawtooth pattern with ε=1.5"
    },

    # Test Case 4: Step function with small variations
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1.1], [2, 0.9], [3, 1.0],  # ~1
                  [4, 2.9], [5, 3.1], [6, 3.0],  # ~3
                  [7, 1.9], [8, 2.1], [9, float('inf')]],  # ~2
        "epsilon": 0.2,
        "expected_pieces": 3,  # Three distinct levels within epsilon
        "description": "Noisy step function"
    },

    # Test Case 5: Single point spike
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1], [3, 10],  # Spike at x=3
                  [4, 1], [5, 1], [6, 1],
                  [7, 1], [8, 1], [9, float('inf')]],
        "epsilon": 5,  # Large enough to cover the spike
        "expected_pieces": 1,
        "description": "Single point spike with large epsilon"
    },

    # Test Case 6: Alternating pattern with small epsilon
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 4], [3, 1],
                  [4, 4], [5, 1], [6, 4],
                  [7, 1], [8, 4], [9, float('inf')]],
        "epsilon": 0.1,  # Too small to combine any segments
        "expected_pieces": 5,  # Each segment needs its own piece
        "description": "Alternating pattern with small epsilon"
    },

    # Test Case 7: Gradually increasing values
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1.5], [3, 2.0],
                  [4, 2.5], [5, 3.0], [6, 3.5],
                  [7, 4.0], [8, 4.5], [9, float('inf')]],
        "epsilon": 0.6,  # Can combine every 2-3 segments
        "expected_pieces": 3,
        "description": "Gradually increasing values"
    },

    # Test Case 8: Empty or single-point domain
    {
        "pc_fx": [[-float('inf'), 0], [1, 5], [1, float('inf')]],  # Single point at x=1
        "epsilon": 0.1,
        "expected_pieces": 1,
        "description": "Single point domain"
    },

    # Test Case 9: Large epsilon covering all variations
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 10], [2, 15], [3, 5],
                  [4, 12], [5, 8], [6, 14],
                  [7, 6], [8, 11], [9, float('inf')]],
        "epsilon": 10,  # Large enough to cover all variations
        "expected_pieces": 1,
        "description": "Large epsilon covering all variations"
    },

    # Test Case 10: Multiple possible optimal solutions
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1], [3, 5],
                  [4, 5], [5, 1], [6, 1],
                  [7, 5], [8, 5], [9, float('inf')]],
        "epsilon": 1.5,  # Multiple ways to achieve 3 pieces
        "expected_pieces": 3,
        "description": "Multiple optimal solutions"
    }
]
#Iteration12
test_cases12 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "pc_fx": [[-float('inf'), 0], [1, 1], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 2: Two pieces with clear separation
    {
        "pc_fx": [[-float('inf'), 0], [1, 1], [3, 5], [5, 5], [6, float('inf')]],
        "epsilon": 1.0
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 3], [3, 1], [4, 3],
                  [5, 1], [6, 3], [7, 1], [8, 3],
                  [9, float('inf')]],
        "epsilon": 1.0
    },

    # Test Case 4: Single outlier in the middle
    {
        "pc_fx": [[-float('inf'), 10],
                  [1, 10], [2, 10], [3, 50], [4, 10],
                  [5, 10], [6, float('inf')]],
        "epsilon": 5.0
    },

    # Test Case 5: Gradually increasing values
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 2], [3, 3], [4, 4],
                  [5, 5], [6, float('inf')]],
        "epsilon": 1.0
    },

    # Test 6: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 10], [2, 1], [3, 10], [4, 1],
                  [5, 10], [6, 1], [7, 10], [8, 1],
                  [9, 10], [10, float('inf')]],
        "epsilon": 4.5
    },

    # Test 7: Single point with large jump
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1], [2.5, 100], [3, 1],
                  [4, 1], [5, float('inf')]],
        "epsilon": 2.0
    },

    # Test 8: Flat line with small noise
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 9.9], [2, 10.1], [3, 9.8], [4, 10.2],
                  [5, 10.0], [6, float('inf')]],
        "epsilon": 0.2
    },

    # Test 9: Multiple plateaus
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 10], [2, 10], [3, 10],  # First plateau
                  [4, 5], [5, 5], [6, 5],  # Second plateau
                  [7, 15], [8, 15], [9, 15],  # Third plateau
                  [10, float('inf')]],
        "epsilon": 2.0
    },

    # Test 10: Random-looking data
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 3.2], [2, 7.8], [3, 4.1], [4, 9.9],
                  [5, 2.3], [6, 8.7], [7, 5.4], [8, 6.7],
                  [9, 1.2], [10, float('inf')]],
        "epsilon": 2.5
    }
]
#Iteration13
test_cases13 = [
    # Test Case 1: Simple single piece (should require exactly 1 piece)
    {
        "pc_fx": [[-float('inf'), 0], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, float('inf')]],
        "epsilon": 0.5,
        "description": "Single constant piece - should require 1 piece"
    },

    # Test Case 2: Two distinct levels
    {
        "pc_fx": [[-float('inf'), 0], [1, 2], [2, 2], [3, 5], [4, 5], [5, 5], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Two distinct levels - should require 2 pieces"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 3], [3, 1], [4, 3],
                  [5, 1], [6, 3], [7, 1], [8, 3],
                  [9, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern - should require 1 piece with ε=1"
    },

    # Test Case 4: Staircase pattern
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1],
                  [3, 2], [4, 2],
                  [5, 3], [6, 3],
                  [7, 4], [8, 4],
                  [9, float('inf')]],
        "epsilon": 0.5,
        "description": "Staircase pattern - should require 4 pieces with ε=0.5"
    },

    # Test Case 5: Single outlier
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1],
                  [3, 10],  # Outlier
                  [4, 1], [5, 1],
                  [6, float('inf')]],
        "epsilon": 0.5,
        "description": "Single outlier - should require 3 pieces"
    },

    # Test Case 6: Empty function
    {
        "pc_fx": [[-float('inf'), 0], [float('inf'), 0]],
        "epsilon": 1.0,
        "description": "Empty function - should require 0 pieces"
    },

    # Test Case 7: Large epsilon that can cover all variations
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 5],
                  [3, 2], [4, 6],
                  [5, 3], [6, 4],
                  [7, float('inf')]],
        "epsilon": 10.0,
        "description": "Large epsilon - should require 1 piece"
    },

    # Test Case 8: Alternating values with small epsilon
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1.0], [2, 1.2],
                  [3, 1.0], [4, 1.2],
                  [5, 1.0], [6, 1.2],
                  [7, float('inf')]],
        "epsilon": 0.15,
        "description": "Small variations - should require multiple pieces with small ε"
    },

    # Test Case 9: Single point with large jump
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1],
                  [3, 100],  # Large jump
                  [4, 1], [5, 1],
                  [6, float('inf')]],
        "epsilon": 0.5,
        "description": "Single point with large jump - should require 3 pieces"
    },

    # Test Case 10: Gradually increasing values
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1.0], [2, 1.1],
                  [3, 1.2], [4, 1.3],
                  [5, 1.4], [6, 1.5],
                  [7, float('inf')]],
        "epsilon": 0.25,
        "description": "Gradually increasing values - should require multiple pieces"
    }
]
#Iteration14
test_cases14 = [
    # Test Case 1: Simple single piece (should return 1 piece)
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 2: Two pieces with clear separation
    {
        "name": "two_pieces_clear_separation",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0],
                  [5, 2.0],
                  [10, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 3: Sawtooth pattern (tests handling of oscillations)
    {
        "name": "sawtooth_pattern",
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1.0 if i % 2 == 0 else 0.0] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 0.6  # Should allow merging of some pieces
    },

    # Test Case 4: Gradually increasing values
    {
        "name": "gradual_increase",
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, i * 0.1] for i in range(11)] +
                 [[10, float('inf')]],
        "epsilon": 0.25  # Tests optimal merging
    },

    # Test Case 5: Large jump in values
    {
        "name": "large_jump",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0], [2, 10.0], [3, 10.0],
                  [4, float('inf')]],
        "epsilon": 2.0  # Should require at least 2 pieces
    },

    # Test Case 6: Single point with epsilon = 0 (should return original function)
    {
        "name": "single_point_zero_epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, float('inf')]],
        "epsilon": 0.0
    },

    # Test Case 7: Multiple pieces with varying lengths
    {
        "name": "varying_length_pieces",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [2, 1.5],  # First piece: length 2
                  [3, 2.0], [3.5, 2.5],  # Second piece: length 0.5
                  [5, 3.0], [8, 3.0],  # Third piece: length 3
                  [9, float('inf')]],
        "epsilon": 0.6
    },

    # Test Case 8: Edge case with very small epsilon
    {
        "name": "very_small_epsilon",
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1.0 + (i * 0.0001)] for i in range(100)] +
                 [[100, float('inf')]],
        "epsilon": 0.00001
    },

    # Test Case 9: Piece with zero width (should be handled gracefully)
    {
        "name": "zero_width_piece",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [0, 2.0],  # Zero width at x=0
                  [1, 2.0], [2, 1.0],
                  [3, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 10: Large number of pieces with random values
    {
        "name": "large_random_pieces",
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1.0 + (i % 3)] for i in range(1000)] +
                 [[1000, float('inf')]],
        "epsilon": 1.5  # Should allow significant reduction in pieces
    }
]
#Iteration15
test_cases15= [
    # Test Case 1: Single piece (minimum complexity)
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 5.0],  # Single piece with value 5.0
            [10.0, 0],
            [10.0, float('inf')]
        ],
        "epsilon": 2.0,
        "description": "Single piece - should return 1 piece",
        "expected_pieces": 1
    },

    # Test Case 2: Two pieces with clear separation
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1.0],  # First piece
            [5.0, 10.0],  # Second piece
            [10.0, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Two clearly separated pieces - should return 2 pieces",
        "expected_pieces": 2
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 0.0],
            [1, 1.0],
            [2, 0.0],
            [3, 1.0],
            [4, 0.0],
            [5, 1.0],
            [6, 0.0],
            [7, 1.0],
            [8, 0.0],
            [9, 1.0],
            [10, 0.0],
            [10, float('inf')]
        ],
        "epsilon": 0.6,
        "description": "Sawtooth pattern - should find optimal number of pieces",
        "expected_pieces": 6  # Can be approximated with alternating high/low pieces
    },

    # Test Case 4: Flat line with single outlier
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1.0],
            [1, 1.0],
            [2, 1.0],
            [3, 1.0],
            [4, 5.0],  # Single outlier
            [5, 1.0],
            [6, 1.0],
            [7, 1.0],
            [8, 1.0],
            [8, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Flat line with single outlier - should require 3 pieces",
        "expected_pieces": 3  # Before, during, and after the outlier
    },

    # Test Case 5: Gradually increasing values
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1.0],
            [1, 1.2],
            [2, 1.4],
            [3, 1.6],
            [4, 1.8],
            [5, 2.0],
            [6, 2.2],
            [7, 2.4],
            [8, 2.6],
            [9, 2.8],
            [10, 3.0],
            [10, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Gradually increasing values - should find optimal segmentation",
        "expected_pieces": 3
    },

    # Test Case 6: Single point with large epsilon
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 100.0],
            [1, 0],
            [1, float('inf')]
        ],
        "epsilon": 100.0,
        "description": "Single point with large epsilon - should return 1 piece",
        "expected_pieces": 1
    },

    # Test Case 7: Alternating high and low values
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 10.0],
            [1, 0.0],
            [2, 10.0],
            [3, 0.0],
            [4, 10.0],
            [5, 0.0],
            [6, 10.0],
            [7, 0.0],
            [8, 10.0],
            [9, 0.0],
            [10, 10.0],
            [10, float('inf')]
        ],
        "epsilon": 5.0,
        "description": "Alternating high and low values - should require all pieces",
        "expected_pieces": 11  # Cannot merge any pieces without exceeding epsilon
    },

    # Test Case 8: Multiple pieces with same value
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1.0],
            [1, 1.0],  # Same value as previous
            [2, 1.0],  # Same value as previous
            [3, 2.0],  # Different value
            [4, 2.0],  # Same as previous
            [5, 1.0],  # Back to first value
            [6, 1.0],  # Same value
            [7, 1.0],  # Same value
            [8, 1.0],  # Same value
            [8, float('inf')]
        ],
        "epsilon": 0.5,
        "description": "Multiple pieces with same value - should merge same-value pieces",
        "expected_pieces": 3  # First group of 1s, then 2s, then 1s again
    },

    # Test Case 9: Large jump in the middle
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 0.0],
            [1, 0.0],
            [2, 0.0],
            [3, 0.0],
            [4, 0.0],
            [5, 100.0],  # Large jump
            [6, 0.0],
            [7, 0.0],
            [8, 0.0],
            [9, 0.0],
            [10, 0.0],
            [10, float('inf')]
        ],
        "epsilon": 1.0,
        "description": "Single large jump in the middle - should require 3 pieces",
        "expected_pieces": 3  # Before, at, and after the jump
    },

    # Test Case 10: Random-looking data
    {
        "pc_fx": [
            [-float('inf'), 0],
            [0, 2.3],
            [1, 4.1],
            [2, 1.7],
            [3, 5.2],
            [4, 3.8],
            [5, 2.9],
            [6, 6.1],
            [7, 4.7],
            [8, 3.2],
            [9, 5.8],
            [10, 4.4],
            [10, float('inf')]
        ],
        "epsilon": 1.5,
        "description": "Random-looking data - should find good approximation",
        "expected_pieces": 4  # Reasonable approximation with 4 pieces
    }
]
#Iteration16
test_cases16 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "pc_fx": [[-float('inf'), 2.0], [1.0, 2.0], [3.0, 2.0], [5.0, 2.0], [float('inf'), 2.0]],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "Single constant piece, should require only 1 piece"
    },

    # Test Case 2: Two distinct pieces with clear separation
    {
        "pc_fx": [[-float('inf'), 1.0], [1.0, 2.0], [3.0, 5.0], [5.0, 5.0], [float('inf'), 5.0]],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "description": "Two distinct pieces with clear separation, should require 2 pieces"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), 0.0],
                  [1.0, 1.0], [2.0, 0.0], [3.0, 1.0],
                  [4.0, 0.0], [5.0, 1.0], [6.0, 0.0],
                  [7.0, 1.0], [8.0, 0.0], [float('inf'), 0.0]],
        "epsilon": 0.5,
        "expected_pieces": 5,
        "description": "Sawtooth pattern, should require multiple pieces"
    },

    # Test Case 4: Single outlier point
    {
        "pc_fx": [[-float('inf'), 1.0],
                  [1.0, 1.0], [2.0, 1.0], [3.0, 10.0],
                  [4.0, 1.0], [5.0, 1.0], [float('inf'), 1.0]],
        "epsilon": 2.0,
        "expected_pieces": 3,
        "description": "Single outlier point, should require 3 pieces"
    },

    # Test Case 5: Empty function
    {
        "pc_fx": [[-float('inf'), 0.0], [float('inf'), 0.0]],
        "epsilon": 1.0,
        "expected_pieces": 0,
        "description": "Empty function, should require 0 pieces"
    },

    # Test Case 6: Step function with varying step sizes
    {
        "pc_fx": [[-float('inf'), 0.0],
                  [1.0, 1.0], [2.0, 1.0],
                  [3.0, 3.0], [4.0, 3.0],
                  [5.0, 6.0], [6.0, 6.0],
                  [float('inf'), 6.0]],
        "epsilon": 2.0,
        "expected_pieces": 2,
        "description": "Step function with varying step sizes, should be approximable with 2 pieces"
    },

    # Test Case 7: High-frequency oscillation
    {
        "pc_fx": [[-float('inf'), 0.0]] +
                 [[x, 1.0 if i % 2 == 0 else -1.0] for i, x in enumerate(range(1, 21))] +
                 [[21.0, 0.0], [float('inf'), 0.0]],
        "epsilon": 1.5,
        "expected_pieces": 3,
        "description": "High-frequency oscillation, should require 3 pieces"
    },

    # Test Case 8: Large epsilon that can cover all variations
    {
        "pc_fx": [[-float('inf'), 0.0],
                  [1.0, 1.0], [2.0, 2.0], [3.0, 1.0],
                  [4.0, 2.0], [5.0, 1.0], [float('inf'), 0.0]],
        "epsilon": 2.0,
        "expected_pieces": 1,
        "description": "Large epsilon that can cover all variations, should require 1 piece"
    },

    # Test Case 9: Non-uniform x-spacing
    {
        "pc_fx": [[-float('inf'), 0.0],
                  [0.1, 1.0], [0.2, 1.0], [0.5, 1.0],
                  [1.0, 5.0], [1.1, 5.0], [10.0, 5.0],
                  [10.1, 1.0], [10.2, 1.0], [float('inf'), 0.0]],
        "epsilon": 2.0,
        "expected_pieces": 3,
        "description": "Non-uniform x-spacing, should require 3 pieces"
    },

    # Test Case 10: Edge case with epsilon = 0
    {
        "pc_fx": [[-float('inf'), 0.0],
                  [1.0, 1.0], [2.0, 2.0], [3.0, 2.0],
                  [4.0, 1.0], [5.0, 1.0], [float('inf'), 0.0]],
        "epsilon": 0.0,
        "expected_pieces": 5,  # Must match original exactly
        "description": "Epsilon = 0, must match original function exactly"
    }
]
#Iteration17
test_cases17 = [
    # Test Case 1: Simple single piece (should return 1 piece)
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), 5.0], [1.0, 5.0], [2.0, 5.0], [3.0, 5.0], [4.0, 5.0], [5.0, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1  # Can be represented by a single constant value 5.0
    },

    # Test Case 2: Two distinct plateaus
    {
        "name": "two_plateaus",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [1.0, 1.0], [2.0, 4.0], [3.0, 4.0], [4.0, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2  # Two distinct plateaus at y=1.0 and y=4.0
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [1.0, 2.0], [2.0, 1.0], [3.0, 2.0], [4.0, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2  # Can be approximated with two pieces at y=1.5±0.5
    },

    # Test Case 4: Large epsilon allowing single piece
    {
        "name": "large_epsilon",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [1.0, 3.0], [2.0, 2.0], [3.0, 4.0], [4.0, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 1  # All values within 2.0 of 2.5
    },

    # Test Case 5: Small epsilon requiring many pieces
    {
        "name": "small_epsilon",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 4  # Each piece needs its own constant value
    },

    # Test Case 6: Empty or single-point function
    {
        "name": "single_point",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [0.0, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 1  # Single point can be represented by one piece
    },

    # Test Case 7: Piecewise constant with large gaps
    {
        "name": "large_gaps",
        "pc_fx": [[-float('inf'), 1.0], [0.0, 1.0], [10.0, 20.0], [20.0, 20.0], [30.0, 1.0], [40.0, float('inf')]],
        "epsilon": 5.0,
        "expected_pieces": 2  # Can be approximated with two pieces (around 1.0 and 20.0)
    },

    # Test Case 8: Alternating values within epsilon
    {
        "name": "alternating_within_epsilon",
        "pc_fx": [[-float('inf'), 0.0], [0.0, 0.0], [1.0, 0.2], [2.0, 0.1], [3.0, 0.3], [4.0, 0.0],
                  [5.0, float('inf')]],
        "epsilon": 0.2,
        "expected_pieces": 1  # All values are within 0.2 of 0.15
    },

    # Test Case 9: Step function with exact epsilon
    {
        "name": "step_function",
        "pc_fx": [[-float('inf'), 0.0], [0.0, 0.0], [1.0, 0.0], [2.0, 1.0], [3.0, 1.0], [4.0, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2  # Needs two pieces to stay within 0.5 of both 0.0 and 1.0
    },

    # Test Case 10: Large dataset with varying density
    {
        "name": "varying_density",
        "pc_fx": [[-float('inf'), 1.0]] +
                 [[x, 1.0 + 0.1 * (x % 2)] for x in range(0, 10)] +
                 [[x, 2.0 + 0.1 * (x % 3)] for x in range(10, 20)] +
                 [[20.0, float('inf')]],
        "epsilon": 0.15,
        "expected_pieces": 2  # Should find two distinct plateaus
    }
]
#Iteration18
test_cases18 = [
    # Test Case 1: Single piece (already optimal)
    {
        "pc_fx": [[-float('inf'), 0], [1, 1], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Single constant piece - already optimal",
        "min_pieces": 1
    },

    # Test Case 2: Two pieces with clear separation
    {
        "pc_fx": [[-float('inf'), 0], [1, 1], [2, 1], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Two clearly separated constant pieces",
        "min_pieces": 2
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 3], [3, 1], [4, 3],
                  [5, 1], [6, 3], [7, 1], [8, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern with period 2",
        "min_pieces": 2  # Can be approximated with two pieces
    },

    # Test Case 4: Single spike in the middle
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1], [3, 10], [4, 1],
                  [5, 1], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Single spike in the middle",
        "min_pieces": 3  # Need one piece for the spike
    },

    # Test Case 5: Alternating pattern with varying gaps
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 0], [2, 2], [3, 0], [4, 2],
                  [5, 0], [6, 2], [7, 0], [8, 2],
                  [9, 0], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Alternating pattern that can be approximated with one piece",
        "min_pieces": 1
    },

    # Test Case 6: Staircase pattern
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1], [3, 2], [4, 2],
                  [5, 3], [6, 3], [7, 4], [8, 4],
                  [9, 5], [10, float('inf')]],
        "epsilon": 0.9,
        "description": "Staircase pattern",
        "min_pieces": 5  # Each step needs its own piece
    },

    # Test Case 7: Flat with single outlier
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1], [3, 5], [4, 1],
                  [5, 1], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Flat line with single outlier",
        "min_pieces": 3  # Need separate piece for the outlier
    },

    # Test Case 8: High frequency oscillation
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, 1 + 0.8 * (-1) ** i] for i in range(1, 20)] +
                 [[20, float('inf')]],
        "epsilon": 1.0,
        "description": "High frequency oscillation",
        "min_pieces": 1  # Can be approximated with one piece
    },

    # Test Case 9: Piecewise constant with varying lengths
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [4, 1],  # Length 3
                  [5, 2], [6, 2],  # Length 1
                  [7, 1], [10, 1],  # Length 3
                  [11, float('inf')]],
        "epsilon": 0.5,
        "description": "Pieces with varying lengths",
        "min_pieces": 3  # Each distinct value needs its own piece
    },

    # Test Case 10: Large number of small pieces
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, i % 3] for i in range(1, 101)] +
                 [[101, float('inf')]],
        "epsilon": 1.0,
        "description": "Large number of small pieces with 3 distinct values",
        "min_pieces": 3  # Can be approximated with 3 pieces
    }
]
#Iteration19
test_cases19 = [
    # Test Case 1: Single piece (minimum possible)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [10.0, 5.0], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece with constant value, should require exactly 1 piece"
    },

    # Test Case 2: Two pieces with clear separation
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0],
                  [5.0, 10.0],
                  [10.0, 0.0],
                  [15.0, 10.0],
                  [20.0, 0.0],
                  [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "description": "Clear step function, should require 3 pieces"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, i % 2] for i in range(10)] +
                 [[10, 0], [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "description": "Sawtooth pattern, should require multiple pieces"
    },

    # Test Case 4: Gradually increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, i / 10.0] for i in range(11)] +
                 [[11, 1.0], [float('inf'), float('inf')]],
        "epsilon": 0.2,
        "description": "Gradually increasing values, tests merging of similar pieces"
    },

    # Test Case 5: Large jump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0],
                  [5.0, 1000.0],
                  [10.0, 0.0],
                  [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "description": "Large jump in value, tests handling of significant changes"
    },

    # Test Case 6: Small oscillation within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 5.0 + 0.9 * ((-1) ** i)] for i in range(10)] +
                 [[10, 5.0], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "description": "Small oscillations within epsilon, should be approximated by 1 piece"
    },

    # Test Case 7: Varying segment lengths
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0],
                  [1, 1.0],
                  [1.1, 0.0],
                  [1.2, 1.0],
                  [2.0, 0.0],
                  [10.0, 0.0],
                  [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "description": "Varying segment lengths, tests handling of different interval sizes"
    },

    # Test Case 8: Large number of small pieces
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i / 10.0, (i % 2) * 2.0] for i in range(101)] +
                 [[10.1, 0.0], [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "description": "Many small pieces, tests efficiency and merging logic"
    },

    # Test Case 9: Edge case with minimal difference
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0],
                  [1, 0.5],
                  [2, 0.0],
                  [3, 0.5],
                  [4, 0.0],
                  [float('inf'), float('inf')]],
        "epsilon": 0.6,
        "description": "Small differences around epsilon, tests boundary conditions"
    },

    # Test Case 10: Complex pattern
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 0.0] for i in range(0, 5)] +
                 [[5, 1.0], [6, 0.0], [7, 1.0], [8, 0.0], [9, 1.0]] +
                 [[i, 0.0] for i in range(10, 20)] +
                 [[20, 2.0], [21, 0.0], [22, 2.0], [23, 0.0]] +
                 [[24, 0.0], [25, 1.0], [26, 0.0], [27, 1.0], [28, 0.0], [29, 1.0]] +
                 [[30, 0.0], [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "description": "Complex pattern with multiple features, tests overall robustness"
    }
]
#Iteration20
test_cases20 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), 0], [0, 1.0], [1.0, 0]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Single piece function - should require exactly 1 piece"
    },

    # Test Case 2: Two piece function with clear separation
    {
        "name": "two_pieces_clear",
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1.0],
            [1.0, 3.0],
            [2.0, 0]
        ],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Two clearly separated pieces - should require 2 pieces"
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth",
        "pc_fx": [
            [-float('inf'), 0],
            [0, 0], [1, 1], [2, 0], [3, 1],
            [4, 0], [5, 1], [6, 0],
            [7, float('inf')]
        ],
        "epsilon": 0.6,
        "expected_min_pieces": 4,
        "description": "Sawtooth pattern - tests handling of alternating values"
    },

    # Test Case 4: Flat with single outlier
    {
        "name": "single_outlier",
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1.0], [1, 1.0], [2, 1.0],
            [3, 5.0],  # Outlier
            [4, 1.0], [5, 1.0], [6, 1.0],
            [7, float('inf')]
        ],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Flat line with single outlier - should require 2 pieces"
    },

    # Test Case 5: Step function
    {
        "name": "step_function",
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1], [1, 1], [2, 1],  # y=1
            [3, 2], [4, 2], [5, 2],  # y=2
            [6, 1], [7, 1], [8, 1],  # y=1
            [9, float('inf')]
        ],
        "epsilon": 0.6,
        "expected_min_pieces": 3,
        "description": "Step function - should find minimum steps"
    },

    # Test Case 6: High frequency oscillation
    {
        "name": "high_freq_oscillation",
        "pc_fx": [
            [-float('inf'), 0],
            *[[x, 1.0 + 0.1 * (-1) ** i] for i, x in enumerate([0, 0.1, 0.2, 0.3, 0.4, 0.5])],
            [0.6, float('inf')]
        ],
        "epsilon": 0.2,
        "expected_min_pieces": 1,
        "description": "High frequency oscillation within epsilon - should be approximable with 1 piece"
    },

    # Test Case 7: Empty function
    {
        "name": "empty_function",
        "pc_fx": [
            [-float('inf'), 0],
            [0, float('inf')]
        ],
        "epsilon": 1.0,
        "expected_min_pieces": 0,
        "description": "Empty function - should handle edge case gracefully"
    },

    # Test Case 8: Large epsilon
    {
        "name": "large_epsilon",
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1], [1, 2], [2, 1], [3, 2], [4, 1],
            [5, float('inf')]
        ],
        "epsilon": 10.0,
        "expected_min_pieces": 1,
        "description": "Very large epsilon - should require only 1 piece"
    },

    # Test Case 9: Small epsilon
    {
        "name": "small_epsilon",
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1.0], [1, 1.05], [2, 1.0], [3, 1.05],
            [4, float('inf')]
        ],
        "epsilon": 0.01,
        "expected_min_pieces": 4,
        "description": "Very small epsilon - should require many pieces"
    },

    # Test Case 10: Non-uniform x-spacing
    {
        "name": "non_uniform_x",
        "pc_fx": [
            [-float('inf'), 0],
            [0, 1.0],
            [0.1, 1.0],  # Dense sampling
            [1.0, 2.0],
            [10.0, 2.0],  # Sparse sampling
            [10.1, 1.0],
            [11.0, float('inf')]
        ],
        "epsilon": 0.5,
        "expected_min_pieces": 3,
        "description": "Non-uniform x-spacing - should handle varying intervals"
    }
]
#Iteration21
test_cases21 = [
    # Test Case 1: Simple single-step function
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 1.0],
            [1.0, 2.0],
            [2.0, 1.0],
            [3.0, float('inf')]
        ],
        "epsilon": 0.5
    },

    # Test Case 2: Sawtooth pattern
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 0.0],
            [1.0, 1.0],
            [2.0, 0.0],
            [3.0, 1.0],
            [4.0, 0.0],
            [5.0, float('inf')]
        ],
        "epsilon": 0.6
    },

    # Test Case 3: Flat line with single outlier
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 0.0],
            [1.0, 0.0],
            [2.0, 1.0],  # Single outlier
            [3.0, 0.0],
            [4.0, 0.0],
            [5.0, float('inf')]
        ],
        "epsilon": 0.5
    },

    # Test Case 4: Staircase function
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 1.0],
            [1.0, 2.0],
            [2.0, 3.0],
            [3.0, 2.0],
            [4.0, 1.0],
            [5.0, float('inf')]
        ],
        "epsilon": 0.75
    },

    # Test Case 5: High-frequency oscillation
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 0.0],
            [0.2, 1.0],
            [0.4, 0.0],
            [0.6, 1.0],
            [0.8, 0.0],
            [1.0, 1.0],
            [1.2, 0.0],
            [1.4, 1.0],
            [1.6, 0.0],
            [1.8, 1.0],
            [2.0, float('inf')]
        ],
        "epsilon": 0.6
    },

    # Test Case 6: Single point with large epsilon
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 10.0],
            [1.0, float('inf')]
        ],
        "epsilon": 5.0
    },

    # Test Case 7: Alternating high and low values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 10.0],
            [1.0, 0.0],
            [2.0, 10.0],
            [3.0, 0.0],
            [4.0, 10.0],
            [5.0, float('inf')]
        ],
        "epsilon": 5.1
    },

    # Test Case 8: Gradually increasing values
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 0.0],
            [1.0, 0.5],
            [2.0, 1.0],
            [3.0, 1.5],
            [4.0, 2.0],
            [5.0, float('inf')]
        ],
        "epsilon": 0.6
    },

    # Test Case 9: Two large steps
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 0.0],
            [1.0, 10.0],
            [2.0, 20.0],
            [3.0, float('inf')]
        ],
        "epsilon": 5.0
    },

    # Test Case 10: Random-looking data
    {
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0.0, 1.2],
            [1.0, 3.4],
            [2.0, 2.1],
            [3.0, 4.0],
            [4.0, 2.8],
            [5.0, 3.9],
            [6.0, 5.1],
            [7.0, 4.7],
            [8.0, 6.0],
            [9.0, float('inf')]
        ],
        "epsilon": 1.0
    }
]
#Iteration22
test_cases22 = [
    # Test Case 1: Simple single piece (should require 1 piece)
    {
        "pc_fx": [[-float('inf'), 0], [0, 1.0], [1.0, 1.0], [2.0, float('inf')]],
        "epsilon": 0.5,
        "description": "Single constant piece - should require 1 piece"
    },

    # Test Case 2: Two clearly separated pieces
    {
        "pc_fx": [[-float('inf'), 0], [0, 1.0], [1.0, 1.0], [2.0, 3.0], [3.0, 3.0], [4.0, float('inf')]],
        "epsilon": 0.1,
        "description": "Two clearly separated constant pieces - should require 2 pieces"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, i % 2] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 0.5,
        "description": "Sawtooth pattern - should require 1 piece with ε=0.5"
    },

    # Test Case 4: Step function with varying step sizes
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, i] for i in range(5)] +
                 [[5, float('inf')]],
        "epsilon": 0.6,
        "description": "Step function - should require 3 pieces with ε=0.6"
    },

    # Test Case 5: Single outlier in the middle
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, 1.0] for i in range(5)] +
                 [[5, 10.0], [6, 1.0]] +
                 [[i, 1.0] for i in range(7, 10)] +
                 [[10, float('inf')]],
        "epsilon": 2.0,
        "description": "Single outlier in middle - should require 3 pieces with ε=2.0"
    },

    # Test Case 6: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, 1.0 if i % 2 == 0 else 3.0] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 1.1,
        "description": "Alternating high/low values - should require 1 piece with ε=1.1"
    },

    # Test Case 7: Linear increase with noise
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, i + (0.5 if i % 2 == 0 else -0.5)] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 1.0,
        "description": "Linear increase with noise - should require 1 piece with ε=1.0"
    },

    # Test Case 8: Plateau in the middle
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, 1.0] for i in range(5)] +  # Increasing
                 [[i, 3.0] for i in range(5, 15)] +  # Plateau
                 [[i, 1.0] for i in range(15, 20)] +  # Decreasing
                 [[20, float('inf')]],
        "epsilon": 1.1,
        "description": "Plateau in middle - should require 3 pieces with ε=1.1"
    },

    # Test Case 9: Large jump in the middle
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i, 1.0] for i in range(5)] +
                 [[i, 10.0] for i in range(5, 10)] +
                 [[10, float('inf')]],
        "epsilon": 0.5,
        "description": "Large jump in middle - should require 2 pieces with ε=0.5"
    },

    # Test Case 10: Very small epsilon test
    {
        "pc_fx": [[-float('inf'), 0]] +
                 [[i / 10, 1.0 + (i % 3) * 0.01] for i in range(100)] +
                 [[10, float('inf')]],
        "epsilon": 0.02,
        "description": "Very small epsilon - should require multiple pieces with ε=0.02"
    }
]
#Iteration23
test_cases23 = [
    # Test Case 1: Single piece (minimum possible)
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [10.0, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },

    # Test Case 2: Two pieces with clear separation
    {
        "name": "two_pieces_clear_separation",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0],
            [5.0, 3.0],
            [10.0, float('inf')]
        ],
        "epsilon": 0.5,
        "expected_min_pieces": 2
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth_pattern",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.0],
            [1, 1.0],
            [2, 0.0],
            [3, 1.0],
            [4, 0.0],
            [5, float('inf')]
        ],
        "epsilon": 0.6,
        "expected_min_pieces": 3
    },

    # Test Case 4: Step function
    {
        "name": "step_function",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.0],
            [1, 1.0],
            [2, 2.0],
            [3, 3.0],
            [4, 4.0],
            [5, float('inf')]
        ],
        "epsilon": 0.8,
        "expected_min_pieces": 1  # Can be approximated by a single constant value of 2.0
    },

    # Test Case 5: Alternating high and low values
    {
        "name": "alternating_high_low",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 10.0],
            [1, 0.0],
            [2, 10.0],
            [3, 0.0],
            [4, 10.0],
            [5, float('inf')]
        ],
        "epsilon": 4.9,
        "expected_min_pieces": 1  # Can be approximated by a single constant value of 5.0
    },

    # Test Case 6: Gradually increasing values
    {
        "name": "gradual_increase",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.0],
            [1, 0.3],
            [2, 0.6],
            [3, 0.9],
            [4, 1.2],
            [5, float('inf')]
        ],
        "epsilon": 0.3,
        "expected_min_pieces": 3
    },

    # Test Case 7: Single spike
    {
        "name": "single_spike",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.0],
            [1, 0.0],
            [2, 5.0],  # Spike
            [3, 0.0],
            [4, 0.0],
            [5, float('inf')]
        ],
        "epsilon": 0.5,
        "expected_min_pieces": 3
    },

    # Test Case 8: Flat with noise
    {
        "name": "flat_with_noise",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 1.0],
            [1, 1.1],
            [2, 0.9],
            [3, 1.0],
            [4, 0.95],
            [5, float('inf')]
        ],
        "epsilon": 0.2,
        "expected_min_pieces": 1  # All values within 0.2 of 1.0
    },

    # Test Case 9: Two steps with different widths
    {
        "name": "two_steps_different_widths",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.0],
            [2, 1.0],  # First step at x=2
            [3, 1.0],
            [5, 2.0],  # Second step at x=5
            [6, 2.0],
            [7, float('inf')]
        ],
        "epsilon": 0.6,
        "expected_min_pieces": 2
    },

    # Test Case 10: Complex pattern requiring careful piece placement
    {
        "name": "complex_pattern",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.0],
            [1, 2.0],
            [2, 1.0],
            [3, 3.0],
            [4, 1.0],
            [5, 2.0],
            [6, 0.0],
            [7, float('inf')]
        ],
        "epsilon": 1.0,
        "expected_min_pieces": 2  # Can be approximated with pieces [0,3.5) and [3.5,7)
    }
]
#Iteration24
test_cases24 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece function should remain single piece"
    },

    # Test Case 2: Step function with optimal 2-piece approximation
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0],
                  [3, float('inf')]],
        "epsilon": 0.6,
        "description": "Step function that can be approximated with 2 pieces within epsilon"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0], [4, 0.0],
                  [5, float('inf')]],
        "epsilon": 0.6,
        "description": "Sawtooth pattern requiring careful piece selection"
    },

    # Test Case 4: Constant function with noise
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1.0 + (0.1 if i % 2 else -0.1)] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 0.2,
        "description": "Noisy constant function that should be approximated by a single piece"
    },

    # Test Case 5: Increasing function with varying slopes
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, i + (i % 3 - 1) * 0.5] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 1.0,
        "description": "Increasing function with varying slopes"
    },

    # Test Case 6: Piece with exactly epsilon deviation
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.5], [2, 1.0], [3, 1.5], [4, 2.0],
                  [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Function where some points are exactly epsilon away from the approximation"
    },

    # Test Case 7: Non-uniform x-spacing
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [0.1, 0.2], [0.2, 0.4], [1.0, 1.0], [2.0, 0.0],
                  [3.0, float('inf')]],
        "epsilon": 0.3,
        "description": "Non-uniform x-spacing testing interval handling"
    },

    # Test Case 8: Large epsilon making single piece optimal
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, i % 2] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 1.1,
        "description": "Large epsilon making single piece optimal"
    },

    # Test Case 9: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 2.0 if i % 2 else 0.0] for i in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 1.1,
        "description": "Alternating high and low values testing piece merging"
    },

    # Test Case 10: Complex pattern requiring careful piece selection
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[0, 0.0], [1, 0.8], [2, 0.2], [3, 1.0], [4, 0.1],
                  [5, 0.9], [6, 0.3], [7, 1.1], [8, 0.0], [9, 0.7], [10, 0.4]] +
                 [[11, float('inf')]],
        "epsilon": 0.6,
        "description": "Complex pattern requiring careful piece selection"
    }
]
#Iteration25
test_cases25 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [10, 1.0], [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "description": "Single constant piece should require only 1 segment"
    },

    # Test Case 2: Two pieces with gap exactly 2ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [5, 2.0], [10, 0.0], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "Two pieces with gap exactly 2ε can be merged"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')]] + [[i, 1.0 if i % 2 == 0 else -1.0] for i in range(10)] + [[10, 1.0], [
            float('inf'), float('inf')]],
        "epsilon": 1.5,
        "expected_pieces": 1,
        "description": "Sawtooth pattern within ε should be approximated by one piece"
    },

    # Test Case 4: Staircase with varying step heights
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [2, 1.0],
                  [2, 2.0], [4, 2.0],
                  [4, 3.0], [6, 3.0],
                  [6, 4.0], [8, 4.0],
                  [float('inf'), float('inf')]],
        "epsilon": 0.9,
        "expected_pieces": 4,
        "description": "Staircase with steps of height 1.0, ε=0.9 should require 4 pieces"
    },

    # Test Case 5: Single spike
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [4, 0.0],
                  [5, 5.0],  # spike
                  [6, 0.0], [10, 0.0],
                  [float('inf'), float('inf')]],
        "epsilon": 2.5,
        "expected_pieces": 3,
        "description": "Single spike requires 3 pieces with ε=2.5"
    },

    # Test Case 6: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 10.0 if i % 2 == 0 else 0.0] for i in range(10)] +
                 [[10, 10.0], [float('inf'), float('inf')]],
        "epsilon": 5.0,
        "expected_pieces": 1,
        "description": "Alternating values within 5.0 of each other should be one piece"
    },

    # Test Case 7: Gradually increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, i * 0.1] for i in range(11)] +
                 [[float('inf'), float('inf')]],
        "epsilon": 0.25,
        "expected_pieces": 3,
        "description": "Gradually increasing values with ε=0.25 should require 3 pieces"
    },

    # Test Case 8: Single point with large jump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.0],
                  [1, 10.0],  # jump
                  [2, 10.0],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 3,
        "description": "Single point with large jump requires 3 pieces"
    },

    # Test Case 9: Multiple plateaus
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 0.0] for i in range(5)] +  # 0-4: 0.0
                 [[5, 2.0], [6, 2.0],  # 5-6: 2.0
                  [7, 0.0], [8, 0.0],  # 7-8: 0.0
                  [9, 2.0], [10, 2.0],  # 9-10: 2.0
                  [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "description": "Multiple plateaus with ε=1.0 can be merged into 2 pieces"
    },

    # Test Case 10: Empty or single-point function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [float('inf'), float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "description": "Single-point function should require only 1 piece"
    }
]
#Iteration26
test_cases26 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), 0], [1.0, 1.0], [2.0, 0], [float('inf'), 0]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },

    # Test Case 2: Two pieces with clear separation
    {
        "name": "two_pieces_clear_separation",
        "pc_fx": [[-float('inf'), 0], [1.0, 1.0], [2.0, 3.0], [3.0, 0], [float('inf'), 0]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },

    # Test Case 3: Sawtooth pattern
    {
        "name": "sawtooth_pattern",
        "pc_fx": [[-float('inf'), 0],
                  [1.0, 1.0], [2.0, -1.0], [3.0, 1.0],
                  [4.0, -1.0], [5.0, 1.0], [6.0, 0],
                  [float('inf'), 0]],
        "epsilon": 0.9,
        "expected_pieces": 3
    },

    # Test Case 4: Step function
    {
        "name": "step_function",
        "pc_fx": [[-float('inf'), 0],
                  [1.0, 1.0], [2.0, 1.0], [3.0, 2.0],
                  [4.0, 2.0], [5.0, 3.0], [6.0, 0],
                  [float('inf'), 0]],
        "epsilon": 0.5,
        "expected_pieces": 3
    },

    # Test Case 5: Large epsilon (should reduce to single piece)
    {
        "name": "large_epsilon",
        "pc_fx": [[-float('inf'), 0],
                  [1.0, 1.0], [2.0, 1.5], [3.0, 0.5],
                  [4.0, 1.0], [5.0, 0.8], [6.0, 0],
                  [float('inf'), 0]],
        "epsilon": 2.0,
        "expected_pieces": 1
    },

    # Test Case 6: Very small epsilon (should require many pieces)
    {
        "name": "small_epsilon",
        "pc_fx": [[-float('inf'), 0],
                  [1.0, 1.0], [1.5, 1.1], [2.0, 0.9],
                  [2.5, 1.05], [3.0, 0.95], [3.5, 0],
                  [float('inf'), 0]],
        "epsilon": 0.05,
        "expected_pieces": 5
    },

    # Test Case 7: Single point with large jump
    {
        "name": "single_point_jump",
        "pc_fx": [[-float('inf'), 0],
                  [1.0, 1.0], [1.0001, 10.0], [2.0, 0],
                  [float('inf'), 0]],
        "epsilon": 4.0,
        "expected_pieces": 2
    },

    # Test Case 8: Empty function
    {
        "name": "empty_function",
        "pc_fx": [[-float('inf'), 0], [float('inf'), 0]],
        "epsilon": 1.0,
        "expected_pieces": 0
    },

    # Test Case 9: Piece with zero width
    {
        "name": "zero_width_piece",
        "pc_fx": [[-float('inf'), 0],
                  [1.0, 1.0], [1.0, 2.0], [2.0, 0],
                  [float('inf'), 0]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },

    # Test Case 10: Random noise within epsilon
    {
        "name": "random_noise_within_epsilon",
        "pc_fx": [[-float('inf'), 0],
                  [1.0, 1.0], [1.5, 1.2], [2.0, 0.8],
                  [2.5, 1.1], [3.0, 0.9], [3.5, 1.0],
                  [4.0, 0], [float('inf'), 0]],
        "epsilon": 0.25,
        "expected_pieces": 1
    }
]
#Iteration27
test_cases27 = [
    # Test Case 1: Simple single piece (should return 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, float('inf')]],
        "epsilon": 0.5,
        "description": "Single piece function should return exactly 1 piece"
    },

    # Test Case 2: Two pieces with clear separation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [2, 2.0], [3, float('inf')]],
        "epsilon": 0.4,
        "description": "Two clearly separated pieces should return 2 pieces"
    },

    # Test Case 3: Step function with varying step heights
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0], [4, 0.0], [5, float('inf')]],
        "epsilon": 0.6,
        "description": "Step function with alternating heights, should need 2-3 pieces"
    },

    # Test Case 4: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0],
                  [4, 0.0], [5, 1.0], [6, 0.0], [7, float('inf')]],
        "epsilon": 0.6,
        "description": "Sawtooth pattern, should need multiple pieces"
    },

    # Test Case 5: Large epsilon that can cover all variations
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.1], [2, 0.9], [3, 1.0],
                  [4, 1.1], [5, 0.9], [6, 1.0], [7, float('inf')]],
        "epsilon": 0.5,
        "description": "Small variations within epsilon should be covered by one piece"
    },

    # Test Case 6: Single outlier point
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0], [2, 5.0], [3, 1.0],
                  [4, 1.0], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Single outlier point requiring an additional piece"
    },

    # Test Case 7: Gradually increasing function
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.2], [2, 0.4], [3, 0.6],
                  [4, 0.8], [5, 1.0], [6, float('inf')]],
        "epsilon": 0.3,
        "description": "Gradually increasing function, tests optimal piece placement"
    },

    # Test Case 8: Large number of small pieces
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1.0 if i % 2 == 0 else 0.0] for i in range(20)] +
                 [[20, float('inf')]],
        "epsilon": 0.6,
        "description": "Many small pieces, should be able to combine many into single pieces"
    },

    # Test Case 9: Edge case with minimum possible pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0], [2, 1.0], [3, 1.0],
                  [4, 1.0], [5, float('inf')]],
        "epsilon": 0.0,
        "description": "All values identical with epsilon=0, should return 1 piece"
    },

    # Test Case 10: Challenging case with alternating high and low points
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0],
                  [4, 0.0], [5, 2.0], [6, 0.0], [7, float('inf')]],
        "epsilon": 1.0,
        "description": "Alternating high and low points, tests optimal piece placement"
    }
]
#Iteration28
test_cases28 = [
    # Test Case 1: Single piece (minimum case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [10, float('inf')]],
        "epsilon": 2.0,
        "description": "Single piece within tolerance, should return 1 piece"
    },

    # Test Case 2: Step function with exact fit
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [5, 1.0], [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Step function that can be exactly represented with 2 pieces"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0],
                  [3, 1.0], [4, 0.0], [5, float('inf')]],
        "epsilon": 0.6,
        "description": "Sawtooth pattern, should require 3 pieces"
    },

    # Test Case 4: Constant function with noise
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[x, 5.0 + (0.5 if x % 2 else -0.5)] for x in range(0, 11)] +
                 [[11, float('inf')]],
        "epsilon": 1.0,
        "description": "Constant function with small noise, should be 1 piece"
    },

    # Test Case 5: Two distinct plateaus
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[x, 0.0] for x in range(0, 5)] +
                 [[x, 1.0] for x in range(5, 10)] +
                 [[10, float('inf')]],
        "epsilon": 0.1,
        "description": "Two distinct plateaus, should require 2 pieces"
    },

    # Test Case 6: Alternating values
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[x, 0.0 if x % 2 == 0 else 1.0] for x in range(0, 10)] +
                 [[10, float('inf')]],
        "epsilon": 1.5,
        "description": "Alternating values, should require 1 piece"
    },

    # Test Case 7: Large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[x, x] for x in range(0, 10)] +
                 [[10, float('inf')]],
        "epsilon": 10.0,
        "description": "Linear function with large epsilon, should require 1 piece"
    },

    # Test Case 8: Small epsilon requiring all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[x, x] for x in range(0, 5)] +
                 [[5, float('inf')]],
        "epsilon": 0.01,
        "description": "Linear function with tiny epsilon, should require all pieces"
    },

    # Test Case 9: Piece with zero width
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [0, 2.0],  # Zero-width piece at x=0
                  [1, 3.0], [2, float('inf')]],
        "epsilon": 1.0,
        "description": "Contains zero-width piece, should be handled gracefully"
    },

    # Test Case 10: Large range with small features
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[x, 0.0] for x in range(0, 100, 10)] +
                 [[100, float('inf')]],
        "epsilon": 0.1,
        "description": "Large range with small features, should test numerical stability"
    }
]
#Iteration29
test_cases29 = [
    # Test Case 1: Single piece (minimum case)
    {
        "pc_fx": [[-float('inf'), 0], [1, 5], [2, 5], [3, 5], [4, 5], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece constant function should require only 1 piece"
    },

    # Test Case 2: Simple step function
    {
        "pc_fx": [[-float('inf'), 0], [1, 1], [2, 1], [3, 4], [4, 4], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Simple step function with two distinct levels"
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 3], [3, 1],
                  [4, 3], [5, 1], [6, 3],
                  [7, 1], [8, float('inf')]],
        "epsilon": 1.0,
        "description": "Sawtooth pattern testing alternating peaks and valleys"
    },

    # Test Case 4: Noisy constant with single outlier
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 1], [3, 10],
                  [4, 1], [5, 1], [6, float('inf')]],
        "epsilon": 0.5,
        "description": "Single outlier in otherwise constant function"
    },

    # Test Case 5: Gradually increasing function
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 2], [3, 3],
                  [4, 4], [5, 5], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "Monotonically increasing function"
    },

    # Test Case 6: Varying segment lengths
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [3, 1],  # 2 units wide
                  [3.1, 2],  # 0.1 units wide
                  [5, 2], [7, 2],  # 2 units wide
                  [7.5, 1],  # 0.5 units wide
                  [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Segments with varying lengths and values"
    },

    # Test Case 7: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 10], [2, 1], [3, 10],
                  [4, 1], [5, 10], [6, 1],
                  [7, 10], [8, float('inf')]],
        "epsilon": 2.0,
        "description": "Alternating between high and low values"
    },

    # Test Case 8: Large epsilon test
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1], [2, 5], [3, 8],
                  [4, 4], [5, 7], [6, 2],
                  [7, 6], [8, float('inf')]],
        "epsilon": 4.0,
        "description": "Large epsilon that should allow significant approximation"
    },

    # Test Case 9: Small epsilon test
    {
        "pc_fx": [[-float('inf'), 0],
                  [1, 1.0], [2, 1.1], [3, 1.05],
                  [4, 1.15], [5, 1.2], [6, 1.18],
                  [7, 1.22], [8, float('inf')]],
        "epsilon": 0.05,
        "description": "Small epsilon requiring precise approximation"
    },

    # Test Case 10: Empty function (edge case)
    {
        "pc_fx": [[-float('inf'), 0], [float('inf'), 0]],
        "epsilon": 1.0,
        "description": "Empty function with no actual pieces"
    }
]
#Iteration30
test_cases30 = [
    # Test Case 1: Simple single piece (already optimal)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 1.0], [3, 1.0], [4, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 2: Two pieces with clear separation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [2, 1.0], [3, 2.0], [4, 2.0], [5, 2.0], [6, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 3: Sawtooth pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0],
                  [4, 0.0], [5, 1.0], [6, 0.0], [7, float('inf')]],
        "epsilon": 0.6
    },

    # Test Case 4: Staircase pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0],
                  [2, 2.0], [3, 2.0],
                  [4, 3.0], [5, 3.0],
                  [6, 4.0], [7, float('inf')]],
        "epsilon": 0.9
    },

    # Test 5: Single point that can't be merged (edge case)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, float('inf')]],
        "epsilon": 0.4
    },

    # Test 6: Multiple possible optimal solutions
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0], [2, 3.0], [3, 3.0],
                  [4, 1.0], [5, 1.0], [6, 3.0], [7, 3.0], [8, float('inf')]],
        "epsilon": 1.0
    },

    # Test 7: Large number of pieces with small variations
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1.0 + 0.1 * (i % 3)] for i in range(0, 20)] +
                 [[20, float('inf')]],
        "epsilon": 0.2
    },

    # Test 8: Vertical gap that requires splitting
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.0], [2, 2.0], [3, 2.0], [4, 0.0], [5, 0.0], [6, float('inf')]],
        "epsilon": 0.9
    },

    # Test 9: Alternating high and low values
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, 1.0 + (i % 2)] for i in range(0, 10)] +
                 [[10, float('inf')]],
        "epsilon": 0.6
    },

    # Test 10: Large epsilon that should allow complete merging
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, i % 3] for i in range(0, 15)] +
                 [[15, float('inf')]],
        "epsilon": 2.0
    }
]
