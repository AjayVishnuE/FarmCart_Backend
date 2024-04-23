from rest_framework import serializers
from api.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review_id', 'product', 'reviewer', 'rating', 'comment', 'review_datetime']
