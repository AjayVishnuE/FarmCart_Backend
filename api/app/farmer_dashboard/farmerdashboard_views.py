from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import CustomUser, Product, OrderDetail
from api.user.authentication import get_user_id
from .farmdash_serializer import UserProductOrdersSerializer, ProductDetailSerializer

class UserProductStatsAPIView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        try:
            user = CustomUser.objects.get(id=user_id, role='Farmer')
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found or not a farmer."}, status=404)

        one_day_ago = timezone.now() - timezone.timedelta(days=1)
        products = Product.objects.filter(seller=user_id)
        product_serializer = ProductDetailSerializer(products, many=True)

        num_recent_orders = OrderDetail.objects.filter(
            product__in=products,
            order__order_datetime__gte=one_day_ago
        ).count()

        total_orders = OrderDetail.objects.filter(product__in=products).count()

        user_data = {
            "user": user,
            "num_recent_orders": num_recent_orders,
            "total_orders": total_orders,
            "product_details": product_serializer.data
        }

        serializer = UserProductOrdersSerializer(user_data)
        response_data = serializer.data
        top_sold_product = Product.objects.filter(seller=user).order_by('-sold_quantity').first()
        if top_sold_product:
            response_data['top_sold_product'] = {
                'product_name': top_sold_product.product_name,
                'sold_quantity': top_sold_product.sold_quantity
            }
        else:
            response_data['top_sold_product'] = 'No sales'

        return Response(response_data)