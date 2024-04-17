from rest_framework import serializers
from api.models import CustomUser, Order, OrderDetail, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_name', 'product_image', 'price')

class OrderDetailSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderDetail
        fields = ('product_details', 'quantity', 'price_at_purchase')

class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(source='orderdetail_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('order_id', 'total_price', 'order_status', 'order_details')

class UserOrderDetailSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(source='order_set', many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_image', 'orders')
