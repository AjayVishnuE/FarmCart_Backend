from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from api.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)