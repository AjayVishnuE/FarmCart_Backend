from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .products_views import ProductsListView


urlpatterns = [
    path('productlist/', ProductsListView.as_view(), name='product-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
