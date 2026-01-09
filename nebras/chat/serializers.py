from rest_framework import serializers
from .models import ChatMessage, MessageFile

class MessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFile
        fields = ['id', 'message', 'file', 'user']
        read_only_fields = ['message', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_file(self, value):
        # 10MB = 10 * 1024 * 1024 bytes
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size exceeds 10MB limit.")
        return value

class ChatMessageSerializer(serializers.ModelSerializer):
    files = MessageFileSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'username', 'message', 'files', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
