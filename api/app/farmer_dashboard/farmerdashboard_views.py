from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from api.models import CustomUser, Product, OrderDetail, FarmerDetails
from .farmdash_serializer import ProductSerializer, ProductSalesSerializer, TopSoldProductSerializer, FarmerDetailsSerializer
from api.user.authentication import get_user_id

class UserProductStatsAPIView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        try:
            user = CustomUser.objects.get(id=user_id, role='Farmer')
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found or not a farmer."}, status=404)

        products = Product.objects.filter(seller=user)
        products_data = ProductSerializer(products, many=True).data

        one_day_ago = timezone.now() - timezone.timedelta(days=1)
        num_recent_orders = OrderDetail.objects.filter(
            product__in=products,
            order__order_datetime__gte=one_day_ago
        ).count()

        total_orders = OrderDetail.objects.filter(product__in=products).count()

        farmer_details = FarmerDetails.objects.get(user=user)
        farms_data = FarmerDetailsSerializer(farmer_details).data

        top_product = products.order_by('-sold_quantity').first()
        top_product_data = TopSoldProductSerializer({
            'product_name': top_product.product_name,
            'sold_quantity': top_product.sold_quantity
        }).data if top_product else None

        sales_data = ProductSalesSerializer(products, many=True).data

        response_data = {
            'username': user.username,
            'farms': farms_data['farms'],
            'products': products_data,
            'daily_orders': num_recent_orders,
            'total_orders': total_orders,
            'top_sold_product': top_product_data,
            'product_sales': sales_data
        }

        return Response(response_data)
