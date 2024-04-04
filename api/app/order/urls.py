from django.urls import path
from .order_views import OrderCrudView


urlpatterns = [
    path('order-crud/', OrderCrudView.as_view(), name='order-crud'),
    path('order-crud/<uuid:order_id>/', OrderCrudView.as_view(), name='order-crud'),
]