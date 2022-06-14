import numpy as np


def interpolate(
    t: np.ndarray,
    t0: float,
    t1: float,
    level0: float,
    level1: float,
) -> np.ndarray:
    """
    Calculates interpolated envelope between two times
    given a start and end level.

    :param t: time stamps
    :param t0: start time
    :param t1: end time
    :param level0: start level
    :param level1: end level
    :return: array containing interpolated envelope
    """
    envelope = ((t0 <= t) * (t < t1)).astype(np.float64)
    if t1 > t0:
        tt = (t - t0) / (t1 - t0)
        envelope *= level1 * tt + level0 * (1 - tt)
    return envelope


class Tone:
    def __init__(
        self,
        start_time: float,
        attack_time: float,
        decay_time: float,
        sustain_time: float,
        sustain_level: float,
        release_time: float,
        pitch: float,
        volume: float,
        pan: float,
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
        self.pan = pan
        self.wave = wave

        self.attack = attack_time
        self.decay_time = decay_time
        self.sustain_time = sustain_time
        self.sustain_level = sustain_level
        self.release_time = release_time

        self.noise = 0.1

    @property
    def _duration(self):
        result = self.attack + self.decay_time
        result = result + self.sustain_time + self.release_time
        return result

    @property
    def _pan(self):
        return np.clip(self.pan, 0, 1)

    def _calculate_envelope(self, t: np.ndarray) -> np.ndarray:
        """
        Given an array with time stamps, calculate the
        loudness envelope of the tone for each time stamp.

        :param t: array with time stamps
        :return: envelope value for each time stamp
        """

        result = np.zeros(t.shape)

        # calculate ADSR times
        t0 = 0.0
        t1 = self.attack
        t2 = t1 + self.decay_time
        t3 = t2 + self.sustain_time
        t4 = self._duration

        # calculate ADSR envelopes
        attack_envelope = interpolate(t, t0, t1, 0, 1)
        decay_envelope = interpolate(t, t1, t2, 1, self.sustain_level)
        sustain_envelope = interpolate(
            t, t2, t3, self.sustain_level, self.sustain_level
        )
        release_envelope = interpolate(t, t3, t4, self.sustain_level, 0)

        # add them to result
        result = (
            result
            + attack_envelope
            + decay_envelope
            + sustain_envelope
            + release_envelope
        )

        return result

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
        x = x.reshape(-1, 1)

        # sine law panning
        left = np.sin((1 - self._pan) * np.pi / 2) * x
        right = np.sin(self._pan * np.pi / 2) * x

        result = np.concatenate([left * x, right * x], axis=1)
        return result
