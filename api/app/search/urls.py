from django.urls import path
from .search_views import SearchCreateAPIView, RecentUserSearchesAPIView, SearchDeleteAPIView, FrequentSearchesAPIView

urlpatterns = [
    path('create/', SearchCreateAPIView.as_view(), name='search-create'),
    path('recent/', RecentUserSearchesAPIView.as_view(), name='search-recent'),
    path('delete/<uuid:pk>/', SearchDeleteAPIView.as_view(), name='search-delete'),
    path('frequent/', FrequentSearchesAPIView.as_view(), name="frequent searches")
]
