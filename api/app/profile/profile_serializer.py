from rest_framework import serializers
from api.models import CustomUser, Order, OrderDetail, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'product_name', 'product_image', 'price')

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

class CustomOrderDetailSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderDetail
        fields = ('product_details', 'quantity', 'price_at_purchase')

class CustomOrderSerializer(serializers.ModelSerializer):
    custom_order_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('order_id', 'total_price', 'order_status', 'custom_order_details')

    def get_custom_order_details(self, obj):
        user = self.context['user']
        order_details = obj.orderdetail_set.filter(product__seller=user).order_by('-order__order_datetime')
        return CustomOrderDetailSerializer(order_details, many=True, read_only=True).data

class SellerOrdersSerializer(serializers.ModelSerializer):
    user_orders = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_image', 'user_orders')

    def get_user_orders(self, obj):
        orders = Order.objects.filter(orderdetail__product__seller=obj).order_by('-order_datetime').distinct()
        context = {'user': obj}
        return CustomOrderSerializer(orders, many=True, context=context).data
