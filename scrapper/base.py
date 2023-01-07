import dataclasses, typing
import logging
import requests
import bs4
from .constants import MarketPlace


logger = logging.getLogger(__name__)

def get_scrapper(url: str):
    """Returns scrapper based on url"""
    from .amazon import AmazonScrapper
    from .argos import Argos
    from .flipkart import Flipkart
    from .currys import Curry

    # Extract the market place from the url e.g. amazon, ebay, flipkart etc
    market_place = Scrapper.get_base_url(url).split(".")[1]

    scrappers = {
        MarketPlace.AMAZON: AmazonScrapper,
        MarketPlace.ARGOS: Argos,
        MarketPlace.FLIPKART: Flipkart,
        MarketPlace.CURRYS: Curry,
    }

    return scrappers.get(market_place, None)

@dataclasses.dataclass
class Scrapper:
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
        return bs4.BeautifulSoup(self.get_html(url).content, "html.parser",)

    @classmethod
    def get_base_url(self,url:str) -> str:
        """Returns base url"""
        # Split the url by / and take the first 3 elements and join them with :// to get the base url
        return "".join(url.split("/")[0:3]).replace(":", "://")

    @property
    def base_url(self) -> str:
        """Returns base url"""
        return self.get_base_url(self.url)




