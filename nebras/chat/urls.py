from django.urls import path
from .views import (
    ChatMessageListRetrieveUpdateDestroyView, 
    ChatMessageCreateView, 
    MessageFileCreateView,
    MessageFileRetrieveUpdateDestroyView
)

urlpatterns = [
    path('messages/', ChatMessageListRetrieveUpdateDestroyView.as_view(), name='chat-message-list'),
    path('messages/<int:pk>/', ChatMessageCreateView.as_view(), name='chat-message-detail'),
    path('files/', MessageFileCreateView.as_view(), name='chat-file-list-create'),
    path('files/<int:pk>/', MessageFileRetrieveUpdateDestroyView.as_view(), name='chat-file-detail'),
]
