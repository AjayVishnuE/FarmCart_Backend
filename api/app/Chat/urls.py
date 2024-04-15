from django.urls import path
from .chats_views import ChatGPTView

urlpatterns = [
    path('chat/', ChatGPTView.as_view(), name='chat-gpt'),
]
