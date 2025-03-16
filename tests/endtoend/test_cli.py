from pathlib import Path
import pytest
from typer.testing import CliRunner

from pokepapers.cli.app import app


runner = CliRunner()


@pytest.mark.vcr
def test_download(tmp_path: Path):
    result = runner.invoke(app, ["download", "--downloads-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert len(list(tmp_path.iterdir())) > 0
