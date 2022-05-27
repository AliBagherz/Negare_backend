from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from authentication.models import AppUser
from chat.coder_service import get_users_from_code
from chat.models import Chat, Message, MessageTypeChoices
from chat.serializers import MessageSerializer, ChatSerializer
from core.commonResponses import errorResponse
from core.models import Image, Content


def get_sender_index(data: dict) -> int:
    users = get_users_from_code(data['chat_code'])
    return users.index(data['sender_id'])


def add_message_to_chat(data: dict) -> dict:
    chat = get_object_or_404(Chat.objects.all(), chat_code=data['chat_code'])

    if not chat:
        return errorResponse(detail="chat not found")

    message = Message(chat=chat)
    message.type = data['type']
    message.sender_index = get_sender_index(data)

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

    return data


def get_all_chats(user: AppUser) -> list:
    chats = Chat.objects.filter(users=user).order_by("-updated_at")
    return ChatSerializer(instance=chats, many=True, context={"user": user}).data


def get_all_chat_messages(chat_code: str, user: AppUser, request: Request) -> list:
    chat = get_object_or_404(Chat.objects.all(), chat_code=chat_code)
    messages = Message.objects.filter(chat=chat).order_by("-created_at")
    return MessageSerializer(messages, many=True, context={"user": user, "request": request}).data
