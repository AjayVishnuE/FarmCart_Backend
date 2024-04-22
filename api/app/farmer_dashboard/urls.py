from django.urls import path
from .farmerdashboard_views import UserProductStatsAPIView

urlpatterns = [
    path('data/', UserProductStatsAPIView.as_view(), name='user-product-stats'),
]
