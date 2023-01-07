"""Scrapper for https://www.currys.co.uk/"""

import logging
import requests
from dataclasses import dataclass, asdict
from entities import Product, Review

from scrapper.base import Scrapper

logger = logging.getLogger(__name__)

@dataclass
class Curry(Scrapper):

    REVIEW_URL = "https://widgets.reevoo.com/api/product_reviews?trkref=CYS&sku={}&locale=en-GB"
    review_json = None


    def __post_init__(self):
        logger.info("Curry initialized.")
        self.soup = self.get_soup(self.url)
        self.review_json = self.get_review_json()

    def get_product_sku(self):
            """Returns the product sku."""
            return self.soup.find("form").attrs["action"].split(".html")[0].split("/")[-1].split("-")[-1]
    
    def get_review_json(self):
        """Returns the review json."""
        sku = self.get_product_sku()
        url = self.REVIEW_URL.format(sku)
        response = requests.get(url)
        self.review_json = response.json()
        return self.review_json

    def get_product_details(self)-> Product:
        """Returns the product details."""
        return Product(
            name=self.get_title(),
            rating=self.get_average_rating(),
            reviews=self.get_all_reviews(),
            price=None
        ).serialize()


    def get_title(self):
        """Returns the product title."""
        title = self.review_json["header"]["title"].split("reviews")[0]
        return title

    def get_num_of_reviews(self):
        """Returns the number of reviews."""
        return self.review_json["body"]["pagination"]["total_entries_with_content"]

    def get_average_rating(self):
        """Returns the average rating."""
        return self.review_json["header"]["average_score"]

    def get_total_pages(self):
        """Returns the total number of pages."""
        return self.review_json["body"]["pagination"]["total_pages"]

    def _generate_review_url(self, sku, page):
        """Generates the review url for a given page."""
        url = f"{self.REVIEW_URL.format(sku)}&page={page}"
        return url

    def get_all_reviews(self):
        """Returns all the reviews."""
        sku = self.get_product_sku()
        total_pages = self.get_total_pages()
        reviews = []
        for page in range(1, total_pages + 1):
            url = self._generate_review_url(sku, page)
            response = requests.get(url)
            review_data = response.json()["body"]["reviews"]
            for review in review_data:
                text = review["text"]
                if text is not None:
                    reviews.append(self.extract_reviews(review))
        return reviews

    def extract_reviews(self, review):
        """Returns the reviews."""
        text = review["text"]
        return Review(
                rating=review["overall_score"],
                title="",
                content=str(text["good_points"]) + "." + str(text["bad_points"]),
                verified_purchase = review["translations"]["verified_purchase"] == "Confirmed purchase:",
                author=review["reviewer"]["name"],
            )