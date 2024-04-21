from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from rest_framework import status
from django.http import Http404


from .search_serializer import SearchSerializer,ProductSerializer
from api.models import Search, Product
from user.authentication import get_user_id


class RecentUserSearchesAPIView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        recent_searches = Search.objects.filter(user_id=user_id).order_by('-created_at')[:10] 
        serializer = SearchSerializer(recent_searches, many=True)
        return Response(serializer.data)

class SearchCreateAPIView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)  
        data = request.data.copy()
        data['user'] = user_id
        serializer = SearchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            search_keyword = data['search_keyword']
            matching_products = Product.objects.filter(product_name__icontains=search_keyword)

            product_serializer = ProductSerializer(matching_products, many=True)

            return Response({
                'search': serializer.data,
                'products': product_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SearchDeleteAPIView(APIView):
    def get_object(self, pk, user_id):
        try:
            return Search.objects.get(pk=pk, user__id=user_id)
        except Search.DoesNotExist:
            raise Http404("No Search found matching the ID provided.")

    def delete(self, request, pk):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)  
        search = self.get_object(pk, user_id)
        search.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FrequentSearchesAPIView(APIView):
    def get(self, request):
        one_day_ago = timezone.now() - timezone.timedelta(days=1)

        recent_searches = Search.objects.filter(created_at__gte=one_day_ago)
        search_counts = recent_searches.values('search_keyword').annotate(total=Count('search_keyword')).order_by('-total')[:10]

        keywords = [search['search_keyword'] for search in search_counts]

        top_products = Product.objects.filter(product_name__in=keywords).order_by('-product_name__in')

        products_dict = {product.product_name: product for product in top_products}
        sorted_products = sorted(top_products, key=lambda x: keywords.index(x.product_name))

        serializer = ProductSerializer(sorted_products, many=True)

        return Response(serializer.data)