#27 Sept 4:12PM Copilot  (Chat mode: Think Deeper) (took 45mins)
test_cases1 = [
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 2], [5, 2], [10, float("inf")]],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Single piece across domain returns one piece."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 2.0], [5, 2.1], [10, float("inf")]],
        "epsilon": 0.05,
        "expected_min_pieces": 1,
        "description": "Two adjacent pieces with difference 0.1 merge when 2*epsilon equals 0.1."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 2.0], [5, 2.11], [10, float("inf")]],
        "epsilon": 0.05,
        "expected_min_pieces": 2,
        "description": "Two adjacent pieces with difference 0.11 cannot merge when 2*epsilon is 0.1."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 0.2], [2, 0.4], [3, float("inf")]],
        "epsilon": 0.1,
        "expected_min_pieces": 2,
        "description": "Three monotone pieces where adjacent pairs can merge but the triple cannot, optimal split is two pieces."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0], [4, float("inf")]],
        "epsilon": 0.6,
        "expected_min_pieces": 4,
        "description": "Alternating high/low values with epsilon too small to merge any neighbors, requires all original pieces."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 0.0], [2, 5.0], [3, 0.0], [4, float("inf")]],
        "epsilon": 2.0,
        "expected_min_pieces": 3,
        "description": "Narrow spike forces its own piece; contiguous zero regions merge independently, yielding three pieces."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 1.0], [1, 2.0], [2, 3.0], [3, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "description": "Zero tolerance requires exact reproduction and returns original number of pieces."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1e-12], [2, float("inf")]],
        "epsilon": 5e-13,
        "expected_min_pieces": 1,
        "description": "Floating point borderline case where difference equals 2*epsilon, merge should succeed."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 1.0], [5, 0.0], [5, 1.0], [10, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Zero-length middle piece at boundary should not prevent merging of surrounding values when allowable."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 10.0], [2, -5.0], [3, float("inf")]],
        "epsilon": 8.0,
        "expected_min_pieces": 1,
        "description": "Large epsilon merges widely varying values into a single piece."
    }
]
test_cases2 = [
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 5], [10, float("inf")]],
        "epsilon": 0.1,
        "expected_pieces": 1,
        "note": "Single piece (already constant)."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.0], [2, float("inf")]],
        "epsilon": 0.5,
        "expected_pieces": 1,
        "note": "Two adjacent pieces with |y1 - y2| = 2*epsilon (boundary equality)."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.0], [2, 2.0], [3, float("inf")]],
        "epsilon": 0.5,
        "expected_pieces": 2,
        "note": "Chain where adjacent pairs can merge but the full triple cannot; optimal = 2 pieces."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [0.001, 0.8], [100, 1.6], [1000, float("inf")]],
        "epsilon": 0.8,
        "expected_pieces": 1,
        "note": "Very uneven interval lengths; merge depends only on value range not lengths."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, -2.0], [5, 2.0], [10, float("inf")]],
        "epsilon": 2.0,
        "expected_pieces": 1,
        "note": "Negative and positive values with |min-max| = 4 = 2*epsilon (sign crossing)."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 2e-9 + 1e-12], [2, float("inf")]],
        "epsilon": 1e-9,
        "expected_pieces": 2,
        "note": "Floating-point precision: diff is just above 2*epsilon, should NOT merge."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.9], [2, 0.0], [3, float("inf")]],
        "epsilon": 1.0,
        "expected_pieces": 1,
        "note": "Middle value between equal extremes; global merge possible because max-min <= 2*epsilon."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 3.0], [2, 6.0], [3, float("inf")]],
        "epsilon": 1.5,
        "expected_pieces": 2,
        "note": "Adjacent pairs meet boundary (|diff| = 3 = 2*epsilon) but full block cannot merge; tests greedy pitfalls."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 1.0], [1, 1.0], [2, 2.0], [3, float("inf")]],
        "epsilon": 0.0,
        "expected_pieces": 2,
        "note": "Zero tolerance: only exactly-equal adjacent pieces should merge."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, -1000.0], [1, 0.0], [2, 1000.0], [3, 42.0], [4, -500.0], [5, float("inf")]],
        "epsilon": 1e6,
        "expected_pieces": 1,
        "note": "Huge epsilon that should collapse all pieces to one."
    }
]
test_cases3 = [
    # 1. Uniform values exactly match epsilon zero -> should merge to 1 piece
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 5], [1, 5], [2, 5], [3, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "All piece values identical and epsilon 0, single-piece optimal"
    },

    # 2. Alternating values with epsilon zero -> no merges allowed
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 1], [1, 2], [2, 1], [3, 2], [4, 1], [5, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 5,
        "description": "Alternating values and epsilon 0, algorithm must keep every piece"
    },

    # 3. Small epsilon allowing pairwise merges but not triple merges
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.0], [2, 2.0], [3, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Values [0,1,2] with epsilon 0.5: optimal groups [0,1] and [2]"
    },

    # 4. Oscillating values where adjacent pairs merge but full triple fails
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.1], [2, 2.0], [3, float("inf")]],
        "epsilon": 0.55,
        "expected_min_pieces": 2,
        "description": "Adjacent ranges small (<=2*epsilon) but full range exceeds 2*epsilon"
    },

    # 5. Very large epsilon that allows merging all pieces into one
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 100.0], [2, 50.0], [3, float("inf")]],
        "epsilon": 60.0,
        "expected_min_pieces": 1,
        "description": "Large epsilon permits a single constant approximant"
    },

    # 6. Zero length interval inside sequence with an outlier value
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 5.0], [1, 100.0], [1, 5.0], [2, float("inf")]],
        "epsilon": 10.0,
        "expected_min_pieces": 3,
        "description": "Zero-length piece with extreme value prevents merging surrounding pieces"
    },

    # 7. Negative and positive values around zero
    {
        "pc_fx": [[-float("inf"), float("inf")], [-1, -1.0], [0, 0.0], [1, 1.0], [2, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Values [-1,0,1] with epsilon 0.5, best is [ -1,0 ] and [1]"
    },

    # 8. Floating point precision edge where 2*epsilon equals the value range
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1e-12, 1e-12], [2e-12, 2e-12], [3, float("inf")]],
        "epsilon": 1e-12,
        "expected_min_pieces": 1,
        "description": "Tiny values where 2*epsilon equals range, must accept single merge"
    },

    # 9. Increasing sequence where optimal grouping is nontrivial
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.0], [2, 2.0], [3, 3.0], [4, 4.0], [5, float("inf")]],
        "epsilon": 0.6,
        "expected_min_pieces": 3,
        "description": "Values [0,1,2,3,4] with epsilon 0.6 -> optimal partition example [0,1],[2,3],[4]"
    },

    # 10. Case with multiple optimal partitions but same minimal piece count
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.0], [2, 2.0], [3, 1.0], [4, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Values [0,1,2,1] epsilon 0.5; multiple valid 2-piece partitions exist"
    }
]
test_cases4 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, float('inf')]],
        "epsilon": 0.0,
        "description": "Single piece over finite interval; already constant (should be 1).",
        "expected_min_pieces": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, float('inf')]],
        "epsilon": 0.0,
        "description": "Two adjacent identical values; algorithm must merge identical neighbors (should be 1).",
        "expected_min_pieces": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "Alternating values 0,2,0 where a single constant (1) attains error exactly epsilon (should be 1).",
        "expected_min_pieces": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Monotone staircase 0,1,2,3 where optimal grouping is two pairs; greedy local choices can be tested (should be 2).",
        "expected_min_pieces": 2
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, float('inf')]],
        "epsilon": 4.0,
        "description": "Sharp spike in the middle that prevents merging across peak (should remain 3).",
        "expected_min_pieces": 3
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [-100, 1], [0, 1], [100, 2], [200, float('inf')]],
        "epsilon": 0.5,
        "description": "Large intervals with first two equal values and a different far-right value; tests merging adjacent identical pieces across wide ranges (should be 2).",
        "expected_min_pieces": 2
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1e-9], [2, float('inf')]],
        "epsilon": 5e-10,
        "description": "Numerical precision edge: tiny difference within tolerance; algorithm must handle floating precision (should be 1).",
        "expected_min_pieces": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.2], [2, 0.1], [3, 0.2], [4, 0.15], [5, float('inf')]],
        "epsilon": 0.1,
        "description": "Small oscillations where full merge is impossible but a two-piece grouping exists; tests grouping choices (should be 2).",
        "expected_min_pieces": 2
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -2], [1, -1], [2, -2], [3, float('inf')]],
        "epsilon": 0.5,
        "description": "Negative values symmetric around a higher middle value; tests sign handling and merging of first two (should be 2).",
        "expected_min_pieces": 2
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, float('inf')]],
        "epsilon": 1.0,
        "description": "Repeated 0/2 oscillation where optimal grouping is pairing neighbors into three pieces; exposes whether algorithm finds global optimal 3-piece partition (should be 3).",
        "expected_min_pieces": 3
    }
]
test_cases5 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.0,
        "description": "Single piece only, trivial merge to 1 piece",
        "expected_min_pieces": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.0], [2, 2.0], [3, float('inf')]],
        "epsilon": 0.0,
        "description": "Multiple pieces with identical values, zero tolerance should still merge all",
        "expected_min_pieces": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 3.0], [2, 0.0], [3, 3.0], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Alternating high/low values with small epsilon so no adjacent merges possible",
        "expected_min_pieces": 4
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 5.0], [2, 2.0], [3, 4.0], [4, float('inf')]],
        "epsilon": 3.0,
        "description": "Large epsilon that can merge all pieces into one",
        "expected_min_pieces": 1
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 3.0], [2, 6.0], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "Boundary case where an adjacent pair difference equals 2*epsilon (allowed), forcing grouping of first two only",
        "expected_min_pieces": 2
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.9], [2, 1.8], [3, 2.7], [4, float('inf')]],
        "epsilon": 0.95,
        "description": "Increasing small steps where first three can merge but the last must remain separate",
        "expected_min_pieces": 2
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 1.0], [3, 3.0], [4, float('inf')]],
        "epsilon": 0.5,
        "description": "Non-monotonic values requiring a middle merge but first and last remain separate",
        "expected_min_pieces": 3
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.5000000001], [2, 3.0], [3, float('inf')]],
        "epsilon": 0.75,
        "description": "Floating point precision edge where first two differ by just over 2*epsilon",
        "expected_min_pieces": 3
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.9], [2, 3.8], [3, 5.7], [4, 7.6], [5, float('inf')]],
        "epsilon": 0.95,
        "description": "Long sequence where optimal grouping is in pairs except a final leftover",
        "expected_min_pieces": 3
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1e-12], [2, float('inf')]],
        "epsilon": 0.0,
        "description": "Zero epsilon with tiny nonzero difference so no merge due to strict L-infinity tolerance",
        "expected_min_pieces": 2
    }
]
test_cases6 = [
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 3.0], [10.0, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },  # Single constant piece; always optimal = 1

    {
        "name": "two_identical_zero_epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 5.0], [2.0, 5.0], [4.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1
    },  # Adjacent pieces identical and epsilon=0; must merge into one

    {
        "name": "boundary_merge_exact",
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 2.0], [1.0, 3.0], [2.0, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },  # Two pieces differ by exactly 2*epsilon (merge allowed)

    {
        "name": "four_merge_all",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [1.0, 0.9],
                  [2.0, 0.9],
                  [3.0, 0.0],
                  [4.0, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },  # Four-piece pattern where max-min <= 2*epsilon so all can be one piece

    {
        "name": "alternating_high_low",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [1.0, 10.0],
                  [2.0, 0.0],
                  [3.0, 10.0],
                  [4.0, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 4
    },  # Alternating extremes with small epsilon; no adjacent merges possible

    {
        "name": "monotonic_ramp_two_groups",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [1.0, 0.6],
                  [2.0, 1.2],
                  [3.0, 1.8],
                  [4.0, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 2
    },  # Increasing by uniform step: first three can merge (max-min=1.2 ≤ 2*eps), last stands alone

    {
        "name": "floating_precision_borderline",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [1.0, 0.3333333],
                  [2.0, 0.6666667],
                  [3.0, 1.0],
                  [4.0, float('inf')]],
        "epsilon": 0.1666667,
        "expected_min_pieces": 2
    },  # Tests floating precision on borderline intervals: expected partition into [0,0.3333333] and [0.6666667,1.0]

    {
        "name": "nontrivial_grouping_mid_peak",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0],
                  [1.0, 2.0],
                  [2.0, 1.5],
                  [3.0, 2.0],
                  [4.0, float('inf')]],
        "epsilon": 0.25,
        "expected_min_pieces": 2
    },  # First piece cannot join second, but last three can form one group (max-min=0.5 ≤ 2*eps)

    {
        "name": "large_epsilon_merge_all_extremes",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -1000.0],
                  [1.0, 0.0],
                  [2.0, 1000.0],
                  [3.0, float('inf')]],
        "epsilon": 1000.0,
        "expected_min_pieces": 1
    },  # Very large epsilon should allow merging wildly different values into one piece

    {
        "name": "tiny_values_zero_epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1e-12],
                  [1.0, 1e-12],
                  [2.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1
    }   # Very small identical values with epsilon=0; numerical equality case
]
test_cases7 = [
    {
        "name": "single_constant",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        "name": "adjacent_identical_values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [2, 5], [5, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 1
    },
    {
        "name": "merge_many_within_tolerance",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.8], [2, 0.2], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "boundary_equality_precision",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 1
    },
    {
        "name": "single_outlier_blocks_global_merge",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.0], [2, 10.0], [3, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2
    },
    {
        "name": "monotone_full_merge_with_exact_threshold",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, 3.0], [4, 4.0], [5, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 1
    },
    {
        "name": "alternating_high_low",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 3.0], [2, 0.0], [3, 3.0], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 4
    },
    {
        "name": "zero_length_middle_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 100.0], [1, 1.0], [2, float('inf')]],
        "epsilon": 0.5,
        "expected_pieces": 2
    },
    {
        "name": "very_large_epsilon_all_merge",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 50.0], [2, -40.0], [3, 100.0], [4, float('inf')]],
        "epsilon": 1000.0,
        "expected_pieces": 1
    },
    {
        "name": "pairwise_mergeable_but_not_global",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.9], [2, 3.8], [3, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2
    }
]
test_cases8 = [
    {
        "id": "single_piece_exact",
        "desc": "Single piece, epsilon 0 (requires exact match; algorithm should return 1 piece).",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [10, float('inf')]],
        "epsilon": 0.0
    },
    {
        "id": "merge_all_within_epsilon",
        "desc": "Three adjacent pieces whose values lie within epsilon when choosing the optimal constant; should merge into 1.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [2, 5.4], [4, 4.7], [6, float('inf')]],
        "epsilon": 0.5
    },
    {
        "id": "must_split_middle_outlier",
        "desc": "Middle piece is an outlier; optimal segmentation should keep middle piece separate.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 0.0], [3, float('inf')]],
        "epsilon": 0.5
    },
    {
        "id": "zero_length_piece",
        "desc": "Contains a zero-length piece (repeated breakpoint). Tests handling of empty intervals.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 7.0], [1, 6.0], [2, float('inf')]],
        "epsilon": 0.5
    },
    {
        "id": "epsilon_boundary_equal_allowed",
        "desc": "Piece values differ by exactly 2; epsilon equals 1 so merging into one constant yields max error = epsilon (should be allowed).",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, float('inf')]],
        "epsilon": 1.0
    },
    {
        "id": "very_large_epsilon_merge_everything",
        "desc": "Very large epsilon should allow merging all pieces into one constant regardless of values.",
        "pc_fx": [[-float('inf'), float('inf')], [0, -100.0], [1, 0.0], [2, 100.0], [3, float('inf')]],
        "epsilon": 1000.0
    },
    {
        "id": "alternating_high_low",
        "desc": "Alternating extreme values (0,10,0,10) with small epsilon; forces many pieces and tests nontrivial segmentation.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 0.0], [3, 10.0], [4, float('inf')]],
        "epsilon": 3.0
    },
    {
        "id": "non_monotonic_tricky",
        "desc": "Nonmonotonic sequence where local greedy merges can be suboptimal; checks global optimality.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.9], [2, 3.8], [3, float('inf')]],
        "epsilon": 1.5
    },
    {
        "id": "floating_point_precision",
        "desc": "Values that expose floating-point precision issues and boundary rounding behavior.",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.1], [1, 0.2], [2, 0.30000000000000004], [3, float('inf')]],
        "epsilon": 0.1
    },
    {
        "id": "many_small_pieces_mixed",
        "desc": "Larger number of small pieces with subtle value changes; tests performance and grouping decisions.",
        "pc_fx": [
            [-float('inf'), float('inf')],
            [0, 0.0], [1, 0.4], [2, 0.9], [3, 1.5], [4, 1.0],
            [5, 0.5], [6, 0.45], [7, 0.43], [8, 0.44], [9, 0.46],
            [10, float('inf')]
        ],
        "epsilon": 0.5
    }
]
test_cases9 = [
    {
        "id": 1,
        "name": "identical_adjacent_merge_exact",
        "pc_fx": [[-float("inf"), float("inf")], [0, 2], [1, 2], [2, float("inf")]],
        "epsilon": 0.0,
        "expected": 1
    },
    {
        "id": 2,
        "name": "borderline_three_equal_range",
        "pc_fx": [[-float("inf"), float("inf")], [0, 2], [1, 2.5], [2, 3], [3, float("inf")]],
        "epsilon": 0.5,
        "expected": 1
    },
    {
        "id": 3,
        "name": "pairwise_merge_but_not_global",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 1], [2, 2], [3, float("inf")]],
        "epsilon": 0.6,
        "expected": 2
    },
    {
        "id": 4,
        "name": "exact_boundary_two_segments",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.0], [2, float("inf")]],
        "epsilon": 0.5,
        "expected": 1
    },
    {
        "id": 5,
        "name": "very_large_epsilon_merges_all",
        "pc_fx": [[-float("inf"), float("inf")], [0, 10], [1, -10], [2, 20], [3, float("inf")]],
        "epsilon": 100.0,
        "expected": 1
    },
    {
        "id": 6,
        "name": "single_piece_input",
        "pc_fx": [[-float("inf"), float("inf")], [0, 42], [1, float("inf")]],
        "epsilon": 0.0,
        "expected": 1
    },
    {
        "id": 7,
        "name": "uneven_widths_borderline_merge",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [0.1, 1.5], [10, 3], [100, float("inf")]],
        "epsilon": 1.5,
        "expected": 1
    },
    {
        "id": 8,
        "name": "arithmetic_progression_many_segments",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 1], [2, 2], [3, 3], [4, float("inf")]],
        "epsilon": 1.5,
        "expected": 1
    },
    {
        "id": 9,
        "name": "two_well_separated_groups",
        "pc_fx": [[-float("inf"), float("inf")], [0, 1], [1, 1], [2, 1], [3, 10], [4, 10], [5, float("inf")]],
        "epsilon": 0.4,
        "expected": 2
    },
    {
        "id": 10,
        "name": "repeating_decimals_borderline",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1/3], [2, 2/3], [3, float("inf")]],
        "epsilon": 1/3,
        "expected": 1
    }
]
test_cases10 = [
    # 1. Single piece (already minimal)
    {
        "name": "single_piece",
        "pc_fx": [[-float("inf"), float("inf")], [0, 5], [10, float("inf")]],
        "epsilon": 0.1,
        "expected_parts": 1
    },

    # 2. Two identical adjacent values; zero tolerance should allow merge
    {
        "name": "two_identical_zero_eps",
        "pc_fx": [[-float("inf"), float("inf")], [0, 5], [2, 5], [5, float("inf")]],
        "epsilon": 0.0,
        "expected_parts": 1
    },

    # 3. Two values exactly at the L∞ merge threshold (max-min == 2*epsilon)
    {
        "name": "exact_threshold_merge",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 4], [3, float("inf")]],
        "epsilon": 2.0,
        "expected_parts": 1
    },

    # 4. Two values slightly above the merge threshold (should remain separate)
    {
        "name": "slightly_over_threshold",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 4.1], [3, float("inf")]],
        "epsilon": 2.0,
        "expected_parts": 2
    },

    # 5. Floating-point equality / rounding sensitivity where total range == 2*epsilon
    {
        "name": "float_rounding_boundary",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.1], [1, 0.3], [2, 0.1], [3, float("inf")]],
        "epsilon": 0.1,
        "expected_parts": 1
    },

    # 6. Zero-length piece (repeated x), values within tolerance so merge into one
    {
        "name": "zero_length_segment",
        "pc_fx": [[-float("inf"), float("inf")], [0, 2.0], [0, 3.0], [1, 2.5], [2, float("inf")]],
        "epsilon": 0.75,
        "expected_parts": 1
    },

    # 7. Alternating values that cannot be merged across neighbors (forces every piece)
    {
        "name": "alternating_forces_all_separate",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 3], [2, 0], [3, 3], [4, float("inf")]],
        "epsilon": 1.0,
        "expected_parts": 4
    },

    # 8. Single large outlier in middle; optimal is three groups (left cluster, outlier, right cluster)
    {
        "name": "middle_outlier_requires_split",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 0], [2, 10], [3, 0], [4, 0], [5, float("inf")]],
        "epsilon": 4.9,
        "expected_parts": 3
    },

    # 9. Same data as above but epsilon large enough to merge everything
    {
        "name": "large_epsilon_merge_all",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 0], [2, 10], [3, 0], [4, 0], [5, float("inf")]],
        "epsilon": 5.0,
        "expected_parts": 1
    },

    # 10. Tiny incremental differences with zero tolerance (no merges allowed)
    {
        "name": "tiny_differences_zero_tol",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 0.001], [2, 0.002], [3, 0.003], [4, 0.004], [5, float("inf")]],
        "epsilon": 0.0,
        "expected_parts": 5
    }
]
test_cases11 = [
    {
        "id": "identical_values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [3, float('inf')]],
        "epsilon": 0.0,
        "description": "Two adjacent pieces with identical values (should be mergeable when epsilon = 0).",
        "expected_min_pieces": 1
    },
    {
        "id": "exact_threshold_inclusive",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, float('inf')]],
        "epsilon": 0.5,
        "description": "Values 0,1,2 with epsilon at the half-range boundary (2*epsilon = 1). Tests inclusive threshold behavior.",
        "expected_min_pieces": 2
    },
    {
        "id": "alternating_large_jumps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, float('inf')]],
        "epsilon": 0.5,
        "description": "Alternating 0 and 2 values; no adjacent merge possible when 2*epsilon < 2. Tests worst-case fragmentation.",
        "expected_min_pieces": 5
    },
    {
        "id": "floating_point_precision",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1e-10], [2, 2e-10], [3, float('inf')]],
        "epsilon": 1e-10,
        "description": "Very small values to test floating-point edge behavior; all three should merge when 2*epsilon = 2e-10.",
        "expected_min_pieces": 1
    },
    {
        "id": "zero_length_segment",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.05], [1, 1.04], [2, float('inf')]],
        "epsilon": 0.03,
        "description": "Contains a zero-length domain piece (two consecutive x with equal boundary). Tests robustness to zero-length segments; values are within 0.05 range so mergeable if 2*epsilon = 0.06.",
        "expected_min_pieces": 1
    },
    {
        "id": "unsorted_x_inputs",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.00], [2, 0.90], [1, 0.95], [3, float('inf')]],
        "epsilon": 0.06,
        "description": "x positions provided out of order. A correct implementation should sort by x and then compute partitions; after sorting values are [1.00,0.95,0.90] with total range 0.10 and 2*epsilon=0.12 so they merge into one piece.",
        "expected_min_pieces": 1
    },
    {
        "id": "isolated_spike",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 100.0], [2, 0.1], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "A single large spike in the middle; spike is too large to merge with neighbors when 2*epsilon = 2. Tests algorithms that attempt invalid averaging across large jumps.",
        "expected_min_pieces": 3
    },
    {
        "id": "many_small_steps",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.4], [2, 0.8], [3, 1.2], [4, 1.6], [5, float('inf')]],
        "epsilon": 0.4,
        "description": "Monotone increasing small steps where grouping should form two pieces: [0.0,0.4,0.8] and [1.2,1.6] when 2*epsilon = 0.8.",
        "expected_min_pieces": 2
    },
    {
        "id": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 42.0], [1, float('inf')]],
        "epsilon": 0.0,
        "description": "Single actual piece in input (n = 1). Algorithm must return 1 regardless of epsilon >= 0.",
        "expected_min_pieces": 1
    },
    {
        "id": "edge_inclusive_nontrivial",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 4.0], [3, float('inf')]],
        "epsilon": 1.0,
        "description": "Three values [0,2,4] with 2*epsilon = 2. Greedy grouping should produce two pieces: [0,2] and [4]. Tests borderline multi-step merges.",
        "expected_min_pieces": 2
    }
]
test_cases12 = [
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 5], [10, float("inf")]],
        "epsilon": 0.0,
        "expected": 1,
        "description": "Single actual piece; trivial optimal result is 1."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 5], [2, float("inf")]],
        "epsilon": 2.0,
        "expected": 2,
        "description": "Two pieces with |y1-y2| > 2*epsilon so no merge is possible."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 1], [2, 0], [3, 1], [4, float("inf")]],
        "epsilon": 0.5,
        "expected": 1,
        "description": "Alternating 0/1 values where 2*epsilon equals the range so all can merge (boundary tie)."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 1.0000001], [2, float("inf")]],
        "epsilon": 0.5,
        "expected": 2,
        "description": "Floating precision sensitivity: difference just over 2*epsilon should prevent merge."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 2], [0, 2.5], [1, 3], [3, float("inf")]],
        "epsilon": 0.5,
        "expected": 1,
        "description": "Repeated x (zero-width first segment) plus mergeable values; algorithm must ignore empty interval and merge others."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [-10, -5], [0, 8], [5, 3], [10, float("inf")]],
        "epsilon": 7.0,
        "expected": 1,
        "description": "Very large epsilon that allows merging all pieces into one."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [6, float("inf")]],
        "epsilon": 0.4,
        "expected": 6,
        "description": "Frequent alternation 0/1 with epsilon too small to merge any adjacent differing segments."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [2, 1], [1, 2], [3, float("inf")]],
        "epsilon": 0.5,
        "expected": None,
        "description": "Out-of-order x boundaries; input invalid or requires pre-sorting. Expect algorithm to raise or return error/None."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 1], [2, float("inf")]],
        "epsilon": -0.1,
        "expected": None,
        "description": "Negative epsilon; invalid tolerance should be rejected."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 1], [2, 2], [3, float("inf")]],
        "epsilon": 0.5,
        "expected": 2,
        "description": "Three consecutive values 0,1,2 where adjacent pairs can merge but all three cannot, minimal partition is 2."
    }
]
test_cases13 = [
    # 1. Single global constant piece (already optimal)
    {
        "pc_fx": [[-float("inf"), float("inf")], [-float("inf"), 5.0], [float("inf"), float("inf")]],
        "epsilon": 0.0,
        "expected": 1,
        "description": "Single piece covering entire domain, epsilon 0"
    },

    # 2. Two adjacent pieces with identical values (should merge)
    {
        "pc_fx": [[-float("inf"), float("inf")], [0.0, 2.0], [10.0, 2.0], [float("inf"), float("inf")]],
        "epsilon": 0.0,
        "expected": 1,
        "description": "Two contiguous pieces with equal values, epsilon 0"
    },

    # 3. Two pieces whose values differ but within epsilon (mergeable)
    {
        "pc_fx": [[-float("inf"), float("inf")], [0.0, 2.0], [5.0, 2.4], [float("inf"), float("inf")]],
        "epsilon": 0.5,
        "expected": 1,
        "description": "Two pieces with value difference <= 2*epsilon"
    },

    # 4. Three pieces where only adjacent pairs can merge (borderline)
    {
        "pc_fx": [[-float("inf"), float("inf")], [0.0, 0.0], [1.0, 3.0], [2.0, 6.0], [float("inf"), float("inf")]],
        "epsilon": 1.5,
        "expected": 2,
        "description": "Values 0,3,6 with epsilon 1.5: adjacent pairs mergeable but all three are not"
    },

    # 5. Floating precision borderline case (tests numeric robustness)
    {
        "pc_fx": [[-float("inf"), float("inf")], [0.0, 0.0], [1.0, 2.0 + 1e-12], [2.0, 4.0], [float("inf"), float("inf")]],
        "epsilon": 1.000000000001,
        "expected": 2,
        "description": "Tiny floating offset in middle value, epsilon chosen to allow pair merges"
    },

    # 6. Large epsilon that should merge all pieces into one
    {
        "pc_fx": [[-float("inf"), float("inf")], [-100.0, 0.0], [0.0, 10.0], [50.0, -5.0], [51.0, 7.0], [float("inf"), float("inf")]],
        "epsilon": 10.0,
        "expected": 1,
        "description": "Wide range of values but epsilon large enough to merge entire domain"
    },

    # 7. Very small epsilon preventing any merges
    {
        "pc_fx": [[-float("inf"), float("inf")], [0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [float("inf"), float("inf")]],
        "epsilon": 0.4,
        "expected": 4,
        "description": "Adjacent value differences too large for merging with small epsilon"
    },

    # 8. Alternating extremes where entire sequence is mergeable at borderline
    {
        "pc_fx": [[-float("inf"), float("inf")], [0.0, 0.0], [1.0, 5.0], [2.0, 0.0], [3.0, 5.0], [4.0, 0.0], [float("inf"), float("inf")]],
        "epsilon": 2.5,
        "expected": 1,
        "description": "Alternating 0 and 5; 2*epsilon equals max-min so full merge is valid"
    },

    # 9. Long vs tiny interval values to detect algorithms that incorrectly weight by length
    {
        "pc_fx": [[-float("inf"), float("inf")], [0.0, 0.0], [1e6, 100.0], [1e6 + 1.0, 0.0], [float("inf"), float("inf")]],
        "epsilon": 50.0,
        "expected": 1,
        "description": "Tiny spike of 100 in a narrow region; under L-infinity 2*epsilon == 100 allows full merge"
    },

    # 10. Negative and mixed values where optimal split is nontrivial
    {
        "pc_fx": [[-float("inf"), float("inf")], [-10.0, -1.0], [0.0, 1.0], [10.0, 0.0], [float("inf"), float("inf")]],
        "epsilon": 0.5,
        "expected": 2,
        "description": "Values -1, 1, 0; only the last two can be merged given epsilon"
    }
]
test_cases14 = [
    # 1. All pieces identical values, zero tolerance -> should merge into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.0], [3, 2.0], [5, float('inf')]],
        "epsilon": 0.0,
        "expected": 1,
        "description": "Multiple equal-value pieces; epsilon 0 forces exact equality merge."
    },

    # 2. Tiny floating difference, zero tolerance -> should NOT merge (precision edge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.0 + 1e-12], [5, float('inf')]],
        "epsilon": 0.0,
        "expected": 2,
        "description": "Values differ by tiny amount; epsilon 0 should keep them separate."
    },

    # 3. Large epsilon exactly at threshold to merge all (boundary equality)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, float('inf')]],
        "epsilon": 5.0,
        "expected": 1,
        "description": "max-min = 10 so eps = 5 equals half-range; single-piece approximation allowed."
    },

    # 4. No possible adjacent merges given small epsilon -> all separate
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 3.0], [2, 6.0], [4, float('inf')]],
        "epsilon": 1.0,
        "expected": 3,
        "description": "Adjacent intervals do not overlap under epsilon; each piece must remain."
    },

    # 5. Single-point intersections between neighbors (edge-case intersection at a point)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 4.0], [5, float('inf')]],
        "epsilon": 1.0,
        "expected": 2,
        "description": "Neighbor intervals touch at a point; grouping should permit single-point overlap."
    },

    # 6. Alternating values that only allow grouping in adjacent pairs
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0], [4, 0.0], [6, float('inf')]],
        "epsilon": 1.0,
        "expected": 3,
        "description": "Pattern 0,2,0,2,0 with eps 1 forces merges into adjacent pairs plus one leftover."
    },

    # 7. Increasing sequence where first four can merge but last cannot
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 2.0], [3, 3.0], [4, 4.0], [6, float('inf')]],
        "epsilon": 1.5,
        "expected": 2,
        "description": "Chain intersection holds for first four (including single-point), last piece separates."
    },

    # 8. Duplicate breakpoint (zero-width piece) with values within epsilon -> should merge all
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [0, 1.4], [2, 1.0], [4, float('inf')]],
        "epsilon": 0.5,
        "expected": 1,
        "description": "Zero-width piece present; all values intersect under epsilon so single group."
    },

    # 9. Exact single-point overlap between two pieces (boundary numeric test)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [3, float('inf')]],
        "epsilon": 1.0,
        "expected": 1,
        "description": "Two-piece case with interval intersection exactly at one point; should merge."
    },

    # 10. Three widely spaced values where only two can be grouped (chain-touching at points)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 20.0], [4, float('inf')]],
        "epsilon": 5.0,
        "expected": 2,
        "description": "Intervals touch pairwise at points but global intersection empty; minimal segmentation 2."
    }
]
test_cases15 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0,
        "expected_min_pieces": 1,
        "description": "Single actual piece on [0,10) with exact fit"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0,
        "expected_min_pieces": 1,
        "description": "Adjacent identical piece values should merge to one"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 4], [2, float('inf')]],
        "epsilon": 2,
        "expected_min_pieces": 1,
        "description": "Pairwise difference equals 2*epsilon boundary case"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 3], [2, 0], [3, float('inf')]],
        "epsilon": 1.5,
        "expected_min_pieces": 1,
        "description": "Three pieces mergeable exactly at L-infinity threshold"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 4], [3, float('inf')]],
        "epsilon": 1,
        "expected_min_pieces": 2,
        "description": "Chain where adjacent merges possible but full merge not possible"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.199999999999], [2, float('inf')]],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Floating point borderline just below 2*epsilon"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.00], [1, 5.05], [2, 4.95], [3, 5.03], [4, 5.00], [5, float('inf')]],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Small fluctuations all within epsilon"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 10], [3, 1], [4, 1], [5, float('inf')]],
        "epsilon": 1,
        "expected_min_pieces": 3,
        "description": "Single large outlier inside uniform signal"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [100, 1], [101, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 1,
        "description": "Nonuniform interval widths where L-inf mergeability should hold"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 50], [2, 2], [3, float('inf')]],
        "epsilon": 1,
        "expected_min_pieces": 1,
        "description": "Zero-length piece with extreme value should not force extra pieces"
    }
]
test_cases16 = [
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 5], [1, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Single actual piece returns 1."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 3], [2, 3], [4, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Two adjacent pieces with identical values merge when epsilon is zero."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 3.0], [1, 3.5], [2, float("inf")]],
        "epsilon": 0.25,
        "expected_min_pieces": 1,
        "description": "Values differ by exactly 2*epsilon across pieces; merge allowed."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0], [1, 10], [2, 0], [3, 10], [4, float("inf")]],
        "epsilon": 2.0,
        "expected_min_pieces": 4,
        "description": "Alternating large jumps prevent merging beyond single pieces."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 0.4], [2, 0.8], [3, 1.2], [4, float("inf")]],
        "epsilon": 0.6,
        "expected_min_pieces": 1,
        "description": "Monotonic ramp whose total range is within 2*epsilon merges into one piece."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 2.0], [0, 3.0], [1, 2.5], [2, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Includes a zero-length first piece; all values' range fits within 2*epsilon."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 1.0], [-1, 2.0], [2, 1.5], [3, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": None,
        "description": "Unsorted piece boundaries detect invalid input or require preprocessing; expected result is undefined."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 100.0], [2, 200.0], [3, float("inf")]],
        "epsilon": 200.0,
        "expected_min_pieces": 1,
        "description": "Very large epsilon merges widely separated values into a single piece."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.1], [1, 0.30000000000000004], [2, 0.1], [3, float("inf")]],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "description": "Floating point precision edge case where mathematical range equals 2*epsilon."
    },
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 0.1], [2, 0.0], [3, 0.1], [4, 0.0], [5, float("inf")]],
        "epsilon": 0.05,
        "expected_min_pieces": 3,
        "description": "Small oscillation sequence where optimal grouping pairs adjacent 0.0/0.1 segments producing three groups."
    }
]
test_cases17 = [
    {
        "name": "Constant function (all equal values)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 5], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1
    },
    {
        "name": "Zero tolerance, no identical neighbors",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 1], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3
    },
    {
        "name": "Exact borderline merge across whole domain",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 2], [3, 1], [4, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },
    {
        "name": "Just below merge threshold (floating failure risk)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 2], [2, 2], [3, 1], [4, float('inf')]],
        "epsilon": 0.49,
        "expected_min_pieces": 4
    },
    {
        "name": "Large peak removable at equality",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, float('inf')]],
        "epsilon": 5.0,
        "expected_min_pieces": 1
    },
    {
        "name": "Alternating small range values (greedy can fail if wrong)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 1
    },
    {
        "name": "Borderline pair merge (exact equality check)",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1
    },
    {
        "name": "Single piece input",
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [1, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1
    },
    {
        "name": "Monotone increasing values requiring partitioning",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 4], [3, 6], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2
    },
    {
        "name": "Negative and positive clusters",
        "pc_fx": [[-float('inf'), float('inf')], [0, -10], [1, -9], [2, 0], [3, 9], [4, 10], [5, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 3
    }
]
test_cases18 = [
    {
        "id": 1,
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Single actual piece; algorithm must return 1 regardless of epsilon."
    },
    {
        "id": 2,
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, 2], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Multiple contiguous pieces with identical values and epsilon zero; must merge to 1."
    },
    {
        "id": 3,
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Monotone increasing values where first three can merge (range 2 <= 2*epsilon) and last stands alone."
    },
    {
        "id": 4,
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 5,
        "description": "Alternating high/low values that prevent any adjacent merges with small epsilon."
    },
    {
        "id": 5,
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1.0000001], [2, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Floating precision edge: values differ by just above 1.0 so 2*epsilon = 1.0 is insufficient to merge."
    },
    {
        "id": 6,
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [0, 5], [1, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Zero-length interval followed by identical-value interval; both should be treated as a single piece."
    },
    {
        "id": 7,
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 1], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Nontrivial grouping where the first piece must stand alone but the last two can merge."
    },
    {
        "id": 8,
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.4], [2, 0.8], [3, 1.2], [4, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 1,
        "description": "Small incremental changes whose overall range equals 2*epsilon; entire sequence must merge to one piece."
    },
    {
        "id": 9,
        "pc_fx": [[-float('inf'), float('inf')], [-3, -1.5], [-1, -1.0], [0, 0.5], [2, 0.9], [4, float('inf')]],
        "epsilon": 0.4,
        "expected_min_pieces": 2,
        "description": "Mixed negative and positive values that split into two optimal blocks: negatives together and positives together."
    },
    {
        "id": 10,
        "pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 1], [2, 1], [3, 2], [4, 2], [5, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 2,
        "description": "Epsilon zero with two distinct exact values; must compress contiguous identical-value runs but not merge different values."
    }
]
test_cases19 = [
    {
        "id": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.0,
        "expected": 1,
        "desc": "Trivial single piece; algorithm must return 1."
    },
    {
        "id": "adjacent_equal_values",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2], [5, float('inf')]],
        "epsilon": 0.0,
        "expected": 1,
        "desc": "Two adjacent pieces with identical values; zero tolerance should allow full merge."
    },
    {
        "id": "three_way_merge_via_boundary_point",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [2, 1.0], [4, 0.0], [6, float('inf')]],
        "epsilon": 0.5,
        "expected": 1,
        "desc": "Values 0,1,0 with ε=0.5 have a common intersection at 0.5; all three contiguous pieces can be merged to one. Detects algorithms that pick a representative value too early."
    },
    {
        "id": "pairwise_intersections_but_no_triple",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [2, 1.0], [4, 2.0], [6, float('inf')]],
        "epsilon": 0.5,
        "expected": 2,
        "desc": "Values 0,1,2 where adjacent pairs intersect but the triple does not; optimal result is 2 pieces (merge one adjacent pair)."
    },
    {
        "id": "alternating_small_epsilon",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.9,
        "expected": 4,
        "desc": "Strong alternation 0,2,0,2 with small ε that prevents merging; should keep all pieces separate."
    },
    {
        "id": "alternating_large_epsilon_all_merge",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0], [4, float('inf')]],
        "epsilon": 1.1,
        "expected": 1,
        "desc": "Same alternating pattern but ε large enough so a single value exists in all intervals; entire domain should merge to one piece."
    },
    {
        "id": "exact_boundary_intersection",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.6], [2, 1.2], [3, float('inf')]],
        "epsilon": 0.6,
        "expected": 1,
        "desc": "Intersections occur exactly at boundary value 0.6; tests correct handling of closed/open endpoints and exact-equality numeric boundaries."
    },
    {
        "id": "floating_point_precision",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.30000000000000004], [2, 0.6], [3, float('inf')]],
        "epsilon": 0.3,
        "expected": 1,
        "desc": "Values that expose floating-point representation issues; intervals overlap at exact boundary, algorithm must treat them as mergeable."
    },
    {
        "id": "nontrivial_grouping_required",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 0.9], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.1,
        "expected": 3,
        "desc": "Middle two pieces (1.0 and 0.9) can be merged while first and last cannot; optimal segmentation is [0],[1+2],[3]. Detects greedy mistakes that fix values early."
    },
    {
        "id": "wide_plateau_with_outlier",
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 10.0], [3, 1.0], [4, float('inf')]],
        "epsilon": 2.5,
        "expected": 3,
        "desc": "A wide plateau of 1 surrounding a single outlier 10. Epsilon allows merging adjacent 1s but not across the outlier; optimal is three pieces (left plateau, outlier, right plateau)."
    }
]
test_cases20 = [
    {
        "name": "All values identical single piece",
        "pc_fx": [[-float("inf"), float("inf")], [0, 5.0], [1, 5.0], [2, 5.0], [3, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Trivial case: all y identical, any epsilon >= 0 permits single piece"
    },
    {
        "name": "Exactly at merge threshold",
        "pc_fx": [[-float("inf"), float("inf")], [0, 1.0], [1, 3.0], [2, float("inf")]],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "notes": "max(y)-min(y)=2 equals 2*epsilon; should be mergeable into one piece"
    },
    {
        "name": "Just above merge threshold",
        "pc_fx": [[-float("inf"), float("inf")], [0, 1.0], [1, 3.1], [2, float("inf")]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "notes": "max(y)-min(y)=2.1 > 2*epsilon; cannot merge"
    },
    {
        "name": "Pairwise mergeable but triple not mergeable",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 2.0], [2, 4.0], [3, float("inf")]],
        "epsilon": 1.5,
        "expected_min_pieces": 2,
        "notes": "Adjacent pairs pass pairwise check but overall range 4 > 2*epsilon; optimal is 2 pieces"
    },
    {
        "name": "Floating point boundary equality",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.1], [1, 0.3], [2, float("inf")]],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "notes": "max-min = 0.2 equals 2*epsilon; tests float rounding handling"
    },
    {
        "name": "Gradual ramp grouped into blocks",
        "pc_fx": [[-float("inf"), float("inf")],
                  [0, 0.0], [1, 0.2], [2, 0.4], [3, 0.6], [4, 0.8], [5, float("inf")]],
        "epsilon": 0.25,
        "expected_min_pieces": 2,
        "notes": "2*epsilon=0.5 so first three (0.0..0.4) form one block and remaining two form second block"
    },
    {
        "name": "Single actual piece",
        "pc_fx": [[-float("inf"), float("inf")], [0, 10.0], [5, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "notes": "Only one actual piece; algorithm must handle minimal n correctly"
    },
    {
        "name": "Plateau and outlier just below threshold",
        "pc_fx": [[-float("inf"), float("inf")], [0, 5.0], [1, 5.0], [2, 5.0], [3, 8.0], [4, float("inf")]],
        "epsilon": 1.49,
        "expected_min_pieces": 2,
        "notes": "max-min=3 just above 2*epsilon; tests epsilon rounding near boundary"
    },
    {
        "name": "Ambiguous local merges requiring global view",
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 2.0], [2, 2.0], [3, 0.0], [4, float("inf")]],
        "epsilon": 1.0,
        "expected_min_pieces": 1,
        "notes": "Overall range 2 equals 2*epsilon so full merge is optimal; catches greedy local-only merging mistakes"
    },
    {
        "name": "Zero tolerance with tiny numerical difference",
        "pc_fx": [[-float("inf"), float("inf")], [0, 1.0], [1, 1.0], [2, 1.0000000001], [3, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 2,
        "notes": "epsilon zero forces exact equality; last value differs slightly and must form separate piece"
    }
]
test_cases21 = [
    # 1. Single piece (trivial): algorithm must keep 1 piece for any epsilon >= 0
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [10, float('inf')]],
        "epsilon": 0.0
    },

    # 2. Borderline two-piece merge: difference 100, half-diff = 50 (tests exact-equality boundary)
    {
        "name": "borderline_merge_two",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 100], [2, float('inf')]],
        "epsilon": 50.0
    },

    # 3. Alternating values (short intervals): small epsilon prevents any merges (tests many adjacent alternations)
    {
        "name": "alternating_tiny_epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [6, float('inf')]],
        "epsilon": 0.49
    },

    # 4. Floating-point equality edge: extremely small difference, epsilon equals half-diff (tests numerical stability)
    {
        "name": "fp_equality",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1e-9], [2, float('inf')]],
        "epsilon": 5e-10
    },

    # 5. Global vs greedy counterexample: three increasing values where a global merge into one is valid
    {
        "name": "global_vs_greedy",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, float('inf')]],
        "epsilon": 1.0
    },

    # 6. Ambiguous adjacent merge choices: merging either neighbor is allowed, but merging all three is not
    {
        "name": "ambiguous_merge_choice",
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.2], [2, 0.0], [3, float('inf')]],
        "epsilon": 0.6
    },

    # 7. Zero-length interval included: one piece has zero width (identical breakpoints) to test robustness
    {
        "name": "zero_length_interval",
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [3, 5], [3, 2], [7, float('inf')]],
        "epsilon": 0.5
    },

    # 8. Negative x and y values: varied signs and nonuniform spacing (tests sign handling and grouping)
    {
        "name": "negative_values_and_x",
        "pc_fx": [[-float('inf'), float('inf')], [-5, -3], [-3, -2], [-1, -1], [2, 1], [5, float('inf')]],
        "epsilon": 0.9
    },

    # 9. Many pieces (linear ramp): tests grouping across many adjacent pieces when epsilon allows block merges
    {
        "name": "many_pieces_linear",
        "pc_fx": [[-float('inf'), float('inf')],
                 [0, 0], [1, 1], [2, 2], [3, 3], [4, 4],
                 [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, float('inf')]],
        "epsilon": 2.0
    },

    # 10. Zero epsilon with repeated adjacent equal values: identical neighbors must merge even when epsilon == 0
    {
        "name": "zero_epsilon_adjacent_equals",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 5], [2, 6], [3, 6], [4, 5], [5, float('inf')]],
        "epsilon": 0.0
    }
]
test_cases22 = [
    {
        "name": "single_piece",
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [100, float('inf')]],
        "epsilon": 0.1,
        "expected": 1,
        "notes": "Trivial: only one actual piece across the domain."
    },
    {
        "name": "three_equal_values_zero_epsilon",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2.0], [1, 2.0], [2, 2.0], [3, float('inf')]],
        "epsilon": 0.0,
        "expected": 1,
        "notes": "Multiple pieces with identical values; epsilon 0 should allow full merge."
    },
    {
        "name": "endpoint_intersection_exact",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 10.0], [2, 0.0], [3, float('inf')]],
        "epsilon": 5.0,
        "expected": 1,
        "notes": "Intersection exists only at an endpoint (value 5). Tests <= vs < and exact-boundary handling."
    },
    {
        "name": "floating_point_precision",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 2e-9], [2, float('inf')]],
        "epsilon": 1e-9,
        "expected": 1,
        "notes": "Very small values near floating precision limits; tests numeric stability."
    },
    {
        "name": "no_possible_merges",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 10.0], [2, 20.0], [3, float('inf')]],
        "epsilon": 3.0,
        "expected": 3,
        "notes": "Pieces are far apart; algorithm should keep all pieces separate."
    },
    {
        "name": "avoid_committing_to_rep_value",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 4.0], [2, 8.0], [3, float('inf')]],
        "epsilon": 4.0,
        "expected": 1,
        "notes": "All three can be merged because the intersection includes 4 exactly; catches algorithms that commit to an interior representative and then fail future merges."
    },
    {
        "name": "zero_length_intervals",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [0, 1.0], [1, float('inf')]],
        "epsilon": 0.0,
        "expected": 1,
        "notes": "Adjacent pieces with identical x boundaries (zero-length piece) should be handled correctly."
    },
    {
        "name": "very_large_values",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1e18], [1, 1e18 + 1.0], [2, float('inf')]],
        "epsilon": 1.0,
        "expected": 1,
        "notes": "Large magnitudes to check for overflow/precision issues in comparisons."
    },
    {
        "name": "negative_positive_bridge",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -5.0], [1, 0.0], [2, 5.0], [3, float('inf')]],
        "epsilon": 5.0,
        "expected": 1,
        "notes": "Values span negative to positive but share endpoint intersection at 0; tests sign-crossing merges."
    },
    {
        "name": "long_chain_narrowing_intervals",
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 10.0], [2, 20.0], [3, 30.0], [4, 40.0], [5, float('inf')]],
        "epsilon": 20.0,
        "expected": 1,
        "notes": "Chain of pieces where successive interval intersections progressively narrow but remain non-empty overall; checks whether algorithm can merge long chains."
    }
]
test_cases23 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 1,
        "description": "Single actual piece should remain one piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2], [1, 2], [2, 2], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 1,
        "description": "All piece values identical so optimal merge to one piece with epsilon zero."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, float('inf')]],
        "epsilon": 5.0,
        "expected_pieces": 1,
        "description": "Alternating values that admit a single constant (value 5) within L∞ tolerance."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 0.8], [2, 1.6], [3, float('inf')]],
        "epsilon": 0.75,
        "expected_pieces": 2,
        "description": "First two pieces can merge but all three cannot, so optimal two pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1], [2, 2], [3, 3], [4, float('inf')]],
        "epsilon": 100.0,
        "expected_pieces": 1,
        "description": "Very large epsilon should allow merging all pieces into one."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 2], [2, 4], [3, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 1,
        "description": "Three-piece chain whose intersection of tolerance intervals is a single point, mergeable to one piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 5], [2, 5], [3, 0], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 3,
        "description": "Adjacent identical middle pieces merge, but differing ends remain separate."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 4], [2, 0], [3, 4], [4, float('inf')]],
        "epsilon": 2.0,
        "expected_pieces": 1,
        "description": "Nonmonotone alternating values that admit a single constant within tolerance."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1e-12], [2, 0], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_pieces": 3,
        "description": "Tiny floating differences with zero tolerance must remain separate pieces."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [0.5, 2], [1.0, 1], [2.0, 3], [3.0, float('inf')]],
        "epsilon": 1.0,
        "expected_pieces": 2,
        "description": "First three pieces can merge to a single constant; last piece must remain separate, so optimal two pieces."
    }
]
test_cases24 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Two adjacent identical pieces merge into a single piece with zero tolerance."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.4], [2, 2.8], [3, float('inf')]],
        "epsilon": 0.75,
        "expected_min_pieces": 2,
        "description": "Chain where adjacent pairs are mergeable but the entire chain is not; tests pairwise vs global decisions."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0], [4, float('inf')]],
        "epsilon": 0.75,
        "expected_min_pieces": 4,
        "description": "Alternating extreme values prevent any adjacent merge under the tolerance."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.0], [2, 10.0], [3, 0.0], [4, 0.0], [5, float('inf')]],
        "epsilon": 4.9,
        "expected_min_pieces": 3,
        "description": "Single large outlier separates identical-value blocks; tests handling of isolated outliers."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.5], [2, 1.0], [3, 1.4], [4, float('inf')]],
        "epsilon": 0.7,
        "expected_min_pieces": 1,
        "description": "Monotone small ramp whose global half-range equals tolerance so all pieces can merge."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [10, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Single actual piece in input; algorithm must return one piece."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 1.000001], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "description": "Tiny floating difference with zero tolerance; tests strict equality handling and numeric precision."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 5.0], [2, 10.0], [3, -3.0], [4, 2.0], [5, float('inf')]],
        "epsilon": 100.0,
        "expected_min_pieces": 1,
        "description": "Very large tolerance that should merge all pieces into one."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 2.0], [2, 4.0], [3, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "description": "Three values where adjacent pairs are mergeable but the whole triple is not."
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.9], [2, 3.8], [3, 5.7], [4, float('inf')]],
        "epsilon": 0.95,
        "expected_min_pieces": 2,
        "description": "Equally spaced chain where optimal grouping is into two pairs; tests partitioning into minimal groups."
    }
]
test_cases25 = [
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 5], [10, float("inf")]],
        "epsilon": 0.1,
        "expected": 1,
        "desc": "Single piece over the domain (trivial 1-piece case)."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 3], [2, 3], [5, float("inf")]],
        "epsilon": 0.0,
        "expected": 1,
        "desc": "Adjacent pieces have exactly equal values; should merge even with epsilon=0."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 0], [1, 5], [2, 0], [3, float("inf")]],
        "epsilon": 2.5,
        "expected": 1,
        "desc": "Three-piece chain where whole-range max-min = 5, (max-min)/2 = 2.5 borderline merge into one piece."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 0], [1, 5 * (1 + 1e-12)], [2, 0], [3, float("inf")]],
        "epsilon": 2.5,
        "expected": 2,
        "desc": "Floating-point precision: middle value slightly >5 so whole-range merge should fail."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 0], [100, 5], [101, float("inf")]],
        "epsilon": 2.5,
        "expected": 1,
        "desc": "Large interval lengths should not affect L-infinity merge (values only matter)."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 1], [1, 2], [2, 3], [3, 4], [4, float("inf")]],
        "epsilon": 1.0,
        "expected": 2,
        "desc": "Monotone increasing values 1-4; first three can form one segment (max-min=2), last value remains separate."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 2], [1, 2], [2, 3], [3, float("inf")]],
        "epsilon": 0.0,
        "expected": 2,
        "desc": "Zero tolerance with exact-equality merge for first two pieces, distinct third piece stays separate."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 1], [1, 2], [2, float("inf")]],
        "epsilon": -0.5,
        "expected": "error",
        "desc": "Invalid negative epsilon: algorithm should reject or raise an error."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 0], [1, 1], [2, 0], [3, 1], [4, float("inf")]],
        "epsilon": 0.5,
        "expected": 1,
        "desc": "Alternating 0/1 values where global merge is allowed because (max-min)/2 = 0.5; tests global vs greedy merging."
    },
    {
        "pc_fx": [[float("-inf"), float("inf")], [0, 0], [1, 2.1], [2, 4.2], [3, 6.3], [4, float("inf")]],
        "epsilon": 1.05,
        "expected": 2,
        "desc": "Sequence of values spaced so pairs merge (diff=2.1) but whole range cannot; optimal partition is two segments."
    }
]
test_cases26 = [
    # 1. Single piece (trivial). Expect no reduction possible.
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 5], [1, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Single piece; algorithm must return 1."
    },

    # 2. Two adjacent identical values (exact merge with epsilon=0).
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 3], [1, 3], [2, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "Adjacent identical values; should merge to one piece."
    },

    # 3. Two adjacent values within epsilon (non-equal but mergeable).
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 0.4], [2, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "description": "Values differ but max-absolute error allows single-piece approximation."
    },

    # 4. Small oscillation where merging two adjacent pieces is optimal.
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 1.0], [2, 0.0], [3, float("inf")]],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "description": "Sequence 0,1,0 with epsilon=0.5; optimal is two pieces."
    },

    # 5. Outlier in middle that must remain separate while flanks merge.
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 1.0], [1, 1.0], [2, 10.0], [3, 1.0], [4, 1.0], [5, float("inf")]],
        "epsilon": 2.0,
        "expected_min_pieces": 3,
        "description": "Central outlier (10) forces at least three pieces: left block, outlier, right block."
    },

    # 6. Very large epsilon makes entire domain approximable by single constant.
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 100.0], [2, -50.0], [3, float("inf")]],
        "epsilon": 100.0,
        "expected_min_pieces": 1,
        "description": "Large epsilon; all values can be approximated by one constant under L-infinity."
    },

    # 7. Floating-point precision edge where midpoint error equals epsilon.
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.3333333], [1, 0.6666667], [2, float("inf")]],
        "epsilon": 0.1666667,
        "expected_min_pieces": 1,
        "description": "Midpoint error equals epsilon; implementation must handle float precision correctly."
    },

    # 8. Negative values and zero epsilon (identical negatives).
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, -1.0], [1, -1.0], [2, -1.0], [3, float("inf")]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "description": "All pieces equal negative value; should merge to one with epsilon 0."
    },

    # 9. Tight epsilon that allows merging of some neighbors but not across an outlier.
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, 0.0], [1, 0.6], [2, 0.2], [3, 0.7], [4, 0.1], [5, float("inf")]],
        "epsilon": 0.25,
        "expected_min_pieces": 3,
        "description": "Middle three values can form one block; first and last remain separate -> three pieces."
    },

    # 10. Mixed signs with very small epsilon (no merges allowed except identical neighbors).
    {
        "pc_fx": [[-float("inf"), float("inf")], [0, -2.0], [1, -2.0000001], [2, 0.0], [3, 2.0], [4, 2.0], [5, float("inf")]],
        "epsilon": 1e-7,
        "expected_min_pieces": 4,
        "description": "Tiny epsilon exposes float equality issues; only exactly-equal adjacent 2.0's should merge."
    }
]
test_cases27 = [
    # 1. Single piece (trivial)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]], "epsilon": 0.0},

    # 2. Two adjacent identical values (should merge when epsilon = 0)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 2], [2, 2], [5, float('inf')]], "epsilon": 0.0},

    # 3. Adjacent differences exactly at the merging threshold (range = 2*epsilon)
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 4], [2, 8], [3, float('inf')]], "epsilon": 2.0},

    # 4. Floating precision edge (0.1 + 0.2 representation) with equality at threshold
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0.1], [1, 0.30000000000000004], [2, float('inf')]], "epsilon": 0.1},

    # 5. Alternating high/low values that should prevent merging across neighbors
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 10], [2, 0], [3, 10], [4, 0], [5, float('inf')]], "epsilon": 4.0},

    # 6. Very large epsilon that should allow merging all pieces into one
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1], [1, 100], [2, -50], [3, 20], [4, float('inf')]], "epsilon": 100.0},

    # 7. Zero-width piece (duplicate boundary) to test robustness against degenerate intervals
    {"pc_fx": [[-float('inf'), float('inf')], [0, 5], [1, 10], [1, 15], [2, float('inf')]], "epsilon": 3.0},

    # 8. Negative and sign-crossing values with epsilon that allows local merges but not global
    {"pc_fx": [[-float('inf'), float('inf')], [0, -1], [1, -0.5], [2, 0], [3, 0.4], [4, float('inf')]], "epsilon": 0.25},

    # 9. Long chain with gradual increases; tests grouping across multiple small ranges
    {"pc_fx": [[-float('inf'), float('inf')], [0, 0], [1, 1.9], [2, 3.8], [3, 5.7], [4, float('inf')]], "epsilon": 0.95},

    # 10. Machine-precision close values to check numerical stability
    {"pc_fx": [[-float('inf'), float('inf')], [0, 1.000000000000001], [1, 1.000000000000002], [2, float('inf')]], "epsilon": 1e-15},
]
test_cases28 = [
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [10, float('inf')]],
        "epsilon": 0.5,
        "expected": 1,
        "description": "Single piece already minimal"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [5, 1.0], [10, float('inf')]],
        "epsilon": 0.0,
        "expected": 1,
        "description": "Two adjacent pieces equal; zero epsilon allows exact merge"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [4, 2.6], [8, float('inf')]],
        "epsilon": 0.3,
        "expected": 1,
        "description": "Two-piece mergeable because max-min = 0.6 <= 2*epsilon"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 2.0], [2, 3.0], [3, 4.0], [4, float('inf')]],
        "epsilon": 0.0,
        "expected": 4,
        "description": "Zero tolerance forces exact reproduction (no merges across differing values)"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.9], [2, 0.0], [3, 1.9], [4, 0.0], [5, float('inf')]],
        "epsilon": 0.95,
        "expected": 1,
        "description": "Alternating values with global range = 1.9 equal to 2*epsilon -> full merge allowed"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')]] +
                 [[i, round(0.1 * i, 3)] for i in range(0, 10)] + [[10, float('inf')]],
        "epsilon": 0.5,
        "expected": 1,
        "description": "Many small steps with total range 0.9 <= 2*epsilon -> one piece"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.0], [2, 5.0], [3, 0.0], [4, 0.0], [5, float('inf')]],
        "epsilon": 2.0,
        "expected": 3,
        "description": "Middle spike too large to absorb; expects left plateau, spike alone, right plateau"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [5, 2.0], [10, 0.0], [15, float('inf')]],
        "epsilon": 1.0,
        "expected": 1,
        "description": "Exact tie: global max-min = 2.0 equals 2*epsilon, merge all into one"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [2, 3.0], [4, 2.0], [6, float('inf')]],
        "epsilon": 0.5,
        "expected": 2,
        "description": "Only right two pieces can merge (3.0 and 2.0); left piece stays separate"
    },
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 2.0], [2, 0.0], [3, 2.0], [4, 0.0], [5, float('inf')]],
        "epsilon": 0.4,
        "expected": 5,
        "description": "Alternating high/low with small epsilon prevents any adjacent merges"
    }
]
test_cases29 = [
    # 1. Single constant piece across domain
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "One piece only; algorithm must return 1."
    },

    # 2. Adjacent pieces with identical values (should merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3], [2, 3], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "Two adjacent pieces have identical y; optimal answer is 1."
    },

    # 3. Small within-noise variations mergeable into one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [10, 0.05], [20, -0.02], [30, float('inf')]],
        "epsilon": 0.10,
        "expected_min_pieces": 1,
        "note": "All y lie within tolerance so single-piece approximation is possible."
    },

    # 4. Alternating extreme values forcing no merges
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0], [10, 2], [20, 0], [30, 2], [40, float('inf')]],
        "epsilon": 0.4,
        "expected_min_pieces": 4,
        "note": "Adjacent ranges exceed 2*epsilon so no merges; expect one piece per original segment."
    },

    # 5. Isolated outlier in the middle
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5], [10, 5], [20, 100], [30, 5], [40, 5], [50, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 3,
        "note": "Two runs of equal values separated by one outlier; optimal is 3 pieces."
    },

    # 6. Smooth ramp that remains within tolerance across many pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [5, 0.2], [10, 0.4], [15, 0.6], [20, float('inf')]],
        "epsilon": 0.30,
        "expected_min_pieces": 1,
        "note": "Monotone small increments with total range = 0.6 <= 2*epsilon, mergeable to one."
    },

    # 7. Zero-length interval entries (identical x coordinates)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 10], [0, 10], [5, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "Consecutive entries share the same x but identical y; algorithm must treat them as mergeable."
    },

    # 8. Floating point boundary case where range equals 2*epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [10, 1e-9], [20, float('inf')]],
        "epsilon": 5e-10,
        "expected_min_pieces": 1,
        "note": "Range == 2*epsilon; numerical handling must allow a single-piece solution."
    },

    # 9. Larger alternating pattern to test scalability and correctness
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0], [1, 2], [2, 0], [3, 2], [4, 0], [5, 2], [6, 0], [7, 2], [8, 0], [9, 2],
                  [10, float('inf')]],
        "epsilon": 0.9,
        "expected_min_pieces": 10,
        "note": "Repeated alternation with large jumps; no adjacent merges possible under epsilon."
    },

    # 10. Case requiring strategic grouping into two pieces (first two merge)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [10, 0.49], [20, 1.0], [30, float('inf')]],
        "epsilon": 0.25,
        "expected_min_pieces": 2,
        "note": "First two values fit within one piece, third must be separate; optimal = 2."
    }
]
test_cases30 = [
    # 1. All pieces identical; epsilon 0 should merge to a single piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 1.0], [3, 1.0], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "constant function across all segments"
    },

    # 2. Small oscillation entirely within tolerance; should merge to one piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.2], [2, 0.9], [3, 1.1], [4, float('inf')]],
        "epsilon": 0.2,
        "expected_min_pieces": 1,
        "note": "max-min = 1.2-0.9 = 0.3 so half = 0.15 < 0.2"
    },

    # 3. Large spike in the middle prevents any merges with small epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, 0.0], [3, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 3,
        "note": "spike value far outside tolerance"
    },

    # 4. Adjacent pairs can merge but full merge not allowed; optimal is two pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.4], [2, 5.0], [3, 5.3], [4, float('inf')]],
        "epsilon": 0.25,
        "expected_min_pieces": 2,
        "note": "left two merge and right two merge; global merge fails"
    },

    # 5. Zero epsilon with equal adjacent values; identical neighbors must merge
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.0], [1, 2.0], [2, 3.0], [3, 3.0], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 2,
        "note": "two constant blocks present: 2 and 3"
    },

    # 6. Borderline float equality; diff = 0.3, epsilon = 0.15 exactly half -> merge allowed
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.3], [2, float('inf')]],
        "epsilon": 0.15,
        "expected_min_pieces": 1,
        "note": "tests floating point boundary behavior"
    },

    # 7. Single interior piece (n = 1) must remain a single piece regardless of epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "note": "trivial single-piece input"
    },

    # 8. Symmetric extremes where full merge is exactly on the epsilon threshold
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 5.0], [2, 0.0], [3, float('inf')]],
        "epsilon": 2.5,
        "expected_min_pieces": 1,
        "note": "max-min = 5, half = 2.5 equal to epsilon"
    },

    # 9. Longer prefix must be grouped across three pieces to be optimal; result should be two pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.9], [2, 1.9], [3, 3.8], [4, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "note": "first three can form one block (max-min=1.9 half=0.95 < 1); last stays separate"
    },

    # 10. Very small differences to test numeric stability with tiny epsilon
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1e-12], [2, 0.0], [3, 1e-12], [4, float('inf')]],
        "epsilon": 5e-13,
        "expected_min_pieces": 1,
        "note": "tiny alternating values where half-range equals epsilon"
    }
]


























