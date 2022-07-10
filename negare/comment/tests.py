from django.core.files.images import ImageFile
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from authentication.models import AppUser
from art.models import ArtTypeChoice, ArtPiece
from core.models import Image
from userprofile.models import UserProfile


class CommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create user
        self.user = AppUser.objects.create_user(username='test_user', password='12345678')
        self.user.is_active = True
        self.user.save()
        UserProfile.objects.create(user=self.user)
        self.client.force_authenticate(self.user)

        self.image = Image.objects.create(image=ImageFile(open("./test_images/test.png", "rb")))

        self.art_piece1 = ArtPiece.objects.create(cover_id=self.image.id, type="P", owner_id=self.user.id)
        self.art_piece2 = ArtPiece.objects.create(cover_id=self.image.id, type="V", owner_id=self.user.id)

        self.client.post(reverse("comment:add-comment", args=(self.art_piece1.id,)), {"content": "so nice"}, format="json")
        self.client.post(reverse("comment:add-comment", args=(self.art_piece1.id,)), {"content": "greatest pic ive ever seen"}, format="json")
        self.client.post(reverse("comment:add-comment", args=(self.art_piece1.id,)), {"content": "beautiful"}, format="json")

    def test_add_comment_successfully(self):
        url = reverse("comment:add-comment", args=(self.art_piece1.id,))
        data = {"content": "nice"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_add_comment_successfully_content(self):
        url = reverse("comment:add-comment", args=(self.art_piece1.id,))
        data = {"content": "nice"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.data['content'], "nice")

    def test_add_comment_successfully_user(self):
        url = reverse("comment:add-comment", args=(self.art_piece1.id,))
        data = {"content": "nice"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.data['writer']['id'], self.user.id)

    def test_add_comment_art_piece_not_found(self):
        url = reverse("comment:add-comment", args=(5,))
        data = {"content": "nice"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_add_comment_art_piece_not_found_detail(self):
        url = reverse("comment:add-comment", args=(5,))
        data = {"content": "nice"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.data['detail'].title(), "Not Found.")

    def test_add_comment_invalid_data(self):
        url = reverse("comment:add-comment", args=(self.art_piece1.id,))
        data = {"content": None}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_all_comments(self):
        url = reverse("comment:all-comments", args=(self.art_piece1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_all_comments_contents(self):
        url = reverse("comment:all-comments", args=(self.art_piece1.id,))
        response = self.client.get(url)
        self.assertEqual(response.data[0]['content'], "so nice")
        self.assertEqual(response.data[1]['content'], "greatest pic ive ever seen")
        self.assertEqual(response.data[2]['content'], "beautiful")

    def test_all_comments_writer(self):
        url = reverse("comment:all-comments", args=(self.art_piece1.id,))
        response = self.client.get(url)
        self.assertEqual(response.data[0]['writer']['id'], self.user.id)
