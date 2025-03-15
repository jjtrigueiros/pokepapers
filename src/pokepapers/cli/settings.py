from pathlib import Path
from typing import TypedDict


class AppSettings(TypedDict):
    log_level: str
    downloads_dir: Path
    transforms_dir: Path
    pokeapi_url: str
