from django.shortcuts import render
from django.views import View
from scrapper.base import Scrapper, get_scrapper
from analysis.main import analyze_polarity
import logging
import json
from django.http import JsonResponse

logger = logging.getLogger(__name__)


# Create your views here.
class EnterProductURLView(View):

    def get(self, request):
        return render(request, 'index.html', )

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        received_json = json.loads(body_unicode)

        url = received_json["url"]

        logger.info("Received URL: %s", url)
        
        scrapper_class = get_scrapper(url)
        scrapper = scrapper_class(url)
        product_detail = scrapper.get_product_details()
        reviews = product_detail["reviews"]

        # convert tuple to list
        sentiment = list(analyze_polarity(reviews))
        logger.info("Sentiment: %s", sentiment)
        return JsonResponse({"sentiment": sentiment, "product_detail": product_detail} ,safe=False)