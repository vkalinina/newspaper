# flake8: noqa: E731
import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Article, Topic

ARTICLE_LIST_URL = reverse("catalog:article-list")
ARTICLE_DETAIL_URL = lambda pk: reverse("catalog:article-detail", args=[pk])
ARTICLE_CREATE_URL = reverse("catalog:article-create")
ARTICLE_UPDATE_URL = lambda pk: reverse("catalog:article-update", args=[pk])
ARTICLE_DELETE_URL = lambda pk: reverse("catalog:article-delete", args=[pk])


class PublicArticleTests(TestCase):
    def test_login_required(self):
        """Test that login is required for accessing the car list view"""
        response = self.client.get(ARTICLE_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateArticleTests(TestCase):
    def setUp(self):
        """Set up a logged-in user and sample data"""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

        self.topic = Topic.objects.create(
            name="Hot news"
        )
        self.redactor = get_user_model().objects.create_user(
            username="redactor1",
            password="password123",
            years_of_experience="45",
        )
        self.article = Article.objects.create(
            title="Render - free hosting",
            topic=self.topic,
            published_date=datetime.date.today(),
            content="This is the content",
        )
        self.article.redactors.add(self.redactor)

    def test_retrieve_article_list(self):
        """Test retrieving the article list"""
        response = self.client.get(ARTICLE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.article, response.context["article_list"])
        self.assertTemplateUsed(response, "catalog/article_list.html")

    def test_search_article_by_title(self):
        """Test searching articles by title"""
        Article.objects.create(
            title="Camry",
            topic=self.topic,
            published_date=datetime.date.today(),
            content="This is the content",
        )
        response = self.client.get(ARTICLE_LIST_URL, {"title": "Corolla"})
        self.assertEqual(len(response.context["article_list"]), 2)
        self.assertEqual(response.context["article_list"][0], self.article)

    def test_retrieve_article_detail(self):
        """Test retrieving the article detail"""
        url = ARTICLE_DETAIL_URL(self.article.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["article"], self.article)
        self.assertTemplateUsed(response, "catalog/article_detail.html")

    def test_create_article(self):
        """Test creating a new article"""
        from_data = {
            "title": "Prius",
            "topic": self.topic.id,
            "content": "This is the content",
            "published_date": datetime.date.today(),
            "redactors": [self.redactor.id]
        }
        response = self.client.post(ARTICLE_CREATE_URL, data=from_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Article.objects.filter(title="Prius").exists())
        article = Article.objects.get(title="Prius")
        self.assertEqual(article.topic, self.topic)
        self.assertIn(self.redactor, article.redactors.all())

    def test_update_article(self):
        """Test updating an existing article"""
        new_redactor = get_user_model().objects.create_user(
            username="redactor2",
            password="password123",
            years_of_experience="7",
        )
        from_data = {
            "title": "Corolla Updated",
            "topic": self.topic.id,
            "content": "This is the content",
            "published_date": datetime.date.today(),
            "redactors": [self.redactor.id, new_redactor.id]
        }
        url = ARTICLE_UPDATE_URL(self.article.id)
        response = self.client.post(url, data=from_data)
        self.article.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.article.title, "Corolla Updated")
        self.assertIn(new_redactor, self.article.redactors.all())

    def test_delete_article(self):
        """Test deleting a article"""
        url = ARTICLE_DELETE_URL(self.article.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())
