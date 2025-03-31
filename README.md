# Algorithm Variant Optimization Framework

## Overview

This repository contains a framework for generating, testing, and optimizing algorithm variants for piecewise constant function approximation. The framework uses parallelized processing to efficiently evaluate thousands of algorithm variants against test cases to identify optimal parameter combinations.

## Key Components

### Core Files

- **get_variants.py**: Generates algorithm variants with different traversal strategies and parameter combinations
- **variants_test.py**: Tests algorithm variants against multiple criteria using parallel processing
- **pc_cons_apx.py**: Contains the base implementation of piecewise constant function approximation
- **test_cases.py**: Defines test cases for evaluating algorithm performance

### Algorithm Variants

The framework generates algorithm variants by combining:

1. **Traversal Strategies**:
   - Left to right
   - Right to left
   - Lowest to highest
   - Highest to lowest
   - Middle to ends
   - Middle divide and conquer

2. **Parameter Combinations**:
   - Min/max functions with configurable parameters (a, b, c, d, alpha, scaling_factor)
   - Normalization to eliminate redundant parameter sets

## Parallelization

The framework leverages multi-core CPU parallelization to efficiently process algorithm variants:

- **Algorithm Generation**: Parallelized creation of algorithm variants
- **Algorithm Testing**: Parallel evaluation of variants against test cases
- **Optimized Memory Usage**: Efficient handling of large numbers of variants

## Testing Criteria

Algorithm variants are evaluated based on three main criteria:

1. **Number of Pieces**: Ensures that the optimal number of pieces is less than or equal to the given pieces
2. **Epsilon Difference**: Validates that the epsilon difference is maintained between old and new function values
3. **Simpler Approximation**: Evaluates whether variants provide a simpler approximation compared to the original algorithm

## Usage

### Running Tests

To run the test suite and identify optimal algorithm variants:

```bash
python variants_test.py
```

This will:
1. Generate algorithm variants with different parameter combinations
2. Test variants against all test cases
3. Output successful variants that pass all criteria

### Customizing Parameters

You can customize the parameter ranges in `get_variants.py`:

```python
a_values = range(1, 3)        # Range for parameter a
b_values = range(1, 3)        # Range for parameter b
c_values = range(1, 3)        # Range for parameter c
d_values = range(1, 3)        # Range for parameter d
alpha_values = [0.25, 0.5, 1.0]  # Values for alpha coefficient
scaling_factors = [0.25, 0.5, 1.0]  # Scaling factors
```

### Adding New Traversal Strategies

To add a new traversal strategy, define a function in `get_variants.py` and add it to the `loop_variations` list:

```python
def my_new_strategy(pc_fx):
    # Implement your traversal strategy
    return processed_pc_fx

# Add to the list of traversal strategies
loop_variations.append(my_new_strategy)
```

## Performance Considerations

- The framework is optimized for CPU-bound tasks using Python's multiprocessing library
- Process-based parallelism bypasses Python's GIL limitations
- Memory usage is optimized for handling large numbers of algorithm variants
- The number of CPU cores used can be adjusted based on system capabilities

## Requirements

- Python 3.6+
- NumPy
- Multiprocessing (standard library)

