# flake8: noqa: E731

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


REDACTOR_LIST_URL = reverse("catalog:redactor-list")
REDACTOR_DETAIL_URL = lambda pk: reverse("catalog:redactor-detail", args=[pk])
REDACTOR_CREATE_URL = reverse("catalog:redactor-create")
REDACTOR_LICENSE_UPDATE_URL = lambda pk: reverse("catalog:redactor-update", args=[pk])
REDACTOR_DELETE_URL = lambda pk: reverse("catalog:redactor-delete", args=[pk])


class PublicRedactorTests(TestCase):
    def test_login_required(self):
        """Test that login is required to access the redactor list view"""
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateRedactorTests(TestCase):
    def setUp(self):
        """Set up a logged-in user and test data"""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
        )
        self.client.force_login(self.user)

        self.redactor = get_user_model().objects.create_user(
            username="redactor1",
            password="password123",
            years_of_experience="5",
            first_name="John",
            last_name="Doe",
        )

    def test_retrieve_redactor_list(self):
        """Test retrieving the list of redactors"""
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.redactor, response.context["redactor_list"])
        self.assertTemplateUsed(response, "catalog/redactor_list.html")

    def test_search_driver_by_username(self):
        """Test searching redactors by username"""
        get_user_model().objects.create_user(
            username="redactor2",
            password="password123",
            years_of_experience="9",
        )
        response = self.client.get(REDACTOR_LIST_URL, {"username": "redactor1"})
        self.assertEqual(len(response.context["redactor_list"]), 1)
        self.assertEqual(response.context["redactor_list"][0], self.redactor)

    def test_retrieve_redactor_detail(self):
        """Test retrieving a redactor's detail view"""
        url = REDACTOR_DETAIL_URL(self.redactor.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["redactor"], self.redactor)
        self.assertTemplateUsed(response, "catalog/redactor_detail.html")

    def test_create_redactor(self):
        """Test creating a new redactor"""
        form_data = {
            "username": "new_redactor",
            "password1": "Strongpassword123",
            "password2": "Strongpassword123",
            "years_of_experience": "9",
            "first_name": "Jane",
            "last_name": "Smith",
        }
        response = self.client.post(REDACTOR_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(
            get_user_model().objects.filter(username="new_redactor").exists()
        )

    def test_update_redactor_license(self):
        """Test updating a redactor's license"""
        form_data = {"years_of_experience": "19"}
        url = REDACTOR_LICENSE_UPDATE_URL(self.redactor.id)
        response = self.client.post(url, data=form_data)
        self.redactor.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(self.redactor.years_of_experience, 19)

    def test_delete_redactor(self):
        """Test deleting a redactor"""
        url = REDACTOR_DELETE_URL(self.redactor.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(
            get_user_model().objects.filter(id=self.redactor.id).exists()
        )
