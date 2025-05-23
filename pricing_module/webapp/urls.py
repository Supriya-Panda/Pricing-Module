from django.urls import path
from .views import CalculatePriceView

urlpatterns = [
    path("api/calculate-price/", CalculatePriceView.as_view(), name="calculate-price"),
]