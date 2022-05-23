import numpy as np

from just_another_music_generator.tone import Tone


def test_tone():
    Tone(start_time=0, duration=1, pitch=440, volume=0.5)
    assert True


def test_tone_render():
    tone = Tone(start_time=0, duration=1, pitch=440, volume=0.5)

    x = tone.render(t=-1.0)
    assert x == 0

    x = tone.render(t=2.0)
    assert x == 0

    x = tone.render(t=0.3333333)
    assert np.abs(x) > 0


def test_tone_render_array():
    tone = Tone(start_time=0, duration=1, pitch=440, volume=0.5)
    t_array = np.linspace(-1, 2, 101)
    x = tone.render(t=t_array)
    assert len(x) == len(t_array)
    assert x[0] == 0
    assert x[-1] == 0
