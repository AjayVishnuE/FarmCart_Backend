from django.urls import path
from .farmerdetails_views import FarmerDetailsAPI

urlpatterns = [
    path('farmer-details/', FarmerDetailsAPI.as_view(), name='farmer-details'),
]
