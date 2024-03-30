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
    user_image = models.ImageField(upload_to='images/user', null=True, blank=True)
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
    available = models.BooleanField(default=True)
    category = models.CharField(max_length=100)
    upload_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    ]

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Consumer'})
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

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Consumer'})
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    review_datetime = models.DateTimeField(auto_now_add=True)

class Search(models.Model):
    search_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Consumer'})
    search_keyword = models.CharField(max_length=200)
