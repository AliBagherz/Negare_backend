from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.schemas import many_chat_schema
from chat.serializers import MessageSerializer, GetChatMessagesSerializer
from chat.utils import get_all_chats, get_all_chat_messages
from core.commonResponses import invalidDataResponse
from core.commonSchemas import not_found_schema, permission_denied_schema


class GetAllChatsView(APIView):
    @swagger_auto_schema(
        responses={
            200: many_chat_schema()
        },
    )
    def get(self, request):
        chats = get_all_chats(request.user, request)
        return Response(chats, status=200)


class GetAllChatMessages(APIView):
    @swagger_auto_schema(
        query_serializer=GetChatMessagesSerializer,
        responses={
            200: MessageSerializer(many=True),
            404: not_found_schema(),
            403: permission_denied_schema()
        },
    )
    def get(self, request):
        serializer = GetChatMessagesSerializer(data=request.GET)

        if not serializer.is_valid():
            return invalidDataResponse()

        chat_code = serializer.validated_data['chat_code']

        messages = get_all_chat_messages(chat_code, request.user, request)

        return Response(messages, status=200)
