from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.user.authentication import get_user_id
from api.models import FarmerDetails, CustomUser
from .farmerdetails_serializer import FarmerDetailsSerializer

class FarmerDetailsAPI(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None) 
        user_id = get_user_id(token)
        farmer_details = get_object_or_404(FarmerDetails, user__id=user_id)
        serializer = FarmerDetailsSerializer(farmer_details)
        return Response(serializer.data)

    def post(self, request):
        token = request.headers.get('Authorization', None) 
        user_id = get_user_id(token)
        user = get_object_or_404(CustomUser, pk=user_id)
        
        serializer = FarmerDetailsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request):
        token = request.headers.get('Authorization', None) 
        user_id = get_user_id(token)
        farmer_details = get_object_or_404(FarmerDetails, user__id=user_id)
        serializer = FarmerDetailsSerializer(farmer_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)