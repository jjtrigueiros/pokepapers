from pathlib import Path
import aiofiles
from loguru import logger

class ImageSaver:
    def __init__(self, path: Path):
        self.path = path

    async def save_image(self, filename: str, content: bytes):
        async with aiofiles.open(self.path / filename, "wb") as file:
            await file.write(content)
            logger.info(f"Saved: {filename}")
