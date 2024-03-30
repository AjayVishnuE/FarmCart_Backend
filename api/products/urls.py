from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .products_views import ProductsListView, SellerProductCrudView


urlpatterns = [
    path('productlist/', ProductsListView.as_view(), name='product-list'),
    path('seller-crud/<uuid:product_id>/', SellerProductCrudView.as_view(), name='seller-crud'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
