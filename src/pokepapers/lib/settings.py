"""Set configuration via environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        case_sensitive = True

    PATTERNS_DIRECTORY: Path = Path("./out/patterns/")
    WALLPAPER_DIRECTORY: Path = Path("./out/wallpapers/")
    POKEAPI_URL: str = "https://pokeapi.co/api/v2/"
    NUMBER_OF_POKEMON: int = 845
    # Gen 1 - #151 Mew
    # ...
    # Gen 4 - #493 Arceus
    # Gen 5 - #649 Genesect
    # ...
    # Gen 8 - #905 Enamorus
    # Gen 9 - #1010 Iron Leaves
    # Known patterns: 1 to 493 + 810, 813, 816, 819, 845


app = AppSettings()
