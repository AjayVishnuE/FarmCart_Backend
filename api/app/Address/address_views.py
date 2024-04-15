from uuid import UUID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
 
from api.models import Address, CustomUser
from api.user.authentication import get_user_id
from .address_serializer import AddressSerializer


def get_user_id_from_token(request):
    token = request.headers.get('Authorization', None)
    user_id = get_user_id(token)
    return user_id

class AddressListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = get_user_id_from_token(request)
        addresses = Address.objects.filter(user_id=user_id)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            user_id = get_user_id_from_token(request)
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def patch(self, request, pk, *args, **kwargs):
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
