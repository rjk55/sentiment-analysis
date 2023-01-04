from django.test import TestCase

class TestGenericScrapper(TestCase):
    def test_right_scrapper_is_returned(self):
        from scrapper.generic import get_scrapper

        scrapper = get_scrapper("https://www.amazon.com/")

        self.assertEqual(scrapper.__class__.__name__, "AmazonScrapper")