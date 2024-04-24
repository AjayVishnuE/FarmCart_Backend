from django.urls import path
from .review_views import CreateReviewAPIView, RetrieveReviewAPIView, UpdateReviewAPIView, DeleteReviewAPIView

urlpatterns = [
    path('create/', CreateReviewAPIView.as_view(), name='create-review'),
    path('read/<uuid:product_id>/', RetrieveReviewAPIView.as_view(), name='retrieve-review'),
    path('update/<uuid:uuid>/', UpdateReviewAPIView.as_view(), name='update-review'),
    path('reviews/<uuid:uuid>/delete/', DeleteReviewAPIView.as_view(), name='delete-review'),
]
