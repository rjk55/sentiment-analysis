from scrapper.base import BaseScrapper
import unittest
import requests_mock


class TestBaseScrapper(unittest.TestCase):
    """Test BaseScrapper class"""

    @classmethod
    def setUp(cls) -> None:
        cls.url = "https://www.amazon.com"
        cls.response_text = """<html>
            <title>Amazon</title>
            <body><h1>Amazon</h1></body></html>"""

    def test_soup_cannot_be_initialized(self):
        """Test soup is not initialized"""
        with self.assertRaises(TypeError) as ctx:
            BaseScrapper(url=self.url, soup="soup")

        excepted_msg = "__init__() got an unexpected keyword argument 'soup'"
        self.assertEqual(ctx.exception.args[0], excepted_msg)

    def test_default_header(self):
        """Test default header"""
        base_scrapper = BaseScrapper(url=self.url)
        self.assertEqual(
            base_scrapper.header,
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            },
        )

    def test_custom_header(self):
        """Test custom header"""
        header = {
            "User-Agent": "Custom User Agent",
        }
        base_scrapper = BaseScrapper(url=self.url, header=header)
        self.assertEqual(base_scrapper.header, header)

    def test_get_base_url(self):
        """Test get_base_url"""
        base_scrapper = BaseScrapper(url=self.url)
        self.assertEqual(base_scrapper.get_base_url, "www.amazon.com")

    @requests_mock.Mocker()
    def test_get_html(self, mocked_request):
        """Test get_html"""

        mocked_request.get(self.url, text=self.response_text)
        base_scrapper = BaseScrapper(url=self.url)

        response = base_scrapper.get_html(url=self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, self.response_text)

    @requests_mock.Mocker()
    def test_get_soup(self, mocked_request):
        """Test response is parsed to soup"""

        mocked_request.get(self.url, text=self.response_text)
        base_scrapper = BaseScrapper(url=self.url)
        soup = base_scrapper.get_soup(url=self.url)
        self.assertEqual(soup.title.text, "Amazon")
