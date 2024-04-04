from django.urls import path
from .wishlist_views import WishlistCrudView


urlpatterns = [
    path('wishlist-crud/', WishlistCrudView.as_view(), name='wishlist-crud'),
    path('wishlist-crud/<uuid:wishlist_id>/', WishlistCrudView.as_view(), name='wishlist-crud'),

]