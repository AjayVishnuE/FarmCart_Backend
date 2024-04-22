from rest_framework import serializers
from api.models import CustomUser, Product, Order, OrderDetail, FarmerDetails

class FarmDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerDetails
        fields = ['farms']

class ProductDetailSerializer(serializers.ModelSerializer):
    farms = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'farms', 'quantity']

    def get_farms(self, obj):
        if isinstance(obj, Product):
            farmer_details = FarmerDetails.objects.filter(user=obj.seller).first()
            return FarmDetailsSerializer(farmer_details).data
        else:
            return None

class UserProductOrdersSerializer(serializers.Serializer):
    username = serializers.CharField(source='user.username')  
    num_recent_orders = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    product_details = ProductDetailSerializer(many=True)

