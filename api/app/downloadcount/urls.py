from django.urls import path
from .downloadcounter_views import DownloadCountView

urlpatterns = [
    path('getpost/', DownloadCountView.as_view(), name='download-count'),
]
