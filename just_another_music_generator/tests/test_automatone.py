import numpy as np
import pytest

from just_another_music_generator.automatone import Automatone, SCALES
from just_another_music_generator.sequence import Sequence


KWARGS = {
    'n_rules': 5,
    'tone_range': 24,
    'sequence_length': 256,
    'skip': 128,
    'interval': 0.125,
    'tone_duration': 0.05,
    'scale': 'pentatonic',
    'root_frequency': 440,
    'seed': -1,
}


def test_automatone_frequencies_keyerror():
    with pytest.raises(KeyError):
        obj = Automatone(**KWARGS)
        obj.scale = 'foo'
        _ = obj._frequencies


def test_automatone_frequencies_major():
    obj = Automatone(**KWARGS)
    obj.tone_range = 8
    obj.scale = 'major'

    expected = [440 * 2**(i/12) for i in SCALES['major']]
    result = obj._frequencies
    assert result == expected


def test_automatone_frequencies_pentatonic():
    obj = Automatone(**KWARGS)
    obj.tone_range = 6
    obj.scale = 'pentatonic'

    expected = [440 * 2**(i/12) for i in SCALES['pentatonic']]
    result = obj._frequencies
    assert result == expected


def test_automatone_frequencies_chromatic():
    obj = Automatone(**KWARGS)
    obj.tone_range = 13
    obj.scale = 'chromatic'

    expected = [440 * 2**(i/12) for i in SCALES['chromatic']]
    result = obj._frequencies
    assert result == expected


def test_automatone_hash():
    obj = Automatone(**KWARGS)
    h = obj.hash
    assert h == 'ceac467965836e1931e8b0cf9cd54189'


def test_automatone_generate_sequence():
    obj = Automatone(**KWARGS)
    sequence = obj._sequence
    assert type(sequence) == Sequence
    assert len(sequence) > 0


def test_automatone_generate_activations():
    obj = Automatone(**KWARGS)
    img = obj._activations
    assert type(img) == np.ndarray
    assert img.shape[0] == obj.sequence_length
    assert img.shape[1] == obj.tone_range


def test_automatone_render_audio():
    obj = Automatone(**KWARGS)
    au = obj.render_audio(sample_rate=10000)
    assert type(au) == np.ndarray
    assert len(au) > 0


def test_automatone_render_graph():
    obj = Automatone(**KWARGS)
    graph = obj.render_graph()
    assert True
