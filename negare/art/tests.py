from django.core.files.images import ImageFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import AppUser

from art.models import ArtTypeChoice, ArtPiece
from core.models import Image
from userprofile.models import UserProfile


class ArtTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # create user
        self.user = AppUser.objects.create_user(email='mail@mail.ir', username='test_user', password='12345678')
        self.user.is_active = True
        self.user.save()
        UserProfile.objects.create(user=self.user)
        self.client.force_authenticate(self.user)

        self.other_user = AppUser.objects.create_user(email='mail2@mail.ir', username='test_user_2', password='12345678')
        self.other_user.is_active = True
        self.other_user.save()
        UserProfile.objects.create(user=self.other_user)

        self.image = Image.objects.create(image=ImageFile(open("./test_images/test.png", "rb")))

    def test_create_art_piece_successfully(self):
        url = reverse("art:art-piece-cover")
        data = {"cover": self.image.id, "type": ArtTypeChoice.PICTURE}
        response = self.client.post(url, data, format="json")
        self.assertContains(response, "art_piece_id")
        self.assertEqual(response.status_code, 200)

    def test_create_art_piece_wrong_type(self):
        url = reverse("art:art-piece-cover")
        data = {"cover": self.image.id, "type": "Q"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_create_art_piece_image_not_found(self):
        url = reverse("art:art-piece-cover")
        data = {"cover": 205, "type": "P"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_create_art_piece_video_type(self):
        url = reverse("art:art-piece-cover")
        data = {"cover": self.image.id, "type": "V"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "art_piece_id")

    def test_add_detail_to_created_art_piece(self):
        art_piece = ArtPiece.objects.create(cover_id=self.image.id, type="P", owner_id=self.user.id)
        data = {"price": 1000, "description": None, "title": None}
        url = reverse("art:art-piece", args=(art_piece.id,))
        response = self.client.put(url, data, format="json")
        art_piece.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(art_piece.price, 1000)
        self.assertEqual(art_piece.description, '')

    def test_add_detail_to_art_piece_invalid_data(self):
        art_piece = ArtPiece.objects.create(cover_id=self.image.id, type="P", owner_id=self.user.id)
        data = {"price": "Test", "description": None, "title": None}
        url = reverse("art:art-piece", args=(art_piece.id,))
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 406)

    def test_get_art_piece_detail(self):
        art_piece = ArtPiece.objects.create(cover_id=self.image.id, type="V", owner_id=self.user.id)
        url = reverse("art:art-piece", args=(art_piece.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['type'], "video")

    def test_like_art_piece(self):
        art_piece = ArtPiece.objects.create(cover_id=self.image.id, type="V", owner_id=self.user.id)
        url = reverse("art:like-art-piece", args=(art_piece.id,))
        response = self.client.put(url)
        self.assertEqual(response.data['like'], True)
        self.assertEqual(response.status_code, 200)

    def test_unlike_art_piece(self):
        art_piece = ArtPiece.objects.create(cover_id=self.image.id, type="V", owner_id=self.user.id)
        url = reverse("art:like-art-piece", args=(art_piece.id,))
        art_piece.liked_users.add(self.user)
        response = self.client.put(url)
        self.assertEqual(response.data['like'], False)
        self.assertEqual(response.status_code, 200)

    def test_like_art_piece_not_found(self):
        url = reverse("art:like-art-piece", args=(23,))
        response = self.client.put(url)
        self.assertEqual(response.status_code, 404)

    def test_like_art_piece_not_allowed_method(self):
        art_piece = ArtPiece.objects.create(cover_id=self.image.id, type="V", owner_id=self.user.id)
        url = reverse("art:like-art-piece", args=(art_piece.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_explore_get_result(self):
        art_piece = ArtPiece.objects.create(
            cover_id=self.image.id,
            type="V",
            owner_id=self.other_user.id,
            title="art_piece_title"
        )
        art_piece.liked_users.add(self.user)
        art_piece.save()
        url = reverse("art:explore")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "art_piece_title")
        
    def test_search_art_piece(self):
        ArtPiece.objects.create(
            cover_id=self.image.id,
            type="V",
            owner_id=self.other_user.id,
            title="art_piece_title"
        )
        url = reverse("art:search")
        params = {"query": "art_piece_title"}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "art_piece_title")

    def test_gallery_view(self):
        ArtPiece.objects.create(
            cover_id=self.image.id,
            type="V",
            owner_id=self.other_user.id,
            title="art_piece_title"
        )
        url = reverse("art:gallery", args=(self.other_user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "art_piece_title")
