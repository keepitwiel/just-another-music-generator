from just_another_music_generator.sequence import Sequence
from just_another_music_generator.tone import Tone


def test_sequence():
    sequence = Sequence()
    assert len(sequence) == 0


def test_add_tone():
    sequence = Sequence()
    sequence.add(Tone(start_time=0, duration=1, pitch=440, volume=0.5))
    assert len(sequence) == 1


def test_render():
    sequence = Sequence()
    sequence.add(Tone(start_time=0, duration=1, pitch=440, volume=0.5))
    sequence.render(sample_rate=110)
    assert True
