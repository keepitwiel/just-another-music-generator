import numpy as np
import pytest

from just_another_music_generator.automatone import Automatone, SCALES
from just_another_music_generator.sequence import Sequence


KWARGS = {
    'rules': [30],
    'tone_range': 24,
    'sequence_length': 256,
    'skip': 128,
    'interval': 0.125,
    'tone_duration': 0.05,
    'scale': 'pentatonic',
    'root_frequency': 440,
}


def test_automatone_frequencies_keyerror():
    with pytest.raises(KeyError):
        automatone = Automatone(**KWARGS)
        automatone.scale = 'foo'
        _ = automatone._frequencies


def test_automatone_frequencies_major():
    automatone = Automatone(**KWARGS)
    automatone.tone_range = 8
    automatone.scale = 'major'

    expected = [440 * 2**(i/12) for i in SCALES['major']]
    result = automatone._frequencies
    assert result == expected


def test_automatone_frequencies_pentatonic():
    automatone = Automatone(**KWARGS)
    automatone.tone_range = 6
    automatone.scale = 'pentatonic'

    expected = [440 * 2**(i/12) for i in SCALES['pentatonic']]
    result = automatone._frequencies
    assert result == expected


def test_automatone_frequencies_chromatic():
    automatone = Automatone(**KWARGS)
    automatone.tone_range = 13
    automatone.scale = 'chromatic'

    expected = [440 * 2**(i/12) for i in SCALES['chromatic']]
    result = automatone._frequencies
    assert result == expected


def test_automatone_hash():
    automatone = Automatone(**KWARGS)
    h = automatone.hash
    assert h == '5bee22dda0f7dddb6e7fd4d52f4422f4'


def test_automatone_generate_sequence():
    automatone = Automatone(**KWARGS)
    sequence = automatone._sequence
    assert type(sequence) == Sequence
    assert len(sequence) > 0


def test_automatone_generate_activations():
    automatone = Automatone(**KWARGS)
    img = automatone._activations
    assert type(img) == np.ndarray
    assert img.shape[0] == automatone.sequence_length
    assert img.shape[1] == automatone.tone_range


def test_automatone_render_audio():
    automatone = Automatone(**KWARGS)
    au = automatone.render_audio(sample_rate=10000)
    assert type(au) == np.ndarray
    assert len(au) > 0


def test_automatone_render_graph():
    automatone = Automatone(**KWARGS)
    automatone.render_graph()
    assert True


def test_automatone_select_rules_nonrandom():
    automatone = Automatone(**KWARGS)
    assert len(automatone.rules) == 1
    np.testing.assert_array_equal(automatone.rules, np.array([30]))


def test_automatone_select_rules_random():
    kwargs = KWARGS.copy()
    kwargs['rules'] = np.random.randint(2, 100)
    automatone = Automatone(**kwargs)
    assert len(automatone.rules) == kwargs['rules']
