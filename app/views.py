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

        # convert tuple to list
        sentiment = list(analyze_polarity(reviews))
        logger.info("Sentiment: %s", sentiment)
        return render(request, 'results.html', {"sentiment": sentiment, "product_detail": product_detail})