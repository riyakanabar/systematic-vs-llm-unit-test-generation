#17Sept 5:14PM
#takes 25minutes to generate all these testcases using llm > copy paste the prompt > output > paste
#Iteration1
test_cases1 = [
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.2], [2, 5.1], [3, 5.3],
                  [4, float('inf')]],
        "epsilon": 0.3
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.2], [2, 1.6], [3, 2],
                  [4, float('inf')]],
        "epsilon": 0.3
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 0.5], [2, 1.0],
                  [3, float('inf')]],
        "epsilon": 0.5
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 2], [2, 10], [3, 10],
                  [4, float('inf')]],
        "epsilon": 1.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 4], [2, 6], [3, 5],
                  [4, float('inf')]],
        "epsilon": 1.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2],
                  [1, float('inf')]],
        "epsilon": 0.1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 10], [2, 10.1], [3, 10], [4, 10],
                  [5, float('inf')]],
        "epsilon": 0.05
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 1], [2, 2], [3, 3],
                  [4, float('inf')]],
        "epsilon": 1.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 7], [1, 7], [2, 7], [3, 7],
                  [4, float('inf')]],
        "epsilon": 0.0
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0001], [2, 1.0002], [3, 1.0003],
                  [4, float('inf')]],
        "epsilon": 0.00005
    }
]
#Iteration2
test_cases2 = [
    # 1. Simple constant function — should return 1 piece regardless of ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Two-piece exact jump — ε just below the jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 4], [10, float('inf')]],
        "epsilon": 2.5
    },

    # 3. Two-piece, ε exactly equal to the midpoint of jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [3, 6], [6, float('inf')]],
        "epsilon": 2.0
    },

    # 4. Three values with small variation, should be grouped
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5.1], [4, 4.9], [6, float('inf')]],
        "epsilon": 0.15
    },

    # 5. Sharp jump within ε — should not split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Multiple flat regions interrupted by small noise
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 2.1], [2, 1.9], [3, 2],
                  [4, 5], [5, 5.2], [6, 4.9],
                  [7, float('inf')]],
        "epsilon": 0.3
    },

    # 7. Alternating high/low values that exceed ε — should return many segments
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 9], [2, 1], [3, 9], [4, 1], [5, float('inf')]],
        "epsilon": 3.0
    },

    # 8. High plateau then drop — checks that single large piece isn't merged
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [5, 10], [10, 2], [15, 2], [20, float('inf')]],
        "epsilon": 3.0
    },

    # 9. Tiny ε with slight noise — should return as many segments as data points
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.01], [2, 1.02], [3, 1.03], [4, float('inf')]],
        "epsilon": 0.005
    },

    # 10. Segment with linear ramp — shows non-constant trend, must split often
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        "epsilon": 0.6
    },
]

#Iteration3
test_cases3 = [
    # 1. Simple exact fit
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Slight noise within epsilon — should merge all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.1], [2, 2.05], [3, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Sharp jump beyond epsilon — should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 3], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Alternating pattern — needs careful grouping
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        "epsilon": 0.49
    },

    # 5. All same values — trivial merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 6. One spike exceeding epsilon — should break at spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, float('inf')]],
        "epsilon": 2.0
    },

    # 7. Boundary test — edge values near tolerance limit
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 8. Minimal breakpoints with large epsilon — all should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [100, 7], [200, 6], [300, float('inf')]],
        "epsilon": 2.0
    },

    # 9. Two equal-sized plateaus separated by a jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 10. Flat trend with slowly drifting values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        "epsilon": 0.15
    }
]

#Iteration4
test_cases4 = [
    # 1. Single segment, flat function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Two values just within epsilon → should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2.05], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Two values just beyond epsilon → should split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2.11], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 4. Alternating pattern barely within ε
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.05], [2, 0.95], [3, 1.02], [4, 0.98], [5, float('inf')]],
        "epsilon": 0.05
    },

    # 5. Alternating pattern just outside ε
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.06], [2, 0.94], [3, 1.07], [4, 0.93], [5, float('inf')]],
        "epsilon": 0.05
    },

    # 6. Large jump in middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 100], [3, 100], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 7. All values different but within ε
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.01], [2, 1.02], [3, 1.03], [4, 1.04], [5, float('inf')]],
        "epsilon": 0.05
    },

    # 8. Step-wise function with equal alternating values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 4.0
    },

    # 9. Noise with outlier far away
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.1], [2, 1.2], [3, 100], [4, 1.1], [5, float('inf')]],
        "epsilon": 0.2
    },

    # 10. Boundary test with constant segment at start and end
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 10], [2, 50], [3, 50], [4, 10], [5, 10], [6, float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration5
test_cases5 = [
    # 1. Constant function (should always return 1 piece)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, 5], [30, float('inf')]], "epsilon": 0.1},

    # 2. Slight oscillation within epsilon (should be merged into 1 piece)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [10, 5.05], [20, 4.95], [30, float('inf')]], "epsilon": 0.1},

    # 3. Change just over epsilon (should result in 2 segments)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 6.2], [20, float('inf')]], "epsilon": 1.0},

    # 4. Alternating values within tolerance (should be merged into 1)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.5], [2, 9.8], [3, 10.3], [4, float('inf')]], "epsilon": 1.0},

    # 5. Jump exceeds epsilon (forces segmentation)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 1], [3, 4], [4, float('inf')]], "epsilon": 1.2},

    # 6. Increasing staircase with tight epsilon (likely each point forms own segment)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]], "epsilon": 0.5},

    # 7. Sharp change followed by constant (test segment detection)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 10], [3, 10], [4, float('inf')]], "epsilon": 1.0},

    # 8. Noisy pattern (test whether algorithm avoids oversegmentation)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.3], [2, 1.8], [3, 2.2], [4, 2.1], [5, float('inf')]], "epsilon": 0.5},

    # 9. All values exceed epsilon with high variation (forces maximum segmentation)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 2], [3, 9], [4, 3], [5, float('inf')]], "epsilon": 1.0},

    # 10. Borderline merge/split case (designed for ambiguity)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 6], [2, 7], [3, 5.5], [4, float('inf')]], "epsilon": 1.5}
]

#Iteration6
test_cases6 = [

    # Test 1: Single segment sufficient
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]], "epsilon": 0.0},

    # Test 2: Small jump just under epsilon — should be merged
    {"pc_fx": [[-float('inf'), float('inf')], [0, 3], [10, 3.4], [20, float('inf')]], "epsilon": 0.5},

    # Test 3: Jump exactly at epsilon — may or may not merge depending on tie-breaks
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2.5], [10, float('inf')]], "epsilon": 0.5},

    # Test 4: Jump just over epsilon — should not merge
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 2], [10, float('inf')]], "epsilon": 0.9},

    # Test 5: Varying lengths — shorter interval with larger jump
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1.5, 5], [10, float('inf')]], "epsilon": 2.0},

    # Test 6: Flat middle with sharp boundary change — merging not allowed
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 10], [4, 0], [6, float('inf')]], "epsilon": 4.5},

    # Test 7: Many small variations within ε — should all merge into one
    {"pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3.3], [2, 2.9], [3, 3.1], [4, float('inf')]], "epsilon": 0.5},

    # Test 8: Sudden spike — should isolate the spike
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 10], [4, 1], [6, float('inf')]], "epsilon": 4.0},

    # Test 9: Repeating pattern at boundary of ε
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]], "epsilon": 1.0},

    # Test 10: Plateaus with alternating high/low — only one merge possible
    {"pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 10], [3, 0], [4, float('inf')]], "epsilon": 9.9}
]

#Iteration7
test_cases7 = [
    # 1. Exact match possible with one segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [10, 2], [20, float('inf')]],
        "epsilon": 0.5
    },

    # 2. Sharp transition just outside ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1.6], [10, 3.5], [15, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Flat values with single outlier (should be a new piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 12], [6, 5], [8, 5], [10, float('inf')]],
        "epsilon": 3.0
    },

    # 4. Deceptively mergeable if not careful (subtle drift)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1.9], [4, 2.1], [6, 3], [8, float('inf')]],
        "epsilon": 1.0
    },

    # 5. Alternating high/low values (forces multiple segments)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 1], [3, 4], [4, 1], [5, float('inf')]],
        "epsilon": 1.2
    },

    # 6. Constant followed by rapid rise
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 0], [6, 8], [7, float('inf')]],
        "epsilon": 2.5
    },

    # 7. Values within ε range (entire segment can be merged)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.4], [2, 2.2], [3, 1.6], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Long uniform followed by spike and then back (check for correct segmentation)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [5, 10], [6, 50], [7, 10], [10, float('inf')]],
        "epsilon": 5.0
    },

    # 9. ε = 0.0 (forces exact match; all segments should be kept)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 0.0
    },

    # 10. One point just slightly out of range
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [1, 7.4], [2, 7.6], [3, 9.1], [4, 7.2], [5, float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration8
test_cases8 = [

    # 1. Single plateau, all values within epsilon → should merge into 1 piece
    {"pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2.1],[2,1.9],[3,float('inf')]],
     "epsilon": 0.2},

    # 2. Abrupt jump beyond epsilon → should force new piece
    {"pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.1],[2,4],[3,float('inf')]],
     "epsilon": 0.5},

    # 3. Repeating values separated by noise below epsilon → should merge into 1
    {"pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5.4],[2,4.6],[3,5.2],[4,float('inf')]],
     "epsilon": 0.5},

    # 4. Zig-zag just above epsilon → should split at each point
    {"pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,1],[3,3],[4,float('inf')]],
     "epsilon": 0.9},

    # 5. Constant function → should produce 1 piece
    {"pc_fx": [[-float('inf'), float('inf')],[0,7],[1,7],[2,7],[3,float('inf')]],
     "epsilon": 0.01},

    # 6. Linear increase within epsilon tolerance → should merge all
    {"pc_fx": [[-float('inf'), float('inf')],[0,2.0],[1,2.1],[2,2.2],[3,2.25],[4,float('inf')]],
     "epsilon": 0.3},

    # 7. Tiny jump just above epsilon → algorithm must detect split
    {"pc_fx": [[-float('inf'), float('inf')],[0,2.0],[1,2.6],[2,float('inf')]],
     "epsilon": 0.5},

    # 8. Alternating small jumps below epsilon → expect full merge
    {"pc_fx": [[-float('inf'), float('inf')],[0,10.0],[1,10.3],[2,10.1],[3,10.4],[4,float('inf')]],
     "epsilon": 0.5},

    # 9. Large segment followed by a small outlier spike → should split at outlier
    {"pc_fx": [[-float('inf'), float('inf')],[0,8],[1,8.1],[2,20],[3,8.1],[4,float('inf')]],
     "epsilon": 0.5},

    # 10. Nearly all values same, but one sharp drop in middle
    {"pc_fx": [[-float('inf'), float('inf')],[0,7],[1,7.1],[2,1],[3,7.2],[4,float('inf')]],
     "epsilon": 0.5},

]

#Iteration9
test_cases9 = [

    # 1. Flat function - should be approximated with 1 segment for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Sharp jump just at ε boundary – tests if algorithm merges within tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Jump just outside ε – cannot be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2.1], [2, 3.2], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 4. Alternating values within ε band – can be merged into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 1.8], [2, 2.1], [3, 2.05], [4, float('inf')]],
        "epsilon": 0.15
    },

    # 5. Single large outlier – algorithm must separate it
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 10], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Long plateau with gradual drift – tests segment merging sensitivity
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.5], [2, 2.0], [3, 2.5], [4, 3.0], [5, float('inf')]],
        "epsilon": 0.6
    },

    # 7. Very small ε – forces separate segments for each tiny variation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.01], [2, 1.02], [3, float('inf')]],
        "epsilon": 0.001
    },

    # 8. Two large constant blocks with ε gap – should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [5, 5], [6, 10], [7, 10], [8, float('inf')]],
        "epsilon": 4.9
    },

    # 9. Repeating sawtooth pattern – can only merge every few
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1], [3, 3], [4, 1], [5, float('inf')]],
        "epsilon": 1.9
    },

    # 10. Degenerate case – empty domain (no actual segments)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration10
test_cases10 = [

    # 1. Single plateau: all y-values are the same → should return 1 segment for any ε
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,5],[4,float('inf')]],
        "epsilon": 0.1
    },

    # 2. Oscillating values just within ε → should merge into 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2.9],[1,3.1],[2,2.95],[3,3.05],[4,float('inf')]],
        "epsilon": 0.15
    },

    # 3. Oscillating values exceeding ε → must split
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2.9],[1,3.2],[2,2.8],[3,3.3],[4,float('inf')]],
        "epsilon": 0.15
    },

    # 4. Two wide plateaus separated by a spike → should detect 3 segments
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,10],[3,5],[4,5],[5,float('inf')]],
        "epsilon": 1.0
    },

    # 5. ε equals the max deviation possible → should result in 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,2],[3,3],[4,float('inf')]],
        "epsilon": 1.0  # max |yi - mean| = 1, so ε = 1 should allow merging
    },

    # 6. Long flat section followed by gradual increase just above ε → must break
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1],[2,1.1],[3,1.2],[4,2],[5,float('inf')]],
        "epsilon": 0.4
    },

    # 7. Break exactly at ε threshold → to test boundary behavior
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.5],[2,2],[3,2.5],[4,float('inf')]],
        "epsilon": 0.5
    },

    # 8. Tiny segments with large ε → all should merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,10],[0.1,10.2],[0.2,10.1],[0.3,10.3],[0.4,float('inf')]],
        "epsilon": 0.5
    },

    # 9. Strictly increasing steps greater than ε → each segment must be separated
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,5],[3,7],[4,float('inf')]],
        "epsilon": 0.9
    },

    # 10. Values differ by just under ε at breakpoints but overall spread is larger → should merge wisely
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.9],[2,2.8],[3,3.7],[4,float('inf')]],
        "epsilon": 1.0  # e.g., max deviation from mean of [1,1.9,2.8] = 0.9
    },
]

#Iteration11
test_cases11 = [
    # 1. Single flat segment, should return 1 segment if ε >= 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Alternating spikes, tests ability to merge only where feasible
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 10], [2, 1], [3, 10], [4, 1], [5, float('inf')]],
        "epsilon": 4.5
    },

    # 3. Gradual slope — approximation should only use horizontal segments
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 4. High variation in the middle, flat outside
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 10], [2, 1], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 5. All values within ε band — should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.4], [2, 4.7], [3, 5.1], [4, 4.8], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 6. Duplicate values (no variation), but many pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, float('inf')]],
        "epsilon": 0.0
    },

    # 7. Extremely tight ε — forces max segmentation
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 0.1
    },

    # 8. Long constant segments broken by small blips
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 2], [2, 5], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Piece at boundary exceeds ε
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1], [2, 10], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 3.0
    },

    # 10. Flat then jump, test if algorithm separates at right point
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [2, 1], [4, 1], [6, 9], [8, 9], [10, float('inf')]],
        "epsilon": 1.5
    }
]

#Iteration12
test_cases12 = [

    # 1. Constant function — should return 1 segment for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [5, 3], [10, 3], [15, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Alternating small jumps just below ε — should merge all into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1], [3, 1.5], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Alternating just above ε — each jump exceeds ε, so multiple segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 4. Monotonically increasing — should merge all if slope is within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        "epsilon": 0.3
    },

    # 5. Large jump in the middle — should split optimally into 2
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1], [3, 10], [4, 10], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Noisy plateau — small ε forces segmentation at noise
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, 4.5], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 7. Flat region followed by spike — tests handling of outlier
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 10], [3, 0], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 8. Rapid oscillation within tolerance — should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [0.5, 2.1], [1, 1.9], [1.5, 2.05], [2, float('inf')]],
        "epsilon": 0.15
    },

    # 9. Breakpoints at same value — tests if algorithm handles redundant points
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 2], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 10. Almost mergeable blocks — off by ε+δ, should result in separate segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2.01], [2, 0], [3, 2.01], [4, float('inf')]],
        "epsilon": 2.0
    },
]

#Iteration13
test_cases13 = [
    # 1. Constant function (should return 1 piece if ε ≥ 0)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, 5], [30, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Single jump within tolerance (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5.4], [20, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Multiple small oscillations within ε (should be merged)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1.4], [4, 0.8], [6, 1.1], [8, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Alternating values that exceed ε (must split at each)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, float('inf')]],
        "epsilon": 0.9
    },

    # 5. Very small ε requiring every segment to be isolated
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        "epsilon": 0.05
    },

    # 6. Narrow domain segments (testing for tight intervals)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 1.3], [0.2, 1.6], [0.3, float('inf')]],
        "epsilon": 0.4
    },

    # 7. Single point anomaly (should still merge others)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1], [6, 10], [7, 1], [8, float('inf')]],
        "epsilon": 0.9
    },

    # 8. Long flat region, then sudden sharp change
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [10, 1], [11, 8], [12, float('inf')]],
        "epsilon": 0.5
    },

    # 9. Only one segment (trivial case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [10, float('inf')]],
        "epsilon": 1.0
    },

    # 10. Monotonic increasing values just barely within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 0.4], [4, 0.7], [6, 1.0], [8, float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration14
test_cases14 = [
    # 1. Constant function - should be merged into one segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.1
    },
    # 2. Alternating up-down pattern, no merge possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, float('inf')]],
        "epsilon": 0.5
    },
    # 3. Small linear variation within ε — should be approximated with 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3.0], [1, 3.2], [2, 3.1], [3, 3.15], [4, float('inf')]],
        "epsilon": 0.2
    },
    # 4. Large jump in middle only — forces at least two segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 10], [4, float('inf')]],
        "epsilon": 2.0
    },
    # 5. Noisy constant — within ε, so should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 5.1], [2, 4.9], [3, 5.05], [4, float('inf')]],
        "epsilon": 0.15
    },
    # 6. Single value changes only slightly but repeatedly — test greedy merge decisions
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.4], [2, 1.8], [3, 2.2], [4, float('inf')]],
        "epsilon": 0.4  # Can group [0–2) and [2–4) segments
    },
    # 7. Large domain, small ε, constant function — test scaling in x
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [100, 10], [1000, 10], [10000, 10], [20000, float('inf')]],
        "epsilon": 0.01
    },
    # 8. Spike in the middle — test if outlier causes a split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 20], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 1.0
    },
    # 9. Flat followed by a ramp — test where merge stops
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 5], [4, 8], [5, float('inf')]],
        "epsilon": 1.0
    },
    # 10. Floating point precision edge — just at tolerance boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.5], [2, 2.0], [3, float('inf')]],
        "epsilon": 0.5  # Should just allow merging
    }
]

#Iteration15
test_cases15 = [

    # 1. Constant function — one piece should be enough regardless of ε
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]], "epsilon": 0.001},

    # 2. Alternating values, ε too small to merge any
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, 5], [4, float('inf')]], "epsilon": 1.0},

    # 3. Tiny value changes within ε — can merge all
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 5.4], [2, 5.1], [3, 5.2], [4, float('inf')]], "epsilon": 0.5},

    # 4. Large ε — all segments can be merged
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 9], [3, 2], [4, float('inf')]], "epsilon": 10.0},

    # 5. Staircase pattern — increasing values, test greedy merging
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]], "epsilon": 1.0},

    # 6. Flat segments with one spike — tests skipping small spikes
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 10], [3, 2], [4, 2], [5, float('inf')]], "epsilon": 0.5},

    # 7. Long flat followed by jump — test merge up to jump
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1], [6, 10], [7, float('inf')]], "epsilon": 0.4},

    # 8. Random values — real-world behavior
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2.1], [1, 3.8], [2, 3.0], [3, 4.5], [4, 5.0], [5, float('inf')]], "epsilon": 1.0},

    # 9. ε = 0 — strict, no merging unless values are exactly equal
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 2], [3, 1], [4, float('inf')]], "epsilon": 0.0},

    # 10. Discontinuity at boundary — check if edge handling is correct
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, 0], [3, float('inf')]], "epsilon": 50},
]

#Iteration16
test_cases16 = [

    # 1. Constant function — should return 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [10, 3], [20, 3], [30, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Alternating values just within ε — should be compressed to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 4.9], [3, 5], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 3. Alternating values just outside ε — should split at each alternation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.3], [2, 4.7], [3, 5.4], [4, float('inf')]],
        "epsilon": 0.25
    },

    # 4. Step function — must split at every jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 5. Long flat followed by single spike — should not split if spike within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10], [2, 12], [3, 10], [4, 10], [5, float('inf')]],
        "epsilon": 2.0
    },

    # 6. Dense values with random noise — noise just above ε forces many segments
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10.0], [1, 10.4], [2, 9.6], [3, 10.5], [4, 9.3], [5, 10.6], [6, float('inf')]],
        "epsilon": 0.5
    },

    # 7. Noisy function within ε band — all should collapse to one segment
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 100], [1, 100.2], [2, 99.8], [3, 100.1], [4, 99.9], [5, float('inf')]],
        "epsilon": 0.25
    },

    # 8. Plateau followed by ramp — ramp exceeds ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 6], [3, 7], [4, float('inf')]],
        "epsilon": 0.9
    },

    # 9. Wide segment with slow drift — tests ε sensitivity on long segments
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 0.5], [10, 1.0], [15, 1.5], [20, float('inf')]],
        "epsilon": 0.49
    },

    # 10. Very tight ε on constant-ish function — should preserve every piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.1], [2, 0.9], [3, 1.05], [4, float('inf')]],
        "epsilon": 0.05
    }
]

#Iteration17
test_cases17 = [

    # 1. Simple two-interval case, all values within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2.5], [5, float('inf')]],
        "epsilon": 0.6
    },

    # 2. Minimal ε forces no merging (each segment retained)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 5], [3, 2], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. High ε allows all values to be merged into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 12], [2, 9], [3, 13], [4, float('inf')]],
        "epsilon": 4
    },

    # 4. Sudden jump forces split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1.5], [3, 9], [4, float('inf')]],
        "epsilon": 2
    },

    # 5. Flat function with one outlier
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 10], [3, 5], [4, float('inf')]],
        "epsilon": 2
    },

    # 6. Large number of short segments with low ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.5, 1.1], [1, 0.9], [1.5, 1.2], [2, float('inf')]],
        "epsilon": 0.1
    },

    # 7. High frequency alternating values (should not merge)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 1], [3, 3], [4, 1], [5, 3], [6, float('inf')]],
        "epsilon": 0.8
    },

    # 8. Non-uniform x-intervals but same y-values (should merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [3, 5.2], [10, 4.9], [12, float('inf')]],
        "epsilon": 0.3
    },

    # 9. Precision boundary case
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.9999], [2, 3], [3, float('inf')]],
        "epsilon": 1
    },

    # 10. Constant function — should return 1 segment regardless of ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0
    }
]

#Iteration18
test_cases18 = [
    # 1. Flat constant function (should return one piece for any ε ≥ 0)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Alternating values within tolerance — all should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.4], [2, 1.7], [3, 2.1], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Alternating values slightly beyond ε — should create new pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.6], [2, 1.4], [3, 2.9], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Single jump beyond ε — should result in exactly two pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 10], [10, float('inf')]],
        "epsilon": 4.9
    },

    # 5. Tiny ε on a smooth function — must retain each original value
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        "epsilon": 0.1
    },

    # 6. Merging all into one due to high ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 3], [2, 7], [3, 2], [4, float('inf')]],
        "epsilon": 10.0
    },

    # 7. Edge values only at ε — should still merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Sharp spike — one value far off in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Long plateau then small jump beyond ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [10, 2], [20, 5], [30, float('inf')]],
        "epsilon": 2.5
    },

    # 10. Boundary behavior — jump at first and last position
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 1], [2, 1], [3, 10], [4, float('inf')]],
        "epsilon": 4.0
    }
]

#Iteration19
test_cases19 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, float('inf')]],
        "epsilon": 0.0  # Flat constant function — can be merged to a single segment
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, float('inf')]],
        "epsilon": 1.0  # Jump too large to merge all — must split at middle
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 7], [3, 5], [4, float('inf')]],
        "epsilon": 0.75  # Tight ε forces 3 segments
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 2], [3, 2.5], [4, 3], [5, float('inf')]],
        "epsilon": 0.6  # Gradual change — can be approximated by fewer segments
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.4], [2, 1.8], [3, 1.2], [4, float('inf')]],
        "epsilon": 0.5  # All values within 0.4 range — should be compressed to 1 segment
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, -10], [2, 10], [3, -10], [4, float('inf')]],
        "epsilon": 20.1  # Wild oscillation, but high epsilon allows full merge
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 100], [4, 100], [5, float('inf')]],
        "epsilon": 10.0  # One large jump requires split, rest can be merged
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.000001, 1000], [1, float('inf')]],
        "epsilon": 999.0  # One tiny segment forces split if ε < jump
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0.5, 0], [1.0, 0], [1.5, 0], [2.0, 0], [2.5, 0.001], [3.0, float('inf')]],
        "epsilon": 0.001  # Tiny epsilon exposes small changes at the end
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 2], [2, 3], [3, 2], [4, 3], [5, 2], [6, float('inf')]],
        "epsilon": 1.0  # Oscillating between 2 and 3 — merge possible
    }
]

#Iteration20
test_cases20 = [

    # 1. Single constant function - should return one segment for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Two segments with a jump larger than ε — must split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 7], [2, float('inf')]],
        "epsilon": 2.0
    },

    # 3. Multiple small jumps within ε — should be merged into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.5], [2, 6], [3, 5.7], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 4. Alternating above/below a central value — tests merge over variation
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [1, 6], [2, 4], [3, 6], [4, float('inf')]],
        "epsilon": 1.1
    },

    # 5. Jump right on ε — borderline case
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Increasing sequence — should not be merged when difference exceeds ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 5], [3, 7], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 7. Plateau, then spike — spike should be isolated
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [1, 4], [2, 9], [3, 4], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 8. Zero-width intervals — must be ignored or skipped in decision
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 5], [1, 1], [2, float('inf')]],
        "epsilon": 1.5
    },

    # 9. Function with exact repetitions — all values same, should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 3], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 10. Tiny ε with noise — forces segmentation for small variations
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 1.05], [3, 0.95], [4, float('inf')]],
        "epsilon": 0.05
    }
]

#Iteration21
test_cases21 = [

    # 1. Flat function: single constant value across the domain
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1  # Should require only one piece
    },

    # 2. Alternating high-low values with epsilon tight enough to require splitting
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4  # Should need all segments separately
    },

    # 3. Almost equal values within tolerance: can merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.05], [3, float('inf')]],
        "epsilon": 0.2  # All should be merged
    },

    # 4. Large jump in the middle requiring a split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2.1], [4, 20], [5, 2.1], [6, float('inf')]],
        "epsilon": 0.5  # Should split around the peak
    },

    # 5. Small domain intervals with tight epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 2], [0.2, 3], [0.3, float('inf')]],
        "epsilon": 0.4  # Should split each due to tight tolerance
    },

    # 6. Large epsilon: everything can be approximated with one constant
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -100], [1, 50], [2, 100], [3, float('inf')]],
        "epsilon": 200  # One piece is enough
    },

    # 7. Long constant region followed by spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 0], [11, 100], [12, float('inf')]],
        "epsilon": 10  # Should split off the spike
    },

    # 8. Function with oscillation just below the threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.9], [2, 1.1], [3, 1.8], [4, float('inf')]],
        "epsilon": 1  # Should keep all together
    },

    # 9. Values right on the edge of epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1  # Should form overlapping pieces: [0,2), [2,4)
    },

    # 10. Duplicate x-values (should be handled or raise an error depending on implementation)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [0, 10], [1, 5], [2, float('inf')]],
        "epsilon": 5  # Should test robustness
    }
]

#Iteration22
test_cases22 = [
    # Test Case 1: Flat function (should return 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 0.1
    },

    # Test Case 2: One jump exactly within ε (should return 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [10, 3.5], [20, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 3: One jump just outside ε (should return 2 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [10, 3.6], [20, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 4: Zigzag pattern with values within ε band (mergeable)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5.1], [4, 4.9], [6, 5], [10, float('inf')]],
        "epsilon": 0.2
    },

    # Test Case 5: Zigzag pattern outside ε (should split into more segments)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 6], [4, 4], [6, 7], [10, float('inf')]],
        "epsilon": 0.9
    },

    # Test Case 6: Short segments with large ε (should merge all into one)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1.5], [3, 1.7], [4, float('inf')]],
        "epsilon": 1.0
    },

    # Test Case 7: Many identical segments with noise just at ε (sensitive edge)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.5], [2, 0.5], [3, 1.5], [4, 0.5], [5, 1],
                  [6, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 8: Increasing trend within tolerance (all can be one segment)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [2, 2.3], [4, 2.5], [6, 2.1], [8, 2.4], [10, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 9: Monotonic change just beyond ε (should split appropriately)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 0.4], [4, 0.9], [6, 1.5], [8, 2.1], [10, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 10: Very close breakpoints, small ε (tests handling density)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [0.01, 1.1], [0.02, 1.2], [0.03, 1.3], [0.04, float('inf')]],
        "epsilon": 0.05
    }
]

#Iteration23
test_cases23 = [
    # 1. Perfectly constant function — should return 1 segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Small oscillations within epsilon — should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.05], [2, 1.98], [3, float('inf')]],
        "epsilon": 0.1
    },

    # 3. One jump slightly above epsilon — should split into two segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, float('inf')]],
        "epsilon": 0.15
    },

    # 4. Alternating values within epsilon — should merge to one segment
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 3.1], [4, 2.9], [6, float('inf')]],
        "epsilon": 0.15
    },

    # 5. Large jumps beyond epsilon — no segments can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 8], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Long constant region then sudden jump — should return 2 segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [5, 5], [10, 10], [15, float('inf')]],
        "epsilon": 0.9
    },

    # 7. Very small epsilon with small noise — nothing can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.001], [2, 0.999], [3, float('inf')]],
        "epsilon": 0.0005
    },

    # 8. Merging with midpoint value better than endpoints
    # Merging [1,2)=2 and [2,3)=4 → midpoint=3, error to endpoints = 1
    {
        "pc_fx": [[-float('inf'), float('inf')], [1, 2], [2, 4], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Oscillations just outside epsilon — no merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.3], [2, 9.7], [3, float('inf')]],
        "epsilon": 0.25
    },

    # 10. Boundary condition test — merge edge segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, 0.05], [3, float('inf')]],
        "epsilon": 0.1
    }
]

#Iteration24
test_cases24 = [
    {
        # Case 1: Constant function (should return one segment for any ε)
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1
    },
    {
        # Case 2: Small jump just within ε
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5.05], [4, 5.1], [6, float('inf')]],
        "epsilon": 0.1
    },
    {
        # Case 3: Small jump just above ε (should force extra segment)
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5.05], [4, 5.2], [6, float('inf')]],
        "epsilon": 0.1
    },
    {
        # Case 4: Alternating values around a central value, just outside ε
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 1], [3, 3], [4, float('inf')]],
        "epsilon": 0.9
    },
    {
        # Case 5: All values within ε of midpoint — should merge to one segment
        "pc_fx": [[-float('inf'), float('inf')], [0, 4.9], [1, 5.1], [2, 5.0], [3, 4.95], [4, float('inf')]],
        "epsilon": 0.2
    },
    {
        # Case 6: One outlier value forcing a split
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 8], [4, 5], [5, float('inf')]],
        "epsilon": 1.0
    },
    {
        # Case 7: Increasing ramp, forcing fine approximation
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, float('inf')]],
        "epsilon": 0.5
    },
    {
        # Case 8: Random values, all within ε of average
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.9], [1, 3.1], [2, 3.0], [3, 3.05], [4, float('inf')]],
        "epsilon": 0.2
    },
    {
        # Case 9: Flat → jump → flat — check if algorithm isolates the jump
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2], [4, 10], [6, 10], [8, float('inf')]],
        "epsilon": 1.0
    },
    {
        # Case 10: Edge case — only boundary points and one internal point
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, float('inf')]],
        "epsilon": 3.9
    }
]

#Iteration25
test_cases25 = [

    # Test Case 1: Flat function — should require only one piece for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, 5], [30, float('inf')]],
        "epsilon": 0.0
    },

    # Test Case 2: Alternating small variations within epsilon — mergeable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.2], [2, 1.9], [3, 2.1], [4, float('inf')]],
        "epsilon": 0.2
    },

    # Test Case 3: Alternating variations just over epsilon — not mergeable
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.3], [2, 1.8], [3, 2.1], [4, float('inf')]],
        "epsilon": 0.2
    },

    # Test Case 4: Increasing values with large jumps — each piece needs to be separate
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 10], [3, 15], [4, float('inf')]],
        "epsilon": 2
    },

    # Test Case 5: Oscillations around a center value, test tight ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.1], [2, 10.05], [3, 9.95], [4, float('inf')]],
        "epsilon": 0.1
    },

    # Test Case 6: ε = 0 forces exact preservation of function values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.0
    },

    # Test Case 7: One outlier in middle — should force split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 10], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 1
    },

    # Test Case 8: Equal spacing and values oscillating in a range that’s just on the edge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 1
    },

    # Test Case 9: Repeating pattern that could be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 5], [3, 5.1], [4, float('inf')]],
        "epsilon": 0.15
    },

    # Test Case 10: Long segment with small ε — force multiple pieces
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[x, x * 0.01] for x in range(10)] +
                 [[10, float('inf')]],
        "epsilon": 0.02
    }

]

#Iteration26
test_cases26 = [
    # 1. Simple mergeable segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.05], [3, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Constant function (should return 1 segment)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 0.0
    },

    # 3. Single jump exceeding ε (should return 2 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 4. Small oscillation pattern (should be merged)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 2.2], [3, 2.05], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 5. Large value spike in middle (should force 3 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 1], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 6. Minimal values differing exactly by epsilon (can merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, float('inf')]],
        "epsilon": 2.0
    },

    # 7. Just over ε difference (force split)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1.1], [2, 2.2], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 8. Zig-zag pattern inside ε range (should be 1 segment)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4.95], [2, 5.05], [3, 4.9], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 9. Increasing values below ε (should be merged)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3.05], [2, 3.1], [3, 3.15], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 10. Alternating high/low beyond ε (should not merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4.0
    }
]

#Iteration27
test_cases27 = [
    # 1. Constant function – should be approximated with 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Sharp jump just over ε – should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Small fluctuations within ε – should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.3], [2, 1.2], [3, 1.1], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Values alternate above and below mean, just beyond ε – must split each
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, float('inf')]],
        "epsilon": 0.9
    },

    # 5. Long flat + small blip exceeding ε – should split at the blip
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, 1], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 6. Increasing ramp – should be many pieces depending on ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.6
    },

    # 7. Values within ε of each other – entire series should be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.2], [2, 9.8], [3, 10.1], [4, float('inf')]],
        "epsilon": 0.3
    },

    # 8. Single spike in middle exceeding ε – should force a split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 10], [3, 3], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 9. Tolerance just high enough to merge all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2.5], [2, 2.7], [3, 1.1], [4, float('inf')]],
        "epsilon": 1.0  # mean is ~2, all within ±1
    },

    # 10. Two large jumps but one within ε – should result in 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.3], [2, 4], [3, 4.1], [4, float('inf')]],
        "epsilon": 0.4
    },
]

#Iteration28
test_cases28 = [

    # 1. Simple flat constant function — should return 1 piece regardless of ε > 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 2. All values within epsilon band — should merge into a single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1.05], [4, 0.98], [6, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Sharp jump beyond epsilon — must split into 2
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1], [10, 3], [15, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Many small oscillations within ε — should merge all into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 10], [1, 10.2], [2, 9.9], [3, 10.1], [4, 10.05], [5, float('inf')]],
        "epsilon": 0.3
    },

    # 5. One outlier forces splitting — rest could be merged
    {
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 2], [1, 2.1], [2, 7], [3, 2], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 6. Minimum ε = 0 — no approximation allowed, must preserve all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 7. Duplicate values with redundant breakpoints — should merge if within ε
    {
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 5], [1, 5], [2, 5.05], [3, 5], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 8. Large plateau and a small bump that exceeds ε — should split only at bump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 4], [10, 4], [11, 6], [12, 4], [20, float('inf')]],
        "epsilon": 1.0
    },

    # 9. All values increase linearly — need to split at each if ε is small
    {
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 10. Alternating high/low values just at ε — should preserve 1 if inclusive
    {
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 5], [1, 5.5], [2, 4.5], [3, 5.5], [4, float('inf')]],
        "epsilon": 0.5
    }

]

#Iteration29
test_cases29 = [
    # Test Case 1: Single constant function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1
    },
    # Test Case 2: Strict alternation — should result in maximum splitting
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 4.9
    },
    # Test Case 3: All values within ε-band — should merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 4.9], [3, 5.05], [4, float('inf')]],
        "epsilon": 0.2
    },
    # Test Case 4: Large jump just over ε — should force split
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.4], [2, 6.1], [3, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 5: Monotonic increasing, within ε-band
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 6: Noisy values just under ε from a common center
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3.4], [2, 2.6], [3, 3.3], [4, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 7: Constant then sharp spike then constant
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 10], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 3.9
    },
    # Test Case 8: Gradual change that slowly exceeds ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1.5
    },
    # Test Case 9: Redundant identical values (should compress)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [1, 7], [2, 7], [3, 7], [4, float('inf')]],
        "epsilon": 0
    },
    # Test Case 10: Tolerance ε = 0, must match exactly
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0
    }
]

#Iteration30
test_cases30 = [
    # 1. Constant function (should always return 1 piece regardless of epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Alternating values slightly above and below epsilon (tests tight switching)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]],
        "epsilon": 0.4  # Too small to merge; expect 4 pieces
    },

    # 3. Flat segments with small noise within epsilon (should merge all into one)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.05], [3, 0.95], [4, float('inf')]],
        "epsilon": 0.1  # Should merge all; max deviation is 0.1
    },

    # 4. Single jump exceeding epsilon (forces a split at that point)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 2.0  # Jump = 4, needs 2 segments
    },

    # 5. Linear increasing staircase (forces piece creation at each step if jump > ε)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.9  # Each jump = 1, so needs 4 segments
    },

    # 6. All values within ε of a central value (should return 1 segment)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.2], [2, 5.1], [3, 4.9], [4, float('inf')]],
        "epsilon": 0.2  # All deviations ≤ 0.2 → merge into one
    },

    # 7. Long flat, short spike (outlier causes segmentation)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 10], [3, 0], [4, 0], [5, float('inf')]],
        "epsilon": 1.0  # Spike too big → expect 3 pieces
    },

    # 8. ε exactly equals half the max deviation (forces precise behavior)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 4], [3, 6], [4, float('inf')]],
        "epsilon": 3.0  # midpoint is 3, max deviation = 3 → just fits
    },

    # 9. Duplicate x-values with different y-values (invalid, tests robustness)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0, 2], [1, 1.5], [2, 1.5], [3, float('inf')]],
        "epsilon": 0.5  # Should be flagged or handled gracefully
    },

    # 10. Alternating step function, but ε large enough to merge all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 5.5  # Deviation too large to merge all, expect 4 pieces
    }
]


