from unittest import TestCase
from .fixtures.iphone_11 import HTML as iphone_11_html
from .fixtures.iphone_11_reviews import HTML as iphone_11_reviews_html
import requests_mock
from bs4 import BeautifulSoup
from scrapper.ebay import Ebay

@requests_mock.Mocker()
class TestEbay(TestCase):

    def setUp(self) -> None:
        self.product_url = "https://www.ebay.co.uk/itm/284427971922?epid=15034218412&hash=item42393a6d52%3Ag%3A5N8AAOSwxGthKe4R&_trkparms=%2526rpp_cid%253D6310c387591fdbf501f265b1&var=585977478139"
        self.product_reviews_url = "https://www.ebay.co.uk/fdbk/feedback_profile/wjd-store?q=284427971922&_trksid=p2047675.l2560"
    
    def test_get_title(self, mocked_request):
        mocked_request.get(self.product_url, text=iphone_11_html)
        ebay = Ebay(self.product_url)
        self.assertEqual(ebay.get_title(), "Apple iPhone 11 - 64GB 128GB 256GB - Unlocked Smartphone Good Condition Warranty")

    def test_get_price(self, mocked_request):
        mocked_request.get(self.product_url, text=iphone_11_html)
        ebay = Ebay(self.product_url)
        self.assertEqual(ebay.get_price(), "269.95")

    def test_reviews_page(self, mocked_request):
        mocked_request.get(self.product_url, text=iphone_11_html)
        ebay = Ebay(self.product_url)
        self.assertEqual(ebay.get_reviews_page(), "https://www.ebay.co.uk/fdbk/feedback_profile/wjd-store?q=284427971922&_trksid=p2047675.l2560")

    def test_get_review_count(self, mocked_request):
        mocked_request.get(self.product_url, text=iphone_11_html)
        mocked_request.get(self.product_reviews_url, text=iphone_11_reviews_html)
        ebay = Ebay(self.product_url)
        soup = BeautifulSoup(iphone_11_reviews_html, "html.parser")
        self.assertEqual(ebay.get_review_count(soup), "41161")

    def test_get_review_page_count(self, mocked_request):
        mocked_request.get(self.product_url, text=iphone_11_html)
        mocked_request.get(self.product_reviews_url, text=iphone_11_reviews_html)
        ebay = Ebay(self.product_url)
        soup = BeautifulSoup(iphone_11_reviews_html, "html.parser")
        self.assertEqual(ebay.get_review_page_count(soup), "20")