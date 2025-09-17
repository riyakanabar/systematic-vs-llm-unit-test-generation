#12 Sept 2025
#Iteration1 3:40PM
test_cases1 = [
    # 1. Constant function (should collapse to 1 piece if epsilon ≥ 0)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Single jump larger than epsilon (must keep both pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 10], [10, float('inf')]],
        "epsilon": 2.0
    },

    # 3. Single jump within epsilon (can merge into one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 0.5], [10, float('inf')]],
        "epsilon": 1.0
    },

    # 4. Alternating high/low pattern (forces multiple pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 3.0
    },

    # 5. Increasing staircase with small steps (mergeable if ε large)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 1], [4, 2], [6, 3], [8, 4], [10, float('inf')]],
        "epsilon": 2.5
    },

    # 6. Increasing staircase with small steps (not mergeable if ε small)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 1], [4, 2], [6, 3], [8, 4], [10, float('inf')]],
        "epsilon": 0.4
    },

    # 7. Large plateau, then sudden jump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [50, 5], [51, 20], [100, float('inf')]],
        "epsilon": 3.0
    },

    # 8. Very narrow interval (degenerate sensitivity test)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1e-9, 100], [1, 0], [2, float('inf')]],
        "epsilon": 10.0
    },

    # 9. Multiple small oscillations within epsilon (can compress)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.1], [2, 4.9], [3, 5.2], [4, 4.8], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 10. Multiple small oscillations exceeding epsilon (cannot compress)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 7], [2, 3], [3, 8], [4, 2], [5, float('inf')]],
        "epsilon": 1.0
    }
]
#Iteration2 3:41PM
test_cases2 = [
    # 1. Constant function (should collapse to 1 piece for any ε)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },

    # 2. Single jump larger than ε (should require 2 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 10], [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 3. Multiple small jumps below ε (should merge to 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 1.2], [4, 1.1], [6, 1.05], [8, 1.15], [float('inf'), float('inf')]],
        "epsilon": 0.3
    },

    # 4. Alternating high/low values with large jumps (should not merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 5. Monotone increasing (ε small forces many cuts, large ε merges all)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 2], [4, 4], [6, 6], [8, 8], [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 6. Plateau + sharp jump (tests selective merging)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [3, 5], [6, 5], [9, 15], [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 7. Very tight tolerance (forces exact matching, no merging)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 8. Noise-like fluctuations just under ε (should merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.1], [2, 9.95], [3, 10.05], [4, 9.9], [5, 10], [float('inf'), float('inf')]],
        "epsilon": 0.2
    },

    # 9. Noise-like fluctuations just above ε (should not merge all)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.3], [2, 9.6], [3, 10.4], [4, 9.5], [5, 10], [float('inf'), float('inf')]],
        "epsilon": 0.2
    },

    # 10. Long flat region + tiny bump (tests minimal split)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [5, 7], [6, 7.5], [7, 7], [10, 7], [float('inf'), float('inf')]],
        "epsilon": 0.4
    }
]
#Iteration3 3:42PM
test_cases3 = [
    # 1. Single constant function (should need only 1 piece regardless of epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Step function with jump larger than epsilon (should keep 2 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 10], [10, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Step function with jump smaller than epsilon (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 0.5], [10, float('inf')]],
        "epsilon": 1.0
    },

    # 4. Alternating small steps (checkerboard), epsilon too small (must keep all pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 0.4
    },

    # 5. Alternating small steps, epsilon large enough (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Redundant breakpoints (multiple consecutive same values, algorithm should compress)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.01
    },

    # 7. Large jump, but very high epsilon (should collapse into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -100], [1, 100], [2, float('inf')]],
        "epsilon": 500
    },

    # 8. Noise around a constant level, epsilon just enough to smooth (should reduce pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.2], [2, 9.9], [3, 10.1], [4, 10], [5, float('inf')]],
        "epsilon": 0.3
    },

    # 9. Noise too large for given epsilon (must keep several pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 12], [2, 8], [3, 11], [4, 9], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 10. Degenerate case: boundaries at infinity only (empty function body, should return 0 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')]],
        "epsilon": 0.1
    }
]
#Iteration4
test_cases4 = [
    # 1. Constant function (should always collapse to 1 piece if ε >= 0)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 2. Single large jump (ε too small to merge, must use 2 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [5, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 3. Single large jump but ε large enough to merge into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [5, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 10.0
    },

    # 4. Alternating small oscillations (can be merged if ε is larger than oscillation amplitude)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [1, 1],
                  [2, 0],
                  [3, 1],
                  [4, 0],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 5. Alternating oscillations with ε too small (must keep all pieces separate)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [1, 1],
                  [2, 0],
                  [3, 1],
                  [4, 0],
                  [float('inf'), float('inf')]],
        "epsilon": 0.1
    },

    # 6. Multiple flat segments with same value (redundant splits → should merge to 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 3],
                  [1, 3],
                  [2, 3],
                  [3, 3],
                  [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 7. Large jump at the boundary (check handling of -inf and +inf)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [-1000, -5],
                  [0, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 9.0
    },

    # 8. Increasing staircase (ε large enough to merge into fewer steps)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [1, 1],
                  [2, 2],
                  [3, 3],
                  [4, 4],
                  [float('inf'), float('inf')]],
        "epsilon": 2.5
    },

    # 9. Increasing staircase (ε too small → must keep all steps)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [1, 1],
                  [2, 2],
                  [3, 3],
                  [4, 4],
                  [float('inf'), float('inf')]],
        "epsilon": 0.4
    },

    # 10. Non-monotonic with plateaus and jumps (complex merge test)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [2, 0],
                  [3, 5],
                  [5, 5],
                  [6, -2],
                  [8, -2],
                  [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 3.0
    }
]
#Iteration5
test_cases5 = [
    # 1. Constant function, should compress to 1 piece regardless of epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 0.1
    },

    # 2. Single jump function, epsilon smaller than jump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [5, 10],
                  [10, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 3. Single jump, epsilon large enough to merge pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [5, 10],
                  [10, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 10.0
    },

    # 4. Alternating small oscillations just within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [1, 6],
                  [2, 4.5],
                  [3, 5.5],
                  [4, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 5. Alternating oscillations just outside epsilon (forces more pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [1, 8],
                  [2, 2],
                  [3, 7],
                  [4, 3],
                  [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 6. Plateau + sharp peak smaller than epsilon → should flatten
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [2, 5.5],
                  [3, 5],
                  [6, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 7. Plateau + sharp peak larger than epsilon → peak must remain separate
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [2, 8],
                  [3, 5],
                  [6, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 8. Multiple identical consecutive values (should merge to 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 3],
                  [1, 3],
                  [2, 3],
                  [3, 3],
                  [float('inf'), float('inf')]],
        "epsilon": 0.01
    },

    # 9. Extreme boundary values at ±∞, checking stability
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [-1000, 1],
                  [0, 100],
                  [1000, 1],
                  [float('inf'), float('inf')]],
        "epsilon": 99.0
    },

    # 10. Tolerance exactly equal to half the jump (tight edge case)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [1, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 5.0
    },
]
#Iteration6
test_cases6 = [
    # 1. Constant function (should collapse to 1 piece for any ε ≥ 0)
    (
        [[-float('inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        0.0,
        "Constant function, zero tolerance — only 1 piece needed."
    ),

    # 2. Two identical adjacent values (redundant step)
    (
        [[-float('inf'), float('inf')], [0, 3], [5, 3], [10, 7], [float('inf'), float('inf')]],
        0.0,
        "Redundant step: first two pieces identical, should merge."
    ),

    # 3. Small jump smaller than epsilon (tolerance should absorb jump)
    (
        [[-float('inf'), float('inf')], [0, 1], [5, 1.1], [10, 1], [float('inf'), float('inf')]],
        0.2,
        "Small fluctuation absorbed by ε, should reduce to 1 piece."
    ),

    # 4. Alternating values with ε too small to merge
    (
        [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [float('inf'), float('inf')]],
        1.0,
        "Oscillating large jumps, ε too small — must keep all pieces."
    ),

    # 5. Alternating values with large ε (merging possible)
    (
        [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [float('inf'), float('inf')]],
        10.0,
        "Oscillating jumps, large ε allows flattening to 1 piece."
    ),

    # 6. Plateau with a single spike within ε
    (
        [[-float('inf'), float('inf')], [0, 5], [5, 7], [6, 5], [10, 5], [float('inf'), float('inf')]],
        3.0,
        "Single spike inside plateau, within ε, should merge into 1 piece."
    ),

    # 7. Plateau with a spike outside ε
    (
        [[-float('inf'), float('inf')], [0, 5], [5, 20], [6, 5], [10, 5], [float('inf'), float('inf')]],
        3.0,
        "Spike larger than ε, cannot merge, must keep 3 pieces."
    ),

    # 8. Long increasing staircase
    (
        [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [float('inf'), float('inf')]],
        0.4,
        "Staircase with small steps, ε too small — each step must stay."
    ),

    # 9. Long increasing staircase with larger ε
    (
        [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [float('inf'), float('inf')]],
        2.5,
        "Staircase with larger ε, multiple steps can merge into fewer pieces."
    ),

    # 10. Edge case with infinite domains at ends
    (
        [[-float('inf'), float('inf')], [-5, -1], [0, 0], [5, 1], [10, 2], [float('inf'), float('inf')]],
        1.0,
        "Piecewise defined on unbounded domain, checks handling of -inf/+inf."
    ),
]
#Iteration7
test_cases7 = [

    # 1. Constant function (should collapse to 1 piece for any ε ≥ 0)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [10, 5], [20, 5], [30, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Single jump exactly at tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [10, 1], [20, float('inf')]],
        "epsilon": 1.0
    },

    # 3. Alternating high/low values (forces many pieces if ε small)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 2.0
    },

    # 4. Increasing staircase, small increments (can merge under larger ε)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 1], [4, 2], [6, 3], [8, 4], [10, float('inf')]],
        "epsilon": 1.5
    },

    # 5. Large flat region, then small noisy fluctuations (test noise smoothing)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [10, 5.1], [20, 4.9], [30, 5.2], [40, 5.0], [50, float('inf')]],
        "epsilon": 0.3
    },

    # 6. Values differ by exactly ε (borderline merge vs. split)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [10, 2], [20, 4], [30, 6], [40, float('inf')]],
        "epsilon": 2.0
    },

    # 7. Short spike much higher than neighbors (forces isolated piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 0], [6, 100], [7, 0], [10, 0], [15, float('inf')]],
        "epsilon": 5.0
    },

    # 8. Two distant flat regions with small local variations
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [5, 10.5], [10, 9.8], [20, 10], [30, 20], [40, 19.5], [50, 20.2], [60, float('inf')]],
        "epsilon": 1.0
    },

    # 9. Empty interior (just boundaries with no segments)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, float('inf')]],
        "epsilon": 0.0
    },

    # 10. Very small ε (forces exact segmentation, no merging)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [2, 2], [4, 3], [6, 2], [8, 1], [10, float('inf')]],
        "epsilon": 0.0001
    },
]
#Iteration8
test_cases8 = [
    # 1. Single piece, exact fit (ε = 0 should still work)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 2. Two adjacent pieces with the same value (should collapse into one piece if ε >= 0)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [5, 3], [10, 3], [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 3. Two pieces differing slightly, ε large enough to merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [5, 2.1], [10, 2], [float('inf'), float('inf')]],
        "epsilon": 0.2
    },

    # 4. Oscillating values, ε too small to merge → must keep all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, -1], [2, 1], [3, -1], [4, 1], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },

    # 5. Oscillating values, ε large enough to flatten everything into one
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, -1], [2, 1], [3, -1], [4, 1], [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 6. Large constant region with a single spike (check if spike forces extra piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 0], [6, 10], [7, 0], [10, 0], [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 7. Same as above but tolerance high enough to absorb spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 0], [6, 10], [7, 0], [10, 0], [float('inf'), float('inf')]],
        "epsilon": 10.0
    },

    # 8. Strict monotone increasing staircase, ε = 0 (must keep all pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 9. Same staircase, but ε = 0.6 (allows merging close steps)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [float('inf'), float('inf')]],
        "epsilon": 0.6
    },

    # 10. Constant everywhere except jump at ±∞ boundaries (should ignore since boundaries don’t matter)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 7], [100, 7], [float('inf'), float('inf')]],
        "epsilon": 0.0
    }
]
#Iteration9
test_cases9 = [
    # 1. Trivial constant function
    {
        "name": "Constant function, zero tolerance",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 2. Step function within tolerance (mergeable)
    {
        "name": "Small jumps within epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [2, 1.1], [4, 0.9], [6, 1],
                  [float('inf'), float('inf')]],
        "epsilon": 0.2
    },

    # 3. Alternating high-low steps (no merging possible)
    {
        "name": "Alternating values",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 4. Single large jump, larger epsilon allows merging
    {
        "name": "One large jump",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 15.0
    },

    # 5. Flat regions with one outlier (tests robustness)
    {
        "name": "Flat with single spike",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [2, 5], [3, 20], [4, 5], [6, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 14.0
    },

    # 6. Many small oscillations just within epsilon
    {
        "name": "Oscillations within tolerance",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.1], [2, 0.9], [3, 1.05], [4, 0.95],
                  [float('inf'), float('inf')]],
        "epsilon": 0.2
    },

    # 7. Many small oscillations exceeding epsilon
    {
        "name": "Oscillations exceeding tolerance",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 2], [2, -2], [3, 2], [4, -2],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 8. Long flat regions with gradual drift
    {
        "name": "Gradual drift",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 1], [4, 2], [6, 3], [8, 4],
                  [float('inf'), float('inf')]],
        "epsilon": 2.5
    },

    # 9. Boundary-heavy test (infinite intervals matter)
    {
        "name": "Effect of boundaries",
        "pc_fx": [[-float('inf'), float('inf')],
                  [-100, -5], [0, -5], [100, -5],
                  [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 10. Large piece then tiny segment (should not force extra split if ε allows)
    {
        "name": "Tiny segment in middle",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [50, 0], [51, 100], [52, 0], [100, 0],
                  [float('inf'), float('inf')]],
        "epsilon": 120.0
    },
]
#Iteration10
test_cases10 = [
    # 1. Constant function, should collapse to 1 piece for any ε >= 0
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 2. Two-step function with exact jump larger than ε
    # Algorithm must keep both pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [5, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 4.9
    },

    # 3. Two-step function with jump smaller than ε
    # Can merge into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [5, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 10.0
    },

    # 4. Oscillating small variations within ε
    # Should merge into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [2, 6],
                  [4, 4],
                  [6, 5.5],
                  [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 5. Oscillating just beyond ε
    # Should require multiple pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [2, 3],
                  [4, -3],
                  [6, 4],
                  [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 6. Single sharp spike that is within ε
    # Should ignore spike and use 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [5, 50],
                  [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 50.0
    },

    # 7. Single sharp spike beyond ε
    # Must split around spike
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5],
                  [5, 50],
                  [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 20.0
    },

    # 8. Large flat region + tiny segment with small deviation
    # If ε covers the deviation, should merge into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10],
                  [9, 11],
                  [10, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 9. Increasing staircase with jumps smaller than ε
    # Should collapse to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [1, 2],
                  [2, 4],
                  [3, 6],
                  [4, 8],
                  [float('inf'), float('inf')]],
        "epsilon": 10.0
    },

    # 10. Increasing staircase with jumps larger than ε
    # Must keep all steps
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],
                  [1, 2],
                  [2, 4],
                  [3, 6],
                  [4, 8],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },
]

#Iteration11 4:22PM
# Each test case is a dict with keys: 'pc_fx' and 'epsilon'
test_cases11 = [

    # 1. Flat function, should return 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Single jump, epsilon allows merging, should return 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.1], [2, 1.2], [3, 5], [4, 5], [5, float('inf')]],
        "epsilon": 5
    },

    # 3. Single jump, epsilon small, must split at jump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1], [2, 10], [3, 10], [4, float('inf')]],
        "epsilon": 2
    },

    # 4. Oscillating function, tolerance smaller than peaks, many pieces needed
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 3], [2, -2], [3, 3], [4, -3], [5, 0], [6, float('inf')]],
        "epsilon": 1
    },

    # 5. Already optimal segments, epsilon exactly fits jumps
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 2], [2, 4], [3, 6], [4, float('inf')]],
        "epsilon": 2
    },

    # 6. Single-point spike, can be merged if epsilon large enough
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 50], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 50
    },

    # 7. Function decreasing, epsilon small, must maintain separate pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 9], [2, 8], [3, 7], [4, 6], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Function with small ripples under epsilon, should merge all
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.05], [2, 4.95], [3, 5.02], [4, 4.98], [5, float('inf')]],
        "epsilon": 0.1
    },

    # 9. Step function, epsilon smaller than step, must split at each step
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 10. Long flat region, single spike in the middle, epsilon allows ignoring spike
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 10], [2, 50], [3, 10], [4, 10], [5, float('inf')]],
        "epsilon": 45
    }
]

#Iteration12
test_cases12 = [
    # 1. Single constant function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 0.1
    },
    # 2. Two-piece function within tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [5, 1.05], [10, float('inf')]],
        "epsilon": 0.1
    },
    # 3. Two-piece function exceeding tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [5, 1.5], [10, float('inf')]],
        "epsilon": 0.2
    },
    # 4. Increasing linear steps
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.5
    },
    # 5. Plateau followed by a jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [3, 2], [4, 5], [6, float('inf')]],
        "epsilon": 0.5
    },
    # 6. Rapid oscillation around 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, -1], [2, 1], [3, -1], [4, float('inf')]],
        "epsilon": 1.0
    },
    # 7. Sparse x-values, same y
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [100, 3], [200, float('inf')]],
        "epsilon": 0.01
    },
    # 8. Negative values crossing zero
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -2], [2, 0], [4, 2], [6, float('inf')]],
        "epsilon": 1.0
    },
    # 9. Repeated y-values, uneven spacing
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.5, 1], [2, 1], [5, 1], [10, float('inf')]],
        "epsilon": 0.0
    },
    # 10. Edge values at boundaries
    {
        "pc_fx": [[-float('inf'), float('inf')], [-10, 0], [0, 1], [10, 0], [20, float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration13
test_cases13 = [
    # 1. Simple constant function, should require 1 piece only
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Linear increasing function, small epsilon, each point requires new piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Step function already piecewise constant, epsilon small enough to keep original pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 4. Step function with some flat regions, epsilon allows merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.05], [2, 1.1], [3, 2], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 5. Single spike, should create separate pieces around the spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 6. Oscillating function, epsilon large enough to allow some merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.2], [2, -0.1], [3, 0.1], [4, 0], [5, float('inf')]],
        "epsilon": 0.25
    },

    # 7. All points same value except last spike, epsilon smaller than spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 5], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Function with slowly drifting value, epsilon small so each step matters
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.1], [2, 1.2], [3, 1.3], [4, float('inf')]],
        "epsilon": 0.05
    },

    # 9. Function with boundary conditions that can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.05], [2, 0.05], [3, 0], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 10. Alternating high/low values with epsilon exactly at difference threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, float('inf')]],
        "epsilon": 1.0
    },
]

#Iteration14
# Test cases for piecewise constant approximation under L∞ norm
# Format: pc_fx = [[-inf, inf], [x1, y1], [x2, y2], ..., [xn, yn], [x_{n+1}, inf]], epsilon

test_cases14 = [
    # 1. Constant function, should result in a single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "description": "Constant function, minimal epsilon"
    },

    # 2. Strictly increasing function, epsilon small, should produce multiple pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [float('inf'), float('inf')]],
        "epsilon": 0.1,
        "description": "Strictly increasing, small epsilon"
    },

    # 3. Strictly increasing function, epsilon large, should merge into a single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [float('inf'), float('inf')]],
        "epsilon": 5,
        "description": "Strictly increasing, large epsilon allows single piece"
    },

    # 4. Function with single large jump, epsilon smaller than jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 10], [float('inf'), float('inf')]],
        "epsilon": 5,
        "description": "Single large jump, epsilon < jump, should split"
    },

    # 5. Function with small oscillations, epsilon just above oscillation amplitude
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 0.9], [3, 1], [float('inf'), float('inf')]],
        "epsilon": 0.2,
        "description": "Small oscillations, epsilon absorbs them"
    },

    # 6. Function with alternating peaks exactly at epsilon limit
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [float('inf'), float('inf')]],
        "epsilon": 2,
        "description": "Alternating peaks at epsilon, tests optimal merging"
    },

    # 7. Function with repeated values, epsilon zero, should preserve all pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [float('inf'), float('inf')]],
        "epsilon": 0,
        "description": "Repeated values, zero epsilon"
    },

    # 8. Function with one outlier far from rest
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 50], [3, 1], [4, 1], [float('inf'), float('inf')]],
        "epsilon": 10,
        "description": "One outlier, tests splitting around large deviation"
    },

    # 9. Increasing then flat then decreasing, epsilon small
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 2], [3, 1], [4, 0], [float('inf'), float('inf')]],
        "epsilon": 0.5,
        "description": "Increase-flat-decrease, small epsilon"
    },

    # 10. Very dense sampling, epsilon slightly smaller than max slope
    {
        "pc_fx": [[-float('inf'), float('inf')]] + [[i/10, i/10] for i in range(10)] + [[float('inf'), float('inf')]],
        "epsilon": 0.08,
        "description": "Dense points with epsilon slightly smaller than step size"
    },
]


#Iteration15
test_cases15 = [
    # 1. Single constant function (trivial optimal)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Two-piece function, exactly epsilon apart (tests tight tolerance)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Multiple small oscillations within epsilon (should merge into one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [1, 1.05], [2, 0.98], [3, 1.02], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 4. Sharp jump exceeding epsilon (must split)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 5. Flat regions separated by single point outside epsilon (tests splitting)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [1.5, 1], [2, 0], [3, float('inf')]],
        "epsilon": 0.4
    },

    # 6. Increasing linear slope (should split if slope > epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1.0], [3, 1.5], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 7. Decreasing slope with small noise (should not over-split)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 1.8], [2, 1.9], [3, 1.85], [4, float('inf')]],
        "epsilon": 0.3
    },

    # 8. Plateau at start, spike in middle, plateau again (tests spike detection)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 9. Multiple small alternating spikes just below epsilon (should merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 0.9], [3, 1.1], [4, 1], [5, float('inf')]],
        "epsilon": 0.25
    },

    # 10. Edge case: exact epsilon difference at piece boundaries (tests boundary correctness)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1.0], [3, 1.5], [4, float('inf')]],
        "epsilon": 0.5
    },
]

#Iteration16
test_cases16 = [
    # Single constant function
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]], "epsilon": 0.1},

    # Two-piece function with exact epsilon match
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, float('inf')]], "epsilon": 0.5},

    # Three-piece function with slight deviations
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.05], [2, 1.1], [3, float('inf')]], "epsilon": 0.1},

    # Piecewise function with large jump
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, float('inf')]], "epsilon": 0.5},

    # Multiple segments can merge under epsilon
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.05], [2, 1.08], [3, 1.1], [4, float('inf')]],
     "epsilon": 0.15},

    # Zero epsilon (must preserve all changes)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 3], [2, 2], [3, float('inf')]], "epsilon": 0.0},

    # Single small spike in otherwise constant function
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 5], [3, 1], [4, float('inf')]], "epsilon": 0.5},

    # Decreasing function with uniform slope, small epsilon
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 4.9], [2, 4.8], [3, 4.7], [4, float('inf')]],
     "epsilon": 0.05},

    # Increasing then plateau, large epsilon (should merge)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.2], [2, 0.4], [3, 0.4], [4, float('inf')]], "epsilon": 0.5},

    # Alternating high/low values, epsilon too small to merge
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 0], [3, 1], [4, float('inf')]], "epsilon": 0.3}
]

#Iteration17
test_cases17 = [
    # 1. Simple flat function, single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [10, 1], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },
    # 2. Single jump within tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1.05], [10, 1.1], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },
    # 3. Single jump exceeding tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 2], [10, 1], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },
    # 4. Increasing linear ramp, requires multiple pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.4], [2, 0.8], [3, 1.2], [4, 1.6], [5, 2.0], [float('inf'), float('inf')]],
        "epsilon": 0.3
    },
    # 5. Decreasing linear ramp
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 1.7], [2, 1.4], [3, 1.1], [4, 0.8], [5, 0.5], [float('inf'), float('inf')]],
        "epsilon": 0.25
    },
    # 6. Alternating high-low sequence
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, 2], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },
    # 7. Step function with large flat plateaus
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1], [10, 3], [15, 3], [20, 5], [float('inf'), float('inf')]],
        "epsilon": 0.2
    },
    # 8. Edge case: single point jump at start
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0.1, 10], [5, 10], [float('inf'), float('inf')]],
        "epsilon": 1
    },
    # 9. Edge case: last interval barely within tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 1.3], [3, 2.0], [float('inf'), float('inf')]],
        "epsilon": 0.3
    },
    # 10. Highly oscillating small-amplitude function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [0.5, 1.1], [1, 0.9], [1.5, 1.05], [2, 1], [2.5, 0.95], [3, 1], [float('inf'), float('inf')]],
        "epsilon": 0.15
    }
]

#Iteration18
test_cases18 = [
    # 1. Single constant function - trivial case
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Two-level function exactly at epsilon boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, float('inf')]],
        "epsilon": 0.5
    },

    # 3. Monotonically increasing function - should merge into fewer pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1.5
    },

    # 4. Function with spike in the middle - tests splitting around spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, 1], [4, float('inf')]],
        "epsilon": 2
    },

    # 5. Alternating high-low pattern - challenge for minimal pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 5
    },

    # 6. Flat plateau with a tiny deviation inside epsilon - should merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5.1], [2, 5], [3, 5], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 7. Piecewise function with very close values - stress L∞ comparison
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.001], [1, 1.002], [2, 1.003], [3, 1.004], [4, float('inf')]],
        "epsilon": 0.005
    },

    # 8. Edge spikes at boundaries - test handling of infinities
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 50], [2, 0], [3, 0], [4, 50], [5, float('inf')]],
        "epsilon": 10
    },

    # 9. Gradually increasing then decreasing - tricky for optimal merging
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 3], [3, 1], [4, 0], [5, float('inf')]],
        "epsilon": 1
    },

    # 10. Random small fluctuations inside epsilon - algorithm should merge all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.05], [2, 2.02], [3, 1.98], [4, 2.01],
                  [5, float('inf')]],
        "epsilon": 0.1
    }
]

#Iteration19
test_cases19 = [
    # 1. Constant function (should return 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },

    # 2. Single jump exactly at epsilon (boundary test)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [5, 1.5], [10, 1.5], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },

    # 3. Multiple small jumps below epsilon (should be approximated as one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.2], [2, 0.1], [3, 0.15], [4, 0.05], [float('inf'), float('inf')]],
        "epsilon": 0.3
    },

    # 4. Multiple jumps larger than epsilon (should split into multiple pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 1], [4, 0], [6, -1], [8, 0], [float('inf'), float('inf')]],
        "epsilon": 0.4
    },

    # 5. Two consecutive identical values (algorithm should not create unnecessary splits)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [3, 3], [6, 2], [9, 2], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },

    # 6. Noisy signal within epsilon (should merge all into one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.05], [2, 9.95], [3, 10.02], [4, 9.98], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },

    # 7. Signal with extreme values (tests handling of large numbers)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1e9], [5, 1e9+1], [10, 1e9-1], [float('inf'), float('inf')]],
        "epsilon": 2
    },

    # 8. Very small jumps (floating point precision test)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0001], [1, 0.00015], [2, 0.00012], [3, 0.00011], [float('inf'), float('inf')]],
        "epsilon": 0.0001
    },

    # 9. Single long piece with a single outlier (should split at outlier)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [3, 2], [4, 5], [5, 2], [6, 2], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },

    # 10. Alternating pattern around epsilon (tests greedy vs optimal)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.6], [2, -0.6], [3, 0.6], [4, -0.6], [5, 0], [float('inf'), float('inf')]],
        "epsilon": 0.5
    }
]

#Iteration20
test_cases20 = [
    # Test case 1: Single constant function, no approximation needed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 0.1
    },

    # Test case 2: Two-piece function exactly at epsilon boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, float('inf')]],
        "epsilon": 0.5
    },

    # Test case 3: Function with alternating spikes, requires splitting at each spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 5
    },

    # Test case 4: Flat plateau followed by a jump
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2], [3, 5], [4, float('inf')]],
        "epsilon": 1
    },

    # Test case 5: Small oscillations within epsilon, should merge into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.05], [2, 1.02], [3, 0.98], [4, float('inf')]],
        "epsilon": 0.1
    },

    # Test case 6: Large jump at boundary
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, float('inf')]],
        "epsilon": 10
    },

    # Test case 7: Monotone increasing function
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1
    },

    # Test case 8: Monotone decreasing function with step exceeding epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 7], [2, 3], [3, float('inf')]],
        "epsilon": 2
    },

    # Test case 9: Single spike in middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 10], [2, 1], [3, float('inf')]],
        "epsilon": 3
    },

    # Test case 10: Multiple small spikes that can be merged
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.2], [2, 0.9], [3, 1.1], [4, float('inf')]],
        "epsilon": 0.3
    }
]

#Iteration21 14Sept 3:10PM
test_cases21= [

    # 1. Single constant function
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [10, float('inf')]],
        "epsilon": 0.1,
        # Should need only 1 piece (already constant).
    },

    # 2. Step function with two distinct values
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 10], [10, float('inf')]],
        "epsilon": 1,
        # If epsilon < 5, must use 2 pieces. If epsilon >= 5, 1 piece suffices.
    },

    # 3. Alternating high/low (forces multiple pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 2,
        # Cannot merge highs and lows with small epsilon; tests greedy vs. optimal.
    },

    # 4. Monotone increasing staircase
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 2], [2, 4], [3, 6], [4, 8], [5, float('inf')]],
        "epsilon": 3,
        # With ε=3, some steps can merge, but not all. Tests grouping.
    },

    # 5. Flat segments with small jumps
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 0.5], [4, 1.0], [6, 1.5], [8, float('inf')]],
        "epsilon": 0.6,
        # With ε=0.6, multiple adjacent flats should be merged optimally.
    },

    # 6. Sharp outlier in middle
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 0], [6, 100], [7, 0], [10, float('inf')]],
        "epsilon": 10,
        # Outlier forces an extra piece; tests whether algorithm isolates spikes.
    },

    # 7. Very large interval with tiny perturbation
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1000, 5.01], [2000, 5], [3000, float('inf')]],
        "epsilon": 0.05,
        # Small perturbations should not create new pieces.
    },

    # 8. Symmetric structure (tests merge symmetry)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 5], [2, 0], [3, 5], [4, 0], [5, float('inf')]],
        "epsilon": 5,
        # Large epsilon may collapse everything to 1 piece.
    },

    # 9. Values just at tolerance boundary
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 2], [4, 4], [6, float('inf')]],
        "epsilon": 2,
        # Exactly at tolerance: algorithm must merge correctly without extra pieces.
    },

    # 10. Dense oscillations
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [0.1, 1], [0.2, 0], [0.3, 1], [0.4, 0], [0.5, 1], [0.6, float('inf')]],
        "epsilon": 0.4,
        # Stress test: many oscillations. Needs many pieces unless epsilon is high.
    }
]

#Iteration22
test_cases22 = [
    # 1. Trivial constant function (should collapse to 1 piece for any epsilon ≥ 0)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 5], [10, 5], [float("inf"), float("inf")]],
        "epsilon": 0.0
    },

    # 2. Single jump discontinuity (ε small forces 2 pieces, ε large allows 1 piece)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0], [5, 10], [10, 10], [float("inf"), float("inf")]],
        "epsilon": 4.9  # must keep 2 pieces
    },

    # 3. Same as case 2 but larger epsilon (can merge into 1 piece)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0], [5, 10], [10, 10], [float("inf"), float("inf")]],
        "epsilon": 10.0
    },

    # 4. Alternating high-frequency oscillation (tests minimal segmentation under tolerance)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [float("inf"), float("inf")]],
        "epsilon": 4.0  # algorithm should merge pairs into fewer pieces
    },

    # 5. Redundant breakpoints (piecewise constant but with extra identical values)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 7], [2, 7], [4, 7], [6, 7], [float("inf"), float("inf")]],
        "epsilon": 0.0  # should collapse all into 1 piece
    },

    # 6. Gradual staircase (tests tolerance-based merging)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [float("inf"), float("inf")]],
        "epsilon": 2.0  # optimal grouping into ~2-3 pieces
    },

    # 7. Extreme values (very large jump, tests scaling)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, -1e6], [5, 1e6], [float("inf"), float("inf")]],
        "epsilon": 5e5  # forces 2 pieces since tolerance too small
    },

    # 8. Boundary-only case (no interior points, should default to 0 pieces or 1 trivial piece)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [float("inf"), float("inf")]],
        "epsilon": 1.0
    },

    # 9. Small epsilon with tiny oscillations (forces exact preservation)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 0.1], [2, 0.0], [3, -0.1], [4, 0.0], [float("inf"), float("inf")]],
        "epsilon": 0.05  # must keep all oscillations as separate pieces
    },

    # 10. Plateau with a single spike (outlier test)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 5], [4, 5], [5, 100], [6, 5], [10, 5], [float("inf"), float("inf")]],
        "epsilon": 10.0  # spike cannot be absorbed; requires 3 pieces
    }
]

#Iteration23
test_cases23 = [
    # 1. Single constant function (trivial merge case)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.1  # No approximation needed, should stay as 1 piece
    },

    # 2. Two flat pieces separated by a small jump (mergeable if ε large enough)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [5, 5.1], [10, float('inf')]],
        "epsilon": 0.2  # Should merge into 1 piece since jump < ε
    },

    # 3. Two flat pieces with a large jump (cannot merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [5, 20], [10, float('inf')]],
        "epsilon": 5.0  # Must keep 2 pieces, since jump >> ε
    },

    # 4. Alternating up-down sequence (worst case for merging)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 2.0  # Cannot merge across swings, must keep many pieces
    },

    # 5. Large plateau with small noise
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 10.05], [2, 9.95], [3, 10.02], [4, 10], [5, float('inf')]],
        "epsilon": 0.1  # Should merge all into 1 piece despite noise
    },

    # 6. Multiple small steps within ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1.0], [3, 1.5], [4, 2.0], [5, float('inf')]],
        "epsilon": 2.0  # Entire function should collapse to 1 piece
    },

    # 7. Multiple steps just barely outside ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2.1], [3, 3.2], [4, float('inf')]],
        "epsilon": 1.0  # Some can merge, but not all, tests greedy vs optimal
    },

    # 8. Constant segments separated by very large gap
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -100], [1, 100], [2, -100], [3, 100], [4, float('inf')]],
        "epsilon": 50.0  # Must keep all alternating pieces, since gaps are huge
    },

    # 9. Long flat followed by short spike
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 0], [11, 100], [12, 0], [20, float('inf')]],
        "epsilon": 10.0  # Flat should collapse, spike must remain separate
    },

    # 10. Edge case with epsilon = 0 (exact representation required)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 3], [3, 4], [4, float('inf')]],
        "epsilon": 0.0  # Must preserve all 4 pieces, no merging allowed
    },
]

#Iteration24
# 10 test cases for piecewise constant approximation under L∞ norm

test_cases24 = [

    # 1. Single flat function (should collapse to 1 piece for any epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },

    # 2. Two identical adjacent pieces (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [5, 3], [10, 3], [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 3. Sharp jump (cannot merge across boundary unless epsilon is large enough)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 10], [10, 0], [float('inf'), float('inf')]],
        "epsilon": 5.0
    },

    # 4. Alternating high/low values (tests greedy merge failures)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 10], [4, 0], [6, 10], [8, 0], [10, 10], [float('inf'), float('inf')]],
        "epsilon": 5.0
    },

    # 5. Boundary case – discontinuity right at the start and end
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [1, 0], [9, 0], [10, 10], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },

    # 6. Large tolerance allows collapsing everything
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [2, 3], [4, -2], [6, 5], [8, -1], [10, 2], [float('inf'), float('inf')]],
        "epsilon": 10.0
    },

    # 7. Epsilon just small enough to prevent full merge (tests tight tolerance handling)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [5, 1], [10, 2], [float('inf'), float('inf')]],
        "epsilon": 0.9
    },

    # 8. Plateau in the middle (algorithm must detect optimal merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [3, 10], [7, 10], [10, 0], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },

    # 9. Multiple tiny oscillations (should merge aggressively if epsilon allows)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, -0.5], [3, 0.25], [4, -0.25], [5, 0], [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 10. Wide range, small epsilon (forces maximum number of pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -100], [2, -50], [4, 0], [6, 50], [8, 100], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },
]

#Iteration25
test_cases25 = [

    # 1. Constant function (should reduce to 1 piece if epsilon >= 0)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 2. Small jump within epsilon (should merge into 1 piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [5, 5.1], [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 0.2
    },

    # 3. Small jump exceeding epsilon (must keep 2 pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [5, 6], [10, 5],
                  [float('inf'), float('inf')]],
        "epsilon": 0.5
    },

    # 4. Alternating values exactly at ±epsilon (tests boundary condition)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 1], [2, 0], [3, 1],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },

    # 5. Large epsilon allows collapsing many oscillations into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -10], [1, 10], [2, -10], [3, 10], [4, -10],
                  [float('inf'), float('inf')]],
        "epsilon": 20.0
    },

    # 6. Very small epsilon forces each interval to be separate
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 0.01], [2, 0.02], [3, 0.03],
                  [float('inf'), float('inf')]],
        "epsilon": 0.001
    },

    # 7. Large plateau, then a sharp jump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [100, 1], [101, 10], [200, 10],
                  [float('inf'), float('inf')]],
        "epsilon": 0.5
    },

    # 8. Redundant representation (two identical adjacent segments)
    #    Tests if algorithm merges redundant intervals
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [5, 2], [10, 2],
                  [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 9. Narrow spikes that exceed tolerance (forces split even if short)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 100], [2, 0],
                  [float('inf'), float('inf')]],
        "epsilon": 50.0
    },

    # 10. Degenerate case: no finite intervals (should not crash)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [float('inf'), float('inf')]],
        "epsilon": 1.0
    },
    # # 10. Zero-width interval (tests robustness with adjacent breakpoints equal)
    # {
    #     "pc_fx": [[-float('inf'), float('inf')],
    #               [0, 5], [0, 10], [1, 10], [2, 5],
    #               [float('inf'), float('inf')]],
    #     "epsilon": 1.0
    # },
]

#Iteration26
test_cases26 = [

    # 1. Constant function (should collapse to one piece if ε ≥ 0)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [10, 5], [20, 5], [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 2. Single jump (requires exactly 2 pieces if ε < jump/2)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 10], [10, 10], [float('inf'), float('inf')]],
        "epsilon": 4.9
    },

    # 3. Alternating oscillation (forces many pieces if ε small)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, 10], [float('inf'), float('inf')]],
        "epsilon": 4.0
    },

    # 4. Large epsilon (should merge everything to one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 20], [10, -15], [15, 10], [float('inf'), float('inf')]],
        "epsilon": 100.0
    },

    # 5. Tiny epsilon (must preserve exact values)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 1], [4, 2], [6, 3], [float('inf'), float('inf')]],
        "epsilon": 0.0
    },

    # 6. Noise within epsilon (algorithm should optimally merge)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [2, 11], [4, 9], [6, 10], [float('inf'), float('inf')]],
        "epsilon": 2.0
    },

    # 7. Symmetric pattern around center
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [2, 5], [4, 10], [6, 5], [8, 0], [float('inf'), float('inf')]],
        "epsilon": 4.9
    },

    # 8. Sharp spike (ε too small must isolate spike)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [4, 0], [5, 100], [6, 0], [10, 0], [float('inf'), float('inf')]],
        "epsilon": 20.0
    },

    # 9. Long flat + tiny blip
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 50], [100, 50], [101, 55], [102, 50], [200, 50], [float('inf'), float('inf')]],
        "epsilon": 4.0
    },

    # 10. Multiple equal jumps (forces uniform segmentation)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [10, 10], [20, 20], [30, 30], [40, 40], [float('inf'), float('inf')]],
        "epsilon": 5.0
    }
]

#Iteration27
test_cases27 = [

    # 1. Trivial constant function, any epsilon should need only 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [10, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Two identical constant pieces (redundant segmentation)
    # Algorithm should merge into 1 piece if within epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [5, 5], [10, float('inf')]],
        "epsilon": 0.0
    },

    # 3. Sharp jump at middle, small epsilon forces 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 10], [10, float('inf')]],
        "epsilon": 1.0
    },

    # 4. Sharp jump but large epsilon allows approximation with 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 10], [10, float('inf')]],
        "epsilon": 20.0
    },

    # 5. Alternating up-down signal, small epsilon means many pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Alternating signal but large epsilon allows single approximation
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]],
        "epsilon": 15.0
    },

    # 7. Piecewise constant with a tiny outlier
    # Should test whether algorithm splits around outlier or merges
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.1], [2, 5], [3, float('inf')]],
        "epsilon": 0.2
    },

    # 8. Large domain with long flat regions + one jump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [100, 2], [101, 8], [200, 8], [201, float('inf')]],
        "epsilon": 0.5
    },

    # 9. Multiple small deviations within epsilon, should merge to one piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [1, 10.2], [2, 9.9], [3, 10.1], [4, 10], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 10. Extreme values with infinities in range
    # Algorithm should handle large jumps properly
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -1e6], [1, 1e6], [2, float('inf')]],
        "epsilon": 1e5
    }

]

#Iteration28
test_cases28 = [

    # 1. Constant function: should collapse to 1 piece for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [10, 5], [20, 5], [30, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Single jump: tight ε forces 2 pieces, loose ε allows 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [10, 10], [20, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Alternating values: cannot merge if ε small
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 0.1
    },

    # 4. Alternating values but large ε: all mergeable
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 10.0
    },

    # 5. Tiny oscillations within tolerance: should collapse to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.1], [2, 4.9], [3, 5.05], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 6. Same as (5) but ε too small: multiple pieces needed
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [1, 5.1], [2, 4.9], [3, 5.05], [4, float('inf')]],
        "epsilon": 0.01
    },

    # 7. Multiple identical adjacent segments: algorithm should merge
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 7], [5, 7], [10, 7], [15, 7], [20, float('inf')]],
        "epsilon": 0.0
    },

    # 8. Sparse large jump far away: algorithm shouldn’t merge across boundaries
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1000, 100], [2000, float('inf')]],
        "epsilon": 5.0
    },

    # 9. Staircase function: increasing stepwise
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 10. Staircase function but large ε: collapses to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 5.0
    }
]

#Iteration29
test_cases29 = [
    # 1. Single constant function: should return 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 0.1
    },

    # 2. Step function exactly at epsilon: should merge if tolerance allows
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.05], [2, float('inf')]],
        "epsilon": 0.1
    },

    # 3. Alternating small oscillations: should prevent merging due to L∞
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, -1], [2, 1], [3, -1], [4, float('inf')]],
        "epsilon": 0.5
    },

    # 4. Large spike in middle: may need separate piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 10], [2, 2], [3, float('inf')]],
        "epsilon": 1
    },

    # 5. Slowly increasing linear region: algorithm may incorrectly merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.5], [2, 1], [3, 1.5], [4, 2], [5, float('inf')]],
        "epsilon": 0.25
    },

    # 6. Flat region with single outlier: should split for optimal pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [2, 10], [3, 3], [4, 3], [5, float('inf')]],
        "epsilon": 0.5
    },

    # 7. Two plateaus separated by gap smaller than epsilon: may merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2.1], [2, 2], [3, 2.05], [4, float('inf')]],
        "epsilon": 0.2
    },

    # 8. Repeating pattern that could confuse greedy algorithm
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, 2], [4, 1], [5, float('inf')]],
        "epsilon": 0.4
    },

    # 9. Single outlier at start: tests boundary handling
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 100], [1, 1], [2, 1], [3, float('inf')]],
        "epsilon": 1
    },

    # 10. Piecewise with multiple small jumps: ensures algorithm respects L∞
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.2], [2, 0.4], [3, 0.6], [4, 0.8], [5, 1], [6, float('inf')]],
        "epsilon": 0.15
    }
]


#Iteration30
test_cases30 = [
    # 1. Perfectly flat function (no approximation needed)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [float('inf'), float('inf')]],
        "epsilon": 0.1
    },
    # 2. Single jump exceeding epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 10], [float('inf'), float('inf')]],
        "epsilon": 1
    },
    # 3. Two small jumps within epsilon (should merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.05], [2, 1.1], [3, 1.15], [float('inf'), float('inf')]],
        "epsilon": 0.2
    },
    # 4. Oscillating values around a flat line
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.1], [2, 0.9], [3, 1.05], [4, 1], [float('inf'), float('inf')]],
        "epsilon": 0.15
    },
    # 5. Spike at a single point
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 20], [2, 2], [3, 2], [float('inf'), float('inf')]],
        "epsilon": 5
    },
    # 6. Gradually increasing linear ramp (approximation may merge pieces)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [float('inf'), float('inf')]],
        "epsilon": 1.5
    },
    # 7. Function with one large jump and small variations around it
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.1], [2, 10], [3, 10.1], [4, 0.2], [float('inf'), float('inf')]],
        "epsilon": 0.5
    },
    # 8. Two distant identical flat regions (should stay separate)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, 3], [10, 3], [11, 3], [float('inf'), float('inf')]],
        "epsilon": 0.01
    },
    # 9. Small oscillations smaller than epsilon (should merge all into one piece)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1.02], [2, 0.98], [3, 1.01], [4, 0.99], [float('inf'), float('inf')]],
        "epsilon": 0.05
    },
    # 10. Multiple abrupt jumps exceeding epsilon (cannot merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 0], [3, 5], [4, 0], [float('inf'), float('inf')]],
        "epsilon": 1
    }
]
