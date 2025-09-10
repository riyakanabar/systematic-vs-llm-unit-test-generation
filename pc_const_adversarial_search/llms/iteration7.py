# Few-shot prompt on Gemini 2.5 Pro model
# 9 Sept 2025 7:05PM

test_cases = [
    {
        'name': "1. Simple Case",
        'description': "A basic function to check if the algorithm correctly merges several initial pieces.",
        'pc_fx': [[0, 1.0], [1, 1.2], [2, 0.9], [3, 2.5], [4, 2.6], [5, float('inf')]],
        'epsilon': 0.2,
        'expected_pieces': 2
    },
    {
        'name': "2. Zero Epsilon",
        'description': "With epsilon = 0, no approximation is allowed. The output should be identical to the input function.",
        'pc_fx': [[0, 5.0], [1, 5.1], [2, 5.0], [3, float('inf')]],
        'epsilon': 0.0,
        'expected_pieces': 3
    },
    {
        'name': "3. Large Epsilon",
        'description': "A large epsilon should be sufficient to approximate the entire function with a single constant value.",
        'pc_fx': [[0, 10.0], [1, -5.0], [2, 0.0], [3, 12.0], [4, float('inf')]],
        'epsilon': 10.0,
        'expected_pieces': 1
    },
    {
        'name': "4. Monotonically Increasing",
        'description': "Tests a simple upward trend. The greedy algorithm should correctly segment the staircase.",
        'pc_fx': [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        'epsilon': 0.75,
        'expected_pieces': 3
    },
    {
        'name': "5. Monotonically Decreasing",
        'description': "Tests a simple downward trend, ensuring the logic is symmetrical to the increasing case.",
        'pc_fx': [[0, 5.0], [1, 4.0], [2, 3.0], [3, 2.0], [4, 1.0], [5, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 2
    },
    {
        'name': "6. Oscillating Function",
        'description': "An up-and-down pattern tests the algorithm's handling of non-monotonic data.",
        'pc_fx': [[0, 1.0], [1, 3.0], [2, 1.2], [3, 3.1], [4, 1.1], [5, float('inf')]],
        'epsilon': 1.0,
        'expected_pieces': 2
    },
    {
        'name': "7. Single Spike",
        'description': "A sharp spike should be isolated into its own piece, as it cannot be merged with its neighbors.",
        'pc_fx': [[0, 2.0], [1, 2.1], [2, 2.2], [3, 10.0], [4, 2.1], [5, 2.0], [6, float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 3
    },
    {
        'name': "8. Plateau Breaker",
        'description': "Tests if the algorithm correctly handles a scenario where a single intermediate value prevents two otherwise mergeable sections from being combined.",
        'pc_fx': [[0, 3.0], [1, 3.1], [2, 5.0], [3, 3.05], [4, 2.95], [5, float('inf')]],
        'epsilon': 0.1,
        'expected_pieces': 3
    },
    {
        'name': "9. Varying Staircase",
        'description': "A staircase with varying step heights tests the ability to merge across multiple consecutive steps when their cumulative range is within tolerance.",
        'pc_fx': [[0, 1.0], [1, 1.1], [2, 1.6], [3, 1.7], [4, 2.2], [5, 2.3], [6, float('inf')]],
        'epsilon': 0.3,
        'expected_pieces': 2
    },
    {
        'name': "10. Boundary Condition",
        'description': "Tests the inclusive inequality (<=). The range of a merged segment is exactly 2 * epsilon, which should be allowed.",
        'pc_fx': [[0, 1.0], [1, 2.0], [2, 1.5], [3, 2.5], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_pieces': 2
    }
]