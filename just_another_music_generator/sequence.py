from typing import Tuple, List

import numpy as np
from tqdm import tqdm

from just_another_music_generator.tone import Tone


def find_bounds(tone: Tone, sample_rate: int) -> Tuple[int, int]:
    """
    Given a Tone object, find the global indices of the first and last sample of that tone
    (i_start and i_end).

    :param tone: Tone object
    :param t: array containing the timestamps of all samples
    :param sample_rate: sample rate in Hz
    :return: start and end samples of tone

    For example, if a tone has start_time = 1.00001 and duration = 0.5,
    and sample_rate = 10000, then i_start = 10000 and i_end = 15001
    """
    t_start = tone.start_time
    t_end = tone.start_time + tone._duration

    i_start = np.floor(t_start * sample_rate).astype(int)
    i_end = np.ceil(t_end * sample_rate).astype(int)

    return i_start, i_end


class Sequence:
    def __init__(self) -> None:
        self.sequence = []

    def add(self, other: List) -> None:
        """
        Add one or more tones to the sequence
        :param other: a list of tones

        :return: None
        """
        self.sequence += other

    def __len__(self):
        return len(self.sequence)

    @property
    def duration(self) -> float:
        duration = 1
        for tone in self.sequence:
            d = tone.start_time + tone._duration
            if d > duration:
                duration = d

        return duration

    def render(self, sample_rate: int, normalize: bool = True, progress_bar: bool = False) -> np.ndarray:
        n = np.ceil(sample_rate * self.duration).astype(int)
        result = np.zeros(n)
        t = np.linspace(0, self.duration, n)
        assert len(t) == len(result)

        if progress_bar:
            enum = tqdm(self.sequence)
        else:
            enum = self.sequence

        for i, tone in enumerate(enum):
            i_start, i_end = find_bounds(tone, sample_rate)
            result[i_start:i_end] += tone.render(t[i_start:i_end])

        if normalize:
            minimum = np.min(result)
            maximum = np.max(result)
            absmax = np.max(np.abs([minimum, maximum]))
            result /= absmax

        return result
