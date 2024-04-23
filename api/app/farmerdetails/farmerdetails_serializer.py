from rest_framework import serializers
from django.shortcuts import get_object_or_404
from api.models import FarmerDetails, CustomUser

class FarmerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerDetails
        fields = '__all__'
        read_only_fields = ('user',) 
        
    def create(self, validated_data):
        user = validated_data.pop('user', None)
        if not user:
            raise serializers.ValidationError("User is required.")
        return FarmerDetails.objects.create(user=user, **validated_data)
