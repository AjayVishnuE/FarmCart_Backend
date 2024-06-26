from django.db import models

import uuid

class CustomUser(models.Model):
    ROLE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('Consumer', 'Consumer')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    user_image = models.ImageField(upload_to='images/user', null=True, blank=True, default='images/user/default_user_image.png')
    mobile = models.CharField(max_length=20, default = "0000000000")
    location_latitude = models.CharField(max_length=100,  null=True, blank=True)
    location_longitude = models.CharField(max_length=100,  null=True, blank=True)

    def __str__(self):
        return self.username
    
class OTPVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Farmer'})
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='images/products', null=True, blank=True)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    sold_quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    category = models.CharField(max_length=100)
    product_rating = models.PositiveSmallIntegerField(default=0)
    upload_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
class Address(models.Model):
    Address_Type = [
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Other', 'Other')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=10, choices=Address_Type)
    name = models.CharField(max_length=25)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=15)

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    ]

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Consumer'})
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)
    order_datetime = models.DateTimeField(auto_now_add=True)

class OrderDetail(models.Model):
    order_detail_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Consumer'})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Wishlist(models.Model):
    wishlist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Consumer'})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


def update_farmer_rating(farmer):
    products = Product.objects.filter(seller=farmer)
    if products.exists():
        average_rating = products.aggregate(models.Avg('product_rating'))['product_rating__avg']
        farmer_details = FarmerDetails.objects.get(user=farmer)
        farmer_details.farmer_rating = round(average_rating, 1)
        farmer_details.save()

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Consumer'})
    rating = models.CharField(max_length=5)
    comment = models.TextField()
    review_datetime = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_rating()

    def update_product_rating(self):
        reviews = Review.objects.filter(product=self.product)
        average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.product.product_rating = round(average_rating, 1)  # Assuming 'product_rating' can handle decimals.
        self.product.save()
        update_farmer_rating(self.product.seller)

class Search(models.Model):
    search_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Consumer'})
    search_keyword = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class FarmerDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Farmer'})
    farmer_rating = models.CharField(max_length=5)
    farms = models.TextField()
    Verified = models.BooleanField(default=True)

class Complaints(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    complaint = models.TextField()

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)
    redirect = models.CharField(max_length=255)
    message = models.TextField()
    read_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"

class DownloadCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"DownloadCount: {self.quantity}"