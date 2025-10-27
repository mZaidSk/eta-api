from rest_framework import serializers
from .models import Conversation, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'messages', 'message_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()


class ConversationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing conversations without messages"""
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'message_count', 'last_message']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'role': last_msg.role,
                'content': last_msg.content[:100] + '...' if len(last_msg.content) > 100 else last_msg.content,
                'created_at': last_msg.created_at
            }
        return None
