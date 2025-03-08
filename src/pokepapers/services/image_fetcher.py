import typing as t
from loguru import logger
import aiohttp
import asyncio


class ImageFetcher:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session

    async def fetch_image(self, url: str):
        async with self.session.get(url) as response:
            if response.status == 200:
                logger.info(f"Fetched: {url}")
                return await response.read()
            else:
                response.raise_for_status()

    async def fetch_images(self, urls: t.Iterable[str]):
        tasks = [self.fetch_image(url) for url in urls]
        return await asyncio.gather(*tasks)

    async def close(self):
        await self.session.close()
