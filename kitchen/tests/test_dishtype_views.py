from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType

DISHTYPE_LIST_URL = reverse("kitchen:dishtype-list")


class PublicDishTypeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(DISHTYPE_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTypeTest(TestCase):
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

    def test_retrieve_dishtype_list(self):
        DishType.objects.create(name="Curries")
        response = self.client.get(DISHTYPE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        dishtypes = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dishtypes),
        )
        self.assertTemplateUsed(response, "kitchen/dishtype_list.html")


class DishTypeSearchTest(TestCase):
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

    def test_search_by_dishtype(self):
        DishType.objects.create(name="Biscuits")
        DishType.objects.create(name="Pasta")
        response = self.client.get(
            reverse("kitchen:dishtype-list")
            + "?name=Biscuits"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Biscuits")
        self.assertNotContains(response, "Pasta")
