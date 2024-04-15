from rest_framework import serializers
from api.models import CustomUser, OrderDetail

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ["order_detail_id","order","product","quantity","price_at_purchase"]

    def create(self, validated_data):
        return super().create(validated_data)
    