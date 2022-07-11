from django.core.files.images import ImageFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import AppUser
from core.models import Image
from userprofile.models import UserProfile, GENDER_CHOICES


class ArtTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # create user
        self.user = AppUser.objects.create_user(email='mail@mail.ir', username='test_user', password='12345678')
        self.user.is_active = True
        self.user.save()
        UserProfile.objects.create(user=self.user, gender='M', phone_number="09123456789")
        self.client.force_authenticate(self.user)

        self.other_user = AppUser.objects.create_user(email='mail2@mail.ir', username='test_user_2',
                                                      password='12345678')
        self.other_user.is_active = True
        self.other_user.save()
        UserProfile.objects.create(user=self.other_user)

        self.image = Image.objects.create(image=ImageFile(open("./test_images/test.png", "rb")))

    def test_get_profile(self):
        url = reverse("userprofile:profile", args=(self.user.id,))
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "09123456789")

    def test_update_profile(self):
        url = reverse("userprofile:profile", args=(self.user.id,))
        body = {
            "user_profile": {"phone_number": "09121111111"}
        }
        response = self.client.patch(url, body, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "09121111111")

    def test_follow_user(self):
        url = reverse("userprofile:follow-user", args=(self.other_user.id,))
        response = self.client.put(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "follow")
        self.assertContains(self.other_user.user_profile.followers.all(), self.user)
