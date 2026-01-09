from django.contrib import admin
from .models import ChatMessage, MessageFile

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('message', 'user__username')

@admin.register(MessageFile)
class MessageFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'file')
    list_filter = ('user',)
