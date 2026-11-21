from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import Cook

COOK_LIST_URL = reverse("kitchen:cook-list")


class PublicCookTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(COOK_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCookTest(TestCase):
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

    def test_retrieve_cook_list(self):
        Cook.objects.create_user(
            username="testuser5",
            years_of_experience=7,
        )
        response = self.client.get(COOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cooks = Cook.objects.all()
        self.assertEqual(
            list(response.context["cook_list"]),
            list(cooks),
        )
        self.assertTemplateUsed(response, "kitchen/cook_list.html")


class CookSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser5",
            password="test1234",
            years_of_experience=7,
        )
        self.client.login(
            username="testuser5",
            password="test1234",
        )

    def test_search_by_username(self):
        Cook.objects.create_user(
            username="testChef_Barry",
            password="test1234",
            years_of_experience=7,
            first_name="Barry",
            last_name="Allen",
        )
        Cook.objects.create_user(
            username="testChef_Uryu",
            password="test1234",
            years_of_experience=7,
            first_name="Isida",
            last_name="Uryu",
        )
        response = self.client.get(
            reverse("kitchen:cook-list")
            + "?username=Barry"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Barry")
        self.assertNotContains(response, "Isida")
