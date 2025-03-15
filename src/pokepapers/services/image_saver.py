from pathlib import Path
import aiofiles
from loguru import logger


class ImageSaver:
    def __init__(self, path: Path):
        self.path = path

    async def save_image(self, filename: str, content: bytes):
        self.path.mkdir(parents=True, exist_ok=True)
        file_path = self.path / filename
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(content)
            logger.info(f"Saved: {file_path}")

    def exists(self, filename: str) -> bool:
        return (self.path / filename).is_file()
