from django.urls import path
from .profile_views import UserOrderDetailView

urlpatterns = [
    path('consumerprofile/', UserOrderDetailView.as_view(), name='user-order-detail'),
]
