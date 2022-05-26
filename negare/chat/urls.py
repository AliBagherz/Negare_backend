from django.urls import path

from chat.views import GetAllChatsView, GetAllChatMessages

app_name = "chat"
urlpatterns = [
    path("get-all-chats/", GetAllChatsView.as_view(), name='all-chats'),
    path("get-all-chat-messages/", GetAllChatMessages.as_view(), name='all-messages')
]
