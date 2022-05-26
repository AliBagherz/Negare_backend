from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chat.serializers import ChatSerializer, MessageSerializer, GetChatMessagesSerializer
from core.commonSchemas import not_found_schema, permission_denied_schema


class GetAllChatsView(APIView):
    @swagger_auto_schema(
        responses={
            200: ChatSerializer(many=True)
        },
    )
    def get(self, request):
        pass


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
        pass
