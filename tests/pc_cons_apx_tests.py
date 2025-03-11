import unittest
from pc_cons_apx import approximate_pc_cons_fx

class TestPiecewiseConstantApproximation(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            (
                [
                    [-float('inf'), float('inf')],
                    [1.2, 4.2],
                    [4.5, 5.7],
                    [6.0, 5.1],
                    [7.1, 3.2],
                    [8.0, float('inf')]
                ],
                0.5
            ),
            (
                [
                    [-float('inf'), float('inf')],
                    [1.0, 10.5],
                    [2.5, 10.2],
                    [3.0, 12.0],
                    [4.7, 8.5],
                    [7.0, float('inf')]
                ],
                0.6
            ),
            (
                [
                    [-float('inf'), float('inf')],
                    [0.0, 5.2],
                    [2.0, 5.5],
                    [4.5, 9.0],
                    [6.0, 4.0],
                    [8.0, float('inf')]
                ],
                0.5
            ),
            (
                [
                    [-float('inf'), float('inf')],
                    [1.0, 3.2],
                    [1.8, 2.8],
                    [4.2, 6.1],
                    [6.5, 3.3],
                    [7.3, 9.2],
                    [9.0, float('inf')]
                ],
                1.0
            ),
            (
                [
                    [-float('inf'), float('inf')],
                    [1.3, 4.1],
                    [3.2, 5.4],
                    [4.8, 4.2],
                    [6.3, 3.0],
                    [9.1, float('inf')]
                ],
                0.2
            )
        ]

    def test_number_of_pieces(self):
        for pc_cons_fx, epsilon in self.test_cases:
            optimal_pc_fx, optimal_num_pieces, given_num_pieces = approximate_pc_cons_fx(pc_cons_fx, epsilon)
            self.assertGreaterEqual(given_num_pieces, optimal_num_pieces,
                f"Expected given pieces ({given_num_pieces}) >= optimal pieces ({optimal_num_pieces})")

    def test_epsilon_difference(self):
        for pc_cons_fx, epsilon in self.test_cases:
            optimal_pc_fx, optimal_num_pieces, given_num_pieces = approximate_pc_cons_fx(pc_cons_fx, epsilon)
            for i in range(1, len(pc_cons_fx) - 1):
                old_x, old_fx = pc_cons_fx[i]
                new_fx = None
                for j in range(1, len(optimal_pc_fx)):
                    if old_x < optimal_pc_fx[j][0]:  # Ensure left-side continuity
                        new_fx = optimal_pc_fx[j - 1][1]
                        break
                self.assertIsNotNone(new_fx, f"No new value found for old x = {old_x}")
                self.assertLessEqual(abs(old_fx - new_fx), epsilon,
                    f"At x = {old_x}, |Old value ({old_fx}) - New value ({new_fx})| > epsilon ({epsilon})")

if __name__ == "__main__":
    unittest.main()
