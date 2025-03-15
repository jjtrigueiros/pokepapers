import asyncio
from pathlib import Path

import aiohttp
from loguru import logger

from pokepapers.services.image_fetcher import ImageFetcher
from pokepapers.services.image_saver import ImageSaver


class ImageDownloader:
    def __init__(self, fetcher: ImageFetcher, saver: ImageSaver):
        self.fetcher = fetcher
        self.saver = saver

    async def download_image(self, url: str) -> None:
        name = url.split("/")[-1]
        if self.saver.exists(name):
            logger.warning(f"File exists, skipping: {name}")
            return
        image = await self.fetcher.fetch_image(url)
        await self.saver.save_image(name, image)

    async def download_images(self, urls: list[str]):
        tasks = [self.download_image(url) for url in urls]
        await asyncio.gather(*tasks)


def create_image_downloader(path: Path, session: aiohttp.ClientSession):
    return ImageDownloader(ImageFetcher(session), ImageSaver(path))
