from rest_framework import serializers
from api.models import CustomUser, Product, FarmerDetails, Review


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
        fields = ['farmer_rating', 'farms', 'Verified']

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
            'product_rating', 
            'farmer_details', 
        ]

    def get_farmer_details(self, obj):
        farmer_details = FarmerDetails.objects.filter(user=obj.seller).first()
        return FarmerDetailsSerializer(farmer_details).data if farmer_details else None

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['reviewer', 'rating', 'comment']

class SellerProductDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'product_id', 'product_name', 'product_image',
            'product_description', 'price', 'quantity',
            'available', 'category', 'product_rating',
            'upload_datetime', 'reviews'
        ]

    def get_reviews(self, obj):
        reviews = Review.objects.filter(product=obj)
        return ReviewSerializer(reviews, many=True).data