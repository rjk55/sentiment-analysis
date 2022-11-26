from django.shortcuts import render, HttpResponse
from django.views import View
from scrapper.amazon import AmazonScrapper
from analysis.main import analyze_polarity
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class EnterProductURLView(View):

    def get(self, request):
        return render(request, 'index.html', )

    def post(self, request):
        url = request.POST["url"]
        logger.info("Received URL: %s", url)
        scrapper = AmazonScrapper(url)
        product_detail = scrapper.product_detail()
        reviews = product_detail["reviews"]
        text = []
        for review in reviews:
            text.append("".join(review["title"] + review["content"]))
        polarity = analyze_polarity(text)

        # Convert values to a list
        sentiment = [polarity["positive"], polarity["negative"], polarity["neutral"]]
        return render(request, 'results.html', {"sentiment": sentiment, "product_detail": product_detail})