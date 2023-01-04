import logging
from .base import Scrapper
from entities import Product
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Argos(Scrapper):
    """Scrapes Argos product details."""

    def __post_init__(self):
        logger.info("AmazonScrapper initialized.")
        self.soup = self.get_soup(self.url)


    def get_product_details(self)-> Product:
        """Returns the product details."""
        return Product(
            name=self.get_product_name(),
            price=self.get_price(),
            rating=self.get_rating(),
            color=self.get_color(),
            reviews=[]
        ).as_dict()
    
    def get_product_name(self):
        return self.soup.find("h1", {"data-test":"product-name-main"}).span.text.strip()

    def get_price(self):
        """Returns the price of the product."""
        try:
            print(self.soup.find("li", {"data-test":"product-price-primary"}).h2.text.strip())
            return self.soup.find("li", {"data-test":"product-price-primary"}).h2.text.strip()
        except IndexError:
            return None

    def get_rating(self):
        """Returns the product rating."""
        try:
            rating_text = self.soup.find("span", {"class":"Reviewsstyles__TrustmarkMessage-sc-6g3q7a-3 bkuzqy"}).text.strip()
            rating_text = rating_text.split("|")[0]
        except IndexError:
            return None