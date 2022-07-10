from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from authentication.models import AppUser


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create temporary users
        self.user = AppUser.objects.create_user(username='negare_test_user@mail.com', password='12345678')
        self.user.is_active = True
        self.user.save()

        self.user = AppUser.objects.create_user(username='negare_test_user2@mail.com', password='12345678')
        self.user.is_active = False
        self.user.save()

    def test_register_successfully(self):
        url = reverse("auth:register")
        data = {"email": "testtest@gmail.com", "password": "12345678", "first_name": "test-first",
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_register_invalid_data_email(self):
        url = reverse("auth:register")
        data = {"email": "test-email", "password": "12345678", "first_name": "test-first",
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_invalid_data_password(self):
        url = reverse("auth:register")
        data = {"email": "testtest@gmail.com", "password": 123456, "first_name": "test-first",
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_invalid_data_first_name(self):
        url = reverse("auth:register")
        data = {"email": "testtest@gmail.com", "password": "12345678", "first_name": 1234,
                "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_invalid_data_last_name(self):
        url = reverse("auth:register")
        data = {"email": "testtest@gmail.com", "password": "12345678", "first_name": "test-first",
                "last_name": 1234}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_null_email(self):
        url = reverse("auth:register")
        data = {"email": None, "password":"12345678", "first_name": "test-first",
        "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_null_password(self):
        url = reverse("auth:register")
        data = {"email": "testtest@gmail.com", "password":None, "first_name": "test-first",
        "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_null_first_name(self):
        url = reverse("auth:register")
        data = {"email": "testtest@gmail.com", "password":"12345678", "first_name": None,
        "last_name": "test-last"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_register_null_last_name(self):
        url = reverse("auth:register")
        data = {"email": "testtest@gmail.com", "password":"12345678", "first_name": "test-first",
        "last_name": None}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_login_successfully(self):
        url = reverse("auth:login")
        data = {"username": "negare_test_user@mail.com", "password": "12345678"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_login_not_verified(self):
        url = reverse("auth:login")
        data = {"username": "negare_test_user2@mail.com", "password": "12345678"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_login_un_authorized_invalid_email(self):
        url = reverse("auth:login")
        data = {"username": "negare_test@mail.com", "password": "12345678"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_login_un_authorized_invalid_password(self):
        url = reverse("auth:login")
        data = {"username": "negare_test_user@mail.com", "password": "1234"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_login_un_authorized_null_email(self):
        url = reverse("auth:login")
        data = {"username": None, "password": "1234"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_login_un_authorized_null_password(self):
        url = reverse("auth:login")
        data = {"username": "negare_test_user@mail.com", "password": None}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 403)
