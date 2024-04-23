from django.urls import path
from .search_views import SearchCreateAPIView, SearchDeleteAPIView, CombinedSearchesAPIView

urlpatterns = [
    path('create/', SearchCreateAPIView.as_view(), name='search-create'),
    path('delete/<uuid:pk>/', SearchDeleteAPIView.as_view(), name='search-delete'),
    path('frequentrecent/', CombinedSearchesAPIView.as_view(), name="frequent recent searches"),
]
