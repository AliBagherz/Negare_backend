from rest_framework import serializers

from authentication.serializers import UserSerializer
from chat.models import Chat, Message, MessageTypeChoices
from core.serializers import ImageSerializer


class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    last_message = serializers.SerializerMethodField()

    @staticmethod
    def get_last_message(chat):
        last_message = chat.messages.last()
        return str(last_message)

    class Meta:
        model = Chat
        fields = [
            'id',
            'chat_code',
            'user',
            'last_message',
            'updated_at',
            'created_at'
        ]


class MessageSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    @staticmethod
    def get_type(message):
        return message.get_type_display()

    @staticmethod
    def get_content(message):
        if message.type == MessageTypeChoices.TEXT:
            return message.text
        if message.type == MessageTypeChoices.PICTURE:
            return ImageSerializer(message.image)
        if not message.content:
            return ""
        return message.content.url

    class Meta:
        model = Message
        fields = [
            'id',
            'type',
            'content',
            'updated_at',
            'created_at'
        ]


class GetChatMessagesSerializer(serializers.Serializer):
    chat_code = serializers.CharField(max_length=200)
