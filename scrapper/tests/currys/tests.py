from unittest import TestCase 
from .fixtures.mac_book_air import HTML as mac_book_air_html
import requests_mock
from bs4 import BeautifulSoup
from scrapper.currys import Curry

import json
import os

def read_json_file(filename):
    with open(filename, "r") as f:
        return json.load(f)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JSON_DIR = os.path.join(BASE_DIR,  "currys", "fixtures","json_response")

class TestCurrys(TestCase):
    
    def setUp(self):
        self.maxDiff = None
        self.soup = BeautifulSoup(mac_book_air_html, "html.parser")
        self.url = "https://www.currys.co.uk/products/apple-macbook-air-13.6-2022-m2-256-gb-ssd-starlight-10239790.html"
        self.review_urls = {
            "page_1": "https://widgets.reevoo.com/api/product_reviews?trkref=CYS&sku=10239790&locale=en-GB&page=1",
            "page_2": "https://widgets.reevoo.com/api/product_reviews?trkref=CYS&sku=10239790&locale=en-GB&page=2",
            "page_3": "https://widgets.reevoo.com/api/product_reviews?trkref=CYS&sku=10239790&locale=en-GB&page=3",
            "page_4": "https://widgets.reevoo.com/api/product_reviews?trkref=CYS&sku=10239790&locale=en-GB&page=4",
            "page_5": "https://widgets.reevoo.com/api/product_reviews?trkref=CYS&sku=10239790&locale=en-GB&page=5",
        }

        self.scrapper = self.get_scrapper()

    @requests_mock.Mocker()
    def get_scrapper(self, mocked_request):
        """Returns scrapper object"""
        response_json = read_json_file(f"{JSON_DIR}/page_1.json")
        mocked_request.get(self.url, text=mac_book_air_html)
        mocked_request.get("https://widgets.reevoo.com/api/product_reviews?trkref=CYS&sku=10239790&locale=en-GB", json=response_json)
        return Curry(self.url)

    def test_html_is_parsed_to_soup(self):
        """Test that html is parsed to soup"""
        self.assertEqual(self.scrapper.soup, self.soup)
    
    def test_get_product_product_sku(self):
        """Test that product sku is returned"""
        self.assertEqual(self.scrapper.get_product_sku(), "10239790")
    
    @requests_mock.Mocker()
    def test_get_review_json(self, mocked_request):
        """Test that review json is returned"""
        response_json = read_json_file(f"{JSON_DIR}/page_1.json")
        mocked_request.get("https://widgets.reevoo.com/api/product_reviews?trkref=CYS&sku=10239790&locale=en-GB", json=response_json)

        self.assertEqual(self.scrapper.get_review_json(), response_json)

    @requests_mock.Mocker()
    def test_get_reviews(self, mocked_request):
        """Test that reviews are returned"""
        excepted_reviews = []
        for key, value in self.review_urls.items():
            json_response = read_json_file(f"{JSON_DIR}/{key}.json")
            mocked_request.get(value, json=json_response)
            reviews = json_response["body"]["reviews"]
            for review in reviews[0:2]:
                text = review["text"]
                if text is not None:
                    excepted_reviews.append(self.scrapper.extract_reviews(review))


