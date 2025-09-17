#17 Sept 12:25AM
#Iteration1
test_cases1 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, 5], [30, float('inf')]],
        "epsilon": 0.1,
        "description": "Constant function — should compress to 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.05], [2, 4.95], [3, 5], [4, float('inf')]],
        "epsilon": 0.2,
        "description": "Oscillations within ε — should merge into 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.3], [2, 4.6], [3, 5.1], [4, float('inf')]],
        "epsilon": 0.2,
        "description": "Oscillations exceed ε — must keep multiple pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 2], [4, float('inf')]],
        "epsilon": 0.0,
        "description": "Zero tolerance — must preserve all pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, -10], [3, 5], [4, float('inf')]],
        "epsilon": 20,
        "description": "Huge tolerance — everything merges to 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2], [10, 8], [15, 2], [20, float('inf')]],
        "epsilon": 1,
        "description": "Middle jump — should preserve central piece, merge others if possible."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Alternating high/low — forces nearly all cuts."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 15,
        "description": "Alternating high/low but large ε — should compress to 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1], [6, 20], [10, 20], [15, float('inf')]],
        "epsilon": 2,
        "description": "Flat then jump — should keep 2 pieces (before and after jump)."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.1, 1.5], [10, 1.2], [100, 1.4], [200, float('inf')]],
        "epsilon": 0.6,
        "description": "Non-uniform x spacing — should merge if values within ε."
    }
]

#Iteration2
test_cases2 = [
    # 1. Simple single jump (ε small, must preserve jump)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 5], [2, float('inf')]],
        "epsilon": 1.0
    },

    # 2. Jump smaller than epsilon (should merge into one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 2.4], [2, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Oscillating values within epsilon (should collapse into one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.5], [2, 4.8], [3, 5.2], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 4. Alternating big jumps (forces multiple pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 5. Long flat segment (should remain 1 piece regardless of epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 7], [10, 7], [20, 7], [30, float('inf')]],
        "epsilon": 0.5
    },

    # 6. Just at epsilon threshold (borderline merge vs split)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, float('inf')]],
        "epsilon": 2.0
    },

    # 7. Multiple small jumps add up but individually < epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 0.5], [2, 1.0], [3, 1.5], [4, float('inf')]],
        "epsilon": 0.6
    },

    # 8. Extreme boundaries with large values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [-1000, 100], [0, -100], [1000, 100], [2000, float('inf')]],
        "epsilon": 150.0
    },

    # 9. Duplicate consecutive values (should compress redundancies)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 4], [1, 4], [2, 4], [3, 4], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 10. High-frequency oscillation just above epsilon (forces many cuts)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [0.5, 2.1], [1, -2.2], [1.5, 2.3], [2, -2.4], [2.5, float('inf')]],
        "epsilon": 2.0
    }
]

#Iteration3
test_cases3 = [
    # 1. Single flat piece, no approximation needed
    {
        "desc": "Flat constant function, any ε > 0 should merge to 1 piece.",
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[10,5],[20,5],[30,float('inf')]],
        "epsilon": 0.1
    },

    # 2. Two constant pieces, exactly ε apart
    {
        "desc": "Values differ by exactly ε, should remain 2 pieces (not merge).",
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[5,2],[10,float('inf')]],
        "epsilon": 1.0
    },

    # 3. Two constant pieces, difference < ε
    {
        "desc": "Values differ less than ε, should merge to 1 piece.",
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[5,1.5],[10,float('inf')]],
        "epsilon": 1.0
    },

    # 4. Rapid oscillation around a baseline
    {
        "desc": "Alternating ±0.4 around 5, should merge into 1 piece if ε >= 0.5.",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,5],[1,5.4],[2,4.6],[3,5.2],[4,4.8],[5,5],
                  [6,float('inf')]],
        "epsilon": 0.5
    },

    # 5. Increasing ramp, large ε
    {
        "desc": "Strictly increasing but within ε tolerance, should merge all to 1 piece.",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,0],[2,1],[4,2],[6,3],[8,4],[10,5],[12,float('inf')]],
        "epsilon": 3.0
    },

    # 6. Increasing ramp, small ε
    {
        "desc": "Strictly increasing, small ε forces many pieces.",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,0],[2,1],[4,2],[6,3],[8,4],[10,5],[12,float('inf')]],
        "epsilon": 0.4
    },

    # 7. Edge case: tiny domain segment
    {
        "desc": "One segment is very short but value differs beyond ε, must be separate.",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,1],[0.001,10],[1,1],[2,float('inf')]],
        "epsilon": 2.0
    },

    # 8. Large flat regions separated by spikes
    {
        "desc": "Flat baseline with spikes outside ε, spikes must remain separate pieces.",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,5],[2,5],[3,20],[4,5],[6,5],[8,50],[9,5],[12,float('inf')]],
        "epsilon": 3.0
    },

    # 9. Step function alternating between two values
    {
        "desc": "Alternating high/low values larger than ε, must keep all steps.",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,0],[1,10],[2,0],[3,10],[4,0],[5,10],[6,float('inf')]],
        "epsilon": 5.0
    },

    # 10. Boundary markers only, no internal pieces
    {
        "desc": "No actual pieces, should return empty or handle gracefully.",
        "pc_fx": [[-float('inf'), float('inf')],[0,float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration4
test_cases4 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 0.0,
        "description": "Flat function — should reduce to 1 piece regardless of interval length."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.4,
        "description": "Oscillating function with small epsilon — should require many pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 10], [4, 0], [6, float('inf')]],
        "epsilon": 5,
        "description": "Large jump with medium epsilon — allows merging into 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 0.9,
        "description": "Monotone increasing values, epsilon just under step size — no merging possible."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 1.1,
        "description": "Monotone increasing values, epsilon just above step size — allows merging into fewer pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 9.9,
        "description": "Alternating extremes with epsilon just under jump size — cannot merge across jumps."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 10,
        "description": "Alternating extremes with epsilon equal to jump size — everything can merge into 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 2.9], [3, 3.1], [4, 2.95], [5, float('inf')]],
        "epsilon": 0.2,
        "description": "Clustered small oscillations within tolerance — should merge into 1 piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 100], [50, 102], [100, 98], [150, 101], [200, 99], [250, float('inf')]],
        "epsilon": 3,
        "description": "Large plateau with small fluctuations — should merge into 1 piece if algorithm is optimal."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, 50], [3, 100], [4, 0], [5, float('inf')]],
        "epsilon": 49.9,
        "description": "Non-monotone with huge swings, epsilon just under mid-gap — forces multiple pieces."
    }
]

#Iteration5
test_cases5 = [
    # 1. Simple constant function (should compress to 1 piece regardless of epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[5,2],[10,2],[15,float('inf')]],
        "epsilon": 0.1
    },

    # 2. Single jump just above epsilon (forces 2 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[5,1.9],[10,float('inf')]],
        "epsilon": 0.5
    },

    # 3. Single jump within epsilon (compressible to 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[5,1.4],[10,float('inf')]],
        "epsilon": 0.5
    },

    # 4. Alternating up-down pattern (tests greedy vs optimal)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,1],[3,3],[4,1],[5,float('inf')]],
        "epsilon": 1.0
    },

    # 5. Increasing staircase (epsilon small, must keep all jumps)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,4],[5,float('inf')]],
        "epsilon": 0.4
    },

    # 6. Increasing staircase (large epsilon, can merge all)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,4],[5,float('inf')]],
        "epsilon": 2.5
    },

    # 7. Sharp spike in the middle (forces extra piece locally)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[2,2],[3,10],[4,2],[5,2],[6,float('inf')]],
        "epsilon": 1.5
    },

    # 8. Small oscillations (all within epsilon, should merge)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5.2],[2,4.9],[3,5.1],[4,5.05],[5,float('inf')]],
        "epsilon": 0.3
    },

    # 9. Large gap in domain with same values (tests boundaries)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,7],[1000,7],[2000,7],[3000,float('inf')]],
        "epsilon": 0.1
    },

    # 10. Mixed pattern: flat → jump → noisy region (stress test)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,1],[2,1],[3,5],   # jump
                  [4,5.1],[5,4.9],[6,5.05],[7,5],  # noise
                  [8,float('inf')]],
        "epsilon": 0.2
    }
]

#Iteration6
test_cases6 = [

    # 1. Simple single plateau, no approximation needed
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[5,2],[10,float('inf')]],
        "epsilon": 0.1,
        # Expect: only 1 piece needed (flat function)
    },

    # 2. Small variation within epsilon, should merge to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[2,2.2],[4,1.9],[6,float('inf')]],
        "epsilon": 0.3,
        # Expect: all merged since variation ≤ 0.3
    },

    # 3. Variation just above epsilon, should split
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[2,3],[4,float('inf')]],
        "epsilon": 0.5,
        # Expect: two pieces, since |2-3|=1 > epsilon
    },

    # 4. Alternating high/low values (forces splitting)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,0],[3,10],[4,float('inf')]],
        "epsilon": 4,
        # Expect: many pieces, since jumps > epsilon
    },

    # 5. Constant ramp (monotone increasing values)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,float('inf')]],
        "epsilon": 1.0,
        # Expect: can group in fewer pieces (each span of 2 units can merge)
    },

    # 6. Tight epsilon (forces exact preservation)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,float('inf')]],
        "epsilon": 0.0,
        # Expect: every change is significant, so all n pieces preserved
    },

    # 7. Large epsilon (collapse everything)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[2,10],[4,15],[6,20],[8,float('inf')]],
        "epsilon": 100,
        # Expect: only 1 piece, since tolerance covers all variation
    },

    # 8. Boundary markers only (edge case)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,float('inf')]],
        "epsilon": 0.1,
        # Expect: trivial case, exactly 1 piece
    },

    # 9. Flat sections with one big outlier
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[2,2],[3,20],[4,2],[5,float('inf')]],
        "epsilon": 1,
        # Expect: one piece for flat baseline, one piece isolating the outlier
    },

    # 10. Long sequence of small oscillations
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,5],[1,5.1],[2,4.9],[3,5.2],[4,4.8],[5,5.05],[6,float('inf')]],
        "epsilon": 0.3,
        # Expect: all merged into one piece, since all oscillations are within epsilon
    },
]

#Iteration7
test_cases7 = [
    # 1. Trivial constant function (should always reduce to 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[10,5],[20,float('inf')]],
        "epsilon": 0.1
    },

    # 2. Two equal values within epsilon tolerance (mergeable into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[5,2.2],[10,float('inf')]],
        "epsilon": 0.25
    },

    # 3. Strict alternating values just outside epsilon (cannot merge)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,1],[3,3],[4,float('inf')]],
        "epsilon": 0.9
    },

    # 4. Alternating values within epsilon (all mergeable into 1)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.4],[2,0.9],[3,1.3],[4,float('inf')]],
        "epsilon": 0.5
    },

    # 5. Large jump vs small jump (forces split at big jump only)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[2,1.1],[4,1.05],[6,10],[8,float('inf')]],
        "epsilon": 0.2
    },

    # 6. Increasing linear-like staircase within tolerance (should merge to 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,0.3],[2,0.6],[3,0.9],[4,float('inf')]],
        "epsilon": 0.5
    },

    # 7. Boundary stress case with inf at start/end (step jump at boundaries)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[2,9],[5,float('inf')]],
        "epsilon": 3.9
    },

    # 8. Exact equality at epsilon boundary (merge should succeed)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,float('inf')]],
        "epsilon": 1.0
    },

    # 9. Floating-point precision edge case (tiny differences)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1.0000001],[1,1.0000002],[2,1.0000003],[3,float('inf')]],
        "epsilon": 1e-6
    },

    # 10. Non-mergeable multi-segment test (forces maximum segmentation)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,0],[3,10],[4,float('inf')]],
        "epsilon": 4.9
    }
]

#Iteration8
test_cases8 = [

    # 1. Constant function (should compress fully to 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [2, 5], [4, 5], [7, 5], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Small oscillations within epsilon (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.2], [2, 4.9], [3, 5.1], [4, float('inf')]],
        "epsilon": 0.3
    },

    # 3. Oscillations above epsilon (must split into multiple pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 3], [2, 0], [3, 4], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Two large plateaus with a big jump (must keep 2 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [5, 1], [6, 10], [10, 10], [12, float('inf')]],
        "epsilon": 2.0
    },

    # 5. Just barely mergeable (difference = epsilon exactly)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [2, 7], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 6. Just barely not mergeable (difference = epsilon + tiny amount)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [2, 7.1], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 7. Increasing staircase (multiple small steps)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 1.5
    },

    # 8. Decreasing staircase (mirror case of 7)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 9], [2, 8], [3, 7], [4, 6], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Sharp spike in the middle (forces local split)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [2, 2], [3, 100], [4, 2], [5, 2], [6, float('inf')]],
        "epsilon": 5.0
    },

    # 10. Alternating high/low values (checkerboard, forces many pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 4.0
    },
]

#Iteration9
test_cases9 = [
    # 1. Constant function (should merge into 1 piece regardless of epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[2,5],[4,5],[6,float('inf')]],
        "epsilon": 0.1
    },

    # 2. Small oscillations within epsilon (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.2],[2,0.9],[3,1.05],[4,float('inf')]],
        "epsilon": 0.3
    },

    # 3. Oscillations just above epsilon (should not merge fully)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,2],[2,0],[3,2],[4,float('inf')]],
        "epsilon": 0.9
    },

    # 4. Exact epsilon threshold merge
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[2,1],[4,2],[6,float('inf')]],
        "epsilon": 1.0
    },

    # 5. Big jump requiring split (forces multiple pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,0],[3,10],[4,float('inf')]],
        "epsilon": 2.0
    },

    # 6. Redundant boundaries (should ignore duplicates and merge correctly)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,2],[3,2],[4,float('inf')]],
        "epsilon": 0.0
    },

    # 7. Piecewise increasing slope (check gradual growth against epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,float('inf')]],
        "epsilon": 1.1
    },

    # 8. Alternating up/down values (hardest case for greedy algorithms)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,5],[2,0],[3,5],[4,0],[5,float('inf')]],
        "epsilon": 2.5
    },

    # 9. Large epsilon (should collapse everything into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,100],[1,-100],[2,50],[3,-50],[4,float('inf')]],
        "epsilon": 200
    },

    # 10. Very small epsilon (forces exact partitioning, no merges)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,0.5],[2,1],[3,1.5],[4,2],[5,float('inf')]],
        "epsilon": 0.01
    },
]

#Iteration10
test_cases10 = [
    # 1. Simple linear increase, small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 2],[2, 3],[3, float('inf')]],
        "epsilon": 0.1
    },
    # 2. Constant function (should return single piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 5],[2, 5],[3, float('inf')]],
        "epsilon": 0.0
    },
    # 3. Single large jump
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 10],[2, 10],[3, float('inf')]],
        "epsilon": 2.0
    },
    # 4. Oscillating values within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 1.4],[2, 1.2],[3, float('inf')]],
        "epsilon": 0.5
    },
    # 5. Sharp peak that exceeds epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 2],[1, 8],[2, 2],[3, float('inf')]],
        "epsilon": 1.0
    },
    # 6. Single piece already within epsilon tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 3],[1, 3.2],[2, 3.1],[3, float('inf')]],
        "epsilon": 0.25
    },
    # 7. Decreasing then increasing
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 10],[1, 5],[2, 10],[3, float('inf')]],
        "epsilon": 4.0
    },
    # 8. Multiple equal segments (should merge if epsilon allows)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 7],[1, 7.1],[2, 7.05],[3, 7],[4, float('inf')]],
        "epsilon": 0.2
    },
    # 9. Tiny epsilon forcing all separate pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 2],[2, 1.5],[3, 2.5],[4, float('inf')]],
        "epsilon": 0.01
    },
    # 10. Large epsilon collapsing multiple peaks
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 5],[2, 3],[3, 4],[4, float('inf')]],
        "epsilon": 5.0
    }
]

#Iteration11
test_cases11 = [
    # 1. Already constant function: should merge all into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,5],[4,float('inf')]],
        "epsilon": 0.5
    },
    # 2. Alternating small oscillations: epsilon smaller than oscillation, cannot merge
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,1],[3,2],[4,float('inf')]],
        "epsilon": 0.4
    },
    # 3. Oscillations exactly at epsilon: can merge optimally
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.5],[2,1],[3,1.5],[4,float('inf')]],
        "epsilon": 0.5
    },
    # 4. Linear increase: constant pieces will be small, testing tolerance merging
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,float('inf')]],
        "epsilon": 1
    },
    # 5. Sharp peak: algorithm must decide whether to split or merge
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,5],[2,1],[3,0],[4,float('inf')]],
        "epsilon": 2
    },
    # 6. Flat with single spike: tests ignoring isolated outlier
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,10],[3,2],[4,float('inf')]],
        "epsilon": 3
    },
    # 7. Gradual rise and fall: should merge into fewer pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,1],[4,0],[5,float('inf')]],
        "epsilon": 1
    },
    # 8. Two distant flat regions: testing boundaries
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,3],[1,3],[5,7],[6,7],[10,float('inf')]],
        "epsilon": 0.5
    },
    # 9. High-frequency oscillation within epsilon: can merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.2],[2,0.8],[3,1.1],[4,0.9],[5,float('inf')]],
        "epsilon": 0.5
    },
    # 10. Edge case: epsilon = 0, must retain all original pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,2],[2,1],[3,3],[4,float('inf')]],
        "epsilon": 0
    },
]

#Iteration12
test_cases12 = [
    # 1. Simple increasing sequence
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 2],[2, 3],[3, float('inf')]],
        "epsilon": 0.5
    },

    # 2. Simple decreasing sequence
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 4],[2, 3],[3, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Single plateau in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 2],[1, 2],[2, 2],[3, float('inf')]],
        "epsilon": 0.1
    },

    # 4. Oscillating values that cannot merge easily
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 3],[2, 1],[3, 3],[4, 1],[5, float('inf')]],
        "epsilon": 0.5
    },

    # 5. Large jump exceeding epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 0],[1, 10],[2, 0],[3, float('inf')]],
        "epsilon": 2.0
    },

    # 6. Flat function, should be one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 5],[2, 5],[3, 5],[4, float('inf')]],
        "epsilon": 0.01
    },

    # 7. Values barely within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1.0],[1, 1.4],[2, 1.9],[3, 2.3],[4, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Negative and positive values
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, -2],[1, -1],[2, 0],[3, 1],[4, 2],[5, float('inf')]],
        "epsilon": 0.5
    },

    # 9. Repeated values interspersed with jumps
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 1],[2, 4],[3, 4],[4, 2],[5, 2],[6, float('inf')]],
        "epsilon": 0.75
    },

    # 10. Minimal pieces but large tolerance, should merge everything
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 2],[1, 5],[2, 3],[3, 6],[4, 1],[5, float('inf')]],
        "epsilon": 10
    }
]

#Iteration13
test_cases13 = [

    # 1. Simple linear increasing values, small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,float('inf')]],
        "epsilon": 0.1
    },

    # 2. Constant function (should return 1 piece for any epsilon >= 0)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,float('inf')]],
        "epsilon": 0.0
    },

    # 3. Single jump, epsilon smaller than jump (requires splitting)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,10],[2,float('inf')]],
        "epsilon": 2.0
    },

    # 4. Single jump, epsilon large enough to merge pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,float('inf')]],
        "epsilon": 2.0
    },

    # 5. Oscillating values (alternating high/low), small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,5],[2,0],[3,5],[4,float('inf')]],
        "epsilon": 1.0
    },

    # 6. Edge case: very small interval differences
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[0.001,1.2],[0.002,1.1],[0.003,float('inf')]],
        "epsilon": 0.05
    },

    # 7. Increasing then decreasing (like a peak), medium epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,2],[3,1],[4,float('inf')]],
        "epsilon": 0.5
    },

    # 8. Long flat section followed by a jump
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[5,2],[10,8],[15,float('inf')]],
        "epsilon": 1.0
    },

    # 9. Multiple very close jumps, testing tolerance merging
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1.01,1.05],[1.02,1.1],[1.03,float('inf')]],
        "epsilon": 0.1
    },

    # 10. Large negative and positive values
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,-100],[1,100],[2,-100],[3,100],[4,float('inf')]],
        "epsilon": 50
    }

]

#Iteration14
test_cases14 = [
    # 1. Simple increasing sequence, small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,float('inf')]],
        "epsilon": 0.1
    },
    # 2. Constant function, any epsilon should allow single piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,float('inf')]],
        "epsilon": 0.5
    },
    # 3. Alternating high/low values, small epsilon (forces max pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,0],[3,10],[4,float('inf')]],
        "epsilon": 1
    },
    # 4. Two equal neighboring values, epsilon equal to difference (tests merge)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,3],[3,float('inf')]],
        "epsilon": 1
    },
    # 5. Sharp spike in middle, epsilon just below spike (cannot merge spike)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,10],[2,1],[3,float('inf')]],
        "epsilon": 4
    },
    # 6. Gradually increasing then decreasing, epsilon allows partial merge
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,2],[4,1],[5,float('inf')]],
        "epsilon": 1
    },
    # 7. Large plateau in middle, small spikes at ends
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,5],[2,5],[3,5],[4,0],[5,float('inf')]],
        "epsilon": 0.5
    },
    # 8. Single discontinuity exactly at epsilon threshold
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,3],[2,float('inf')]],
        "epsilon": 0.5
    },
    # 9. Random small fluctuations, epsilon large enough to merge all
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.1],[2,0.9],[3,1.05],[4,float('inf')]],
        "epsilon": 0.2
    },
    # 10. Increasing then plateau, then drop (tests optimal cut placement)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,3],[4,0],[5,float('inf')]],
        "epsilon": 0.5
    },
]

#Iteration15
test_cases15 = [
    # Test Case 1: Already constant
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,5],[4,float('inf')]],
        "epsilon": 0.1
    },
    # Test Case 2: Two values within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5.05],[2,5],[3,float('inf')]],
        "epsilon": 0.1
    },
    # Test Case 3: Small spike exceeding epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,3],[2,2],[3,float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 4: Monotonically increasing
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,4],[4,float('inf')]],
        "epsilon": 0.8
    },
    # Test Case 5: Edge at boundary
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.9],[2,2.8],[3,float('inf')]],
        "epsilon": 0.95
    },
    # Test Case 6: Alternating high-low pattern
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,1],[3,3],[4,float('inf')]],
        "epsilon": 1
    },
    # Test Case 7: Single piece large jump
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,10],[2,2],[3,float('inf')]],
        "epsilon": 5
    },
    # Test Case 8: Gradual slope, epsilon smaller than max slope
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,4],[4,5],[5,float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 9: Two identical peaks separated
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,5],[2,1],[3,5],[4,float('inf')]],
        "epsilon": 1
    },
    # Test Case 10: Piece with large epsilon to merge all
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,3],[2,4],[3,5],[4,float('inf')]],
        "epsilon": 5
    }
]

#Iteration16
test_cases16 = [
    # 1. Simple increasing function, should be approximable by merging some segments
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 2. Function with a plateau in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Decreasing then increasing (V-shape)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 3], [2, 2], [3, 4], [4, 6], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 4. Sharp spike in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 2.0
    },

    # 5. All constant, should merge into a single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 3], [3, 3], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 6. Alternating high-low values (zigzag)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, 5], [4, 1], [5, float('inf')]],
        "epsilon": 2.0
    },

    # 7. Small differences below epsilon (should merge all)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 1.05], [3, 1.0], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 8. Edge case: first and last piece extreme values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -100], [1, 0], [2, 100], [3, float('inf')]],
        "epsilon": 50
    },

    # 9. Single sharp jump, testing optimal merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 10], [3, 10], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 10. Function oscillating near epsilon boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.49], [2, 0.51], [3, 1.0], [4, float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration17
test_cases17 = [
    # Test Case 1: Simple increasing sequence, should merge some pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,4],[4,float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 2: Plateau with exact epsilon match, should merge plateau pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5.5],[2,6],[3,6.5],[4,float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 3: Alternating high and low, cannot merge due to epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,4],[2,1],[3,4],[4,float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 4: Single-piece large jump, should keep separate
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,10],[2,2],[3,2],[4,float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 5: All identical values, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,3],[1,3],[2,3],[3,3],[4,float('inf')]],
        "epsilon": 0.1
    },
    # Test Case 6: Small epsilon, each piece distinct, no merges possible
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,4],[4,float('inf')]],
        "epsilon": 0.01
    },
    # Test Case 7: Sharp spike in middle, should isolate spike
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1],[2,10],[3,1],[4,1],[5,float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 8: Gradual slope, should merge several pieces under large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,4],[5,float('inf')]],
        "epsilon": 2.0
    },
    # Test Case 9: Negative values with variation, test algorithm handles negatives
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,-2],[1,-1],[2,0],[3,1],[4,2],[5,float('inf')]],
        "epsilon": 1.5
    },
    # Test Case 10: Edge case with only two real pieces, check boundaries
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[2,6],[3,float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration18
test_cases18 = [
    # 1. Simple monotone increasing values
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,float('inf')]],
        "epsilon": 0.5
    },
    # 2. Simple monotone decreasing values
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,4],[2,3],[3,float('inf')]],
        "epsilon": 0.5
    },
    # 3. Plateau in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,2],[3,float('inf')]],
        "epsilon": 0.0
    },
    # 4. Sharp spike (tests handling of outlier)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,10],[2,1],[3,float('inf')]],
        "epsilon": 2.0
    },
    # 5. Alternating up and down (zig-zag)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,0],[3,2],[4,float('inf')]],
        "epsilon": 1.0
    },
    # 6. Flat values within epsilon tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5.2],[2,4.8],[3,5],[4,float('inf')]],
        "epsilon": 0.5
    },
    # 7. Single large jump at the end
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1],[2,1],[3,10],[4,float('inf')]],
        "epsilon": 0.5
    },
    # 8. Gradually increasing then flat
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,3],[4,3],[5,float('inf')]],
        "epsilon": 0.25
    },
    # 9. Noise around a constant value
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,10],[1,10.3],[2,9.8],[3,10.1],[4,10],[5,float('inf')]],
        "epsilon": 0.5
    },
    # 10. Non-uniform x intervals
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[0.5,2.5],[2,3],[5,7],[6,float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration19
test_cases19 = [
    # 1. Simple increasing sequence
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.5
    },
    # 2. Simple decreasing sequence
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4], [2, 3], [3, float('inf')]],
        "epsilon": 0.5
    },
    # 3. Flat plateau
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.1
    },
    # 4. Single spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, float('inf')]],
        "epsilon": 2
    },
    # 5. Alternating high-low
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 1], [3, 4], [4, float('inf')]],
        "epsilon": 1.5
    },
    # 6. Tiny variations
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 1.9], [3, 2], [4, float('inf')]],
        "epsilon": 0.15
    },
    # 7. Piecewise with overlapping values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.5
    },
    # 8. Negative values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -2], [1, -3], [2, -1], [3, float('inf')]],
        "epsilon": 1
    },
    # 9. Edge case with immediate jump at start
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [0.1, 2], [1, 2], [2, float('inf')]],
        "epsilon": 3
    },
    # 10. Large epsilon merging everything
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 10
    }
]

#Iteration20
test_cases20 = [
    # 1. Simple increasing sequence
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 2],[2, 3],[3,float('inf')]],
        "epsilon": 0.5
    },
    # 2. Constant function (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 5],[2, 5],[3,5],[4,float('inf')]],
        "epsilon": 0.1
    },
    # 3. Single sharp spike (tests algorithm's split)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 10],[2, 1],[3,float('inf')]],
        "epsilon": 2
    },
    # 4. Small oscillations around a plateau
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 3],[1, 3.2],[2, 2.8],[3, 3],[4,float('inf')]],
        "epsilon": 0.25
    },
    # 5. Large flat then sudden jump
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 0],[1, 0],[2, 10],[3, 10],[4,float('inf')]],
        "epsilon": 0.5
    },
    # 6. Decreasing then small spike (to test epsilon handling)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 4],[2, 4.9],[3, 3],[4,float('inf')]],
        "epsilon": 0.4
    },
    # 7. Tiny segments (should test minimal merging)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[0.1, 1.1],[0.2, 1.05],[0.3, 1],[1,float('inf')]],
        "epsilon": 0.1
    },
    # 8. Alternating highs and lows (stress test)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 4],[2, 1],[3, 4],[4, 1],[5,float('inf')]],
        "epsilon": 1
    },
    # 9. Plateau with one outlier (tests ignoring small spike)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 2],[1, 2.1],[2, 2],[3, 10],[4, 2],[5,float('inf')]],
        "epsilon": 0.2
    },
    # 10. Already optimal segments (should stay the same)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 3],[2, 7],[3, 5],[4,float('inf')]],
        "epsilon": 0.75
    }
]

#Iteration21
test_cases21 = [
    # 1. Simple increasing sequence, epsilon allows merging some pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,4],[4,float('inf')]],
        "epsilon": 1.0
    },

    # 2. Flat sequence, epsilon small, should merge all into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,5],[4,float('inf')]],
        "epsilon": 0.1
    },

    # 3. Alternating up and down (oscillatory), epsilon too small to merge
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,1],[3,3],[4,1],[5,float('inf')]],
        "epsilon": 0.5
    },

    # 4. Single sharp jump in middle
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,10],[3,10],[4,float('inf')]],
        "epsilon": 1.0
    },

    # 5. Decreasing then increasing (V-shape)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,3],[2,1],[3,3],[4,5],[5,float('inf')]],
        "epsilon": 1.0
    },

    # 6. Very small epsilon, no merging possible
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,4],[4,5],[5,float('inf')]],
        "epsilon": 0.01
    },

    # 7. All equal values, large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,7],[1,7],[2,7],[3,7],[4,float('inf')]],
        "epsilon": 5.0
    },

    # 8. Single non-boundary point, edge case with 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,10],[1,float('inf')]],
        "epsilon": 2.0
    },

    # 9. Non-uniform x-spacing, test algorithm handles irregular intervals
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[0.5,1.5],[2,2],[5,2.5],[10,float('inf')]],
        "epsilon": 0.5
    },

    # 10. Combination of flat, increasing, decreasing, large jump
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,3],[3,1],[4,1],[5,10],[6,float('inf')]],
        "epsilon": 1.0
    }
]

#Iteration22
test_cases22 = [
    # Test Case 1: Simple increasing sequence
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 2: Plateaus (all equal values)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0
    },

    # Test Case 3: Sudden large jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 10], [4, float('inf')]],
        "epsilon": 1
    },

    # Test Case 4: Alternating high/low values
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, 5], [4, float('inf')]],
        "epsilon": 2
    },

    # Test Case 5: Small oscillations within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.2], [2, 0.8], [3, 1.1], [4, float('inf')]],
        "epsilon": 0.25
    },

    # Test Case 6: Single long plateau
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [1, 7], [2, 7], [3, 7], [4, float('inf')]],
        "epsilon": 0.5
    },

    # Test Case 7: Decreasing sequence with large jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 8], [2, 5], [3, 2], [4, float('inf')]],
        "epsilon": 1
    },

    # Test Case 8: Only two real pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 6], [2, float('inf')]],
        "epsilon": 2
    },

    # Test Case 9: Pieces exactly at epsilon threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 4], [3, 5], [4, float('inf')]],
        "epsilon": 1
    },

    # Test Case 10: Mixed small and large jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 4], [3, 3.9], [4, 7], [5, float('inf')]],
        "epsilon": 0.2
    }
]

#Iteration23
test_cases23 = [
    # 1. Simple increasing values, epsilon large enough to merge all
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,float('inf')]],
        "epsilon": 5.0
    },
    # 2. Simple decreasing values, small epsilon prevents merging
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,4],[2,3],[3,float('inf')]],
        "epsilon": 0.5
    },
    # 3. Constant function, should merge everything
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,2],[3,float('inf')]],
        "epsilon": 0.1
    },
    # 4. Alternating values, epsilon just enough to merge some pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,1],[3,2],[4,float('inf')]],
        "epsilon": 0.6
    },
    # 5. Sharp spike, epsilon smaller than spike amplitude
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,10],[2,1],[3,float('inf')]],
        "epsilon": 2.0
    },
    # 6. Sharp spike, epsilon large enough to ignore spike
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,10],[2,1],[3,float('inf')]],
        "epsilon": 10.0
    },
    # 7. Small oscillations, testing boundary merging
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.1],[2,0.9],[3,1.05],[4,float('inf')]],
        "epsilon": 0.2
    },
    # 8. Single piece (trivial case)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,float('inf')]],
        "epsilon": 0.1
    },
    # 9. Multiple equal spikes, checking correct piece selection
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,5],[2,2],[3,5],[4,2],[5,float('inf')]],
        "epsilon": 2.0
    },
    # 10. Random varying function, small epsilon forces minimal merges
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,2],[3,4],[4,3],[5,float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration24
test_cases24 = [
    # 1. Simple increasing function, no approximation possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Flat function, should approximate with 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Single large jump, epsilon too small to merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, float('inf')]],
        "epsilon": 2
    },

    # 4. Values oscillate around epsilon, testing minimal piece selection
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 5. Negative values, plateau in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -2], [1, -2], [2, -2], [3, 0], [4, float('inf')]],
        "epsilon": 1
    },

    # 6. Sharp drop then plateau, epsilon allows some merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [2, 0], [3, 5], [4, float('inf')]],
        "epsilon": 2.5
    },

    # 7. Single-piece function (trivial case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [1, float('inf')]],
        "epsilon": 1
    },

    # 8. Increasing then decreasing, challenging optimality
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 6], [3, 3], [4, 1], [5, float('inf')]],
        "epsilon": 1
    },

    # 9. Two identical adjacent pieces, epsilon allows merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [1, 4], [2, 5], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 10. Complex oscillation with boundary effects
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 4], [2, 2], [3, 5], [4, 3], [5, 6], [6, float('inf')]],
        "epsilon": 1.5
    }
]

#Iteration25
test_cases25 = [
    # 1. Constant function, should return 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,5],[4,float('inf')]],
        "epsilon": 0.1
    },
    # 2. Single jump, epsilon allows merging two pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2.4],[2,2.1],[3,float('inf')]],
        "epsilon": 0.5
    },
    # 3. Increasing linear trend, epsilon small (cannot merge)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,2],[2,3],[3,4],[4,float('inf')]],
        "epsilon": 0.2
    },
    # 4. Increasing then decreasing, epsilon allows partial merge
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,3],[2,2],[3,1],[4,float('inf')]],
        "epsilon": 1
    },
    # 5. Alternating high-low values, epsilon too small (no merge possible)
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,5],[2,1],[3,5],[4,float('inf')]],
        "epsilon": 0.5
    },
    # 6. Plateau at start, sharp drop, test boundary merging
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,0],[3,0],[4,float('inf')]],
        "epsilon": 0.1
    },
    # 7. Gradual slope within epsilon, should merge all into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,0.2],[2,0.4],[3,0.3],[4,float('inf')]],
        "epsilon": 0.5
    },
    # 8. Two separate clusters, epsilon cannot merge, should keep 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1.1],[2,5],[3,5.1],[4,float('inf')]],
        "epsilon": 0.05
    },
    # 9. Single extreme outlier, epsilon large enough to absorb
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,50],[3,2],[4,float('inf')]],
        "epsilon": 48
    },
    # 10. Multiple peaks and valleys, epsilon moderate
    {
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,4],[2,2],[3,5],[4,3],[5,float('inf')]],
        "epsilon": 1.5
    }
]

#Iteration26
test_cases26 = [
    # 1. Simple increasing function, small epsilon, expect no merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Flat function, large epsilon, expect all pieces merged into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Alternating high-low values, epsilon too small to merge anything
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Function with one outlier, epsilon allows merging everything except the outlier
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 50], [4, float('inf')]],
        "epsilon": 1.0
    },

    # 5. Single piece (trivial case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, float('inf')]],
        "epsilon": 0.5
    },

    # 6. Two pieces within epsilon, should merge into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.2], [2, float('inf')]],
        "epsilon": 0.25
    },

    # 7. Pieces exactly on epsilon threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 8. Non-monotone function, overlapping peaks
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 2], [3, 4], [4, 3], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 9. Decreasing function, small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 8], [2, 6], [3, 4], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 10. Constant except boundary jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, 7], [4, 7], [5, float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration27
test_cases27 = [
    # 1. Simple linear increase, small epsilon (no merging possible)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.1
    },
    # 2. Flat pieces within epsilon (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 1.95], [3, float('inf')]],
        "epsilon": 0.2
    },
    # 3. Single peak exceeding epsilon (cannot merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 5], [2, 2], [3, float('inf')]],
        "epsilon": 1
    },
    # 4. Sudden jump at end (tests last piece handling)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 10], [3, float('inf')]],
        "epsilon": 0.5
    },
    # 5. Negative values, mergeable plateau
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -3], [1, -3.1], [2, -2.9], [3, float('inf')]],
        "epsilon": 0.2
    },
    # 6. Large numbers with small epsilon (no merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1000], [1, 1001], [2, 999], [3, float('inf')]],
        "epsilon": 0.5
    },
    # 7. Single long piece with boundary infinity (should remain 1)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 4], [10, 4], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },
    # 8. Alternating high-low values, epsilon allows partial merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 3], [2, 2], [3, 4], [4, float('inf')]],
        "epsilon": 1
    },
    # 9. Piece exactly at epsilon limit (tests rounding/tolerance)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1], [3, float('inf')]],
        "epsilon": 0.5
    },
    # 10. Multiple plateaus separated by large jumps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 10], [3, 10], [4, 2], [5, 2], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },
]

#Iteration28
test_cases28 = [
    # 1. Simple increasing sequence, small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Flat sequence, epsilon > 0, can merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Alternating peaks and valleys, epsilon small
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, float('inf')]],
        "epsilon": 0.1
    },

    # 4. Alternating peaks and valleys, epsilon large
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, float('inf')]],
        "epsilon": 2.0
    },

    # 5. Single peak, epsilon allows merging neighbors
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 5], [2, 1], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Strictly decreasing function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 8], [2, 6], [3, 4], [4, 2], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 7. Step function with exactly epsilon difference
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1.0], [3, 1.5], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Two large flat segments separated by one small spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 10], [3, 3], [4, 3], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Single point spike at boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 5.0
    },

    # 10. Very large flat region with tiny variations
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 100], [1, 100.1], [2, 99.9], [3, 100], [4, 100.05], [5, float('inf')]],
        "epsilon": 0.2
    }
]

#Iteration29
test_cases29 = [
    # 1. Simple increasing sequence, small epsilon (no merging)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, float('inf')]],
        "epsilon": 0.1
    },
    # 2. Flat sequence, large epsilon (all merged into 1)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 1.0
    },
    # 3. Alternating high-low sequence (forces no merging)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 10], [4, float('inf')]],
        "epsilon": 0.5
    },
    # 4. Edge case: exactly epsilon apart (merge possible at boundary)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1.0], [3, float('inf')]],
        "epsilon": 0.5
    },
    # 5. Single piece (trivial case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 1.0
    },
    # 6. Large jump in middle (forces separate pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 10], [4, float('inf')]],
        "epsilon": 2.0
    },
    # 7. Small oscillations within epsilon (should merge all)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 1.9], [3, 2], [4, float('inf')]],
        "epsilon": 0.2
    },
    # 8. Decreasing sequence, exact epsilon at the last piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4.6], [2, 4.2], [3, 3.8], [4, float('inf')]],
        "epsilon": 0.5
    },
    # 9. Non-uniform spacing of x-values, checks interval handling
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.5, 2], [2, 2], [3, 3], [5, float('inf')]],
        "epsilon": 0.7
    },
    # 10. Multiple small peaks, tests algorithm's optimality for merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.5], [2, 1], [3, 1.2], [4, 1], [5, float('inf')]],
        "epsilon": 0.3
    }
]

#Iteration30
test_cases30 = [
    # Test Case 1: Simple increasing sequence, epsilon allows merging all
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 2],[2, 3],[3, float('inf')]],
        "epsilon": 2.0
    },
    # Test Case 2: Flat sequence, epsilon zero, should not merge
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 5],[2, 5],[3, float('inf')]],
        "epsilon": 0.0
    },
    # Test Case 3: Single big jump, epsilon smaller than jump
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 10],[2, 1],[3, float('inf')]],
        "epsilon": 5.0
    },
    # Test Case 4: Alternating high-low pattern, tests greedy failure if not optimal
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 3],[2, 1],[3, 3],[4, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 5: Two identical consecutive segments, epsilon allows merge
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 2],[1, 2],[2, 4],[3, 4],[4, float('inf')]],
        "epsilon": 0.5
    },
    # Test Case 6: Increasing then decreasing, epsilon just enough to merge middle
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 3],[2, 2],[3, float('inf')]],
        "epsilon": 1.0
    },
    # Test Case 7: Single constant segment, large epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 7],[1, 7],[2, 7],[3, float('inf')]],
        "epsilon": 10.0
    },
    # Test Case 8: Oscillating small values, epsilon smaller than oscillation
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 0],[2, 1],[3, 0],[4, float('inf')]],
        "epsilon": 0.4
    },
    # Test Case 9: Extreme values, large jump at end
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 2],[2, 3],[3, 100],[4, float('inf')]],
        "epsilon": 50
    },
    # Test Case 10: Overlapping segments with same value, epsilon zero
    {
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 5],[2, 5],[3, 5],[4, float('inf')]],
        "epsilon": 0
    }
]

