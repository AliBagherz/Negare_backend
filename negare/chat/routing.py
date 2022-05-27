from django.urls import path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('socket/chat/<str:chat_code>/', ChatConsumer.as_asgi())
]
