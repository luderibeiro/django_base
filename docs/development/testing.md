# Como Testar

A adoção da Arquitetura Limpa torna o projeto altamente testável. A lógica de negócio reside nas camadas de Domínio e Aplicação, que são completamente independentes de frameworks e bancos de dados, permitindo testes unitários rápidos e isolados.

### Testes Unitários (Camadas de Domínio e Aplicação)

Para testar as camadas de Domínio e Aplicação, você pode usar um framework de teste como `pytest`. Você precisaria:

1. **Mockar as dependências**: Criar `mocks` para `UserRepository` e `AuthGateway` (que são interfaces). Isso permite que você teste os casos de uso sem precisar de um banco de dados real ou sistema de autenticação.

```python
# test_user_use_cases.py
from unittest.mock import Mock
from core.domain.entities.user import User as DomainUser
from core.domain.use_cases.user_use_cases import CreateUserRequest, CreateUserUseCase, GetUserByIdRequest, GetUserByIdUseCase

def test_create_user_use_case_success():
    # Given
    mock_user_repository = Mock()
    mock_user_repository.create_user.return_value = DomainUser(
        id="123", email="test@example.com", first_name="Test", last_name="User"
    )
    use_case = CreateUserUseCase(user_repository=mock_user_repository)
    request = CreateUserRequest(
        email="test@example.com", first_name="Test", last_name="User", password="password123"
    )

    # When
    response = use_case.execute(request)

    # Then
    mock_user_repository.create_user.assert_called_once()
    assert response.email == "test@example.com"
    assert response.id == "123"

def test_get_user_by_id_use_case_success():
    # Given
    mock_user_repository = Mock()
    expected_user = DomainUser(
        id="123", email="test@example.com", first_name="Test", last_name="User"
    )
    mock_user_repository.get_user_by_id.return_value = expected_user
    use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
    request = GetUserByIdRequest(user_id="123")

    # When
    response = use_case.execute(request)

    # Then
    mock_user_repository.get_user_by_id.assert_called_once_with("123")
    assert response.id == expected_user.id
    assert response.email == expected_user.email
```

### Testes de Integração (Camada de Apresentação - API)

Para testar a integração da API com as camadas inferiores, você pode usar `APITestCase` do Django REST Framework. Esses testes simularão requisições HTTP e verificarão as respostas da API.

```python
# test_user_api.py
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITests(APITestCase):
    def test_create_user_success():
        url = reverse("v1:create-user")
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpassword123",
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201
        assert "id" in response.data
        assert response.data["email"] == "newuser@example.com"
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_login_user_success():
        # Criar um usuário primeiro
        self.client.post(reverse("v1:create-user"), {
            "email": "loginuser@example.com",
            "first_name": "Login",
            "last_name": "User",
            "password": "loginpassword123",
        }, format='json')

        url = reverse("v1:login")
        data = {
            "email": "loginuser@example.com",
            "password": "loginpassword123",
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 200
        assert "access_token" in response.data
        assert "refresh_token" in response.data

    def test_list_users_success():
        # Criar alguns usuários
        self.client.post(reverse("v1:create-user"), {
            "email": "user1@example.com", "first_name": "User", "last_name": "One", "password": "password123"
        }, format='json')
        self.client.post(reverse("v1:create-user"), {
            "email": "user2@example.com", "first_name": "User", "last_name": "Two", "password": "password123"
        }, format='json')

        url = reverse("v1:user-list")
        # É necessário estar autenticado para listar usuários (assumindo IsAdminUser ou similar)
        # Por enquanto, se a permissão é AllowAny, pode ser testado diretamente.
        response = self.client.get(url, format='json')
        assert response.status_code == 200
        assert len(response.data["users"]) >= 2

    def test_get_user_by_id_success():
        # Criar um usuário
        create_response = self.client.post(reverse("v1:create-user"), {
            "email": "getuser@example.com", "first_name": "Get", "last_name": "User", "password": "getuser123"
        }, format='json')
        user_id = create_response.data["id"]

        url = reverse("v1:retrieve-user", kwargs={'pk': user_id})
        # Este teste precisa de autenticação de admin. Para simplificar, vamos assumir que
        # um admin está fazendo a requisição. Em um cenário real, você autenticaria o admin.
        response = self.client.get(url, format='json')
        assert response.status_code == 200
        assert response.data["id"] == user_id
        assert response.data["email"] == "getuser@example.com"

    def test_change_password_success():
        # Criar um usuário e autenticar (ou obter o ID do usuário de outra forma)
        create_response = self.client.post(reverse("v1:create-user"), {
            "email": "changepass@example.com", "first_name": "Change", "last_name": "Pass", "password": "oldpassword123"
        }, format='json')
        user_id = create_response.data["id"]

        url = reverse("v1:user-alter-password", kwargs={'pk': user_id})
        data = {
            "old_password": "oldpassword123",
            "new_password": "newstrongpassword123",
        }
        # Este teste precisa de autenticação de admin. Para simplificar, vamos assumir que
        # um admin está fazendo a requisição. Em um cenário real, você autenticaria o admin.
        response = self.client.put(url, data, format='json') # Ou patch
        assert response.status_code == 200
        assert response.data["success"]

        # Tentar logar com a nova senha para confirmar
        login_url = reverse("v1:login")
        login_data = {"email": "changepass@example.com", "password": "newstrongpassword123"}
        login_response = self.client.post(login_url, login_data, format='json')
        assert login_response.status_code == 200
```

### Comandos `curl` para Teste Manual

Você pode usar `curl` para testar os endpoints da API manualmente.

### 1. Criar Usuário (Register)

```bash
curl -X POST http://localhost:8000/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{ "email": "user@example.com", "first_name": "John", "last_name": "Doe", "password": "mypassword123" }'
```

### 2. Login de Usuário

```bash
curl -X POST http://localhost:8000/v1/login/ \
     -H "Content-Type: application/json" \
     -d '{ "email": "user@example.com", "password": "mypassword123" }'
```

(A resposta incluirá `access_token` e `refresh_token`)

### 3. Listar Usuários

```bash
# Você precisará de um token de autenticação (Bearer Token) para esta requisição,
# caso a permissão IsAdminUser esteja ativa na view.
# Supondo que você tem um token de um usuário admin:
# TOKEN="seu_access_token_aqui"

curl -X GET http://localhost:8000/v1/users/list/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN"
```

### 4. Obter Detalhes de um Usuário por ID

```bash
# Você precisará do ID do usuário e de um token de autenticação (Bearer Token)
# de um usuário admin.
# USER_ID="o_id_do_usuario_aqui"
# TOKEN="seu_access_token_aqui"

curl -X GET http://localhost:8000/v1/users/$USER_ID/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN"
```

### 5. Alterar Senha de Usuário

```bash
# Você precisará do ID do usuário e de um token de autenticação (Bearer Token)
# de um usuário admin.
# USER_ID="o_id_do_usuario_aqui"
# TOKEN="seu_access_token_aqui"

curl -X PUT http://localhost:8000/v1/users/alter_password/$USER_ID/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{ "old_password": "mypassword123", "new_password": "mynewpassword456" }'
```
