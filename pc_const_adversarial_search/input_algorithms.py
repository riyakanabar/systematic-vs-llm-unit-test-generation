from optimal_algorithms.pc_cons_apx import approximate_pc_cons_fx
from grid_search.get_variants import variant_function, loop_variations
import functools
import operator
import numpy as np

#approximate_pc_cons_fx function - optimal variant suggested by prof
variant1 = approximate_pc_cons_fx
variant2 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[1],
        params_min=[1,2,1,2,-1],
        params_max=[1,1,1,1,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )
variant3 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[2],
        params_min=[1,1,1,1,-1],
        params_max=[1,1,1,1,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )
variant4 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[1],
        params_min=[2,5,2,5,-1],
        params_max=[2,5,2,5,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )
variant5 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[1],
        params_min=[1,1,1,1,-1],
        params_max=[1,1,1,1,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )
variant6 = functools.partial(
        variant_function,
        loop_behavior=loop_variations[0],
        params_min=[1,1,1,1,-1],
        params_max=[1,1,1,1,1],
        condition_params=[operator.ge, operator.ge, operator.le]
    )


def variant7(pc_fx, epsilon):
        """
        Non-optimal greedy algorithm for approximating a piecewise constant function
        using a top-down ε-satisfying split.
        """

        def recursive_split(start_idx, end_idx):
                segment = pc_fx[start_idx:end_idx + 1]
                ys = np.array([y for _, y in segment])
                max_y = np.max(ys)
                min_y = np.min(ys)

                if np.isclose(max_y, min_y, atol=2 * epsilon, rtol=1e-9):
                        y_value = (max_y + min_y) / 2
                        return [[pc_fx[start_idx][0], y_value]]

                # Find index of max error
                mid_idx = -1
                max_error = -1
                for i in range(start_idx + 1, end_idx):
                        y = pc_fx[i][1]
                        if y > max_y or y < min_y:
                                continue
                        error = abs(y - (max_y + min_y) / 2)
                        if error > max_error:
                                max_error = error
                                mid_idx = i

                if mid_idx == -1 or start_idx == mid_idx or end_idx == mid_idx:
                        y_value = (max_y + min_y) / 2
                        return [[pc_fx[start_idx][0], y_value]]

                left = recursive_split(start_idx, mid_idx)
                right = recursive_split(mid_idx, end_idx)
                return left + right

        # Call recursive splitting on points between -inf and +inf
        segments = recursive_split(1, len(pc_fx) - 2)
        segments.append([pc_fx[-1][0], float('inf')])

        num_pieces = len(segments) - 1
        given_pieces = len(pc_fx) - 2
        return segments, num_pieces, given_pieces
