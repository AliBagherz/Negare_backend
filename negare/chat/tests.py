from django.core.files.images import ImageFile
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from authentication.models import AppUser
from art.models import ArtTypeChoice, ArtPiece
from chat.models import Chat, Message
from core.models import Image
from userprofile.models import UserProfile


class ChatTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create user
        self.user1 = AppUser.objects.create_user(email='negare_test_user@mail.com', password='12345678',
                                                 username="negare_test_user")
        self.user1.is_active = True
        self.user1.is_verified = True
        self.user1.save()

        # create temporary users
        self.user2 = AppUser.objects.create_user(email='negare_test_user2@mail.com', password='12345678',
                                                 username="negare_test_user2")
        self.user2.is_verified = False
        self.user2.is_active = True
        self.user2.save()

        # create chat
        users = []
        users.append(self.user1)
        users.append(self.user2)
        self.chat = Chat.objects.create(chat_code='ABCD', users=users)

        # create message
        self.message = Message.objects.create()
        #

        UserProfile.objects.create(user=self.user1)
        UserProfile.objects.create(user=self.user2)
        self.client.force_authenticate(self.user1)

    def test_all_chats_successfully(self):
        url = reverse("chat:all-chats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_all_chats_successfully_chat_code(self):
        url = reverse("chat:all-chats")
        response = self.client.get(url)
        self.assertEqual(response.data[0]['chat_code'], self.chat.chat_code)

    def test_all_chats_successfully_user_id(self):
        url = reverse("chat:all-chats")
        response = self.client.get(url)
        self.assertEqual(response.data[0]['user']['id'], self.user2.id)

    def test_all_chat_messages_successfully(self):
        url = reverse("chat:all-messages")
        data = {"chat_code": self.chat.chat_code}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_all_chat_messages_successfully_message(self):
        url = reverse("chat:all-messages")
        data = {"chat_code": self.chat.chat_code}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data[0]['id'], self.message.id)

    def test_all_chat_messages_not_found(self):
        url = reverse("chat:all-messages")
        data = {"chat_code": "QWERTY"}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_all_chat_messages_not_found_detail(self):
        url = reverse("chat:all-messages")
        data = {"chat_code": "QWERTY"}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data['detail'].title(), "Not Found.")

    def test_all_chat_message_access_denied(self):
        return True

