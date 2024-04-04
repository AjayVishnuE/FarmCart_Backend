from rest_framework import serializers
from api.models import CustomUser, Wishlist



class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["__all__"]

    def create(self, validated_data):
        return super().create(validated_data)