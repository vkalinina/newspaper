from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import Topic, Article


class ModelTests(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="Test Topic")
        self.assertEqual(
            str(topic),
            f"{topic.name}"
        )

    def test_redactor_str(self):
        redactor = get_user_model().objects.create(
            username="Test redactor",
            first_name="test first",
            last_name="test last",
            password="test123",
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username} ({redactor.first_name} {redactor.last_name})"
        )

    def test_article_str(self):
        topic = Topic.objects.create(name="Test Topic")
        article = Article.objects.create(
            title="Test Title",
            topic=topic,
            content="Test Content",
            published_date=datetime.now()
        )
        self.assertEqual(str(article), article.title)

    def test_create_redactor_with_license(self):
        username = "Test redactor"
        years_of_experience = "5"
        password = "test123"
        redactor = get_user_model().objects.create_user(
            username=username,
            years_of_experience=years_of_experience,
            password=password,
        )
        self.assertEqual(redactor.username, username)
        self.assertEqual(redactor.years_of_experience, years_of_experience)
        self.assertTrue(redactor.check_password(password))
