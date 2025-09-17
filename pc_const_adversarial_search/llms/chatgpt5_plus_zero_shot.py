#12 Sept 2025

#Iteration1 3:18PM
test_cases1 = [
    # 1) Tight single-piece feasibility: max(y)-min(y) == 2*epsilon  → should still be compressible to 1 piece
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (0.0, 0.0),
            (1.0, 0.4),
            (2.0, 0.2),
            (3.0, 0.3),
            (4.0, 0.1),
            (5.0, float('inf')),
        ],
        "epsilon": 0.2,
    },

    # 2) Just-over-ε spike forces a split even if narrow width doesn't matter under L∞
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (0.0, 0.0),
            (1.0, 0.0),
            (2.0, 0.41),
            (3.0, 0.0),
            (4.0, float('inf')),
        ],
        "epsilon": 0.2,
    },

    # 3) Alternating highs/lows: adjacent jumps >> 2ε → many splits unless globally compressible (it isn't here)
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 0.0),
            (3.0, 1.0),
            (4.0, 0.0),
            (5.0, float('inf')),
        ],
        "epsilon": 0.2,
    },

    # 4) Ultra-thin tall spike: amplitude > 2ε so must split even if the spike is very narrow
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (0.0, 0.0),
            (1e-6, 5.0),
            (2.0, 0.0),
            (3.0, float('inf')),
        ],
        "epsilon": 2.0,
    },

    # 5) Values straddling 0 but globally compressible: range < 2ε → should be 1 piece despite large local jumps
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (-2.0, -0.3),
            (-1.0,  0.3),
            ( 0.0, -0.3),
            ( 1.0,  0.3),
            ( 2.0, -0.2),
            ( 3.0, float('inf')),
        ],
        "epsilon": 0.35,
    },

    # 6) Staircase that stays within band until a final step exceeds 2ε: split should happen only once at the end
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (0.0, 0.00),
            (1.0, 0.10),
            (2.0, 0.20),
            (3.0, 0.30),
            (4.0, 0.60),  # pushes max-min over 2ε (2*0.25=0.5)
            (5.0, float('inf')),
        ],
        "epsilon": 0.25,
    },

    # 7) Large jump at the very first real piece boundary: tests left-continuity / segment start handling
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (0.0, 10.0),
            (1.0,  0.0),
            (2.0,  0.0),
            (3.0, float('inf')),
        ],
        "epsilon": 0.4,
    },

    # 8) Non-uniform x spacing with nearly-equal plateaus: should compress to one piece (range <= 2ε)
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (-1.5, 1.00),
            (-0.5, 1.00),
            ( 2.2, 1.05),
            ( 3.8, 1.05),
            ( 5.0, float('inf')),
        ],
        "epsilon": 0.05,
    },

    # 9) Huge magnitudes (numerical robustness): tiny variations around 1e9 should be mergable
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (0.0, 1e9),
            (1.0, 1e9 + 0.10),
            (2.0, 1e9 - 0.05),
            (3.0, float('inf')),
        ],
        "epsilon": 0.2,
    },

    # 10) Globally compressible despite large adjacent jumps: [0,1,0] fits a single constant (0.5) with ε=0.5
    {
        "pc_fx": [
            (-float('inf'), float('inf')),
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 0.0),
            (3.0, float('inf')),
        ],
        "epsilon": 0.5,
    },
]
#Iteration2 3:22PM
test_cases2 = [
    {
        # 1) Pure constant: optimal = 1 piece for any ε ≥ 0 (useful sanity check for ε = 0)
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 3.0), (5.0, float("inf"))],
        "epsilon": 0.0,
    },
    {
        # 2) Tiny jitter within ε ⇒ should collapse to 1 piece
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 1.00), (1.0, 1.05), (2.0, 0.95), (3.0, 1.02),
                  (4.0, float("inf"))],
        "epsilon": 0.10,
    },
    {
        # 3) Alternating highs/lows well beyond 2ε ⇒ needs many pieces; tests non-mergability
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0),
                  (4.0, float("inf"))],
        "epsilon": 0.40,
    },
    {
        # 4) Exact-threshold case: gaps = 2ε (0 ↔ 1.2 with ε=0.6) ⇒ whole block can be merged
        #    Tests ≤ vs < and floating-point guard logic.
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 1.2), (2.0, 0.0),
                  (3.0, float("inf"))],
        "epsilon": 0.60,
    },
    {
        # 5) Narrow spike (height >> 2ε) inside a long plateau ⇒ must isolate spike
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 0.0), (2.0, 3.0), (3.0, 0.0), (4.0, 0.0),
                  (5.0, float("inf"))],
        "epsilon": 0.50,
    },
    {
        # 6) Redundant duplicates / zero-width variety ⇒ identical adjacent values
        #    With ε=0, algorithm should merge equal runs exactly and split at true changes only.
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 2.0), (1.0, 2.0), (1.5, 2.0), (2.0, 1.0), (3.0, 1.0),
                  (4.0, float("inf"))],
        "epsilon": 0.0,
    },
    {
        # 7) Staircase with total span > 2ε ⇒ cannot all merge; tests best grouping
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 0.4), (2.0, 0.8), (3.0, 1.2),
                  (4.0, float("inf"))],
        "epsilon": 0.50,
    },
    {
        # 8) Boundary sensitivity with negatives; overall span ≤ 2ε ⇒ can merge all
        "pc_fx": [(-float("inf"), float("inf")),
                  (-3.0, 5.0), (-2.0, 7.0), (0.0, 5.0), (1.0, 6.0),
                  (2.0, float("inf"))],
        "epsilon": 1.0,   # span = 2, 2ε = 2 ⇒ mergeable
    },
    {
        # 9) Three-level pattern where middle level blocks global merge (span > 2ε);
        #    forces ≥ 3 pieces if ε too small to bridge neighbors
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 0.9), (2.0, 0.0), (3.0, 1.8), (4.0, 0.9), (5.0, 0.0),
                  (6.0, float("inf"))],
        "epsilon": 0.50,  # 0↔1.8 span = 1.8 > 2ε (=1.0) so not all mergeable
    },
    {
        # 10) “Greedy trap” zigzag with consecutive jumps at exactly 2ε:
        #     correct solution may need carefully chosen split points; stresses tie-handling.
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0), (4.0, 0.0),
                  (5.0, float("inf"))],
        "epsilon": 0.50,
    },
]
#Iteration3 3:27PM
test_cases3 = [
    # 1) Single plateau
    {
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 2.0], [5.0, float('inf')]],
        "epsilon": 0.1,
    },

    # 2) Small wiggles within 2*ε
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.92], [1.0, 1.08], [2.0, 0.95],
                  [3.0, 1.05], [4.0, 1.00], [5.0, float('inf')]],
        "epsilon": 0.1,
    },

    # 3) Exact-on-threshold adjacency
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0], [1.0, 1.6], [2.0, 1.0],
                  [3.0, 1.6], [4.0, float('inf')]],
        "epsilon": 0.3,
    },

    # 4) Narrow spike far outside tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 3.0], [2.0, 0.0], [3.0, float('inf')]],
        "epsilon": 0.4,
    },

    # 5) Alternating high/low beyond tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -1.5], [1.0, 1.5], [2.0, -1.5],
                  [3.0, 1.5], [4.0, -1.5], [5.0, float('inf')]],
        "epsilon": 0.4,
    },

    # 6) Large amplitude but short interval
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [0.9, 2.0], [1.1, 0.0], [2.0, float('inf')]],
        "epsilon": 0.4,
    },

    # 7) Monotone staircase within tolerance
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0], [1.0, 1.2], [2.0, 1.3],
                  [3.0, 1.4], [4.0, 1.5], [5.0, float('inf')]],
        "epsilon": 0.25,
    },

    # 8) Big jumps at boundaries
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 5.0], [1.0, 5.1], [2.0, 4.9],
                  [3.0, 5.0], [10.0, float('inf')]],
        "epsilon": 0.08,
    },

    # 9) Floating-point tight case
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0], [1.0, 1.6000000000000001],
                  [2.0, 1.0000000000000002], [3.0, float('inf')]],
        "epsilon": 0.3,
    },

    # 10) Long plateau with noise and mild drift
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.00], [1.0, 2.02], [2.0, 1.98], [3.0, 2.01],
                  [4.0, 2.10], [5.0, 2.00], [6.0, 2.03], [7.0, 1.99],
                  [8.0, float('inf')]],
        "epsilon": 0.07,
    },
]
#Iteration4 3:33PM
test_cases4 = [
    # 1) Constant function, ε = 0 → should compress to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0], [1.0, 2.0], [2.0, 2.0],
                  [3.0, float('inf')]],
        "epsilon": 0.0
    },

    # 2) All values within 2ε ⇒ single-piece feasible (range ≤ 2ε)
    # max=0.4, min=-0.3, range=0.7, ε=0.5 → 0.7 ≤ 1.0 ⇒ 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0,  0.0], [1.0,  0.4], [2.0, -0.3], [3.0, 0.2],
                  [4.0, float('inf')]],
        "epsilon": 0.5
    },

    # 3) Just-outside tolerance: range > 2ε, so cannot merge into 1
    # max=1.2, min=0.0, range=1.2, ε=0.5 → 1.2 > 1.0 ⇒ need ≥2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.2],
                  [2.0, float('inf')]],
        "epsilon": 0.5
    },

    # 4) Chain-merge trap (pairwise close, globally too wide)
    # Values: 0.0, 0.9, 1.8 with ε=0.5 → any two adjacent can merge, all three cannot.
    # Optimal = 2 pieces, greedy “merge-first” can be tricked.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.9], [2.0, 1.8],
                  [3.0, float('inf')]],
        "epsilon": 0.5
    },

    # 5) Narrow spike (width shouldn’t matter under L∞): needs 2 pieces if spike exceeds 2ε
    # range=5, ε=2.4 → 5 > 4.8 ⇒ ≥2 pieces (middle isolated)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 5.0], [1.001, 0.0],  # very short spike
                  [2.0, float('inf')]],
        "epsilon": 2.4
    },

    # 6) Plateau with small noise fully within 2ε ⇒ 1 piece
    # max=1.1, min=0.95, range=0.15 ≤ 0.2 (2ε) with ε=0.1 ⇒ 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.00], [1.0, 1.10], [2.0, 0.95], [3.0, 1.05],
                  [4.0, float('inf')]],
        "epsilon": 0.1
    },

    # 7) Monotone ramp: optimal grouping should respect range ≤ 2ε per block
    # Values: 0, 0.4, 0.8, 1.2, 1.6 with ε=0.25 (2ε=0.5)
    # Optimal grouping: [0,0.4], [0.8,1.2], [1.6] ⇒ 3 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.4], [2.0, 0.8], [3.0, 1.2], [4.0, 1.6],
                  [5.0, float('inf')]],
        "epsilon": 0.25
    },

    # 8) Redundant breakpoints (duplicate values); even with small ε, should collapse to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0], [0.5, 2.0], [1.0, 2.0], [2.0, 2.0],
                  [3.0, float('inf')]],
        "epsilon": 1e-9
    },

    # 9) Alternating sign flips just beyond tolerance ⇒ cannot merge across flips
    # diff=2.0, ε=0.9 → 2.0 > 1.8 ⇒ each segment stands alone ⇒ 4 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -1.0], [1.0, 1.0], [2.0, -1.0], [3.0, 1.0],
                  [4.0, float('inf')]],
        "epsilon": 0.9
    },

    # 10) Minimal n=1 case: exactly one real piece, any ε → optimal must be 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 3.2],
                  [2.0, float('inf')]],
        "epsilon": 0.0
    },
]
#Iteration5 3:35PM
test_cases5 = [
    # 1) Constant function → should merge to 1 piece
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 5.0), (1.0, 5.0), (2.0, 5.0),
                  (3.0, float('inf'))],
        "epsilon": 0.1
    },

    # 2) Small wiggles within 2*ε → globally mergeable to 1 piece
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.0), (1.0, 1.3), (2.0, 0.8), (3.0, 1.1),
                  (4.0, float('inf'))],
        "epsilon": 0.5  # max-min = 0.5; 2*ε = 1.0 ⇒ mergeable
    },

    # 3) Alternating high/low just beyond mergeability → forces many cuts
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.9  # max-min = 2.0 > 2*ε = 1.8 ⇒ cannot merge all
    },

    # 4) Gentle staircase: local jumps ≤ ε but global drift > 2*ε
    #    Greedy may over-merge then split suboptimally.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.4), (2.0, 0.8), (3.0, 1.2),
                  (4.0, float('inf'))],
        "epsilon": 0.5  # global range = 1.2 > 1.0 ⇒ needs ≥2 pieces
    },

    # 5) Two near-equal change points in x (precision near ties)
    #    Tests handling of very short middle segment.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 2.0), (1.000001, 0.0), (2.0, 2.0),
                  (3.0, float('inf'))],
        "epsilon": 0.6  # max-min = 2.0 > 1.2 ⇒ cannot merge everything
    },

    # 6) Short, tall spike that SHOULD be absorbable with large ε
    #    Some algorithms incorrectly isolate spikes even when mergeable.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 3.0), (2.0, 0.0),
                  (3.0, float('inf'))],
        "epsilon": 1.6  # range = 3.0 ≤ 2*ε = 3.2 ⇒ mergeable to 1 piece
    },

    # 7) Same spike but ε too small → optimal is to split (not 3 pieces)
    #    Checks that algorithm merges the two 0-plateaus together.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 2.0), (2.0, 0.0),
                  (3.0, float('inf'))],
        "epsilon": 0.4  # range = 2.0 > 0.8 ⇒ best is 2 pieces (0-plateaus + spike)
    },

    # 8) Exactly-on-the-boundary case (max-min == 2*ε)
    #    Off-by-one / strict-inequality bugs show up here.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.6), (2.0, 0.0), (3.0, 0.6), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.3  # range = 0.6 == 2*ε ⇒ should be mergeable
    },

    # 9) Large-magnitude values (numeric stability / scaling)
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1e9), (1.0, 1e9 + 0.5), (2.0, 1e9),
                  (3.0, float('inf'))],
        "epsilon": 1.0  # range = 0.5 ≤ 2*ε = 2.0 ⇒ mergeable
    },

    # 10) Long plateau then mild tail shift that SHOULD still merge globally
    #     Greedy “close segment early” bugs often split at the tail.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0),
                  (5.0, 1.1),
                  (6.0, float('inf'))],
        "epsilon": 0.6  # range = 1.1 ≤ 1.2 ⇒ mergeable to 1 piece
    },
]
#Iteration6 3:52PM
test_cases6 = [
    # 1) Constant function repeated: should compress to 1 piece even with epsilon = 0.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 3.0), (1.0, 3.0), (2.0, 3.0), (3.0, 3.0),
                  (4.0, float("inf"))],
        "epsilon": 0.0
    },

    # 2) Two-level signal with jump < 2ε: globally mergeable to a single piece.
    # max-min = 0.9, 2ε = 1.0  ⇒ mergeable.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 0.9),
                  (2.0, float("inf"))],
        "epsilon": 0.5
    },

    # 3) Narrow, tall spike: width is tiny but L∞ cares only about amplitude ⇒ needs ≥2 pieces.
    # max-min = 2.0, 2ε = 1.0  ⇒ not mergeable to 1.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 2.0), (2.0, 0.0),
                  (3.0, float("inf"))],
        "epsilon": 0.5
    },

    # 4) Alternating small oscillations, globally within 2ε: greedy splitters can fail here.
    # range = 0.8, 2ε = 1.0  ⇒ single-piece approximation exists.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.1), (1.0, 0.9), (2.0, 0.2), (3.0, 0.8),
                  (4.0, float("inf"))],
        "epsilon": 0.5
    },

    # 5) Alternating large oscillations, range > 2ε: cannot compress to 1; optimal is >1 piece.
    # range = 1.4, 2ε = 1.0  ⇒ at least 2 pieces needed.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 1.4), (2.0, 0.0), (3.0, 1.4),
                  (4.0, float("inf"))],
        "epsilon": 0.5
    },

    # 6) “Just-above” threshold: tiny level shift barely exceeding 2ε ⇒ should force a split.
    # range = 0.6, 2ε = 0.5  ⇒ not mergeable to 1.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 2.0), (2.0, 2.6), (4.0, 2.0),
                  (5.0, float("inf"))],
        "epsilon": 0.25
    },

    # 7) Exact boundary case range = 2ε: numerically tricky; should still be mergeable to 1 piece.
    # range = 1.0, 2ε = 1.0  ⇒ mergeable (test for off-by-one / tolerance bugs).
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 5.0), (1.0, 6.0), (2.0, 5.5),
                  (3.0, float("inf"))],
        "epsilon": 0.5
    },

    # 8) Two tight clusters far apart: optimal is exactly 2 pieces (cluster compression).
    # Cluster A range ≈ 0.09 ≤ 2ε; Cluster B range ≈ 0.05 ≤ 2ε; gap ≈ 1.25 > 2ε.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.00), (0.5, 0.05), (1.0, -0.04),
                  (2.0, 1.20), (2.5, 1.25),
                  (3.0, float("inf"))],
        "epsilon": 0.10
    },

    # 9) Strictly increasing large steps: each jump exceeds 2ε ⇒ optimal is 3 distinct pieces.
    # Differences 1.2 > 0.6 = 2ε across neighbors.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 1.2), (2.0, 2.4),
                  (3.0, float("inf"))],
        "epsilon": 0.30
    },

    # 10) Ultra-short middle spike (domain width ~0); amplitude >> 2ε ⇒ requires its own piece.
    # Tests algorithms that (incorrectly) ignore spikes due to tiny width.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1e-9, 3.0), (1.0, 0.0),
                  (2.0, float("inf"))],
        "epsilon": 0.4  # 2ε = 0.8, spike amplitude 3.0 ⇒ not mergeable across
    },
]
#Iteration7
test_cases7 = [
    # 1) Trivial constant signal — should compress to exactly 1 piece for any ε ≥ 0
    {
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 2.0), (1.0, 2.0), (3.0, float("inf"))],
        "epsilon": 0.0
    },

    # 2) Borderline merge: total range == 2ε (exact-touch case). Single piece is just feasible.
    # Values span [1.0, 2.0], ε = 0.5 ⇒ max deviation to midpoint is 0.5.
    {
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 1.0), (1.0, 2.0), (2.0, float("inf"))],
        "epsilon": 0.5
    },

    # 3) Small oscillations entirely within ε — algorithm should merge all into 1 piece.
    # Range 0.95..1.05, ε = 0.06 ⇒ max deviation ≤ 0.05 < ε.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 1.00), (0.4, 1.05), (0.8, 0.97), (1.2, 1.02), (1.6, 0.95),
                  (2.0, float("inf"))],
        "epsilon": 0.06
    },

    # 4) Alternating spikes beyond ε — nothing can merge; optimal uses all pieces.
    # Adjacent differences ≥ 1.0 with ε = 0.3.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 1.2), (2.0, 0.0), (3.0, 1.2), (4.0, 0.0),
                  (5.0, float("inf"))],
        "epsilon": 0.3
    },

    # 5) Staircase (monotone). With ε large enough, multiple steps can merge; too small, they can’t.
    # Here ε = 0.6 allows merging groups but not all into one.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 0.7), (2.0, 1.4), (3.0, 2.1), (4.0, 2.8),
                  (5.0, float("inf"))],
        "epsilon": 0.6
    },

    # 6) Single narrow outlier just outside ε — forces a short middle segment around the outlier.
    # Baseline ~0, outlier 0.7 with ε = 0.3 (since 0.7 > 2ε=0.6, one piece can’t cover all).
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 0.0), (2.0, 0.7), (3.0, 0.0), (4.0, 0.0),
                  (5.0, float("inf"))],
        "epsilon": 0.3
    },

    # 7) Valley exactly at ε from a feasible single-mean — just-feasible one-piece case.
    # High 2.0, low 1.0; midpoint 1.5; max deviation 0.5 = ε.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 2.0), (1.0, 1.0), (2.0, 2.0),
                  (3.0, float("inf"))],
        "epsilon": 0.5
    },

    # 8) Many tiny segments (pathological granularity). Range small but nonzero; should still merge to 1.
    # Range 1.00..1.08 with ε = 0.05 ⇒ choose a representative ≈1.04, max deviation 0.04 < ε.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.00, 1.00), (0.10, 1.02), (0.20, 1.04), (0.30, 1.06), (0.40, 1.08),
                  (0.50, 1.05), (0.60, 1.03), (0.70, 1.01),
                  (0.80, float("inf"))],
        "epsilon": 0.05
    },

    # 9) Two plateaus separated by a short bridge just within ε — should merge all into 1 piece despite the bridge.
    # Low 0.0, bridge 0.4, high 0.8 with ε = 0.4 (range 0.8 = 2ε exactly).
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 0.0), (1.1, 0.4), (1.2, 0.8), (2.0, 0.8),
                  (3.0, float("inf"))],
        "epsilon": 0.4
    },

    # 10) Large coordinate gaps (x-spacing irrelevant under L∞) with wide value range.
    # Must split by value, not by distance in x. ε = 0.25; range [0,1] forces ≥3 pieces optimally.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.00), (10.0, 0.50), (100.0, 1.00),
                  (1000.0, float("inf"))],
        "epsilon": 0.25
    },
]
#Iteration8
test_cases8 = [
    {
        # 1) Completely flat function → optimal is 1 piece for any ε > 0.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, float("inf"))],
        "epsilon": 0.3,
        "note": "All y equal; checks trivial merge to a single piece."
    },
    {
        # 2) Single jump exactly at 2ε → boundary case: still mergeable to 1 piece.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 1.0), (2.0, float("inf"))],
        "epsilon": 0.5,
        "note": "Jump size = 1.0 = 2ε; algorithm should allow single-piece fit."
    },
    {
        # 3) Oscillations within ε around baseline → range ≤ 2ε → 1 piece.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 0.4), (2.0, -0.3), (3.0, 0.2), (4.0, float("inf"))],
        "epsilon": 0.5,
        "note": "Range = 0.7 ≤ 2ε=1.0; everything should merge."
    },
    {
        # 4) Short, tall spike (very narrow middle interval) → spike must be separate.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (0.001, 3.0), (1.0, 0.0), (2.0, float("inf"))],
        "epsilon": 0.5,
        "note": "Spike height 3.0 >> 2ε; optimal = 2 pieces (baseline + spike)."
    },
    {
        # 5) Staircase with small steps; pairwise groups feasible, global merge not.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 0.3), (2.0, 0.6), (3.0, 0.9), (4.0, float("inf"))],
        "epsilon": 0.25,
        "note": "2ε=0.5. Best is two groups: {0,0.3} and {0.6,0.9} → 2 pieces."
    },
    {
        # 6) Near-boundary precision case slightly exceeding 2ε by ~2e-7.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 1.0000002), (2.0, float("inf"))],
        "epsilon": 0.5,
        "note": "Range=1.0000002 > 2ε=1.0 by a hair; should require 2 pieces."
    },
    {
        # 7) Values hitting exactly ±ε around 0 → total range = 2ε → 1 piece.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, -0.5), (1.0, 0.0), (2.0, 0.5), (3.0, float("inf"))],
        "epsilon": 0.5,
        "note": "Range=1.0=2ε; boundary merge case to single piece."
    },
    {
        # 8) Two-by-two grouping where adjacent pairs merge exactly at the threshold.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 1.1), (2.0, 2.2), (3.0, 3.3), (4.0, float("inf"))],
        "epsilon": 0.55,
        "note": "Step=1.1=2ε. Optimal merges into two pieces: {0,1.1} and {2.2,3.3}."
    },
    {
        # 9) Outlier at the start; rest flat. Greedy pitfalls if not careful.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 5.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, float("inf"))],
        "epsilon": 0.5,
        "note": "Outlier must be its own piece; optimal = 2 pieces."
    },
    {
        # 10) Many values with total range exactly 2ε spread irregularly.
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 1.0), (0.5, 1.4), (1.5, 1.2), (2.5, 1.3), (3.5, 1.0), (4.5, float("inf"))],
        "epsilon": 0.2,
        "note": "Range=0.4=2ε; despite irregular order, should merge to 1 piece."
    },
]
#Iteration9
test_cases9 = [
    # 1) Completely flat function → should compress to 1 piece for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 3.0], [5.0, 3.0], [10.0, 3.0],
                  [15.0, float('inf')]],
        "epsilon": 0.1
    },

    # 2) Two-level signal with jump exactly at the 2ε boundary → still mergeable
    # |y2 - y1| = 2ε ⇒ one piece possible if the algorithm handles the boundary correctly
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0], [5.0, 2.0],  # Δ=1.0; set ε=0.5 ⇒ 2ε=1.0
                  [10.0, float('inf')]],
        "epsilon": 0.5
    },

    # 3) Small oscillations fully within 2ε → should merge to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 10.0], [2.0, 10.6], [4.0, 9.6], [6.0, 10.4], [8.0, 9.7],
                  [10.0, float('inf')]],
        "epsilon": 0.6  # range ≈ 1.0 ≤ 2ε (1.2)
    },

    # 4) Alternating spikes that slightly exceed 2ε → must split
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.3], [2.0, 0.0], [3.0, 1.3], [4.0, 0.0],
                  [5.0, float('inf')]],
        "epsilon": 0.6  # 2ε=1.2 < 1.3 → cannot merge across spikes
    },

    # 5) Very narrow high spike (short interval but tall) → cannot “average it away”
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.0], [1.001, 5.0], [1.002, 0.0], [3.0, 0.0],
                  [4.0, float('inf')]],
        "epsilon": 1.0  # spike height 5.0 >> 2ε → needs its own piece despite tiny width
    },

    # 6) Staircase with mixed steps: some ≤ 2ε (mergeable), some > 2ε (must split)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0], [2.0, 2.6],  # Δ=0.6 ≤ 2ε (with ε=0.35 → 2ε=0.7) → mergeable
                  [4.0, 3.4],              # Δ=0.8 > 0.7 → split here
                  [6.0, 3.8],              # Δ=0.4 ≤ 0.7 → could merge with 3.4
                  [8.0, 4.7],              # Δ=0.9 > 0.7 → split
                  [10.0, float('inf')]],
        "epsilon": 0.35
    },

    # 7) Floating-point nasties near boundary: values like 0.1 can expose rounding bugs
    # Here max-min = 1.0000000000000002 ≈ 1.0; with ε=0.5 the boundary is tight
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.3], [2.0, 0.7], [3.0, 1.0000000000000002],
                  [4.0, float('inf')]],
        "epsilon": 0.5  # tests robust use of isclose / numerical tolerances at 2ε boundary
    },

    # 8) Long plateau, brief bridge, then plateau at a close level: should become 1–2 pieces
    # depending on ε; here crafted so overall range ≤ 2ε → single piece is feasible
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 5.0], [10.0, 5.0], [10.5, 5.8], [11.0, 6.0], [20.0, 6.0],
                  [25.0, float('inf')]],
        "epsilon": 0.5  # range = 1.0 = 2ε → mergeable if boundary handled correctly
    },

    # 9) Repeated equal levels with intervening noise within ε → should coalesce
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [-5.0, -2.0], [-1.0, -2.05], [0.0, -2.0], [1.0, -1.96], [2.0, -2.0],
                  [3.0, float('inf')]],
        "epsilon": 0.05  # all deviations within ±ε around -2.0 → single piece expected
    },

    # 10) Mixed signs and large magnitude jump; also includes negative x’s
    # Ensures algorithm handles extremes and sign changes correctly
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [-10.0, -100.0], [-2.0, -99.2], [0.0, 50.0], [5.0, 49.4], [12.0, 50.1],
                  [20.0, float('inf')]],
        "epsilon": 0.4  # left block range 0.8 ≤ 2ε → mergeable; jump to ~50 is >> 2ε → split
    },
]

#Iteration10
test_cases10 = [
    # 1) Already flat function (sanity check). With any epsilon >= 0, minimum is 1 piece.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 2.0], [5.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1
    },

    # 2) Threshold-tight merge (range = 2*epsilon). Should merge into a single piece.
    # Values: 0.0 and 1.2; epsilon = 0.6 -> max-min = 1.2 = 2*epsilon -> 1 piece.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [1.0, 1.2], [2.0, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 1
    },

    # 3) Just-over-threshold (range > 2*epsilon). Must split into two pieces.
    # Values: 0.0 and 1.21; epsilon = 0.6 -> 1.21 > 1.2 -> cannot merge -> 2 pieces.
    {
        "pc_fx": [[-float('inf'), float('inf')], [0.0, 0.0], [1.0, 1.21], [2.0, float('inf')]],
        "epsilon": 0.6,
        "expected_min_pieces": 2
    },

    # 4) Strict alternation (worst case for merging when 2*epsilon < level gap).
    # Gap = 1.0, epsilon = 0.49 -> 2*epsilon = 0.98 < 1.0, so no 0/1 merge anywhere.
    # Optimal must keep each original change -> 6 pieces.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.0], [2.0, 0.0],
                  [3.0, 1.0], [4.0, 0.0], [5.0, 1.0],
                  [6.0, float('inf')]],
        "epsilon": 0.49,
        "expected_min_pieces": 6
    },

    # 5) Same pattern, but just enough tolerance to collapse everything.
    # Gap = 1.0, epsilon = 0.51 -> 2*epsilon = 1.02 >= 1.0 -> all mergeable -> 1 piece.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.0], [2.0, 0.0],
                  [3.0, 1.0], [4.0, 0.0], [5.0, 1.0],
                  [6.0, float('inf')]],
        "epsilon": 0.51,
        "expected_min_pieces": 1
    },

    # 6) Tiny jitter within tolerance across many segments (tests consolidation over long runs).
    # Range = max(0.12) - min(-0.08) = 0.20; epsilon = 0.1 -> 2*epsilon = 0.2 -> 1 piece.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.02], [1.0, 0.07], [2.0, -0.08],
                  [3.0, 0.05], [4.0, 0.12], [5.0, 0.00],
                  [6.0, float('inf')]],
        "epsilon": 0.10,
        "expected_min_pieces": 1
    },

    # 7) Monotone drift with cumulative span exceeding 2*epsilon.
    # Values: 0.0, 0.4, 0.8, 1.2; epsilon = 0.3 -> 2*epsilon = 0.6.
    # Best is to cut into two groups: [0.0,0.4] and [0.8,1.2] -> 2 pieces.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.4], [2.0, 0.8], [3.0, 1.2],
                  [4.0, float('inf')]],
        "epsilon": 0.30,
        "expected_min_pieces": 2
    },

    # 8) Narrow spike outlier: cannot be absorbed when 2*epsilon < spike gap; else collapses.
    # Here use epsilon small so spike forces a second piece.
    # Values mostly 0.0 with one 3.0; epsilon = 1.49 -> 2*epsilon = 2.98 < 3.0 -> 2 pieces.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.0], [2.0, 3.0], [3.0, 0.0], [4.0, 0.0],
                  [5.0, float('inf')]],
        "epsilon": 1.49,
        "expected_min_pieces": 2
    },

    # 9) Consecutive identical levels should not cause extra segments.
    # Even with epsilon = 0, consecutive identical-value pieces can be one piece in the approximation.
    # Optimal result: a single piece at value 5.0 -> 1 piece.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 5.0], [1.0, 5.0], [2.0, 5.0], [3.0, 5.0],
                  [4.0, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1
    },

    # 10) Endpoint sensitivity: big jump only at the last interval.
    # With epsilon too small to cover the final jump, optimal is to keep a long first piece and a short last piece.
    # Values: 0.0,...,0.0, then 2.0; epsilon = 0.9 -> 2*epsilon = 1.8 < 2.0 -> 2 pieces.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [2.0, 0.0], [4.0, 0.0], [6.0, 2.0],
                  [7.0, float('inf')]],
        "epsilon": 0.9,
        "expected_min_pieces": 2
    },
]
#Iteration11
test_cases11 = [
    # 1) Perfectly constant → should collapse to 1 piece even with ε = 0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 3.0], [1, 3.0], [2, 3.0], [3, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "why": "All segments identical; exact merge allowed when ε=0."
    },

    # 2) Small oscillations within ε → 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.06], [2, -0.08], [3, 0.02], [4, float('inf')]],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "why": "Range ≤ 2ε, so a single constant fits under L∞."
    },

    # 3) Big jump far beyond ε → needs ≥ 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 10.0], [2, float('inf')]],
        "epsilon": 1.0,
        "expected_min_pieces": 2,
        "why": "Any single constant has ≥5 error; violates ε=1."
    },

    # 4) Two clusters (tight within) separated by a gap → 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.2],         # cluster A (range 0.2)
                  [2, 5.0], [3, 5.1], [4, 5.0],  # cluster B (range 0.1)
                  [5, float('inf')]],
        "epsilon": 0.3,
        "expected_min_pieces": 2,
        "why": "Each cluster fits within one piece; gap between clusters too large."
    },

    # 5) ε = 0 with alternating values → must keep every change
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0], [4, float('inf')]],
        "epsilon": 0.0,
        "expected_min_pieces": 4,
        "why": "Exact match required; no smoothing allowed."
    },

    # 6) Very large ε → everything collapses to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -3.0], [1, 4.0], [2, -1.0], [3, 2.0], [4, float('inf')]],
        "epsilon": 10.0,
        "expected_min_pieces": 1,
        "why": "Range 7 ≤ 2ε (=20), so one piece suffices."
    },

    # 7) Exactly at the merge boundary (range = 2ε) → still 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 1,
        "why": "Range 1.0 equals 2ε; a single constant (e.g., 0.5) achieves max error ε."
    },

    # 8) Single narrow spike outside ε → 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.0], [2, 2.0], [3, 0.0], [4, float('inf')]],
        "epsilon": 0.4,
        "expected_min_pieces": 2,
        "why": "Spike requires its own piece when ε is small."
    },

    # 9) Gradual drift exceeding 2ε overall, but adjacent pairs within → 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.6], [2, 1.2], [3, float('inf')]],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "why": "Total range 1.2 > 2ε (=1.0), so can’t be 1 piece; first two can merge."
    },

    # 10) Symmetric bumps with a high middle; edge pairs at boundary → 3 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.3], [1, 0.8], [2, 1.3], [3, 0.8], [4, 0.3],
                  [5, float('inf')]],
        "epsilon": 0.25,
        "expected_min_pieces": 3,
        "why": "Edges can pair (range = 0.5 = 2ε), middle peak must stand alone."
    },
]

#Iteration12
test_cases12 = [
    {
        # 1) Constant function — should collapse to 1 piece for any ε ≥ 0
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, float("inf"))],
        "epsilon": 0.0
    },
    {
        # 2) Small wiggles strictly within tolerance band (range < 2ε) — merge to one piece
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 0.4), (2.0, 0.8), (3.0, float("inf"))],
        "epsilon": 0.5  # max-min = 0.8 ≤ 1.0
    },
    {
        # 3) Just-barely over the 2ε boundary — must split at least once
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 1.001), (2.0, 1.001), (3.0, float("inf"))],
        "epsilon": 0.5  # max-min = 1.001 > 1.0
    },
    {
        # 4) Alternating highs/lows within tolerance — temptingly many segments, but still mergeable
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 1.0), (1.0, 1.9), (2.0, 1.1), (3.0, 1.8), (4.0, float("inf"))],
        "epsilon": 0.5  # range = 0.9 ≤ 1.0
    },
    {
        # 5) Exactly at the threshold max-min = 2ε — edge case for ≤ vs <
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 1.2), (2.0, 1.2), (3.0, float("inf"))],
        "epsilon": 0.6  # range = 1.2 == 2ε → should be mergeable if rule is ≤ 2ε
    },
    {
        # 6) Narrow “spike” beyond tolerance on a tiny interval — width should not matter under L∞
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 0.0),
            (0.99, 0.0),
            (1.00, 2.0),   # spike violates tolerance band
            (1.01, 0.0),
            (2.0, float("inf"))
        ],
        "epsilon": 0.4  # spike forces at least one additional piece despite tiny width
    },
    {
        # 7) Long flat then staircase of small steps; cumulative range exceeds 2ε → should split minimally
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 5.0),
            (5.0, 5.0),
            (6.0, 5.7),
            (7.0, 6.1),
            (8.0, 6.6),
            (9.0, float("inf"))
        ],
        "epsilon": 0.5  # range = 1.6 > 1.0; expect ~2–3 pieces depending on grouping
    },
    {
        # 8) Floating-point tightness: values differ by ~2ε ± 1e-12 — tests numerical robustness
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 0.6),
            (1.0, 1.2000000000001),  # slightly over 2ε if ε=0.3?
            (2.0, 0.6000000000000),
            (3.0, float("inf"))
        ],
        "epsilon": 0.3  # careful handling of isclose/rounding determines merging
    },
    {
        # 9) Large magnitudes but small relative variation vs ε — scaling shouldn’t matter for L∞
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 1e6),
            (1.0, 1e6 + 0.3),
            (2.0, 1e6 - 0.4),
            (3.0, 1e6 + 0.2),
            (4.0, float("inf"))
        ],
        "epsilon": 0.5  # range = 0.7 ≤ 1.0 → mergeable despite large baseline
    },
    {
        # 10) Two distant clusters separated by a big jump — minimal answer should be two pieces
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, -2.0),
            (1.0, -2.1),
            (2.0, -1.9),
            (3.0, 3.0),   # big jump
            (4.0, 3.1),
            (5.0, float("inf"))
        ],
        "epsilon": 0.4  # inter-cluster range ≫ 2ε → at least two pieces
    }
]

#Iteration13
test_cases13 = [
    # 1) Trivial constant function → optimal is 1 piece for any ε ≥ 0
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 2.0),
                  (10.0, 2.0),
                  (20.0, 2.0),
                  (25.0, float("inf"))],
        "epsilon": 0.0
    },

    # 2) Threshold case: jump exactly 2ε → still mergeable into 1 piece under L∞
    # |y1 - y2| = 2ε ⇒ with value set to midpoint, max error = ε
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 1.0),
                  (1.0, 2.0),   # jump of 1.0
                  (2.0, 2.0),
                  (3.0, float("inf"))],
        "epsilon": 0.5
    },

    # 3) Just-not-mergeable: jump slightly larger than 2ε → requires 2 pieces
    # |y1 - y2| = 1.01 > 2ε = 1.0
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 1.0),
                  (1.0, 2.01),
                  (2.0, 2.01),
                  (3.0, float("inf"))],
        "epsilon": 0.5
    },

    # 4) Oscillation within a band of width ≤ 2ε → should compress to 1 piece
    # All y in [1.0 - 0.4, 1.0 + 0.4], 2ε = 1.0
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.6),
                  (1.0, 1.3),
                  (2.0, 0.8),
                  (3.0, 1.2),
                  (4.0, 0.9),
                  (5.0, float("inf"))],
        "epsilon": 0.5
    },

    # 5) Narrow spike (width doesn’t matter under L∞): amplitude forces a split
    # Base 0.0, spike 3.0 ⇒ to cover both with one piece, ε ≥ 1.5 is needed; here ε = 0.9 ⇒ must split
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0),
                  (1.0, 3.0),   # spike
                  (1.1, 0.0),
                  (3.0, 0.0),
                  (4.0, float("inf"))],
        "epsilon": 0.9
    },

    # 6) Many alternating runs with large jumps → minimal equals number of runs
    # High/low alternate with |Δ| = 3.0 > 2ε (=2.0) ⇒ cannot merge across transitions
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0),
                  (0.5, 3.0),
                  (1.0, 0.0),
                  (1.5, 3.0),
                  (2.0, 0.0),
                  (2.5, 3.0),
                  (3.0, float("inf"))],
        "epsilon": 1.0
    },

    # 7) Slow drift staying within a 2ε band → compressible to 1 piece
    # Range = 0.8, need 2ε ≥ 0.8 ⇒ ε ≥ 0.4; here ε = 0.5
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (-2.0, 0.0),
                  (0.0, 0.2),
                  (2.0, 0.4),
                  (4.0, 0.6),
                  (6.0, 0.8),
                  (8.0, float("inf"))],
        "epsilon": 0.5
    },

    # 8) Zero tolerance (ε = 0) → must reproduce the original (no merges allowed)
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (-3.0, -1.0),
                  (-1.0, 0.0),
                  (2.0, 2.0),
                  (5.0, -0.5),
                  (7.0, float("inf"))],
        "epsilon": 0.0
    },

    # 9) Boundary-adjacent threshold: first and last markers ignored; edge jump = 2ε
    # The first *actual* piece starts at x = -5.0; jump exactly at threshold
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (-5.0, 4.0),
                  (0.0, 5.0),    # |Δ| = 1.0 = 2ε ⇒ could be merged to 1 piece
                  (6.0, 5.0),
                  (9.0, float("inf"))],
        "epsilon": 0.5
    },

    # 10) Large dynamic range with tiny ε → stresses precision; many pieces required
    # Differences of 10.0 with ε = 1e-6 ⇒ no merges should be allowed
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0),
                  (1.0, 10.0),
                  (2.0, 0.0),
                  (3.0, 10.0),
                  (4.0, 0.0),
                  (5.0, float("inf"))],
        "epsilon": 1e-6
    },
]

#Iteration14
test_cases14 = [
    {
        # 1) Collapse-to-one-piece when full-range < 2ε (strictly inside)
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.9), (2.0, 1.8), (3.0, 0.2),
                  (4.0, float('inf'))],
        "epsilon": 1.0,  # max-min = 1.8 < 2.0 → 1 piece feasible
    },
    {
        # 2) Borderline equality: max-min == 2ε exactly (should still allow 1 piece)
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -1.0), (1.0, 0.0), (2.0, 1.0),
                  (3.0, float('inf'))],
        "epsilon": 1.0,  # max-min = 2.0 == 2ε
    },
    {
        # 3) Just-over-the-threshold: max-min slightly > 2ε (forces ≥2 pieces)
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -1.01), (1.0, 0.0), (2.0, 1.0),
                  (3.0, float('inf'))],
        "epsilon": 1.0,  # max-min = 2.01 > 2ε
    },
    {
        # 4) Isolated spike beyond 2ε between two mergeable plateaus → optimal is 3 pieces (merge left, isolate spike, merge right)
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.1), (2.0, 3.5), (3.0, 0.2), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.6,  # left/right plateaus fit within 2ε=1.2; spike forces splits
    },
    {
        # 5) Monotone staircase where global grouping beats greedy local breaks
        # Example: group first three (range 1.8 ≤ 2ε), last one alone → 2 pieces optimal.
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.9), (2.0, 1.8), (3.0, 2.7),
                  (4.0, float('inf'))],
        "epsilon": 1.0,  # full range 2.7 > 2; optimal grouping is [0,1.8] | [2.7]
    },
    {
        # 6) Floating-point tight case: values mathematically at the boundary 2ε
        # Tiny perturbation may trick algorithms without robust comparisons.
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.0 - 1e-12), (2.0, 2.0 - 2e-12),
                  (3.0, float('inf'))],
        "epsilon": 1.0,  # intended max-min == 2ε within FP noise
    },
    {
        # 7) Redundant consecutive constant segments (should merge regardless of ε)
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.8), (4.0, 2.9),
                  (5.0, float('inf'))],
        "epsilon": 0.4,  # first three identical; last two within 0.1 range (mergeable)
    },
    {
        # 8) Very small ε → essentially no merging unless values exactly match
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -2.0), (0.5, -1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 2.0),
                  (2.5, float('inf'))],
        "epsilon": 1e-6,  # any difference > 0 forces its own piece
    },
    {
        # 9) Two far-separated clusters separated by a big spike
        # Each cluster’s range ≤ 2ε; cannot merge across the spike → expect 3 pieces.
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -0.1), (1.0, 0.1),   # cluster A (range 0.2)
                  (2.0, 4.0),               # spike
                  (3.0, 0.0), (4.0, 0.2),   # cluster B (range 0.2)
                  (5.0, float('inf'))],
        "epsilon": 0.2,  # 2ε = 0.4 fits each cluster, not across spike
    },
    {
        # 10) Alternating near-threshold highs/lows to test stable band tracking
        # Adjacent differences hover around 2ε; optimal grouping should alternate.
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.01), (2.0, -0.99), (3.0, 1.02), (4.0, -0.98),
                  (5.0, float('inf'))],
        "epsilon": 1.0,  # swings ~2; careful handling of boundary conditions needed
    },
]

#Iteration15
test_cases15 = [
    # 1) All-constant values → should compress to 1 piece for any ε ≥ 0
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0],
                  [5.0, 2.0],
                  [10.0, 2.0],
                  [12.0, float('inf')]],
        "epsilon": 0.1
    },

    # 2) Two-level signal exactly at merge boundary: (y_range = 2ε) → mergable into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [1.0, 1.2],
                  [2.0, float('inf')]],
        "epsilon": 0.6
    },

    # 3) Two-level signal *just over* merge boundary: (y_range = 2ε + 5e-7) → must be 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [1.0, 1.2000005],
                  [2.0, float('inf')]],
        "epsilon": 0.6
    },

    # 4) Alternating high/low levels far beyond tolerance (cannot merge any adjacent pieces)
    #    Stresses that minimal = original piece count when 2ε < |Δ|
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [1.0, 10.0],
                  [2.0, 0.0],
                  [3.0, 10.0],
                  [4.0, 0.0],
                  [5.0, 10.0],
                  [6.0, float('inf')]],
        "epsilon": 4.9  # 2ε = 9.8 < 10, so no merges allowed
    },

    # 5) Narrow spike: interval length is tiny but L∞ ignores length → spike forces an extra piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [4.0, 0.0],
                  [4.0000001, 3.0],
                  [4.0000002, 0.0],
                  [8.0, 0.0],
                  [9.0, float('inf')]],
        "epsilon": 1.0  # 2ε = 2 < 3, spike cannot be absorbed
    },

    # 6) Staircase within one tolerance window: all values lie inside a 2ε band → compress to 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [2.0, 0.5],
                  [4.0, 0.9],
                  [6.0, 1.2],
                  [7.0, float('inf')]],
        "epsilon": 0.7  # y_range = 1.2 ≤ 2ε = 1.4 → mergable
    },

    # 7) Floating-point “noise”: near-identical levels; tests np.isclose / boundary handling
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.0],
                  [1.0, 1.0000002],
                  [2.0, 0.9999997],
                  [3.0, float('inf')]],
        "epsilon": 1e-6  # y_range ≈ 5e-7 ≤ 2e-6 → mergable
    },

    # 8) Mixed negative/positive with wide swings → cannot collapse to 1; likely needs 3 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -2.0],
                  [1.5, 1.0],
                  [3.0, -1.0],
                  [4.5, float('inf')]],
        "epsilon": 1.0  # y_range = 3 between -2 and 1 (2ε = 2) → extra pieces required
    },

    # 9) Near-tolerance triad: first two can merge; third just tips overall range over 2ε
    #    Encourages minimal = 2 pieces, not 1
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0],
                  [2.0, 1.19],    # close to 2ε but inside
                  [4.0, -0.02],   # pushes total range to 1.21 > 2ε (=1.2)
                  [6.0, float('inf')]],
        "epsilon": 0.6
    },

    # 10) Tiny-width segments around tolerance boundary (stress handling of very small intervals)
    #     First two within 2ε; last one forces split due to slight excess over boundary
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0],
                  [1e-9, 2.5999999],     # Δ = 0.5999999 within ε=0.6 (pair-wise ok)
                  [2e-9, 3.200001],      # overall range from 2.0 to 3.200001 = 1.200001 > 2ε
                  [1.0, float('inf')]],
        "epsilon": 0.6
    },
]

#Iteration16
test_cases16 = [
    # 1) Flat function → everything should merge to 1 piece
    {
        "pc_fx": [(-float("inf"), float("inf")), (0, 2.0), (1, 2.0), (2, 2.0), (3, float("inf"))],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
    },

    # 2) Single small jump: range == 2*ε → still mergeable into 1 piece (threshold case)
    {
        "pc_fx": [(-float("inf"), float("inf")), (0, 0.0), (1, 0.9), (2, float("inf"))],
        "epsilon": 0.45,  # 2*ε = 0.9 == range
        "expected_min_pieces": 1,
    },

    # 3) Single jump just over the threshold: range > 2*ε → must be 2 pieces
    {
        "pc_fx": [(-float("inf"), float("inf")), (0, 0.0), (1, 1.1000001), (2, float("inf"))],
        "epsilon": 0.55,  # 2*ε = 1.10 < 1.1000001 (nudges numerical robustness)
        "expected_min_pieces": 2,
    },

    # 4) Alternating highs/lows with range slightly > 2*ε → greedy merges can fail; needs many splits
    {
        "pc_fx": [(-float("inf"), float("inf")), (0, 0.0), (1, 1.0), (2, 0.0), (3, 1.0), (4, float("inf"))],
        "epsilon": 0.49,  # 2*ε = 0.98 < 1.0
        "expected_min_pieces": 4,
    },

    # 5) Narrow spike far from neighbors: width is tiny but L∞ cares only about value → isolate spike
    {
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 0.0),
            (0.99, 0.0),
            (1.00, 3.0),   # spike
            (1.01, 0.0),
            (2.0, float("inf")),
        ],
        "epsilon": 0.9,   # 2*ε = 1.8; |3.0 - 0.0| = 3.0 > 1.8 → spike requires its own piece
        "expected_min_pieces": 3,
    },

    # 6) Gradual drift contained within 2*ε overall → compress to 1 piece
    {
        "pc_fx": [(-float("inf"), float("inf")), (0, 0.0), (1, 0.2), (2, 0.3), (3, 0.1), (4, float("inf"))],
        "epsilon": 0.2,   # range = 0.3 ≤ 0.4
        "expected_min_pieces": 1,
    },

    # 7) Large jump right at the start; also checks boundary sentinels are ignored
    {
        "pc_fx": [(-float("inf"), float("inf")), (0, -2.0), (1, 2.0), (2, 2.0), (3, float("inf"))],
        "epsilon": 1.9,   # 2*ε = 3.8; range = 4.0 > 3.8 → at least 2 pieces
        "expected_min_pieces": 2,
    },

    # 8) Exact-on-threshold symmetric band: max - min = 2*ε → mergeable into 1 (tests equality handling)
    {
        "pc_fx": [(-float("inf"), float("inf")), (0, -0.5), (1, 0.0), (2, 0.5), (3, float("inf"))],
        "epsilon": 0.5,   # range = 1.0 == 2*ε
        "expected_min_pieces": 1,
    },

    # 9) Tiny overshoot beyond threshold (floating point corner): forces an extra piece
    {
        "pc_fx": [(-float("inf"), float("inf")), (0, 0.0), (1, 1.0000002), (2, float("inf"))],
        "epsilon": 0.5,   # 2*ε = 1.0; range = 1.0000002 → must split
        "expected_min_pieces": 2,
    },

    # 10) Two tight clusters far apart: each cluster collapses to 1, but clusters require a split → total 2
    {
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 0.0),
            (1.0, 0.2),
            (2.0, -0.1),
            (3.0, 0.1),     # cluster A (range 0.3)
            (4.0, 2.7),
            (5.0, 3.0),
            (6.0, 2.9),     # cluster B (range 0.3)
            (7.0, float("inf")),
        ],
        "epsilon": 0.6,   # 2*ε = 1.2; inter-cluster gap ~2.8 → need 2 pieces total
        "expected_min_pieces": 2,
    },
]

#Iteration17

test_cases17 = [
    # 1) Single constant piece (baseline). Optimal is 1 piece for any ε ≥ 0.
    {
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 2.0), (10.0, float("inf"))],
        "epsilon": 0.0,
    },

    # 2) Two pieces with jump < 2ε → can be merged to 1 piece (greedy should not over-split).
    # y1=1.0, y2=1.9, ε=0.5 ⇒ span=0.9 ≤ 2ε=1.0
    {
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 1.0), (5.0, 1.9), (10.0, float("inf"))],
        "epsilon": 0.5,
    },

    # 3) Boundary case: jump exactly 2ε (algorithm must allow merge at equality).
    # y1=0.0, y2=1.0, ε=0.5 ⇒ span=1.0 = 2ε
    {
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (3.0, 1.0), (6.0, float("inf"))],
        "epsilon": 0.5,
    },

    # 4) Alternating high-low sequence where local greedy merges can be suboptimal.
    # 0,2,0,2 with ε=0.9 (span=2 > 2ε=1.8 → cannot compress all to one; optimal grouping matters).
    {
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 0.0), (2.0, 2.0), (4.0, 0.0), (6.0, 2.0),
            (8.0, float("inf")),
        ],
        "epsilon": 0.9,
    },

    # 5) Narrow spike (amplitude matters, not width): 0 → 5 → 0 with ε=2.5.
    # Entire range can be approximated by y=2.5 with max error 2.5 (exactly ε).
    {
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 0.0), (1.0, 5.0), (2.0, 0.0), (3.0, float("inf"))],
        "epsilon": 2.5,
    },

    # 6) Staircase with small steps; cannot merge all, but optimal grouping should be minimal.
    # Values: 0, 0.4, 0.8, 1.2 with ε=0.5 → span=1.2, midpoint 0.6 gives error 0.6 > ε, so need ≥2 pieces.
    {
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 0.0), (2.0, 0.4), (4.0, 0.8), (6.0, 1.2),
            (8.0, float("inf")),
        ],
        "epsilon": 0.5,
    },

    # 7) Tiny jitter around a level (floating-point robustness).
    # Values ~1.0 ± 1e-7; ε=1e-6 should allow a single merged piece despite roundoff.
    {
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 1.0000000), (1.0, 0.9999999), (2.0, 1.0000001), (3.0, 1.0000000),
            (4.0, float("inf")),
        ],
        "epsilon": 1e-6,
    },

    # 8) Long flat then a big jump; must place a cut exactly when span exceeds 2ε.
    # 0,0,0, then 1.1 with ε=0.5 → span becomes 1.1 > 1.0 at the last piece → split before jump.
    {
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.0, 0.0), (3.0, 0.0), (6.0, 0.0), (9.0, 1.1),
            (12.0, float("inf")),
        ],
        "epsilon": 0.5,
    },

    # 9) Extreme symmetric values; boundary equality again.
    # -100 and 100 with ε=100 → mid=0 gives max error 100 = ε → can compress to 1 piece.
    {
        "pc_fx": [(-float("inf"), float("inf")), (0.0, -100.0), (5.0, 100.0), (10.0, float("inf"))],
        "epsilon": 100.0,
    },

    # 10) Many rapid oscillations; equality case permits full compression.
    # 0/1 alternating, ε=0.5 → span=1, mid=0.5 gives error 0.5 = ε → 1 piece is feasible.
    {
        "pc_fx": [
            (-float("inf"), float("inf")),
            (0.000, 0.0), (0.001, 1.0), (0.002, 0.0), (0.003, 1.0),
            (0.004, 0.0), (0.005, 1.0),
            (0.006, float("inf")),
        ],
        "epsilon": 0.5,
    },
]

#Iteration18
test_cases18 = [

    # 1) Trivial constant function: should compress to 1 piece even with ε=0.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 2.0), (1.0, 2.0), (2.0, 2.0),
                  (3.0, float('inf'))],
        "epsilon": 0.0
    },

    # 2) Exact 2ε boundary (tie case): range == 2ε → merge should be just barely allowed.
    # y jumps 0 → 1.2 with ε=0.6 (2ε=1.2).
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (2.0, 1.2), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.6
    },

    # 3) Alternating over-threshold oscillation: forces multiple pieces (1.3 > 2ε=1.2).
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.3), (2.0, 0.0), (3.0, 1.3),
                  (4.0, float('inf'))],
        "epsilon": 0.6
    },

    # 4) Staircase with total range < 2ε: globally mergeable (should become 1 piece).
    # Range = 1.5, ε=0.8 → 2ε=1.6.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5),
                  (4.0, float('inf'))],
        "epsilon": 0.8
    },

    # 5) Narrow high spike: amplitude exceeds 2ε so spike must remain its own piece.
    # Range with spike = 5, ε=2 → 2ε=4 (insufficient to cover), even if interval is tiny.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 5.0), (1.1, 0.0),
                  (2.0, float('inf'))],
        "epsilon": 2.0
    },

    # 6) Pairwise OK but globally not: adjacent jumps ≤ 2ε, total range > 2ε → needs ≥2 pieces.
    # 0 → 1.1 → 2.2 with ε=0.6: each step 1.1 ≤ 1.2, but global 2.2 > 1.2.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.1), (2.0, 2.2),
                  (3.0, float('inf'))],
        "epsilon": 0.6
    },

    # 7) Endpoint-threshold jump at the tail: merge decision hinging on left-continuity.
    # Last plateau is exactly 2ε away (1.2 with ε=0.6).
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.0), (2.0, 1.2), (3.0, 1.2),
                  (4.0, float('inf'))],
        "epsilon": 0.6
    },

    # 8) Floating-point tightness: barely over the 2ε boundary by 1e-10 → should NOT merge.
    # diff = 0.6000000001, ε=0.3 → 2ε=0.6.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.6000000001), (2.0, 0.0),
                  (3.0, float('inf'))],
        "epsilon": 0.3
    },

    # 9) Long gentle drift within ε followed by a big jump: first block should merge, then split.
    # Drift range 0.6 < 2ε=1.0 (ε=0.5), jump to 2.0 forces a new piece.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.3), (2.0, 0.5), (3.0, 0.6), (4.0, 2.0),
                  (5.0, float('inf'))],
        "epsilon": 0.5
    },

    # 10) Redundant breakpoints with microscopic jitter: should still collapse to 1 piece.
    # Jitter ~1e-9, ε=1e-6.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.0), (0.5, 1.000000001), (1.0, 0.999999999),
                  (1.5, 1.0), (2.0, 1.0000000005),
                  (3.0, float('inf'))],
        "epsilon": 1e-6
    },
]

#Iteration19

test_cases19 = [
    # 1) Constant function → optimal should be 1 piece even with ε=0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 2.5], [1, 2.5], [2, 2.5], [3, float('inf')]],
        "epsilon": 0.0,
    },

    # 2) Single small jump with range <= 2ε → merge to 1 piece
    # |1.8 - 1.0| = 0.8 ≤ 2*0.5 = 1.0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.8], [2, float('inf')]],
        "epsilon": 0.5,
    },

    # 3) Jump just over the threshold → cannot merge
    # |2.01 - 1.0| = 1.01 > 2*0.5 = 1.0
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 2.01], [2, float('inf')]],
        "epsilon": 0.5,
    },

    # 4) Many oscillations exactly at the 2ε boundary → should still merge (≤ 2ε is allowed)
    # max-min = 0.9, 2ε = 0.9
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.9], [2, 0.0], [3, 0.9], [4, float('inf')]],
        "epsilon": 0.45,
    },

    # 5) Non-transitive mergeability (A~B and B~C but A!~C) → optimal is 2 pieces
    # |0.8-0.0|=0.8 ≤1.0, |1.6-0.8|=0.8 ≤1.0, but |1.6-0.0|=1.6 >1.0 (ε=0.5)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.8], [2, 1.6], [3, float('inf')]],
        "epsilon": 0.5,
    },

    # 6) Narrow spike between long plateaus → spike must stand alone (width irrelevant under L∞)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 5.0], [1.001, 0.0], [5, float('inf')]],
        "epsilon": 1.0,
    },

    # 7) Alternating large sign flips with tight ε → no merges
    # diffs = 2 > 2*0.4 = 0.8
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1.0], [1, 1.0], [2, -1.0], [3, 1.0], [4, float('inf')]],
        "epsilon": 0.4,
    },

    # 8) Huge ε that swallows everything → optimal is 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -3.0], [1, 1.0], [2, 4.0], [3, -2.0], [4, float('inf')]],
        "epsilon": 10.0,
    },

    # 9) ε=0 but repeated equal values → merges only identical runs (tests strict equality handling)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.0], [2, 2.0], [3, 2.0], [4, 1.0], [5, float('inf')]],
        "epsilon": 0.0,
    },

    # 10) Numerical stability at boundary: |Δ| = 2ε exactly (useful for isclose/tolerance logic)
    # |1.000000001 - 1.0| = 1e-9, 2ε = 1e-9
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.000000001], [2, float('inf')]],
        "epsilon": 5e-10,
    },
]

#Iteration20
test_cases20 = [
    # 1) Constant function — with zero tolerance, should collapse to exactly 1 piece.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 2.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0),
                  (4.0, float('inf'))],
        "epsilon": 0.0
    },

    # 2) Alternating highs/lows — adjacent jumps far larger than 2ε; cannot merge across alternations.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0), (5.0, 2.0),
                  (6.0, float('inf'))],
        "epsilon": 0.4
    },

    # 3) Small oscillations within a narrow band — global max-min ≤ 2ε so everything should merge to 1 piece.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.10), (1.0, 0.90), (2.0, 1.20), (3.0, 0.80), (4.0, 1.05),
                  (5.0, float('inf'))],
        "epsilon": 0.50
    },

    # 4) Single narrow spike — requires isolating the spike; tests that span-length doesn’t “average out” under L∞.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.0), (2.0, 3.0), (3.0, 0.0), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.60
    },

    # 5) Gradual staircase — increments accumulate beyond 2ε; forces multiple merges/breaks at the right places.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.4), (2.0, 0.8), (3.0, 1.2), (4.0, 1.6),
                  (5.0, float('inf'))],
        "epsilon": 0.50
    },

    # 6) Borderline band just under 2ε — numerical robustness test (max-min is close to 2ε).
    #    Here max-min = 0.39 and 2ε = 0.40 → should be mergable to 1 piece if implemented carefully.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.00), (1.0, 1.39), (2.0, 1.01),
                  (3.0, float('inf'))],
        "epsilon": 0.20
    },

    # 7) Two tight clusters separated by a big gap — should yield exactly two pieces.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.00), (1.0, 0.10), (2.0, 0.20),
                  (3.0, 1.80), (4.0, 1.90), (5.0, 2.00),
                  (6.0, float('inf'))],
        "epsilon": 0.15
    },

    # 8) Very short segments (tiny widths) within 2ε band — spacing in x shouldn’t affect L∞ merging.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0000, 1.00), (0.0001, 1.04), (0.0002, 0.98), (0.0003, 1.02), (0.0004, 0.99),
                  (0.0005, float('inf'))],
        "epsilon": 0.05
    },

    # 9) Sign flip cluster test — negatives cluster and positives cluster; gap too large for one piece.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -1.00), (1.0, -0.90), (2.0, 0.90), (3.0, 1.00),
                  (4.0, float('inf'))],
        "epsilon": 0.40
    },

    # 10) Late jump near the end — checks handling of final-piece logic and boundary.
    #     Overall range slightly above 2ε, so expect at least 2 pieces with a split near the jump.
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.00), (1.0, 1.00), (2.0, 1.00), (3.0, 3.00),
                  (4.0, float('inf'))],
        "epsilon": 0.90
    },
]

#Iteration21 4:35PM
test_cases21 = [
    # 1) Tight equality: global range == 2*epsilon → mergable into 1 piece
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 1.0], [1, 1.3], [2, 0.9], [3, float('inf')]],
        "epsilon": 0.2
    },

    # 2) Slightly over boundary (range > 2*epsilon) → needs ≥2 pieces, but first two fit
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.5], [2, 1.1], [3, float('inf')]],
        "epsilon": 0.25
    },

    # 3) Alternating high/low spikes (adjacent diffs all > 2*epsilon) → no merges
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 1.0], [2, 0.0], [3, 1.0], [4, float('inf')]],
        "epsilon": 0.4
    },

    # 4) Any two adjacent can merge; all three cannot → optimal should be 2 pieces
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 0.0], [1, 0.9], [2, 1.8], [3, float('inf')]],
        "epsilon": 0.5
    },

    # 5) Very small epsilon: gentle ramp with boundary-equality → many small groups
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4], [5, 0.5],
                  [6, float('inf')]],
        "epsilon": 0.05
    },

    # 6) Large numeric range stress test
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -1e9], [1, 0.0], [2, 1e9], [3, float('inf')]],
        "epsilon": 1e8
    },

    # 7) Exact boundary merge with negatives/positives (range == 2*epsilon)
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, -0.3], [1, 0.3], [2, float('inf')]],
        "epsilon": 0.3
    },

    # 8) Two tight clusters separated by a jump
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.00], [1, 0.20], [2, 0.10], [3, 0.15],
                  [4, 2.50], [5, 2.60], [6, 2.55],
                  [7, float('inf')]],
        "epsilon": 0.10
    },

    # 9) Floating-point jitter around a plateau (requires isclose-style logic)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.0], [1, 1.0 + 1e-9], [2, 1.0 - 1e-9],
                  [3, float('inf')]],
        "epsilon": 1e-8
    },

    # 10) Long flat then small step exactly at boundary → full merge possible
    {
        "pc_fx": [[-float('inf'), float('inf')], [0, 5.0], [1, 5.0], [2, 5.0], [3, 5.2], [4, float('inf')]],
        "epsilon": 0.1
    },
]
#Iteration22
test_cases22 = [
    {   # 1) Trivial single-piece
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 2.0),
                  (10.0, float('inf'))],
        "epsilon": 0.0
    },
    {   # 2) All values within 2ε band
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.2), (1.0, 1.7), (2.0, 1.5), (3.0, 1.4),
                  (4.0, float('inf'))],
        "epsilon": 0.25
    },
    {   # 3) Alternating low/high, boundary case
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.0), (2.0, 0.0),
                  (3.0, float('inf'))],
        "epsilon": 0.5
    },
    {   # 4) Same but just over tolerance
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.000001), (2.0, 0.0),
                  (3.0, float('inf'))],
        "epsilon": 0.5
    },
    {   # 5) Large spike inside plateau
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (0.5, 0.0), (0.6, 3.0), (0.7, 0.0),
                  (1.0, float('inf'))],
        "epsilon": 1.4
    },
    {   # 6) Greedy trap 0–2–0–2–0
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 2.0), (2.0, 0.0),
                  (3.0, 2.0), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.99
    },
    {   # 7) Nearly-flat with outlier
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.41),
                  (4.0, float('inf'))],
        "epsilon": 0.2
    },
    {   # 8) Tiny oscillations, small ε
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1e-8), (2.0, 0.0), (3.0, 1e-8),
                  (4.0, float('inf'))],
        "epsilon": 1e-9
    },
    {   # 9) Large ± swings
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -5.0), (1.0, 5.0), (2.0, -5.0),
                  (3.0, float('inf'))],
        "epsilon": 4.9
    },
    {   # 10) Dense duplicates + tiny intervals
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.000000000, 0.0),
                  (0.000000001, 0.0),
                  (0.000000002, 0.0),
                  (0.000001000, 2.0),
                  (0.000001001, 2.0),
                  (0.1, 0.0),
                  (1.0, float('inf'))],
        "epsilon": 1.0
    }
]
#Iteration23
test_cases23 = [
    # 1) Trivial single-piece baseline: optimal must be 1 piece for any ε ≥ 0.
    {
        "pc_fx": [(-float("inf"), float("inf")), (0.0, 2.0), (10.0, float("inf"))],
        "epsilon": 0.1,
    },

    # 2) Exact merge boundary: adjacent values differ by exactly 2ε → mergeable into 1 piece.
    # y: 0.0 -> 1.0, ε = 0.5 (diff = 1.0 = 2ε)
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (5.0, 1.0), (10.0, float("inf"))],
        "epsilon": 0.5,
    },

    # 3) Just-over boundary: adjacent values differ by 2ε + tiny → NOT mergeable.
    # y: 0.0 -> 1.01, ε = 0.5 (diff = 1.01 > 1.0 = 2ε)
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (5.0, 1.01), (10.0, float("inf"))],
        "epsilon": 0.5,
    },

    # 4) Oscillation entirely within ε-band: many small ups/downs within ±ε → should compress to 1 piece.
    # All |y - c| ≤ ε for some c (e.g., near 0).
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (-3.0, 0.10), (-1.0, -0.20), (0.0, 0.22), (4.0, -0.12), (9.0, 0.05),
                  (12.0, float("inf"))],
        "epsilon": 0.25,
    },

    # 5) Staircase with gaps > 2ε everywhere: nothing can be merged; optimal equals n pieces.
    # Diffs: 0→1.5, 1.5→3.1, 3.1→4.8; with ε = 0.5 (2ε=1.0) all jumps exceed 1.0.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (2.0, 1.5), (5.0, 3.1), (9.0, 4.8),
                  (15.0, float("inf"))],
        "epsilon": 0.5,
    },

    # 6) Narrow “impulse” exactly at boundary: extreme middle plateau forces borderline decision.
    # Baseline 0 → spike 5 → back 0, ε = 2.5 (2ε=5). Single constant at 2.5 has max error = ε → mergeable.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 5.0), (2.0, 0.0),
                  (6.0, float("inf"))],
        "epsilon": 2.5,
    },

    # 7) Same as (6) but ε slightly smaller → NOT mergeable; at least 2 pieces are required.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (1.0, 5.0), (2.0, 0.0),
                  (6.0, float("inf"))],
        "epsilon": 2.49,
    },

    # 8) Three levels with adjacent diffs ≤ 2ε but outermost diff > 2ε:
    # y: 0.0 → 0.9 → 1.7, ε = 0.5 (2ε=1.0): 0.0↔0.9=0.9 ≤1.0, 0.9↔1.7=0.8 ≤1.0, 0.0↔1.7=1.7 >1.0
    # Optimal should be 2 pieces (cannot compress all three into one).
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (0.0, 0.0), (3.0, 0.9), (7.0, 1.7),
                  (12.0, float("inf"))],
        "epsilon": 0.5,
    },

    # 9) Redundant break & A–B–A pattern:
    # Equal consecutive values (2.0, then 2.0 again) + short dip to 1.2 in the middle.
    # With ε = 0.4 (2ε=0.8): 2.0↔1.2 diff=0.8 = 2ε (borderline), may allow merging all into 1.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (-10.0, 2.0), (-2.0, 2.0), (0.0, 1.2), (0.5, 2.0), (10.0, 2.0),
                  (20.0, float("inf"))],
        "epsilon": 0.4,
    },

    # 10) Mostly within ε but one slight outlier just above ε:
    # Many segments near 0 within ±0.4, but one at 0.81 with ε=0.4 (2ε=0.8) breaks single-piece feasibility.
    # Optimal likely splits around the outlier to minimize pieces.
    {
        "pc_fx": [(-float("inf"), float("inf")),
                  (-5.0, 0.10), (-1.0, -0.35), (1.0, 0.40), (2.0, -0.25),
                  (3.0, 0.81), (4.0, -0.30), (8.0, 0.15),
                  (12.0, float("inf"))],
        "epsilon": 0.4,
    },
]

#Iteration24
test_cases24 = [
    # 1) Trivially mergeable: all values within ε of each other → optimal answer is 1 piece.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.00], [1.0, 1.05], [2.0, 0.95], [3.0, 1.02], [4.0, float('inf')]],
        "epsilon": 0.10
    },

    # 2) Tight alternating highs/lows just within ε-span if taken as a whole; greedy local merges may fail.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.6], [2.0, 0.0], [3.0, 0.6], [4.0, 0.0], [5.0, float('inf')]],
        "epsilon": 0.30  # Global range = 0.6, which is 2*ε → feasible as 1 piece for L∞ if centered; some heuristics split.
    },

    # 3) “Plateau–spike–plateau”: a single short outlier forces at least 2 pieces; naive averaging may violate ε.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0], [1.0, 2.0], [2.0, 3.0], [3.0, 2.0], [4.0, 2.0], [5.0, float('inf')]],
        "epsilon": 0.8  # Needs 2 pieces: one for spike or split a side; 1-piece would need radius ≥1.0 > ε.
    },

    # 4) “Sandwich”: two similar outer plateaus with a mid region slightly offset—optimal is 2; greedy ends may yield 3.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 5.0], [1.0, 5.1], [2.0, 5.2],  # left plateau ~5.x
                  [3.0, 6.0], [4.0, 6.1],              # middle ~6.x
                  [5.0, 5.0], [6.0, 5.1],              # right plateau ~5.x
                  [7.0, float('inf')]],
        "epsilon": 0.25  # Outer segments can be one piece, middle another → 2 total; local merges can over-split.
    },

    # 5) “Growing staircase” barely feasible in 2 pieces; tests lookahead vs local thresholding.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.2], [2.0, 0.4], [3.0, 0.6], [4.0, 0.8], [5.0, 1.0], [6.0, float('inf')]],
        "epsilon": 0.30  # Optimal: split around mid to keep each side within ±ε; greedy may produce 3+.
    },

    # 6) Long flat with two distant outliers: optimal is 3 (flat core + 2 tiny islands) though many heuristics make 4+.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 10.0], [1.0, 10.0], [2.0, 12.0], [3.0, 10.0],
                  [4.0, 10.0], [5.0, 8.0], [6.0, 10.0], [7.0, 10.0], [8.0, float('inf')]],
        "epsilon": 1.2   # Core 10±1.2 ok; spikes at 12 and 8 require their own pieces → exactly 3.
    },

    # 7) Boundary-tight feasibility: one big interval becomes 1 piece only if the representative is chosen carefully.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -0.3], [1.0, 0.0], [2.0, 0.3], [3.0, 0.0], [4.0, -0.3], [5.0, float('inf')]],
        "epsilon": 0.30  # Range = 0.6 = 2*ε → single piece is feasible but numerically delicate.
    },

    # 8) Repeated tiny jitters around two levels: optimal is 2; local “reset on exceed” strategies may over-fragment.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 3.00], [1.0, 3.05], [2.0, 2.95], [3.0, 3.00],   # cluster A ~3
                  [4.0, 4.00], [5.0, 3.95], [6.0, 4.05], [7.0, 4.00],   # cluster B ~4
                  [8.0, float('inf')]],
        "epsilon": 0.10  # Each cluster fits one piece; overall requires 2.
    },

    # 9) Near-duplicate consecutive pieces (equal y’s) that should be merged; tests handling of redundant boundaries.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.5], [1.0, 1.5], [2.0, 1.5], [3.0, 2.8], [4.0, 2.8], [5.0, float('inf')]],
        "epsilon": 0.05  # First three must collapse to 1 piece; last two to another → optimal 2.
    },

    # 10) Asymmetric cluster + tail: a compact cluster and a far tail barely within ε if split once at the right place.
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -2.0], [1.0, -2.1], [2.0, -1.9], [3.0, -2.0],   # tight cluster around -2
                  [4.0, -0.9], [5.0, -1.0], [6.0, float('inf')]],       # shallow tail around -1
        "epsilon": 0.15  # Requires exactly 2 pieces; naive global fit would violate ε on one side.
    },
]

#Iteration25
test_cases25 = [
    {
        "name": "T1_constant_trivial_1piece",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 2.0), (10.0, 2.0),
                  (20.0, float('inf'))],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "why": "All values identical; with ε=0, still 1 piece."
    },
    {
        "name": "T2_two_values_just_mergeable_below_threshold",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.199999999999),  # diff ≈ 2ε - tiny
                  (2.0, float('inf'))],
        "epsilon": 0.6,
        "expected_min_pieces": 1,
        "why": "|Δy| < 2ε so both can be covered by a single value within ε."
    },
    {
        "name": "T3_two_values_just_not_mergeable_above_threshold",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.200000000001),  # diff ≈ 2ε + tiny
                  (2.0, float('inf'))],
        "epsilon": 0.6,
        "expected_min_pieces": 2,
        "why": "|Δy| > 2ε by a hair; must keep as two pieces."
    },
    {
        "name": "T4_many_small_oscillations_within_band_one_piece",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -0.20), (1.0, 0.10), (2.0, 0.29), (3.0, -0.19),
                  (4.0, float('inf'))],
        "epsilon": 0.25,
        "expected_min_pieces": 1,
        "why": "Global range ≈ 0.49 < 2ε (=0.5); all collapsible into one."
    },
    {
        "name": "T5_alternating_high_low_forces_many_pieces",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.4,
        "expected_min_pieces": 5,
        "why": "Adjacent Δy=2.0 >> 2ε (=0.8); each piece must stand alone."
    },
    {
        "name": "T6_single_large_spike_requires_exactly_two_pieces",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 2.4,
        "expected_min_pieces": 2,
        "why": "Spike at 5.0 has Δy=5 > 2ε (=4.8); isolate spike; merge the rest."
    },
    {
        "name": "T7_staircase_pairs_merge_global_range_blocks_single_piece",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.00), (1.0, 1.19), (2.0, 2.38), (3.0, 3.57),
                  (4.0, float('inf'))],
        "epsilon": 0.6,
        "expected_min_pieces": 2,
        "why": "Every adjacent pair has Δy<2ε (=1.2), but range over 3>2ε, so best is two pieces (e.g., first two, last two)."
    },
    {
        "name": "T8_boundary_and_indexing_check_first_last_sensitive",
        "pc_fx": [(-float('inf'), float('inf')),
                  (-100.0, 1.0), (-50.0, 1.9), (0.0, 1.1), (100.0, 3.6),
                  (200.0, float('inf'))],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "why": "First three values fit within 2ε (=1.0): range 0.9 → merge; last forces new piece."
    },
    {
        "name": "T9_floating_point_knife_edge_vs_tolerance",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.6000000000000001), (2.0, 0.0),
                  (3.0, float('inf'))],
        "epsilon": 0.3,
        "expected_min_pieces": 2,
        "why": "Middle value is ≈ 2ε + 1e-16; should not merge all three if comparisons are exact."
    },
    {
        "name": "T10_large_magnitude_values_scale_sensitivity",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1e9), (1.0, 1e9 + 0.9), (2.0, 1e9 - 0.9),
                  (3.0, float('inf'))],
        "epsilon": 0.5,
        "expected_min_pieces": 2,
        "why": "Pairwise near (Δy=0.9<2ε) but global range 1.8>1.0; best is two pieces."
    },
]

#Iteration26 13 Sept 4:20PM
test_cases26 = [
    # 1) Constant function — should collapse to 1 piece for small ε
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0),
                  (4.0, float('inf'))],
        "epsilon": 0.10
    },

    # 2) Small noise within a tight band — span = 0.08, exactly 2ε (borderline mergeable)
    # max=1.05, min=0.97 ⇒ max-min = 0.08, choose ε=0.04 so 2ε = 0.08
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.00), (1.0, 1.05), (2.0, 0.97), (3.0, 1.02), (4.0, 1.01),
                  (5.0, float('inf'))],
        "epsilon": 0.04
    },

    # 3) Alternating highs/lows well beyond ε — forces multiple pieces
    # span per alternation = 2.0 >> 2ε with ε=0.4 (2ε=0.8)
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 2.0), (2.0, 0.0), (3.0, 2.0), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.40
    },

    # 4) Single tall spike amid flats — optimal isolates spike; rest can merge
    # spike amplitude 5.0 vs baseline 0.0; ε=0.9 ⇒ 2ε=1.8 < 5
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.0), (2.0, 5.0), (3.0, 0.0), (4.0, 0.0),
                  (5.0, float('inf'))],
        "epsilon": 0.90
    },

    # 5) Staircase where early steps merge but final jump forces a split
    # early span 0→0.6 fits 2ε with ε=0.35 (2ε=0.7), last step to 1.8 breaks it
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.2), (2.0, 0.4), (3.0, 0.6), (4.0, 1.8),
                  (5.0, float('inf'))],
        "epsilon": 0.35
    },

    # 6) Exact-boundary case: a single blip at exactly 2ε from plateau (mergeable)
    # plateau 1.0 with a blip 1.8; ε=0.4 ⇒ 2ε=0.8 = span
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.0), (1.0, 1.0), (2.0, 1.8), (3.0, 1.0), (4.0, 1.0),
                  (5.0, float('inf'))],
        "epsilon": 0.40
    },

    # 7) Big jump near the end — stresses handling of late splits
    # 0→3 jump; ε=1.0 ⇒ 2ε=2.0 < 3, so last segment must split off
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 3.0),
                  (4.0, float('inf'))],
        "epsilon": 1.00
    },

    # 8) Large positive outlier amid negatives — optimal isolates the outlier
    # -2, -2, 1.9, -2, -2 with ε=1.0 ⇒ 2ε=2.0; span = 3.9 > 2
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -2.0), (1.0, -2.0), (2.0, 1.9), (3.0, -2.0), (4.0, -2.0),
                  (5.0, float('inf'))],
        "epsilon": 1.00
    },

    # 9) Gradual drift that exceeds tolerance — should segment into minimal runs
    # 0→2 drift; ε=0.49 ⇒ 2ε=0.98 < span 2.0
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (3.0, 1.5), (4.0, 2.0),
                  (5.0, float('inf'))],
        "epsilon": 0.49
    },

    # 10) “Greedy trap”: full span equals 2ε so the whole thing is mergeable,
    # but naive early splitting could over-segment.
    # values 0, 1.2, 1.2, 0; ε=0.6 ⇒ 2ε=1.2 = span
    {
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 1.2), (2.0, 1.2), (3.0, 0.0),
                  (4.0, float('inf'))],
        "epsilon": 0.60
    },
]

#Iteration27
test_cases27 = [
    # 1) All segments within ε-window → should collapse to ONE piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.00], [1.0, 1.01], [2.0, 0.99],
                  [3.0, float('inf')]],
        "epsilon": 0.02
    },

    # 2) Just-too-far to merge anywhere → optimal equals original piece count
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.00], [1.0, 1.05], [2.0, 0.95],
                  [3.0, float('inf')]],
        "epsilon": 0.02
    },

    # 3) Threshold equality: vmax - vmin == 2*ε → should be mergeable
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.4],
                  [2.0, float('inf')]],
        "epsilon": 0.20
    },

    # 4) Alternating highs/lows but still inside one ε-window → collapse to ONE
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 1.00], [1.0, 1.39], [2.0, 1.00], [3.0, 1.39],
                  [4.0, float('inf')]],
        "epsilon": 0.20
    },

    # 5) Single outlier far beyond ε among flats → outlier must be its own piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.0], [2.0, 1.0], [3.0, 0.0], [4.0, 0.0],
                  [5.0, float('inf')]],
        "epsilon": 0.20
    },

    # 6) Floating-point subtlety (0.1+0.2 vs 0.3) → should still merge
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.1 + 0.2], [1.0, 0.3], [2.0, 0.1 + 0.2],
                  [3.0, float('inf')]],
        "epsilon": 1e-12
    },

    # 7) Many near-plateau values within ε → collapse many to ONE piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 5.04], [1.0, 4.97], [2.0, 5.00], [3.0, 5.06], [4.0, 4.95],
                  [5.0, float('inf')]],
        "epsilon": 0.10
    },

    # 8) Two tight clusters separated by > 2ε → optimal is TWO pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -0.31], [1.0, -0.29], [2.0, 0.29], [3.0, 0.31],
                  [4.0, float('inf')]],
        "epsilon": 0.20
    },

    # 9) Gradual staircase; pairs fit but all together don’t → optimal TWO pieces
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.00], [1.0, 0.15], [2.0, 0.30], [3.0, 0.45],
                  [4.0, float('inf')]],
        "epsilon": 0.10
    },

    # 10) Final jump only exceeds ε → first block merges, last needs its own piece
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0], [1.0, 2.0], [2.0, 2.5],
                  [3.0, float('inf')]],
        "epsilon": 0.20
    },
]

#Iteration28

test_cases28 = [
    # 1) Constant function → should collapse to 1 piece for any small ε
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 2.0], [1.0, 2.0], [2.0, 2.0], [3.0, float('inf')]],
        "epsilon": 0.1
    },

    # 2) Small oscillations all within a 2ε band → expect 1 piece
    # Range = 0.5, 2ε = 0.6
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.1], [1.0, 0.3], [2.0, -0.2], [3.0, 0.2], [4.0, float('inf')]],
        "epsilon": 0.3
    },

    # 3) Just-over-threshold gap → must split (cannot merge across 1.1 with ε=0.5)
    # Range between 0.0 and 1.1 is 1.1 > 2ε (=1.0)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1.1], [2.0, 0.0], [3.0, float('inf')]],
        "epsilon": 0.5
    },

    # 4) Plateau with a single spike larger than 2ε → spike isolated
    # Spike 0.9 vs plateau 0.0; 0.9 > 2ε (=0.6)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 0.0], [2.0, 0.9], [3.0, 0.0], [4.0, float('inf')]],
        "epsilon": 0.3
    },

    # 5) Exact boundary case (range == 2ε) across many flips → should allow merge if implementation uses ≤
    # Range 1.0 with ε=0.5
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [0.5, 1.0], [1.0, 0.0], [1.5, 1.0], [2.0, 0.0], [2.5, float('inf')]],
        "epsilon": 0.5
    },

    # 6) Very short interval with big jump (>2ε) → duration should not matter for L∞, still must split
    # Jump to 1.2 exceeds 2ε (=1.0)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [10.0, 0.0], [10.1, 1.2], [10.2, 0.0], [20.0, float('inf')]],
        "epsilon": 0.5
    },

    # 7) Staircase where first three steps can merge but the last forces a split
    # 0 → 0.49 → 0.98 can merge (range 0.98 ≤ 1.0); 1.47 breaks (1.47 > 1.0)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.00], [1.0, 0.49], [2.0, 0.98], [3.0, 1.47], [4.0, float('inf')]],
        "epsilon": 0.5
    },

    # 8) Floating-point tight boundary noise → stresses numerical robustness (range ~ 2e-7, 2ε = 2e-7)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.0], [1.0, 1e-7], [2.0, -1e-7], [3.0, float('inf')]],
        "epsilon": 1e-7
    },

    # 9) Crossing zero at boundary threshold (range == 2ε) → should merge to 1 if ≤ is allowed
    # Range from -0.6 to 0.4 is 1.0; 2ε = 1.0
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, -0.6], [1.0, -0.2], [2.0, 0.4], [3.0, float('inf')]],
        "epsilon": 0.5
    },

    # 10) Three well-separated clusters → expect exactly 3 pieces for small ε
    # Clusters near 0, 1.25, and -1.25 with gaps > 2ε (=0.5)
    {
        "pc_fx": [[-float('inf'), float('inf')],
                  [0.0, 0.00], [1.0, 0.10],
                  [2.0, 1.20], [3.0, 1.30],
                  [4.0, -1.20], [5.0, -1.10],
                  [6.0, float('inf')]],
        "epsilon": 0.25
    },
]

#Iteration29
test_cases29 = [
    {
        # 1) Perfectly flat (strict): with ε=0, optimal is a single piece spanning all x.
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 2.5], [1, 2.5], [2, 2.5], [3, 2.5], [4, 2.5],
                  [5, float('inf')]],
        "epsilon": 0.0,
    },
    {
        # 2) Tight-at-boundary merge: span = 0.2, ε = 0.1 ⇒ span == 2ε, should still merge to 1 piece.
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.2], [2, -0.2], [3, 0.0],
                  [4, float('inf')]],
        "epsilon": 0.1,
    },
    {
        # 3) Just-over-boundary (numerical pitfall): span ≈ 0.4200000002 > 2ε=0.2 ⇒ cannot merge all.
        # Should force multiple pieces; catches sloppy <=/rounding.
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.2100000001], [2, -0.2100000001], [3, 0.0],
                  [4, float('inf')]],
        "epsilon": 0.1,
    },
    {
        # 4) Single narrow spike: mostly 0 with one tall spike; optimal isolates the spike into its own piece.
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.0], [2, 3.0], [3, 0.0], [4, 0.0],
                  [5, float('inf')]],
        "epsilon": 0.9,  # Big enough to merge flats, too small to absorb the spike
    },
    {
        # 5) Two opposite spikes far apart: forces at least three pieces (flat, +spike, -spike).
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 1.0], [2, 0.0], [3, -1.0], [4, 0.0],
                  [5, float('inf')]],
        "epsilon": 0.4,
    },
    {
        # 6) Staircase with small steps: cannot merge everything, but optimal should cluster steps into minimal groups.
        # Designed to expose greedy vs. globally optimal grouping mistakes.
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.00], [1, 0.09], [2, 0.18], [3, 0.27], [4, 0.36],
                  [5, float('inf')]],
        "epsilon": 0.10,  # 2ε = 0.20; some triples fit (span 0.18), all together do not (span 0.36)
    },
    {
        # 7) Redundant equal runs: equal consecutive y's should not create extra pieces (ε=0).
        # Optimal recognizes runs and collapses them.
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.0], [2, 1.0], [3, 1.0], [4, 0.0], [5, 0.0],
                  [6, float('inf')]],
        "epsilon": 0.0,
    },
    {
        # 8) Floating-point knife-edge: span is 0.2000000001 with ε=0.1 (2ε=0.2) ⇒ should NOT merge.
        # Catches algorithms that round aggressively then merge incorrectly.
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 0.0], [1, 0.2000000001],
                  [2, float('inf')]],
        "epsilon": 0.1,
    },
    {
        # 9) Late jump after long calm drift: algorithm must defer splitting until the true jump arrives.
        # Exposes implementations that prematurely split due to minor within-ε fluctuations.
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, 1.00], [1, 1.05], [2, 0.98], [3, 1.02], [4, 1.01],  # small drift (span <= 0.07)
                  [5, 1.80],  # late jump well beyond ε window
                  [6, float('inf')]],
        "epsilon": 0.05,
    },
    {
        # 10) Mixed signs and large magnitudes with generous ε: should collapse many pieces into one or two,
        # testing that the algorithm exploits a large tolerance correctly (not overly conservative).
        "pc_fx": [[-float('inf'), float('inf')],
                  [0, -50.0], [1, -49.6], [2, -50.3], [3, 49.7], [4, 50.1], [5, 49.9],
                  [6, float('inf')]],
        "epsilon": 50.0,  # 2ε = 100; global span ≈ 100.4 ⇒ likely needs 2 pieces; easy to mis-handle
    },
]

#Iteration30
test_cases30 = [
    {
        "name": "TC1_constant_all_merge",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 3.0), (1.0, 3.0), (2.0, 3.0), (5.0, float('inf'))],
        "epsilon": 0.0,
        "expected_min_pieces": 1,
        "notes": "Perfectly constant → should compress to 1 piece for any ε ≥ 0."
    },
    {
        "name": "TC2_noise_within_eps",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 1.00), (1.0, 1.05), (2.0, 0.95), (3.0, 1.02), (4.0, float('inf'))],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "notes": "Range = 0.10 ≤ 2ε (=0.2) ⇒ one value can fit all; tests robust merging with small noise."
    },
    {
        "name": "TC3_exact_threshold_2eps",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 2.0), (1.0, 1.6), (2.0, 2.4), (3.0, 2.0), (4.0, float('inf'))],
        "epsilon": 0.2,
        "expected_min_pieces": 1,
        "notes": "max−min = 0.8 = 2ε → still mergeable (midpoint within ε). Catches ‘>’ vs ‘≥’ threshold bugs."
    },
    {
        "name": "TC4_just_over_threshold",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 2.0), (1.0, 1.599999999999), (2.0, 2.400000000001), (3.0, 2.0), (4.0, float('inf'))],
        "epsilon": 0.2,
        "expected_min_pieces": 2,
        "notes": "Range ≈ 0.800000000001 > 2ε; floating-point sliver prevents full merge. Tests numerical tolerance."
    },
    {
        "name": "TC5_hilo_oscillation_small_eps",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (0.5, 1.0), (1.0, 0.0), (1.5, 1.0), (2.0, 0.0), (2.5, 1.0), (3.0, float('inf'))],
        "epsilon": 0.2,
        "expected_min_pieces": 6,
        "notes": "Alternating 0↔1 with small ε: no adjacent merge possible (range 1 > 2ε=0.4). Stresses worst-case splitting."
    },
    {
        "name": "TC6_single_spike_forced_split",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 5.0), (1.0, 5.0), (2.0, 9.0), (3.0, 5.0), (4.0, 5.0), (5.0, float('inf'))],
        "epsilon": 1.5,
        "expected_min_pieces": 2,
        "notes": "Flat at 5 with a spike at 9 (Δ=4 > 2ε=3). Flats can merge; spike must be its own piece."
    },
    {
        "name": "TC7_staircase_cumulative_drift",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.0), (1.0, 0.9), (2.0, 1.8), (3.0, 2.7), (4.0, 3.6), (5.0, float('inf'))],
        "epsilon": 0.5,
        "expected_min_pieces": 3,
        "notes": (
            "Each step Δ=0.9 < 2ε (=1.0), but total span 3.6 > 2ε. "
            "Greedy local merges can fail; optimal needs ~3 blocks so each block’s range ≤ 2ε."
        ),
    },
    {
        "name": "TC8_plateau_with_small_outliers",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, -2.0), (1.0, -2.1), (2.0, -2.0), (3.0, -2.05), (4.0, -2.0), (5.0, float('inf'))],
        "epsilon": 0.1,
        "expected_min_pieces": 1,
        "notes": "Tiny outliers within ε around a plateau; should still compress to one piece. Checks sign handling and symmetry."
    },
    {
        "name": "TC9_boundary_markers_ignored",
        "pc_fx": [(-float('inf'), float('inf')),
                  (10.0, -100.0), (20.0, -100.0), (30.0, -100.0), (40.0, float('inf'))],
        "epsilon": 0.01,
        "expected_min_pieces": 1,
        "notes": "Ensures algorithm ignores the first/last boundary markers and respects left-continuity of [xi, x_{i+1})."
    },
    {
        "name": "TC10_precision_trap_sum_ops",
        "pc_fx": [(-float('inf'), float('inf')),
                  (0.0, 0.3),              # exactly 0.3
                  (1.0, 0.1 + 0.2),        # 0.30000000000000004 in binary FP
                  (2.0, 0.30000000000000004),
                  (3.0, float('inf'))],
        "epsilon": 1e-12,
        "expected_min_pieces": 1,
        "notes": "All values mathematically equal but differ at FP roundoff. Tests np.isclose/tolerance-aware comparisons."
    },
]


