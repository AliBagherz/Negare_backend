from channels.consumer import AsyncConsumer


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Connected', event)
