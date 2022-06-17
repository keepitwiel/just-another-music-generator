import os
from click.testing import CliRunner

from just_another_music_generator.cli import generate, parse_rules, parse_adslr

runner = CliRunner()


def test_parse_rules_ok_1():
    result = parse_rules("1")
    assert result == [1]


def test_parse_rules_ok_2():
    result = parse_rules("1,2,3")
    assert result == [1, 2, 3]


def test_parse_adslr_ok_2():
    result = parse_adslr("0.1,0.2,0.3")
    assert result == [0.1, 0.2, 0.3]


def test_parse_rules_from_cli_ok_1():
    response = runner.invoke(generate, ["--rules", "2"])
    assert response.exit_code == 0


def test_parse_rules_from_cli_ok_2():
    response = runner.invoke(generate, ["--rules", "2,3"])
    assert response.exit_code == 0


def test_parse_rules_from_cli_error():
    response = runner.invoke(generate, ["--rules", "2 3"])
    assert response.exit_code == 1


def test_cli_works():
    basepath = os.getcwd()
    outpath = "output"
    fullpath = os.path.join(basepath, outpath)
    response = runner.invoke(generate, ["--output-root", fullpath])
    assert response.exit_code == 0


def test_cli_fails():
    response = runner.invoke(generate, ["--foo", "bar"])
    assert response.exit_code == 2
