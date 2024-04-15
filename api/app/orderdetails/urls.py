from django.urls import path
from .orderdetails_views import OrderDetailView

urlpatterns = [
    path('<uuid:order_id>/', OrderDetailView.as_view(), name='order-details-by-order'),
]