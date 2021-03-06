import numpy as np

from just_another_music_generator.automata import (
    int_to_bin,
    step,
    generate_cellular_automaton,
)


def test_int_to_bin():
    rule = 30
    rule_b = int_to_bin(rule)
    np.testing.assert_array_equal(rule_b, np.array([0, 0, 0, 1, 1, 1, 1, 0]))


def test_step_zeros():
    inp = np.zeros(50, dtype=np.int8)
    expected = inp.copy()

    rule = 0
    rule_b = int_to_bin(rule)
    result = step(inp, rule_b)

    np.testing.assert_array_equal(result, expected)


def test_step_one():
    inp = np.array([0, 1, 0], dtype=np.int8)
    expected = np.array([1, 1, 1], dtype=np.int8)

    rule = 30
    rule_b = int_to_bin(rule)
    result = step(inp, rule_b)

    np.testing.assert_array_equal(result, expected)


def test_generate_cellular_automaton():
    result = generate_cellular_automaton(rule=30, size=13, steps=37, skip=0)
    assert result.shape == (37, 13)


def test_generate_cellular_automaton_1():
    result = generate_cellular_automaton(rule=30, size=5, steps=2, skip=0)
    expected = np.array(
        [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
        ]
    )
    np.testing.assert_array_equal(result, expected)


def test_generate_cellular_automaton_2():
    result = generate_cellular_automaton(rule=30, size=5, steps=2, skip=1)
    expected = np.array(
        [
            [0, 1, 1, 1, 0],
            [1, 1, 0, 0, 1],
        ]
    )
    np.testing.assert_array_equal(result, expected)
