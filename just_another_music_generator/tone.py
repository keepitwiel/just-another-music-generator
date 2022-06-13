import numpy as np


class Tone:
    def __init__(
        self,
        start_time: float,
        attack: float,
        decay: float,
        sustain_time: float,
        sustain_level: float,
        release: float,
        pitch: float,
        volume: float,
        wave: str = 'square'
    ) -> None:
        """
        Defines a sine carrier wave that is convoluted
        with another sine wave (the "envelope") between 0 and pi.

        :param start_time: start time of the note
        :param duration: duration of the note
        :param pitch: tone pitch in Hertz
        """
        # TODO: implement Attack/Decay/Sustain/Release
        self.start_time = start_time
        self.pitch = pitch
        self.volume = volume
        self.wave = wave

        self.attack = attack
        self.decay = decay
        self.sustain_time = sustain_time
        self.sustain_level = sustain_level
        self.release = release

        self.noise = 0.1

    @property
    def _duration(self):
        return self.attack + self.decay + self.sustain_time + self.release

    # def render(self, t: np.ndarray) -> np.ndarray:
    #     """
    #     renders tone value at given time
    #
    #     :param t: array of timestamps at which to render the tone
    #     :return: rendered value
    #     """
    #     return self.render_array(t)

    def render(self, t: np.ndarray) -> np.ndarray:
        """
        renders tone value at given time

        :param t: array of timestamps at which to render the tone
        :return: rendered value
        """
        u = t - self.start_time

        envelope = ((0 < u) & (u < self._duration))

        # TODO: fix this with ADSR
        envelope = envelope * (1 - u / self._duration)

        carrier_phase = u * self.pitch * 2 * np.pi
        if self.wave == 'sin':
            carrier = np.sin(carrier_phase)
        elif self.wave == 'square':
            carrier = np.sign(np.sin(carrier_phase))
        else:
            raise NotImplementedError

        noise = np.random.normal(0, 1, len(u))
        x = self.volume * envelope * ((1 - self.noise) * carrier + self.noise * noise)
        return x
