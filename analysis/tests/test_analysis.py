from unittest import TestCase, mock
from .fixtures import iphone_13
from analysis import main


class TestSentimentAnalysis(TestCase):
    """Test sentiment analysis"""

    def test_analyze(self):
        """Test analyze"""
        reviews = iphone_13.data["reviews"]
        text = []
        for review in reviews:
            text.append("".join(review["title"] + review["content"]))
        main.analyze_polarity(text)
