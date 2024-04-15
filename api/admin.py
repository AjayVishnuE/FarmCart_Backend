from django.contrib import admin
from .models import CustomUser,Product, Order, OrderDetail, Cart, Wishlist,Review,FarmerDetails,Address

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(FarmerDetails)
admin.site.register(Address)




