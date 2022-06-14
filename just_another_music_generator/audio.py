import os
import sys
import logging

import numpy as np
from pydub import AudioSegment

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def write_audio(au, sample_rate, output_path) -> None:
    if not (os.path.exists(output_path)):
        os.mkdir(output_path)

    audio_path = f"{output_path}/audio.wav"

    logger.info(f"Write audio to {audio_path}...")
    segment = create_audiosegment(au, sample_rate=sample_rate)
    try:
        segment.export(audio_path, format="wav")
    except IOError as e:
        logger.error(f"Error writing file: {e}")


def create_audiosegment(arr: np.ndarray, sample_rate: int) -> AudioSegment:
    tmp = (arr * 2**31).astype(np.int32)
    result = AudioSegment(
        tmp.tobytes(),
        frame_rate=sample_rate,
        sample_width=tmp.dtype.itemsize,
        channels=1,
    )
    return result
