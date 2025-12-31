from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.test import APITestCase

from core.api.throttles import LoginRateThrottle

User = get_user_model()


@pytest.mark.django_db
class AuthAPITest(APITestCase):
    def setUp(self):
        # Desabilitar rate limiting nos testes
        from core.api.v1.views.auth import LoginAPIView

        LoginAPIView.throttle_classes = []

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

    @patch("core.api.v1.views.auth.get_login_user_use_case")
    def test_login_failure_authentication_failed(self, mock_get_use_case):
        """Testa tratamento de exceção AuthenticationFailed."""
        mock_use_case = mock_get_use_case.return_value
        mock_use_case.execute.side_effect = AuthenticationFailed(
            "Authentication failed"
        )

        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        # Aceita tanto a mensagem original quanto a genérica
        self.assertIn(
            response.data["detail"],
            ["Authentication failed", "Falha de autenticação"],
        )

    @patch("core.api.v1.views.auth.get_login_user_use_case")
    def test_login_failure_permission_denied(self, mock_get_use_case):
        """Testa tratamento de exceção PermissionDenied."""
        mock_use_case = mock_get_use_case.return_value
        mock_use_case.execute.side_effect = PermissionDenied("Permission denied")

        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
        # Aceita tanto a mensagem original quanto a genérica
        self.assertIn(
            response.data["detail"], ["Permission denied", "Permissão negada"]
        )

    @patch("core.api.v1.views.auth.get_login_user_use_case")
    def test_login_failure_unexpected_exception(self, mock_get_use_case):
        """Testa tratamento de exceção genérica inesperada."""
        mock_use_case = mock_get_use_case.return_value
        mock_use_case.execute.side_effect = RuntimeError("Unexpected error")

        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Erro interno do servidor")

    def test_login_throttled_exception(self):
        """Testa que exceção Throttled é re-lançada para DRF tratar."""
        from core.api.v1.views.auth import LoginAPIView

        # Reabilitar rate limiting para este teste
        LoginAPIView.throttle_classes = [LoginRateThrottle]

        # Limpar cache antes do teste
        from django.core.cache import cache

        cache.clear()

        # Simular múltiplas requisições para atingir o limite
        for i in range(6):  # 5 é o limite, 6 deve ser bloqueado
            response = self.client.post(
                self.login_url,
                {
                    "email": self.user_data["email"],
                    "password": "wrongpassword",
                },
                format="json",
            )

        # A última requisição deve retornar 429
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

        # Desabilitar novamente para outros testes
        LoginAPIView.throttle_classes = []
