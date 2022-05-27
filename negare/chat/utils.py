from channels.db import database_sync_to_async
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from authentication.models import AppUser
from chat.coder_service import get_users_from_code
from chat.models import Chat, Message, MessageTypeChoices
from chat.serializers import MessageSerializer, ChatSerializer
from core.models import Image, Content


def get_sender_index(chat_code: str, sender_id: int) -> int:
    users = get_users_from_code(chat_code)
    return users.index(sender_id)


@database_sync_to_async
def add_message_to_chat(data: dict, user: AppUser, chat_code: str) -> dict:
    chats = Chat.objects.filter(chat_code=chat_code)

    if chats.count():
        chat = chats.first()
    else:
        chat = Chat(chat_code=chat_code)
        users = get_users_from_code(chat_code)
        user1 = get_object_or_404(AppUser.objects.all(), pk=users[0])
        user2 = get_object_or_404(AppUser.objects.all(), pk=users[1])
        chat.users.add(user1)
        chat.users.add(user2)
        chat.save()

    message = Message(chat=chat)
    message.type = data['type']
    message.sender_index = get_sender_index(chat_code, user.id)

    if data['type'] == MessageTypeChoices.TEXT:
        message.text = data['message']
    elif data['type'] == MessageTypeChoices.PICTURE:
        image = get_object_or_404(Image.objects.all(), pk=int(data['message']))
        message.image = image
    else:
        content = get_object_or_404(Content.objects.all(), pk=int(data['message']))
        message.content = content

    message.save()
    data['id'] = message.id

    return dict(data)


def get_all_chats(user: AppUser) -> list:
    chats = Chat.objects.filter(users=user).order_by("-updated_at")
    return ChatSerializer(instance=chats, many=True, context={"user": user}).data


def get_all_chat_messages(chat_code: str, user: AppUser, request: Request) -> list:
    chat = get_object_or_404(Chat.objects.all(), chat_code=chat_code)
    messages = Message.objects.filter(chat=chat).order_by("-created_at")
    return MessageSerializer(messages, many=True, context={"user": user, "request": request}).data
