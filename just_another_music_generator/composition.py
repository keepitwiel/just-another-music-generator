import numpy as np

from just_another_music_generator.automatone import Automatone
from just_another_music_generator.sequence import Sequence


class Composition:
    def __init__(self):
        self.automatones = []

    def add(self, automatone: Automatone):
        self.automatones.append(automatone)

    def render_audio(self, sample_rate, normalize):
        sequence = Sequence()
        for automatone in self.automatones:
            sequence.add(automatone._sequence.sequence)

        audio = sequence.render(sample_rate=sample_rate, normalize=normalize)
        return audio

    def activations(self):
        activations = []
        for automatone in self.automatones:
            activations.append(automatone._activations)

        new_activations = []
        max_width = np.max([a.shape[1] for a in activations])
        for a in activations:
            new = np.zeros((a.shape[0], max_width))
            new[: a.shape[0], : a.shape[1]] = a
            new_activations.append(new)

        result = np.concatenate(new_activations, axis=0)
        return result
