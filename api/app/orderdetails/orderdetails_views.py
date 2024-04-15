from uuid import UUID
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied


from api.models import OrderDetail
from api.user.authentication import get_user_id
from .orderdetails_serializer import OrderDetailSerializer

class OrderDetailView(APIView):
    def get(self, request, order_id):
        order_details = OrderDetail.objects.filter(order=order_id)
        serializer = OrderDetailSerializer(order_details, many=True)
        return Response(serializer.data)

    def post(self, request, order_id):
        data = request.data
        data['order'] = order_id  # Ensure the order ID is set to the current order
        serializer = OrderDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, orderDetail_id):
        pass

    def delete(self, request, orderDetail_id):
        token = request.headers.get('Authorization', None)
        try:
            user_id = get_user_id(token)  
            user_id = UUID(user_id)  

            orderDetail_data = OrderDetail.objects.get( orderDetail_id = orderDetail_id)
            if orderDetail_data.buyer.id == user_id: 
                orderDetail_data.delete()
                return Response({'message': 'OrderDetail deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied({'error': 'Not Your Product'})

        except OrderDetail.DoesNotExist:
            raise NotFound({'error': 'OrderDetail not found'})
        except PermissionDenied as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:  
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)