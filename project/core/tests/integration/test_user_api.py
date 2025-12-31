import uuid
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


@pytest.mark.django_db
class UserAPITest(APITestCase):
    def setUp(self):
        self.create_user_url = reverse("core:create-user")
        self.list_users_url = reverse("core:user-list")
        self.login_url = reverse("core:login")

        # Limpar usuários existentes para evitar conflitos
        User.objects.filter(
            email__in=["admin@example.com", "regular@example.com"]
        ).delete()

        self.admin_user_data = {
            "email": "admin@example.com",
            "password": "adminpassword123",
            "first_name": "Admin",
            "last_name": "User",
            "is_staff": True,
            "is_superuser": True,
        }
        self.admin_user = User.objects.create_superuser(**self.admin_user_data)
        self.admin_access_token = self._get_access_token(self.admin_user)

        self.regular_user_data = {
            "email": "regular@example.com",
            "password": "regularpassword123",
            "first_name": "Regular",
            "last_name": "User",
        }
        self.regular_user = User.objects.create_user(**self.regular_user_data)
        self.regular_access_token = self._get_access_token(self.regular_user)

    def _get_access_token(self, user):
        # Usar o mesmo client_id definido no conftest.py e settings
        application, _ = Application.objects.get_or_create(
            client_id="test-client-id",
            defaults={
                "name": "Test App",
                "client_type": "public",
                "authorization_grant_type": "password",
                "skip_authorization": True,  # Importante para testes
            },
        )
        # Garantir que skip_authorization está True
        application.skip_authorization = True
        application.save()

        token = AccessToken.objects.create(
            user=user,
            application=application,
            token=str(uuid.uuid4()),
            expires=timezone.now() + timedelta(days=1),
            scope="read write",
        )

        return token.token

    def test_create_user_success(self):
        new_user_data = {
            "email": "newuser@example.com",
            "password": "newuserpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.create_user_url, new_user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["email"] == new_user_data["email"]

    def test_create_user_failure_duplicate_email(self):
        response = self.client.post(
            self.create_user_url, self.regular_user_data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data

    def test_list_users_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_users_url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "items" in response.data
        assert "total_items" in response.data

    def test_retrieve_user_not_found(self):
        """Testa recuperação de usuário inexistente."""
        from core.api.v1.views.user import UserRetrieveAPIView

        # Desabilitar rate limiting para este teste
        UserRetrieveAPIView.throttle_classes = []

        self.client.force_authenticate(user=self.admin_user)
        fake_user_id = "00000000-0000-0000-0000-000000000000"
        url = reverse("core:user-detail", kwargs={"pk": fake_user_id})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.data

    def test_list_users_as_admin_with_pagination_and_filter(self):
        for i in range(3):
            User.objects.create_user(
                email=f"test{i}@example.com",
                password="pass",
                first_name=f"Test{i}",
                last_name="User",
            )
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(
            f"{self.list_users_url}?limit=2&offset=1&search_query=test1", format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert "items" in response.data

    def test_list_users_unauthenticated_failure(self):
        response = self.client.get(self.list_users_url, format="json")
        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
            or response.status_code == status.HTTP_403_FORBIDDEN
        )

    def test_retrieve_user_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(
            reverse("core:retrieve-user", kwargs={"pk": str(self.regular_user.id)}),
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(self.regular_user.id)
        assert response.data["email"] == self.regular_user.email

    def test_retrieve_user_as_admin_not_found(self):
        """Testa recuperação de usuário inexistente."""
        from core.api.v1.views.user import UserRetrieveAPIView

        # Desabilitar rate limiting para este teste
        UserRetrieveAPIView.throttle_classes = []

        self.client.force_authenticate(user=self.admin_user)
        non_existent_id = uuid.uuid4()
        response = self.client.get(
            reverse("core:retrieve-user", kwargs={"pk": str(non_existent_id)}),
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.data

    def test_retrieve_user_unauthenticated_failure(self):
        response = self.client.get(
            reverse("core:retrieve-user", kwargs={"pk": str(self.regular_user.id)}),
            format="json",
        )
        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
            or response.status_code == status.HTTP_403_FORBIDDEN
        )

    def test_alter_password_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        change_password_url = reverse(
            "core:user-alter-password", kwargs={"pk": str(self.regular_user.id)}
        )
        new_password = "new_regular_password123"
        response = self.client.put(
            change_password_url,
            {
                "old_password": self.regular_user_data["password"],
                "new_password": new_password,
            },
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        login_response = self.client.post(
            self.login_url,
            {"email": self.regular_user_data["email"], "password": new_password},
            format="json",
        )
        assert login_response.status_code == status.HTTP_200_OK

    def test_alter_password_as_admin_failure_incorrect_old_password(self):
        self.client.force_authenticate(user=self.admin_user)
        change_password_url = reverse(
            "core:user-alter-password", kwargs={"pk": str(self.regular_user.id)}
        )
        response = self.client.put(
            change_password_url,
            {"old_password": "wrongpassword", "new_password": "irrelevant"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_alter_password_unauthenticated_failure(self):
        change_password_url = reverse(
            "core:user-alter-password", kwargs={"pk": str(self.regular_user.id)}
        )
        response = self.client.put(
            change_password_url,
            {
                "old_password": self.regular_user_data["password"],
                "new_password": "irrelevant",
            },
            format="json",
        )
        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
            or response.status_code == status.HTTP_403_FORBIDDEN
        )
