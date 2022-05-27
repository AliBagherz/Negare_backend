import os

from django.db import models
from rest_framework import serializers

from authentication.models import AppUser
from authentication.serializers import UserSerializer
from chat.coder_service import get_users_from_code
from chat.models import Chat, Message, MessageTypeChoices
from core.serializers import ImageSerializer


class ChatSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    @staticmethod
    def get_last_message(chat):
        last_message = chat.messages.last()
        return str(last_message)

    def get_user(self, chat):
        request_user = self.context['user']
        users = get_users_from_code(chat.chat_code)
        _id = users[1] if users[0] == request_user.id else users[0]
        chat_user = AppUser.objects.get(pk=_id)
        return UserSerializer(instance=chat_user).data

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
    is_user_sender = serializers.SerializerMethodField()

    @staticmethod
    def get_type(message):
        return message.get_type_display()

    def get_content(self, message):
        if message.type == MessageTypeChoices.TEXT:
            return message.text
        if message.type == MessageTypeChoices.PICTURE:
            url = self.context['request'].build_absolute_uri()
            base_index = url.index('//')
            slash_index = url.index('/', base_index + 2)
            base_url = url[0:slash_index]
            return base_url + ImageSerializer(message.image).data['image']['full_size']
        if not message.content:
            return ""
        return message.content.file.url

    def get_is_user_sender(self, message):
        request_user = self.context['user']
        users = get_users_from_code(message.chat.chat_code)
        sender_id = users[message.sender_index]
        return request_user.id == sender_id

    class Meta:
        model = Message
        fields = [
            'id',
            'type',
            'is_user_sender',
            'content',
            'updated_at',
            'created_at'
        ]


class GetChatMessagesSerializer(serializers.Serializer):
    chat_code = serializers.CharField(max_length=200)


class NewMessageSerializer(serializers.Serializer):
    class TypeChoices(models.TextChoices):
        P = "P"
        V = "V"
        M = "M"
        T = 'T'

    type = serializers.ChoiceField(TypeChoices, default=TypeChoices.T)
    message = serializers.CharField()
