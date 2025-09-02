import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


@pytest.mark.django_db
class AuthAPITest(APITestCase):
    def setUp(self):
        self.login_url = reverse("core:login")
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("id", response.data)
        self.assertIn("email", response.data)

    def test_login_failure_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "test@example.com",
                "password": "wrongpassword",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid credentials")

    def test_login_failure_user_not_found(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "nonexistent@example.com",
                "password": "anypassword",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid credentials")

    def test_login_failure_missing_fields(self):
        response = self.client.post(
            self.login_url, {"email": "test@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

        response = self.client.post(
            self.login_url, {"password": "testpassword123"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
