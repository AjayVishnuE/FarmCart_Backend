from django.urls import path
from .wishlist_views import WishlistCrudView


urlpatterns = [
    path('wishlist-crud/<uuid:product_id>/', WishlistCrudView.as_view(), name='seller-crud'),

]