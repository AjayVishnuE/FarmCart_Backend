from uuid import UUID
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from math import radians, cos, sin, asin, sqrt
from rest_framework.exceptions import PermissionDenied

from api.models import Product, CustomUser
from api.user.authentication import get_user_id
from .products_serializer import ProductSerializer, ProductDetailsSerializer, SellerProductDetailSerializer

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  
    return c * r

class ProductsListView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        user = CustomUser.objects.get(id=user_id)
        user_location = (float(user.location_latitude), float(user.location_longitude))

        nearby_sellers_ids = []
        for seller in CustomUser.objects.filter(role='Farmer'):
            seller_location = (float(seller.location_latitude), float(seller.location_longitude))
            distance = haversine(user_location[1], user_location[0], seller_location[1], seller_location[0])
            if distance <= 30:
                nearby_sellers_ids.append(seller.id)
        
        products = Product.objects.filter(seller_id__in=nearby_sellers_ids)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductdetailsView(APIView):
    def get_object(self, product_id):
        try:
            return Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            raise Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, product_id):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        product = self.get_object(product_id)
        serializer = ProductDetailsSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductSellerDetailView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            serializer = SellerProductDetailSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SellerProductCrudView(APIView):
    def get(self,request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        products = Product.objects.filter(seller = user_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self,request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        data = request.data.copy()
        data['seller']=user_id
        serializer = ProductSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
        except product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, product_id):
        try:
            token = request.headers.get('Authorization', None)
            user_id = get_user_id(token)
            user_id = UUID(user_id)

            product = Product.objects.get(product_id=product_id)
            if product.seller.id == user_id: 
                product.delete()
                return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied({'error': 'Not Your Product'})
        except Product.DoesNotExist:  
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
