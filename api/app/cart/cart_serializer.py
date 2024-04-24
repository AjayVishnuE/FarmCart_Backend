from rest_framework import serializers
from api.models import CustomUser, Cart, Product
from django.db.models import F
from django.db import transaction

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["cart_id","user","product","quantity"]

    def create(self, validated_data):
        user = validated_data['user']
        product = validated_data['product']
        quantity = validated_data['quantity']

        with transaction.atomic():
            cart_item, created = Cart.objects.select_for_update().get_or_create(
                user=user,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                Cart.objects.filter(pk=cart_item.pk).update(quantity=F('quantity') + quantity)
                cart_item.refresh_from_db()

        return cart_item
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_name","product_image","quantity","price"]
    
class CartDisplaySerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["cart_id", "user", "product", "quantity", "product_details"]

    def get_product_details(self, obj):
        return ProductSerializer(obj.product).data