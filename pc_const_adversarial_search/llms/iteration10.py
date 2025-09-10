# Few-shot prompt on ChatGPT-4o model
# 10 Sept 2025 8:25AM

test_cases = [
    # 1. Minimal input: Already within tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 1.0], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 2. All values exceed ε difference, must return full segmentation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, float('inf')]],
        "epsilon": 0.4
    },

    # 3. Alternating values just on the boundary of 2ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 1.0], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Values within a tight tube of ε, should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.1], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 5. First and last segment large jump, middle flat
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 10], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 6. High precision floats (test rounding and precision tolerance)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.1000001], [1, 0.1000002], [2, 0.1000003], [3, float('inf')]],
        "epsilon": 0.000001
    },

    # 7. Large number of identical segments except one
    {
        "pc_fx": [[-float('inf'), float('inf')]] + [[i, 2.0] for i in range(10)] + [[10, 5.0], [11, float('inf')]],
        "epsilon": 2.9
    },

    # 8. Edge alignment with ε tube (e.g., segment ends just at ε tolerance)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.6], [2, 2.2], [3, float('inf')]],
        "epsilon": 0.6
    },

    # 9. Piece alternating below and above reference value
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 0.0], [2, 1.0], [3, 0.0], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 10. High variance early, flat tail
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 20], [2, 10], [3, 10], [4, 10], [5, float('inf')]],
        "epsilon": 5.0
    }
]
