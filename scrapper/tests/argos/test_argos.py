from unittest import TestCase, mock
from .fixtures.iphone_13_5g_128gb import HTML as iphone_html
import requests_mock
from bs4 import BeautifulSoup
from scrapper.argos import Argos


@requests_mock.Mocker()
class TestArgos(TestCase):
    """Test Argos scrapper"""

    def setUp(self):
        self.iphone_url = "https://www.argos.co.uk/product/9520103?clickPR=plp:3:107" 
        self.soup = BeautifulSoup(iphone_html, "html.parser")
        self.product = {
            "name": "SIM Free iPhone 13 5G 128GB Mobile Phone - Pink",
            "price": "Â£749.00",
            "rating": 4.9,}
                                                                                                                                                                                                                                                                                                                                                                              

    def test_html_is_parsed_to_soup(self, mocked_request):
        """Test that html is parsed to soup"""

        # Mock request for iphone url
        mocked_request.get(self.iphone_url, text=iphone_html)
        scrapper = Argos(self.iphone_url)
        self.assertEqual(scrapper.soup, self.soup)

    def test_product_name(self, mocked_request):
        """Test product name"""
        
        # Mock request for iphone url
        mocked_request.get(self.iphone_url, text=iphone_html)

        scrapper = Argos(self.iphone_url)
        self.assertEqual(scrapper.get_product_name(), self.product["name"])

    def test_product_price(self, mocked_request):
        """Test product price"""
        
        # Mock request for iphone url
        mocked_request.get(self.iphone_url, text=iphone_html)

        scrapper = Argos(self.iphone_url)
        self.assertEqual(scrapper.get_price(), self.product["price"])

    def test_product_rating(self, mocked_request):
        """Test product rating"""
        
        # Mock request for iphone url
        mocked_request.get(self.iphone_url, text=iphone_html)

        scrapper = Argos(self.iphone_url)
        self.assertEqual(scrapper.get_rating(), None)