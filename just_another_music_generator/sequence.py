import numpy as np
from tqdm import tqdm

from just_another_music_generator.tone import Tone


class Sequence:
    def __init__(self) -> None:
        self.sequence = []

    def add(self, tone: Tone) -> None:
        """
        Add a tone to the sequence
        :param tone: a tone

        :return: None
        """
        self.sequence.append(tone)

    def __len__(self):
        return len(self.sequence)

    @property
    def duration(self) -> float:
        duration = 1
        for tone in self.sequence:
            d = tone.start_time + tone.duration
            if d > duration:
                duration = d

        return duration

    def render(self, sample_rate: int, normalize: bool = True) -> np.ndarray:
        n = np.ceil(sample_rate * self.duration).astype(int)
        result = np.zeros(n)
        t = np.linspace(0, self.duration, n)
        assert len(t) == len(result)

        for i, tone in enumerate(tqdm(self.sequence)):
            result += tone.render(t)

        if normalize:
            minimum = np.min(result)
            maximum = np.max(result)
            absmax = np.max(np.abs([minimum, maximum]))
            result /= absmax

        return result
