from django.urls import path
from .products_views import ProductsListView

urlpatterns = [
    path('productList/', ProductsListView.as_view(), name='product-list'),
]
