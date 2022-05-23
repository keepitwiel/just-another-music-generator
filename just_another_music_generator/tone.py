import numpy as np


class Tone:
    def __init__(self, start_time: float, duration: float, pitch: float, volume: float) -> None:
        """
        Defines a sine carrier wave that is convoluted
        with another sine wave (the "envelope") between 0 and pi.

        :param start_time: start time of the note
        :param duration: duration of the note
        :param pitch: tone pitch in Hertz
        """
        self.start_time = start_time
        self.duration = duration
        self.pitch = pitch
        self.volume = volume

    def render(self, t):
        """
        renders tone value at given time

        :param t: time at which to render the tone (can be a scalar or array)
        :return: rendered value
        """
        if type(t) == float:
            x = 0
            u = t - self.start_time
            if 0 < u < self.duration:
                envelope_phase = (u / self.duration) * np.pi
                envelope = np.sin(envelope_phase)
                tone_phase = u * self.pitch * 2 * np.pi
                tone = np.sin(tone_phase)
                x = self.volume * envelope * tone
            return x
        elif type(t) == np.ndarray:
            x = np.empty_like(t)
            u = t - self.start_time
            envelope_phase = u * np.pi
            envelope = ((0 < u) & (u < self.duration)) * np.sin(envelope_phase)
            tone_phase = u * self.pitch * 2 * np.pi
            tone = np.sin(tone_phase)
            x = self.volume * envelope * tone
            return x
