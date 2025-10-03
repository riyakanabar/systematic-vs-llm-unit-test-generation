#2 Oct 11:13AM Claude Sonnet 4.5
test_cases1 = [
    # Test 1: Trivial case - single piece (no merging possible)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 0.5,
        'description': 'Single piece - baseline test'
    },

    # Test 2: Two pieces with exact epsilon difference (boundary case)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [5, 6], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two pieces exactly at epsilon threshold - tests boundary merging'
    },

    # Test 3: Two pieces just under epsilon (should merge)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [5, 5.9], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two pieces within epsilon - should merge to 1 piece'
    },

    # Test 4: Two pieces just over epsilon (should not merge)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [5, 6.1], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two pieces outside epsilon - should remain 2 pieces'
    },

    # Test 5: Multiple pieces with alternating values (challenging merge decision)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 7], [2, 6], [3, 8], [4, 5.5], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'Oscillating values - tests greedy vs optimal merging strategy'
    },

    # Test 6: Long sequence where early merge prevents better overall solution
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10.8], [2, 10.2], [3, 10.9], [4, 10.1],
                  [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Tests if algorithm uses greedy merging that leads to suboptimal solution'
    },

    # Test 7: Three pieces forming a "spike" pattern
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 10], [2, 5.5], [3, float('inf')]],
        'epsilon': 2.5,
        'description': 'Spike pattern - middle piece prevents merging of neighbors'
    },

    # Test 8: Very small epsilon with near-identical values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.01], [2, 5.02], [3, 5.03], [4, float('inf')]],
        'epsilon': 0.015,
        'description': 'Small epsilon - tests precision and optimal grouping of similar values'
    },

    # Test 9: Zero epsilon (no merging allowed)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon with identical values - tests if exact equality is handled'
    },

    # Test 10: Wide range with unequal piece widths
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [0.1, 12], [5, 11], [5.5, 13], [10, float('inf')]],
        'epsilon': 1.5,
        'description': 'Unequal piece widths - tests if algorithm considers piece lengths in optimization'
    }
]
test_cases2 = [
    # Test Case 1: Already optimal - single piece needed
    # All values within epsilon, should return 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 5.2], [2, 4.8], [3, 5.1], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "All values within epsilon - optimal is 1 piece"
    },

    # Test Case 2: Two distinct groups requiring exactly 2 pieces
    # Values [0,1): ~2.0, values [1,3): ~10.0, gap > 2*epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 10.0], [2, 10.1], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "Two clear groups - optimal is 2 pieces"
    },

    # Test Case 3: Greedy vs optimal choice at boundaries
    # Greedy might merge early pieces suboptimally
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.9], [2, 3.0], [3, 3.9], [4, 5.0], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Boundary decision test - greedy might fail"
    },

    # Test Case 4: Monotonically increasing with tight epsilon
    # Each piece differs by exactly epsilon, tests if algorithm is too aggressive
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 3.0], [3, 4.0], [4, 5.0], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Monotonic increase at epsilon boundary - should need all pieces"
    },

    # Test Case 5: Oscillating values
    # Tests ability to find optimal merge points with alternating high/low values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 0.0], [2, 5.0], [3, 0.0], [4, 5.0], [5, float('inf')]],
        "epsilon": 2.0,
        "description": "Oscillating values - tests merge strategy"
    },

    # Test Case 6: Three clusters with small gaps
    # Tests if algorithm correctly identifies 3 optimal pieces when gaps are just above threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 5.0], [3, 5.1], [4, 10.0], [5, 10.1],
                  [6, float('inf')]],
        "epsilon": 0.5,
        "description": "Three clusters - optimal is 3 pieces"
    },

    # Test Case 7: Single outlier in the middle
    # Tests whether algorithm correctly splits around an outlier
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 5.1], [2, 10.0], [3, 5.0], [4, 5.1], [5, float('inf')]],
        "epsilon": 0.3,
        "description": "Single outlier spike - should need 3 pieces"
    },

    # Test Case 8: Epsilon equals max difference
    # Boundary case where epsilon exactly equals the range
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 3.0], [2, 4.0], [3, 5.0], [4, float('inf')]],
        "epsilon": 1.5,
        "description": "Epsilon equals half-range - tests boundary merging"
    },

    # Test Case 9: Very small epsilon (near zero)
    # Should require one piece per original segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.001], [2, 1.002], [3, 1.003], [4, float('inf')]],
        "epsilon": 0.0005,
        "description": "Tiny epsilon - should preserve all pieces"
    },

    # Test Case 10: Large epsilon covering everything
    # Should reduce to 1 piece regardless of value spread
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 100.0], [2, -50.0], [3, 200.0], [4, float('inf')]],
        "epsilon": 150.0,
        "description": "Large epsilon - optimal is 1 piece covering all"
    }
]
test_cases3 = [
    # Test Case 1: Already optimal - single piece should remain single
    {
        "name": "Single piece - already optimal",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece spanning [0,10) with value 5. Should remain 1 piece."
    },

    # Test Case 2: Two pieces with values within epsilon - should merge
    {
        "name": "Two mergeable pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [5, 5.4], [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces with values 5.0 and 5.4 (diff=0.4 < epsilon). Should merge to 1 piece."
    },

    # Test Case 3: Two pieces with values exactly at epsilon boundary
    {
        "name": "Boundary case - exactly epsilon difference",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [5, 6.0], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Two pieces with values differing by exactly epsilon. Tests boundary condition."
    },

    # Test Case 4: Three pieces where first two can merge but not with third
    {
        "name": "Partial merge - three pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [3, 5.3], [6, 10.0], [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Three pieces: 5.0, 5.3, 10.0. First two should merge (diff=0.3), but not with third (diff=4.7). Should result in 2 pieces."
    },

    # Test Case 5: Alternating values - no merging possible
    {
        "name": "Alternating high-low values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 2], [3, 9], [4, 1.5], [5, float('inf')]],
        "epsilon": 0.6,
        "description": "Alternating between low and high values. Should remain 5 pieces as no adjacent pieces are within epsilon."
    },

    # Test Case 6: Multiple consecutive pieces all within epsilon
    {
        "name": "Long chain of mergeable pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [2, 5.2], [4, 5.1], [6, 4.9], [8, 5.3], [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Five pieces with values in range [4.9, 5.3]. All should merge to 1 piece since max-min=0.4 < epsilon."
    },

    # Test Case 7: Greedy vs optimal - requires look-ahead
    {
        "name": "Greedy trap case",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2.5], [3, 2.0], [4, float('inf')]],
        "epsilon": 1.0,
        "description": "Values: 1, 1.5, 2.5, 2.0. Greedy might merge (1,1.5), then (2.5,2.0) = 2 pieces. Optimal: merge all 4 to 1 piece (max-min=1.5, but with right grouping could be optimal)."
    },

    # Test Case 8: Zero epsilon - no merging allowed
    {
        "name": "Zero tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.0,
        "description": "Four pieces with identical values but epsilon=0. Should remain 4 pieces (or merge all if algorithm allows exact matches)."
    },

    # Test Case 9: Large epsilon - everything should merge
    {
        "name": "Large epsilon merges all",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 100], [4, 50], [6, 200], [8, 5], [10, float('inf')]],
        "epsilon": 200.0,
        "description": "Five pieces with widely varying values. Large epsilon should merge all to 1 piece."
    },

    # Test Case 10: Negative values and mixed signs
    {
        "name": "Negative and mixed sign values",
        "pc_fx": [[-float('inf'), float('inf')], [0, -5.0], [2, -4.6], [4, -10.0], [6, 0.5], [8, 0.9],
                  [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Mixed negative and positive values. (-5.0, -4.6) should merge (diff=0.4). (-10.0) separate. (0.5, 0.9) should merge (diff=0.4). Should result in 3 pieces."
    }
]
test_cases4 = [
    # Test 1: Already optimal - no merging possible
    # Adjacent pieces differ by more than 2*epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 8], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'No merging possible - all differences > 2*epsilon'
    },

    # Test 2: All pieces can merge into one
    # All values within epsilon of each other
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.2], [2, 4.9], [3, 5.1], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'All pieces should merge into one'
    },

    # Test 3: Greedy vs optimal choice
    # First two pieces barely mergeable, but optimal solution merges different pairs
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 3], [1, 4], [2, 4.5], [3, 9], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Tests if algorithm chooses optimal merging strategy'
    },

    # Test 4: Single piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece - should return as is'
    },

    # Test 5: Alternating high-low pattern
    # Tests whether algorithm can identify long-range merging opportunities
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1.5], [3, 2.5], [4, 1.8], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Oscillating values - tests merge spanning multiple pieces'
    },

    # Test 6: Exact boundary case
    # Two pieces differ by exactly 2*epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 2.0], [2, 4.0], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'Boundary case - differences exactly at 2*epsilon threshold'
    },

    # Test 7: Negative values with zero
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, -5], [1, -4.5], [2, 0], [3, 0.5], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Mixed negative and positive values'
    },

    # Test 8: Very small epsilon - precision test
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.001], [1, 1.002], [2, 1.003], [3, float('inf')]],
        'epsilon': 0.0005,
        'description': 'Tests precision with very small epsilon'
    },

    # Test 9: Large value differences with tight epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, 0.1], [3, 99.9], [4, float('inf')]],
        'epsilon': 0.1,
        'description': 'Large jumps - no merging should occur'
    },

    # Test 10: Non-uniform interval widths with merge potential
    # Tests if algorithm considers only values, not interval widths
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [0.1, 5.5], [10, 6], [10.5, 4.5], [20, float('inf')]],
        'epsilon': 1.0,
        'description': 'Non-uniform intervals - should merge based on L∞ norm only'
    }
]
test_cases5 = [
    # Test Case 1: Single piece - already optimal
    {
        'name': 'Single piece - trivially optimal',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Only one piece, algorithm should return 1 piece'
    },

    # Test Case 2: Two pieces with values within epsilon - can merge
    {
        'name': 'Two pieces mergeable within epsilon',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [5, 5.5], [10, float('inf')]],
        'epsilon': 0.6,
        'description': 'Two pieces differ by 0.5, should merge to 1 piece with epsilon=0.6'
    },

    # Test Case 3: Two pieces with values exactly at epsilon boundary
    {
        'name': 'Two pieces at exact epsilon boundary',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [5, 6.0], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Values differ by exactly epsilon - tests boundary condition'
    },

    # Test Case 4: Multiple pieces with alternating high-low values
    {
        'name': 'Alternating values - no merging possible',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        'epsilon': 2.0,
        'description': 'Large oscillations prevent merging - should remain 5 pieces'
    },

    # Test Case 5: Gradual increase where greedy might not be optimal
    {
        'name': 'Gradual staircase - tests optimality',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'Can merge [1,2,3] and [4,5] separately, or greedy might miss optimal grouping'
    },

    # Test Case 6: Very small epsilon with tiny differences
    {
        'name': 'Small epsilon with precision test',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.01], [2, 1.02], [3, 1.03], [4, float('inf')]],
        'epsilon': 0.015,
        'description': 'Tests if algorithm handles small tolerances correctly'
    },

    # Test Case 7: Zero epsilon - no merging allowed
    {
        'name': 'Zero epsilon - no merging',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 2], [3, float('inf')]],
        'epsilon': 0.0,
        'description': 'Even identical values cannot merge with zero epsilon'
    },

    # Test Case 8: Large epsilon - everything should merge
    {
        'name': 'Large epsilon - merge all',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 3], [3, 7], [4, 2], [5, float('inf')]],
        'epsilon': 10.0,
        'description': 'All pieces within range of 6, should merge to 1 piece'
    },

    # Test Case 9: Pattern exposing non-optimal greedy behavior
    {
        'name': 'Anti-greedy pattern',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1.5], [2, 0.5], [3, 2], [4, 1], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Greedy left-to-right might choose [0,1.5,0.5] using range 1.5, but optimal might be different groupings'
    },

    # Test Case 10: Negative values with symmetric pattern
    {
        'name': 'Negative values - symmetry test',
        'pc_fx': [[-float('inf'), float('inf')], [0, -5], [1, -3], [2, 0], [3, 3], [4, 5], [5, float('inf')]],
        'epsilon': 2.5,
        'description': 'Tests handling of negative values and whether algorithm finds optimal grouping across zero'
    }
]
test_cases6 = [
    # Test Case 1: Single piece (trivial case - already optimal)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece - trivially optimal'
    },

    # Test Case 2: Two pieces with exact epsilon difference
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [5, 7], [10, float('inf')]],
        'epsilon': 2.0,
        'description': 'Two pieces exactly at epsilon boundary - tests if mergeable'
    },

    # Test Case 3: Two pieces just under epsilon difference
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [5, 6.99], [10, float('inf')]],
        'epsilon': 2.0,
        'description': 'Two pieces just under epsilon - should merge'
    },

    # Test Case 4: Two pieces just over epsilon difference
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [5, 7.01], [10, float('inf')]],
        'epsilon': 2.0,
        'description': 'Two pieces just over epsilon - cannot merge'
    },

    # Test Case 5: Alternating high-low pattern
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        'epsilon': 3.0,
        'description': 'Alternating pattern - tests greedy vs optimal merging strategy'
    },

    # Test Case 6: Monotonically increasing with small steps
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'Monotonic increase - tests if algorithm finds optimal grouping'
    },

    # Test Case 7: Three pieces where middle prevents merging outer two
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [3, 8], [6, 5.5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Middle piece creates barrier - tests non-contiguous merging logic'
    },

    # Test Case 8: Multiple pieces with same value
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [6, 5], [8, float('inf')]],
        'epsilon': 0.1,
        'description': 'Identical values - all should merge into one'
    },

    # Test Case 9: Valley pattern (low-high-low)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [2, 2], [4, 10], [6, float('inf')]],
        'epsilon': 3.0,
        'description': 'Valley pattern - tests if algorithm handles non-monotonic optimally'
    },

    # Test Case 10: Large number of pieces with epsilon = 0
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
                  [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero tolerance - no merging possible, exposes if algorithm changes anything'
    }
]
test_cases7 = [
    # Test 1: Already optimal - single piece needed
    # All values within epsilon of each other
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.2], [2, 4.8], [3, 5.1], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'All values within epsilon - should return 1 piece'
    },

    # Test 2: Forced split at minimum
    # Values just outside epsilon - needs exactly 2 pieces
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [5, 2.1], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two values with distance > 2*epsilon - must use 2 pieces'
    },

    # Test 3: Greedy trap - early merge prevents global optimum
    # [0,1) and [1,2) are close, [2,3) is far; greedy might merge first two
    # but optimal might be different grouping
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 5.0], [3, 5.5], [4, float('inf')]],
        'epsilon': 0.6,
        'description': 'Greedy early merge may prevent optimal solution'
    },

    # Test 4: Alternating high-low pattern
    # Tests if algorithm handles oscillating values optimally
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 0.0], [3, 10.0], [4, 0.0], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating pattern - each piece needs its own segment'
    },

    # Test 5: Monotonic increase with exact epsilon boundaries
    # Values increase by exactly 2*epsilon - tests boundary conditions
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 4.0], [3, 6.0], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Monotonic with exact 2*epsilon steps - boundary test'
    },

    # Test 6: Single outlier in middle
    # Most values similar except one outlier - tests if split optimally
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.1], [2, 15.0], [3, 5.2], [4, 5.0], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Single outlier - should isolate outlier optimally'
    },

    # Test 7: Three distinct clusters
    # Clear grouping into 3 pieces - tests multi-segment optimization
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.1], [2, 5.0], [3, 5.1], [4, 10.0], [5, 10.1],
                  [6, float('inf')]],
        'epsilon': 0.2,
        'description': 'Three distinct clusters - optimal should find 3 pieces'
    },

    # Test 8: Zero epsilon (exact matching required)
    # Only identical consecutive values can be merged
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 3.0], [1, 3.0], [2, 3.0], [3, 4.0], [4, 4.0], [5, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon - only exact matches can merge'
    },

    # Test 9: Large epsilon (everything should merge)
    # Epsilon large enough to merge all pieces
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 3.0], [2, 7.0], [3, 2.0], [4, 9.0], [5, float('inf')]],
        'epsilon': 10.0,
        'description': 'Large epsilon - all should merge into 1 piece'
    },

    # Test 10: Non-greedy optimal - middle value determines split
    # Values [a, b, c] where b-a < epsilon and c-b < epsilon, but c-a > epsilon
    # Greedy might merge a,b then fail, optimal should recognize 2 pieces needed
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.9], [2, 1.7], [3, 2.5], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Transitive epsilon violation - tests optimal piece selection'
    }
]
test_cases8 = [
    # Test Case 1: Single piece is optimal
    # All values within epsilon of each other
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.3], [2, 4.8], [3, 5.2], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'All values within 0.5 - single piece should be optimal'
    },

    # Test Case 2: Forced split - two clear clusters
    # Values alternate between two distant levels
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 10.0], [2, 1.1], [3, 9.9], [4, 1.0], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two distinct value clusters requiring at least 2 pieces'
    },

    # Test Case 3: Staircase pattern
    # Monotonically increasing values with exact epsilon gaps
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, 3.0], [4, 4.0], [5, float('inf')]],
        'epsilon': 0.9,
        'description': 'Staircase with gaps > epsilon - tests greedy vs optimal'
    },

    # Test Case 4: Zero epsilon - each piece must be separate
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 3.0], [3, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero tolerance - no merging possible'
    },

    # Test Case 5: Large epsilon - all mergeable
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 5.0], [2, 3.0], [3, 7.0], [4, 2.0], [5, float('inf')]],
        'epsilon': 10.0,
        'description': 'Large epsilon should merge all pieces into one'
    },

    # Test Case 6: V-shape pattern (down then up)
    # Tests if algorithm considers future values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 3.0], [2, 1.0], [3, 3.0], [4, 5.0], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'V-shape - greedy might split too early'
    },

    # Test Case 7: Exact boundary case
    # Maximum value difference equals exactly 2*epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'Range exactly 2*epsilon - tests boundary condition'
    },

    # Test Case 8: Alternating high-low with tight epsilon
    # Rapid oscillation
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.5], [2, 0.0], [3, 0.5], [4, 0.0], [5, 0.5],
                  [6, float('inf')]],
        'epsilon': 0.2,
        'description': 'High-frequency oscillation beyond epsilon'
    },

    # Test Case 9: Plateau with outliers
    # Most values same, but few outliers
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.0], [2, 10.0], [3, 5.0], [4, 5.0], [5, 5.0],
                  [6, float('inf')]],
        'epsilon': 0.5,
        'description': 'Single outlier disrupts otherwise uniform sequence'
    },

    # Test Case 10: Gradual slope with exact epsilon increments
    # Tests whether algorithm looks ahead optimally
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.6], [2, 1.2], [3, 1.8], [4, 2.4], [5, 3.0],
                  [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Gradual slope - consecutive pairs within epsilon but full range exceeds'
    }
]
test_cases9 = [
    # Test 1: Already optimal - no merging possible
    # Each adjacent pair differs by more than 2*epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 10], [3, float('inf')]],
        'epsilon': 1.5,
        'description': 'Already optimal: all adjacent values differ by > 2*epsilon'
    },

    # Test 2: All pieces can merge into one
    # All values within 2*epsilon range
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.2], [2, 5.1], [3, 5.3], [4, 5.0], [5, float('inf')]],
        'epsilon': 0.2,
        'description': 'All pieces mergeable into single piece'
    },

    # Test 3: Greedy vs optimal merge decision
    # Tests if algorithm considers global optimality vs greedy merging
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Alternating pattern - tests greedy vs optimal strategy'
    },

    # Test 4: Single piece - trivial case
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece - should return 1'
    },

    # Test 5: Large epsilon - should merge everything
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 100], [2, 50], [3, 200], [4, float('inf')]],
        'epsilon': 150,
        'description': 'Very large epsilon - all pieces should merge'
    },

    # Test 6: Zero epsilon - no merging allowed
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon - no merging possible, should return n pieces'
    },

    # Test 7: Clusters of mergeable pieces separated by unmergeable ones
    # Tests if algorithm finds all independent merge opportunities
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 10], [3, 10.5], [4, 20], [5, 20.5],
                  [6, float('inf')]],
        'epsilon': 0.3,
        'description': 'Three separate clusters, each pair mergeable'
    },

    # Test 8: Nested merging opportunity
    # Three consecutive pieces where outer two are similar but middle is different
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 8], [2, 5.5], [3, float('inf')]],
        'epsilon': 2.0,
        'description': 'Tests if middle piece blocks optimal merge of outer pieces'
    },

    # Test 9: Long chain with threshold boundary
    # Values exactly at or near the 2*epsilon boundary
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1.0], [2, 2.0], [3, 3.0], [4, 4.0], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Each adjacent pair exactly at 2*epsilon boundary - tests strict vs non-strict inequality'
    },

    # Test 10: Non-uniform piece widths with varying values
    # Tests if algorithm considers only values (not interval widths) for L∞ norm
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [0.1, 10.5], [5, 10.2], [5.5, 15], [10, float('inf')]],
        'epsilon': 0.3,
        'description': 'Non-uniform widths: first 3 pieces have similar values and should merge despite different widths'
    }
]
test_cases10 = [
    # Test 1: Single piece - trivial case (optimal = 1)
    {
        'name': 'Single piece trivial',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 1,
        'description': 'Single piece, already optimal'
    },

    # Test 2: Two pieces with values differing by exactly 2*epsilon
    {
        'name': 'Boundary case - exactly 2*epsilon difference',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 1,
        'description': 'Values differ by exactly 2*epsilon, should merge to 1 piece'
    },

    # Test 3: Two pieces with values differing by slightly more than 2*epsilon
    {
        'name': 'Just over threshold - cannot merge',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 2.01], [2, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 2,
        'description': 'Values differ by 2.01 > 2*epsilon, cannot merge'
    },

    # Test 4: Alternating high-low pattern
    {
        'name': 'Alternating pattern',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 5,
        'description': 'Cannot merge alternating high-low values'
    },

    # Test 5: Gradually increasing values within epsilon
    {
        'name': 'Gradual increase within epsilon',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.3], [2, 5.6], [3, 5.9], [4, 6.2], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'All values within [4.2, 7.2] range, max spread = 1.2, can merge if 1.2/2 <= epsilon'
    },

    # Test 6: Three distinct groups
    {
        'name': 'Three distinct value groups',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 10], [3, 10.5], [4, 20], [5, 20.5],
                  [6, float('inf')]],
        'epsilon': 0.75,
        'expected_min_pieces': 3,
        'description': 'Three groups: ~0, ~10, ~20, each group mergeable'
    },

    # Test 7: Spike in the middle
    {
        'name': 'Middle spike',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 15], [3, 5], [4, 5], [5, float('inf')]],
        'epsilon': 2.0,
        'description': 'Spike to 15 surrounded by 5s, tests if algorithm considers global vs local optimization'
    },

    # Test 8: Zero epsilon - no merging allowed
    {
        'name': 'Zero tolerance',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.0001], [2, 1.0002], [3, float('inf')]],
        'epsilon': 0.0,
        'expected_min_pieces': 3,
        'description': 'With epsilon=0, only identical values can merge'
    },

    # Test 9: Long sequence with subtle optimization opportunity
    {
        'name': 'Greedy vs optimal trap',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [6, float('inf')]],
        'epsilon': 0.5,
        'expected_min_pieces': 1,
        'description': 'All values in [0,1], range=1, can all merge into one piece with value 0.5'
    },

    # Test 10: Identical values with large epsilon
    {
        'name': 'All identical values',
        'pc_fx': [[-float('inf'), float('inf')], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, float('inf')]],
        'epsilon': 100.0,
        'expected_min_pieces': 1,
        'description': 'All identical values, trivially optimal with 1 piece'
    }
]
test_cases11 = [
    # Test Case 1: Already optimal - constant function
    # All pieces have the same value, should merge into 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Constant function - should merge all into 1 piece',
        'expected_min_pieces': 1
    },

    # Test Case 2: Epsilon exactly at boundary
    # Values differ by exactly 2*epsilon, testing boundary condition
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Values differ by exactly 2*epsilon - boundary test',
        'expected_min_pieces': 1
    },

    # Test Case 3: Epsilon just below boundary
    # Values differ by slightly more than 2*epsilon, cannot merge
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2.01], [2, 3.02], [3, float('inf')]],
        'epsilon': 0.5,
        'description': 'Values exceed 2*epsilon threshold - should require multiple pieces',
        'expected_min_pieces': 3
    },

    # Test Case 4: Alternating pattern
    # High-low-high-low pattern that cannot be simplified
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        'epsilon': 1,
        'description': 'Alternating high-low pattern - tests greedy vs optimal',
        'expected_min_pieces': 5
    },

    # Test Case 5: Gradual increase then sharp drop
    # Tests ability to recognize when merging early pieces is beneficial
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, 2.5], [4, 10], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Gradual increase followed by sharp jump - tests lookahead',
        'expected_min_pieces': 2
    },

    # Test Case 6: Zero epsilon
    # No tolerance for error - each piece must remain separate
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.001], [2, 1.002], [3, float('inf')]],
        'epsilon': 0,
        'description': 'Zero epsilon - no merging allowed',
        'expected_min_pieces': 3
    },

    # Test Case 7: Very large epsilon
    # Tolerance large enough to merge everything
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 100], [2, 50], [3, 200], [4, float('inf')]],
        'epsilon': 100,
        'description': 'Large epsilon - should merge all pieces',
        'expected_min_pieces': 1
    },

    # Test Case 8: Single piece input
    # Minimal input case
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        'epsilon': 1,
        'description': 'Single piece input - already optimal',
        'expected_min_pieces': 1
    },

    # Test Case 9: Symmetric peak
    # Values increase then decrease symmetrically
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 2], [4, 1], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Symmetric peak - tests if algorithm finds optimal midpoint',
        'expected_min_pieces': 2
    },

    # Test Case 10: Nested ranges test
    # Some pieces can be merged but others cannot - tests optimal grouping
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, 5.2], [3, 10], [4, 10.5], [5, 10.3],
                  [6, float('inf')]],
        'epsilon': 0.6,
        'description': 'Two groups of similar values - should identify 2 optimal pieces',
        'expected_min_pieces': 2
    }
]
test_cases12 = [
    # Test Case 1: Single piece function - should return 1 piece
    {
        'name': 'Single piece - trivial case',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single constant piece, algorithm must return 1 piece'
    },

    # Test Case 2: Two pieces with values within epsilon - should merge to 1
    {
        'name': 'Two mergeable pieces',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [5, 5.5], [10, float('inf')]],
        'epsilon': 0.6,
        'description': 'Two pieces differ by 0.5, with epsilon=0.6 should merge to 1 piece'
    },

    # Test Case 3: Two pieces just outside epsilon - must stay 2 pieces
    {
        'name': 'Two non-mergeable pieces (boundary)',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [5, 6.1], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two pieces differ by 1.1, with epsilon=1.0 must stay 2 pieces'
    },

    # Test Case 4: Alternating high-low pattern - tests greedy vs optimal
    {
        'name': 'Alternating values - greedy trap',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating 0,2,0,2,0 pattern. Greedy might keep alternating, optimal merges all to 1 piece at value 1'
    },

    # Test Case 5: Staircase increasing - tests optimal chunking
    {
        'name': 'Staircase increasing',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, float('inf')]],
        'epsilon': 2.5,
        'description': 'Values 1,2,3,4,5,6. With epsilon=2.5, optimal is 2 pieces: [1-3.5] and [3.5-6]'
    },

    # Test Case 6: Three pieces with middle piece as outlier
    {
        'name': 'Middle outlier spike',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [2, 10], [3, 5.2], [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Values 5, 10(spike), 5.2. Cannot merge all; optimal is likely 2 pieces (merge first and last)'
    },

    # Test Case 7: Zero epsilon - no merging allowed
    {
        'name': 'Zero epsilon - no tolerance',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 1.00001], [3, float('inf')]],
        'epsilon': 0.0,
        'description': 'With epsilon=0, even tiny differences prevent merging. Should return 2 pieces (first two merge)'
    },

    # Test Case 8: Large epsilon - everything should merge
    {
        'name': 'Large epsilon - merge all',
        'pc_fx': [[-float('inf'), float('inf')], [0, -10], [1, 0], [2, 5], [3, 20], [4, 15], [5, float('inf')]],
        'epsilon': 15.0,
        'description': 'Values -10,0,5,20,15 with range 30. Epsilon=15 should allow merging to 1 piece at value 5'
    },

    # Test Case 9: Symmetric pattern around center value
    {
        'name': 'Symmetric around center',
        'pc_fx': [[-float('inf'), float('inf')], [0, 3], [1, 5], [2, 7], [3, 5], [4, 3], [5, float('inf')]],
        'epsilon': 2.0,
        'description': 'Symmetric 3,5,7,5,3. With epsilon=2, optimal merges to 1 piece at value 5'
    },

    # Test Case 10: Edge case with very unequal piece widths
    {
        'name': 'Unequal piece widths',
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [0.1, 8], [10, 9], [20, float('inf')]],
        'epsilon': 1.0,
        'description': 'Short piece (width 0.1) with value 8 between longer pieces (10,9). Tests if algorithm considers piece width in optimization'
    }
]
test_cases13 = [
    # Test Case 1: Simple monotonic increase - should merge all pieces
    # All values within 2*epsilon, optimal is 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 2.0], [3, 2.5], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Monotonic increase within tolerance - should merge to 1 piece',
        'expected_min_pieces': 1
    },

    # Test Case 2: Alternating high-low values - cannot merge adjacent pieces
    # Forces algorithm to keep separate pieces due to large jumps
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 0.0], [3, 10.0], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating values - exposes greedy vs optimal merging',
        'expected_min_pieces': 4
    },

    # Test Case 3: Three pieces where middle can bridge to either side
    # Tests if algorithm considers all merge possibilities
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.5], [2, 4.0], [3, float('inf')]],
        'epsilon': 1.5,
        'description': 'Middle piece can bridge left or right - tests merge strategy',
        'expected_min_pieces': 1
    },

    # Test Case 4: Epsilon exactly at boundary
    # Tests strict inequality vs non-strict inequality handling
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 4.0], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'Values exactly at 2*epsilon boundary - tests boundary conditions',
        'expected_min_pieces': 2
    },

    # Test Case 5: Single piece input
    # Edge case with minimal input
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [10, float('inf')]],
        'epsilon': 0.5,
        'description': 'Single piece - trivial case',
        'expected_min_pieces': 1
    },

    # Test Case 6: Zero epsilon with identical values
    # Tests if algorithm handles epsilon=0 correctly
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 3.0], [1, 3.0], [2, 3.0], [3, 3.0], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon with identical values - should merge all',
        'expected_min_pieces': 1
    },

    # Test Case 7: Zero epsilon with different values
    # Tests if algorithm keeps all pieces when epsilon=0 and values differ
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 3.0], [3, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon with different values - cannot merge',
        'expected_min_pieces': 3
    },

    # Test Case 8: Long sequence with groups
    # Tests if algorithm finds optimal grouping (groups of similar values)
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.2], [2, 1.1],  # Group 1
                  [3, 5.0], [4, 5.3], [5, 5.1],  # Group 2
                  [6, 9.0], [7, 9.2], [8, 9.1],  # Group 3
                  [9, float('inf')]],
        'epsilon': 0.5,
        'description': 'Three clusters - tests if algorithm finds cluster boundaries',
        'expected_min_pieces': 3
    },

    # Test Case 9: Gradual slope that requires splitting
    # Tests if greedy merging fails vs optimal dynamic programming
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.8], [2, 1.6], [3, 2.4], [4, 3.2], [5, 4.0],
                  [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Gradual slope - greedy might fail to find optimal split',
        'expected_min_pieces': 2
    },

    # Test Case 10: Large epsilon that allows full merge
    # Tests if algorithm correctly merges when epsilon is very large
    {
        'pc_fx': [[-float('inf'), float('inf')],
                  [0, -100.0], [1, 0.0], [2, 100.0], [3, -50.0], [4, 200.0],
                  [5, float('inf')]],
        'epsilon': 200.0,
        'description': 'Large epsilon - should merge all pieces',
        'expected_min_pieces': 1
    }
]
test_cases14 = [
    # Test Case 1: Single piece (already optimal)
    # No merging possible - each piece differs by more than epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 10], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'No merging possible - values differ significantly'
    },

    # Test Case 2: All pieces identical
    # Should merge into single piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, float('inf')]],
        'epsilon': 0.0,
        'description': 'All identical values - should merge to 1 piece'
    },

    # Test Case 3: Gradual increase within tolerance
    # Tests greedy vs optimal merging strategy
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.4], [2, 1.8], [3, 2.2], [4, 2.6], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Gradual increase - greedy might miss optimal grouping'
    },

    # Test Case 4: Alternating high-low pattern
    # Tests if algorithm recognizes oscillating patterns
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, 10], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating pattern - cannot merge adjacent pieces'
    },

    # Test Case 5: Three pieces where middle can bridge gap
    # Critical test: [1, 5, 2] with epsilon=2 - can merge all to value 3 (L∞=2)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 2], [3, float('inf')]],
        'epsilon': 2.0,
        'description': 'Middle value bridges gap - optimal uses middle value'
    },

    # Test Case 6: Narrow spike in middle
    # Tests if algorithm handles outlier values optimally
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 15], [3, 5.2], [4, 5], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Spike value forces split - cannot merge around it'
    },

    # Test Case 7: Monotonic sequence at boundary
    # Tests epsilon boundary conditions
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        'epsilon': 2.0,
        'description': 'Monotonic at exactly epsilon boundary (L∞=2 for range [0,4])'
    },

    # Test Case 8: Long tail with small variations
    # Tests if algorithm optimally handles many similar values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10.1], [2, 9.9], [3, 10.05],
                  [4, 9.95], [5, 10.02], [6, 9.98], [7, 10.03], [8, float('inf')]],
        'epsilon': 0.2,
        'description': 'Many values clustered around 10 - should merge to 1 piece'
    },

    # Test Case 9: Two clusters separated by gap
    # Tests if algorithm recognizes disconnected optimal groups
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1.3], [3, 10], [4, 10.5], [5, 10.3],
                  [6, float('inf')]],
        'epsilon': 0.6,
        'description': 'Two separate clusters - should result in 2 pieces'
    },

    # Test Case 10: Zero epsilon with floating point values
    # Tests exact equality handling
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0000000001], [2, 1.0], [3, 2.0], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero tolerance with floating point - tests exact equality'
    }
]
test_cases15 = [
    # Test Case 1: Single piece (trivial case - should return 1 piece)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece - trivial optimal case'
    },

    # Test Case 2: Two pieces with values within epsilon (should merge to 1)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [5, 5.3], [10, float('inf')]],
        'epsilon': 0.5,
        'description': 'Two pieces mergeable within epsilon - tests if algorithm merges optimally'
    },

    # Test Case 3: Two pieces with values outside epsilon (cannot merge - should return 2)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [5, 7.0], [10, float('inf')]],
        'epsilon': 0.5,
        'description': 'Two pieces not mergeable - tests if algorithm recognizes necessity of 2 pieces'
    },

    # Test Case 4: Alternating high-low pattern (worst case for greedy approaches)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, 10], [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating pattern - exposes non-optimal greedy merging'
    },

    # Test Case 5: Three pieces in ascending order with middle piece as bottleneck
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [3, 5.0], [6, 9.0], [10, float('inf')]],
        'epsilon': 3.0,
        'description': 'Three pieces where middle piece determines if merge is possible'
    },

    # Test Case 6: Multiple pieces with same value (should merge to 1)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 7.5], [2, 7.5], [4, 7.5], [6, 7.5], [8, float('inf')]],
        'epsilon': 0.1,
        'description': 'All same values - tests if algorithm merges identical pieces'
    },

    # Test Case 7: Epsilon is zero (no merging possible)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon - no pieces should merge, optimal = n pieces'
    },

    # Test Case 8: Long sequence with gradual increase (tests interval selection)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8],
                  [8, float('inf')]],
        'epsilon': 2.5,
        'description': 'Gradual increase - tests optimal interval partitioning with L-infinity constraint'
    },

    # Test Case 9: Two groups of similar values separated by outlier
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2.0], [1, 2.2], [2, 2.1], [3, 10.0], [4, 7.8], [5, 8.1], [6, 7.9],
                  [7, float('inf')]],
        'epsilon': 0.3,
        'description': 'Two clusters separated by outlier - tests if algorithm segments optimally'
    },

    # Test Case 10: Boundary case with very small pieces and tight epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.00], [0.1, 5.05], [0.2, 4.95], [0.3, 5.10], [0.4, 4.90],
                  [0.5, float('inf')]],
        'epsilon': 0.08,
        'description': 'Small variations with tight epsilon - exposes precision and boundary handling'
    }
]
test_cases16 = [
    # Test 1: Already optimal - single piece needed
    # All y-values within 2*epsilon, should return 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.3], [2, 4.8], [3, 5.2], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'All values within epsilon - should merge to 1 piece'
    },

    # Test 2: Two distinct groups requiring exactly 2 pieces
    # First group [0,2): y in [1.0, 1.5], second group [2,4): y in [10.0, 10.5]
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 10.0], [3, 10.5], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Two well-separated groups - optimal is 2 pieces'
    },

    # Test 3: Boundary case - values exactly at epsilon boundary
    # Tests if algorithm handles y2 - y1 = 2*epsilon exactly
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 4.0], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'Values exactly at 2*epsilon apart - tests boundary handling'
    },

    # Test 4: Greedy trap - early merge prevents global optimum
    # [0,1): y=0, [1,2): y=0.9, [2,3): y=0, [3,4): y=0.9
    # Greedy might merge [0,2) but optimal could be different grouping
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.9], [2, 0.0], [3, 0.9], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Alternating values - tests greedy vs optimal merging'
    },

    # Test 5: Single piece input - trivial case
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece input - should return 1 piece'
    },

    # Test 6: Ascending staircase just beyond epsilon
    # Each step increases by slightly more than 2*epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 1.1], [2, 2.2], [3, 3.3], [4, 4.4], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Ascending staircase - no merging possible, needs n pieces'
    },

    # Test 7: Three clusters with minimal separation
    # Tests if algorithm can identify 3 distinct groups
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.2], [2, 5.0], [3, 5.2], [4, 9.0], [5, 9.2],
                  [6, float('inf')]],
        'epsilon': 0.3,
        'description': 'Three distinct clusters - optimal is 3 pieces'
    },

    # Test 8: Epsilon = 0 - no tolerance
    # Each piece must remain separate
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 3.0], [3, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero tolerance - all pieces must remain separate'
    },

    # Test 9: Large epsilon - everything should merge
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 20.0], [3, 30.0], [4, float('inf')]],
        'epsilon': 20.0,
        'description': 'Very large epsilon - should merge all to 1 piece'
    },

    # Test 10: Valley pattern - tests non-monotonic merging
    # y-values: 5, 3, 1, 3, 5 - creates a valley
    # Tests if algorithm handles non-monotonic patterns optimally
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 3.0], [2, 1.0], [3, 3.0], [4, 5.0], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'Valley pattern - tests handling of non-monotonic values'
    }
]
test_cases17 = [
    # Test 1: Adjacent pieces with values within epsilon - should merge
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.3], [2, 5.5], [3, float('inf')]],
        'epsilon': 0.6,
        'description': 'Adjacent pieces all within epsilon range - optimal should merge all'
    },

    # Test 2: Alternating high-low values - cannot merge non-adjacent
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 10.0], [2, 1.5], [3, 10.5], [4, float('inf')]],
        'epsilon': 0.6,
        'description': 'Alternating values - tests if algorithm incorrectly merges non-adjacent pieces'
    },

    # Test 3: Exact epsilon boundary - critical threshold test
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'Values exactly at epsilon boundaries - tests strict vs non-strict inequalities'
    },

    # Test 4: Single outlier preventing merge
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.2], [2, 7.5], [3, 5.3], [4, 5.1], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'One outlier in middle prevents merging otherwise compatible pieces'
    },

    # Test 5: Multiple valid groupings - tests optimality
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.4], [2, 5.0], [3, 5.4], [4, 9.0], [5, 9.4],
                  [6, float('inf')]],
        'epsilon': 0.5,
        'description': 'Three separate groups - tests if algorithm finds globally optimal grouping'
    },

    # Test 6: Already optimal - no merge possible
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 5.0], [2, 10.0], [3, float('inf')]],
        'epsilon': 2.0,
        'description': 'All pieces too far apart - should remain unchanged'
    },

    # Test 7: Greedy vs optimal trade-off
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.5], [2, 2.0], [3, 3.5], [4, float('inf')]],
        'epsilon': 1.6,
        'description': 'Greedy might merge [0,1,2] but optimal is [0,1],[2,3] - exposes greedy failures'
    },

    # Test 8: Very small epsilon - tests numerical precision
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0001], [2, 1.0002], [3, float('inf')]],
        'epsilon': 0.0001,
        'description': 'Tiny epsilon tests floating point precision handling'
    },

    # Test 9: Large range with gradual drift
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10.0], [1, 10.3], [2, 10.6], [3, 10.9], [4, 11.2], [5, 11.5],
                  [6, float('inf')]],
        'epsilon': 0.5,
        'description': 'Gradual drift - tests sliding window vs fixed window approaches'
    },

    # Test 10: Zero epsilon - no approximation allowed
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.0], [2, 5.0], [3, 7.0], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon - only identical consecutive values can merge'
    }
]
test_cases18 = [
    # Test 1: Already optimal - uniform values within epsilon
    # All pieces have values within epsilon of each other, should merge to 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.3], [2, 4.8], [3, 5.2], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'All values within epsilon - should merge to single piece'
    },

    # Test 2: Two distinct groups - tests merging decision boundaries
    # Values alternate between ~2 and ~8, epsilon doesn't allow merging across groups
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [1, 8], [2, 2.5], [3, 7.8], [4, 2.2], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two distinct value groups - should form 2 pieces minimum'
    },

    # Test 3: Greedy vs optimal distinction
    # Greedy might take [10,10.5,11] as one piece, forcing [15] alone
    # Optimal should pair [10,10.5] and [11,15]
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10.5], [2, 11], [3, 15], [4, float('inf')]],
        'epsilon': 2.5,
        'description': 'Tests greedy vs optimal - requires look-ahead'
    },

    # Test 4: Single piece already optimal
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece input - trivially optimal'
    },

    # Test 5: Monotonic increasing with tight epsilon
    # Strictly increasing values, small epsilon forces many pieces
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, float('inf')]],
        'epsilon': 0.5,
        'description': 'Monotonic increase - each step exceeds epsilon'
    },

    # Test 6: Alternating pattern - tests non-contiguous merging
    # Pattern: 0, 10, 0.5, 10.5, 1, 11 - should we group similar values?
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0.5], [3, 10.5], [4, 1], [5, 11],
                  [6, float('inf')]],
        'epsilon': 1.5,
        'description': 'Alternating high-low pattern - tests merging strategy'
    },

    # Test 7: Boundary case - values at exact epsilon distance
    # Values differ by exactly epsilon - algorithm must handle equality correctly
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 0.75], [2, 1.5], [3, 2.25], [4, float('inf')]],
        'epsilon': 0.75,
        'description': 'Values at exact epsilon boundaries - edge precision test'
    },

    # Test 8: Long constant plateau followed by spike
    # Many identical values then a jump - tests whether algorithm exploits constancy
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 10], [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Long plateau then spike - should form 2 pieces'
    },

    # Test 9: Challenging optimization problem
    # Values: 0, 5, 1, 6, 2, 7 with epsilon=3
    # Greedy might go [0,5], [1], [6], [2], [7] or similar
    # Optimal might be [0,1,2] and [5,6,7]
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 1], [3, 6], [4, 2], [5, 7], [6, float('inf')]],
        'epsilon': 3.0,
        'description': 'Complex interleaving - distinguishes greedy from optimal'
    },

    # Test 10: Zero epsilon - no approximation allowed
    # Each value must remain separate unless identical
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 1.01], [3, 1.0], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon - only identical values can merge'
    }
]
test_cases19 = [
    # Test 1: Single piece required - all values within epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.3], [2, 4.8], [3, 5.2], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'All values within epsilon - should merge to 1 piece',
        'expected_min_pieces': 1
    },

    # Test 2: No merging possible - alternating high/low values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 0.0], [3, 10.0], [4, 0.0], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating values exceeding 2*epsilon - no merging possible',
        'expected_min_pieces': 5
    },

    # Test 3: Boundary case - values exactly at epsilon distance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 6.0], [2, 7.0], [3, 8.0], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Values exactly epsilon apart - tests boundary merging',
        'expected_min_pieces': 1
    },

    # Test 4: Greedy trap - local merging prevents global optimum
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.5], [2, 1.2], [3, 2.3], [4, 1.1], [5, float('inf')]],
        'epsilon': 0.8,
        'description': 'Tests if algorithm is greedy vs optimal (should be 2 pieces optimally)',
        'expected_min_pieces': 2
    },

    # Test 5: Long plateau with outliers at ends
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 5.0], [2, 5.0], [3, 5.0], [4, 5.0], [5, 10.0],
                  [6, float('inf')]],
        'epsilon': 0.1,
        'description': 'Plateau in middle with outliers - should create 3 pieces',
        'expected_min_pieces': 3
    },

    # Test 6: Two distinct groups separated by large gap
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 1.2], [3, 10.0], [4, 10.5], [5, 10.2],
                  [6, float('inf')]],
        'epsilon': 0.6,
        'description': 'Two clusters with large gap - should create 2 pieces',
        'expected_min_pieces': 2
    },

    # Test 7: Monotonic increasing just beyond epsilon threshold
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 1.1], [2, 2.2], [3, 3.3], [4, 4.4], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Monotonic increase with cumulative drift beyond epsilon',
        'expected_min_pieces': 3
    },

    # Test 8: V-shape pattern - tests merging across valleys
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 4.0], [2, 3.0], [3, 4.0], [4, 5.0], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'V-shape - tests if algorithm can merge across minimum',
        'expected_min_pieces': 1
    },

    # Test 9: Single outlier in uniform region
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10.0], [1, 10.0], [2, 15.0], [3, 10.0], [4, 10.0],
                  [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single spike - should isolate outlier (3 pieces)',
        'expected_min_pieces': 3
    },

    # Test 10: Staircase with exact 2*epsilon steps
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.0], [2, 2.0], [3, 2.0], [4, 4.0], [5, 4.0],
                  [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Staircase pattern with pairs - should create 3 pieces',
        'expected_min_pieces': 3
    }
]
test_cases20 = [
    # Test 1: Single piece - already optimal
    {
        'name': 'single_piece_optimal',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece - algorithm should return 1 piece (trivially optimal)'
    },

    # Test 2: Two pieces that can be merged
    {
        'name': 'two_pieces_mergeable',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [5, 5.5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two pieces with values differing by 0.5, epsilon=1.0 - should merge to 1 piece'
    },

    # Test 3: Two pieces that cannot be merged
    {
        'name': 'two_pieces_not_mergeable',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [5, 7.5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two pieces with values differing by 2.5, epsilon=1.0 - should remain 2 pieces'
    },

    # Test 4: Three pieces where outer two can merge but not with middle
    {
        'name': 'three_pieces_outer_similar',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [3, 10.0], [6, 5.2], [10, float('inf')]],
        'epsilon': 0.5,
        'description': 'First and third pieces differ by 0.2 (can merge), but middle is 5.0 away - optimal is 2 pieces if greedy fails'
    },

    # Test 5: Oscillating values - tests greedy vs optimal
    {
        'name': 'oscillating_values',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1.5], [3, 2.8], [4, 1.2], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Oscillating pattern where greedy merging might miss optimal grouping'
    },

    # Test 6: Gradual increase - all within epsilon of neighbors
    {
        'name': 'gradual_increase',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 2.0], [3, 2.5], [4, 3.0], [5, float('inf')]],
        'epsilon': 0.6,
        'description': 'Each piece within epsilon of neighbors, but first and last differ by 2.0 - tests transitivity handling'
    },

    # Test 7: Zero epsilon - no merging possible
    {
        'name': 'zero_epsilon',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0001], [2, 1.0002], [3, float('inf')]],
        'epsilon': 0.0,
        'description': 'Epsilon = 0 means no pieces can merge unless identical'
    },

    # Test 8: Large epsilon - all should merge
    {
        'name': 'large_epsilon',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 100], [2, 50], [3, -20], [4, 75], [5, float('inf')]],
        'epsilon': 150.0,
        'description': 'Very large epsilon should allow all pieces to merge into 1'
    },

    # Test 9: Exact epsilon boundary
    {
        'name': 'exact_epsilon_boundary',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [2, 6.0], [4, 7.0], [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Each consecutive pair differs by exactly epsilon - tests boundary condition'
    },

    # Test 10: Non-uniform intervals with clustered values
    {
        'name': 'clustered_values_different_intervals',
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [0.1, 10.3], [0.2, 10.1], [5, 20], [5.5, 20.4],
                  [10, float('inf')]],
        'epsilon': 0.5,
        'description': 'Two clusters of similar values separated by large gap - optimal should find 2 pieces'
    }
]
test_cases21 = [
    # Test Case 1: Single piece is optimal (all values within epsilon)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.5], [2, 5.3], [3, 4.8], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'All values within epsilon range - single piece should be optimal'
    },

    # Test Case 2: Requires exactly 2 pieces (values jump beyond epsilon)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 5.0], [3, 5.5], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Clear jump at x=2 - requires exactly 2 pieces'
    },

    # Test Case 3: Greedy vs optimal - oscillating values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 0.5], [3, 2.5], [4, 1.0], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'Oscillating values - greedy might split suboptimally'
    },

    # Test Case 4: Monotonically increasing with small epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.5], [2, 1.0], [3, 1.5], [4, 2.0], [5, 2.5],
                  [6, float('inf')]],
        'epsilon': 0.6,
        'description': 'Monotonic increase - tests optimal grouping of gradual changes'
    },

    # Test Case 5: Extreme values at boundaries
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10.0], [1, 0.0], [2, 0.2], [3, 0.1], [4, 9.8], [5, float('inf')]],
        'epsilon': 0.5,
        'description': 'Extreme jumps at start and end - tests boundary handling'
    },

    # Test Case 6: All identical values (trivial optimal = 1 piece)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 3.0], [1, 3.0], [2, 3.0], [3, 3.0], [4, 3.0], [5, float('inf')]],
        'epsilon': 0.1,
        'description': 'All identical values - must return 1 piece'
    },

    # Test Case 7: Epsilon = 0 (each piece must be separate)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 3.0], [3, 4.0], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero tolerance - must return n pieces'
    },

    # Test Case 8: Large epsilon (everything fits in one piece)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, -100.0], [1, 50.0], [2, 200.0], [3, -50.0], [4, float('inf')]],
        'epsilon': 500.0,
        'description': 'Very large epsilon - should return 1 piece'
    },

    # Test Case 9: Alternating high-low pattern (tests look-ahead)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 0.5], [3, 10.5], [4, 1.0], [5, 11.0],
                  [6, float('inf')]],
        'epsilon': 2.0,
        'description': 'Alternating pattern - greedy might create more pieces than optimal'
    },

    # Test Case 10: Narrow spike in the middle
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.2], [2, 5.1], [3, 15.0], [4, 5.3], [5, 5.0], [6, 5.1],
                  [7, float('inf')]],
        'epsilon': 0.5,
        'description': 'Single spike surrounded by similar values - tests if spike is isolated optimally'
    }
]
test_cases22 = [
    # Test Case 1: Already optimal - single piece sufficient
    # All values within epsilon, should return 1 piece
    {
        'name': 'Single piece sufficient',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.2], [2, 4.8], [3, 5.1], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_min_pieces': 1,
        'description': 'All values are within epsilon=0.5 of each other, should merge into 1 piece'
    },

    # Test Case 2: Strict boundary - forces split exactly at epsilon threshold
    # Tests if algorithm handles exact epsilon boundary correctly
    {
        'name': 'Exact epsilon boundary',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 2,
        'description': 'Values differ by exactly epsilon, tests boundary handling (0 to 2.0 needs split)'
    },

    # Test Case 3: Alternating high-low pattern
    # Tests greedy vs optimal: greedy might make suboptimal splits
    {
        'name': 'Alternating values',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 3.0], [2, 1.5], [3, 3.5], [4, 2.0], [5, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 3,
        'description': 'Alternating pattern where greedy might split prematurely'
    },

    # Test Case 4: Monotonic increasing with large jump
    # Tests if algorithm correctly identifies where jump exceeds 2*epsilon
    {
        'name': 'Monotonic with jump',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 2.0], [3, 5.0], [4, 5.5], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Monotonic sequence with one large jump from 2.0 to 5.0'
    },

    # Test Case 5: Very small epsilon with close values
    # Stress test for numerical precision
    {
        'name': 'Small epsilon precision test',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.001], [2, 1.002], [3, 1.0051], [4, float('inf')]],
        'epsilon': 0.002,
        'expected_min_pieces': 2,
        'description': 'Tests numerical precision: 1.0 to 1.0051 exceeds 2*epsilon=0.004'
    },

    # Test Case 6: Single outlier in middle
    # Tests if algorithm can "skip over" outlier optimally
    {
        'name': 'Middle outlier',
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.1], [2, 10.0], [3, 5.2], [4, 5.0], [5, float('inf')]],
        'epsilon': 0.5,
        'expected_min_pieces': 3,
        'description': 'Outlier at position 2 forces splits'
    },

    # Test Case 7: Staircase pattern
    # Each step is within epsilon but accumulated difference grows
    {
        'name': 'Staircase accumulation',
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.6], [2, 1.2], [3, 1.8], [4, 2.4], [5, 3.0],
                  [6, float('inf')]],
        'epsilon': 0.7,
        'expected_min_pieces': 3,
        'description': 'Each step is 0.6, but range grows: tests lookahead vs greedy'
    },

    # Test Case 8: Two separate clusters
    # Tests if algorithm correctly identifies independent regions
    {
        'name': 'Two distinct clusters',
        'pc_fx': [[-float('inf'), float('inf')], [0, 2.0], [1, 2.3], [2, 2.1], [3, 8.0], [4, 8.2], [5, 8.1],
                  [6, float('inf')]],
        'epsilon': 0.5,
        'expected_min_pieces': 2,
        'description': 'Two clusters: [2.0-2.3] and [8.0-8.2], should need exactly 2 pieces'
    },

    # Test Case 9: Epsilon zero - no merging possible
    # Edge case where each piece must remain separate
    {
        'name': 'Zero epsilon',
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 3.0], [3, float('inf')]],
        'epsilon': 0.0,
        'expected_min_pieces': 3,
        'description': 'Zero epsilon means no approximation, each distinct value needs own piece'
    },

    # Test Case 10: Large epsilon - everything mergeable
    # Tests if algorithm recognizes when single piece suffices
    {
        'name': 'Large epsilon merge all',
        'pc_fx': [[-float('inf'), float('inf')], [0, -10.0], [1, 5.0], [2, 20.0], [3, -5.0], [4, 15.0],
                  [5, float('inf')]],
        'epsilon': 20.0,
        'expected_min_pieces': 1,
        'description': 'Range is [-10, 20] = 30, with epsilon=20 all values should merge (max-min ≤ 2*epsilon)'
    }
]
test_cases23 = [
    # Test 1: Single piece - already optimal
    {
        "name": "single_piece_optimal",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece, already optimal - should return 1 piece"
    },

    # Test 2: Two pieces with values within epsilon - can merge
    {
        "name": "two_pieces_mergeable",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [5, 5.5], [10, float('inf')]],
        "epsilon": 0.6,
        "description": "Two pieces differing by 0.5, epsilon=0.6 - should merge to 1 piece"
    },

    # Test 3: Two pieces with values outside epsilon - cannot merge
    {
        "name": "two_pieces_not_mergeable",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [5, 6.5], [10, float('inf')]],
        "epsilon": 0.5,
        "description": "Two pieces differing by 1.5, epsilon=0.5 - should stay 2 pieces"
    },

    # Test 4: Alternating high-low values (zigzag pattern)
    {
        "name": "zigzag_pattern",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 2.0,
        "description": "Alternating 0 and 10, epsilon=2 - tests greedy vs optimal merging"
    },

    # Test 5: Monotonically increasing values
    {
        "name": "monotonic_increasing",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 1.5,
        "description": "Values 1,2,3,4,5 with epsilon=1.5 - tests optimal grouping"
    },

    # Test 6: Step function with large jump in middle
    {
        "name": "large_jump_middle",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 10], [4, 10.1], [5, 10.2],
                  [6, float('inf')]],
        "epsilon": 0.5,
        "description": "Two clusters (around 1 and 10) separated by large jump - should get 2 pieces"
    },

    # Test 7: Three pieces where middle prevents merging first and last
    {
        "name": "blocking_middle_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 8], [4, 5.5], [6, float('inf')]],
        "epsilon": 1.0,
        "description": "First=5, Middle=8, Last=5.5. Middle blocks merging all three"
    },

    # Test 8: Epsilon equals exact difference - boundary case
    {
        "name": "epsilon_equals_difference",
        "pc_fx": [[-float('inf'), float('inf')], [0, 3.0], [1, 5.0], [2, float('inf')]],
        "epsilon": 2.0,
        "description": "Difference exactly equals epsilon - tests boundary condition"
    },

    # Test 9: Many pieces with same value
    {
        "name": "constant_value_multiple_pieces",
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, float('inf')]],
        "epsilon": 0.1,
        "description": "All pieces have same value - should merge to 1 piece"
    },

    # Test 10: Non-greedy optimal - requires look-ahead
    {
        "name": "non_greedy_optimal",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 1], [3, 3], [4, 2], [5, float('inf')]],
        "epsilon": 1.5,
        "description": "Values: 0,2,1,3,2. Greedy might give suboptimal; optimal requires strategic merging"
    }
]
test_cases24 = [
    # Test Case 1: Single piece (already optimal)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece - trivially optimal'
    },

    # Test Case 2: Two pieces with values differing by exactly 2*epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [5, 2], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Boundary case: values differ by exactly 2*epsilon, should merge'
    },

    # Test Case 3: Two pieces with values differing by slightly more than 2*epsilon
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [5, 2.1], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Boundary case: values differ by 2.1 (> 2*epsilon), cannot merge'
    },

    # Test Case 4: Three pieces where middle can bridge outer two
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [3, 1], [6, 2], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Three pieces mergeable into one via middle value'
    },

    # Test Case 5: Alternating high-low pattern
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating pattern - tests greedy vs optimal merging'
    },

    # Test Case 6: Staircase increasing pattern
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, float('inf')]],
        'epsilon': 1.5,
        'description': 'Monotonic staircase - tests consecutive merging strategy'
    },

    # Test Case 7: Very small epsilon (near-zero tolerance)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.001], [2, 1.002], [3, float('inf')]],
        'epsilon': 0.0005,
        'description': 'Very small epsilon - tests numerical precision'
    },

    # Test Case 8: Pyramid pattern (up then down)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [2, 2], [4, 4], [6, 2], [8, 0], [10, float('inf')]],
        'epsilon': 1.5,
        'description': 'Pyramid pattern - non-monotonic, tests look-ahead merging'
    },

    # Test Case 9: Many pieces with identical values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, float('inf')]],
        'epsilon': 0.1,
        'description': 'All identical values - should merge into single piece'
    },

    # Test Case 10: Complex pattern requiring dynamic programming
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1.5], [2, 0.5], [3, 2], [4, 1], [5, 2.5], [6, 1.5],
                  [7, float('inf')]],
        'epsilon': 1.0,
        'description': 'Complex pattern - greedy may fail, requires optimal substructure analysis'
    }
]
test_cases25 = [
    # Test Case 1: Single piece - trivial case (should return 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 1.0,
        "description": "Single piece - already optimal",
        "expected_min_pieces": 1
    },

    # Test Case 2: Two pieces with values just within epsilon (mergeable)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [5, 5.5], [10, float('inf')]],
        "epsilon": 0.6,
        "description": "Two pieces within tolerance - should merge to 1",
        "expected_min_pieces": 1
    },

    # Test Case 3: Two pieces with values just outside epsilon (not mergeable)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [5, 5.5], [10, float('inf')]],
        "epsilon": 0.4,
        "description": "Two pieces outside tolerance - must stay 2",
        "expected_min_pieces": 2
    },

    # Test Case 4: Oscillating values - challenging for greedy algorithms
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, 1], [5, float('inf')]],
        "epsilon": 1.5,
        "description": "Oscillating pattern - tests greedy vs optimal merging",
        "expected_min_pieces": 2
    },

    # Test Case 5: Monotonically increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 1.5,
        "description": "Monotonic increase - tests range-based merging",
        "expected_min_pieces": 3
    },

    # Test Case 6: All values identical (should always merge to 1)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [2, 7], [5, 7], [8, 7], [10, float('inf')]],
        "epsilon": 0.1,
        "description": "All identical values - must merge to 1",
        "expected_min_pieces": 1
    },

    # Test Case 7: Large range with tight epsilon (no merging possible)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 10], [3, 15], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Large differences with tight tolerance - no merging",
        "expected_min_pieces": 4
    },

    # Test Case 8: Boundary case - epsilon exactly equals max difference
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 4], [3, float('inf')]],
        "epsilon": 2.0,
        "description": "Epsilon equals range - should merge all to 1",
        "expected_min_pieces": 1
    },

    # Test Case 9: Three pieces forming a valley (tests optimal grouping)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [2, 5], [4, 10], [6, float('inf')]],
        "epsilon": 3.0,
        "description": "Valley pattern - tests if algorithm finds optimal grouping",
        "expected_min_pieces": 2
    },

    # Test Case 10: Many pieces with gradual drift
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.3], [2, 5.6], [3, 5.9],
                  [4, 6.2], [5, 6.5], [6, 6.8], [7, 7.1], [8, float('inf')]],
        "epsilon": 1.0,
        "description": "Gradual drift - tests optimal segmentation points",
        "expected_min_pieces": 3
    }
]
test_cases26 = [
    # Test Case 1: Already optimal - single piece needed
    # All values within epsilon of each other
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.2], [2, 4.9], [3, 5.1], [4, float('inf')]],
        'epsilon': 0.3,
        'description': 'All pieces can be merged into one (values 5.0, 5.2, 4.9, 5.1 within ε=0.3)'
    },

    # Test Case 2: Two distinct groups
    # Values cluster into two groups that cannot be merged
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 5.0], [3, 5.1], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Two distinct groups: [1.0, 1.1] and [5.0, 5.1], need minimum 2 pieces'
    },

    # Test Case 3: Alternating values
    # Forces algorithm to handle non-contiguous merging decisions
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 10.0], [2, 1.5], [3, 10.5], [4, 2.0], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Alternating low/high values to test optimal grouping strategy'
    },

    # Test Case 4: Gradual increase at epsilon boundary
    # Each consecutive pair is exactly at epsilon distance
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, 3.0], [4, 4.0], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Values increase by exactly epsilon each step - tests boundary conditions'
    },

    # Test Case 5: Single outlier in middle
    # One value differs significantly from others
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.1], [2, 10.0], [3, 5.2], [4, 5.0], [5, float('inf')]],
        'epsilon': 0.3,
        'description': 'Single outlier (10.0) splits otherwise mergeable pieces'
    },

    # Test Case 6: Zero epsilon
    # No merging allowed unless values are identical
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 3.0], [1, 3.0], [2, 3.0], [3, 3.1], [4, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero epsilon: only identical values can merge'
    },

    # Test Case 7: Large epsilon
    # All pieces should merge into one
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, -100.0], [1, 50.0], [2, 200.0], [3, -50.0], [4, float('inf')]],
        'epsilon': 1000.0,
        'description': 'Very large epsilon should merge all pieces into one'
    },

    # Test Case 8: Monotonic increase with varying gaps
    # Tests if algorithm optimally handles different gap sizes
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 2.0], [3, 4.0], [4, 4.5], [5, 5.0],
                  [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Monotonic increase with gaps of 0.5, 0.5, 2.0, 0.5, 0.5 - should yield 2 pieces'
    },

    # Test Case 9: Three clusters at exact boundaries
    # Tests whether algorithm correctly identifies minimum pieces when clusters are at epsilon boundaries
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.9], [2, 2.0], [3, 2.9], [4, 4.0], [5, 4.9],
                  [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Three clusters: [0.0, 0.9], [2.0, 2.9], [4.0, 4.9] - each pair within epsilon but clusters separated'
    },

    # Test Case 10: V-shaped pattern
    # Values decrease then increase, testing non-monotonic behavior
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10.0], [1, 8.0], [2, 6.0], [3, 4.0], [4, 6.0], [5, 8.0], [6, 10.0],
                  [7, float('inf')]],
        'epsilon': 2.5,
        'description': 'V-shaped: tests optimal grouping with non-monotonic pattern'
    }
]
test_cases27 = [
    # Test Case 1: Already optimal - single constant function
    # All pieces have the same value, should merge into 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_min_pieces': 1,
        'description': 'Constant function - should merge all into 1 piece'
    },

    # Test Case 2: Values within epsilon - can be merged
    # Values differ by less than epsilon, testing if algorithm merges optimally
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10.3], [2, 9.8], [3, 10.1], [4, float('inf')]],
        'epsilon': 0.5,
        'expected_min_pieces': 1,
        'description': 'Values within epsilon tolerance - should merge into 1 piece'
    },

    # Test Case 3: Step function with large jumps
    # Values differ by more than epsilon, cannot merge
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 20], [3, 30], [4, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 4,
        'description': 'Large jumps - no merging possible'
    },

    # Test Case 4: Epsilon is zero
    # With zero tolerance, only identical consecutive values can merge
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5.001], [3, 5.001], [4, float('inf')]],
        'epsilon': 0.0,
        'expected_min_pieces': 2,
        'description': 'Zero epsilon - only exact matches merge'
    },

    # Test Case 5: Alternating values at boundary
    # Values alternate between two levels exactly epsilon apart
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 11], [2, 10], [3, 11], [4, 10], [5, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 1,
        'description': 'Alternating values at epsilon boundary - optimal merging unclear'
    },

    # Test Case 6: Single piece input
    # Minimal input with only one actual piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 42], [10, float('inf')]],
        'epsilon': 5.0,
        'expected_min_pieces': 1,
        'description': 'Single piece - trivial case'
    },

    # Test Case 7: Gradual ramp testing greedy vs optimal
    # Tests if greedy approach fails when optimal requires lookahead
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 0.9], [2, 1.8], [3, 2.7], [4, 3.6], [5, 4.5],
                  [6, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 2,
        'description': 'Gradual ramp - tests greedy vs optimal strategy'
    },

    # Test Case 8: Large epsilon relative to value range
    # Epsilon larger than the range of all values
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 12], [2, 8], [3, 11], [4, 9], [5, float('inf')]],
        'epsilon': 10.0,
        'expected_min_pieces': 1,
        'description': 'Large epsilon covers entire range - should merge all'
    },

    # Test Case 9: Two distinct groups with gap exactly at 2*epsilon
    # Tests boundary condition where groups are separable
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, 6], [3, 10], [4, 10.5], [5, 11],
                  [6, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 2,
        'description': 'Two groups separated by gap - tests separation threshold'
    },

    # Test Case 10: Negative values and mixed signs
    # Tests handling of negative values crossing zero
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, -10], [1, -9.5], [2, -0.5], [3, 0], [4, 0.5], [5, 9.5], [6, 10],
                  [7, float('inf')]],
        'epsilon': 1.0,
        'expected_min_pieces': 3,
        'description': 'Negative and positive values - tests sign handling'
    }
]
test_cases28 = [
    # Test Case 1: Already optimal - single piece sufficient
    # Input has 2 pieces [0,1) with value 5 and [1,2) with value 5.5
    # With ε=1, these can be merged into 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two similar values that should merge into one piece'
    },

    # Test Case 2: Cannot be reduced - values differ by more than 2ε
    # Values 0 and 5 differ by 5, cannot merge with ε=2
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, float('inf')]],
        'epsilon': 2.0,
        'description': 'Two pieces with large difference, cannot merge'
    },

    # Test Case 3: Multiple pieces, some mergeable
    # Values: 10, 10.5, 11, 15 - first three can merge with ε=1
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 10.5], [2, 11], [3, 15], [4, float('inf')]],
        'epsilon': 1.0,
        'description': 'Four pieces where first three should merge'
    },

    # Test Case 4: Alternating high-low values
    # Values: 0, 10, 0, 10 - no consecutive pieces can merge with ε=4
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        'epsilon': 4.0,
        'description': 'Alternating values preventing merges'
    },

    # Test Case 5: All identical values
    # All values are 7, should merge into single piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, float('inf')]],
        'epsilon': 0.0,
        'description': 'All identical values should become one piece'
    },

    # Test Case 6: Boundary case - exactly at 2ε threshold
    # Values differ by exactly 2ε, testing if algorithm handles equality correctly
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 7], [2, 9], [3, float('inf')]],
        'epsilon': 1.0,
        'description': 'Values at exactly 2ε apart (5,7,9 with ε=1)'
    },

    # Test Case 7: Long sequence with gradual increase
    # Values: 0, 0.5, 1, 1.5, 2, 2.5 - testing greedy vs optimal merge
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1], [3, 1.5], [4, 2], [5, 2.5],
                  [6, float('inf')]],
        'epsilon': 0.6,
        'description': 'Gradual increase testing greedy merge decisions'
    },

    # Test Case 8: Single piece input (minimal case)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [5, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single piece - already optimal'
    },

    # Test Case 9: Zero epsilon with varying values
    # With ε=0, no merging possible unless values are identical
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 1.0001], [2, 1], [3, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero tolerance - only identical values merge'
    },

    # Test Case 10: Large epsilon - everything should merge
    # All values within range [0, 100], ε=50 should allow all to merge
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 25], [2, 50], [3, 75], [4, 100], [5, float('inf')]],
        'epsilon': 50.0,
        'description': 'Large epsilon allowing all pieces to merge'
    }
]
test_cases29 = [
    # Test Case 1: Already optimal - single piece needed
    # Function is constant, should return 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        'epsilon': 0.1,
        'description': 'Constant function - should need only 1 piece'
    },

    # Test Case 2: Two pieces with values within epsilon
    # y1=2, y2=2.5 differ by 0.5 < epsilon=1.0, should merge to 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 2], [5, 2.5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Two pieces within tolerance - should merge to 1 piece'
    },

    # Test Case 3: Two pieces with values exactly at epsilon boundary
    # y1=0, y2=1.0, difference equals epsilon, tests boundary condition
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [5, 1.0], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Pieces differ by exactly epsilon - boundary test'
    },

    # Test Case 4: Three pieces where outer two can merge but not with middle
    # y1=0, y2=5, y3=0.5. With epsilon=1, pieces 1&3 close but separated by piece 2
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [2, 5], [4, 0.5], [6, float('inf')]],
        'epsilon': 1.0,
        'description': 'Non-adjacent pieces within tolerance - tests greedy vs optimal'
    },

    # Test Case 5: Oscillating values
    # Alternating high/low: 10, 0, 10, 0. Tests if algorithm handles oscillation
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, float('inf')]],
        'epsilon': 5.0,
        'description': 'Oscillating values - tests handling of alternating extremes'
    },

    # Test Case 6: Monotonic increase
    # Values: 1, 2, 3, 4, 5 with epsilon=1.5. Tests sequential merging
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'Monotonic increase - tests sequential merging strategy'
    },

    # Test Case 7: Single outlier in the middle
    # Values: 5, 5, 100, 5, 5. Middle piece is outlier
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 100], [6, 5], [8, 5], [10, float('inf')]],
        'epsilon': 1.0,
        'description': 'Single outlier piece - tests splitting around anomaly'
    },

    # Test Case 8: Very small epsilon (near zero tolerance)
    # All pieces have slightly different values, should need all pieces
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.01], [2, 1.02], [3, 1.03], [4, float('inf')]],
        'epsilon': 0.005,
        'description': 'Near-zero tolerance - should preserve all pieces'
    },

    # Test Case 9: Large epsilon (very loose tolerance)
    # Wide range of values but large epsilon should merge all
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [2, 50], [4, 100], [6, 25], [8, 75], [10, float('inf')]],
        'epsilon': 100.0,
        'description': 'Very large tolerance - should merge all to 1 piece'
    },

    # Test Case 10: Clustered groups
    # Two clusters: (0,1,0.5) and (10,11,10.5) with epsilon=1
    # Should result in 2 pieces, tests cluster detection
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0.5], [3, 10], [4, 11], [5, 10.5],
                  [6, float('inf')]],
        'epsilon': 1.5,
        'description': 'Two distinct clusters - should result in 2 pieces'
    }
]
test_cases30 = [
    # Test Case 1: Already optimal - single piece within tolerance
    # All values are within 2ε of each other, should return 1 piece
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.5], [2, 4.8], [3, 5.2], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'All values within tolerance - should merge to 1 piece'
    },

    # Test Case 2: Exactly at boundary - values differ by exactly 2ε
    # Tests whether algorithm correctly handles boundary condition
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, float('inf')]],
        'epsilon': 0.5,
        'description': 'Values at exact 2ε boundary - tests strict vs non-strict inequality'
    },

    # Test Case 3: Alternating high-low pattern
    # Cannot merge non-adjacent pieces, tests greedy vs optimal
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 10.0], [2, 1.5], [3, 10.5], [4, 2.0], [5, float('inf')]],
        'epsilon': 0.6,
        'description': 'Alternating values - adjacent pieces incompatible but non-adjacent compatible'
    },

    # Test Case 4: Decreasing then increasing (V-shape)
    # Tests if algorithm considers global optimization vs local greedy
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 10.0], [1, 8.0], [2, 6.0], [3, 8.0], [4, 10.0], [5, float('inf')]],
        'epsilon': 1.5,
        'description': 'V-shaped values - tests if middle piece blocks optimal merging'
    },

    # Test Case 5: Single outlier in middle
    # One incompatible piece prevents merging
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 5.0], [1, 5.0], [2, 10.0], [3, 5.0], [4, 5.0], [5, float('inf')]],
        'epsilon': 0.1,
        'description': 'Single outlier - forces at least 3 pieces'
    },

    # Test Case 6: Gradual drift
    # Small incremental changes that accumulate
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.6], [2, 1.2], [3, 1.8], [4, 2.4], [5, 3.0],
                  [6, float('inf')]],
        'epsilon': 0.4,
        'description': 'Gradual drift - each adjacent pair compatible but ends incompatible'
    },

    # Test Case 7: Zero epsilon (exact matching required)
    # Tests handling of strict optimality requirement
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 2.0], [3, 2.0], [4, 3.0], [5, float('inf')]],
        'epsilon': 0.0,
        'description': 'Zero tolerance - only exact matches can merge'
    },

    # Test Case 8: Large epsilon (everything mergeable)
    # Tests if algorithm finds the global minimum (1 piece)
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 5.0], [2, 3.0], [3, 7.0], [4, 2.0], [5, float('inf')]],
        'epsilon': 10.0,
        'description': 'Large tolerance - all pieces should merge to 1'
    },

    # Test Case 9: Three-cluster pattern
    # Tests dynamic programming vs greedy - need to find optimal breakpoints
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 5.0], [3, 5.5], [4, 10.0], [5, 10.5],
                  [6, float('inf')]],
        'epsilon': 0.5,
        'description': 'Three distinct clusters - optimal solution is 3 pieces'
    },

    # Test Case 10: Tight merging decision
    # Two pieces barely within tolerance, third forces split
    {
        'pc_fx': [[-float('inf'), float('inf')], [0, 0.0], [1, 0.99], [2, 5.0], [3, 5.99], [4, float('inf')]],
        'epsilon': 0.5,
        'description': 'Tight boundaries - tests numerical precision in comparisons'
    }
]
