from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(OTPVerification)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(Search)
admin.site.register(FarmerDetails)
admin.site.register(Complaints)
admin.site.register(Notification)
admin.site.register(DownloadCount)



