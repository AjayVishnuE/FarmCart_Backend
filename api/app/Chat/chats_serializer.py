from rest_framework import serializers
from api.models import Complaints

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = ['complaint']

class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    response = serializers.CharField(max_length=1000, read_only=True)
