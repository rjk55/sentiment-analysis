from django.urls import path

from .views import EnterProductURLView

urlpatterns = [
    path('enter-product-url', EnterProductURLView.as_view(), name='product_url'),
]