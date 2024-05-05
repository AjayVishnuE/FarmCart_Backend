from rest_framework import serializers
from api.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'redirect', 'message', 'read_status', 'timestamp']
