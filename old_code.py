import numpy as np
import random
from utils import middle_to_end_alternating_traversal, middle_divide_conquer_traversal
def approximate_pc_cons_fx0(pc_fx, epsilon):
    optimal_pc_fx = []
    current_x, current_fx = pc_fx[1]

    for next_x, next_fx in pc_fx[2:-1]:
        adjusted_fx = current_fx + np.sign(next_fx - current_fx) * epsilon
        if abs(next_fx - adjusted_fx) > epsilon:
            optimal_pc_fx.append([current_x, current_fx])
            current_x, current_fx = next_x, next_fx
        else:
            current_fx = adjusted_fx

    optimal_pc_fx.append([current_x, current_fx])
    optimal_pc_fx.append([pc_fx[-1][0], float('inf')])

    optimal_num_pieces = len(optimal_pc_fx) - 1
    given_num_pieces = len(pc_fx) - 2

    return optimal_pc_fx, optimal_num_pieces, given_num_pieces

def get_variation_algorithms0(algorithms):
    algorithms = []

    # Define variations for adjustment within epsilon
    adjusted_fx_formulas = [
        lambda current_fx, next_fx, epsilon: current_fx + np.sign(next_fx - current_fx) * epsilon,
        lambda current_fx, next_fx, epsilon: current_fx + min(abs(next_fx - current_fx), epsilon) * np.sign(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: (current_fx + next_fx) / 2,
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.cos(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sin(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.tan(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.cosh(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sinh(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.tanh(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(np.cos(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(np.sin(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(np.tan(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(np.cosh(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(np.sinh(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(np.tanh(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.exp(-abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.exp2(-abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + np.log10(abs(next_fx - current_fx)) * epsilon,
        lambda current_fx, next_fx, epsilon: current_fx + np.log2(abs(next_fx - current_fx)) * epsilon,
        lambda current_fx, next_fx, epsilon: current_fx + np.log1p(abs(next_fx - current_fx)) * epsilon,
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.arcsin(np.clip(next_fx * current_fx, -1, 1)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.arccos(np.clip(next_fx - current_fx, -1, 1)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.arctan(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.arcsinh(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.arccosh(max(1, next_fx - current_fx + 1)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.arctanh(
            np.clip(next_fx - current_fx, -0.99, 0.99)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + random.uniform(-epsilon, epsilon),
        lambda current_fx, next_fx, epsilon: max(current_fx, next_fx) - epsilon,
        lambda current_fx, next_fx, epsilon: current_fx + (epsilon ** 2) * np.sign(next_fx - current_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.clip(next_fx - current_fx, -1, 1),
        lambda current_fx, next_fx, epsilon: next_fx if abs(next_fx - current_fx) < epsilon else current_fx,
        lambda current_fx, next_fx, epsilon: current_fx + (next_fx - current_fx) * random.random(),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx - current_fx) / (1 + abs(next_fx - current_fx)),

        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.abs(next_fx - current_fx) ** 0.5),
        # Square root for dampening large changes.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.abs(np.sin(next_fx) - np.cos(current_fx)),
        # Difference of sin and cos.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.maximum(next_fx, current_fx) / (
                    1 + np.abs(next_fx - current_fx)),  # Ratio-based adjustment.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.minimum(next_fx, current_fx) * np.sign(
            next_fx - current_fx),  # Minimum-based scaled.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx ** 2 - current_fx ** 2) / (
                    1 + abs(next_fx - current_fx)),  # Squared difference-based.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.exp(abs(next_fx - current_fx)) - 1) / (
                    np.exp(abs(next_fx - current_fx)) + 1),  # Softmax-like adjustment.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(np.log1p(abs(next_fx - current_fx))) * (
                    np.log1p(abs(next_fx - current_fx)) ** 0.5),  # Sign + log-root scaling.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx) * np.abs(current_fx) / (
                    1 + abs(next_fx - current_fx)),  # Weighted sign adjustment.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx - current_fx) ** 2 / (
                    1 + abs(next_fx - current_fx)),  # Squared with smoothness.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx - current_fx) * np.tan(
            np.abs(next_fx - current_fx)),  # Scaled tangent difference.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.arctan(next_fx) - np.arcsinh(current_fx)) / (
                    1 + abs(next_fx - current_fx)),  # Combined arctan/arcsinh ratio.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx - current_fx) * np.sqrt(
            abs(next_fx * current_fx) + 1e-8),  # Smoothed root-based adjustment.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx - current_fx) * np.abs(
            np.tanh(next_fx) - np.sinh(current_fx)),  # Tanh/sinh difference.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.abs(next_fx - current_fx)) ** 1.5 / (
                    1 + abs(next_fx - current_fx)),  # Cubic root scaling.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.log1p(np.abs(next_fx ** 2 - current_fx ** 2)),
        # Log of squared difference.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx - current_fx) * (
                    np.exp2(abs(next_fx - current_fx)) - 1),  # Exponential scaling.
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.clip((next_fx - current_fx) ** 2, -epsilon,
                                                                            epsilon),  # Bounded square adjustment.

        lambda current_fx, next_fx, epsilon: current_fx - epsilon * np.sign(next_fx + current_fx),
        lambda current_fx, next_fx, epsilon: current_fx * (1 + epsilon * np.tanh(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx * (1 - epsilon * np.exp(-abs(next_fx - current_fx))),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.sqrt(abs(next_fx - current_fx))),
        lambda current_fx, next_fx, epsilon: current_fx - epsilon * np.sqrt(max(0, next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon / (1 + abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx - current_fx) * np.exp(-next_fx ** 2),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx + current_fx) / (
                    1 + abs(current_fx * next_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon / (1 + np.exp(-abs(next_fx - current_fx))),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sin(np.pi * (next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.tan(np.pi / 4 * (next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.arctan(abs(next_fx * current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(current_fx) * np.abs(
            next_fx - current_fx) ** 0.5,
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.abs(next_fx - current_fx) / (1 + next_fx ** 2),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.tan(next_fx - current_fx) - np.sin(next_fx)),
        lambda current_fx, next_fx, epsilon: current_fx - epsilon * np.cosh(abs(next_fx - current_fx)) * np.sign(
            next_fx),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx - current_fx) ** 2 / (
                    1 + abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.log1p(next_fx * current_fx) / (
                    1 + abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sin(next_fx ** 2 - current_fx ** 2),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (1 / (1 + np.exp(next_fx - current_fx))),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx) * (
                    abs(next_fx - current_fx) ** 1.5),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sinh(next_fx + current_fx) / (
                    1 + abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx - epsilon * np.log(np.abs(next_fx - current_fx) + 1),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx - current_fx) * np.log1p(
            abs(next_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.sin(next_fx) * np.cos(current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx - epsilon * (np.sign(next_fx) * np.tanh(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon / (1 + abs(next_fx + current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.abs(next_fx) - np.abs(current_fx)) / 2,
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.exp(-np.sqrt(abs(next_fx - current_fx))),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.log1p(abs(next_fx * current_fx)) / (
                    1 + next_fx ** 2),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sinh(next_fx - current_fx) / (1 + next_fx ** 2),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sin(abs(next_fx) - abs(current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx) * np.tanh(
            abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sqrt(abs(next_fx * current_fx)) / (
                    1 + next_fx ** 2),

        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.linalg.norm(next_fx - current_fx),
        # Norm of the difference
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(current_fx) * np.linalg.norm(
            [next_fx, current_fx]),  # Combined norm
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.dot(next_fx, current_fx),  # Dot product
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.clip(np.linalg.norm(current_fx), -epsilon,
                                                                            epsilon),  # Clipped norm
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (1 - np.linalg.norm(next_fx - current_fx)), # Norm difference factor
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (
                    np.dot(next_fx, current_fx) / (np.linalg.norm(next_fx) + 1e-7)),  # Dot scaled by norm
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.clip(np.dot(next_fx, current_fx), -1, 1)),
        # Clipped dot product
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.interp(current_fx, [current_fx, next_fx],
                                                                              [0, 1]),  # Linear interpolation
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(current_fx) * np.tanh(
            np.dot(next_fx, current_fx)),  # Tanh dot product
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (
                    1 - np.dot(next_fx, current_fx) / (np.linalg.norm(next_fx) * np.linalg.norm(current_fx) + 1e-7)),
        # 1 - cosine similarity
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.clip(np.linalg.norm([next_fx, current_fx]), -1,
                                                                            1),  # Combined norm clipped
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.linalg.norm(next_fx - current_fx) / (
                    1 + abs(current_fx)),  # Norm scaled by current_fx
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.tanh(np.linalg.norm(next_fx - current_fx)),
        # Tanh of the norm difference
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx - current_fx) * np.dot(next_fx,
                                                                                                           current_fx),
        # Signed dot product
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (
                    np.dot(next_fx, current_fx) / (1 + np.linalg.norm(next_fx - current_fx))),  # Dot over scaled norm
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.linalg.norm(next_fx) / (
                    1 + np.linalg.norm(current_fx)),  # Ratio of norms
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.cos(
            np.dot(next_fx, current_fx) / (np.linalg.norm(next_fx) + 1e-7)),  # Cosine of dot/norm
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx) * np.interp(current_fx, [next_fx,
                                                                                                              next_fx + epsilon],
                                                                                                 [0, 1]),
        # Signed interpolation
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.linalg.norm(next_fx - current_fx) / (
                    1 + np.dot(next_fx, current_fx)),  # Norm scaled by dot
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(current_fx) * np.tanh(
            np.clip(next_fx - current_fx, -1, 1)),  # Signed tanh of clipped difference
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.abs(next_fx - current_fx) / (
                    1 + np.linalg.norm(next_fx + current_fx)),  # Absolute difference over norm
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(
            np.dot(next_fx, current_fx)) * np.linalg.norm(next_fx - current_fx),  # Signed norm by dot
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.interp(np.dot(next_fx, current_fx), [-1, 1],
                                                                              [current_fx, next_fx]),
        # Interpolated dot
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (
                    np.dot(next_fx, current_fx) - np.linalg.norm(next_fx - current_fx)),  # Dot minus norm
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.log1p(
            np.linalg.norm([next_fx, current_fx]) / (1 + abs(current_fx))),  # Log-scaled norm
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.linalg.norm(next_fx) / (
                    1 + np.abs(np.dot(next_fx, current_fx))),  # Norm over scaled dot
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sinh(
            np.clip(np.linalg.norm(next_fx - current_fx), -1, 1)),  # Sinh of clipped norm
        lambda current_fx, next_fx, epsilon: current_fx - epsilon * (next_fx - current_fx) ** 3,
        lambda current_fx, next_fx, epsilon: (current_fx * next_fx) / (epsilon + abs(current_fx + next_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.log(1 + abs(next_fx - current_fx)) / (
                    1 + abs(current_fx - next_fx)),
        lambda current_fx, next_fx, epsilon: (current_fx + next_fx) / (1 + epsilon * abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx * (1 - epsilon) + next_fx * epsilon ** 2,
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.cbrt(abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (1 / (1 + abs(next_fx - current_fx) ** 2)),
        lambda current_fx, next_fx, epsilon: next_fx - epsilon / (1 + np.abs(current_fx - next_fx) ** 0.5),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx - current_fx) / (
                    1 + abs(next_fx - current_fx) ** 2),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (1 - np.exp(-abs(next_fx - current_fx) ** 2)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (next_fx - current_fx) ** 2 / (
                    1 + abs(next_fx - current_fx)),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * np.sign(next_fx - current_fx) * (
                    abs(next_fx * current_fx) ** 0.5),
        lambda current_fx, next_fx, epsilon: current_fx + epsilon * (np.exp(abs(next_fx - current_fx)) - 1) / (
                    np.exp(abs(next_fx - current_fx)) + 1),
    ]

    # Define variations for loop behavior
    loop_variations = [
        lambda pc_fx: pc_fx[1:-1], #left to right
        lambda pc_fx: reversed(pc_fx[1:-1]), # right to left
        lambda pc_fx: sorted(pc_fx[1:-1], key=lambda x: x[1]), # Lowest function value to highest
        lambda pc_fx: sorted(pc_fx[1:-1], key=lambda x: x[1], reverse=True), # Highest function value to lowest
        lambda pc_fx: middle_to_end_alternating_traversal(pc_fx[1:-1]), #middle to left and right
        lambda pc_fx: middle_divide_conquer_traversal(pc_fx[1:-1])  #middle-Divide-and-Conquer
    ]
    # Generate all combinations of variations
    for adjusted_fx_formula in adjusted_fx_formulas:

        for loop_behavior in loop_variations:
            def create_variant(adjusted_fx_formula, loop_behavior):
                def variant(pc_fx, epsilon):
                    optimal_pc_fx = []
                    pc_fx_traversal_order = list(loop_behavior(pc_fx))

                    current_x, current_fx = pc_fx_traversal_order[0]
                    for i in range(1, len(pc_fx_traversal_order)):
                        next_x, next_fx = pc_fx_traversal_order[i]
                        adjusted_fx = adjusted_fx_formula(current_fx, next_fx, epsilon)

                        if abs(next_fx - adjusted_fx) > epsilon:
                            optimal_pc_fx.append([current_x, current_fx])
                            current_x, current_fx = next_x, next_fx
                        else:
                            current_fx = adjusted_fx

                    optimal_pc_fx.append([current_x, current_fx])
                    optimal_pc_fx.append([pc_fx[-1][0], float('inf')])
                    optimal_num_pieces = len(optimal_pc_fx) - 1
                    given_num_pieces = len(pc_fx) - 2

                    return optimal_pc_fx, optimal_num_pieces, given_num_pieces

                variant.adjusted_fx_formula = adjusted_fx_formula  # Attach the formula
                variant.loop_behavior = loop_behavior  # Attach the loop behavior
                return variant

            algorithms.append(create_variant(adjusted_fx_formula,loop_behavior))

    return algorithms

def get_variation_algorithms():
    algorithms = []

    # Define variations for loop behavior
    loop_variations = [
        lambda pc_fx: pc_fx[1:-1], #left to right
        lambda pc_fx: reversed(pc_fx[1:-1]), # right to left
        lambda pc_fx: sorted(pc_fx[1:-1], key=lambda x: x[1]), # Lowest function value to highest
        lambda pc_fx: sorted(pc_fx[1:-1], key=lambda x: x[1], reverse=True), # Highest function value to lowest
        lambda pc_fx: middle_to_end_alternating_traversal(pc_fx[1:-1]), #middle to left and right
        lambda pc_fx: middle_divide_conquer_traversal(pc_fx[1:-1])  #middle-Divide-and-Conquer
    ]
    for loop_behavior in loop_variations:
        def create_variant(loop_behavior):
            def variant(pc_fx, epsilon):
                optimal_pc_fx = []
                pc_fx_traversal_order = list(loop_behavior(pc_fx))
                min_val = pc_fx_traversal_order[0][1]  # Initialize min value
                max_val = pc_fx_traversal_order[0][1]  # Initialize max value
                x = pc_fx_traversal_order[0][0]
                for i in range(1, len(pc_fx_traversal_order)):
                    yi = pc_fx_traversal_order[i][1]
                    min_old, max_old = min_val, max_val
                    if yi < min_val:
                        min_val = yi
                        if not np.isclose(min_val, max_val, atol=2 * epsilon, rtol=1e-9):  # If exceeding threshold
                            y_value = (max_val + min_old) / 2  # Take midpoint before update
                            optimal_pc_fx.append([x, y_value])  # Append segment
                            x = pc_fx_traversal_order[i][0]  # Start new segment
                            min_val = max_val = yi  # Reset min/max
                    elif yi > max_val:
                        max_val = yi
                        if not np.isclose(min_val, max_val, atol=2 * epsilon, rtol=1e-9):
                            y_value = (max_old + min_val) / 2  # Take midpoint before update
                            optimal_pc_fx.append([x, y_value])  # Append segment
                            x = pc_fx_traversal_order[i][0]  # Start new segment
                            min_val = max_val = yi  # Reset min/max
                # Store the last segment
                y_value = (max_val + min_val) / 2
                optimal_pc_fx.append([x, y_value])
                optimal_pc_fx.append([pc_fx[-1][0], float('inf')])  # Append last boundary
                optimal_num_pieces = len(optimal_pc_fx) - 1
                given_num_pieces = len(pc_fx) - 2
                return optimal_pc_fx, optimal_num_pieces, given_num_pieces
            variant.loop_behavior = loop_behavior  # Attach the loop behavior
            return variant
        algorithms.append(create_variant(loop_behavior))
    return algorithms