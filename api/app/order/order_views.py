from uuid import UUID
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied


from api.models import Order
from api.user.authentication import get_user_id
from .order_serializer import OrderSerializer

class OrderCrudView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None) 
        user_id = get_user_id(token)
        cart_list = Order.objects.filter(buyer_id = user_id)
        serializer = OrderSerializer(cart_list, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        data = request.data.copy()
        data['buyer']=user_id
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, order_id):
        pass

    def delete(self, request, order_id):
        token = request.headers.get('Authorization', None)
        try:
            user_id = get_user_id(token)  
            user_id = UUID(user_id)  

            order_data = Order.objects.get( order_id = order_id)
            if order_data.buyer.id == user_id: 
                order_data.delete()
                return Response({'message': 'Order deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied({'error': 'Not Your Product'})

        except Order.DoesNotExist:
            raise NotFound({'error': 'Order not found'})
        except PermissionDenied as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:  
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)