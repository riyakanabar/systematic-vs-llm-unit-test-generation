from optimal_algorithms.pc_cons_apx import approximate_pc_cons_fx
from grid_search.get_variants import variant_function, loop_variations
import functools
import operator

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