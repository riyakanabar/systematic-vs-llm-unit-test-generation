#17Sept 5:48PM
#Iteration1
test_cases1 = [

    # 1. Small ε, should return all segments (no merging possible)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 6], [3, 10], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 2. Large ε, all segments should be merged into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 1], [3, 4], [4, float('inf')]],
        "epsilon": 3
    },

    # 3. Values oscillate just below ε, should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.4], [2, 4.7], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Oscillate just above ε, shouldn't be merged fully
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.6], [2, 4.3], [3, 5.8], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 5. ε matches exact midpoint deviation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, float('inf')]],
        "epsilon": 1
    },

    # 6. Long flat segments with small bumps – should be merged with sufficient ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 2.2], [3, 2.15], [4, float('inf')]],
        "epsilon": 0.25
    },

    # 7. Steep jump between one pair only – tests if one jump forces a split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 20], [3, 5], [4, 5], [5, float('inf')]],
        "epsilon": 4
    },

    # 8. Alternating highs/lows – cannot be merged with small ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4
    },

    # 9. Edge case: one segment only (nothing to merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 10. Boundary values very close to ±∞ – tests algorithm stability near extremes
    {
        "pc_fx": [[-float('inf'), float('inf')], [-1e10, 1], [0, 2], [1e10, float('inf')]],
        "epsilon": 1.5
    }
]

#Iteration2
test_cases2 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.2], [3, float('inf')]],
        "epsilon": 0.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 0], [3, 5], [4, float('inf')]],
        "epsilon": 2
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1e-8], [1, 2e-8], [2, 3e-8], [3, float('inf')]],
        "epsilon": 1e-8
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, float('inf')]],
        "epsilon": 4.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 3], [4, 3], [6, 3], [8, float('inf')]],
        "epsilon": 0.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.6], [2, 1.2], [3, float('inf')]],
        "epsilon": 0.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 9], [3, 2.2], [4, float('inf')]],
        "epsilon": 0.25
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, 1], [2, float('inf')]],
        "epsilon": 0.9
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1
    }
]

#Iteration3
test_cases3 = [
    # 1. Simple Mergeable Case: All values within epsilon, so should merge into 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.2], [2, 0.9], [3, 1.1], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 2. Slightly Over Threshold: One value just exceeds the epsilon, expect 2 segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.2], [2, 1.5], [3, 1.6], [4, float('inf')]],
        "epsilon": 0.25
    },

    # 3. Alternating values: Forces many small segments unless ε is large
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4.9
    },

    # 4. Flat segments with one spike: One outlier should create a separate segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 10], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 1
    },

    # 5. All values the same: Entire function should be merged into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0
    },

    # 6. Monotonic increasing: Test greedy vs optimal segmenting with fixed ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 7. Large ε should allow everything to merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, -10], [3, 5], [4, float('inf')]],
        "epsilon": 15
    },

    # 8. Sharp jump in middle: expect split exactly at discontinuity
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 100], [3, 100], [4, float('inf')]],
        "epsilon": 10
    },

    # 9. Short segments with small differences: test whether grouping is greedy or optimal
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1.5], [3, 2.2], [4, 1.7], [5, float('inf')]],
        "epsilon": 0.8
    },

    # 10. Original example: Moderate differences to test threshold tuning
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    },
]

#Iteration4
test_cases4 = [
    # 1. Flat function, should be merged into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 2], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Single large jump barely within epsilon, merge all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.9], [3, 2.1], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Single value violating epsilon, forces a split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, 1], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 4. Gradual increase within epsilon, merge all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.4], [2, 1.8], [3, 2.0], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 5. Large oscillation forces every segment to be isolated
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 3], [2, 0], [3, 3], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Minimum length segment just within epsilon, tests tight tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [0.1, 10.4], [0.2, 10.8], [0.3, 11.1], [1, float('inf')]],
        "epsilon": 1.2
    },

    # 7. All values exactly on epsilon boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 8. Monotonic decreasing with large drop requiring multiple splits
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 8], [2, 5], [3, 2], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Tiny noise added to constant function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.01], [2, 4.99], [3, 5.02], [4, float('inf')]],
        "epsilon": 0.05
    },

    # 10. Example given by user
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    }
]

#Iteration5
test_cases5 = [
    # Test Case 1: No merging possible (all jumps exceed epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 7], [3, 10], [4, float('inf')]],
        "epsilon": 1
    },
    # Test Case 2: All values within epsilon band, should merge to one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 1.8], [3, 2.3], [4, float('inf')]],
        "epsilon": 0.6
    },
    # Test Case 3: Alternating high-low values to test greedy decisions
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 0], [3, 5], [4, 0], [5, float('inf')]],
        "epsilon": 2
    },
    # Test Case 4: Flat segments followed by a spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 10], [4, float('inf')]],
        "epsilon": 1
    },
    # Test Case 5: Gradual slope within epsilon, tests multi-point merges
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.2], [2, 0.4], [3, 0.5], [4, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 6: Random values that require partitioning in between
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 4], [2, 6], [3, 4], [4, 3], [5, float('inf')]],
        "epsilon": 0.9
    },
    # Test Case 7: Precision boundary test (just inside epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.9], [2, 2.8], [3, 3.7], [4, float('inf')]],
        "epsilon": 0.9  # Can merge all
    },
    # Test Case 8: Precision boundary test (just outside epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.9], [2, 2.8], [3, 3.71], [4, float('inf')]],
        "epsilon": 0.9  # Must split last point
    },
    # Test Case 9: Edge case with only 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 10
    },
    # Test Case 10: Jump at the end
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, float('inf')]],
        "epsilon": 2
    }
]

#Iteration6
test_cases6 = [
    # 1. Example from your prompt
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    },

    # 2. Constant function - should always merge to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Alternating values just outside ε threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, float('inf')]],
        "epsilon": 0.9
    },

    # 4. Alternating values within ε, all can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 1.5], [3, 2], [4, float('inf')]],
        "epsilon": 0.6
    },

    # 5. Very tight ε forces no merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 6. Large ε allows complete merging despite large jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, -5], [3, 8], [4, float('inf')]],
        "epsilon": 10
    },

    # 7. Short domain with big jump in value
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 100], [0.2, float('inf')]],
        "epsilon": 50
    },

    # 8. Gradual slope — should merge only if ε large enough
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 2
    },

    # 9. Flat sections with small noise — should merge if ε ≥ noise
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 4.95], [3, 5.05], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 10. Piecewise constant, but last value far from rest — only one split expected
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 20], [4, float('inf')]],
        "epsilon": 0.5
    },
]
#Iteration7
test_cases7 = [
    # Test 1: Single segment, small epsilon — should remain unchanged
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2], [10, float('inf')]], "epsilon": 0.1},

    # Test 2: Small jumps within epsilon — should merge all into one
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 2.2], [3, 2.1], [4, float('inf')]], "epsilon": 0.25},

    # Test 3: Alternating values exceeding epsilon — no merging possible
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, float('inf')]], "epsilon": 0.5},

    # Test 4: Values in decreasing slope within epsilon range — should all merge
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4.9], [2, 4.8], [3, 4.85], [4, float('inf')]], "epsilon": 0.3},

    # Test 5: Tiny variation at beginning, large jump at end
    {"pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.2], [2, 10.1], [3, 18], [4, float('inf')]], "epsilon": 0.3},

    # Test 6: Jump in middle but tolerable overall if merged smartly
    {"pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 2.5], [4, 3.4], [6, 3.0], [8, float('inf')]], "epsilon": 0.5},

    # Test 7: Constant region followed by spike
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 5], [3, 0], [4, float('inf')]], "epsilon": 0.4},

    # Test 8: Edge case with only one real piece
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, float('inf')]], "epsilon": 1.0},

    # Test 9: Very large number of nearly equal values — test for efficiency and merging
    {"pc_fx": [[-float('inf'), float('inf')]] + [[i, 100 + (-1)**i * 0.1] for i in range(20)] + [[20, float('inf')]], "epsilon": 0.2},

    # Test 10: Example provided — mix of variations
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]], "epsilon": 0.75},
]

#Iteration8
test_cases8 = [
    # 1. Constant function — should return 1 segment for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Step function with jumps > ε — each jump must be separate
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 1], [3, 4], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 3. All values within ε range — should merge into 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.3], [3, 2.2], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Boundary case — difference exactly 2ε between two groups
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 3.2], [3, 3], [4, float('inf')]],
        "epsilon": 1.1  # First two and last two should form two segments
    },

    # 5. Floating-point precision issue (values very close to ε)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.999999], [2, 3.0], [3, float('inf')]],
        "epsilon": 1.0  # Should be careful not to split the first two
    },

    # 6. Long flat region with single outlier — must split only around the outlier
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 10], [3, 5], [4, 5], [5, float('inf')]],
        "epsilon": 2.0  # Should split outlier into its own segment
    },

    # 7. Minimal tolerance ε = 0 — every distinct value becomes its own segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 8. Overlapping ε windows — greedy merge may or may not be optimal
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 1.0  # Tricky: might form 1 segment, but optimal might need 2
    },

    # 9. Very short segments with large jumps — greedy might over-split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 10], [0.2, 1], [0.3, 10], [0.4, float('inf')]],
        "epsilon": 4.0
    },

    # 10. Alternating close-high-close pattern — tests backtracking / lookahead
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 2], [3, 3], [4, 2], [5, float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration9
test_cases9 = [

    # 1. Small jumps within epsilon – should collapse all into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.4], [2, 1.8], [3, 2.1], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 2. Large jump – should prevent merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 10], [2, float('inf')]],
        "epsilon": 3
    },

    # 3. Alternating values just at epsilon tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 1
    },

    # 4. Single interval – trivial case
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [5, float('inf')]],
        "epsilon": 0.1
    },

    # 5. Large flat region followed by steep jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 9], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 6. Values slowly drifting out of tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.3], [2, 0.6], [3, 0.9], [4, 1.2], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 7. Two large jumps far apart – 3 segments expected
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 10], [3, 10], [4, 20], [5, float('inf')]],
        "epsilon": 2
    },

    # 8. Extreme noise – nothing can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 5], [2, 0], [3, 5], [4, 0], [5, float('inf')]],
        "epsilon": 2
    },

    # 9. All values within epsilon of a constant – full merge possible
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 4], [1, 4.1], [2, 3.95], [3, 4.05], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 10. Worst-case merge point at the middle – greedy may fail
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 4], [2, 0], [3, 4], [4, float('inf')]],
        "epsilon": 2
    }
]

#Iteration10
test_cases10 = [
    # 1. Example case: Should result in 3 pieces if optimal
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,3],[3,7],[6,5],[7,float('inf')]],
        "epsilon": 0.75
    },

    # 2. Perfectly flat function: Should merge all into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[2,5],[4,5],[6,5],[10,float('inf')]],
        "epsilon": 0.0
    },

    # 3. All values vary but within epsilon: Should be one merged piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,3],[1,3.2],[2,2.8],[3,3.1],[4,float('inf')]],
        "epsilon": 0.3
    },

    # 4. Slight oscillation around a value, but exceeding epsilon: Should detect individual pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.4],[2,0.5],[3,1.3],[4,float('inf')]],
        "epsilon": 0.3
    },

    # 5. Alternating pattern exactly at epsilon threshold
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,3],[2,2],[3,3],[4,2],[5,float('inf')]],
        "epsilon": 1.0
    },

    # 6. Sudden large jump beyond epsilon in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[2,2.1],[4,9],[6,9.1],[8,float('inf')]],
        "epsilon": 0.5
    },

    # 7. Redundant pieces that can be merged within ε
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,10],[1,10.1],[2,10.2],[3,10.3],[4,float('inf')]],
        "epsilon": 0.5
    },

    # 8. Only one pair of pieces can be merged, others cannot
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.2],[2,3],[3,6],[4,float('inf')]],
        "epsilon": 0.3
    },

    # 9. Edge case: Very tight tolerance, nearly zero
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1.0],[1,1.0001],[2,1.0002],[3,1.0003],[4,float('inf')]],
        "epsilon": 1e-5
    },

    # 10. Piece values have sharp transitions just under and over ε
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5.49],[2,5.51],[3,5.0],[4,float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration11
test_cases11 = [

    # 1. Varying values close enough to be merged under ε
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 2],[1, 2.4],[2, 1.8],[3, 2.1],[4, float('inf')]],
        "epsilon": 0.5
    },

    # 2. Sharp jumps that cannot be merged
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 5],[2, 1],[3, 5],[4, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Constant function (should return a single segment)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 3],[1, 3],[2, 3],[3, 3],[4, float('inf')]],
        "epsilon": 0.0
    },

    # 4. Alternating values just outside ε
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 0],[1, 2.1],[2, 0],[3, 2.1],[4, float('inf')]],
        "epsilon": 1.0
    },

    # 5. Exactly ε apart — testing inclusivity of the bound
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1.0],[1, 2.0],[2, 3.0],[3, 4.0],[4, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Large flat region followed by small blip
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 10],[1, 10],[2, 10],[3, 13],[4, 10],[5, float('inf')]],
        "epsilon": 2.9
    },

    # 7. Values slowly increasing within ε bounds
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 0],[1, 0.5],[2, 1.0],[3, 1.5],[4, float('inf')]],
        "epsilon": 0.75
    },

    # 8. Two clusters separated by a big jump
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 10],[1, 10.2],[2, 10.1],[3, 30],[4, 30.2],[5, float('inf')]],
        "epsilon": 0.5
    },

    # 9. Single-point spikes in a flat signal
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 5],[2, 20],[3, 5],[4, 5],[5, float('inf')]],
        "epsilon": 10
    },

    # 10. Sparse data — large domain ranges with minimal changes
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[100, 1.5],[200, 1.2],[300, 1.4],[400, float('inf')]],
        "epsilon": 0.6
    }

]

#Iteration12
test_cases12 = [
    # 1. Simple mergeable values within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.1], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 2. Values jump just over epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.6], [2, 2.2], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Long plateau with one sharp outlier (should force split if epsilon is low)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 12], [3, 5], [4, float('inf')]],
        "epsilon": 2
    },

    # 4. Gradual ramp (tests tolerance handling across slowly increasing function)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        "epsilon": 1
    },

    # 5. Oscillation near threshold (forces optimal breakpoints)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.9
    },

    # 6. Redundant breakpoints (same value repeated, all should be merged)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 3], [4, float('inf')]],
        "epsilon": 0.01
    },

    # 7. Large constant jump in middle, rest flat
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 10], [3, 0], [4, 0], [5, float('inf')]],
        "epsilon": 1
    },

    # 8. Tiny epsilon forcing no merges at all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.01
    },

    # 9. All values within epsilon of each other (should merge into one segment)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [1, 4.2], [2, 4.1], [3, 4.3], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 10. Alternating values with exact distance = epsilon (tests open vs. closed interval logic)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        "epsilon": 1.0
    },
]

#Iteration13
test_cases13 = [
    # 1. Minimal test - already within epsilon, should return 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [10, 2.1], [20, 2.05], [30, float('inf')]],
        "epsilon": 0.2
    },
    # 2. Alternating values within epsilon – should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, 4.6], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.6
    },
    # 3. Sharp jump just beyond epsilon – should be a split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 2], [4, 4.1], [6, float('inf')]],
        "epsilon": 1.0
    },
    # 4. Flat regions interrupted by one spike – algorithm must split only at the spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 20], [3, 10], [4, 10], [5, float('inf')]],
        "epsilon": 4.9
    },
    # 5. All values distinct but linearly increasing – must segment frequently for small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        "epsilon": 0.5
    },
    # 6. Sudden large spike in middle – tests ability to isolate a narrow discontinuity
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 100], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 2
    },
    # 7. Two clusters of values far apart – should be split in two even if within-cluster variation is 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 50], [3, 50], [4, float('inf')]],
        "epsilon": 5
    },
    # 8. Plateau with one small deviation – if epsilon covers it, it must not split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [1, 7], [2, 7.4], [3, 7], [4, float('inf')]],
        "epsilon": 0.5
    },
    # 9. High-frequency noise within a narrow band – should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3.1], [1, 3.4], [2, 3.0], [3, 2.9], [4, 3.2], [5, float('inf')]],
        "epsilon": 0.6
    },
    # 10. Two pieces barely beyond tolerance – should split, tests near-boundary behavior
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.5], [2, 11.6], [3, float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration14
test_cases14 = [
    # 1. Simple flat function (should return 1 segment regardless of epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Alternating spikes (forces max splitting if epsilon is tight)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4.9
    },

    # 3. Gradual ramp (can group together if ε is large enough)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 4. Tight ε prevents any merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 5. Midpoint jumps (testing values around segment boundaries)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 7], [4, 2], [6, float('inf')]],
        "epsilon": 2
    },

    # 6. Segment with zero-length (redundant breakpoint)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1], [2, 10], [4, float('inf')]],
        "epsilon": 5
    },

    # 7. Long plateau followed by spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [11, 15], [12, float('inf')]],
        "epsilon": 4.5
    },

    # 8. Multiple constant regions with small jitters (noise handling)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.1], [1, 5.2], [2, 5.05], [3, 4.9], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 9. Worst-case merge temptation (values vary just around ε)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1.9], [2, 0.1], [3, float('inf')]],
        "epsilon": 1
    },

    # 10. Extreme boundaries with abrupt internal jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [-1000, 0], [0, 50], [1000, float('inf')]],
        "epsilon": 49.9
    }
]

#Iteration15
test_cases15 = [
    # 1. Flat function — should return a single piece for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [6, 5], [8, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Large jump — ε too small to merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, float('inf')]],
        "epsilon": 4.0  # Not enough to merge the jump of 9
    },

    # 3. Exactly mergeable — values within ε tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1.25], [3, float('inf')]],
        "epsilon": 0.5  # Should merge into one segment
    },

    # 4. Boundary condition — first and last points outside range
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 4], [2, 3.5], [3, float('inf')]],
        "epsilon": 0.6  # Can be merged into one
    },

    # 5. High variation but tolerable ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 10], [3, 5], [4, 0], [5, float('inf')]],
        "epsilon": 5.0  # All values within [0, 10], so not all can be merged
    },

    # 6. Staircase increase — forces optimal segmentation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.9  # Can group [0,1], [1,2], [2,3] -> 3 pieces
    },

    # 7. Zig-zag pattern — alternating high/low values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 0], [3, 5], [4, float('inf')]],
        "epsilon": 2.5  # Too tight to merge high-low pairs
    },

    # 8. Single spike — one outlier should force a split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 10], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 1.5  # The spike at x=2 forces a split
    },

    # 9. Near-mergeable pattern — just outside ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 3.1], [3, float('inf')]],
        "epsilon": 0.5  # Difference 1.1, just over ε
    },

    # 10. All values within ε-tube around a mean
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.1], [1, 4.8], [2, 5.2], [3, 5.0], [4, float('inf')]],
        "epsilon": 0.3  # All values within ±0.3 of 5
    }
]

#Iteration16
test_cases16 = [

    # Test Case 1: Simple merge possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    },

    # Test Case 2: All values are within epsilon of each other — should merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 1.9], [3, 2.05], [4, float('inf')]],
        "epsilon": 0.15
    },

    # Test Case 3: No merge possible — all values differ by more than epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 5], [3, 7], [4, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 4: Merge possible in the middle only
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.4], [2, 4], [3, 4.2], [4, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 5: Large flat region in between sharp changes
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 10], [3, 100], [4, float('inf')]],
        "epsilon": 1.0
    },

    # Test Case 6: Alternating up/down within epsilon (can be merged)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.9], [2, 1.1], [3, 1.8], [4, float('inf')]],
        "epsilon": 1.0
    },

    # Test Case 7: Tiny intervals with large jump — check if algorithm respects boundaries
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.01, 10], [0.02, 1], [0.03, 10], [0.04, float('inf')]],
        "epsilon": 8.0
    },

    # Test Case 8: Long constant followed by one outlier
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 20], [4, float('inf')]],
        "epsilon": 1.0
    },

    # Test Case 9: Repeating pattern that should be approximated in blocks
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 1], [3, 2], [4, 1], [5, 2],
                  [6, 10], [7, 10], [8, 10], [9, float('inf')]],
        "epsilon": 0.6
    },

    # Test Case 10: Borderline merge — exactly on epsilon limit
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 6], [2, 7], [3, 8], [4, float('inf')]],
        "epsilon": 1.5
    }
]

#Iteration17
test_cases17 = [
    # 1. Monotonic increasing with small jumps within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, float('inf')]],
        "epsilon": 0.6
    },

    # 2. Sudden large jump — should force a cut
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 5], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Alternating values around a center line — hard for greedy
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 4. Constant values — should be collapsed into 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 5. All values differ but within epsilon — still collapsible to one segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.2], [2, 2.3], [3, 2.4], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 6. Breakpoint right at the boundary of epsilon (tight threshold)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.75], [2, 2.5], [3, float('inf')]],
        "epsilon": 0.75
    },

    # 7. Large uniform jump at midpoint only
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 10], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 8. Flat followed by oscillating pattern — test hybrid behavior
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 6], [4, 4], [5, 6], [6, 4],
                  [7, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Values spaced with exact epsilon difference — greedy may be misled
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1.0], [3, 1.5], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 10. Random large values with tiny epsilon — should return all individual segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 10], [2, 3], [3, 15], [4, 5], [5, float('inf')]],
        "epsilon": 0.1
    }
]

#Iteration18
test_cases18 = [
    # 1. Basic test — should merge the first two segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    },

    # 2. Constant function — entire domain can be merged into one segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [6, 5], [8, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Alternating high/low values — no merges should occur
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4.9
    },

    # 4. Gradually increasing values within epsilon range — all segments merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, 2.4], [4, float('inf')]],
        "epsilon": 0.6
    },

    # 5. Very tight epsilon, no merges allowed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.6], [2, 1.2], [3, 1.8], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 6. Two mergeable clusters with a gap in between
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 10], [3, 10.4], [4, float('inf')]],
        "epsilon": 0.6
    },

    # 7. Outlier in the middle — forces a split despite surrounding constancy
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 100], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 5
    },

    # 8. Near-merge at the boundary of epsilon — edge case for merge threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Repeating pattern within epsilon — test consistent grouping
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 6], [2, 5], [3, 6], [4, float('inf')]],
        "epsilon": 0.6
    },

    # 10. Function with plateaus and steps — mix of mergeable and non-mergeable segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 0], [3, 10], [4, 10], [5, 20], [6, float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration19
test_cases19 = [

    # 1. Minimal constant function (should be merged to 1 segment regardless of epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Alternating high/low values just at epsilon threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 1
    },

    # 3. Large flat area with a spike (should split around spike)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 10], [6, 2], [10, float('inf')]],
        "epsilon": 2
    },

    # 4. All values increasing slowly (can be merged under large ε)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1.8], [3, 2], [4, float('inf')]],
        "epsilon": 1
    },

    # 5. Each segment just exceeds ε — should force new piece at each point
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1.6], [2, 3.2], [3, 4.8], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 6. Values alternate just within ε to encourage merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, 4.5], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.75
    },

    # 7. Plateau followed by sharp jump and back — should detect jump as isolated piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 3], [3, 10], [4, 3], [6, float('inf')]],
        "epsilon": 1.5
    },

    # 8. Decreasing values in staircase (should break every time if ε small)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 8], [2, 6], [3, 4], [4, 2], [5, float('inf')]],
        "epsilon": 1.9
    },

    # 9. Tiny jitter (noise within tolerance) — should all merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.05], [2, 2.1], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 10. Edge case with only 1 actual piece (baseline case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [10, float('inf')]],
        "epsilon": 0.0001
    }
]

#Iteration20
test_cases20 = [

    # 1. Constant function — should be approximated with 1 segment regardless of epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, 5], [30, float('inf')]],
        "epsilon": 0.001
    },

    # 2. Two regions differing just above ε — should NOT merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1.9], [10, float('inf')]],
        "epsilon": 0.8
    },

    # 3. Two regions differing just below ε — should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1.7], [10, float('inf')]],
        "epsilon": 0.75
    },

    # 4. Slowly increasing values within ε — should merge all
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.2], [2, 1.4], [3, 1.6], [4, 1.8], [5, float('inf')]],
        "epsilon": 0.9
    },

    # 5. Alternating values at boundary of ε — no merges possible
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.9], [2, 1], [3, 1.9], [4, 1], [5, float('inf')]],
        "epsilon": 0.89
    },

    # 6. Long plateau with one spike — test skipping spike or not
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 2], [2, 10], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 7. Large jumps in data — only exact segmenting would be optimal
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 4
    },

    # 8. Tiny tolerance — no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.001], [2, 1.002], [3, 1.003], [4, float('inf')]],
        "epsilon": 0.0005
    },

    # 9. Repeated values — should collapse to fewer segments
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 2], [2, 2], [3, 3], [4, 3], [5, 2], [6, float('inf')]],
        "epsilon": 0.1
    },

    # 10. Random pattern where only a subset can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.3], [2, 1.2], [3, 3.5], [4, 3.4], [5, 3.6], [6, 8], [7, float('inf')]],
        "epsilon": 0.4
    }
]

#Iteration21
test_cases21 = [

    # 1. Flat constant function: optimal is 1 segment regardless of epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Strictly increasing, needs all breakpoints unless large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Sharp peak that exceeds epsilon → must split around it
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, float('inf')]],
        "epsilon": 4.0
    },

    # 4. Alternating high/low values to test how well epsilon merges them
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 8], [2, 2], [3, 8], [4, float('inf')]],
        "epsilon": 2.5
    },

    # 5. Constant values with noise just under ε, should be approximated with 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.4], [2, 4.7], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 6. Edge case where change is exactly ε, test inclusion/exclusion edge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3.75], [2, 4.5], [3, float('inf')]],
        "epsilon": 0.75
    },

    # 7. Decreasing trend with one anomaly requiring its own segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 9], [2, 3], [3, 8], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 8. All values within ε of each other → 1 segment expected
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3.1], [2, 3.05], [3, 2.9], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 9. Sparse long segment followed by frequent changes
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [10, 2], [11, 5], [12, 7], [13, 1], [14, float('inf')]],
        "epsilon": 1.0
    },

    # 10. Realistic case with plateaus and jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 5], [3, 5], [4, 8], [5, 8], [6, float('inf')]],
        "epsilon": 0.75
    }

]

#Iteration22
test_cases22 = [

    # 1. No simplification possible due to large jumps in y-values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 2. All y-values within ε range — should reduce to one segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.1], [1, 2.2], [2, 1.9], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 3. Oscillation around two levels — should alternate and segment at each change
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, float('inf')]],
        "epsilon": 0.9
    },

    # 4. Gradual increase — test tolerance envelope (ε just enough to compress)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.3], [2, 1.6], [3, 1.9], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 5. Plateaus with sudden jumps — should preserve boundaries at jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.49
    },

    # 6. All constant — trivial reduction to one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [2, 7], [4, 7], [6, 7], [8, float('inf')]],
        "epsilon": 0.0
    },

    # 7. Alternating values just within ε — test greedy segment merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3.4], [2, 2.6], [3, 3.4], [4, 2.6], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Values just outside ε bound — should segment at each jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.6], [2, 2.2], [3, 2.8], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 9. Multiple small ranges — test optimal piece grouping
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.2], [2, 2.1], [3, 6], [4, 6.1], [5, 10], [6, 10.2], [7, float('inf')]],
        "epsilon": 0.25
    },

    # 10. Random values with exact ε tight bounds — edge of approximation tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, 2.5], [4, 3], [5, float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration23
test_cases23 = [

    # 1. Simple mergeable case: all values within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.4], [2, 2.2], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 2. Needs 1 split in the middle due to a big jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 4.5], [3, 4.7], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Large ε: allows all to merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 5], [3, float('inf')]],
        "epsilon": 5
    },

    # 4. Small ε: no values within tolerance, should return max number of segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 6], [3, float('inf')]],
        "epsilon": 0.1
    },

    # 5. Identical values: should merge into one segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [2, 4], [3, 4], [4, float('inf')]],
        "epsilon": 0
    },

    # 6. High-frequency noise within ε: should all merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.5, 1.1], [1, 0.95], [1.5, 1.05], [2, float('inf')]],
        "epsilon": 0.15
    },

    # 7. Alternating high/low outside ε: every other value forces split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4
    },

    # 8. Tolerance barely sufficient to merge boundary segments but not middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2.5], [2, 6], [3, 2.4], [4, 1], [5, float('inf')]],
        "epsilon": 1.5
    },

    # 9. Multiple small clusters separated by large jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.2], [2, 5], [3, 5.1], [4, 8.5], [5, 8.7], [6, float('inf')]],
        "epsilon": 0.3
    },

    # 10. Long flat segment interrupted by one outlier
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 25], [3, 10], [4, 10], [5, float('inf')]],
        "epsilon": 5
    }

]

#Iteration24
test_cases24 = [

    # 1. Simple mergeable segments (all values within ε = 1)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.9], [3, 2.4], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 2. Sharp jump not mergeable (forces split)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 3. All segments equal: trivial case (should merge into one)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [6, 5], [8, float('inf')]],
        "epsilon": 0.0
    },

    # 4. Edge case with ε = 0 (must preserve all changes)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 5. Floating point tolerance just enough to merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.49], [2, 1.51], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 6. Boundary condition: min and max y-values exactly ε apart
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 6], [4, 5.5], [6, 6], [8, float('inf')]],
        "epsilon": 1.0
    },

    # 7. Many small changes within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, 1.4], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Alternating pattern: merge only every two segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        "epsilon": 0.75
    },

    # 9. Large number of segments all equal – scalability check
    {
        "pc_fx": [[-float('inf'), float('inf')]] + [[i, 3] for i in range(0, 100)] + [[100, float('inf')]],
        "epsilon": 0.1
    },

    # 10. One extreme outlier should not affect merging of others
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 100], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration25
test_cases25 = [

    # 1. Simple merge possible: small difference between values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 3], [3, float('inf')]],
        "epsilon": 0.6
    },

    # 2. No merging possible due to large jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 9], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Constant function — can always be merged into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [6, float('inf')]],
        "epsilon": 0.0
    },

    # 4. Fluctuating around a base with small variance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3.1], [1, 3.0], [2, 2.9], [3, float('inf')]],
        "epsilon": 0.15
    },

    # 5. One exact ε-difference at a breakpoint
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.75], [2, 2.5], [3, float('inf')]],
        "epsilon": 0.75
    },

    # 6. Plateau followed by sharp spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 10], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 7. Zig-zag pattern to test greedy vs optimal
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 8. Short segment outlier among smooth ones
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [1.1, 10], [2, 2], [3, float('inf')]],
        "epsilon": 2.0
    },

    # 9. Minimum ε needed to merge all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 10. One mergeable cluster, one not
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.2], [2, 8], [3, 8.1], [4, float('inf')]],
        "epsilon": 0.25
    }

]

#Iteration26
test_cases26 = [

    # 1. Constant function (should return 1 segment for any ε ≥ 0)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, 5], [30, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Small jumps, but under epsilon (can be merged into 1 segment)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [5, 1.2], [10, 1.1], [15, float('inf')]],
        "epsilon": 0.3
    },

    # 3. One large jump that forces a split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1.1], [10, 5], [15, float('inf')]],
        "epsilon": 0.4
    },

    # 4. Repeating pattern of jumps and flat (should alternate merge/split)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 5], [4, 1], [6, 5], [8, float('inf')]],
        "epsilon": 1.5
    },

    # 5. No tolerance allowed (must preserve original)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 3], [4, 4], [6, 5], [8, float('inf')]],
        "epsilon": 0.0
    },

    # 6. Gradual increasing trend, all within epsilon range
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 0.5], [4, 1.0], [6, 1.4], [8, float('inf')]],
        "epsilon": 0.5
    },

    # 7. Alternating ±ε around a constant (tests max deviation bound)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 2.5], [4, 3.5], [6, 2.6], [8, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Sudden peak in middle (should be isolated)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [3, 1], [5, 10], [7, 1], [9, 1], [10, float('inf')]],
        "epsilon": 2.0
    },

    # 9. Multiple small segments that can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 4.0], [1, 4.2], [2, 4.1], [3, 4.3], [4, 4.25], [5, float('inf')]],
        "epsilon": 0.3
    },

    # 10. Two flat zones with jump just exceeding ε (forces split)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2], [10, 3], [15, 3], [20, float('inf')]],
        "epsilon": 0.9
    }
]

#Iteration27
test_cases27 = [

    # 1. Constant function (should merge everything)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Small jumps in increasing function, within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.4], [2, 1.9], [3, 2.3], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Sharp jump in the middle, must split at jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 2.2], [3, 10], [4, 10.1], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Alternating high/low values, difficult to merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 0], [3, 5], [4, 0], [5, float('inf')]],
        "epsilon": 2.4
    },

    # 5. Small random noise within ε, should be fully merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3.0], [1, 3.2], [2, 3.1], [3, 2.9], [4, 3.05], [5, float('inf')]],
        "epsilon": 0.25
    },

    # 6. Large outlier in the center, must split at it
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 100], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 7. Flat region followed by increasing trend
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5.5], [4, 6], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Minimal input case (only one interval)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, float('inf')]],
        "epsilon": 0.1
    },

    # 9. All values increasing, but mergeable under high ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 2.5
    },

    # 10. Staircase pattern just exceeding ε → must split at every step
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        "epsilon": 0.9
    }

]

#Iteration28
test_cases28 = [
    # 1. Mixed mergeable segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [3, 7], [6, 5], [7, float('inf')]],
        "epsilon": 0.75
    },
    # 2. All values the same — should return 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [6, 5], [8, float('inf')]],
        "epsilon": 0
    },
    # 3. Alternating extremes — no merges possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, float('inf')]],
        "epsilon": 4.5
    },
    # 4. Gradually increasing — many merges possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 1.5
    },
    # 5. One big spike blocks full merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 3], [4, 15], [6, 3], [8, 3], [10, float('inf')]],
        "epsilon": 5
    },
    # 6. Close values within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.4], [2, 1.8], [3, 2.2], [4, float('inf')]],
        "epsilon": 0.9
    },
    # 7. Zero-length interval (duplicate x values)
    {
        "pc_fx": [[-float('inf'), float('inf')], [1, 5], [1, 5], [2, 6], [3, 5], [4, float('inf')]],
        "epsilon": 1.0
    },
    # 8. Plateau with a sudden jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 15], [4, float('inf')]],
        "epsilon": 4.9
    },
    # 9. Sparse inputs over long x-range
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [100, 2], [200, 1], [300, 2], [400, float('inf')]],
        "epsilon": 1
    },
    # 10. Sharp spike in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 30], [3, 10], [4, 10], [5, float('inf')]],
        "epsilon": 19.9
    }
]

#Iteration29
test_cases29 = [
    # Test Case 1: Single jump, within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2.5], [4, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 2: Requires two pieces to satisfy epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 4], [4, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 3: Constant function (should return 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [3, 5], [6, 5], [8, float('inf')]],
        "epsilon": 0.01
    },
    # Test Case 4: Alternating high-low spikes
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 9], [2, 1], [3, 9], [4, 1], [5, float('inf')]],
        "epsilon": 3.5
    },
    # Test Case 5: Monotonic increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 1.5
    },
    # Test Case 6: High variance but all within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 100], [1, 101], [2, 99], [3, 100.5], [4, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 7: Requires splitting mid-flat region
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2], [3, 10], [4, 10], [5, float('inf')]],
        "epsilon": 3.5
    },
    # Test Case 8: Extreme outlier in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 100], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 5.0
    },
    # Test Case 9: Step-like increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 4], [3, 8], [4, 16], [5, float('inf')]],
        "epsilon": 6.0
    },
    # Test Case 10: Minimal difference between points
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 5.01], [2, 5.02], [3, 5.03], [4, float('inf')]],
        "epsilon": 0.05
    }
]

#Iteration30
test_cases30 = [

    # Test Case 1: Simple mergeable segments within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.5], [2, 2.25], [3, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 2: Sudden jump just outside tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.6], [2, 3], [3, float('inf')]],
        "epsilon": 0.6
    },

    # Test Case 3: Oscillating values just within tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.4], [2, 0.6], [3, 1.3], [4, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 4: All values same, ε = 0 (test degenerate case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 0
    },

    # Test Case 5: Tiny ε, every segment must be preserved
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.1
    },

    # Test Case 6: Large ε, should merge all into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 5], [3, 4], [4, float('inf')]],
        "epsilon": 5
    },

    # Test Case 7: Small jump near the boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.7], [2, 2.5], [3, float('inf')]],
        "epsilon": 0.75
    },

    # Test Case 8: Noise-like pattern, alternating up/down within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.3], [2, 4.7], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 9: Values differ only at one point
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 6], [3, 3], [4, float('inf')]],
        "epsilon": 2.9
    },

    # Test Case 10: Repeated small violations—should prevent merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.6], [2, 2.2], [3, 2.9], [4, float('inf')]],
        "epsilon": 0.5
    }

]

