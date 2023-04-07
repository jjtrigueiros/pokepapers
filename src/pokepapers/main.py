#!usr/bin/env python3

import asyncio

from pathlib import Path
from time import perf_counter

import typer

from .download_image import download_image_set_async
from .lib import settings
from .pokeapi import PokeAPI

app = typer.Typer()


# STORE_PAGE_URL = 'https://originalstitch.com/pokemon/order/'
LIST_OF_POKEMON: list[str] = client.list_pokemon()
DOWNLOAD_FROM_URLS: list[str] = [
    f"{settings.app.IMAGES_SOURCE_URL}{pokemon_id}.jpg"
    for pokemon_id in range(1, settings.app.NUMBER_OF_POKEMON + 1)
]


@app.command()
def download():
    """Downloads all Pokémon patterns into the configured output folder."""
    urls = DOWNLOAD_FROM_URLS
    filenames = [f"{i+1}_{LIST_OF_POKEMON[i]}" for i in range(len(LIST_OF_POKEMON))]

    # create output directory (prompt)
    dl_folder = Path(settings.app.PATTERNS_DIRECTORY)
    if not dl_folder.is_dir():
        if input(f'Create directory on "{dl_folder}" ? (y/N)') in {"y", "Y"}:
            dl_folder.mkdir(parents=True, exist_ok=True)
        else:
            raise Exception("Could not create download directory.")

    start_time = perf_counter()
    asyncio.run(download_image_set_async(urls, dl_folder, filenames))
    print(f"Finished in {round(perf_counter() - start_time, 2)} seconds!")


@app.command()
def search(pkmn: str):
    """Returns the pokémon National ID for a given pokémon name."""
    client = PokeAPI()
    id: int = client.get_id(pkmn)
    print(id)
