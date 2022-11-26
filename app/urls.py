from django.urls import path

from .views import EnterProductURLView

urlpatterns = [
    path('', EnterProductURLView.as_view(), name='product_url'),
]