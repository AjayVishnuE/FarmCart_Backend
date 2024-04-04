from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('product/', include('api.app.products.urls')),
    path('cart/', include('api.app.cart.urls')),
    path('wishlist/', include('api.app.wishlist.urls')),
    path('order/', include('api.app.order.urls')),


]
