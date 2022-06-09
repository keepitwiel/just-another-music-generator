import logging
import os
import sys
from hashlib import md5

import numpy as np
from pydub import AudioSegment

from just_another_music_generator.generate_audio import trigger_sounds, generate_activations

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


class Automatone:
    def __init__(
        self,
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
        An Automatone is a class that defines a piece of audio generated using cellular automata.

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
        """
        self.n_rules = n_rules
        self.tone_range = tone_range
        self.sequence_length = sequence_length
        self.skip = skip
        self.sample_rate = sample_rate
        self.interval = interval
        self.tone_duration = tone_duration
        self.scale = scale
        self.root_frequency = root_frequency
        self.seed = seed

        self._activations_cached = None
        self._sequence_cached = None

    def __str__(self):
        params = f"Number of rules: {self.n_rules}\n" \
            f"Tone range: {self.tone_range}\n" \
            f"Sequence length: {self.sequence_length}\n" \
            f"Skip: {self.skip}\n" \
            f"Sample rate: {self.sample_rate}\n" \
            f"Tone interval: {self.interval}\n" \
            f"Tone duration: {self.tone_duration}\n" \
            f"Scale: {self.scale}\n" \
            f"Root frequency: {self.root_frequency}\n" \
            f"Random seed: {self.seed}\n"
        return params

    @property
    def hash(self):
        m = md5()
        m.update(bytes(self.__str__(), 'utf-8'))
        return m.hexdigest()

    @property
    def _activations(self):
        if self._activations_cached is None:
            self._activations_cached = generate_activations(
                n_rules=self.n_rules,
                tone_range=self.tone_range,
                sequence_length=self.sequence_length,
                skip=self.skip,
                seed=self.seed,
            )
        return self._activations_cached

    @property
    def _sequence(self):
        if self._sequence_cached is None:
            self._sequence_cached = trigger_sounds(
                self._activations,
                interval=self.interval,
                duration=self.tone_duration,
                scale=self.scale,
                root_frequency=self.root_frequency,
            )
        return self._sequence_cached

    def generate_audio(self):
        au = self._sequence.render(sample_rate=self.sample_rate)
        return au

# TODO: also save artifacts


def write_audio(au, sample_rate, output_root, params, hashed) -> None:
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
