# Few-shot prompt on Windsurf SWE-1 model
# 10 Sept 2025 8:10AM
test_cases = [
    # Test Case 1: Simple 2-piece function
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2.0], [5, 4.0], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Simple 2-piece function with clear separation'
    },

    # Test Case 2: Single piece with small variations
    {
        'pc_fx': [[-float('inf'), float('inf')], [1, 3.0], [2, 3.2], [3, 2.9], [4, 3.1], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Single piece with variations within epsilon'
    },

    # Test Case 3: Sawtooth pattern
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0],
                  [4, 0.0], [5, 1.0], [6, 0.0], [7, float('inf')]],
        'epsilon': 1.0,
        'description': 'Sawtooth pattern, should be approximable with 1 piece'
    },

    # Test Case 4: Staircase
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 2.0], [2, 3.0], [3, 4.0],
                  [4, 5.0], [5, float('inf')]],
        'epsilon': 0.1,
        'description': 'Strictly increasing staircase'
    },

    # Test Case 5: Large epsilon test
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 2.0], [2, 4.0], [3, 6.0],
                  [4, 4.0], [5, 2.0], [6, 0.0], [7, float('inf')]],
        'epsilon': 3.0,
        'description': 'Large epsilon should allow single piece approximation'
    },

    # Test Case 6: Single point spike
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.0], [2, 5.0], [3, 0.0],
                  [4, 0.0], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single point spike requiring multiple pieces'
    },

    # Test Case 7: Flat with small bump
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0], [2, 1.1], [3, 1.0],
                  [4, 1.0], [5, float('inf')]],
        'epsilon': 0.2,
        'description': 'Mostly flat with small bump'
    },

    # Test Case 8: Alternating values
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0],
                  [4, 0.0], [5, 1.0], [6, 0.0], [7, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating 0 and 1 values'
    },

    # Test Case 9: Gradual increase
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.2], [2, 1.4], [3, 1.6],
                  [4, 1.8], [5, 2.0], [6, float('inf')]],
        'epsilon': 0.5,
        'description': 'Gradual linear increase'
    },

    # Test Case 10: Edge case with minimum pieces
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.0], [2, 0.0], [3, 0.0],
                  [4, 5.0], [5, 5.0], [6, 5.0], [7, 5.0],
                  [8, 0.0], [9, 0.0], [10, 0.0], [11, float('inf')]],
        'epsilon': 1.0,
        'description': 'Large flat regions with single step'
    }
]