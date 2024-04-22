from django.urls import path
from .profile_views import UserOrderDetailView, SellerOrdersAPIView

urlpatterns = [
    path('consumerprofile/', UserOrderDetailView.as_view(), name='user-order-detail'),
    path('farmerprofile/', SellerOrdersAPIView.as_view(), name='farmer-profile')
]
