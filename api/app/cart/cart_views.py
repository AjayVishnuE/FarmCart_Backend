from uuid import UUID
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied


from api.models import Cart
from .cart_serializer import CartSerializer, CartDisplaySerializer
from api.user.authentication import get_user_id

class CartCrudView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return Response({"error": "Authorization token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = get_user_id(token)
        if not user_id:
            return Response({"error": "Token is invalid or expired"}, status=status.HTTP_401_UNAUTHORIZED)
        
        cart_list = Cart.objects.filter(user=user_id)
        serializer = CartDisplaySerializer(cart_list, many=True)  # Note the `many=True` for queryset serialization
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        data = request.data.copy()
        data['user']=user_id
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, cart_id):
        try:
            cart_product = Cart.objects.get(cart_id=cart_id)
        except cart_product.DoesNotExist:
            return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cart_id):
        token = request.headers.get('Authorization', None)
        try:
            user_id = get_user_id(token)  
            user_id = UUID(user_id)  

            cart_product = Cart.objects.get(cart_id=cart_id)
            if cart_product.user.id == user_id: 
                cart_product.delete()
                return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied({'error': 'Not Your Product'})

        except Cart.DoesNotExist:
            raise NotFound({'error': 'Product not found'})
        except PermissionDenied as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:  
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            