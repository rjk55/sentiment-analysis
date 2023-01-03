from .base import Scrapper
import logging
from entities import Product, Review

from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Flipkart(Scrapper):
    def __post_init__(self):
        logger.info("AmazonScrapper initialized.")
        self.soup = self.get_soup(self.url)

    def get_product_details(self):

        return Product(
            name=self.get_title(),
            price=self.get_price(),
            rating=self.get_rating(),
            reviews=self.get_all_reviews(),
        ).serialize()

    def get_title(self):
        title = self.soup.find('span', attrs={'class': 'B_NuCI'}).text.strip()
        return title

    def get_price(self):
        price = self.soup.find('div', attrs={'class': '_30jeq3 _16Jk6d'})
        return price.text.split("¹")[-1]

    def get_rating(self):
        rating = self.soup.find('div', attrs={'class': '_2d4LTz'})
        return rating.text

    def get_description(self):
        description = self.soup.find('div', attrs={'class': '_1mXcCf RmoJUZ'})
        return description.text

    def get_specifications(self):
        specifications = self.soup.find('div', attrs={'class': '_1mXcCf RmoJUZ'})
        return specifications.text


    def get_seller(self):
        seller = self.soup.find('div', attrs={'class': '_1mXcCf RmoJUZ'})
        return seller.text

    def get_all_reviews_page_url(self):
        """Returns the URL of the page containing all the reviews."""
        item_id = self.soup.find("link", {"rel": "canonical"})["href"].split("/p/")[-1]
        product_id = self.soup.find("li", {"class": "_38I6QT"}).find("a")["href"].split("pid=")[1].split("&amp")[0]
        return self.url.split("/p/")[0] + f"/product-reviews/{item_id}?pid={product_id}"

    def get_all_reviews(self):
        """Returns all the reviews."""
        all_reviews_page_url = self.get_all_reviews_page_url()
        # print("all_reviews_page_url", all_reviews_page_url)
        soup = self.get_soup(all_reviews_page_url)
        number_of_pages = self.get_number_of_pages(soup)

        all_page_urls = []

        navigation_div = soup.find("nav", {"class": "yFHi8N"})

        link = navigation_div.find_all("a", )[0]["href"].split("page=")[0]

        for i in range(1, number_of_pages):
            url = f"{self.base_url}{link}page={i}"
            all_page_urls.append(url)


        all_reviews = []

        for page_url in all_page_urls:
            # print(page_url)
            soup = self.get_soup(page_url)
            try:
                all_reviews.append(self.extract_reviews(soup))
            except Exception as e:
                logger.error("Error while extracting reviews: %s", e)
                continue

        
        return all_reviews

    def extract_reviews(self, soup)->Review:
        """Extracts reviews from the soup object."""
        wrapper_div = soup.find("div", {"class": "col _2wzgFH K0kLPL"})
        rating = wrapper_div.find("div", {"class": "_3LWZlK _1BLPMq"}).text
        review_heading = wrapper_div.find("p", {"class": "_2-N8zT"}).text
        review_text = wrapper_div.find("div", {"class": "t-ZTKy"}).div.div.text
        author = wrapper_div.find("p", {"class": "_2sc7ZR _2V5EHH"}).text
        certified_buyer = wrapper_div.find("p", {"class": "_2mcZGG"})
        verified_purchase = certified_buyer and certified_buyer.span.text == "Certified Buyer"
        return Review(rating=rating, title=review_heading, content=review_text, 
            author=author,verified_purchase=verified_purchase
        )

    def get_number_of_pages(self, soup):
        """Returns the number of pages containing reviews."""
        page_count = soup.find("div", {"class": "_2MImiq _1Qnn1K"}).span.text.split(" ")[-1]
        # remove ',' from the page count
        page_count = page_count.replace(",", "")
        return int(page_count)

