from django.urls import path
from .user_views import RegistrationAPIView, LoginAPIView, RefreshAPIView, LogoutAPIView,ForgotPasswordView, VerifyOTPView, LocationView, UsernameView, EditUserView, ResetPasswordView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('refresh/', RefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', LogoutAPIView.as_view(), name="user-logout"),
    path('forgotpassword/', ForgotPasswordView.as_view(), name="user-forgot-password"),
    path('verifyotp/', VerifyOTPView.as_view(), name="user-verify-otp"),
    path('resetpassword/', ResetPasswordView.as_view(), name="reset-password"),

    path('location/', LocationView.as_view(), name="user-location"),
    path('username/', UsernameView.as_view(), name="username"),
    path('edituser/', EditUserView.as_view(), name='edit_user'),
    
]
