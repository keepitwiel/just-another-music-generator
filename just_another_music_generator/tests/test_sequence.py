from just_another_music_generator.sequence import Sequence, find_bounds
from just_another_music_generator.tone import Tone


def test_find_bounds():
    tone = Tone(start_time=1.00001, attack=0.0, decay=0.5, sustain_time=0.0, sustain_level=0.0, release=0.0, pitch=440, volume=0.5)
    sample_rate = 1000
    expected = (1000, 1501)

    result = find_bounds(tone, sample_rate)

    assert result == expected


def test_sequence():
    sequence = Sequence()
    assert len(sequence) == 0


def test_add_tone():
    sequence = Sequence()
    sequence.add(
        Tone(start_time=0, attack=0.0, decay=0.5, sustain_time=0.0, sustain_level=0.0, release=0.0, pitch=440, volume=0.5)
    )
    assert len(sequence) == 1


def test_render():
    sequence = Sequence()
    sequence.add(
        Tone(start_time=0, attack=0.0, decay=0.5, sustain_time=0.0, sustain_level=0.0, release=0.0, pitch=440, volume=0.5)
    )
    sequence.render(sample_rate=110)
    assert True
