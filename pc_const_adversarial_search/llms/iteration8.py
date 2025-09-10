# Zero-shot prompt on Windsurf SWE-1 model
# 10 Sept 2025 7:58AM
test_cases = [
    # Test Case 1: Simple case with 2 pieces, should be optimal
    {
        'pc_fx': [[-float('inf'), float('inf')], [1, 2], [3, 4], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Simple 2-piece function, should require exactly 2 pieces'
    },

    # Test Case 2: Single piece with noise within epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [1, 3], [2, 4], [3, 3], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece with small variations within epsilon'
    },

    # Test Case 3: Sawtooth pattern
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [1, 0], [2, 2], [3, 0], [4, 2],
                  [5, 0], [6, 2], [7, 0], [9, float('inf')]],
        'epsilon': 1.0,
        'description': 'Sawtooth pattern, optimal should have fewer pieces'
    },

    # Test Case 4: Staircase with varying step sizes
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [1, 1], [2, 2], [4, 3], [7, 4],
                  [11, 5], [16, float('inf')]],
        'epsilon': 1.0,
        'description': 'Staircase with increasing step sizes'
    },

    # Test Case 5: Large epsilon, should collapse to single piece
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [1, 1], [2, 3], [3, 2], [4, 4],
                  [5, 2], [6, 3], [7, 1], [8, float('inf')]],
        'epsilon': 2.0,
        'description': 'Large epsilon should allow single piece approximation'
    },

    # Test Case 6: Alternating high and low values
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [1, 10], [2, 0], [3, 10], [4, 0],
                  [5, 10], [6, 0], [7, 10], [8, float('inf')]],
        'epsilon': 5.0,
        'description': 'Alternating high and low values within epsilon'
    },

    # Test Case 7: Single point spike
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [1, 0], [2, 0], [3, 10], [4, 0],
                  [5, 0], [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single point spike requiring multiple pieces'
    },

    # Test Case 8: Flat with single outlier
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [1, 0], [2, 0], [3, 2], [4, 0],
                  [5, 0], [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Mostly flat with single outlier'
    },

    # Test Case 9: Gradual increase with noise
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [1, 1.1], [2, 1.9], [3, 3.1], [4, 3.9],
                  [5, 4.9], [6, float('inf')]],
        'epsilon': 0.5,
        'description': 'Gradual increase with small noise'
    },

    # Test Case 10: Edge case with minimum number of pieces
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [1, 0], [2, 0], [3, 0], [4, 0],
                  [5, 5], [6, 5], [7, 5], [8, 5],
                  [9, 0], [10, 0], [11, 0], [12, 0],
                  [13, float('inf')]],
        'epsilon': 1.0,
        'description': 'Large flat regions with single bump'
    }
]