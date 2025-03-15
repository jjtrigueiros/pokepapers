import asyncio
from typing_extensions import Annotated
from pathlib import Path
from time import perf_counter

import aiohttp
import typer
from loguru import logger

from pokepapers.cli.settings import AppSettings
from pokepapers.resolutions import autocomplete_resolution_name
from pokepapers.services.image_downloader import create_image_downloader
from pokepapers.services.scrapers.serebii import SerebiiPokeprintCollector


# typer isn't big on dependency injection, so we'll have to make do with a global settings object
# https://github.com/fastapi/typer/issues/80
settings: AppSettings = AppSettings(
    log_level="INFO",
    downloads_dir=Path("./out/downloads/"),
    transforms_dir=Path("./out/wallpapers/"),
    pokeapi_url="https://pokeapi.co/api/v2/",
)


def callback(
    log_level: Annotated[str, typer.Option(envvar="PPP_LOG_LEVEL")] = settings[
        "log_level"
    ],
):
    global settings
    settings |= {"log_level": log_level}
    logger.level(log_level)


def download(
    downloads_dir: Annotated[Path, typer.Option(envvar="PPP_DOWNLOADS_DIR")] = settings[
        "downloads_dir"
    ],
):
    """
    Downloads all Pokémon patterns into the configured output folder.

    Default: download from Serebii.
    Planned: other sources like Bulbapedia or custom/self-hosted
    """
    asyncio.run(download_async(downloads_dir))


async def download_async(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    start_time = perf_counter()
    connector = aiohttp.TCPConnector(limit=20)
    async with aiohttp.ClientSession(connector=connector) as session:
        collector = SerebiiPokeprintCollector(session)
        for page_name, page_url in (await collector.fetch_collection_pages()).items():
            typer.echo(f"Downloading images for {page_name}...")
            image_urls = await collector.fetch_pokeprint_urls(page_url)
            imdl = create_image_downloader(path=output_dir / page_name, session=session)
            await imdl.download_images(image_urls)
    print(f"Finished in {round(perf_counter() - start_time, 2)} seconds!")


def autocomplete_pkmn_name(incomplete: str):
    # for pkmn in ALL_POKEMON:
    #     if pkmn.name.startswith(incomplete):
    #         yield pkmn.name
    pass


def search(
    id_or_name: str = typer.Argument(
        default=None,
        autocompletion=autocomplete_pkmn_name,
    ),
    language: str = typer.Option(default="en"),
):
    """Returns the pokémon National ID for a given pokémon name."""

    # client = PokeAPI()
    # species = client.get_pokemon_species(id_or_name)
    # print(f"#{species.id} - {species.get_proper_name(language)}")
    raise NotImplementedError


def generate(
    input: Path = typer.Argument(None, autocompletion=None),
    width: int = typer.Option(1920, "--width", "-w"),
    height: int = typer.Option(1080, "--height", "-h"),
    preset: str = typer.Option(
        None, "--preset", "-p", autocompletion=autocomplete_resolution_name
    ),
    scaling: float = typer.Option(1.0, "--scaling", "-s"),
):
    """
    Generates a wallpaper featuring the Pokémon with chosen ID,
    with the set width, height and scaling factor (default 1920x1080 at x1.0 scale).
    """
    # if preset:  # override width and height
    #     resolution = get_resolution_by_name(preset)
    #     width = resolution.width
    #     height = resolution.height

    # img_local_matches = settings.app.PATTERNS_DIRECTORY.glob(f"**/*_{pokemon}*.*")
    # if not (input_file := next(img_local_matches, None)):
    #     print("Image not found locally.")
    #     return

    # # generate output filename
    # i, r = divmod(scaling, 1)
    # i = int(i)
    # r = round(100 * r)
    # output_file = (
    #     settings.app.WALLPAPER_DIRECTORY
    #     / input_file.with_stem(f"{input_file.stem}_{width}x{height}_{i}p{r}").name
    # )

    # input_image = cv2.imread(str(input_file))
    # output_image = transform_image(input_image, width, height, scaling)
    # print(output_file)
    # output_file.parent.mkdir(exist_ok=True)
    # cv2.imwrite(str(output_file), output_image)
    raise NotImplementedError


def create_app(settings: AppSettings = settings, use_callback: bool = True):
    app = typer.Typer(
        no_args_is_help=True,
    )
    if use_callback:
        app.callback()(callback)
    app.command()(download)
    app.command()(search)
    app.command()(generate)
    return app
