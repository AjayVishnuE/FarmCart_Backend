from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import DownloadCount
from .downloadcount_serializer import DownloadCountSerializer

class DownloadCountView(APIView):
    def get(self, request):
        download_counts = DownloadCount.objects.all()
        serializer = DownloadCountSerializer(download_counts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DownloadCountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
