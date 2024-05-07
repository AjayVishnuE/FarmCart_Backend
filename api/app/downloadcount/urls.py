from django.urls import path
from .downloadcounter_views import DownloadCountView

urlpatterns = [
    path('getpost/', DownloadCountView.as_view(), name='download-count'),
    path('download-count/<uuid:pk>/', DownloadCountView.as_view()),
]
