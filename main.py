import argparse
import logging
import sys
from scrapper.amazon import AmazonScrapper
from analysis.main import analyze_polarity

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()

parser.add_argument(
    "product_url",
    nargs="?",
)


def main(URL):
    logger.info("Starting Scrapper")
    scrapper = AmazonScrapper(URL)

    product_detail = scrapper.product_detail()
    logger.info("Scrapper finished")
    logger.info("Product Title: %s", product_detail["title"])
    

    logger.info("Starting Analysis")
    reviews = product_detail["reviews"]
    text = []
    for review in reviews:
        text.append("".join(review["title"] + review["content"]))

    logger.info("Sentiment Analysis")
    logger.info("----------------------------------------\n")

    analyze_polarity(text)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.product_url)
