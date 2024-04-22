from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Product
from api.user.authentication import get_user_id
from .products_serializer import ProductSerializer, ProductDetailsSerializer, SellerProductDetailSerializer


class ProductsListView(APIView):
    def get(self, request):
        products = Product.objects.all()
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
                product = Product.objects.get(product_id=product_id)
            except product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
