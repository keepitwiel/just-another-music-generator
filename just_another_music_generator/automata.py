import numpy as np

U = np.array([[4], [2], [1]])


def int_to_bin(rule):
    """
    Converts an 8-bit unsigned integer into binary form

    :param rule: 8-bit unsigned integer
    :return:
    """
    rule_b = np.array(
        [int(_) for _ in np.binary_repr(rule, 8)],
        dtype=np.int8)

    return rule_b


def step(x, rule_b):
    """Compute a single stet of an elementary cellular
    automaton."""
    # The columns contains the L, C, R values
    # of all cells.
    y = np.vstack((np.roll(x, 1), x,
                   np.roll(x, -1))).astype(np.int8)
    # We get the LCR pattern numbers between 0 and 7.
    z = np.sum(y * U, axis=0).astype(np.int8)
    # We get the patterns given by the rule.
    return rule_b[7 - z]


def generate_cellular_automaton(rule: int, size: int = 100, steps: int = 100, seed: int = -1):
    """
    Simulate an elementary cellular automaton given its rule (number between 0 and 255).
    If seed < 0, then we initialize with a zero "line" except for the middle element
    (left of middle if the line length is even)

    :param rule: which rule the automaton performs
    :param size: width of the "line" on which the automaton operates
    :param steps: number of times the calculation is performed
    :param seed: random seed
    """
    # Compute the binary representation of the rule.
    rule_b = int_to_bin(rule)
    x = np.zeros((steps, size), dtype=np.int8)

    if seed < 0:
        # fixed initial state
        x[0, size//2] = 1
    else:
        # Random initial state.
        np.random.seed(seed)
        x[0, :] = np.random.rand(size) < .5

    # Apply the step function iteratively.
    for i in range(steps - 1):
        x[i + 1, :] = step(x[i, :], rule_b)
    return x
