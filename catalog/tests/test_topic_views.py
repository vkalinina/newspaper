# flake8: noqa: E731

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Topic

TOPIC_URL = reverse("catalog:topic-list")
TOPIC_CREATE_URL = reverse("catalog:topic-create")
TOPIC_UPDATE_URL = lambda pk: reverse(
    "catalog:topic-update", args=[pk]
)
TOPIC_DELETE_URL = lambda pk: reverse(
    "catalog:topic-delete", args=[pk]
)


class PublicTopicTests(TestCase):
    def test_login_required(self):
        response = self.client.get(TOPIC_URL)
        self.assertNotEqual(response.status_code, 200)

        response = self.client.get(TOPIC_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTopicTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1223",
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(
            name="Test Topic",
        )

    def test_search_topic_by_username(self):
        """Test searching topic by name"""
        Topic.objects.create(
            name="New Topic",
        )
        response = self.client.get(
            TOPIC_URL,
            {"name": "Test Topic"}
        )
        self.assertEqual(
            len(response.context["topic_list"]),
            1
        )
        self.assertEqual(
            response.context["topic_list"][0],
            self.topic
        )

    def test_retrieve_topic(self):
        Topic.objects.create(name="Test Topic 1")
        Topic.objects.create(name="Test Topic 2")
        response = self.client.get(TOPIC_URL)
        self.assertEqual(response.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(len(topics), 3)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics)
        )
        self.assertTemplateUsed(
            response,
            "catalog/topic_list.html"
        )

    def test_create_topic(self):
        from_data = {
            "name": "New Topic",
        }
        response = self.client.post(TOPIC_CREATE_URL, from_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Topic.objects.filter(name="New Topic").exists()
        )

    def test_update_topic(self):
        update_url = TOPIC_UPDATE_URL(self.topic.id)
        form_data = {
            "name": "Updated Topic",
        }
        response = self.client.post(update_url, data=form_data)
        self.topic.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(self.topic.name, "Updated Topic")

    def test_delete_topic(self):
        delete_url = TOPIC_DELETE_URL(self.topic.id)
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(
            Topic.objects.filter(id=self.topic.id).exists()
        )
