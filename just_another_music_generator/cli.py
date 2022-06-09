import json
import logging
import os
import sys

import click
import numpy as np

from just_another_music_generator.automatone import Automatone, write_audio

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
    '--tone-range', default=24, show_default=True,
    help='Range of tones to use in the 12-tone system.'
)
@click.option(
    '--sequence-length', default=256, show_default=True,
    help='Sequence length expressed in number of tones.'
)
@click.option(
    '--skip', default=128, show_default=True,
    help='Number of initial tones to skip.'
)
@click.option(
    '--sample-rate', default=96000, show_default=True,
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
    '--root-frequency', default=440, show_default=True,
    help='frequency of the lowest note'
)
@click.option(
    '--seed', default=-1, show_default=True,
    help='Random seed. If seed < 0, a fixed nonzero initial state is used.'
)
@click.option(
    '--output-root', default='/tmp/just-another-music-generator', show_default=True,
    help='Root of the output path.'
)
def generate(
    n_rules: int,
    tone_range: int,
    sequence_length: int,
    skip: int,
    sample_rate: int,
    interval: float,
    tone_duration: float,
    scale: str,
    root_frequency: float,
    seed: int,
    output_root: str,
):
    """
    Generates audio and saves to tmp file as Numpy array.
    """

    logger.info('generating Automatone object...')
    automatone = Automatone(
        n_rules,
        tone_range,
        sequence_length,
        skip,
        sample_rate,
        interval,
        tone_duration,
        scale,
        root_frequency,
        seed,
    )

    logger.info(automatone.__str__())
    au = automatone.render_audio()
    graph = automatone.render_graph()

    logger.info(f'Write audio to file.'
                f'Root dir: {output_root}'
                f'Hash: {automatone.hash}')

    write_audio(au, sample_rate, output_root, automatone.__str__(), automatone.hash)


if __name__ == '__main__':
    cli()
