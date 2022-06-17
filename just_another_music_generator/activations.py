from typing import List, Any

import numpy as np

from just_another_music_generator.automata import generate_cellular_automaton
from just_another_music_generator.sequence import Sequence
from just_another_music_generator.tone import Tone


def generate_activations(
    rules: List[int], tone_range: int, sequence_length: int, skip: int
) -> np.ndarray[Any, Any]:
    """
    Generates boolean matrices from 1-D cellular automata with
    randomly selected rules, and then performs the elemtwise "and"
    operation on all of them.

    The resulting matrix indicates instrument activations.

    :param rules: rules to use for calculating cell values
    :param tone_range: range of tones to use in the 12-tone system
    :param sequence_length: sequence length
    :param skip: number of initial tones to skip
    :return: sequence_length x tone_range boolean matrix
    """
    # we exclude rule 0 and 255, because they produce all 0s or all 1s
    result = [
        generate_cellular_automaton(
            rule=rule,
            size=tone_range,
            steps=sequence_length,
            skip=skip,
        )
        for rule in rules
    ]
    result = np.prod(np.stack(result, axis=2), axis=2)
    return result


def trigger_sounds(
    activations: np.ndarray,
    interval: float,
    sequence_offset: int,
    attack_time: float,
    decay_time: float,
    sustain_time: float,
    sustain_level: float,
    release_time: float,
    frequencies: List[float],
    pan: float,
    volume: float,
) -> Sequence:
    """
    given boolean activation matrix, trigger sounds where
    matrix == 1 into a Sequence object

    :param attack_time: attack duration of envelope in seconds
    :param decay_time: decay duration of envelope in seconds
    :param sustain_time: sustain duration of envelope in seconds
    :param sustain_level: sustain level of envelope
    :param release_time: release duration of envelope in seconds
    :param activations: boolean activation matrix
    :param interval: time between activations
    :param sequence_offset: number of empty activations before start
        I.e. if sequence_offset = 10, then the 1st activation
        will start at 10
    :param release_time: tone duration in seconds
    :param frequencies: list of frequencies to trigger
    :param pan: stereo panning (0=left, 1=right)
    :return: Sequence object
    """
    s = Sequence()

    for time_idx in range(activations.shape[0]):
        for tone_idx in range(activations.shape[1]):
            if activations[time_idx, tone_idx] > 0:
                frequency = frequencies[tone_idx]
                tone = Tone(
                    start_time=interval * (time_idx + sequence_offset),
                    attack_time=attack_time,
                    decay_time=decay_time,
                    sustain_time=sustain_time,
                    sustain_level=sustain_level,
                    release_time=release_time,
                    pitch=frequency,
                    volume=volume,
                    pan=pan,
                )
                s.add([tone])
    return s
