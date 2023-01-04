import logging
from scrapper.base import Scrapper
import dataclasses, typing

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class AmazonScrapper(Scrapper):
    """Scrapes Amazon product details."""

    RECENT = "recent"
    HELPFUL = "helpful"

    REVIEW_SORTING = {"recent": RECENT, "helpful": HELPFUL}

    def __post_init__(self):
        logger.info("AmazonScrapper initialized.")
        self.soup = self.get_soup(self.url)

    def get_product_title(self):
        return self.soup.find("span", {"id": "productTitle"}).text.strip()

    def get_price(self):
        """Returns the price of the product."""
        try:
            return self.soup.find_all("span", class_="a-offscreen")[0].text
        except IndexError:
            return None

    def get_rating(self):
        """Returns the product rating."""
        histogram = {}
        table_rows = self.soup.find("table", {"id": "histogramTable"}).find_all(
            "tr",
        )

        for row in table_rows:
            rating = row.find_all("td")[0].text.strip()
            count = row.find_all("td")[-1].text.strip()
            histogram[rating] = count

        return histogram

    def get_size(self):
        try:
            size, *_ = self.soup.find_all("span", {"class": "selection"})
            if size:
                return size.text.strip()
            return None
        except ValueError:
            return None

    def get_color(self):
        try:
            _, color, *_ = self.soup.find_all("span", {"class": "selection"})
            if color:
                return color.text.strip()
            return None
        except ValueError:
            return None

    def number_of_global_ratings(self):
        return self.soup.find("span", {"id": "acrCustomerReviewText"}).text.strip()

    def get_all_reviews_url(self) -> str:
        """Returns the review url."""
        try:
            reviews_page_url = self.soup.find(
                "a", {"data-hook": "see-all-reviews-link-foot"}
            ).get("href")
            return f"{self.base_url}{reviews_page_url}"
        except AttributeError:
            raise AttributeError("There are no reviews for this product.")

    def review_page_urls(self, sort_by: str = RECENT):
        """Returns the review details."""
        all_reviews_url = self.get_all_reviews_url()
        all_reviews_url += f"&sortBy={sort_by}"

        # Get all reviews page
        soup = self.get_soup(all_reviews_url)

        # 2,230 total ratings, 185 with reviews
        total_ratings_and_reviews = soup.find(
            "div", {"data-hook": "cr-filter-info-review-rating-count"}
        ).text.strip()
        review_count = int(total_ratings_and_reviews.split(",")[-1].split()[0])

        total_review_pages = review_count // 10
        urls = []

        if total_review_pages == 0:
            raise ValueError(f"There are only {review_count} reviews.")

        for page_number in range(1, total_review_pages):
            url = f"{all_reviews_url}&pageNumber={page_number}"
            urls.append(url)

        return urls

    def reviews(self, urls: typing.List):
        """ """
        user_reviews = []
        for url in urls:
            soup = self.get_soup(url)
            reviews = soup.find_all("div", {"data-hook": "review"})

            for review in reviews:
                author = review.find("span", {"class": "a-profile-name"}).text
                rating = review.find("span", {"class": "a-icon-alt"}).text
                try:
                    title = review.find("a", {"data-hook": "review-title"}).text.strip()
                except AttributeError:
                    title = ""

                place_and_date = soup.find(
                    "span", {"data-hook": "review-date"}
                ).text.strip()
                place, date = place_and_date.split("on")
                _, place = place.split("Reviewed in")

                # Specifications
                spec = soup.find("a", {"data-hook": "format-strip"})
                try:
                    spec_list = [x.text for x in spec if x.text != ""]
                    specifications = {
                        x.split(":")[0].strip(): x.split(":")[1].strip()
                        for x in spec_list
                    }
                except TypeError:
                    specifications = None
                try:
                    verified_purchase = (
                        review.find("span", {"data-hook": "avp-badge"}).text
                        == "Verified Purchase"
                    )
                except AttributeError:
                    verified_purchase = False

                try:
                    content = review.find("span", {"data-hook": "review-body"}).text
                except AttributeError:
                    content = ""

                user_reviews.append(
                    {
                        "author": author,
                        "rating": rating,
                        "title": title,
                        "place": place,
                        "date": date,
                        "specifications": specifications,
                        "verified_purchase": verified_purchase,
                        "content": content,
                    }
                )
        return user_reviews

    def get_product_details(self):
        reviews = self.reviews(self.review_page_urls())
        return {
            "title": self.get_product_title(),
            "rating": self.get_rating(),
            "size": self.get_size(),
            "color": self.get_color(),
            "global_ratings": self.number_of_global_ratings(),
            "price": self.get_price(),
            "reviews": reviews,
        }
