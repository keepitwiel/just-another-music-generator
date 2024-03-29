import logging
import sys

import click

from automatone import Automatone
from audio import write_audio

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--rules",
    default="[30]",
    show_default=True,
    help="""
    Fundamental cellular automata rules to use.
    If value is integer, randomly select that number of rules.
    """,
)
@click.option(
    "--tone-range",
    default=24,
    show_default=True,
    help="Range of tones to use in the 12-tone system.",
)
@click.option(
    "--sequence-length",
    default=256,
    show_default=True,
    help="Sequence length expressed in number of tones.",
)
@click.option(
    "--sequence-offset",
    default=0,
    show_default=True,
    help="Number of time steps to skip from start.",
)
@click.option(
    "--skip",
    default=128,
    show_default=True,
    help="Number of initial rows in cellular automata to skip.",
)
@click.option(
    "--sample-rate",
    default=96000,
    show_default=True,
    help="Number of audio samples per second.",
)
@click.option(
    "--interval",
    default=0.125,
    show_default=True,
    help="Interval between onsets of tones in seconds.",
)
@click.option(
    "--adslr",
    default="0.01,0.02,0.03,0.5,0.04",
    show_default=True,
    help="adslr: (a)ttack, (d)ecay, (s)ustain, -(l)evel, "
    "(r)release parameters. adsr in seconds, level between 0 and 1",
)
@click.option(
    "--scale",
    default="pentatonic",
    show_default=True,
    help="Which musical scale to use. e.g. major, pentatonic.",
)
@click.option(
    "--root-frequency",
    default=440,
    show_default=True,
    help="frequency of the lowest note",
)
@click.option(
    "--pan",
    default=0.5,
    show_default=True,
    help="Stereo pan (0.0 = left, 0.5 = center, 1.0 = right)",
)
@click.option(
    "--volume",
    default=0.5,
    show_default=True,
    help="Relative volume. Can be any number",
)
@click.option(
    "--output-root",
    default="/tmp/just-another-music-generator",
    show_default=True,
    help="Root of the output path.",
)
def generate(
    rules: str,
    tone_range: int,
    sequence_length: int,
    sequence_offset: int,
    skip: int,
    sample_rate: int,
    interval: float,
    adslr: str,
    scale: str,
    root_frequency: float,
    pan: float,
    volume: float,
    output_root: str,
):
    """
    Generates audio and saves to tmp file as Numpy array.
    """

    logger.info("generating Automatone object...")
    rules = parse_rules(rules)
    adslr = parse_adslr(adslr)

    automatone = Automatone(
        rules=rules,
        tone_range=tone_range,
        sequence_length=sequence_length,
        sequence_offset=sequence_offset,
        skip=skip,
        interval=interval,
        attack_time=adslr[0],
        decay_time=adslr[1],
        sustain_time=adslr[2],
        sustain_level=adslr[3],
        release_time=adslr[4],
        scale=scale,
        root_frequency=root_frequency,
        pan=pan,
        volume=volume,
        wave="square",
        noise_ratio=0.1,
    )

    logger.info(automatone.__str__())
    au = automatone.render_audio(sample_rate=sample_rate)

    logger.info(f"Write audio to file. Output dir: {output_root}")
    logger.info(f"Hash: {automatone.hash}")

    write_audio(au, sample_rate, output_root)


def parse_rules(rules):
    rules = rules.strip("[]")
    rules = rules.split(",")
    try:
        rules = [int(rule) for rule in rules]
    except ValueError:
        raise """
        Invalid parameter passed: rules. "rules" should be either
        an integer or a list of integers separated by commas (e.g. "1,2,3,5,8")
        """
    return rules


def parse_adslr(string):
    s = string.strip("[]")
    s = s.split(",")
    try:
        adslr = [float(v) for v in s]
    except ValueError:
        raise """
        Invalid parameter passed: rules. "rules" should be either
        an integer or a list of integers separated by commas (e.g. "1,2,3,5,8")
        """
    return adslr


if __name__ == "__main__":
    cli()
