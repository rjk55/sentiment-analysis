import dataclasses, typing
import logging
import requests
import bs4

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class BaseScrapper:
    """Base class for scrapping data from web pages"""

    url: str
    soup: bs4.BeautifulSoup = dataclasses.field(init=False)
    header: typing.Dict[str, str] = dataclasses.field(
        default_factory=lambda: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
    )

    def get_html(self, url: str):
        """Get html from url"""
        logger.info(f"Getting html from {url}")
        return requests.get(url, headers=self.header)

    def get_soup(self, url: str):
        """Parse html to soup"""
        logger.info(f"Parsing html to soup from {url}")
        return bs4.BeautifulSoup(self.get_html(url).content, "html.parser")

    @property
    def get_base_url(self) -> str:
        """Returns base url"""
        return self.url.split("https://")[-1].split("/")[0]
