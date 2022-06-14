import numpy as np

from just_another_music_generator.tone import Tone, interpolate


def test_tone():
    Tone(
        start_time=0,
        attack_time=0.0,
        decay_time=0.5,
        sustain_time=0.0,
        sustain_level=0.0,
        release_time=0.0,
        pitch=440,
        volume=0.5,
        pan=0.5,
    )
    assert True


def test_tone_render_array():
    tone = Tone(
        start_time=0,
        attack_time=0.1,
        decay_time=0.1,
        sustain_time=0.7,
        sustain_level=0.5,
        release_time=0.1,
        pitch=440,
        volume=0.5,
        pan=0.5,
    )
    t = np.linspace(-1, 2, 101)
    x = tone.render(t)
    assert x.shape[0] == len(t)
    assert x.shape[1] == 2
    assert x[0, 0] == 0
    assert x[-1, 0] == 0
    assert x[0, 1] == 0
    assert x[-1, 1] == 0


def test_interpolate():
    t0 = 0.0
    t1 = 1.0
    level0 = 1.0
    level1 = 0.5

    t = np.linspace(-1, 2, 151)
    result = interpolate(t, t0, t1, level0, level1)
    assert result[0] == 0.0
    assert result[49] == 0.0
    assert result[50] == 1.0
    assert result[99] == 0.51
    assert result[100] == 0.0


def test_interpolate_zeros():
    t0 = 0.0
    t1 = 0.0
    level0 = 0.0
    level1 = 1.0

    t = np.linspace(-1, 2, 151)
    result = interpolate(t, t0, t1, level0, level1)
    np.testing.assert_equal(result, 0)


def test_tone_envelope():
    tone = Tone(
        start_time=0,
        attack_time=0.1,
        decay_time=0.2,
        sustain_time=0.3,
        sustain_level=0.5,
        release_time=0.4,
        pitch=440,
        volume=0.5,
        pan=0.5,
    )
    t = np.linspace(0, 1, 101)
    envelope = tone._calculate_envelope(t=t)

    assert len(envelope) == len(t)
    assert envelope[0] == 0.0
    np.testing.assert_almost_equal(envelope[9], 0.9)
    assert envelope[10] == 1.0
    assert envelope[29] > 0.5
    np.testing.assert_almost_equal(envelope[30], 0.5)
    np.testing.assert_almost_equal(envelope[40], 0.5)
    np.testing.assert_almost_equal(envelope[50], 0.5)
    assert envelope[61] < 0.5
    assert envelope[99] < 0.1
    assert envelope[100] == 0.0
