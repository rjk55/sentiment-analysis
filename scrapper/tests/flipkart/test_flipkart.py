from unittest import TestCase, mock
from .fixtures.sony_camera import HTML as sony_html
from .fixtures.sony_first_review_page import HTML as sony_first_review_page_html
import requests_mock
from bs4 import BeautifulSoup
from scrapper.flipkart import Flipkart

@requests_mock.Mocker()
class TestFlipkart(TestCase):
    """
    Test Flipkart scrapper
    """

    def setUp(self):
        self.sony_camera_url = "https://www.flipkart.com/sony-alpha-full-frame-ilce-7m2k-bq-in5-mirrorless-camera-body-28-70-mm-lens/p/itm92df94dc68fff?pid=DLLF6QZPNKTQMS8J&lid=LSTDLLF6QZPNKTQMS8JPI2J50&marketplace=FLIPKART&store=jek%2Fp31%2Ftrv&srno=b_1_1&otracker=hp_omu_Best%2Bof%2BElectronics_2_3.dealCard.OMU_Q5LU1U8PHMK6_3&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Best%2Bof%2BElectronics_NA_dealCard_cc_2_NA_view-all_3&fm=neo%2Fmerchandising&iid=d7d8dd53-55c6-44d5-b13b-8a1a055a24bb.DLLF6QZPNKTQMS8J.SEARCH&ppt=hp&ppn=homepage&ssid=h4z4i7t3a80000001672555573919"
        self.soup = BeautifulSoup(sony_html, "html.parser")
        self.sony_camera_product = {
            "name":"SONY Alpha Full Frame ILCE-7M2K/BQ IN5 Mirrorless Camera Body with 28 - 70 mm Lens  (Black)",
            "price":"₹82,999",
            "rating":"4.5",
            "see_all_reviews":"https://www.flipkart.com/sony-alpha-full-frame-ilce-7m2k-bq-in5-mirrorless-camera-body-28-70-mm-lens/product-reviews/itm92df94dc68fff?pid=DLLF6QZPNKTQMS8J",
            "reviews_page_url":"https://www.flipkart.com/reviews/3f6044dd-50a5-400c-ad5b-f3cedddb537d"
        }   

    def test_html_is_parsed_to_soup(self, mocked_request):
        """Test that html is parsed to soup"""

        # Mock request for sony camera url
        mocked_request.get(self.sony_camera_url, text=sony_html)
        scrapper = Flipkart(self.sony_camera_url)
        self.assertEqual(scrapper.soup, self.soup)

    def test_product_name(self, mocked_request):
        """Test product name"""
        
        # Mock request for sony camera url
        mocked_request.get(self.sony_camera_url, text=sony_html)

        scrapper = Flipkart(self.sony_camera_url)
        self.assertEqual(scrapper.get_title(), self.sony_camera_product["name"])

    def test_product_price(self, mocked_request):
        """Test product price"""
        
        # Mock request for sony camera url
        mocked_request.get(self.sony_camera_url, text=sony_html)

        scrapper = Flipkart(self.sony_camera_url)
        self.assertEqual(scrapper.get_price(), self.sony_camera_product["price"])

    def test_product_rating(self, mocked_request):
        """Test product rating"""
        
        # Mock request for sony camera url
        mocked_request.get(self.sony_camera_url, text=sony_html)

        scrapper = Flipkart(self.sony_camera_url)
        self.assertEqual(scrapper.get_rating(), self.sony_camera_product["rating"])

    def test_get_all_reviews_page_url(self, mocked_request):
        """Test get all reviews page url"""
        
        # Mock request for sony camera url
        mocked_request.get(self.sony_camera_url, text=sony_html)
        mocked_request.get(self.sony_camera_product["reviews_page_url"], text="""
        <div class="col-9-12"><div class="_3t4Eas">Customer Review</div>
        <div class="_2zlSTn"><div class="sHtZEY row">
        <div class="_3LWZlK _2LrrLv">5<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMyIgaGVpZ2h0PSIxMiI+PHBhdGggZmlsbD0iI0ZGRiIgZD0iTTYuNSA5LjQzOWwtMy42NzQgMi4yMy45NC00LjI2LTMuMjEtMi44ODMgNC4yNTQtLjQwNEw2LjUuMTEybDEuNjkgNC4wMSA0LjI1NC40MDQtMy4yMSAyLjg4Mi45NCA0LjI2eiIvPjwvc3ZnPg==" class="_1wB99o"></div><div class="_2Xz2nt">Terrific purchase</div></div>
        <div class="wdVh9J">I was looking for a full frame budget camera.. finally shortlisted A7 2 and eos rp.. <br><br>A7 2<br>Good for stills with excellent dynamic range but auto focus is bit slow.<br><br>Eos rp<br>Good autofocus capabilities compared to A7 2 but dynamic range is not upto the mark.<br><br>Since my focus is completely on stills , decided to get A7 2..<br><br>If you are looking for a still camera go for A7 2. It won't disappoint you ( nikon d810 was my last camera).. for videography don't get this body..<br><br>Positives<br>1. Excellent picture quality<br>2. Easy to set manual white balance( no need to set it in post processing)<br>3. Manual Focus (zoom feature ) is very quick and can get sharp images quickly.<br>4. In body image stabilization.<br>5. WiFi feature.<br>6. Easy to carry (small size).. and nobody notice you in a crowd.<br>7.price.<br><br>Negative<br>1. Autofocus <br>2. Lenses are bit costly compared to canon/ nikon<br><br>If you are primarily focusing on stills(not wildlife). This is a best catch at this price point.If needed a body for videography not recommending this camera.</div><div class="_2nMSwX _2JdVGm"><div class="_21YjFX _1-izrn" style="background-image: url(&quot;https://rukminim1.flixcart.com/blobio/124/124/imr-202208/blobio-imr-202208_096851c9ac21465e9054462df29cd1a3.jpg?q=90&quot;), url(&quot;data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjIiIGhlaWdodD0iMTgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgZmlsbD0iIzlEOUQ5RCIgZmlsbC1ydWxlPSJub256ZXJvIj48cGF0aCBkPSJNMjAgMEgyQzEgMCAwIDEgMCAydjE0YzAgMS4xLjkgMiAyIDJoMThjMSAwIDItMSAyLTJWMmMwLTEtMS0yLTItMnptMCAxNS45MmMtLjAyLjAzLS4wNi4wNi0uMDguMDhIMlYyLjA4TDIuMDggMmgxNy44M2MuMDMuMDIuMDYuMDYuMDguMDh2MTMuODRIMjB6Ii8+PHBhdGggZD0iTTEwIDEyLjUxTDcuNSA5LjUgNCAxNGgxNGwtNC41LTZ6Ii8+PC9nPjwvc3ZnPg==&quot;); width: 62px; height: 62px;"></div></div><div class="_3G7LJF row"><div class="_1sk9Vt">Shamnad Razak</div><div class="_2a2aeg"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgdmlld0JveD0iMCAwIDEyIDEyIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPGNpcmNsZSBjeD0iNiIgY3k9IjYiIHI9IjYiIGZpbGw9IiM4Nzg3ODciLz4KICAgICAgICA8cGF0aCBzdHJva2U9IiNGRkYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS13aWR0aD0iMS41IiBkPSJNMy4wNzcgNi4wNjRMNS4wMjMgOC4wMWwzLjk4NS0zLjk4NiIvPgogICAgPC9nPgo8L3N2Zz4K" class="_3KmO3E"><div class="_1sk9Vt">Certified Buyer</div></div><div class="_1sk9Vt">17 Aug, 2022</div><div class="row Ljko-4"><div><div class="_1LmwT9"><svg width="20" height="15" xmlns="http://www.w3.org/2000/svg" class="skCrcq"><path fill="#fff" class="_1LIt4y" d="M9.58.006c-.41.043-.794.32-1.01.728-.277.557-2.334 4.693-2.74 5.1-.41.407-.944.6-1.544.6v8.572h7.5c.45 0 .835-.28 1.007-.665 0 0 2.207-6.234 2.207-6.834 0-.6-.47-1.072-1.07-1.072h-3.216c-.6 0-1.07-.535-1.07-1.07 0-.537.835-3.387 1.006-3.944.17-.557-.107-1.157-.664-1.35-.15-.043-.257-.086-.407-.064zM0 6.434v8.572h2.143V6.434H0z" fill-rule="evenodd"></path></svg><span class="_3c3Px5">0</span></div><div class="_1LmwT9 pkR4jH"><svg width="20" height="15" xmlns="http://www.w3.org/2000/svg" class="skCrcq pkR4jH"><path fill="#fff" class="_1LIt4y" d="M9.58.006c-.41.043-.794.32-1.01.728-.277.557-2.334 4.693-2.74 5.1-.41.407-.944.6-1.544.6v8.572h7.5c.45 0 .835-.28 1.007-.665 0 0 2.207-6.234 2.207-6.834 0-.6-.47-1.072-1.07-1.072h-3.216c-.6 0-1.07-.535-1.07-1.07 0-.537.835-3.387 1.006-3.944.17-.557-.107-1.157-.664-1.35-.15-.043-.257-.086-.407-.064zM0 6.434v8.572h2.143V6.434H0z" fill-rule="evenodd"></path></svg><span class="_3c3Px5">0</span></div></div></div></div></div><a href="/sony-alpha-full-frame-ilce-7m2k-bq-in5-mirrorless-camera-body-28-70-mm-lens/product-reviews/itm92df94dc68fff?pid=DLLF6QZPNKTQMS8J"><div class="_2yVg4P">View all reviews of the product</div></a></div>""")

        scrapper = Flipkart(self.sony_camera_url)
        self.assertEqual(scrapper.get_all_reviews_page_url(), self.sony_camera_product["see_all_reviews"])

    def test_extract_reviews(self, mocked_request):
        """Tests the extract_reviews method."""
        mocked_request.get(self.sony_camera_url, text=sony_html)
        scrapper = Flipkart(self.sony_camera_url)
        soup = BeautifulSoup(sony_first_review_page_html, "html.parser")
        reviews = scrapper.extract_reviews(soup)

        excepted_reviews = ('5', 'Terrific purchase', "I was looking for a full frame budget camera.. finally shortlisted A7 2 and eos rp.. A7 2Good for stills with excellent dynamic range but auto focus is bit slow.Eos rpGood autofocus capabilities compared to A7 2 but dynamic range is not upto the mark.Since my focus is completely on stills , decided to get A7 2..If you are looking for a still camera go for A7 2. It won't disappoint you ( nikon d810 was my last camera).. for videography don't get this body..Positives1. Excellent pi...")
        self.assertEqual(reviews, excepted_reviews)
        
    
    def test_get_number_of_pages(self, mocked_request):
        """Tests the get_number_of_pages method."""
        mocked_request.get(self.sony_camera_url, text=sony_html)
        scrapper = Flipkart(self.sony_camera_url)
        soup = BeautifulSoup(sony_first_review_page_html, "html.parser")
        number_of_pages = scrapper.get_number_of_pages(soup)
        self.assertEqual(number_of_pages, 11)

    # def test_get_all_reviews(self, mocked_request):
    #     """Tests the get_reviews method."""
    #     mocked_request.get(self.sony_camera_url, text=sony_html)
    #     mocked_request.get(self.sony_camera_product["reviews_page_url"], text="""
    #     <div class="col-9-12"><div class="_3t4Eas">Customer Review</div>
    #     <div class="_2zlSTn"><div class="sHtZEY row">
    #     <div class="_3LWZlK _2LrrLv">5<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMyIgaGVpZ2h0PSIxMiI+PHBhdGggZmlsbD0iI0ZGRiIgZD0iTTYuNSA5LjQzOWwtMy42NzQgMi4yMy45NC00LjI2LTMuMjEtMi44ODMgNC4yNTQtLjQwNEw2LjUuMTEybDEuNjkgNC4wMSA0LjI1NC40MDQtMy4yMSAyLjg4Mi45NCA0LjI2eiIvPjwvc3ZnPg==" class="_1wB99o"></div><div class="_2Xz2nt">Terrific purchase</div></div>
    #     <div class="wdVh9J">I was looking for a full frame budget camera.. finally shortlisted A7 2 and eos rp.. <br><br>A7 2<br>Good for stills with excellent dynamic range but auto focus is bit slow.<br><br>Eos rp<br>Good autofocus capabilities compared to A7 2 but dynamic range is not upto the mark.<br><br>Since my focus is completely on stills , decided to get A7 2..<br><br>If you are looking for a still camera go for A7 2. It won't disappoint you ( nikon d810 was my last camera).. for videography don't get this body..<br><br>Positives<br>1. Excellent picture quality<br>2. Easy to set manual white balance( no need to set it in post processing)<br>3. Manual Focus (zoom feature ) is very quick and can get sharp images quickly.<br>4. In body image stabilization.<br>5. WiFi feature.<br>6. Easy to carry (small size).. and nobody notice you in a crowd.<br>7.price.<br><br>Negative<br>1. Autofocus <br>2. Lenses are bit costly compared to canon/ nikon<br><br>If you are primarily focusing on stills(not wildlife). This is a best catch at this price point.If needed a body for videography not recommending this camera.</div><div class="_2nMSwX _2JdVGm"><div class="_21YjFX _1-izrn" style="background-image: url(&quot;https://rukminim1.flixcart.com/blobio/124/124/imr-202208/blobio-imr-202208_096851c9ac21465e9054462df29cd1a3.jpg?q=90&quot;), url(&quot;data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjIiIGhlaWdodD0iMTgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgZmlsbD0iIzlEOUQ5RCIgZmlsbC1ydWxlPSJub256ZXJvIj48cGF0aCBkPSJNMjAgMEgyQzEgMCAwIDEgMCAydjE0YzAgMS4xLjkgMiAyIDJoMThjMSAwIDItMSAyLTJWMmMwLTEtMS0yLTItMnptMCAxNS45MmMtLjAyLjAzLS4wNi4wNi0uMDguMDhIMlYyLjA4TDIuMDggMmgxNy44M2MuMDMuMDIuMDYuMDYuMDguMDh2MTMuODRIMjB6Ii8+PHBhdGggZD0iTTEwIDEyLjUxTDcuNSA5LjUgNCAxNGgxNGwtNC41LTZ6Ii8+PC9nPjwvc3ZnPg==&quot;); width: 62px; height: 62px;"></div></div><div class="_3G7LJF row"><div class="_1sk9Vt">Shamnad Razak</div><div class="_2a2aeg"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgdmlld0JveD0iMCAwIDEyIDEyIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPGNpcmNsZSBjeD0iNiIgY3k9IjYiIHI9IjYiIGZpbGw9IiM4Nzg3ODciLz4KICAgICAgICA8cGF0aCBzdHJva2U9IiNGRkYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS13aWR0aD0iMS41IiBkPSJNMy4wNzcgNi4wNjRMNS4wMjMgOC4wMWwzLjk4NS0zLjk4NiIvPgogICAgPC9nPgo8L3N2Zz4K" class="_3KmO3E"><div class="_1sk9Vt">Certified Buyer</div></div><div class="_1sk9Vt">17 Aug, 2022</div><div class="row Ljko-4"><div><div class="_1LmwT9"><svg width="20" height="15" xmlns="http://www.w3.org/2000/svg" class="skCrcq"><path fill="#fff" class="_1LIt4y" d="M9.58.006c-.41.043-.794.32-1.01.728-.277.557-2.334 4.693-2.74 5.1-.41.407-.944.6-1.544.6v8.572h7.5c.45 0 .835-.28 1.007-.665 0 0 2.207-6.234 2.207-6.834 0-.6-.47-1.072-1.07-1.072h-3.216c-.6 0-1.07-.535-1.07-1.07 0-.537.835-3.387 1.006-3.944.17-.557-.107-1.157-.664-1.35-.15-.043-.257-.086-.407-.064zM0 6.434v8.572h2.143V6.434H0z" fill-rule="evenodd"></path></svg><span class="_3c3Px5">0</span></div><div class="_1LmwT9 pkR4jH"><svg width="20" height="15" xmlns="http://www.w3.org/2000/svg" class="skCrcq pkR4jH"><path fill="#fff" class="_1LIt4y" d="M9.58.006c-.41.043-.794.32-1.01.728-.277.557-2.334 4.693-2.74 5.1-.41.407-.944.6-1.544.6v8.572h7.5c.45 0 .835-.28 1.007-.665 0 0 2.207-6.234 2.207-6.834 0-.6-.47-1.072-1.07-1.072h-3.216c-.6 0-1.07-.535-1.07-1.07 0-.537.835-3.387 1.006-3.944.17-.557-.107-1.157-.664-1.35-.15-.043-.257-.086-.407-.064zM0 6.434v8.572h2.143V6.434H0z" fill-rule="evenodd"></path></svg><span class="_3c3Px5">0</span></div></div></div></div></div><a href="/sony-alpha-full-frame-ilce-7m2k-bq-in5-mirrorless-camera-body-28-70-mm-lens/product-reviews/itm92df94dc68fff?pid=DLLF6QZPNKTQMS8J"><div class="_2yVg4P">View all reviews of the product</div></a></div>""")

    #     scrapper = Flipkart(self.sony_camera_url)
    #     reviews = scrapper.get_all_reviews()
        
