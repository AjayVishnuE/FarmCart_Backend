from rest_framework import serializers
from api.models import CustomUser, Product, FarmerDetails
from django.db.models import Sum, F

class FarmerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerDetails
        fields = ('farms',)

class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = ('product_name', 'product_image', 'quantity')

class ProductSalesSerializer(serializers.ModelSerializer):
    sold_quantity = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('product_name', 'sold_quantity')

class TopSoldProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    sold_quantity = serializers.IntegerField()


