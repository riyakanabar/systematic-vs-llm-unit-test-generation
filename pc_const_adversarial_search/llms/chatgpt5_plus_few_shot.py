#16 Sept 5:27PM
#Iteration1
test_cases1 = [
    # 1) All values lie within a band of width <= 2ε ⇒ optimally mergeable into one piece.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2.0], [1, 2.3], [2, 1.7], [5, 2.1], [6, 1.9],
                  [7, float('inf')]],
        "epsilon": 0.4
    },

    # 2) Range exactly equals 2ε ⇒ still mergeable (boundary condition).
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0],
                  [4, float('inf')]],
        "epsilon": 0.5
    },

    # 3) Range just exceeds 2ε by a hair ⇒ should force at least one split (float-sensitivity).
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0000002],
                  [2, float('inf')]],
        "epsilon": 0.5
    },

    # 4) Narrow “spike” way outside tolerance (width doesn’t matter under L∞).
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [0.001, 3.0], [0.002, 0.0],
                  [1.0, float('inf')]],
        "epsilon": 1.0
    },

    # 5) Monotone ramp with step size slightly > 2ε ⇒ multiple pieces are required.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 2.0], [2, 4.0], [3, 6.0],
                  [4, float('inf')]],
        "epsilon": 0.9
    },

    # 6) First block barely mergeable (range = 2ε), then a final value makes range > 2ε ⇒ split point detection.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5.0], [1, 5.9], [2, 6.1],   # range = 1.1 = 2ε (mergeable)
                  [3, 6.2],                       # pushes range to 1.2 > 2ε ⇒ split before here
                  [4, float('inf')]],
        "epsilon": 0.55
    },

    # 7) Alternating extremes around a center; 2ε just shy of spanning the gap ⇒ many splits.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -10.0], [1, 10.0], [2, -10.0], [3, 10.0],
                  [4, float('inf')]],
        "epsilon": 9.9  # 2ε = 19.8 < 20 ⇒ cannot merge -10 with +10
    },

    # 8) Duplicates with tiny numerical noise; should still merge (robustness to 1e-9 jitter).
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 3.0], [1, 3.0], [2, 3.0 + 1e-9],
                  [3, float('inf')]],
        "epsilon": 1e-6
    },

    # 9) Negative values with asymmetric drops; range > 2ε ⇒ multiple pieces needed.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -2.0], [2, -2.9], [3, -4.1],
                  [5, float('inf')]],
        "epsilon": 0.5  # range = 2.1 > 1.0
    },

    # 10) ε = 0 (exact matching): must keep every run of equal values (no approximation allowed).
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0], [2, 2.0], [3, 2.0], [4, 1.0],
                  [5, float('inf')]],
        "epsilon": 0
    },
]

#Iteration2
test_cases2 = [
    {
        "id": 1,
        "pc_fx": [[-float('inf'), float('inf')],[0,3],[5,3],[10,3],[12,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "Constant function; even with ε=0 it should be 1 piece."
    },
    {
        "id": 2,
        "pc_fx": [[-float('inf'), float('inf')],[0,2.0],[1,2.3],[3,2.1],[5,2.2],[6,float('inf')]],
        "epsilon": 0.2,
        "expected_min_pieces": 1,
        "note": "All values lie in a band of width 0.3 ≤ 2ε (=0.4) ⇒ collapses to 1."
    },
    {
        "id": 3,
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,1.4],[2,0.0],[3,1.4],[4,float('inf')]],
        "epsilon": 0.7,
        "expected_min_pieces": 1,
        "note": "Exact boundary case: max−min = 1.4 = 2ε. Should merge to 1 (inclusive inequality)."
    },
    {
        "id": 4,
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,1.401],[2,0.0],[3,1.401],[4,float('inf')]],
        "epsilon": 0.7,
        "expected_min_pieces": 4,
        "note": "Just over boundary: 1.401 > 2ε (=1.4). Alternating ⇒ no cross-merges; each stays separate."
    },
    {
        "id": 5,
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[2,0.6],[4,1.2],[6,1.8],[8,float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "note": "Monotone drift. Whole range 1.8 > 2ε (=1.0). Optimal partition: [0,0.6] and [1.2,1.8]."
    },
    {
        "id": 6,
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,10.0],[2,0.0],[3,float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 3,
        "note": "Narrow spike: |10−0| = 10 » 2ε (=2). Must isolate the spike ⇒ 3 pieces."
    },
    {
        "id": 7,
        "pc_fx": [[-float('inf'), float('inf')],[0.0,0.0],[1e-9,0.9],[1e-6,0.95],[1e-3,1.0],[1.0,float('inf')]],
        "epsilon": 0.55,
        "expected_min_pieces": 1,
        "note": "Tiny x-intervals (robustness). Value range 1.0 ≤ 2ε (=1.1) ⇒ 1 piece; tests FP stability."
    },
    {
        "id": 8,
        "pc_fx": [[-float('inf'), float('inf')],[0,-5.0],[2,-5.6],[4,-5.1],[6,float('inf')]],
        "epsilon": 0.3,
        "expected_min_pieces": 1,
        "note": "All negative and within band: range 0.6 ≤ 2ε (=0.6) at boundary ⇒ 1 piece."
    },
    {
        "id": 9,
        "pc_fx": [[-float('inf'), float('inf')],[0,2.0],[1,2.1],[2,2.2],[3,10.0],[4,float('inf')]],
        "epsilon": 0.2,
        "expected_min_pieces": 2,
        "note": "Late large jump. First three can merge (range 0.2 ≤ 0.4). Last must stand alone."
    },
    {
        "id": 10,
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,0.2],[2,0.8],[3,0.2],[4,0.0],[5,float('inf')]],
        "epsilon": 0.3,
        "expected_min_pieces": 2,
        "note": "Near-threshold oscillations: global range 0.8 > 2ε (=0.6). Optimal split e.g. [0,0.2,0.2,0.0] and [0.8]."
    },
]

#Iteration3
test_cases3 = [
    {
        # 1) Perfectly constant signal → should collapse to 1 piece even with ε=0
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2], [1, 2], [3, 2], [5, 2], [6, float('inf')]],
        "epsilon": 0.0
    },
    {
        # 2) Two-level signal at exact merge boundary (range == 2ε) → merge sensitivity
        # range = |2.7 - 2.0| = 0.7; ε = 0.35 → 2ε = 0.7 (boundary case)
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2.0], [1, 2.7], [2, 2.0], [4, 2.7], [5, float('inf')]],
        "epsilon": 0.35
    },
    {
        # 3) Just over the boundary (range > 2ε by a hair) → must NOT merge all
        # range = 0.700001; ε = 0.35 → 2ε = 0.7
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2.0], [1, 2.700001], [2, 2.0], [4, 2.700001], [5, float('inf')]],
        "epsilon": 0.35
    },
    {
        # 4) Alternating small ups/downs all fitting in a band of width 2ε → should merge to 1
        # values in [-0.4, 0.4], range = 0.8; ε = 0.5 → 2ε = 1.0
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [0.5, 0.4], [1.0, -0.4], [1.5, 0.3], [2.0, -0.2], [2.5, 0.1],
                  [3.0, float('inf')]],
        "epsilon": 0.5
    },
    {
        # 5) Narrow spike: one level jumps far outside the band → spike forces an extra piece
        # range across all = 5; ε = 2 → 2ε = 4 < 5, can't merge all
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 5], [2, 0], [3, 0], [4, float('inf')]],
        "epsilon": 2.0
    },
    {
        # 6) Long plateau with exact duplicates, then a jump well beyond 2ε → split into 2
        # First three are equal (mergeable even at ε=0); jump to 3 with ε=0 keeps them separate
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1], [2, 1], [3, 1], [5, 3], [6, float('inf')]],
        "epsilon": 0.0
    },
    {
        # 7) Monotone staircase where best is to group into two bands
        # values: 0, 0.4, 0.8, 1.2, 1.6; ε=0.5 → 2ε=1.0
        # Optimal grouping: [0..0.8] (range 0.8) and [1.2..1.6] (range 0.4) → 2 pieces
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.4], [2, 0.8], [3, 1.2], [4, 1.6], [5, float('inf')]],
        "epsilon": 0.5
    },
    {
        # 8) Two tight clusters separated by a gap bigger than 2ε → should yield 2 pieces
        # cluster A around 2 ± 0.2, cluster B around 5 ± 0.2; ε=0.3 → 2ε=0.6 (clusters OK), gap ~3
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.1], [0.9, 1.9], [1.8, 2.2], [2.7, 1.8],
                  [4.0, 5.2], [5.0, 4.9], [6.0, 5.1], [7.0, 5.0],
                  [8.0, float('inf')]],
        "epsilon": 0.3
    },
    {
        # 9) Negative-to-positive separation → best is 2 bands (left negative, right positive)
        # values: -3, -2.4, 2.4, 3; ε=2.5 → 2ε=5; full range=6 (>5), so at least 2 pieces
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -3.0], [1, -2.4], [2, 2.4], [3, 3.0], [4, float('inf')]],
        "epsilon": 2.5
    },
    {
        # 10) Very large ε → everything should collapse to 1 piece regardless of levels
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -10], [1, 3], [2, -4], [3, 8], [4, 1], [5, float('inf')]],
        "epsilon": 100.0
    },
]

#Iteration4
test_cases4 = [
    # 1) All equal values → merges to 1 even with ε=0
    {
        "id": "TC01_equal_values",
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,2],[3,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "All yi identical."
    },

    # 2) Alternating within tolerance band → whole thing merges at equality threshold
    {
        "id": "TC02_within_band",
        "pc_fx": [[-float('inf'), float('inf')],[0,2.4],[1,2.6],[2,2.5],[3,2.55],[4,float('inf')]],
        "epsilon": 0.1,  # max-min = 0.2 == 2ε
        "expected_min_pieces": 1,
        "notes": "Max-min equals 2ε; boundary-tight merge."
    },

    # 3) Just over the threshold → nothing merges
    {
        "id": "TC03_just_over",
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,0.21],[2,0.0],[3,float('inf')]],
        "epsilon": 0.10,  # adjacent ranges = 0.21 > 2ε=0.20
        "expected_min_pieces": 3,
        "notes": "Fails by 0.01; forces 3 pieces."
    },

    # 4) Big spike in the middle, ε too small → no adjacent merge
    {
        "id": "TC04_spike_no_merge",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,3],[2,0],[3,float('inf')]],
        "epsilon": 1.0,  # diff 3 > 2ε = 2
        "expected_min_pieces": 3,
        "notes": "Large jump blocks any merge."
    },

    # 5) Monotone ramp; only pairs fit the band
    {
        "id": "TC05_ramp_pairing",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,float('inf')]],
        "epsilon": 0.6,  # allowed band 2ε = 1.2 → best is [0,1] and [2,3]
        "expected_min_pieces": 2,
        "notes": "Greedy pairing is optimal here."
    },

    # 6) ε = 0 with repeated runs → only identical runs merge (adjacency matters)
    {
        "id": "TC06_zero_eps_runs",
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,1],[2,2],[3,2],[4,1],[5,1],[6,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "notes": "Runs [1,1], [2,2], [1,1]; non-adjacent equals can't merge across the 2's."
    },

    # 7) Non-uniform x spacing; equality threshold allows full collapse
    {
        "id": "TC07_nonuniform_x",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[10,10],[10.5,0],[20,float('inf')]],
        "epsilon": 5.0,  # max-min = 10 == 2ε
        "expected_min_pieces": 1,
        "notes": "Spacing irrelevant under L∞; equality case."
    },

    # 8) Sign changes with ε just too small → no merges anywhere
    {
        "id": "TC08_sign_change_tight",
        "pc_fx": [[-float('inf'), float('inf')],[0,-1],[1,1],[2,-1],[3,float('inf')]],
        "epsilon": 0.9,  # diff 2 > 2ε = 1.8
        "expected_min_pieces": 3,
        "notes": "Every adjacent diff exceeds 2ε."
    },

    # 9) Single tall spike flanked by zeros → three pieces (adjacency constraint)
    {
        "id": "TC09_single_spike",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,0],[2,10],[3,0],[4,0],[5,float('inf')]],
        "epsilon": 1.0,  # zeros can merge only within each contiguous block
        "expected_min_pieces": 3,
        "notes": "Left zeros, spike, right zeros → cannot bridge across the spike."
    },

    # 10) Huge ε collapses any sequence → 1 piece
    {
        "id": "TC10_huge_epsilon",
        "pc_fx": [[-float('inf'), float('inf')],[0,-5],[1,4],[2,0],[3,7],[4,-3],[5,float('inf')]],
        "epsilon": 1e9,
        "expected_min_pieces": 1,
        "notes": "Stress test for over-merging."
    },
]

#Iteration5
test_cases5 = [
    {
        "name": "TC1_constant_everywhere_epsilon0",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0], [1.0, 2.0], [3.0, 2.0], [5.0, float('inf')]],
        "epsilon": 0.0,
        # All values identical ⇒ can be approximated exactly by a single level
        "expected_min_pieces": 1,
        "why": "Completely flat function; sanity check that algorithm collapses to 1 piece."
    },
    {
        "name": "TC2_borderline_merge_eq_2epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [2.0, 1.0], [4.0, float('inf')]],
        "epsilon": 0.5,
        # Range = 1.0 = 2*epsilon ⇒ a single level exists within ±epsilon of all y's
        "expected_min_pieces": 1,
        "why": "Exact threshold case: range == 2ε should still allow merging to 1 piece."
    },
    {
        "name": "TC3_just_over_threshold_no_merge",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [2.0, 1.01], [4.0, float('inf')]],
        "epsilon": 0.5,
        # Range = 1.01 > 2*epsilon ⇒ need ≥2 pieces
        "expected_min_pieces": 2,
        "why": "Barely above threshold; algorithm must NOT merge into 1 piece."
    },
    {
        "name": "TC4_alternating_within_band_global_merge",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.6], [2.0, 0.1], [3.0, 0.7], [4.0, float('inf')]],
        "epsilon": 0.35,
        # Range = 0.7 = 2*epsilon ⇒ all should merge to 1
        "expected_min_pieces": 1,
        "why": "Non-monotone oscillations but still within a single ±ε band overall."
    },
    {
        "name": "TC5_narrow_high_spike",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [5.0, 10.0], [5.0001, 0.0], [10.0, float('inf')]],
        "epsilon": 4.9,
        # Range across entire domain is 10.0; 2ε = 9.8 < 10 ⇒ at least 2 pieces
        "expected_min_pieces": 2,
        "why": "Tiny interval spike (measure ~0) still matters in L∞; must create a separate piece."
    },
    {
        "name": "TC6_ramp_of_steps_pairwise_merge_only",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, float('inf')]],
        "epsilon": 0.6,
        # Values 0,1,2,3 (range=3). 2ε=1.2 ⇒ cannot merge all, but can merge into 2 groups (e.g., {0,1} and {2,3})
        "expected_min_pieces": 2,
        "why": "Monotone step increases; optimal solution groups adjacent steps."
    },
    {
        "name": "TC7_tiny_intervals_numerical_robustness",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -1.0], [1e-9, 1.0], [2e-9, -1.0], [3e-9, 1.0], [1.0, float('inf')]],
        "epsilon": 0.49,
        # Values alternate ±1 (range=2). 2ε=0.98 < 2 ⇒ merging across signs not allowed
        "expected_min_pieces": 4,
        "why": "Pathological short intervals; tests handling of precision and no over-merging."
    },
    {
        "name": "TC8_small_noise_around_level_global_merge",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.00], [1.0, 2.10], [2.0, 1.90], [3.0, 2.05], [4.0, float('inf')]],
        "epsilon": 0.10,
        # Range = 0.20 = 2ε ⇒ single piece should suffice
        "expected_min_pieces": 1,
        "why": "Noisy plateau; should collapse to one level at threshold."
    },
    {
        "name": "TC9_long_plateau_then_jump_beyond_2epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                  [-5.0, 3.0], [0.0, 3.0], [5.0, 4.2], [10.0, float('inf')]],
        "epsilon": 0.5,
        # Range = 1.2; 2ε=1.0 ⇒ cannot be 1 piece; optimal is 2 pieces
        "expected_min_pieces": 2,
        "why": "Large plateau then a modest jump exceeding the 2ε band."
    },
    {
        "name": "TC10_three_clusters_only_two_mergeable",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -1.0], [2.0, -0.1], [4.0, 1.2], [6.0, float('inf')]],
        "epsilon": 0.55,
        # Pair (-1.0, -0.1): range=0.9 ≤ 2ε=1.1 ⇒ mergeable
        # Including 1.2 expands range to 2.2 > 1.1 ⇒ cannot merge all
        "expected_min_pieces": 2,
        "why": "Two close clusters and one far cluster; optimal should be 2 pieces."
    },
]

#Iteration6
test_cases6 = [
    # 1) All-equal values; epsilon = 0 → everything should merge exactly
    {
        "id": 1,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.5], [1.0, 2.5], [3.0, 2.5], [5.0, 2.5],
                  [6.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Exact merge: all y equal; ε=0 forces exact equality."
    },

    # 2) Alternating 0/1 with ε just too small to merge any jump of 1
    {
        "id": 2,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0], [4, 0.0], [5, 1.0],
                  [6, float('inf')]],
        "epsilon": 0.49,  # 2ε = 0.98 < 1.0
        "expected_min_pieces": 6,
        "description": "No merges: range(0,1)=1 > 2ε."
    },

    # 3) Same pattern as (2) but ε just big enough to merge all
    {
        "id": 3,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0], [4, 0.0], [5, 1.0],
                  [6, float('inf')]],
        "epsilon": 0.5,   # 2ε = 1.0 == range → all mergeable into one
        "expected_min_pieces": 1,
        "description": "Tight threshold: 2ε equals jump; whole series can merge."
    },

    # 4) Monotone small steps: pairwise merges only
    {
        "id": 4,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.4], [2.0, 0.8], [3.0, 1.2],
                  [4.0, float('inf')]],
        "epsilon": 0.25,  # 2ε = 0.5; adjacent ranges 0.4 ≤ 0.5, but global 1.2 > 0.5
        "expected_min_pieces": 2,
        "description": "Chain case: cannot merge all; optimal merges into two blocks."
    },

    # 5) Single spike outlier amid flats
    {
        "id": 5,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.0], [2.0, 2.0], [3.0, 0.0], [4.0, 0.0],
                  [5.0, float('inf')]],
        "epsilon": 0.9,   # 2ε = 1.8 < spike range 2.0
        "expected_min_pieces": 2,
        "description": "Outlier forces its own piece; rest flatten together."
    },

    # 6) Very short intervals (length shouldn’t matter); alternating near-threshold
    {
        "id": 6,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.00, 0.0], [0.01, 1.0], [0.02, 0.0], [0.03, 1.0],
                  [0.04, float('inf')]],
        "epsilon": 0.49,  # 2ε = 0.98 < 1.0 → no merges despite tiny widths
        "expected_min_pieces": 4,
        "description": "Width-agnostic correctness: values control feasibility, not lengths."
    },

    # 7) Large jump on first piece; rest within ε to merge together
    {
        "id": 7,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 10.0], [2.0, 5.1], [4.0, 5.0], [6.0, 5.2],
                  [8.0, float('inf')]],
        "epsilon": 0.15,  # 2ε = 0.30; block {5.1,5.0,5.2} range=0.2 → merge; 10.0 too far
        "expected_min_pieces": 2,
        "description": "Tail merge with one big leading jump."
    },

    # 8) Negative values; two natural blocks
    {
        "id": 8,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -1.00], [1.0, -1.25], [2.0, -2.00], [3.0, -2.20],
                  [4.0, float('inf')]],
        "epsilon": 0.15,  # 2ε = 0.30; block1 range=0.25, block2 range=0.20 → 2 blocks
        "expected_min_pieces": 2,
        "description": "Two tight clusters separated by a large gap."
    },

    # 9) Flat with tiny noise; tests floating-point stability
    {
        "id": 9,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 5.00], [1.0, 5.05], [2.0, 4.95], [3.0, 5.02],
                  [4.0, float('inf')]],
        "epsilon": 0.06,  # 2ε = 0.12; range here is 0.10 → all merge
        "expected_min_pieces": 1,
        "description": "Tiny jitter within tolerance; should compress to one piece."
    },

    # 10) “Non-transitive” chain: each adjacent pair fits, all three together don’t
    {
        "id": 10,
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.00], [1.0, 0.40], [2.0, 0.80],
                  [3.0, float('inf')]],
        "epsilon": 0.21,  # 2ε = 0.42; adj ranges = 0.40 OK, global = 0.80 not OK
        "expected_min_pieces": 2,
        "description": "Forces optimal partition into two merged blocks."
    },
]

#Iteration7
test_cases7 = [
    # 1) Constant function, ε = 0 should still merge all
    {
        "id": 1,
        "pc_fx": [[-float("inf"), float("inf")],[0,2],[1,2],[2,2],[3,2],[4,float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Constant values; tests ε=0 boundary."
    },

    # 2) Alternating two values, just below threshold (cannot merge any 0 with 1)
    {
        "id": 2,
        "pc_fx": [[-float("inf"), float("inf")],[0,0],[1,1],[2,0],[3,1],[4,0],[5,1],[6,float("inf")]],
        "epsilon": 0.49,  # 2ε = 0.98 < range(0,1)=1
        "expected_min_pieces": 6,
        "notes": "Alternating 0/1; below merge threshold; every run stays separate."
    },

    # 3) Same alternating, exactly at threshold (now the whole thing can merge)
    {
        "id": 3,
        "pc_fx": [[-float("inf"), float("inf")],[0,0],[1,1],[2,0],[3,1],[4,0],[5,1],[6,float("inf")]],
        "epsilon": 0.5,   # 2ε = 1.0 == range
        "expected_min_pieces": 1,
        "notes": "Boundary case where 2ε = range; should merge to one piece."
    },

    # 4) Staircase increasing; needs a split when range would exceed 2ε
    {
        "id": 4,
        "pc_fx": [[-float("inf"), float("inf")],[0,0.0],[1,0.4],[2,0.8],[3,1.2],[4,1.6],[5,float("inf")]],
        "epsilon": 0.4,   # 2ε = 0.8
        "expected_min_pieces": 2,  # [0,0.4,0.8] and [1.2,1.6]
        "notes": "Staircase; greedy window reaches range=0.8 then must cut."
    },

    # 5) Plateau with an outlier spike that forces isolating the spike
    {
        "id": 5,
        "pc_fx": [[-float("inf"), float("inf")],[0,2],[1,2],[2,2],[3,10],[4,2],[5,2],[6,float("inf")]],
        "epsilon": 3.9,   # 2ε = 7.8 < range(2..10)=8
        "expected_min_pieces": 3,  # [2,2,2], [10], [2,2]
        "notes": "Single spike slightly beyond threshold; must isolate."
    },

    # 6) Precision edge: tiny float overshoot should force a split
    {
        "id": 6,
        "pc_fx": [[-float("inf"), float("inf")],[0,0.0],[1,0.2],[2,0.4],[3,0.6000000001],[4,float("inf")]],
        "epsilon": 0.3,   # 2ε = 0.6; range = 0.6000000001 > 0.6
        "expected_min_pieces": 2,  # [0,0.2,0.4] and [0.6000000001]
        "notes": "Floating-point hairline breach of 2ε."
    },

    # 7) Very tiny intervals in x; algorithm should ignore x-scale under L∞
    {
        "id": 7,
        "pc_fx": [[-float("inf"), float("inf")],[0.0,0],[1e-12,10],[1e-11,10],[1e-10,10],[2e-10,0],[3e-10,float("inf")]],
        "epsilon": 5.0,   # 2ε = 10; range(0..10)=10 -> mergeable
        "expected_min_pieces": 1,
        "notes": "Checks that x-spacing doesn’t affect L∞ merging."
    },

    # 8) Negative to positive values; must split across the sign gap
    {
        "id": 8,
        "pc_fx": [[-float("inf"), float("inf")],[0,-3],[1,-2],[2,-1],[3,1],[4,2],[5,3],[6,float("inf")]],
        "epsilon": 1.4,   # 2ε = 2.8
        "expected_min_pieces": 2,  # [-3,-2,-1] and [1,2,3]
        "notes": "Sign change; minimal two blocks by range."
    },

    # 9) Huge ε right at threshold across a wide range
    {
        "id": 9,
        "pc_fx": [[-float("inf"), float("inf")],[0,-100],[1,0],[2,100],[3,float("inf")]],
        "epsilon": 100.0, # 2ε = 200 == range(-100..100)
        "expected_min_pieces": 1,
        "notes": "Large ε equals full range; single piece."
    },

    # 10) Many runs; since range(0,5)=5 > 2ε=4, each run must remain separate
    {
        "id": 10,
        "pc_fx": [[-float("inf"), float("inf")],
                  [0,0],[1,0],[2,0],
                  [3,5],[4,5],
                  [5,0],[6,0],
                  [7,5],[8,5],[9,5],
                  [10,0],
                  [11,float("inf")]],
        "epsilon": 2.0,   # 2ε = 4 < 5
        "expected_min_pieces": 5,  # runs: 0s(3),5s(2),0s(2),5s(3),0s(1)
        "notes": "Run segmentation when high/low gap exceeds 2ε."
    },
]

#Iteration8
test_cases8 = [
    {
        "id": 1,
        "desc": "All equal values; ε=0 should still allow 1 piece.",
        "pc_fx": [[-float('inf'), float('inf')],[0,2.0],[1,2.0],[2,2.0],[3,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1
    },
    {
        "id": 2,
        "desc": "Small drift entirely within 2ε → everything should merge.",
        "pc_fx": [[-float('inf'), float('inf')],[0,3.1],[1,3.4],[2,3.6],[3,3.9],[4,float('inf')]],
        "epsilon": 0.5,   # 2ε = 1.0; range = 3.9-3.1 = 0.8 ≤ 1.0
        "expected_min_pieces": 1
    },
    {
        "id": 3,
        "desc": "Strictly increasing far beyond 2ε → nothing merges.",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,2],[2,4],[3,6],[4,float('inf')]],
        "epsilon": 0.49,  # 2ε = 0.98 < step size = 2
        "expected_min_pieces": 4
    },
    {
        "id": 4,
        "desc": "Alternating low/high creating hard boundaries; no merges.",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,0],[3,10],[4,0],[5,10],[6,float('inf')]],
        "epsilon": 4.9,   # 2ε = 9.8 < jump = 10
        "expected_min_pieces": 6
    },
    {
        "id": 5,
        "desc": "Contiguity trap: wide spike blocks merging across it.",
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,0.1],[2,5.0],[3,0.2],[4,0.0],[5,float('inf')]],
        "epsilon": 0.2,   # 2ε = 0.4; before & after spike each mergeable, but not across the spike
        "expected_min_pieces": 3
    },
    {
        "id": 6,
        "desc": "Exactly tight at boundary: max-min = 2ε → should merge.",
        "pc_fx": [[-float('inf'), float('inf')],[0,1.0],[1,2.0],[2,float('inf')]],
        "epsilon": 0.5,   # 2ε = 1.0; range = 1.0
        "expected_min_pieces": 1
    },
    {
        "id": 7,
        "desc": "ε=0 forces exact matching → only equal adjacents can merge (none here).",
        "pc_fx": [[-float('inf'), float('inf')],[0,1.0],[1,2.0],[2,1.0],[3,2.0],[4,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 4
    },
    {
        "id": 8,
        "desc": "Greedy pitfall: optimal cut is early; overextending first block fails.",
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,0.9],[2,1.8],[3,2.7],[4,3.6],[5,float('inf')]],
        "epsilon": 0.5,   # 2ε = 1.0
        # Optimal: [0,0.9] | [1.8,2.7] | [3.6] → 3 pieces
        "expected_min_pieces": 3
    },
    {
        "id": 9,
        "desc": "Negative to positive spread exactly equals 2ε → all mergeable.",
        "pc_fx": [[-float('inf'), float('inf')],[0,-2.0],[1,-2.0],[2,2.0],[3,2.0],[4,float('inf')]],
        "epsilon": 2.0,   # 2ε = 4; range = 4
        "expected_min_pieces": 1
    },
    {
        "id": 10,
        "desc": "Numerical robustness: just-over-threshold prevents merge.",
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,1.0000000001],[2,float('inf')]],
        "epsilon": 0.5,   # 2ε = 1.0; range ≈ 1.0000000001 > 1.0
        "expected_min_pieces": 2
    },
]
#Iteration9
test_cases9 = [
    {
        "id": 1,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 3.0],[1.0, 3.0],[2.0, 3.0],[3.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Pure constant signal; with ε=0 the whole domain can be 1 piece exactly."
    },
    {
        "id": 2,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 0.0],[1.0, 1.0],[2.0, 2.0],[3.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "description": "Strictly increasing steps; ε=0 forces an exact match (no merging)."
    },
    {
        "id": 3,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 0.0],[1.0, 1.0],[2.0, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Tight boundary: jump = 1 equals 2ε ⇒ both intervals can merge into a single piece."
    },
    {
        "id": 4,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 0.0],[1.0, 2.0],[2.0, 0.0],[3.0, 2.0],[4.0, float('inf')]],
        "epsilon": 0.4,
        "expected_min_pieces": 4,
        "description": "Alternating highs/lows; each adjacent jump (Δ=2) > 2ε=0.8, so nothing can merge."
    },
    {
        "id": 5,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 0.0],[1.0, 0.0],[2.0, 5.0],[3.0, 0.0],[4.0, 0.0],[5.0, float('inf')]],
        "epsilon": 2.4,
        "expected_min_pieces": 3,
        "description": "Narrow tall spike (Δ=5 > 2ε=4.8) blocks global merge; zeros on each side merge locally."
    },
    {
        "id": 6,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 0.0],[1.0, 50.0],[2.0, 100.0],[3.0, float('inf')]],
        "epsilon": 50.0,
        "expected_min_pieces": 1,
        "description": "Range = 100 equals 2ε ⇒ entire domain can be a single piece."
    },
    {
        "id": 7,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 2.00],[1.0, 2.10],[2.0, 1.95],[3.0, 2.05],[4.0, 2.00],[5.0, float('inf')]],
        "epsilon": 0.10,
        "expected_min_pieces": 1,
        "description": "Small wobble around a level; max-min = 0.15 ≤ 2ε=0.20 ⇒ 1 piece should suffice."
    },
    {
        "id": 8,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 0.0],[1.0, 3.0],[2.0, 3.0],[3.0, 3.0],[4.0, 0.0],[5.0, float('inf')]],
        "epsilon": 0.9,
        "expected_min_pieces": 3,
        "description": "Large plateau in middle; edges at 0.0. Δ(0↔3)=3 > 2ε=1.8 prevents merging across edges."
    },
    {
        "id": 9,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, -2.0],[1.0, 2.0],[2.0, -2.0],[3.0, float('inf')]],
        "epsilon": 2.0,
        "expected_min_pieces": 1,
        "description": "Symmetric highs/lows; max-min = 4 equals 2ε ⇒ 1-piece fit at ~0 covers all."
    },
    {
        "id": 10,
        "pc_fx": [[-float('inf'), float('inf')],[0.0, 0.0],[1.0, 3.1],[2.0, 0.0],[3.0, 3.1],[4.0, 0.0],[5.0, float('inf')]],
        "epsilon": 1.55,
        "expected_min_pieces": 1,
        "description": "Multiple jumps exactly at 2ε (3.1 ≈ 2×1.55); boundary-equality everywhere ⇒ global 1 piece."
    },
]

#Iteration10
test_cases10 = [
    {
        # Constant function ⇒ always 1 piece (even with epsilon = 0).
        "pc_fx": [[-float('inf'), float('inf')],[0,5.0],[1,5.0],[2,5.0],[3,5.0],[4,float('inf')]],
        "epsilon": 0.0,
        "opt_pieces": 1
    },
    {
        # Boundary-tight: vmax - vmin == 2*epsilon exactly (should MERGE).
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,1.0],[2,float('inf')]],
        "epsilon": 0.5,  # 2*epsilon = 1.0; range = 1.0 → valid as ONE piece
        "opt_pieces": 1
    },
    {
        # Floating precision trap: very slightly over the boundary if compared too strictly.
        # Good implementations use <= with a tolerance (or robust comparisons).
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,1.0000000002],[2,float('inf')]],
        "epsilon": 0.5,  # 2*epsilon = 1.0; true range is 1.0000000002 → requires TWO pieces
        "opt_pieces": 2
    },
    {
        # Greedy pitfall: local oscillations but global range fits within 2*epsilon.
        # Entire set fits with ε = 1.0 (range = 1.9 ≤ 2.0) ⇒ 1 piece; naive greedy may over-split.
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,1.9],[2,0.2],[3,1.8],[4,float('inf')]],
        "epsilon": 1.0,
        "opt_pieces": 1
    },
    {
        # Single spike: best is to isolate the spike, merge the rest.
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,0.0],[2,3.0],[3,0.0],[4,0.0],[5,float('inf')]],
        "epsilon": 1.0,  # 2*epsilon = 2.0; range with spike = 3.0 → needs split
        "opt_pieces": 2
    },
    {
        # Monotone staircase with step 0.6 and ε=0.5 (threshold 1.0).
        # Optimal grouping: (0,0.6), (1.2,1.8), (2.4) ⇒ 3 pieces.
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,0.6],[2,1.2],[3,1.8],[4,2.4],[5,float('inf')]],
        "epsilon": 0.5,
        "opt_pieces": 3
    },
    {
        # Large epsilon: everything merges (stress that width of intervals doesn’t matter under L∞).
        "pc_fx": [[-float('inf'), float('inf')],[0,-5.0],[1,10.0],[2,0.0],[3,7.0],[4,float('inf')]],
        "epsilon": 100.0,
        "opt_pieces": 1
    },
    {
        # Zero epsilon with all distinct values ⇒ each distinct run must be separate.
        "pc_fx": [[-float('inf'), float('inf')],[0,1.0],[1,2.0],[2,3.0],[3,4.0],[4,float('inf')]],
        "epsilon": 0.0,
        "opt_pieces": 4
    },
    {
        # “Chaining” / transitivity trap:
        # Any three consecutive values fit in a segment (span ≤ 2ε), but all four do not.
        # Optimal is 2 pieces: [0, 0.9, 1.8] and [2.7].
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,0.9],[2,1.8],[3,2.7],[4,float('inf')]],
        "epsilon": 1.0,  # 2*epsilon = 2.0; full range = 2.7 → need split
        "opt_pieces": 2
    },
    {
        # Two tight clusters with small jitter; clusters must be split under small ε.
        # Cluster A around 0 (span ≈ 0.02), Cluster B around 3 (span ≈ 0.02),
        # but together span ≈ 3.02 >> 2ε (with ε=0.05 ⇒ 2ε=0.1).
        "pc_fx": [[-float('inf'), float('inf')],[0,0.00],[1,0.01],[2,-0.01],[3,3.00],[4,2.99],[5,3.01],[6,float('inf')]],
        "epsilon": 0.05,
        "opt_pieces": 2
    },
]

#Iteration11
test_cases11 = [
    {
        "name": "All equal values (ε=0 still merges all)",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 3.0], [5.0, 3.0], [10.0, 3.0],
                  [12.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Exact equality across all pieces; with ε=0, one block is feasible."
    },
    {
        "name": "Single big jump blocks merge? (cannot)",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 5.0],
                  [2.0, float('inf')]],
        "epsilon": 2.0,  # 2ε = 4 < jump 5
        "expected_min_pieces": 2,
        "notes": "Jump exceeds 2ε; must split."
    },
    {
        "name": "Borderline == 2ε merges everything",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0], [1.0, 2.5], [2.0, 1.0], [3.0, 2.5],
                  [4.0, float('inf')]],
        "epsilon": 0.75,  # 2ε = 1.5; range {1.0, 2.5} = 1.5
        "expected_min_pieces": 1,
        "notes": "max−min == 2ε is allowed; all four merge."
    },
    {
        "name": "Staircase just over threshold (forces no merges)",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0],
                  [5.0, float('inf')]],
        "epsilon": 0.49,  # 2ε = 0.98 < step size 1
        "expected_min_pieces": 5,
        "notes": "Every adjacent jump slightly exceeds 2ε; no merging is legal."
    },
    {
        "name": "Big outlier spike amid flats",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.0], [2.0, 100.0], [3.0, 0.0], [4.0, 0.0],
                  [5.0, float('inf')]],
        "epsilon": 10.0,  # 2ε = 20 << 100
        "expected_min_pieces": 2,
        "notes": "Spike must be isolated; the rest (all 0) collapse to one block."
    },
    {
        "name": "Jitter fully inside ε band (collapse to one)",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 10.4], [1.0, 10.1], [2.0, 10.6], [3.0, 10.0], [4.0, 10.3],
                  [5.0, float('inf')]],
        "epsilon": 0.5,  # 2ε = 1.0; range ≈ 0.6
        "expected_min_pieces": 1,
        "notes": "All values lie in a 0.6 window; one block is feasible."
    },
    {
        "name": "Negatives: partial merge only",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -3.0], [1.0, -2.0], [2.0, -1.0],
                  [3.0, float('inf')]],
        "epsilon": 0.5,  # 2ε = 1.0
        "expected_min_pieces": 2,
        "notes": "(-3,-2) can merge (range 1 ≤ 1.0); adding -1 gives range 2 > 1.0."
    },
    {
        "name": "Non-uniform x spacing, 3 levels ladder",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [0.7, 1.8], [3.2, 3.6], [7.9, float('inf')]],
        "epsilon": 1.0,  # 2ε = 2.0
        "expected_min_pieces": 2,
        "notes": "0 and 1.8 merge (1.8 ≤ 2.0); 3.6 must be separate."
    },
    {
        "name": "Huge ε makes everything one block",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -7.0], [2.0, 5.0], [4.0, 13.0],
                  [5.0, float('inf')]],
        "epsilon": 10.0,  # 2ε = 20; range -7..13 = 20
        "expected_min_pieces": 1,
        "notes": "max−min == 2ε; still allowed → single block."
    },
    {
        "name": "Adversarial ordering: exactly two optimal blocks",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 2.0], [2.0, 4.0],
                  [3.0, float('inf')]],
        "epsilon": 1.0,  # 2ε = 2.0
        "expected_min_pieces": 2,
        "notes": "All three together have range 4 > 2; best is [0,2] & [4] (or [0] & [2,4])."
    },
]

#Iteration12
test_cases12 = [
    # 1) Epsilon = 0 on a constant signal → optimal must equal the true number of pieces (no merging allowed).
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 5],[1, 5],[2, 5],[3, 5],[4, float("inf")]],
        "epsilon": 0.0
    },

    # 2) All values lie within a band of width <= 2*epsilon → should be mergeable into ONE piece.
    # max-min = 0.6, epsilon = 0.5 → 0.6 <= 1.0 ⇒ 1 piece is feasible.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 5.0],[1, 5.6],[2, 5.3],[3, 5.2],[4, float("inf")]],
        "epsilon": 0.5
    },

    # 3) Two clusters far apart → should split into exactly TWO merged pieces (one per cluster).
    # Jumps ~3 > 2*epsilon=2 → clusters cannot merge across.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0],[1, 0],[2, 3],[3, 3],[4, float("inf")]],
        "epsilon": 1.0
    },

    # 4) Alternating high/low with big jumps → cannot merge across alternations; expects many pieces.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0],[0.5, 10],[1.0, 0],[1.5, 10],[2.0, 0],[2.5, 10],[3.0, float("inf")]],
        "epsilon": 1.0
    },

    # 5) Exact boundary case: jump == 2*epsilon → should be mergeable (tests tie handling).
    # Values in {0,1}, epsilon=0.5 ⇒ range 1.0 == 2*epsilon ⇒ one piece should be allowed.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0],[1, 1],[2, 0],[3, 1],[4, float("inf")]],
        "epsilon": 0.5
    },

    # 6) Narrow tall spike between flats → must isolate spike (left/right flats can’t be merged through it).
    # Jump 5 > 2*epsilon=4 ⇒ spike forces a split (expect 3 pieces: left, spike, right).
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0],[1.0, 5],[1.1, 0],[3.0, float("inf")]],
        "epsilon": 2.0
    },

    # 7) Floating-point hairline merge: range = 1.0000001, 2*epsilon = 1.0000002 → merge should be possible.
    # Stresses numerical robustness at the boundary.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0.0, 0.0],[1.0, 1.0000001],[2.0, 0.5],[3.0, float("inf")]],
        "epsilon": 0.5000001
    },

    # 8) Negative→near-zero→positive: choose the largest feasible merged block and a separate positive tail.
    # From -3 to 0.2 the span is 3.2 == 2*epsilon (epsilon=1.6) → mergeable; 2.9 forces a split.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [-2.0, -3.0],[-1.0, -0.5],[0.0, 0.2],[1.0, 2.9],[2.0, float("inf")]],
        "epsilon": 1.6
    },

    # 9) Small staircase increases: each step < 2*epsilon but cumulative drift breaks the band → forces multiple pieces.
    # With epsilon=0.5 (band width 1.0), values [0,0.9,1.8,2.7,3.6] require splits as the local range exceeds 1.0.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0.0, 0.0],[1.0, 0.9],[2.0, 1.8],[3.0, 2.7],[4.0, 3.6],[5.0, float("inf")]],
        "epsilon": 0.5
    },

    # 10) “Spike” amplitude exactly equals 2*epsilon → should still allow ONE merged piece (tests equality + width irrelevance).
    # Width of intervals shouldn’t matter for L∞ feasibility.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0.0, 0.0],[0.9, 0.6],[1.0, 0.0],[3.0, float("inf")]],
        "epsilon": 0.3
    },
]

#Iteration13
# 10 test cases for piecewise-constant L∞ approximation optimality checks
test_cases13 = [
    {
        # All-flat signal → always 1 piece for any ε≥0
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 5], [5, 5], [10, 5],
                  [11, float('inf')]],
        "epsilon": 0.0,
    },
    {
        # Exact merge threshold: range = 1.9 = 2ε → 1 piece should be feasible
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 1.9],
                  [10, float('inf')]],
        "epsilon": 0.95,
    },
    {
        # Alternating highs/lows → ε too small to merge all; optimal >1
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 4], [2, 0], [3, 4], [4, 0],
                  [5, float('inf')]],
        "epsilon": 1.9,  # 2ε = 3.8 < range 4 → not all collapsible
    },
    {
        # Narrow extreme spike (duration irrelevant under L∞) → needs own piece just below threshold
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [5, 10], [6, 0],
                  [10, float('inf')]],
        "epsilon": 4.99,  # 2ε = 9.98 < 10 → spike can't merge with baseline
    },
    {
        # Large endpoint jump right at a boundary → forces ≥2 pieces
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 10], [10, 0],
                  [12, float('inf')]],
        "epsilon": 4.9,  # 2ε = 9.8 < 10 → cannot merge both sides
    },
    {
        # Gentle staircase; ε just too small to collapse all into 1 piece
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [3, 1], [6, 2], [9, 3],
                  [12, float('inf')]],
        "epsilon": 1.4,  # range = 3, 2ε = 2.8 < 3 → optimal >1
    },
    {
        # Mix of negatives/positives; forces multiple pieces with this ε
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -5], [4, -1], [8, 2],
                  [12, float('inf')]],
        "epsilon": 1.5,  # range = 7, 2ε = 3 → cannot merge all
    },
    {
        # Small blips around a center; should collapse to 1 piece
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 9.1], [2, 10.9], [4, 10.2], [6, 9.4], [8, 10.7],
                  [10, float('inf')]],
        "epsilon": 1.0,  # range ≈ 1.8 ≤ 2ε → 1 piece feasible
    },
    {
        # Wild values but huge ε → everything collapses to 1 piece
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -100], [1, 50], [2, -200], [3, 400], [4, -300],
                  [5, float('inf')]],
        "epsilon": 500.0,  # range = 700 ≤ 2ε = 1000 → 1 piece feasible
    },
    {
        # Chain at exact adjacency thresholds; global range too big for 1 piece
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 1.9], [2, 3.8],
                  [3, float('inf')]],
        "epsilon": 0.95,  # Adjacent diffs = 2ε, but overall range = 4ε → optimal = 2
    },
]

#Iteration14
test_cases14 = [
    # 1) Trivial constant ⇒ always 1 piece, even for ε = 0
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 5], [1, 5], [2, 5], [3, 5],
                  [4, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "All equal values with ε=0 — sanity check for exact merging."
    },

    # 2) Alternating far-apart values ⇒ no merges possible
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0],
                  [5, float("inf")]],
        "epsilon": 4.0,   # 2ε = 8 < 10 gap
        "expected_min_pieces": 5,
        "description": "Pairwise gaps exceed 2ε; minimal = original piece count."
    },

    # 3) Cumulative drift beats pairwise checks (greedy trap)
    #    Adjacent diffs ≤ 2ε but triples break the limit.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0], [1, 1], [2, 2], [3, 3], [4, 4],
                  [5, float("inf")]],
        "epsilon": 0.9,   # 2ε = 1.8; any 3 in a row have range 2 > 1.8
        "expected_min_pieces": 3,  # [0,1], [2,3], [4]
        "description": "Cumulative range violation exposes suboptimal greedy extension."
    },

    # 4) “Just within” global tolerance ⇒ everything merges
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 2.0], [1, 3.4], [2, 3.9], [3, 2.1],
                  [4, float("inf")]],
        "epsilon": 1.0,   # 2ε = 2.0; global range = 3.9 - 2.0 = 1.9 ≤ 2
        "expected_min_pieces": 1,
        "description": "Global range barely under 2ε — tests inclusive comparisons."
    },

    # 5) Boundary equality case (range == 2ε) must merge
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 2.0],
                  [2, float("inf")]],
        "epsilon": 1.0,   # 2ε = 2.0; range = 2.0
        "expected_min_pieces": 1,
        "description": "Exact-boundary case: ensure ≤ (not <) is implemented."
    },

    # 6) Narrow spike surrounded by flats ⇒ spike must be isolated
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 0.0], [2, 10.0], [3, 0.0], [4, 0.0],
                  [5, float("inf")]],
        "epsilon": 1.0,   # 2ε = 2.0; spike forces a split
        "expected_min_pieces": 3,  # [0,0], [10], [0,0]
        "description": "Contiguous-only merging means the spike cannot be skipped."
    },

    # 7) “Bridge” via a high middle value but still within 2ε globally
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 1.9], [2, 0.0],
                  [3, float("inf")]],
        "epsilon": 1.0,   # 2ε = 2.0; global range = 1.9
        "expected_min_pieces": 1,
        "description": "Middle ‘bridge’ value — algorithm must consider full-block range."
    },

    # 8) Negatives + sign change; merge first block only
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, -5.0], [1, -4.2], [2, -4.9], [3, 3.0],
                  [4, float("inf")]],
        "epsilon": 0.6,   # 2ε = 1.2; first three range = 0.8, adding 3.0 breaks it
        "expected_min_pieces": 2,  # [-5,-4.2,-4.9], [3]
        "description": "Mixed signs with one outlier — tests range maintenance logic."
    },

    # 9) ε = 0 ⇒ only identical adjacent values can merge (exact runs)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 1], [1, 1], [2, 2], [3, 2], [4, 2], [5, 1],
                  [6, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,  # [1,1], [2,2,2], [1]
        "description": "Exact-compliance case; checks strict equality handling."
    },

    # 10) Long drift with a final tiny step pushing range just over 2ε
    #     Adjacent diffs small; full block violates — should end with 2 pieces.
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.00], [1, 0.99], [2, 1.98], [3, 2.01],
                  [4, float("inf")]],
        "epsilon": 1.0,   # 2ε = 2.0; full range = 2.01 > 2.0
        "expected_min_pieces": 2,  # [0.00,0.99,1.98], [2.01]
        "description": "Cumulative-drift edge just over limit — catches off-by-ε bugs."
    },
]

#Iteration15
test_cases15 = [
    # 1) Constant function, strict epsilon (everything should merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [4, 5], [6, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "All values equal; width=0 ≤ 2ε=0 ⇒ 1 piece."
    },

    # 2) Very large epsilon (stress that algorithm merges everything)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 5], [3, 7], [4, float('inf')]],
        "epsilon": 100.0,
        "expected_min_pieces": 1,
        "notes": "Huge ε; max-min=10 ≤ 200 ⇒ 1 piece."
    },

    # 3) Tight epsilon forbids any merge (every piece stands alone)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 3], [3, 7], [6, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 3,
        "notes": "Adjacency gaps > 2ε=2 block any merges ⇒ 3 pieces."
    },

    # 4) Boundary case: max-min == 2ε (should merge all)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "notes": "Width=2.0 equals 2ε ⇒ allowed ⇒ 1 piece. Tests boundary tolerance."
    },

    # 5) Alternating highs/lows that defeat merging under moderate ε
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, float('inf')]],
        "epsilon": 4.0,  # 2ε = 8 < width 10
        "expected_min_pieces": 4,
        "notes": "Each adjacent pair spans width=10 > 2ε=8 ⇒ no merges at all."
    },

    # 6) Overlapping-but-not-transitive widths (forces a split into 2)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 3], [2, 6], [3, float('inf')]],
        "epsilon": 2.0,  # 2ε=4; [0,3] ok, [3,6] ok, but [0,6] not ok
        "expected_min_pieces": 2,
        "notes": "Transitivity trap: [0,3] and [3,6] ok, but all three not ⇒ 2 pieces."
    },

    # 7) Single narrow spike between flats (forces 3)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [2, 0], [3, 10], [4, 0], [6, 0], [7, float('inf')]],
        "epsilon": 0.9,  # 2ε=1.8 << spike height
        "expected_min_pieces": 3,
        "notes": "Spike must be isolated; left and right flats each merge separately ⇒ 3."
    },

    # 8) Monotone small steps; optimal greedy windowing yields 2
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.9], [2, 1.8], [3, 2.7], [4, 3.6], [5, float('inf')]],
        "epsilon": 1.0,  # 2ε=2.0
        "expected_min_pieces": 2,
        "notes": "Group [0..1.8] (width 1.8), then [2.7..3.6] ⇒ 2 pieces."
    },

    # 9) Near-boundary jitter (floats close to 2ε); should split into 2
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.9], [2, 2.1], [3, 3.0], [4, float('inf')]],
        "epsilon": 0.5,  # 2ε=1.0
        "expected_min_pieces": 2,
        "notes": "[1.0,1.9] ok (width 0.9), [2.1,3.0] ok (0.9); all three 1.0..2.1 would be 1.1>1.0."
    },

    # 10) ε=0 with runs (forces grouping exactly by equal-value runs)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0], [2, 1], [3, 1], [4, 0], [5, 0], [6, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "notes": "Only exact-equal merges allowed ⇒ runs [0,0], [1,1], [0,0] ⇒ 3."
    },
]

#Iteration16
test_cases16 = [
    # 1) Constant function, ε = 0 → must be exactly 1 piece.
    {
        "name": "constant_exact_zero_eps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 3.0], [10, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "Constant value; with ε=0 the single-piece exact fit is optimal."
    },

    # 2) Merge-at-threshold: |Δ| = 2ε exactly → still mergeable to 1 piece.
    # y in {0.0, 1.4}, ε=0.7 → |Δ|=1.4 = 2ε
    {
        "name": "two_step_boundary_mergeable",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.4], [2, float('inf')]],
        "epsilon": 0.7,
        "expected_min_pieces": 1,
        "note": "Boundary case: adjacent values differ by exactly 2ε, so intervals overlap."
    },

    # 3) Just-not-mergeable: |Δ| > 2ε by a hair → cannot merge.
    # y in {0.0, 1.401}, ε=0.7 → |Δ|=1.401 > 1.4
    {
        "name": "two_step_just_not_mergeable",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.401], [2, float('inf')]],
        "epsilon": 0.7,
        "expected_min_pieces": 2,
        "note": "Tiny violation above 2ε forbids a one-piece fit."
    },

    # 4) Alternating highs/lows well beyond 2ε → no merges anywhere.
    # y in {0, 3, 0, 3}, ε=0.9 → |Δ|=3 > 2ε=1.8
    {
        "name": "alternating_extremes_no_merge",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 3.0], [2, 0.0], [3, 3.0], [4, float('inf')]],
        "epsilon": 0.9,
        "expected_min_pieces": 4,
        "note": "Each interval needs its own piece under L∞."
    },

    # 5) Clustered small steps that can merge, then a far step that cannot.
    # First three {0.0, 0.5, 0.9} overlap for ε=0.55; value 2.0 cannot join.
    {
        "name": "three_can_merge_one_cannot",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.5], [2, 0.9], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.55,
        "expected_min_pieces": 2,
        "note": "One big merged block for first three; last needs its own."
    },

    # 6) Narrow spike: width doesn’t matter in L∞, so spike must be isolated.
    # Baseline 0, spike 10, ε=4.9 → |Δ|=10 > 2ε=9.8 → spike needs its own piece.
    {
        "name": "narrow_spike_requires_isolation",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [0.999, 0.0], [1.0, 10.0], [1.001, 0.0], [2.0, 0.0], [3.0, float('inf')]],
        "epsilon": 4.9,
        "expected_min_pieces": 2,
        "note": "All non-spike parts merge; the spike stands alone."
    },

    # 7) Negative values cluster merge: all overlap for ε=1.0 → one piece.
    # y in {-5, -3, -4}; intervals [-6,-4], [-4,-2], [-5,-3] intersect.
    {
        "name": "negative_values_all_merge",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -5.0], [1, -3.0], [2, -4.0], [3, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "note": "Intersection of [y-ε, y+ε] is nonempty across all three."
    },

    # 8) Three well-separated clusters → minimum 3 pieces.
    # Clusters: {0,0.2}, {1.5,1.7}, {3.0}; ε=0.4 → 2ε=0.8; inter-cluster gaps >0.8.
    {
        "name": "three_clusters_min_three_pieces",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.2], [2.0, 1.5], [3.0, 1.7], [4.0, 3.0], [5.0, float('inf')]],
        "epsilon": 0.4,
        "expected_min_pieces": 3,
        "note": "Two small local merges; clusters remain separate."
    },

    # 9) ε = 0 with redundant adjacent equal runs.
    # Original has [2,2,5,5,2]; with ε=0 you can merge adjacent equal-valued runs.
    # Minimal #pieces = number of runs → 3 (2|5|2).
    {
        "name": "zero_eps_with_redundant_runs",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2.0], [1, 2.0], [2, 5.0], [3, 5.0], [4, 2.0], [5, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "note": "Tests that the algorithm doesn’t over-segment identical adjacents."
    },

    # 10) Large scales: huge x/y to probe numeric stability; still mergeable.
    # y in {1e9, 1e9+1}, ε=0.6 → |Δ|=1 ≤ 2ε=1.2 → one piece.
    {
        "name": "large_scale_mergeable",
        "pc_fx": [[-float('inf'), float('inf')],
                  [1_000_000.0, 1_000_000_000.0],
                  [2_000_000.0, 1_000_000_001.0],
                  [3_000_000.0, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 1,
        "note": "Stress test for large magnitudes with a boundary merge."
    },
]

#Iteration17
test_cases17 = [
    # 1) Trivial constant function → always mergeable into one piece
    {
        "label": "All-constant, ε=0",
        "pc_fx": [[-float('inf'), float('inf')],[0, 2],[1, 2],[2, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "why": "All y identical; span=0 ≤ 2ε."
    },

    # 2) Multiple equal segments → merge to one despite many cuts
    {
        "label": "Many equal values, tiny ε",
        "pc_fx": [[-float('inf'), float('inf')],[0, 5],[1, 5],[2, 5],[3, 5],[4, float('inf')]],
        "epsilon": 0.01,
        "expected_min_pieces": 1,
        "why": "Span=0, merge all."
    },

    # 3) Alternating two values exactly on the merge boundary (tight)
    {
        "label": "Alternating 0/1, ε=0.5 (tight boundary)",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],[1, 1],[2, 0],[3, 1],[4, 0],[5, 1],
                  [6, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "why": "Span=1, 2ε=1 ⇒ merge all (just feasible)."
    },

    # 4) Alternating two values just beyond the boundary → no merges across changes
    {
        "label": "Alternating 0/1, ε=0.49 (just infeasible)",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0],[1, 1],[2, 0],[3, 1],
                  [4, float('inf')]],
        "epsilon": 0.49,
        "expected_min_pieces": 4,
        "why": "Span=1, 2ε=0.98 < 1 ⇒ each change forces a cut."
    },

    # 5) Monotone ramp with tight ε → forces several cuts (greedy matters)
    {
        "label": "Monotone ramp, ε=0.25",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0],[1, 0.4],[2, 0.8],[3, 1.2],[4, 1.6],
                  [5, float('inf')]],
        "epsilon": 0.25,
        "expected_min_pieces": 3,
        "why": "Span grows past 2ε=0.5 as you extend; cut when violated."
    },

    # 6) Plateau–spike–plateau: spike splits both sides
    {
        "label": "Plateau with central spike, ε=3",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 3],[1, 3],[2, 10],[3, 3],[4, 3],
                  [5, float('inf')]],
        "epsilon": 3.0,
        "expected_min_pieces": 3,
        "why": "Span with spike is 7>2ε=6; left, spike, right must be separate."
    },

    # 7) Small oscillations around 10 within ε → all merge
    {
        "label": "Small oscillations around 10, ε=1",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 9.1],[1, 10.9],[2, 9.5],[3, 10.7],[4, 10.0],
                  [5, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "why": "Span=10.9-9.1=1.8 ≤ 2ε=2."
    },

    # 8) Big outlier at start → first piece alone, rest merge
    {
        "label": "Single large outlier at start, ε=10",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 100],[1, 0],[2, 0],[3, 0],
                  [4, float('inf')]],
        "epsilon": 10.0,
        "expected_min_pieces": 2,
        "why": "100 with 0’s: span=100>2ε=20; outlier alone."
    },

    # 9) Negative to positive with moderate ε → one cut
    {
        "label": "Negative-to-positive, ε=1.5",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -5],[1, -4],[2, -1],[3, 0],[4, 2],
                  [5, float('inf')]],
        "epsilon": 1.5,
        "expected_min_pieces": 2,
        "why": "Span across all is 7>2ε=3; optimal split around {-5,-4,-1} | {0,2}."
    },

    # 10) Zero-length middle segment (degenerate cut) that blocks merging
    {
        "label": "Zero-length spike piece in the middle, ε=3",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2],[1, 9],[1, 2],  # note x2 == x3 (zero-length [1,1))
                  [2, float('inf')]],
        "epsilon": 3.0,
        "expected_min_pieces": 3,
        "why": "Even zero-length pieces count: 2–9 span=7>2ε=6; left | spike | right."
    },
]


#Iteration18
test_cases18 = [
    # 1) Constant everywhere, ε = 0  → one piece suffices (exact match)
    {
        "name": "Constant_exact_zero_eps",
        "pc_fx": [[-float("inf"), float("inf")], [0, 5], [10, 5], [20, 5], [30, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "rationale": "All segments have same value; exact reconstruction possible with one constant."
    },

    # 2) Two levels within ε → mergeable into 1 piece
    {
        "name": "Two_levels_within_eps",
        "pc_fx": [[-float("inf"), float("inf")], [0, 2.0], [5, 2.5], [10, float("inf")]],
        "epsilon": 0.6,  # intervals [2±0.6] and [2.5±0.6] overlap → single constant feasible
        "expected_min_pieces": 1,
        "rationale": "Max diff = 0.5; ε = 0.6 ≥ 0.5 → a single constant within ε exists."
    },

    # 3) Two levels beyond ε → need ≥ 2 pieces
    {
        "name": "Two_levels_beyond_eps",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [4, 2.0], [8, float("inf")]],
        "epsilon": 0.9,  # need ε ≥ 1.0 to cover both; here ε < 1 → no single constant fits
        "expected_min_pieces": 2,
        "rationale": "Values 0 and 2 require ε ≥ 1 for one piece; ε = 0.9 < 1 so need two pieces."
    },

    # 4) Alternating 0/1 values with ε just below 0.5 → no merges allowed
    {
        "name": "Alternating_hard_no_merge",
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0], [4, 0.0], [5, float("inf")]],
        "epsilon": 0.49,  # need ε ≥ 0.5 to merge 0 and 1; here just below
        "expected_min_pieces": 5,
        "rationale": "Each 0/1 jump needs its own piece when ε < 0.5."
    },

    # 5) Exact-threshold mergeability (tight boundary case)
    {
        "name": "Exact_threshold_merge",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [2, 2.0], [4, float("inf")]],
        "epsilon": 1.0,  # exactly half the gap; one constant (e.g., 1) fits both within ε
        "expected_min_pieces": 1,
        "rationale": "At ε = gap/2, intervals touch; one piece should be accepted (≤ ε)."
    },

    # 6) Narrow spike (measure-zero intuition trap): ε moderate → spike forces its own piece
    {
        "name": "Narrow_spike_forces_piece",
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [9.9, 10.0], [10.1, 0.0], [20, float("inf")]],
        "epsilon": 4.0,
        "expected_min_pieces": 2,
        "rationale": "Spike value 10 is > ε away from plateau 0; at least two pieces (plateau + spike)."
    },

    # 7) Gradual drift but within ε span → can compress to one piece (boundary multi-step)
    {
        "name": "Monotone_small_drift_mergeable",
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [5, 0.2], [10, 0.4], [15, 0.6], [20, 0.8], [25, float("inf")]],
        "epsilon": 0.4,  # range = 0.8; ε = 0.4 = range/2 → one constant exists
        "expected_min_pieces": 1,
        "rationale": "Range equals 2ε; single-piece boundary case should pass."
    },

    # 8) Huge ε swallows large jumps → 1 piece despite big contrasts
    {
        "name": "Huge_epsilon_everything_merges",
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, -100.0], [1, 100.0], [2, -100.0], [3, 100.0], [4, float("inf")]],
        "epsilon": 200.0,  # any constant in [-100,100] is within ε=200
        "expected_min_pieces": 1,
        "rationale": "With ε very large, a single constant fits all segments."
    },

    # 9) ε = 0 on distinct values → must reproduce exactly (no merges)
    {
        "name": "Zero_epsilon_distinct_values",
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [2, 1.0], [5, 3.0], [9, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "rationale": "Exact reconstruction required; three distinct levels → three pieces."
    },

    # 10) Redundant equal-adjacent segments (should coalesce), ε = 0
    {
        "name": "Equal_adjacent_should_coalesce",
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 5.0], [1, 5.0], [2.5, 5.0], [4, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "rationale": "All adjacent segments have identical value; optimal merges to one piece."
    },
]

#Iteration19
from math import inf
test_cases19 = [
    # 1) Single piece, epsilon irrelevant → always 1
    {
        "name": "Single piece baseline",
        "pc_fx": [[-inf, inf], [0, 5], [10, inf]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "Trivial baseline."
    },

    # 2) All y equal; epsilon = 0 → still 1 (range = 0 <= 2ε)
    {
        "name": "All equal values, epsilon=0",
        "pc_fx": [[-inf, inf], [0, 3], [2, 3], [5, 3], [7, 3], [9, inf]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "Exact merging with zero tolerance."
    },

    # 3) Alternating far-apart values; epsilon too small → no merges
    {
        "name": "Alternating highs/lows forces all separate",
        "pc_fx": [[-inf, inf],
                  [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, 10],
                  [6, inf]],
        "epsilon": 2.0,  # 2ε = 4 < 10 gap
        "expected_min_pieces": 6,
        "note": "Range 10 > 2ε; each piece must stand alone."
    },

    # 4) Borderline exactly meet 2ε → whole thing can merge
    {
        "name": "Exact boundary: max-min = 2ε",
        "pc_fx": [[-inf, inf], [0, 0], [1, 4], [2, 2], [3, inf]],
        "epsilon": 2.0,  # max-min = 4 = 2ε
        "expected_min_pieces": 1,
        "note": "Tests inclusive boundary."
    },

    # 5) Floating-point hair over the boundary → must split
    {
        "name": "Floating boundary violation by 1e-9",
        "pc_fx": [[-inf, inf], [0, 0.0], [1, 4.000000001], [2, inf]],
        "epsilon": 2.0,  # 2ε = 4; range = 4.000000001 > 4
        "expected_min_pieces": 2,
        "note": "Precision/robustness to near-equality."
    },

    # 6) Huge epsilon → everything merges
    {
        "name": "Large epsilon merges all",
        "pc_fx": [[-inf, inf], [0, -5], [1, 3], [2, 9], [3, inf]],
        "epsilon": 100.0,
        "expected_min_pieces": 1,
        "note": "Sanity check for large tolerance."
    },

    # 7) Mixed neg/pos; optimal split happens once in the middle
    {
        "name": "Neg/pos mix with one optimal split",
        "pc_fx": [[-inf, inf], [0, -1.0], [1, 0.5], [2, -0.2], [3, 0.8], [4, inf]],
        "epsilon": 0.6,  # 2ε = 1.2
        "expected_min_pieces": 2,  # [-1.0] | [0.5, -0.2, 0.8]
        "note": "Greedy boundary triggers at first jump."
    },

    # 8) Spiky but within tolerance → all merge to 1
    {
        "name": "Plateau with small spikes within tolerance",
        "pc_fx": [[-inf, inf], [0, 10.0], [1, 10.9], [2, 10.1], [3, 9.2], [4, 10.8], [5, inf]],
        "epsilon": 0.9,  # 2ε = 1.8; range = 10.9 - 9.2 = 1.7 <= 1.8
        "expected_min_pieces": 1,
        "note": "Ensures algorithm doesn’t over-split noisy plateaus."
    },

    # 9) Non-mergeable sandwich: far outlier in the middle forces 3
    {
        "name": "Order/consecutiveness matters (sandwich)",
        "pc_fx": [[-inf, inf], [0, 0], [1, 10], [2, 0], [3, inf]],
        "epsilon": 3.0,  # 2ε = 6; range across all = 10 > 6
        "expected_min_pieces": 3,
        "note": "Even if first and last match, the middle outlier blocks merging."
    },

    # 10) Uneven x-gaps; only y-values matter for L∞ merging
    {
        "name": "Huge x-gaps, merges based on y-range only",
        "pc_fx": [[-inf, inf], [0, 0], [100, 5], [1000, 4], [1_000_000, 5], [10_000_000, inf]],
        "epsilon": 0.5,  # 2ε = 1; block1=[0]; block2=[5,4,5]
        "expected_min_pieces": 2,
        "note": "Confirms spacing of breakpoints is irrelevant to L∞ joinability."
    },
]

#Iteration20
test_cases20 = [
    {
        # 1) Everything within one ε-band → should compress to 1 piece
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.00], [1.0, 2.20], [2.0, 1.90], [3.0, 2.10],
                  [4.0, float('inf')]],
        "epsilon": 0.20,
        # All bands intersect (e.g., final intersection ~ [2.0, 2.1]) → optimal = 1
    },
    {
        # 2) Equality-at-threshold merge: bands just touch at ε
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.0],
                  [2.0, float('inf')]],
        "epsilon": 0.50,
        # [−0.5, 0.5] ∩ [0.5, 1.5] = {0.5} → can merge → optimal = 1
    },
    {
        # 3) Just-below-threshold alternating levels (no merges possible)
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.0], [2.0, 0.0], [3.0, 1.0],
                  [4.0, float('inf')]],
        "epsilon": 0.49,
        # Bands [−0.49,0.49] and [0.51,1.49] disjoint → each run must be separate → optimal = 4
    },
    {
        # 4) Long plateau with tiny spike far outside ε (forces an extra piece, but only 2 total)
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [5.0, 10.0], [5.0001, 0.0], [10.0, 0.0],
                  [12.0, float('inf')]],
        "epsilon": 1.0,
        # Spike [9,11] vs plateau [−1,1] do not overlap → optimal = 2 (isolate the spike)
    },
    {
        # 5) Gradual drift: first 3 merge, last 2 merge → optimal = 2
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.4], [2.0, 0.8], [3.0, 1.2], [4.0, 1.6],
                  [5.0, float('inf')]],
        "epsilon": 0.50,
        # Intersections: first trio share a non-empty band; last pair share a band; not all five.
    },
    {
        # 6) Near-merge chains that break only once (tests greedy errors)
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 5.0], [1.0, 5.9], [2.0, 6.8], [3.0, 7.7], [4.0, 8.6],
                  [5.0, float('inf')]],
        "epsilon": 0.9,
        # Step size ≈0.9; consecutive pairs overlap, but global intersection empties around the 4th/5th.
        # Optimal is to split once (e.g., first 3 + last 2) → optimal = 2
    },
    {
        # 7) Repeated equal values with short different block in the middle
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -2.0], [1.0, -2.0], [2.0, 3.5], [3.0, -2.0], [4.0, -2.0],
                  [5.0, float('inf')]],
        "epsilon": 0.4,
        # The middle 3.5 is far from −2 (bands [3.1,3.9] vs [−2.4,−1.6]) → must isolate → optimal = 2
    },
    {
        # 8) Tiny violations just over ε (ensures algorithm doesn't incorrectly merge)
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0], [1.0, 2.01], [2.0, 1.0], [3.0, 2.01],
                  [4.0, float('inf')]],
        "epsilon": 1.0,
        # Gap = 1.01 > ε → bands [0,2] vs [1.01,3.01] barely miss → cannot merge across flips → optimal = 4
    },
    {
        # 9) Trivial single-interval case (sanity check)
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 7.0],
                  [10.0, float('inf')]],
        "epsilon": 0.0,
        # Already one piece → optimal = 1
    },
    {
        # 10) Large magnitudes & mixed signs (numerical stability / scaling)
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -1e6], [1.0, -1e6 + 400], [2.0, -1e6 - 300],
                  [3.0,  1e6], [4.0,  1e6 - 200], [5.0,  1e6 + 250],
                  [6.0, float('inf')]],
        "epsilon": 350.0,
        # First three (around −1e6) can merge (ranges overlap within ±350);
        # last three (around +1e6) can merge; sign jump forces a split → optimal = 2
    },
]

#Iteration21
test_cases21 = [
    # 1) Trivial single piece (baseline sanity)
    {
        "name": "Single piece, epsilon=0 → stays 1",
        "pc_fx": [[-float('inf'), float('inf')],[0, 2],[5, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Only one actual piece; with ε=0 nothing to do."
    },

    # 2) All equal values across many pieces ⇒ should merge into 1 even with ε=0
    {
        "name": "All equal values, ε=0 → 1 piece",
        "pc_fx": [[-float('inf'), float('inf')],[0, 3],[2, 3],[4, 3],[7, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Range is 0 ≤ 2ε; everything should collapse to one piece."
    },

    # 3) Exactly on the merge boundary (range == 2ε) ⇒ still mergeable
    {
        "name": "Exact boundary merge, range=2ε",
        "pc_fx": [[-float('inf'), float('inf')],[0, 1],[1, 3],[2, 1],[3, 3],[4, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "notes": "Values in {1,3}; range=2 equals 2ε → all can be merged."
    },

    # 4) Just-over-threshold so global merge forbidden
    {
        "name": "Just over threshold → cannot merge all",
        "pc_fx": [[-float('inf'), float('inf')],[0, 1.0],[1, 3.01],[2, 1.0],[3, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "notes": "Range=2.01 > 2ε; best is to isolate the 3.01 block or split into two groups."
    },

    # 5) Narrow but tall spike (width doesn't matter under L∞)
    {
        "name": "Thin tall spike forces a split",
        "pc_fx": [[-float('inf'), float('inf')],[0, 0],[1, 10],[1.1, 0],[3, float('inf')]],
        "epsilon": 4.0,
        "expected_min_pieces": 2,
        "notes": "Background 0 with a spike at 10; range=10 > 2ε=8 → need at least two pieces."
    },

    # 6) Chain-merge non-associativity (pairs merge, triple doesn’t)
    {
        "name": "Chain-merge trap (non-associative)",
        "pc_fx": [[-float('inf'), float('inf')],[0, 0.0],[1, 1.8],[2, 3.6],[3, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "notes": "(0,1.8) and (1.8,3.6) individually OK (range≤2), but all three have range=3.6>2 → need 2 pieces."
    },

    # 7) Multiple optimal partitions with same piece count
    {
        "name": "Two optimal partitions exist",
        "pc_fx": [[-float('inf'), float('inf')],[0, 0],[1, 2],[2, 4],[3, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "notes": "Either merge (0,2) or (2,4); both give 2 pieces total. Good for tie-handling."
    },

    # 8) Negative values and crossing zero
    {
        "name": "Crossing zero with two compact clusters",
        "pc_fx": [[-float('inf'), float('inf')],[0, -5],[1, -3],[2, 2],[3, 4],[4, float('inf')]],
        "epsilon": 1.5,
        "expected_min_pieces": 2,
        "notes": "Clusters {-5,-3} and {2,4} each have range 2 ≤ 2ε=3, but gap across clusters is too large."
    },

    # 9) Jitter inside a band, then a jump
    {
        "name": "Jitter collapses, jump forces split",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 9.2],[1, 10.1],[2, 10.7],[3, 9.4],[4, 14.0],[5, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "notes": "First four values have range=1.5 ≤ 2; jump to 14 makes global merge impossible."
    },

    # 10) ε = 0 with all distinct values ⇒ no merges at all
    {
        "name": "Zero tolerance, all distinct",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1],[1, 2],[2, 3],[3, 5],[4, 8],[5, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 5,
        "notes": "Five actual pieces with different values; ε=0 forbids any merging."
    },
]

#Iteration22
test_cases22 = [
    # 1) Trivially mergeable: all values equal → always 1 piece (even for ε = 0)
    {
        "name": "Constant flat (ε=0)",
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "why": "All segments identical ⇒ one constant fits with 0 error."
    },

    # 2) Two plateaus just-not-mergeable with ε < 0.5 (range = 1)
    {
        "name": "Two plateaus need split (ε=0.49)",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[5,0],[10,1],[15,float('inf')]],
        "epsilon": 0.49,
        "expected_min_pieces": 2,
        "why": "Range=1 ⇒ best single constant gives error=0.5>ε."
    },

    # 3) Exact boundary where a single piece becomes feasible (ε = 0.5)
    {
        "name": "Two plateaus merge at boundary (ε=0.5)",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[5,0],[10,1],[15,float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "why": "Range=1 ⇒ single constant at 0.5 gives max error=0.5=ε."
    },

    # 4) Narrow spike forces an extra piece unless ε is large
    {
        "name": "Single spike (ε=4)",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[10,10],[11,0],[20,float('inf')]],
        "epsilon": 4.0,
        "expected_min_pieces": 2,
        "why": "Range across spike vs baseline = 10 ⇒ need a separate spike piece."
    },

    # 5) Two opposite spikes far apart → baseline + two spikes
    {
        "name": "Two opposite spikes (ε=3)",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[5,8],[6,0],[14,-7],[15,0],[20,float('inf')]],
        "epsilon": 3.0,
        "expected_min_pieces": 3,
        "why": "Baseline 0 plus +8 and −7 excursions each exceed 2ε=6 ⇒ 3 pieces."
    },

    # 6) Width-invariance boundary: huge unequal intervals but mergeable at ε=1
    {
        "name": "Widths don’t matter in L∞ (ε=1)",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,2],[100,0],[101,2],[200,float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "why": "Values alternate between 0 and 2, range=2 ⇒ one constant with error=1."
    },

    # 7) Very large ε collapses everything
    {
        "name": "Everything merges (ε=1e9)",
        "pc_fx": [[-float('inf'), float('inf')],[0,1],[1,10],[2,-4],[5,7],[8,float('inf')]],
        "epsilon": 1e9,
        "expected_min_pieces": 1,
        "why": "ε is huge ⇒ single piece always feasible."
    },

    # 8) Small jitter around a baseline within ε
    {
        "name": "Noisy plateau within ε (ε=0.4)",
        "pc_fx": [[-float('inf'), float('inf')],[0,3.1],[2,2.7],[4,3.3],[6,2.8],[8,3.2],[10,float('inf')]],
        "epsilon": 0.4,
        "expected_min_pieces": 1,
        "why": "All values within ±0.3 of 3 ⇒ one constant works."
    },

    # 9) Staircase with steps larger than 2ε → every step needs its own piece
    {
        "name": "Strict staircase (ε=0.25)",
        "pc_fx": [[-float('inf'), float('inf')],[0,0.0],[1,0.6],[2,1.2],[3,1.8],[4,2.4],[5,float('inf')]],
        "epsilon": 0.25,
        "expected_min_pieces": 5,
        "why": "Step size=0.6 > 2ε=0.5 ⇒ cannot merge across steps."
    },

    # 10) Alternating extremes around ε-threshold → many pieces
    {
        "name": "Alternating extremes (ε=2)",
        "pc_fx": [[-float('inf'), float('inf')],[0,-5],[1,0],[2,5],[3,0],[4,-5],[5,float('inf')]],
        "epsilon": 2.0,
        "expected_min_pieces": 5,
        "why": "Adjacent ranges ≥5 > 2ε=4 ⇒ no merges between runs."
    },
]

#Iteration23
test_cases23 = [
    # 1) Trivial constant (ε = 0) → must be exactly 1 piece
    {
        "name": "constant_one_piece_eps0",
        "pc_fx": [(-float('inf'), float('inf')), (0.0, 5.0), (10.0, float('inf'))],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Single constant segment; ε=0 forces exact match."
    },

    # 2) Exactly mergeable threshold: |Δ| = 2ε → can merge into 1
    {
        "name": "two_levels_exact_threshold_merge",
        "pc_fx": [(-float('inf'), float('inf')), (0.0, 0.0), (5.0, 2.0), (10.0, float('inf'))],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "notes": "Levels 0 and 2 differ by 2ε; one constant at 1.0 stays within ε."
    },

    # 3) Just over threshold: |Δ| > 2ε → cannot merge
    {
        "name": "two_levels_just_over_threshold",
        "pc_fx": [(-float('inf'), float('inf')), (0.0, 0.0), (5.0, 2.1), (10.0, float('inf'))],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "notes": "Δ=2.1 > 2ε=2 → needs two pieces."
    },

    # 4) Three levels where only a pair can merge; overall range too big for 1
    {
        "name": "three_levels_pair_merge_only",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (3.0, 2.0), (6.0, 4.0), (9.0, float('inf'))],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "notes": "Adj diffs are 2 (mergeable), but overall range 4 > 2ε → min 2 pieces."
    },

    # 5) Long plateau with a narrow spike: width doesn’t matter for L∞
    {
        "name": "plateau_with_narrow_spike",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (4.0, 0.0), (4.000001, 5.0), (4.000002, 0.0), (8.0, float('inf'))],
        "epsilon": 2.0,
        "expected_min_pieces": 2,
        "notes": "Spike height 5 → cannot fit with plateaus since 5 > 2ε=4."
    },

    # 6) Duplicate adjacent values should coalesce even with ε = 0
    {
        "name": "adjacent_duplicates_collapse",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.0), (2.0, 1.0), (5.0, 1.0), (9.0, float('inf'))],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Three adjacent identical levels → one piece when merged."
    },

    # 7) Gradual staircase; small steps allow some merging but not all
    {
        "name": "staircase_small_steps_partial_merge",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (2.0, 0.4), (4.0, 0.8), (6.0, 1.2), (8.0, float('inf'))],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "notes": "Overall range 1.2 > 2ε=1.0; but first three fit in one block, last level separate."
    },

    # 8) Negative large magnitudes; subset mergeable, overall not
    {
        "name": "negatives_large_magnitude_mixed",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -100.0), (3.0, -99.0), (6.0, -101.0), (9.0, float('inf'))],
        "epsilon": 0.75,
        "expected_min_pieces": 2,
        "notes": "All-range=2 > 2ε=1.5; {-100,-99} merge; {-101} separate."
    },

    # 9) Tiny interval in the middle with a huge jump (numerical stability)
    {
        "name": "tiny_middle_interval_huge_jump",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 10.0), (1.0 + 1e-12, 0.0), (2.0, float('inf'))],
        "epsilon": 4.9,
        "expected_min_pieces": 2,
        "notes": "Jump 10 > 2ε=9.8 → must split, despite vanishing width."
    },

    # 10) Very large ε collapses a wild signal to one piece
    {
        "name": "huge_epsilon_collapse_all",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -3.0), (1.0, 7.0), (2.5, 1.0), (5.0, -4.0), (9.0, 6.0), (12.0, float('inf'))],
        "epsilon": 5.0,
        "expected_min_pieces": 1,
        "notes": "Overall range 10 ≤ 2ε=10 → a single constant works (tight boundary case)."
    },
]

#Iteration24
test_cases24 = [
    # 1) Constant everywhere → should collapse to 1 piece even with ε=0.
    {
        "name": "All-constant (ε=0 ⇒ 1 piece)",
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[10,5],[20,5],[30,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Range=0 ≤ 2ε ⇒ entire domain by one constant."
    },

    # 2) Two far-apart plateaus, ε just too small for 1 piece.
    {
        "name": "Two-level split, ε just-insufficient",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,float('inf')]],
        "epsilon": 4.9,
        "expected_min_pieces": 2,
        "notes": "Range=10 > 2ε=9.8 ⇒ need 2 pieces."
    },

    # 3) Alternating with ε exactly at the threshold for 1 piece.
    {
        "name": "Alternating 0-10-0 at threshold",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,0],[3,float('inf')]],
        "epsilon": 5.0,
        "expected_min_pieces": 1,
        "notes": "Range=10 = 2ε ⇒ 1 piece allowed (equality)."
    },

    # 4) Redundant boundaries (equal adjacent values) with ε=0: check collapse of redundant cuts.
    {
        "name": "Redundant equal-adjacent plateaus (ε=0)",
        "pc_fx": [[-float('inf'), float('inf')],[0,2],[1,2],[2,3],[3,3],[4,2],[5,2],[6,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "notes": "Actual runs are 2 | 3 | 2 ⇒ 3 pieces; redundant internal boundaries shouldn’t inflate count."
    },

    # 5) Narrow spike in the middle that forces a dedicated piece when ε just too small.
    {
        "name": "Central spike forces 3 pieces",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,0],[2,100],[3,0],[4,0],[5,float('inf')]],
        "epsilon": 49.9,
        "expected_min_pieces": 3,
        "notes": "Spike range with neighbors is 100 > 2ε=99.8 ⇒ spike must stand alone."
    },

    # 6) Monotone ramp; ε big enough to merge into two windows by range≤2ε.
    {
        "name": "Monotone ramp merges into 2 blocks",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,2],[2,4],[3,6],[4,8],[5,float('inf')]],
        "epsilon": 2.0,
        "expected_min_pieces": 2,
        "notes": "Blocks [0,2,4] (range=4) and [6,8] (range=2). 2ε=4 ⇒ 2 pieces."
    },

    # 7) Fine-grained ramp; ε allows windows of range≤2 so expect 3 groups.
    {
        "name": "Fine ramp with 2ε=2 ⇒ three groups",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 3,
        "notes": "Groups [0,1,2], [3,4,5], [6]; each has range≤2ε=2."
    },

    # 8) Greedy trap check: better to split as [0,4] and [1,5] than 3+ pieces.
    {
        "name": "Oscillation pairs into 2 pieces",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,4],[2,1],[3,5],[4,float('inf')]],
        "epsilon": 2.0,
        "expected_min_pieces": 2,
        "notes": "Partition [0,4] (range=4) and [1,5] (range=4); 2ε=4 ⇒ 2 pieces total."
    },

    # 9) Negative values; exact threshold equality permits 1 piece.
    {
        "name": "Negative range at equality threshold",
        "pc_fx": [[-float('inf'), float('inf')],[0,-3],[1,1],[2,-1],[3,float('inf')]],
        "epsilon": 2.0,
        "expected_min_pieces": 1,
        "notes": "Global range max−min=1−(−3)=4 = 2ε ⇒ 1 piece ok."
    },

    # 10) ε=0 baseline: all values distinct ⇒ must match every change.
    {
        "name": "Zero epsilon ⇒ match every change",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 4,
        "notes": "Distinct values ⇒ each interval must be separate under ε=0."
    },
]

#Iteration25
test_cases25 = [
    {
        "name": "T1_constant_all_merge_even_eps0",
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[10,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "Already constant; ε=0 still allows 1 piece."
    },
    {
        "name": "T2_two_levels_exact_2epsilon_mergable",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[5,2],[10,float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "note": "Jump = 2 equals 2ε ⇒ choose midpoint (1.0) to be within ε of both."
    },
    {
        "name": "T3_two_levels_just_over_2epsilon_not_mergable",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[5,2.1],[10,float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "note": "Jump = 2.1 > 2ε ⇒ cannot merge; need 2 pieces."
    },
    {
        "name": "T4_many_small_oscillations_global_range_within_2epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,-0.4],[1,0.3],[2,-0.2],[3,0.4],[4,-0.1],[5,0.2],
                  [6,float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "note": "All values lie in [-0.4,0.4]; total range 0.8 ≤ 2ε=1 ⇒ 1 piece."
    },
    {
        "name": "T5_alternating_high_low_forces_many_pieces",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,0],[1,10],[2,0],[3,10],[4,0],[5,10],[6,0],
                  [7,float('inf')]],
        "epsilon": 2.0,
        "expected_min_pieces": 7,
        "note": "Adjacent jumps = 10 > 2ε=4 ⇒ no merges at all (n pieces)."
    },
    {
        "name": "T6_thin_spike_requires_separate_piece",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,0],[5,100],[5.001,0],[10,float('inf')]],
        "epsilon": 10.0,
        "expected_min_pieces": 2,
        "note": "Spike height 100 > 2ε=20 ⇒ spike isolated; flats merge to one piece."
    },
    {
        "name": "T7_staircase_clusters_into_two_groups",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,0.0],[2,1.4],[4,2.8],[6,4.2],[8,float('inf')]],
        "epsilon": 0.8,
        "expected_min_pieces": 2,
        "note": "Adjacent gaps 1.4 ≤ 2ε=1.6; overall span 4.2 ⇒ two clusters: {0,1.4} and {2.8,4.2}."
    },
    {
        "name": "T8_negatives_and_zero_two_groups",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,-5],[3,-4.2],[6,0],[9,float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 2,
        "note": "(-5,-4.2) merge (Δ=0.8≤1.2); adding 0 would exceed 2ε ⇒ two pieces."
    },
    {
        "name": "T9_redundant_splits_same_value_and_runs",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,1],[2,1],[3,1],[4,2],[5,2],[6,1],[7,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "note": "ε=0 collapses consecutive equal-valued splits ⇒ runs (1)|(2)|(1) ⇒ 3 pieces."
    },
    {
        "name": "T10_huge_epsilon_everything_merges",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0,-50],[2,20],[5,-10],[8,40],[10,float('inf')]],
        "epsilon": 1_000_000.0,
        "expected_min_pieces": 1,
        "note": "Trivial stress: ε so large that 1 piece always feasible."
    },
]

#Iteration26
test_cases26 = [
    # 1) All-equal values, ε=0 ⇒ everything should merge to ONE piece.
    {
        "name": "all_equal_eps0_one_piece",
        "pc_fx": [[-float('inf'), float('inf')],[0,5],[1,5],[2,5],[3,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "rationale": "Range=0 ≤ 2ε=0 → one block over all."
    },

    # 2) ε=0 with actual value changes ⇒ must keep every change as its own piece.
    {
        "name": "strict_exact_eps0_all_changes",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,1],[4,float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 4,
        "rationale": "Any difference at ε=0 is illegal to merge."
    },

    # 3) Very large ε that spans a wide range ⇒ everything can merge.
    {
        "name": "huge_eps_all_merge",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,-5],[3,8],[4,float('inf')]],
        "epsilon": 7.5,  # range=15, 2ε=15
        "expected_min_pieces": 1,
        "rationale": "Range=15, 2ε=15 → borderline merge of all into one."
    },

    # 4) Just-below-threshold ε ⇒ cannot merge all, but can merge into two contiguous blocks.
    {
        "name": "just_below_threshold_split2",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,-5],[3,8],[4,float('inf')]],
        "epsilon": 7.4,  # 2ε=14.8 < 15
        "expected_min_pieces": 2,
        "rationale": "Split [0,10] and [-5,8]: each block range ≤ 2ε."
    },

    # 5) Borderline (cannot all merge): need two blocks.
    {
        "name": "borderline_two_blocks",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,3],[2,6],[3,float('inf')]],
        "epsilon": 2.9,  # 2ε=5.8 < range 6
        "expected_min_pieces": 2,
        "rationale": "Merge [0,3] (range 3) + [6] → two pieces."
    },

    # 6) Exact-threshold ε: now all can merge into one.
    {
        "name": "borderline_all_merge",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,3],[2,6],[3,float('inf')]],
        "epsilon": 3.0,  # 2ε=6 = range
        "expected_min_pieces": 1,
        "rationale": "Range=6, 2ε=6 → all-in-one is feasible."
    },

    # 7) Thin spike: length doesn’t matter in L∞, so isolate the spike unless ε is big enough.
    {
        "name": "narrow_spike_needs_isolation",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,0],[2,5],[3,0],[4,0],[5,float('inf')]],
        "epsilon": 2.4,  # 2ε=4.8 < spike gap 5
        "expected_min_pieces": 3,
        "rationale": "Must split as [0,0], [5], [0,0]."
    },

    # 8) Monotone staircase with small ε: forces multiple blocks by cumulative range.
    {
        "name": "staircase_small_eps",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,1],[2,2],[3,3],[4,4],[5,float('inf')]],
        "epsilon": 0.9,  # 2ε=1.8
        "expected_min_pieces": 3,
        "rationale": "Optimal partition: [0,1], [2,3], [4]."
    },

    # 9) Compact oscillations but just-too-small ε: needs exactly two pieces.
    {
        "name": "tight_band_needs_two",
        "pc_fx": [[-float('inf'), float('inf')],[0,1.00],[1,1.20],[2,0.90],[3,1.10],[4,1.05],[5,0.95],[6,float('inf')]],
        "epsilon": 0.14,  # 2ε=0.28 < global range 0.30
        "expected_min_pieces": 2,
        "rationale": "Feasible as [1.00,1.20] and [0.90,1.10,1.05,0.95]."
    },

    # 10) Alternating highs/lows defeats naive greedy merging for small ε.
    {
        "name": "alternating_high_low_small_eps",
        "pc_fx": [[-float('inf'), float('inf')],[0,0],[1,10],[2,0],[3,10],[4,0],[5,float('inf')]],
        "epsilon": 4.9,  # 2ε=9.8 < gap 10
        "expected_min_pieces": 5,
        "rationale": "No block can contain both 0 and 10 → every segment stands alone."
    },
]

#Iteration27
test_cases27 = [
    # 1) Constant function, ε = 0 → everything should merge to one piece
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 5], [1, 5], [3, 5], [10, 5],
                  [12, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "All values identical; with ε=0 the whole domain is feasible with a single constant."
    },

    # 2) Exactly on the merge boundary: max-min = 2ε → still mergeable
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 1.0], [2, 2.5], [5, 1.8], [7, 2.5],
                  [9, float("inf")]],
        "epsilon": 0.75,  # 2ε = 1.5; range = 2.5 - 1.0 = 1.5 → mergeable
        "expected_min_pieces": 1,
        "note": "Borderline case: range equals 2ε, should still be a single piece."
    },

    # 3) Just over the boundary: max-min = 2ε + tiny → must split
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 1.01], [2, 0.0],
                  [3, float("inf")]],
        "epsilon": 0.5,   # 2ε = 1.0; range = 1.01 → cannot cover all with one value
        "expected_min_pieces": 2,
        "note": "Near-miss. Needs at least two segments because range exceeds 2ε by 0.01."
    },

    # 4) Tight oscillation fully within 2ε → should collapse to one
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 1.00], [1, 0.85], [2, 1.20], [3, 0.95], [4, 1.10],
                  [5, float("inf")]],
        "epsilon": 0.20,  # 2ε = 0.4; range = 1.20 - 0.85 = 0.35 → OK
        "expected_min_pieces": 1,
        "note": "All values lie in a width-0.35 band; 2ε is 0.4."
    },

    # 5) Alternating large jumps beyond 2ε → nothing merges
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0], [4, 0.0],
                  [5, float("inf")]],
        "epsilon": 0.49,  # 2ε = 0.98; adjacent pairs differ by 2.0
        "expected_min_pieces": 5,
        "note": "Each piece must stand alone; differences are too large to merge."
    },

    # 6) Long plateau with one outlier spike → forces a split around the spike
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 5.0], [2, 5.1], [4, 9.0], [5, 5.0], [8, 5.2],
                  [10, float("inf")]],
        "epsilon": 0.3,   # 2ε = 0.6; spike at 9.0 cannot merge with ~5.x plateau
        "expected_min_pieces": 3,
        "note": "Plateau (≈5) — spike (9) — plateau (≈5) requires three segments."
    },

    # 7) Gradual drift that exceeds the band → minimal 3 segments
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 0.3], [2, 0.6], [3, 0.9], [4, 1.2],
                  [5, float("inf")]],
        "epsilon": 0.2,   # 2ε = 0.4
        "expected_min_pieces": 3,
        "note": "Optimal partition: [0,0.3] | [0.6,0.9] | [1.2]."
    },

    # 8) Crossing zero but still within a wide band → can merge all
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, -0.4], [1, -0.2], [2, 0.0], [3, 0.2], [4, 0.4],
                  [6, float("inf")]],
        "epsilon": 0.4,   # 2ε = 0.8; range = 0.4 - (-0.4) = 0.8 → OK
        "expected_min_pieces": 1,
        "note": "Range equals 2ε; still mergeable into one piece."
    },

    # 9) Highly nonuniform intervals (length shouldn’t matter), values mergeable
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0.0, 10.0], [0.0001, 10.2], [100.0, 10.1], [1000.0, 10.05],
                  [1000.1, float("inf")]],
        "epsilon": 0.15,  # 2ε = 0.30; range = 10.2 - 10.0 = 0.2 → OK
        "expected_min_pieces": 1,
        "note": "Checks that spacing of x’s doesn’t affect L∞ feasibility."
    },

    # 10) ε = 0 exactness: only consecutive equal values can merge (runs)
    {
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 1], [1, 1], [2, 2], [3, 2], [4, 1], [5, 1],
                  [6, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "note": "Runs: (1,1) | (2,2) | (1,1) → three segments."
    },
]

#Iteration28
def make_pc(values, start=0.0, step=1.0):
    """Convenience helper to build pc_fx with unit-width pieces."""
    out = [[-float('inf'), float('inf')]]
    x = start
    for v in values:
        out.append([x, float(v)])
        x += step
    out.append([x, float('inf')])
    return out

test_cases28 = [
    {
        "name": "constant_exact",
        "pc_fx": make_pc([5, 5, 5, 5]),
        "epsilon": 0.0,
        "expected_min_pieces": None,  # filled below
        "notes": "All equal; ε=0 should still compress to 1 piece."
    },
    {
        "name": "small_jump_mergeable",
        "pc_fx": make_pc([0, 0.5, 0.2, 0.4]),
        "epsilon": 0.3,  # range=0.5 ≤ 2ε=0.6
        "expected_min_pieces": None,
        "notes": "All values within range 0.5; merge into a single piece."
    },
    {
        "name": "single_big_jump",
        "pc_fx": make_pc([0, 3]),
        "epsilon": 0.9,  # diff=3 > 2ε=1.8
        "expected_min_pieces": None,
        "notes": "One large jump forces at least two pieces."
    },
    {
        "name": "alternating_extremes",
        "pc_fx": make_pc([0, 4, 0, 4, 0]),
        "epsilon": 1.9,  # diff=4 > 2ε=3.8
        "expected_min_pieces": None,
        "notes": "High/low alternation; no merges possible anywhere."
    },
    {
        "name": "single_spike",
        "pc_fx": make_pc([1, 1, 1, 10, 1, 1]),
        "epsilon": 0.6,  # spike isolates a middle piece
        "expected_min_pieces": None,
        "notes": "Outlier spike splits into left, spike, right."
    },
    {
        "name": "narrow_high_still_merge",
        "pc_fx": make_pc([0, 5, 0]),
        "epsilon": 3.0,  # range=5 ≤ 2ε=6
        "expected_min_pieces": None,
        "notes": "Very sharp but allowable with large ε; all merge to 1."
    },
    {
        "name": "negative_mixture",
        "pc_fx": make_pc([-2, -2.5, -2.1, -3.9]),
        "epsilon": 0.5,  # first three can merge; last cannot join
        "expected_min_pieces": None,
        "notes": "Mixed negatives check range logic and ordering."
    },
    {
        "name": "large_scale_precision",
        "pc_fx": make_pc([1_000_000.0, 1_000_000.4, 1_000_000.8]),
        "epsilon": 0.3,  # first two merge; adding third breaks range
        "expected_min_pieces": None,
        "notes": "Large magnitudes to expose precision/float handling."
    },
    {
        "name": "staircase",
        "pc_fx": make_pc([0, 0.9, 1.8, 2.7, 3.6]),
        "epsilon": 1.0,  # greedy grouping by value range
        "expected_min_pieces": None,
        "notes": "Monotone staircase; should group into two blocks."
    },
    {
        "name": "boundary_equal_2eps",
        "pc_fx": make_pc([0, 2, 4]),
        "epsilon": 1.0,  # exact boundary: diff=2 == 2ε
        "expected_min_pieces": None,
        "notes": "Tight boundary case; first two merge, last separates."
    },
]

#Iteration29
from math import inf
test_cases29 = [
    # 1) Trivially constant (should be 1 piece for any ε >= 0)
    {
        "name": "Constant function",
        "pc_fx": [[-inf, inf],[0, 3],[5, 3],[9, 3],[12, inf]],
        "epsilon": 0.0,
    },

    # 2) Jump exactly at the threshold 2ε → still mergeable into 1
    # y-range = 1.0, ε = 0.5 → 2ε = 1.0 ⇒ expected 1
    {
        "name": "Exact threshold merge (max-min == 2ε)",
        "pc_fx": [[-inf, inf],[0, 0.0],[1, 1.0],[2, inf]],
        "epsilon": 0.5,
    },

    # 3) Just over the threshold → must split
    # y-range = 1.01, ε = 0.5 → 2ε = 1.0 ⇒ expected 2
    {
        "name": "Just over threshold (max-min > 2ε)",
        "pc_fx": [[-inf, inf],[0, 0.0],[1, 1.01],[2, inf]],
        "epsilon": 0.5,
    },

    # 4) Many tiny oscillations but all within a 1-wide band → merge to 1
    # range = 1.0, ε = 0.5 → 2ε = 1.0 ⇒ expected 1
    {
        "name": "Long within-band oscillation",
        "pc_fx": [[-inf, inf],[0, 0.0],[1, 0.9],[2, 0.2],[3, 1.0],[4, 0.1],[5, 0.8],[6, inf]],
        "epsilon": 0.5,
    },

    # 5) Alternating big spikes → every piece must stand alone
    # differences are 3 with ε=1 → 2ε=2 < 3 ⇒ expected = number of pieces (=4)
    {
        "name": "Alternating large spikes",
        "pc_fx": [[-inf, inf],[0, 0],[1, 3],[2, 0],[3, 3],[4, inf]],
        "epsilon": 1.0,
    },

    # 6) Drift within band, single outlier, then back within band
    # First three (0,0.2,0.4) merge; outlier 2.6 alone; last 0.5 alone or merged with previous?
    # 0.5 vs 2.6 → span=2.1 with ε=0.5 → 2ε=1 → not mergeable ⇒ expected 3
    {
        "name": "Single outlier splits two large mergeable groups",
        "pc_fx": [[-inf, inf],[0, 0.0],[1, 0.2],[2, 0.4],[3, 2.6],[4, 0.5],[5, inf]],
        "epsilon": 0.5,
    },

    # 7) Tiny-width huge spike (measure ~0 but matters for L∞)
    # Surrounding 0-plateaus can merge; spike must be separate ⇒ expected 2
    {
        "name": "Needle spike of tiny width",
        "pc_fx": [[-inf, inf],[0.0, 0.0],[1.0, 10.0],[1.0 + 1e-9, 0.0],[2.0, inf]],
        "epsilon": 0.1,
    },

    # 8) Negative values with equality edge cases
    # Values within [-1, 0] band → range = 1.0, ε=0.5 → 2ε=1.0 ⇒ all merge to 1
    {
        "name": "Negative plateau with boundary equality",
        "pc_fx": [[-inf, inf],[0, -1.0],[2, -0.3],[5, -0.7],[9, 0.0],[11, inf]],
        "epsilon": 0.5,
    },

    # 9) Slow ramp: individual steps small, total drift large → expect a few groups
    # y: 0,0.4,0.8,1.2,1.6 with ε=0.5 (2ε=1.0)
    # Greedy: [0..0.8] merge (range 0.8), 1.2 doesn't fit there (now range 1.2), so cut.
    # Then [1.2,1.6] merge (range 0.4). ⇒ expected 2
    {
        "name": "Ramp causing limited number of groups",
        "pc_fx": [[-inf, inf],[0, 0.0],[1, 0.4],[2, 0.8],[3, 1.2],[4, 1.6],[5, inf]],
        "epsilon": 0.5,
    },

    # 10) Symmetric hill within two-epsilon windows only locally
    # y: 0,1,2,1,0 with ε=0.5 (2ε=1.0)
    # Best is [0,1], [2,1], [0] → expected 3
    {
        "name": "Hill pattern needs three groups",
        "pc_fx": [[-inf, inf],[0, 0.0],[1, 1.0],[2, 2.0],[3, 1.0],[4, 0.0],[5, inf]],
        "epsilon": 0.5,
    },
]
#Iteration30
# Each testcase is a dict:
# {
#   "name": str,
#   "pc_fx": list[list[float, float]],
#   "epsilon": float,
#   "expected_min_pieces": int,   # ground truth under L∞
#   "notes": str
# }
test_cases30 = [
    # 1) Perfectly flat → should compress to 1 piece even with ε=0
    {
        "name": "Flat function, ε=0",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 3.0], [5.0, 3.0], [10.0, 3.0], [15.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "All values identical; merge all intervals."
    },

    # 2) Single big jump; ε too small to cover both levels with one constant
    {
        "name": "Single jump not coverable by ε",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [5.0, 10.0], [10.0, float('inf')]],
        "epsilon": 4.9,
        "expected_min_pieces": 2,
        "notes": "Range=10 ⇒ best single constant has max error 5 > 4.9."
    },

    # 3) Checkerboard alternation; ε just below 0.5 prevents any merges
    {
        "name": "Alternating 0/1, ε=0.49",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.0], [2.0, 0.0], [3.0, 1.0], [4.0, 0.0],
                  [5.0, float('inf')]],
        "epsilon": 0.49,
        "expected_min_pieces": 5,
        "notes": "Adjacent levels differ by 1; need ε≥0.5 to merge."
    },

    # 4) Narrow tall spike cannot be ignored under L∞
    {
        "name": "Tall spike between flats, ε below half-range",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.0], [1.001, 100.0], [1.002, 0.0],
                  [3.0, float('inf')]],
        "epsilon": 49.0,
        "expected_min_pieces": 3,
        "notes": "Spike 0↔100 forces its own piece (width irrelevant in sup-norm)."
    },

    # 5) Monotone ladder; ε allows at most 2-step groups
    {
        "name": "Monotone steps, ε=1",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 2.0], [2.0, 4.0], [3.0, 6.0], [4.0, 8.0],
                  [5.0, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 3,
        "notes": "Max group with range≤2 ⇒ groups {0,2}, {4,6}, {8}."
    },

    # 6) Two long runs at -5 and +5; ε just below 5 forbids merging runs
    {
        "name": "Two symmetric runs, ε=4.9",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -5.0], [1.0, -5.0], [2.0, 5.0], [3.0, 5.0],
                  [4.0, float('inf')]],
        "epsilon": 4.9,
        "expected_min_pieces": 2,
        "notes": "Runs merge internally; cannot merge across ±5 gap."
    },

    # 7) Huge ε should collapse everything to 1 piece
    {
        "name": "Everything merges with huge ε",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [2.0, 10.0], [3.0, -7.0], [5.0, 15.0],
                  [7.5, float('inf')]],
        "epsilon": 1e6,
        "expected_min_pieces": 1,
        "notes": "Sanity check: algorithm should return a single piece."
    },

    # 8) ε=0 on multiple equal-value runs → compress to number of runs
    {
        "name": "Exact fit with repeated values, ε=0",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0], [1.0, 1.0], [2.0, 2.0], [3.0, 2.0], [4.0, 2.0],
                  [5.0, 1.0], [6.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "notes": "Runs: 1s, then 2s, then 1s ⇒ 3."
    },

    # 9) Very large magnitudes with tiny differences; ε just above half-range
    {
        "name": "Numerical stability: ~1e9 scale, ε=0.6",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1_000_000_000.0],
                  [1.0, 1_000_000_001.0],
                  [2.0, 1_000_000_000.2],
                  [3.0, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 1,
        "notes": "Range=1 ⇒ half-range=0.5 < ε, so all merge."
    },

    # 10) Extremely short middle interval; sup-norm still forces 3 pieces
    {
        "name": "Tiny middle interval forces split, ε=4.9",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [0.000001, 10.0], [0.000002, 0.0], [1.0, float('inf')]],
        "epsilon": 4.9,
        "expected_min_pieces": 3,
        "notes": "Width doesn’t matter for L∞; small blip must be isolated."
    },
]
