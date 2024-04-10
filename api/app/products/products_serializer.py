from rest_framework import serializers
from api.models import CustomUser, Product, FarmerDetails


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["seller","product_id","product_name","product_image","product_description","price","quantity","available","category"]
    
    def create(self, validated_data):
        return super().create(validated_data)
    

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'user_image', 'location_latitude', 'location_longitude']

class FarmerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerDetails
        fields = ['overallrating', 'farms', 'Verified']

class ProductDetailsSerializer(serializers.ModelSerializer):
    seller_details = CustomUserSerializer(source='seller', read_only=True)
    farmer_details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'product_id',
            'product_name',
            'product_image',
            'product_description',
            'price',
            'quantity',
            'available',
            'category',
            'upload_datetime',
            'seller_details',  
            'farmer_details',
        ]

    def get_farmer_details(self, obj):
        farmer_details = FarmerDetails.objects.filter(user=obj.seller).first()
        return FarmerDetailsSerializer(farmer_details).data if farmer_details else None



