from just_another_music_generator.pipeline import generate_audio


def test_integration():
    au = generate_audio(
        n_rules=1,
        tone_range=32,
        sequence_length=5,
        skip=0,
        sample_rate=12000,
        interval=0.1,
        tone_duration=0.2,
        scale='pentatonic',
        root_frequency=220,
        seed=42,
    )
    assert len(au) > 0
