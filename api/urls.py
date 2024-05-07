from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('product/', include('api.app.products.urls')),
    path('cart/', include('api.app.cart.urls')),
    path('wishlist/', include('api.app.wishlist.urls')),
    path('order/', include('api.app.order.urls')),
    path('orderdetails/', include('api.app.orderdetails.urls')),
    path('chat/', include('api.app.Chat.urls')),
    path('address/', include('api.app.Address.urls')),
    path('profile/', include('api.app.profile.urls')),
    path('search/', include('api.app.search.urls')),
    path('farmerdashboard/', include('api.app.farmer_dashboard.urls')),
    path('farmerdetails/', include('api.app.farmerdetails.urls')),
    path('review/', include('api.app.review.urls')),
    path('notification/', include('api.app.notification.urls')),
    path('downloadcount/', include('api.app.downloadcount.urls')),

]
