# # Zero-shot prompt on ChatGPT-4o model
# # 10 Sept 2025 8:46AM
# test_cases = [
#     # Test Case 1: All values within ε — should be approximated to 1 segment
#     {
#         "description": "Flat region with small variations within ε",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 0.9], [3, 1.05], [4, float('inf')]],
#         "epsilon": 0.1
#     },
#
#     # Test Case 2: Alternating values exactly 2ε apart — should not merge more than one segment
#     {
#         "description": "Alternating jumps of 2ε",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.4], [2, 0.0], [3, 0.4], [4, float('inf')]],
#         "epsilon": 0.2
#     },
#
#     # Test Case 3: Monotonically increasing values within 2ε — should merge all into one segment
#     {
#         "description": "Slow increase within 2ε",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.15], [4, float('inf')]],
#         "epsilon": 0.15
#     },
#
#     # Test Case 4: One large jump — forces a new segment
#     {
#         "description": "One jump beyond 2ε",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.6], [4, float('inf')]],
#         "epsilon": 0.15
#     },
#
#     # Test Case 5: Exact bounds case — check behavior at edge of tolerance
#     {
#         "description": "Max-min range exactly 2ε",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.3], [2, 2.1], [3, 2.4], [4, float('inf')]],
#         "epsilon": 0.2
#     },
#
#     # Test Case 6: Single extreme outlier — should create a new segment only for that
#     {
#         "description": "One extreme outlier",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 10.0], [3, 1.0], [4, float('inf')]],
#         "epsilon": 0.5
#     },
#
#     # Test Case 7: All values equal — should return 1 segment regardless of ε
#     {
#         "description": "All constant values",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.0], [2, 2.0], [3, 2.0], [4, float('inf')]],
#         "epsilon": 0.01
#     },
#
#     # Test Case 8: Gradual decrease across many values — checks greedy vs global
#     {
#         "description": "Long gradual decrease",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 4.8], [2, 4.6], [3, 4.4], [4, float('inf')]],
#         "epsilon": 0.3
#     },
#
#     # Test Case 9: Sharp spike in middle — optimal would isolate the spike
#     {
#         "description": "Spike in middle",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.1], [2, 10.0], [3, 2.2], [4, float('inf')]],
#         "epsilon": 0.25
#     },
#
#     # Test Case 10: Multiple minimal segments needed due to tight ε
#     {
#         "description": "Tight ε forces many pieces",
#         "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 2.0], [3, 2.5], [4, float('inf')]],
#         "epsilon": 0.2
#     }
# ]
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
