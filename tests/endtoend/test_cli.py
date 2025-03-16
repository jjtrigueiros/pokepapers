from pathlib import Path
import cv2
import numpy as np
import pytest
from typer.testing import CliRunner

from pokepapers.cli.app import app


runner = CliRunner()


RESOURCES = Path("./tests/endtoend/resources/")
BASE_IMAGE = RESOURCES / "272_ludicolo.png"  # 1160x1160p
REF_IMAGE_1280X720P_2P5 = RESOURCES / "272_ludicolo_1280x720_x2p5.png"


@pytest.mark.vcr
def test_download(tmp_path: Path):
    result = runner.invoke(app, ["download", "--downloads-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert len(list(tmp_path.iterdir())) > 0


def test_generate(tmp_path: Path):
    output_path = tmp_path / "output.png"
    result = runner.invoke(
        app,
        [
            "generate",
            str(BASE_IMAGE),
            "--output",
            str(output_path),
            "--width",
            "1280",
            "--height",
            "720",
            "--scaling",
            "2.5",
        ],
    )
    assert result.exit_code == 0
    assert output_path.is_file()
    assert np.array_equal(
        cv2.imread(str(output_path)),
        cv2.imread(str(REF_IMAGE_1280X720P_2P5)),
    )
