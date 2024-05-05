from django.urls import path
from .notification_views import NotificationsListAPIView, ClearNotificationsAPIView

urlpatterns = [
    path('getpost/', NotificationsListAPIView.as_view(), name='list-notifications'),
    path('clear/', ClearNotificationsAPIView.as_view(), name='clear-notifications'),
]
