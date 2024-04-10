from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .products_views import ProductsListView, SellerProductCrudView, ProductdetailsView


urlpatterns = [
    path('productlist/', ProductsListView.as_view(), name='product-list'),
    path('seller-crud/', SellerProductCrudView.as_view(), name='seller-crud'),
    path('seller-crud/<uuid:product_id>/', SellerProductCrudView.as_view(), name='seller-crud'),
    path('product-details/<uuid:product_id>/',ProductdetailsView.as_view(), name='user-side-product-details'  )
]
