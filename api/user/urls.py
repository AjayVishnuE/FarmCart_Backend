from django.urls import path
from .user_views import RegistrationAPIView, LoginAPIView, RefreshAPIView, LogoutAPIView,ForgotPasswordView, VerifyOTPView, LocationView, UsernameView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('refresh/', RefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', LogoutAPIView.as_view(), name="user-logout"),
    path('forgot-password/', ForgotPasswordView.as_view(), name="user-forgot-password"),
    path('verify-otp/', VerifyOTPView.as_view(), name="user-verify-otp"),
    path('location/', LocationView.as_view(), name="user-location"),
    path('username/', UsernameView.as_view(), name="username")
]
