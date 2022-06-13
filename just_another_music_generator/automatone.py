from typing import List, Union
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

POSSIBLE_RULES = [i for i in range(1, 255)]


class Automatone:
    def __init__(
        self,
        rules: Union[int, List[int]],
        tone_range: int,
        sequence_length: int,
        skip: int,
        interval: float,
        tone_duration: float,
        scale: str,
        root_frequency: float,
    ):
        """
        An Automatone is a class that defines a piece of audio generated using cellular automata.

        :param rules: fundamental cellular automata rules to use. If this parameter is an integer,
            then this number of rules will be randomly chosen; if it is a list, we use the rules
            identified in the list.
        :param tone_range: range of tones to use in the 12-tone system
        :param sequence_length: sequence length
        :param skip: number of tones to skip from start
        :param interval: interval between tones in seconds
        :param tone_duration: tone duration in seconds
        :param scale: which musical scale to use. e.g. major, pentatonic
        :param root_frequency: frequency of the lowest note
        """
        # TODO: move unnecessary parameters away from init (such as sample rate)
        # TODO: rethink randomness: only randomize rules
        if type(rules) == int:
            self.seed = np.random.randint(0, 2 ** 31)
            self.rules = np.random.choice(POSSIBLE_RULES, rules, replace=False)
        elif type(rules) == list:
            self.rules = rules
            self.seed = -1

        self.tone_range = tone_range
        self.sequence_length = sequence_length
        self.skip = skip
        self.interval = interval
        self.tone_duration = tone_duration
        self.scale = scale
        self.root_frequency = root_frequency

    def __str__(self):
        params = f"Selected rules: {self.rules}\n" \
            f"Random seed: {self.seed}\n" \
            f"Tone range: {self.tone_range}\n" \
            f"Sequence length: {self.sequence_length}\n" \
            f"Skip: {self.skip}\n" \
            f"Tone interval: {self.interval}\n" \
            f"Tone duration: {self.tone_duration}\n" \
            f"Scale: {self.scale}\n" \
            f"Root frequency: {self.root_frequency}\n"
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
            rules=self.rules,
            tone_range=self.tone_range,
            sequence_length=self.sequence_length,
            skip=self.skip,
        )
        return result

    @property
    def _frequencies(self):
        # TODO: include 'A4, A#4, B4 etc. notation'
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
        axes.set_title(f'rules: {self.rules}, seed: {self.seed}, scale: {self.scale}')
        axes.set_xlabel('Time step')
        axes.set_ylabel('Pitch (Hz)')
        step_size = 1
        if len(freqs) >= 10:
            step_size = len(freqs) // 5
        axes.set_yticks(ticks=range(0, len(freqs), step_size), labels=freqs[::step_size])
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
