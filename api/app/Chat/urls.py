from django.urls import path
from .chats_views import ChatbotView, ComplaintAPIView

urlpatterns = [
    path('chat/', ChatbotView.as_view(), name='chatbot'),
    path('complaint/', ComplaintAPIView.as_view(), name='complaint-api'),
]
