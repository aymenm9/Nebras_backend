
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):

        user = self.scope["user"]
        
        if not user.is_authenticated:
            await self.close()
       
        self.room_group_name = "global_chat"
        
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        messages = await self.get_recent_messages()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': messages
        }))
    
    
    async def disconnect(self, close_code):
       
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    
    async def receive(self, text_data):
        """Receive message from WebSocket (from client)"""
        data = json.loads(text_data)
        message_content = data.get('message', '')
        message_type = data.get('type', 'text')
        file_ids = data.get('file_ids', [])
        
        user = self.scope["user"]
        
        msg = await self.save_message(user, message_content, file_ids)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': msg['id'],
                'message': message_content,
                'username': user.username,
                'timestamp': msg['timestamp'],
                'message_type': message_type,
                'files': msg['files']
            }
        )
    
    
    async def chat_message(self, event):
        """Receive message from Redis broadcast, send to WebSocket (to client)"""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message_id': event['message_id'],
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
            'message_type': event.get('message_type', 'text'),
            'files': event.get('files', [])
        }))
    
    
    @database_sync_to_async
    def get_recent_messages(self, limit=50):
        """Load recent messages from database"""
        from chat.models import ChatMessage as Message
        
        messages = Message.objects.select_related('sender').prefetch_related('files').order_by('-timestamp')[:limit]
        
        return [
            {
                'id': msg.id,
                'message': msg.content,
                'username': msg.sender.username,
                'timestamp': msg.timestamp.isoformat(),
                'files': [
                    {
                        'id': f.id,
                        'url': f.file.url,
                        'type': f.file_type,
                        'size': f.file_size
                    } for f in msg.files.all()
                ]
            }
            for msg in reversed(messages) 
        ]
    
    
    @database_sync_to_async
    def save_message(self, user, content, file_ids):
        """Save message to database and link files"""
        from chat.models import ChatMessage as Message, MessageFile
        
        msg = Message.objects.create(
            sender=user,
            content=content
        )
        
        if file_ids:
            for file_id in file_ids:
                file = MessageFile.objects.filter(id=file_id)
                if file :
                    if file.user.id == user.id:
                        file.update(message=msg)
                
        
        files = MessageFile.objects.filter(message=msg)
        return {
            'id': msg.id,
            'timestamp': msg.timestamp.isoformat(),
            'files': [
                {
                    'id': f.id,
                    'url': f.file.url,
                    'type': f.file_type,
                    'size': f.file_size
                } for f in files
            ]
        }