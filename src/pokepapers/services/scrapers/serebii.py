import aiohttp
from bs4 import BeautifulSoup
from yarl import URL


class SerebiiPokeprintCollector:
    base_url = URL("https://www.serebii.net/")

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session

    async def fetch_artist_pages(self) -> dict[str, str]:
        async with self.session.get(self.base_url / "pokemonshirts") as response:
            response.raise_for_status()
            content = await response.text()
        soup = BeautifulSoup(content, "html.parser")
        select_options = soup.find(name="select").find_all("option")
        return {
            option.text: self.base_url / val[1:]
            for option in select_options
            if "/" in (val := option.get("value"))
        }

    async def fetch_collection_pages(self) -> dict[str, str]:
        async with self.session.get(self.base_url / "pokemonshirts") as response:
            response.raise_for_status()
            content = await response.text(encoding="latin1")
        soup = BeautifulSoup(content, "html.parser")
        dextables = soup.find(id="content").find_all(name="table", class_="dextable")
        pages: dict[str, str] = {}
        for dextable in dextables:
            links = dextable.find_all("a")
            pages |= {link.text: self.base_url / link.get("href")[1:] for link in links}
        return pages

    async def fetch_pokeprint_urls(self, page: str) -> list[str]:
        async with self.session.get(page) as response:
            response.raise_for_status()
            content = await response.text(encoding="latin1")
        soup = BeautifulSoup(content, "html.parser")
        urls = self.extract_print_urls_from_dextables(soup)
        print_urls = [
            "https://www.serebii.net/pokemonshirts/" + url.replace("/th", "")
            for url in urls
            if "/th/" in url
        ]
        return print_urls

    @staticmethod
    def extract_print_urls_from_dextables(page: BeautifulSoup) -> set[str]:
        relpaths = set()
        dextables = page.find(id="content").find_all(name="table", class_="dextable")
        for dextable in dextables:
            rows = dextable.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                for cell in cells:
                    img = cell.find("img")
                    if not img:
                        continue
                    relpath = img.get("src")
                    relpaths.add(relpath)
        return relpaths
