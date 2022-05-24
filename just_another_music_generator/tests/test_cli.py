from click.testing import CliRunner

from just_another_music_generator.cli import generate

runner = CliRunner()


def test_cli_works():
    response = runner.invoke(generate)
    assert response.exit_code == 0


def test_cli_fails():
    response = runner.invoke(generate, ["--foo", "bar"])
    assert response.exit_code == 2
