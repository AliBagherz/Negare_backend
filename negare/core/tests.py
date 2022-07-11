from django.core.files.images import ImageFile
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from authentication.models import AppUser
from art.models import ArtTypeChoice, ArtPiece
from core.models import Image
from userprofile.models import UserProfile


class CoreTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create user
        self.user = AppUser.objects.create_user(username='test_user', password='12345678')
        self.user.is_active = True
        self.user.save()
        UserProfile.objects.create(user=self.user)
        self.client.force_authenticate(self.user)

        self.image = Image.objects.create(image=ImageFile(open("./test_images/test.png", "rb")))

    def test_homepage_successfully(self):
        url = reverse("home-page")
        data = {"page":1, "page_count":10}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_homepage_not_found_page(self):
        url = reverse("home-page")
        data = {"page":11, "page_count":10}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_homepage_not_found_page_error(self):
        url = reverse("home-page")
        data = {"page":11, "page_count":10}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.data['detail'].title(), "Invalid Page.")
