from rest_framework import serializers
from api.models import DownloadCount

class DownloadCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadCount
        fields = ['id', 'quantity']
