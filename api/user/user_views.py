import random
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from django.http import JsonResponse
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.contrib.auth.hashers import make_password, check_password

from api.models import CustomUser, OTPVerification
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token, get_user_id
from .user_serializer import CustomUserSerializer, ForgotPasswordSerializer, OTPVerificationSerializer, LocationSerializer, UserReadUpdateSerializer, ResetPasswordSerializer

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        EoM = data.get('EmailOrUsername')
        if EoM is None:
            raise APIException('EmailOrUsername is a mandatory field.')
        try:
            user = CustomUser.objects.get(username = EoM)
        except ObjectDoesNotExist:
            user = None
        if user is None:
            try:
                user = CustomUser.objects.get(email = EoM)
            except ObjectDoesNotExist:
                user = None
        if user is None:
            raise APIException('Invalid Credentials')

        if not user or not check_password(request.data['password'], user.password):
            raise APIException('Invalid Credentials')

        accessToken = create_access_token(user.id)
        refreshToken = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key='refreshToken', value=refreshToken, httponly=True)
        response.data = {
            'accessToken': accessToken,
            'refreshToken': refreshToken
        }

        return response

class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token' : access_token
        })
    

class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key = "refreshToken")
        response.data = {
            'message': "SUCCESS"
        }
        return response


class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            print(email)
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'User with this email does not exist.'}, status=400)
            
            otp = str(random.randint(100000, 999999))
            
            OTPVerification.objects.create(user=user, otp=otp)
            print(otp)
            send_mail(
                'Reset Your Password',
                f'Your OTP is {otp}.',
                'teamfarmcart@gmail.com',  
                [email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to your email.'}, status=200)
        return Response(serializer.errors, status=400)
    
class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'Invalid email address.'}, status=400)
            
            otp_valid_time = 10 
            try:
                otp_record = OTPVerification.objects.get(
                    user=user, 
                    otp=otp, 
                    created_at__gte=timezone.now() - timedelta(minutes=otp_valid_time)
                )

                otp_record.delete()

                return Response({'message': 'OTP verified successfully!'}, status=200)
            except OTPVerification.DoesNotExist:
                return Response({'error': 'Invalid or expired OTP.'}, status=400)
        return Response(serializer.errors, status=400)

class LocationView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not token.startswith('Bearer '):
            return Response({'error': 'Authorization header must start with Bearer'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = token.split('Bearer ')[1]
        user_id = decode_access_token(token)
        if not user_id:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LocationSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsernameView(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization', None)
            user_id = get_user_id(token)
            user = CustomUser.objects.get(id=user_id)
            return JsonResponse({"username":user.username,"role":user.role}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

class EditUserView(APIView):
    def get(Self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        user = CustomUser.objects.get(id=user_id)
        serializer = UserReadUpdateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        try:
            token = request.headers.get('Authorization', None)
            user_id = get_user_id(token)
            user = CustomUser.objects.get(id=user_id)
        except user.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserReadUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)