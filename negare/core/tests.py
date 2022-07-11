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
