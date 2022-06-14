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
        wave: str = "square",
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

    def _calculate_envelope(self, t):
        """
        Given an array with time stamps, calculate the
        loudness envelope of the tone for each time stamp.

        :param t: array with time stamps
        :return: envelope value for each time stamp
        """
        result = (0 < t) & (t < self._duration)

        # TODO: ADSR
        return result * (1 - t / self._duration)

    def render(self, t: np.ndarray) -> np.ndarray:
        """
        renders tone value at given time

        :param t: array of timestamps at which to render the tone
        :return: rendered value
        """

        # shift time stamps to start of tone
        u = t - self.start_time

        envelope = self._calculate_envelope(u)

        carrier_phase = u * self.pitch * 2 * np.pi
        if self.wave == "sin":
            carrier = np.sin(carrier_phase)
        elif self.wave == "square":
            carrier = np.sign(np.sin(carrier_phase))
        else:
            raise NotImplementedError

        noise = np.random.normal(0, 1, len(u))
        mixed = (1 - self.noise) * carrier + self.noise * noise
        x = self.volume * envelope * mixed
        return x
