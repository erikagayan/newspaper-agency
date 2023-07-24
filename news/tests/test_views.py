from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from news.models import Redactor, Topic, Newspaper


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

    def test_index_view(self):
        url = reverse("news:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "news/index.html")

        self.assertEqual(response.context["num_redactors"], Redactor.objects.count())
        self.assertEqual(response.context["num_newspapers"], Newspaper.objects.count())
        self.assertEqual(response.context["num_topics"], Topic.objects.count())

        self.assertEqual(self.client.session.get("num_visits"), 1)
        response = self.client.get(url)
        self.assertEqual(self.client.session.get("num_visits"), 2)

    def test_topic_list_view(self):

        Topic.objects.create(name="Topic 1")
        Topic.objects.create(name="Topic 2")

        url = reverse("news:topic-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "news/topic_list.html")
        self.assertContains(response, "Topic 1")
        self.assertContains(response, "Topic 2")

    def test_redactor_create_view(self):
        url = reverse("news:redactor-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "news/redactor_form.html")

    def test_redactor_create_submit(self):
        url = reverse("news:redactor-create")
        data = {
            "username": "new_redactor",
            "password1": "new_password",
            "password2": "new_password",
            "year_of_experience": 5,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        redactor = Redactor.objects.get(username="new_redactor")
        self.assertEqual(redactor.year_of_experience, 5)

    def test_redactor_detail_view(self):
        redactor = Redactor.objects.create_user(
            username="test_redactor",
            password="test_password",
            year_of_experience=8,
        )

        url = reverse("news:redactor-detail", args=[redactor.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/redactor_detail.html")
        self.assertContains(response, "test_redactor")
