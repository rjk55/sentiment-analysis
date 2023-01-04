from .base import Scrapper
import logging
from entities import Product

from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Ebay(Scrapper):
    """Scrapper for Ebay."""

    def __post_init__(self):
        logger.info("EbayScrapper initialized.")
        self.soup = self.get_soup(self.url)

    def get_product_details(self):
        return Product(
            name=self.get_title(),
            price=self.get_price(),
            rating=self.get_rating(),
            reviews=self.get_all_reviews(),
        )

    def get_title(self):
        h1 = self.soup.find('h1', attrs={'class': 'x-item-title__mainTitle'})
        return h1.span.text.strip()

    def get_price(self):
        price = self.soup.find('span', attrs={'itemprop': 'price'})
        return price["content"]
    
    def get_rating(self):
        rating = self.soup.find('span', attrs={'class': 'clipped'})
        return rating.text

    def get_description(self):
        description = self.soup.find('div', attrs={'class': 'itemAttr'})
        return description.text

    def get_reviews_page(self):
        reviews = self.soup.find('a', attrs={'class': 'btn byrfdbk_modal_lg_btn'})
        return reviews["href"]

    def get_review_count(self, soup):
        count = soup.find('p', attrs={'data-test-id':"user-score"}).text
        return count

    def get_review_page_count(self, soup):
        count = soup.find('span', attrs={'data-test-id':"pagination-label"}).text.split(" ")[-1]
        return count