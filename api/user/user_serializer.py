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

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','location_latitude', 'location_longitude']

    def update(self, instance, validated_data):
        instance.location_latitude = validated_data.get('location_latitude', instance.location_latitude)
        instance.location_longitude = validated_data.get('location_longitude', instance.location_longitude)
        instance.save()
        return instance

class UserReadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ['id', 'username', 'email', 'mobile', 'user_image', 'password', 'role']

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        return value

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        
        user = CustomUser.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        return user