import logging
import os
import sys
from hashlib import md5

import numpy as np
from pydub import AudioSegment
from matplotlib import pyplot as plt

from just_another_music_generator.activations import trigger_sounds, generate_activations

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11, 12],
    'pentatonic': [0, 3, 5, 7, 10, 12],  # note: minor pentatonic
    'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
}

class Automatone:
    def __init__(
        self,
        n_rules: int,
        tone_range: int,
        sequence_length: int,
        skip: int,
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
        :param interval: interval between tones in seconds
        :param tone_duration: tone duration in seconds
        :param scale: which musical scale to use. e.g. major, pentatonic
        :param root_frequency: frequency of the lowest note
        :param seed: random seed
        """
        # TODO: move unnecessary parameters away from init (such as sample rate)
        self.n_rules = n_rules
        self.tone_range = tone_range
        self.sequence_length = sequence_length
        self.skip = skip
        self.interval = interval
        self.tone_duration = tone_duration
        self.scale = scale
        self.root_frequency = root_frequency
        self.seed = seed

    def __str__(self):
        params = f"Number of rules: {self.n_rules}\n" \
            f"Tone range: {self.tone_range}\n" \
            f"Sequence length: {self.sequence_length}\n" \
            f"Skip: {self.skip}\n" \
            f"Tone interval: {self.interval}\n" \
            f"Tone duration: {self.tone_duration}\n" \
            f"Scale: {self.scale}\n" \
            f"Root frequency: {self.root_frequency}\n" \
            f"Random seed: {self.seed}\n"
        return params

    @property
    def hash(self):
        # todo: only hash relevant parameters
        m = md5()
        m.update(bytes(self.__str__(), 'utf-8'))
        return m.hexdigest()

    @property
    def _activations(self):
        result = generate_activations(
                n_rules=self.n_rules,
                tone_range=self.tone_range,
                sequence_length=self.sequence_length,
                skip=self.skip,
                seed=self.seed,
            )
        return result

    @property
    def _frequencies(self):
        result = []

        try:
            scale_idx = SCALES[self.scale]
        except KeyError as e:
            logger.error(f'Scale {self.scale} not found: {e}')
            raise

        for m in range(self.tone_range):
            n = len(scale_idx) - 1
            octave = m // n
            note_in_octave = scale_idx[m % n]
            note = octave * 12 + note_in_octave

            frequency = self.root_frequency * (2 ** (note / 12))
            result.append(frequency)

        return result

    @property
    def _sequence(self):
        result = trigger_sounds(
            self._activations,
            interval=self.interval,
            duration=self.tone_duration,
            frequencies=self._frequencies,
        )
        return result

    def render_audio(self, sample_rate: int, progress_bar: bool = False):
        sequence = self._sequence
        au = sequence.render(sample_rate=sample_rate, progress_bar=progress_bar)
        return au

    def render_graph(self):
        fig, axes = plt.subplots(1, 1, figsize=(10, 6))
        img = self._activations.T
        freqs = [f'{freq:2.0f}' for freq in self._frequencies]
        axes.imshow(img)
        axes.set_title(f'n_rules: {self.n_rules}, seed: {self.seed}, scale: {self.scale}')
        axes.set_xlabel('Time step')
        axes.set_ylabel('Pitch (Hz)')
        axes.set_yticks(ticks=range(len(freqs)), labels=freqs)
        return axes


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
