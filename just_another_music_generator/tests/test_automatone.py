import numpy as np

from just_another_music_generator.automatone import Automatone
from just_another_music_generator.sequence import Sequence


KWARGS = {
    'n_rules': 5,
    'tone_range': 24,
    'sequence_length': 256,
    'skip': 128,
    'sample_rate': 96000,
    'interval': 0.125,
    'tone_duration': 0.05,
    'scale': 'pentatonic',
    'root_frequency': 440,
    'seed': -1,
}


def test_automatone_hash():
    obj = Automatone(**KWARGS)
    h = obj.hash
    assert h == '8e7ec3a2e36f41513580f43c5d133125'


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
    au = obj.render_audio()
    assert type(au) == np.ndarray
    assert len(au) > 0


def test_automatone_render_graph():
    obj = Automatone(**KWARGS)
    graph = obj.render_graph()
    assert True
