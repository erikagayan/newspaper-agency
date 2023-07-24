from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from news.forms import RedactorCreationForm, NewspaperForm


class RedactorCreationFormTest(TestCase):
    def test_clean_years_of_experience_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "year_of_experience": 10,
            "first_name": "John",
            "last_name": "Doe"
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class NewspaperFormTest(TestCase):
    def test_clean_published_date_future(self):
        form_data = {
            "title": "Test Newspaper",
            "publishers": [],
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("published_date", form.errors)
