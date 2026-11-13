from django.test import TestCase

from kitchen.forms import CookCreationForm, CookUpdateForm


class FormsTests(TestCase):
    def test_cook_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 5,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_cook_creation_form_negative_experience(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": -5,
        }
        form = CookCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_cook_update_form_is_valid(self):
        form_data = {
            "years_of_experience": 5,
        }
        form = CookUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_cook_update_form_negative_experience(self):
        form_data = {
            "years_of_experience": -5,
        }
        form = CookUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
