# # Zero-shot prompt on ChatGPT-4o model
# # 10 Sept 2025 8:46AM
test_cases = [
    # Test Case 1: All y-values are same, so should merge into 1 segment if ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, float('inf')]],
        "epsilon": 0.1
    },
    # Test Case 2: Zig-zag pattern, just within tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.9], [2, 1.1], [3, float('inf')]],
        "epsilon": 1.0  # Can be merged
    },
    # Test Case 3: Slightly exceeds tolerance between adjacent segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2.1], [2, 1], [3, float('inf')]],
        "epsilon": 1.0  # Should require more than 1 piece
    },
    # Test Case 4: Sudden large jump beyond ε in middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, 5], [3, float('inf')]],
        "epsilon": 0.5  # First two can be merged, third must be separate
    },
    # Test Case 5: Values alternate around central value but all within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 1], [3, 2.5], [4, float('inf')]],
        "epsilon": 1.0  # Can be approximated as single segment
    },
    # Test Case 6: Minimal function, only one segment between infinities
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [10, float('inf')]],
        "epsilon": 0.5  # Already minimal, should return 1 segment
    },
    # Test Case 7: Equal difference between each value but exceeds ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.5  # No two values within range, should return 4 segments
    },
    # Test Case 8: Identical y-values, different x intervals (long, short)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [10, 4], [10.1, 4], [20, float('inf')]],
        "epsilon": 0.0  # All identical, should merge regardless of x-interval
    },
    # Test Case 9: Plateaus with one slight dip exceeding ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 1.4], [3, 3], [4, float('inf')]],
        "epsilon": 1.5  # 1.6 gap — should separate around the dip
    },
    # Test Case 10: Multiple segments with alternating large/small changes
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 3], [2, 2.9], [3, 6], [4, float('inf')]],
        "epsilon": 0.2  # Can only merge [1,3), rest should be separate
    },
]
