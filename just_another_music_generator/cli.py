import json
import logging
import os
import sys

import click
import numpy as np

from just_another_music_generator.pipeline import generate_audio

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


@click.group()
def cli():
    pass

@cli.command()
@click.option(
    '--n-rules', default=5, show_default=True,
    help='Number of cellular automata to use.'
)
@click.option(
    '--tone-range', default=48, show_default=True,
    help='Range of tones to use in the 12-tone system.'
)
@click.option(
    '--sequence-length', default=64, show_default=True,
    help='Sequence length expressed in number of tones.'
)
@click.option(
    '--sample-rate', default=12000, show_default=True,
    help='Number of audio samples per second.'
)
@click.option(
    '--interval', default=0.125, show_default=True,
    help='Interval between onsets of tones in seconds.'
)
@click.option(
    '--tone-duration', default=0.05, show_default=True,
    help='Tone duration in seconds.'
)
@click.option(
    '--scale', default='pentatonic', show_default=True,
    help='Which musical scale to use. e.g. major, pentatonic.'
)
@click.option(
    '--root-frequency', default=110, show_default=True,
    help='frequency of the lowest note'
)
@click.option(
    '--seed', default=-1, show_default=True,
    help='Random seed. If seed < 0, a fixed nonzero initial state is used.'
)
def generate(
    n_rules,
    tone_range,
    sequence_length,
    sample_rate,
    interval,
    tone_duration,
    scale,
    root_frequency,
    seed,
):
    """
    Generates audio and saves to tmp file as Numpy array.
    """

    logger.info(f"Number of rules: {n_rules}\n"
                f"Tone range: {tone_range}\n"
                f"Sequence length: {sequence_length}\n"
                f"Sample rate: {sample_rate}\n"
                f"Tone interval: {interval}\n"
                f"Tone duration: {tone_duration}\n"
                f"Scale: {scale}\n"
                f"Root frequency: {root_frequency}\n"
                f"Random seed: {seed}\n\n")

    au = generate_audio(
        n_rules,
        tone_range,
        sequence_length,
        sample_rate,
        interval,
        tone_duration,
        scale,
        root_frequency,
        seed,
    )

    np.save('/tmp/tmp.npy', au)


if __name__ == '__main__':
    cli()
