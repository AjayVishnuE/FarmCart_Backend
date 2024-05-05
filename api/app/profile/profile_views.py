from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.user.authentication import get_user_id 
from .profile_serializer import UserOrderDetailSerializer, SellerOrdersSerializer
from api.models import CustomUser, OrderDetail, Order

class UserOrderDetailView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        try:
            orders_prefetch = Prefetch(
                'order_set',
                queryset=Order.objects.prefetch_related(
                    Prefetch(
                        'orderdetail_set',
                        queryset=OrderDetail.objects.select_related('product')
                    )
                ).order_by('-order_datetime')
            )
            user = CustomUser.objects.prefetch_related(orders_prefetch).get(id=user_id)
            serializer = UserOrderDetailSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SellerOrdersAPIView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        try:
            seller = CustomUser.objects.get(pk=user_id, role='Farmer')
        except CustomUser.DoesNotExist:
            return Response({'message': 'Seller not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SellerOrdersSerializer(seller, context={'user': seller})
        return Response(serializer.data, status=status.HTTP_200_OK)
