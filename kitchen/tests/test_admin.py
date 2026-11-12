from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType, Ingredient, Dish


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            years_of_experience="5",
        )
        self.client.login(
            username="admin",
            password="admin123",
        )
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="testcook123",
            years_of_experience="5",
        )

    def test_dish_type_listed(self):
        self.dish_type = DishType.objects.create(name="testPizza")
        url = reverse("admin:kitchen_dishtype_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.dish_type.name)

    def test_ingredient_listed(self):
        self.ingredient = Ingredient.objects.create(name="testTomato")
        url = reverse("admin:kitchen_ingredient_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.ingredient.name)

    def test_dish_listed(self):
        self.dish_type = DishType.objects.create(name="testCurries")
        self.dish = Dish.objects.create(
            name="Pizza",
            dish_type=self.dish_type,
            price="150",
            description="test description",
        )
        url = reverse("admin:kitchen_dish_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.dish.name)

    def test_cook_years_of_experience_listed(self):
        url = reverse("admin:kitchen_cook_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.cook.years_of_experience)

    def test_years_of_experience_update(self):
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        response = self.client.get(url)
        self.assertContains(response, "years_of_experience")

    def test_cook_add_years_of_experience(self):
        url = reverse("admin:kitchen_cook_add")
        response = self.client.get(url)
        self.assertContains(response, "years_of_experience")
