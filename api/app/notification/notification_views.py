from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.models import Notification, CustomUser
from .notification_serializer import NotificationSerializer 
from api.user.authentication import get_user_id

class NotificationsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        user = get_object_or_404(CustomUser, id=user_id)
        
        notifications = Notification.objects.filter(user=user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        user = get_object_or_404(CustomUser, id=user_id)

        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClearNotificationsAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        user = get_object_or_404(CustomUser, id=user_id)

        Notification.objects.filter(user=user).delete()
        return Response({"message": "All notifications have been deleted."}, status=status.HTTP_204_NO_CONTENT)
