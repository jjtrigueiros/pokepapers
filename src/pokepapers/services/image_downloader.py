import asyncio
from pathlib import Path

import aiohttp
from pokepapers.services.image_fetcher import ImageFetcher
from pokepapers.services.image_saver import ImageSaver


class ImageDownloader:
    def __init__(self, fetcher: ImageFetcher, saver: ImageSaver):
        self.fetcher = fetcher
        self.saver = saver

    async def download_image(self, url: str) -> None:
        image = await self.fetcher.fetch_image(url)
        await self.saver.save_image(url.split('/')[-1], image)

    async def download_images(self, urls: list[str]):
        tasks = [self.download_image(url) for url in urls]
        await asyncio.gather(*tasks)


def create_image_downloader(path: Path, session: aiohttp.ClientSession):
    return ImageDownloader(ImageFetcher(session), ImageSaver(path))
