import os
from click.testing import CliRunner

from just_another_music_generator.cli import generate

runner = CliRunner()


def test_cli_works():
    basepath = os.getcwd()
    outpath = 'output'
    fullpath = os.path.join(basepath, outpath)
    response = runner.invoke(generate, ['--output-root', fullpath])
    assert response.exit_code == 0


def test_cli_fails():
    response = runner.invoke(generate, ['--foo', 'bar'])
    assert response.exit_code == 2
