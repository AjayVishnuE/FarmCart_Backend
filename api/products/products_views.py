from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .products_serializer import ProductSerializer
from api.user.authentication import decode_access_token

class ProductsListView(APIView):
    def post(self,request):
        pass
        # token = request.headers.get('Authorization', None)
        # if not token:
        #     return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if not token.startswith('Bearer '):
        #     return Response({'error': 'Authorization header must start with Bearer'}, status=status.HTTP_400_BAD_REQUEST)
        
        # token = token[7:]
        # user_id = decode_access_token(token)

        # data = request.data
        # serializer = ProductSerializer(user_id, data,partial = True)
        # if serializer.is_valid():
        #     serializer.save()
        #     print("ok")
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
