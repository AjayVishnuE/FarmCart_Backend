from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Review, Product, CustomUser
from .review_serializer import ReviewSerializer
from api.user.authentication import get_user_id

class CreateReviewAPIView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        user = get_object_or_404(CustomUser, pk=user_id)
        request.data['reviewer'] = user_id  
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RetrieveReviewAPIView(APIView):
    def get(self, request, product_id):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        review = get_object_or_404(Review, product=product_id, reviewer=user_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
class UpdateReviewAPIView(APIView):
    def put(self, request, uuid):
        review = get_object_or_404(Review, review_id=uuid)
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        request.data['reviewer'] = user_id  

        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteReviewAPIView(APIView):
    def delete(self, request, uuid):
        review = get_object_or_404(Review, review_id=uuid)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
