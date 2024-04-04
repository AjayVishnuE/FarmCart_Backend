from django.urls import path
from .cart_views import CartCrudView


urlpatterns = [
    path('cart-crud/', CartCrudView.as_view(), name='seller-crud'),
    path('cart-crud/<uuid:cart_id>/', CartCrudView.as_view(), name='seller-crud'),
]