from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Ingredient, Dish


class ModelTest(TestCase):
    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="test",
            password="test123",
            years_of_experience="5",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(cook),
            f"{cook.username} {cook.first_name} {cook.last_name}"
        )

    def test_cook_get_absolute_url(self):
        cook = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            years_of_experience="6",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(cook.get_absolute_url(), f"/cooks/{cook.pk}/")

    def test_dishtype_str(self):
        dishtype = DishType.objects.create(name="testCakes")
        self.assertEqual(str(dishtype), dishtype.name)

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(name="testTomato")
        self.assertEqual(str(ingredient), ingredient.name)

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="Pizza")
        dish = Dish.objects.create(
            name="test Pizza",
            dish_type=dish_type,
            description="test description",
            price="100",
        )
        self.assertEqual(str(dish), f"{dish.name} |{dish.dish_type}|")
