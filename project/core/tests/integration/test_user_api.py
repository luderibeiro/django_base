from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings

User = get_user_model()


class UserAPITest(APITestCase):
    def setUp(self):
        self.admin_email = "admin@example.com"
        self.admin_password = "adminpassword123"
        self.user_email = "regular@example.com"
        self.user_password = "userpassword123"

        self.admin_user = User.objects.create_superuser(
            email=self.admin_email,
            password=self.admin_password,
            first_name="Admin",
            last_name="User",
        )

        self.regular_user = User.objects.create_user(
            email=self.user_email,
            password=self.user_password,
            first_name="Regular",
            last_name="User",
        )

        # Obter token de acesso para o usuário administrador
        login_data = {"email": self.admin_email, "password": self.admin_password}
        response = self.client.post("/api/v1/auth/login/", login_data, format="json")
        self.admin_access_token = response.data["access_token"]

        self.user_list_url = "/api/v1/users/"
        self.user_create_url = "/api/v1/users/create/"
        self.user_detail_url = lambda user_id: f"/api/v1/users/{user_id}/"
        self.change_password_url = (
            lambda user_id: f"/api/v1/users/{user_id}/change-password/"
        )

        # Criar usuários adicionais para testes de paginação e filtragem
        self.test_users = []
        for i in range(1, 15):
            user = User.objects.create_user(
                email=f"user{i}@example.com",
                password=f"password{i}",
                first_name=f"User{i}",
                last_name=f"Last{i}",
            )
            self.test_users.append(user)

    def get_auth_headers(self, token):
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_list_users_as_admin_success(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)

        # When
        response = self.client.get(self.user_list_url, **headers, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data["items"], list)
        self.assertGreaterEqual(
            len(response.data["items"]), 1
        )  # Deve conter pelo menos o usuário regular
        # Verifica se o admin_user não está na lista por padrão (excluído no get_all)
        self.assertFalse(
            any(user["email"] == self.admin_email for user in response.data["items"])
        )
        self.assertTrue(
            any(user["email"] == self.user_email for user in response.data["items"])
        )

    def test_list_users_as_regular_user_failure(self):
        # Given
        # Obter token de acesso para o usuário regular
        login_data = {"email": self.user_email, "password": self.user_password}
        response = self.client.post("/api/v1/auth/login/", login_data, format="json")
        user_access_token = response.data["access_token"]
        headers = self.get_auth_headers(user_access_token)

        # When
        response = self.client.get(self.user_list_url, **headers, format="json")

        # Then
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Permissão negada

    def test_create_user_success(self):
        # Given
        new_user_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }

        # When
        response = self.client.post(self.user_create_url, new_user_data, format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["email"], new_user_data["email"])

    def test_retrieve_user_as_admin_success(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)

        # When
        response = self.client.get(
            self.user_detail_url(self.regular_user.id), **headers, format="json"
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.regular_user.email)

    def test_retrieve_user_not_found(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        non_existent_id = "99999999-9999-9999-9999-999999999999"

        # When
        response = self.client.get(
            self.user_detail_url(non_existent_id), **headers, format="json"
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_password_as_admin_success(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        change_password_data = {
            "old_password": self.regular_user.password,  # Note: Django user objects don't store plain password
            "new_password": "supernewpassword",
        }
        # Para testes, precisamos da senha em texto plano. No setUp, criamos o usuário com ela.
        # Para mudar a senha, precisamos do ID do usuário
        data_payload = {
            "old_password": self.user_password,
            "new_password": "supernewpassword",
        }

        # When
        response = self.client.post(
            self.change_password_url(self.regular_user.id),
            data_payload,
            **headers,
            format="json",
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

        # Verificar se a senha realmente foi alterada tentando logar com a nova
        login_data_new = {"email": self.user_email, "password": "supernewpassword"}
        login_response_new = self.client.post(
            "/api/v1/auth/login/", login_data_new, format="json"
        )
        self.assertEqual(login_response_new.status_code, status.HTTP_200_OK)

    def test_change_password_as_admin_wrong_old_password(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        data_payload = {
            "old_password": "wrongoldpassword",
            "new_password": "anothernewpassword",
        }

        # When
        response = self.client.post(
            self.change_password_url(self.regular_user.id),
            data_payload,
            **headers,
            format="json",
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid old password")

    def test_list_users_pagination_limit(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        # Quando: Solicitar 5 usuários com limite de 5
        response = self.client.get(
            f"{self.user_list_url}?limit=5", **headers, format="json"
        )

        # Então
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 5)
        self.assertEqual(response.data["limit"], 5)
        self.assertEqual(response.data["offset"], 0)
        self.assertGreaterEqual(
            response.data["total_items"], 15
        )  # Pelo menos 14 + regular_user

    def test_list_users_pagination_offset(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        # Quando: Solicitar 5 usuários a partir do offset 5
        response = self.client.get(
            f"{self.user_list_url}?limit=5&offset=5", **headers, format="json"
        )

        # Então
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 5)
        self.assertEqual(response.data["limit"], 5)
        self.assertEqual(response.data["offset"], 5)

    def test_list_users_filter_by_email(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        search_email = self.test_users[0].email  # Primeiro usuário de teste

        # Quando: Filtrar por email
        response = self.client.get(
            f"{self.user_list_url}?search_query={search_email}",
            **headers,
            format="json",
        )

        # Então
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["email"], search_email)

    def test_list_users_filter_by_first_name(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        search_name = self.test_users[5].first_name  # Sexto usuário de teste

        # Quando: Filtrar por first_name
        response = self.client.get(
            f"{self.user_list_url}?search_query={search_name}", **headers, format="json"
        )

        # Então
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["first_name"], search_name)

    def test_list_users_pagination_and_filter(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        # Criar mais um usuário para garantir que o filtro funciona com paginação
        User.objects.create_user(
            email="unique@example.com",
            password="unique123",
            first_name="Unique",
            last_name="User",
        )

        # Quando: Filtrar por um termo e paginar
        # Busca por 'User' que é comum, e 'Unique' que é específico.
        # Esperamos encontrar o 'Unique User' e possivelmente outros 'UserX'
        response = self.client.get(
            f"{self.user_list_url}?search_query=Unique&limit=1",
            **headers,
            format="json",
        )

        # Então
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["email"], "unique@example.com")
        self.assertEqual(response.data["total_items"], 1)  # apenas o usuário 'Unique'

    def test_global_exception_handler_internal_server_error(self):
        # Given
        headers = self.get_auth_headers(self.admin_access_token)
        # When: Forçar um erro interno na UserListAPIView
        response = self.client.get(
            f"{self.user_list_url}?raise_error=true", **headers, format="json"
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Ocorreu um erro inesperado.")
        self.assertIn("status_code", response.data)
        self.assertEqual(response.data["status_code"], 500)
        if settings.DEBUG: # Importar settings se necessário
            self.assertIn("traceback", response.data)
