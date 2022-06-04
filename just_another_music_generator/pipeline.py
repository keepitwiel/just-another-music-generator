import logging
import os
import sys

import numpy as np
from pydub import AudioSegment

from just_another_music_generator.generate_audio import generate_audio

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


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

    # TODO: use a deterministic hash
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
