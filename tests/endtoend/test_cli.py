from pathlib import Path
import pytest

from pokepapers.cli import download


@pytest.mark.vcr
def test_download(tmp_path: Path):
    download(downloads_dir=tmp_path)
    assert len(list(tmp_path.iterdir())) > 0
