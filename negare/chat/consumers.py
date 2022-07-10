import json
from urllib.parse import parse_qs
from channels.db import database_sync_to_async

from channels.consumer import AsyncConsumer

from authentication.models import AppUser
from chat.serializers import NewMessageSerializer
from chat.utils import add_message_to_chat
from core.utils import get_user_id_from_jwt_token


def get_user_id_from_token(scope):
    token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
    return get_user_id_from_jwt_token(token)


class ChatConsumer(AsyncConsumer):
    def __init__(self):
        self.chat_code = None
        self.user = None

    async def websocket_connect(self, event):
        print("connect1", event)

        self.user = await self.get_user_object(get_user_id_from_token(self.scope))
        self.chat_code = (self.scope['path']).split('/')[3]
        await self.channel_layer.group_add(
            self.chat_code,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("received1", event)
        received_data = json.loads(event['text'])
        serializer = NewMessageSerializer(data=received_data)

        if serializer.is_valid():
            response = await add_message_to_chat(serializer.validated_data, self.user, self.chat_code)

            await self.channel_layer.group_send(
                self.chat_code,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )
        else:
            await self.channel_layer.group_send(
                self.chat_code,
                {
                    'type': 'chat_message',
                    'text': json.dumps(
                        {
                            "success": False,
                            "detail": "invalid data"
                        }
                    )
                }
            )

    async def websocket_disconnect(self, event):
        print('disconnect1', event)

    async def chat_message(self, event):
        await self.send(
            {
                'type': 'websocket.send',
                'text': event['text']
            }
        )

    @database_sync_to_async
    def get_user_object(self, user_id):
        return AppUser.objects.get(pk=user_id)
