from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from authentication.models import AppUser


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create temporary users
        self.user1 = AppUser.objects.create_user(email='negare_test_user@mail.com', password='12345678',
                                                 username="negare_test_user")
        self.user1.is_active = True
        self.user1.is_verified = True
        self.user1.save()

        self.user2 = AppUser.objects.create_user(email='negare_test_user2@mail.com', password='12345678',
                                                 username="negare_test_user2")
        self.user2.is_verified = False
        self.user2.is_active = True
        self.user2.save()

    def test_register_successfully(self):
        url = reverse("authentication:register")
        data = {"email": "testtest@gmail.com", "password": "12345678", "first_name": "test-first",
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_register_invalid_data_email(self):
        url = reverse("authentication:register")
        data = {"email": "test-email", "password": "12345678", "first_name": "test-first",
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_null_email(self):
        url = reverse("authentication:register")
        data = {"email": None, "password": "12345678", "first_name": "test-first",
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_null_password(self):
        url = reverse("authentication:register")
        data = {"email": "testtest@gmail.com", "password": None, "first_name": "test-first",
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_null_first_name(self):
        url = reverse("authentication:register")
        data = {"email": "testtest@gmail.com", "password": "12345678", "first_name": None,
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_null_last_name(self):
        url = reverse("authentication:register")
        data = {"email": "testtest@gmail.com", "password": "12345678", "first_name": "test-first",
                "last_name": None}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_login_successfully(self):
        url = reverse("authentication:login")
        data = {"email": "negare_test_user@mail.com", "password": "12345678"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_login_not_verified(self):
        url = reverse("authentication:login")
        data = {"email": "negare_test_user2@mail.com", "password": "12345678"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_login_un_authorized_invalid_email(self):
        url = reverse("authentication:login")
        data = {"email": "negare_test@mail.com", "password": "12345678"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_login_un_authorized_invalid_password(self):
        url = reverse("authentication:login")
        data = {"email": "negare_test_user@mail.com", "password": "1234"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_login_un_authorized_null_email(self):
        url = reverse("authentication:login")
        data = {"email": None, "password": "1234"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_login_un_authorized_null_password(self):
        url = reverse("authentication:login")
        data = {"email": "negare_test_user@mail.com", "password": None}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
