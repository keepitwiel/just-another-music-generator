import numpy as np

from just_another_music_generator.tone import Tone


def test_tone():
    Tone(start_time=0, attack=0.0, decay=0.5, sustain_time=0.0, sustain_level=0.0, release=0.0, pitch=440, volume=0.5)
    assert True


def test_tone_render_array():
    tone = Tone(start_time=0, attack=0.0, decay=0.5, sustain_time=0.0, sustain_level=0.0, release=0.0, pitch=440, volume=0.5)
    t_array = np.linspace(-1, 2, 101)
    x = tone.render(t=t_array)
    assert len(x) == len(t_array)
    assert x[0] == 0
    assert x[-1] == 0
