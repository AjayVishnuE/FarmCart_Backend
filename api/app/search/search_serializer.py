from rest_framework import serializers
from api.models import Search, Product

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_id","product_name","product_image","price"]
