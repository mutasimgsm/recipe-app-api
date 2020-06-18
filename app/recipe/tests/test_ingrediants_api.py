from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingrediant

from recipe.serializers import IngrediantSerializer

INGREDIANTS_URL = reverse('recipe:ingrediant-list')


class PublicIngrediantsApiTests(TestCase):
    """Test the publicly available ingrediants API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test logiin is required to access the endpoint"""
        res = self.client.get(INGREDIANTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngrediantsApiTests(TestCase):
    """test the private ingrediant API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@etir.com',
            'testpass',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingreidant_list(self):
        """Test retrieving a  list of ingrediant"""
        Ingrediant.objects.create(user=self.user, name='Kale')
        Ingrediant.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIANTS_URL)

        ingrediants = Ingrediant.objects.all().order_by('-name')
        serializer = IngrediantSerializer(ingrediants, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingrediant_limited_to_user(self):
        """Test that ingrediant for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@etir.com',
            'testpass'
        )
        Ingrediant.objects.create(user=user2, name='Vineger')
        ingrediant = Ingrediant.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGREDIANTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingrediant.name)
