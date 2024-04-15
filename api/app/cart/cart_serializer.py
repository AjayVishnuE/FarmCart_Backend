from rest_framework import serializers
from api.models import CustomUser, Cart, Product



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["cart_id","user","product","quantity"]

    def create(self, validated_data):
        return super().create(validated_data)
    
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