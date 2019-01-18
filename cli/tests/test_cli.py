import pytest
from click.testing import CliRunner
from seneca import cli

@pytest.fixture
def runner():
    return CliRunner()


def test_cli_prophet(runner):
    result = runner.invoke(cli.main, ["-c","/Users/michaelzhang/Downloads/Seneca/config/prophet/config.py", "-m", "prophet"])
    assert not result.exception
    assert result.exit_code == 0
