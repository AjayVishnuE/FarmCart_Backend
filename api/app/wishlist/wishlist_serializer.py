from rest_framework import serializers
from api.models import CustomUser, Wishlist, Product



class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["wishlist_id","user","product"]

    def create(self, validated_data):
        return super().create(validated_data)
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'product_name', 'product_image', 'price')

class WishlistGetSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('product_details', "wishlist_id","user")