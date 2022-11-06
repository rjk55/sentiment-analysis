from unittest import TestCase, mock
import requests_mock
from scrapper.amazon import AmazonScrapper
from .fixtures import iphone, book
import bs4


class TestAmazonScrapper(TestCase):
    """Test AmazonScrapper class"""

    def setUp(self) -> None:
        super().setUp()
        self.product_iphone_url = "https://www.amazon.co.uk/Apple-iPhone-13-128GB-Starlight/dp/B09G9FB7LV/ref=cm_cr_arp_d_product_top?ie=UTF8"
        self.product_book_url = "https://www.amazon.co.uk/dp/0008350752/ref=sspa_dk_detail_2?psc=1&pd_rd_i=0008350752&pd_rd_w=qFMsT&content-id=amzn1.sym.940bda19-f0f4-4883-b452-52aff480df74&pf_rd_p=940bda19-f0f4-4883-b452-52aff480df74&pf_rd_r=9QTA3MPRMTEKEXAYFJQ0&pd_rd_wg=sqBo7&pd_rd_r=f5a73e36-b300-4b0a-b624-4c6bfb00cbee&s=books&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy"
        self.iphone_soup = bs4.BeautifulSoup(iphone.HTML, "html.parser")
        self.book_soup = bs4.BeautifulSoup(book.HTML, "html.parser")

        self.iphone = {
            "title": "Apple iPhone 13 (128GB) - Starlight",
            "price": None,
            "rating": {
                "5 star": "86%",
                "4 star": "8%",
                "3 star": "2%",
                "2 star": "1%",
                "1 star": "4%",
            },
            "size": "128GB",
            "color": "Starlight",
            "number_of_global_ratings": "2,263 ratings",
            "all_reviews_url": "https://www.amazon.co.uk/Apple-iPhone-13-128GB-Starlight/product-reviews/B09G9FB7LV/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
        }

        self.book = {
            "title": "Black Holes: The Key to Understanding the Universe",
            "price": "£16.09",
            "rating": {
                "5 star": "59%",
                "4 star": "25%",
                "3 star": "8%",
                "2 star\n        \n\n          0% (0%)": "0%",
                "1 star": "8%",
            },
            "size": None,
            "color": None,
            "number_of_global_ratings": "16 ratings",
            "all_reviews_url": "https://www.amazon.co.uk/Black-Holes-Key-Understanding-Universe/product-reviews/0008350752/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
        }

        self.test_products = [
            {
                "url": self.product_iphone_url,
                "soup": self.iphone_soup,
                **self.iphone,
            },
            {
                "url": self.product_book_url,
                "soup": self.book_soup,
                **self.book,
            },
        ]

    @requests_mock.Mocker()
    def test_post_init_triggers_get_soup(self, mocked_request):
        """Test that post init triggers get soup"""
        mocked_request.get(self.product_iphone_url, text=iphone.HTML)
        with self.assertLogs(level="INFO") as log:
            AmazonScrapper(self.product_iphone_url)

        self.assertIn(
            f"Getting html from {self.product_iphone_url}", "".join(log.output)
        )
        self.assertIn(
            f"Parsing html to soup from {self.product_iphone_url}", "".join(log.output)
        )

    @requests_mock.Mocker()
    def test_html_is_parsed_to_soup(self, mocked_request):
        """Test that html is parsed to soup"""

        # Mock request for iphone url
        mocked_request.get(self.product_iphone_url, text=iphone.HTML)
        scrapper = AmazonScrapper(self.product_iphone_url)
        self.assertEqual(scrapper.soup, self.iphone_soup)

        # Mock request for book url
        mocked_request.get(self.product_book_url, text=book.HTML)
        scrapper = AmazonScrapper(self.product_book_url)
        self.assertEqual(scrapper.soup, self.book_soup)

    def test_product_title(self):
        """Test product title"""

        for product in self.test_products:
            with mock.patch.object(
                AmazonScrapper, "get_soup", return_value=product["soup"]
            ):
                scrapper = AmazonScrapper(product["url"])
                self.assertEqual(scrapper.get_product_title(), product["title"])

    def test_product_price(self):
        """Test product price"""

        for product in self.test_products:
            with mock.patch.object(
                AmazonScrapper, "get_soup", return_value=product["soup"]
            ):
                scrapper = AmazonScrapper(product["url"])
                self.assertEqual(scrapper.get_price(), product["price"])

    def test_product_rating(self):
        """Test product rating"""

        for product in self.test_products:
            with mock.patch.object(
                AmazonScrapper, "get_soup", return_value=product["soup"]
            ):
                scrapper = AmazonScrapper(product["url"])
                self.assertEqual(scrapper.get_rating(), product["rating"])

    def test_get_size(self):
        """Test size and color"""

        for product in self.test_products:
            with mock.patch.object(
                AmazonScrapper, "get_soup", return_value=product["soup"]
            ):
                scrapper = AmazonScrapper(product["url"])
                self.assertEqual(scrapper.get_size(), product["size"])

    def test_get_color(self):
        """Test size and color"""

        for product in self.test_products:
            with mock.patch.object(
                AmazonScrapper, "get_soup", return_value=product["soup"]
            ):
                scrapper = AmazonScrapper(product["url"])
                self.assertEqual(scrapper.get_color(), product["color"])

    def test_global_rating(self):
        """Test global rating"""

        for product in self.test_products:
            with mock.patch.object(
                AmazonScrapper, "get_soup", return_value=product["soup"]
            ):
                scrapper = AmazonScrapper(product["url"])
                self.assertEqual(
                    scrapper.number_of_global_ratings(),
                    product["number_of_global_ratings"],
                )

    def test_all_reviews_url(self):
        """Test all reviews url"""

        for product in self.test_products:
            with mock.patch.object(
                AmazonScrapper, "get_soup", return_value=product["soup"]
            ):
                scrapper = AmazonScrapper(product["url"])
                self.assertEqual(
                    scrapper.get_all_reviews_url(),
                    product["all_reviews_url"],
                )

    def test_product_details(self):
        """Test product details"""
        ...
