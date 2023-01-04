from unittest import TestCase, mock
from scrapper.base import Scrapper
class TestScrapper(TestCase):
    """Test base scrapper"""

    def setUp(self):
        self.amazon_iphone_url = "https://www.amazon.co.uk/Apple-iPhone-13-128GB-Starlight/dp/B09G9FB7LV/ref=cm_cr_arp_d_product_top?ie=UTF8"


    def test_base_url_is_returned_correctly(self):
        """Test base url is returned correctly"""
        self.assertEqual(Scrapper.get_base_url("https://www.amazon.com"), "www.amazon.com")
        self.assertEqual(Scrapper.get_base_url("https://www.amazon.co.uk"), "www.amazon.co.uk")
        self.assertEqual(Scrapper.get_base_url("https://www.flipkart.com"), "www.flipkart.com")
        self.assertEqual(Scrapper.get_base_url("https://www.argos.co.uk"), "www.argos.co.uk")

    def test_scrapper_class_is_returned_correctly(self):
        """Test scrapper class is returned correctly"""

        from scrapper.amazon import AmazonScrapper

        self.assertEqual(Scrapper.get_scrapper("https://www.amazon.co.uk/Apple-iPhone-13-128GB-Starlight/dp/B09G9FB7LV/ref=cm_cr_arp_d_product_top?ie=UTF8"), AmazonScrapper)

    
    def test_get_scrapper_returns_none_if_no_scrapper_is_found(self):
        """Test get scrapper returns none if no scrapper is found"""
        self.assertIsNone(Scrapper.get_scrapper("https://www.google.com"))

  
    def test_scraped_data_is_returned_for_valid_url(self,):
        """Test data is returned for valid url"""
    
        with mock.patch.object(
                Scrapper, "get_product_details", return_value={"title": "test"}
            ):
                self.assertEqual(
                    Scrapper.get_product_details(self.amazon_iphone_url),
                    {"title": "test"},
                )