import logging
import os
import sys

import numpy as np
from pydub import AudioSegment

from just_another_music_generator.automata import generate_cellular_automaton
from just_another_music_generator.sequence import Sequence
from just_another_music_generator.tone import Tone


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


MAJOR = [0, 2, 4, 5, 7, 9, 11, 12]
PENTATONIC = [0, 3, 5, 7, 10, 12]  # note: minor pentatonic


def generate_activations(n_rules: int, tone_range: int, sequence_length: int, skip: int, seed: int):
    """
    Generates boolean matrices from 1-D cellular automata with randomly selected rules,
    and then performs the elemtwise "and" operation on all of them.

    The resulting matrix indicates instrument activations.

    :param n_rules: number of rules to randomly select
    :param tone_range: range of tones to use in the 12-tone system
    :param sequence_length: sequence length
    :param skip: number of initial tones to skip
    :param seed: random seed. if seed < 0, a single fixed rule (30) is chosen
    :return: sequence_length x tone_range boolean matrix
    """
    # we exclude rule 0 and 255, because they produce all 0s or all 1s
    possible_rules = [i for i in range(1, 255)]
    if seed < 0:
        rules = np.array([30] * n_rules)
    else:
        np.random.seed(seed)
        rules = np.random.choice(possible_rules, n_rules, replace=False)
    result = [
        generate_cellular_automaton(
            rule=rule, size=tone_range, steps=sequence_length, skip=skip, seed=seed,
        )
        for rule in rules
    ]
    result = np.prod(np.stack(result, axis=2), axis=2)
    return result


def trigger_sounds(activations: np.ndarray, interval: float, duration: float, scale: str, root_frequency: float):
    """
    given boolean activation matrix, trigger sounds where matrix == 1 into a Sequence object

    :param activations: boolean activation matrix
    :param interval: time between activations
    :param duration: tone duration in seconds
    :param scale: musical scale
    :param root_frequency: frequency of the lowest note
    :return: Sequence object
    """
    s = Sequence()

    for n in range(activations.shape[0]):
        for m in range(activations.shape[1]):
            if activations[n, m]:
                if scale == 'major':
                    octave = m // 8
                    note_in_octave = MAJOR[m % 8]
                elif scale == 'pentatonic':
                    octave = m // 5
                    note_in_octave = PENTATONIC[m % 5]
                else:
                    raise NotImplementedError

                note = octave * 8 + note_in_octave
                tone = Tone(
                    start_time=interval * n,
                    duration=duration,
                    pitch=root_frequency * (2 ** (note / 12)),
                    volume=0.5,
                )
                s.add(tone)
    return s


def generate_audio(
    n_rules: int,
    tone_range: int,
    sequence_length: int,
    skip: int,
    sample_rate: int,
    interval: float,
    tone_duration: float,
    scale: str,
    root_frequency: float,
    seed: int,
):
    """
    Generates audio

    :param n_rules: number of cellular automata to use
    :param tone_range: range of tones to use in the 12-tone system
    :param sequence_length: sequence length
    :param skip: number of tones to skip from start
    :param sample_rate: number of audio samples per second
    :param interval: interval between tones in seconds
    :param tone_duration: tone duration in seconds
    :param scale: which musical scale to use. e.g. major, pentatonic
    :param root_frequency: frequency of the lowest note
    :param seed: random seed
    :return: numpy array containing audio
    """
    activations = generate_activations(
        n_rules=n_rules,
        tone_range=tone_range,
        sequence_length=sequence_length,
        skip=skip,
        seed=seed,
    )
    seq = trigger_sounds(activations, interval, tone_duration, scale, root_frequency)
    print(f"Tones in sequence: {len(seq)}, duration: {seq.duration}")
    au = seq.render(sample_rate=sample_rate)
    return au


def pipeline(
    n_rules: int,
    tone_range: int,
    sequence_length: int,
    skip: int,
    sample_rate: int,
    interval: float,
    tone_duration: float,
    scale: str,
    root_frequency: float,
    seed: int,
    output_root: str,
) -> None:
    params = f"Number of rules: {n_rules}\n" \
        f"Tone range: {tone_range}\n" \
        f"Sequence length: {sequence_length}\n" \
        f"Skip: {skip}\n" \
        f"Sample rate: {sample_rate}\n" \
        f"Tone interval: {interval}\n" \
        f"Tone duration: {tone_duration}\n" \
        f"Scale: {scale}\n" \
        f"Root frequency: {root_frequency}\n" \
        f"Random seed: {seed}\n" \
        f"Output root path: {output_root}\n"

    logger.info(params)

    hashed = hex(abs(hash(params)))[2:]
    logger.info(f"Unique hash of parameters: {hashed}")

    au = generate_audio(
        n_rules,
        tone_range,
        sequence_length,
        skip,
        sample_rate,
        interval,
        tone_duration,
        scale,
        root_frequency,
        seed,
    )

    # TODO: also save artifacts

    if not (os.path.exists(output_root)):
        os.mkdir(output_root)

    path = f'{output_root}/{hashed}'
    if not (os.path.exists(path)):
        os.mkdir(path)

    params_path = f'{path}/params.txt'
    logger.info(f'Write parameters to {params_path}...')
    try:
        with open(params_path, 'w+') as file:
            file.write(params)
    except IOError as e:
        logger.error(f'Error writing file: {e}')

    audio_path = f'{path}/audio.wav'

    logger.info(f'Write audio to {audio_path}...')
    segment = create_audiosegment(au, sample_rate=sample_rate)
    try:
        segment.export(audio_path, format='wav')
    except IOError as e:
        logger.error(f'Error writing file: {e}')


def create_audiosegment(arr: np.ndarray, sample_rate: int) -> AudioSegment:
    tmp = (arr * 2**31).astype(np.int32)
    result = AudioSegment(
        tmp.tobytes(),
        frame_rate=sample_rate,
        sample_width=tmp.dtype.itemsize,
        channels=1,
    )
    return result
