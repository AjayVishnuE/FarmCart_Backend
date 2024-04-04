from uuid import UUID
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied


from api.models import Wishlist
from api.user.authentication import get_user_id
from .wishlist_serializer import WishlistSerializer

class WishlistCrudView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None) 
        user_id = get_user_id(token)
        cart_list = Wishlist.objects.filter(user = user_id)
        serializer = WishlistSerializer(cart_list, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        data = request.data.copy()
        data['user']=user_id
        serializer = WishlistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, cart_id):
        try:
            cart_product = Wishlist.objects.get(cart_id=cart_id)
        except cart_product.DoesNotExist:
            return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WishlistSerializer(cart_product, data=request.data, partial=True)
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

            wishlist_product = Wishlist.objects.get(cart_id=cart_id)
            if wishlist_product.user.id == user_id: 
                wishlist_product.delete()
                return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied({'error': 'Not Your Product'})

        except Wishlist.DoesNotExist:
            raise NotFound({'error': 'Product not found'})
        except PermissionDenied as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:  
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
