from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType, Dish

DISH_LIST_URL = reverse("kitchen:dish-list")


class PublicDishTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(DISH_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTest(TestCase):
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

    def test_retrieve_dish_list(self):
        dish_type = DishType.objects.create(
            name="Pasta",
        )
        Dish.objects.create(
            name="Fettuccine",
            dish_type=dish_type,
            description="test description",
            price=130,
        )
        response = self.client.get(DISH_LIST_URL)
        self.assertEqual(response.status_code, 200)
        dish = Dish.objects.all()
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dish),
        )
        self.assertTemplateUsed(response, "kitchen/dish_list.html")


class DishSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser7",
            password="test1234",
            years_of_experience=7,
        )
        self.client.login(
            username="testuser7",
            password="test1234",
        )

    def test_search_by_dish(self):
        dish_type = DishType.objects.create(
            name="Cherry",
        )
        Dish.objects.create(
            name="Varenyky",
            dish_type=dish_type,
            description="test description",
            price=200,
        )
        Dish.objects.create(
            name="Stuffed pastry",
            dish_type=dish_type,
            description="test description",
            price=50,
        )
        response = self.client.get(
            reverse("kitchen:dish-list")
            + "?name=Varenyky"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Varenyky")
        self.assertNotContains(response, "Stuffed pastry")
