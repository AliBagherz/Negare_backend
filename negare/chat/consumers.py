import json

from channels.consumer import AsyncConsumer


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Connected', event)
        await self.send(
            {
                'type': 'websocket.accept'
            }
        )

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        _type = received_data.get('type')

        if not _type:
            return False

        # ToDo: handle message models

        await self.send(
            {
                'type': 'websocket.send',
                'text': json.dumps({})
            }
        )

    async def websocket_disconnect(self, event):
        print('disconnect', event)
