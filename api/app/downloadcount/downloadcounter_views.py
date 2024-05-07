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

    def patch(self, request, pk):
        try:
            download_count = DownloadCount.objects.get(pk=pk)
        except DownloadCount.DoesNotExist:
            return Response({'error': 'Download count not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DownloadCountSerializer(download_count, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)