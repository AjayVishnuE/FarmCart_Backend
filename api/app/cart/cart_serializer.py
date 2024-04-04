from rest_framework import serializers
from api.models import CustomUser, Cart



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["cart_id","user","product","quantity"]

    def create(self, validated_data):
        return super().create(validated_data)