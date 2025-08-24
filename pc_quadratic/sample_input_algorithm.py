def algorithm(f, pieces, epsilon):
    """
    A simple test algorithm that returns the input function as-is.

    Args:
        f: 3xN numpy array of coefficients [a; b; c]
        pieces: List of breakpoints (including ±inf)
    Returns:
        g: Same as input f
        g_pieces: Same as input pieces
        num_pieces: Number of pieces (N)
    """
    # Just return the input
    num_pieces = len(pieces) - 1
    return f, pieces, num_pieces