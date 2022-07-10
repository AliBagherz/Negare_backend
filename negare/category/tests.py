from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from authentication.models import AppUser
from category.models import Category


class CategoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create user
        self.user = AppUser.objects.create_user(username='test_user', password='12345678')
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(self.user)

        #create categories
        Category.objects.create(name="music")
        Category.objects.create(name="concert")
        Category.objects.create(name="accessories")
        Category.objects.create(name="paint")

    def test_category_get_all_response_code(self):
        url = reverse("category:get-all-categories")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        url = reverse("category:get-all-categories")
        response = self.client.get(url)
        self.assertEqual(response.data[0]['name'], 'music')

    def test_category_names(self):
        url = reverse("category:get-all-categories")
        response = self.client.get(url)
        self.assertEqual(response.data[0]['name'], 'music')
        self.assertEqual(response.data[1]['name'], 'concert')
        self.assertEqual(response.data[2]['name'], 'accessories')
        self.assertEqual(response.data[3]['name'], 'paint')

    def test_category_get_all_length(self):
        url = reverse("category:get-all-categories")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 4)

