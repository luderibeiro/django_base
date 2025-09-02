from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from core.domain.entities.user import User as DomainUser
from core.repositories.user_repository_impl import DjangoUserRepository

User = get_user_model()


class AuthAPITest(APITestCase):
    def setUp(self):
        self.user_repository = DjangoUserRepository()
        self.email = "test@example.com"
        self.password = "testpassword123"
        self.first_name = "Test"
        self.last_name = "User"

        # Criar um usuário Django diretamente para testes de integração
        self.django_user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

        self.login_url = "/api/v1/auth/login/"

    def test_login_success(self):
        # Given
        data = {
            "email": self.email,
            "password": self.password,
        }

        # When
        response = self.client.post(self.login_url, data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("email", response.data)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertEqual(response.data["email"], self.email)

    def test_login_failure_invalid_password(self):
        # Given
        data = {
            "email": self.email,
            "password": "wrongpassword",
        }

        # When
        response = self.client.post(self.login_url, data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid credentials")

    def test_login_failure_user_not_found(self):
        # Given
        data = {
            "email": "nonexistent@example.com",
            "password": self.password,
        }

        # When
        response = self.client.post(self.login_url, data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid credentials")

    def test_login_missing_fields(self):
        # Given
        data = {"email": self.email}  # Missing password

        # When
        response = self.client.post(self.login_url, data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
