import json

from channels.consumer import AsyncConsumer

from chat.serializers import NewMessageSerializer
from chat.utils import add_message_to_chat


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send(
            {
                'type': 'websocket.accept'
            }
        )

    async def websocket_receive(self, event):
        received_data = json.loads(event['text'])
        serializer = NewMessageSerializer(data=received_data)

        if serializer.is_valid():
            response = add_message_to_chat(serializer.validated_data)

            await self.send(
                {
                    'type': 'websocket.send',
                    'text': json.dumps(response)
                }
            )
        else:
            await self.send(
                {
                    'type': 'websocket.send',
                    'text': json.dumps(
                        {
                            "success": False,
                            "detail": "invalid data"
                        }
                    )
                }
            )


    async def websocket_disconnect(self, event):
        print('disconnect', event)
