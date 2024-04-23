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
    sold_products = serializers.SerializerMethodField()
    top_sold_product = serializers.SerializerMethodField()

    def get_sold_products(self, obj):
        products = Product.objects.filter(seller=obj['user'])
        return [{'product_name': product.product_name, 'sold_quantity': product.sold_quantity} for product in products]
    
    def get_top_sold_product(self, obj):
            user = obj['user']
            top_sold_product = Product.objects.filter(seller=user).order_by('-sold_quantity').first()
            if top_sold_product:
                return {
                    'product_name': top_sold_product.product_name,
                    'sold_quantity': top_sold_product.sold_quantity
                }
            return None

