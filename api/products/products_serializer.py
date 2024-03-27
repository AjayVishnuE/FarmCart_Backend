from rest_framework import serializers
from api.models import CustomUser, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["seller","product_id","product_name","product_image","product_description","price","quantity","available","category"]
    
    def create(self, validated_data):
        return super().create(validated_data)







