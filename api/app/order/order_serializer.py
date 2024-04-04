from rest_framework import serializers
from api.models import CustomUser, Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order_id","buyer","total_price","order_status","order_datetime"]

    def create(self, validated_data):
        return super().create(validated_data)
    

