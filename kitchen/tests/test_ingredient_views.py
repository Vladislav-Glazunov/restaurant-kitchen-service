from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import Ingredient

INGREDIENT_LIST_URL = reverse("kitchen:ingredient-list")


class PublicIngredientTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(INGREDIENT_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIngredientTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testcook",
            password="test1234",
            years_of_experience=7,
        )
        self.client.login(
            username="testcook",
            password="test1234",
        )

    def test_retrieve_ingredient_list(self):
        Ingredient.objects.create(name="Tomato")
        response = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        ingredients = Ingredient.objects.all()
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(ingredients),
        )
        self.assertTemplateUsed(response, "kitchen/ingredient_list.html")
