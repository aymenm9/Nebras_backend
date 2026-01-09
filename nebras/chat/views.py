from rest_framework import generics, permissions
from .models import ChatMessage, MessageFile
from .serializers import ChatMessageSerializer, MessageFileSerializer
from users.permissions import IsModerator

class ChatMessageListRetrieveUpdateDestroyView(generics.ListAPIView):

    queryset = ChatMessage.objects.all().order_by('-created_at')
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator]

class ChatMessageCreateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator]

class MessageFileCreateView(generics.ListCreateAPIView):

    queryset = MessageFile.objects.all()
    serializer_class = MessageFileSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator]
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class MessageFileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MessageFile.objects.all()
    serializer_class = MessageFileSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
