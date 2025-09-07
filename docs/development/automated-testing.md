# Adicionando Testes Automatizados

Esta seção detalha a estratégia e a implementação de testes automatizados para o projeto, cobrindo testes unitários para as camadas de Domínio e Aplicação, e testes de integração para a camada de Apresentação (API).

## 1. Contexto e Justificativa

Testes automatizados são fundamentais para garantir a qualidade, robustez e a manutenibilidade de qualquer projeto de software, especialmente em um contexto open source. Eles permitem verificar o comportamento do sistema, detectar regressões precocemente e documentar a funcionalidade do código. Com a Arquitetura Limpa, a testabilidade é maximizada devido ao desacoplamento das camadas.

## 2. Estrutura de Testes

Os testes serão organizados no diretório `project/core/tests/`, com subdiretórios para categorizá-los:

-   `project/core/tests/unit/`: Para testes unitários que focam em componentes isolados (entidades, casos de uso).
-   `project/core/tests/integration/`: Para testes de integração que verificam a interação entre componentes (API com casos de uso e repositórios).

## 3. Ferramentas de Teste

Utilizaremos as seguintes bibliotecas para os testes:

-   **`pytest`**: Um framework de teste robusto e flexível para Python.
-   **`pytest-django`**: Plugin para `pytest` que facilita o teste de aplicações Django.
-   **`pytest-mock`**: Para criar mocks e simular dependências em testes unitários.
-   **`rest_framework.test.APITestCase`**: Para simular requisições HTTP e testar endpoints da API.

## 4. Testes Unitários (Camadas de Domínio e Aplicação)

Testes unitários focam na lógica de negócio das camadas de Domínio e Aplicação. Eles são rápidos, isolados e não dependem de banco de dados ou frameworks externos.

### a. Entidades de Domínio (`project/core/domain/entities/user.py`)

Nesta subseção, demonstramos como testar as entidades de domínio de forma isolada, garantindo que sua lógica interna funcione conforme o esperado. O exemplo abaixo mostra um teste básico para a criação de um usuário e a propriedade `is_admin` da entidade `User`.

```python
# project/core/tests/unit/test_user_entity.py
from core.domain.entities.user import User

def test_user_creation():
    user = User(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        is_active=True,
        is_staff=False,
        is_superuser=False,
        id="123",
    )
    assert user.id == "123"
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.is_admin is False

def test_user_is_admin_property():
    admin_user = User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        is_superuser=True,
    )
    assert admin_user.is_admin is True

    regular_user = User(
        email="regular@example.com",
        first_name="Regular",
        last_name="User",
        is_superuser=False,
    )
    assert regular_user.is_admin is False
```

### b. Casos de Uso (`project/core/domain/use_cases/user_use_cases.py`, `project/core/domain/use_cases/generic_use_cases.py`)

Os testes de casos de uso focam em verificar a lógica de negócio principal, utilizando mocks para simular o comportamento dos repositórios e gateways, garantindo que o caso de uso reaja corretamente às entradas e interaja adequadamente com suas dependências.

#### Exemplo: `CreateUserUseCase`

```python
# project/core/tests/unit/test_user_use_cases.py
from unittest.mock import Mock
import pytest
from core.domain.entities.user import User as DomainUser
from core.domain.use_cases.user_use_cases import CreateUserRequest, CreateUserUseCase

@pytest.fixture
def mock_user_repository():
    return Mock()

def test_create_user_use_case_success(mock_user_repository):
    user_id = "123"
    email = "test@example.com"
    first_name = "Test"
    last_name = "User"
    password = "password123"

    mock_user_repository.create.return_value = DomainUser(
        id=user_id, email=email, first_name=first_name, last_name=last_name
    )

    use_case = CreateUserUseCase(user_repository=mock_user_repository)
    request = CreateUserRequest(
        email=email, first_name=first_name, last_name=last_name, password=password
    )

    response = use_case.execute(request)

    mock_user_repository.create.assert_called_once()
    assert response.id == user_id
    assert response.email == email
    assert response.first_name == first_name
    assert response.last_name == last_name
```

#### Exemplo: `CreateEntityUseCase` (Genérico)

```python
# project/core/tests/unit/test_generic_use_cases.py
from unittest.mock import Mock
import pytest
from core.domain.data_access import GenericRepository
from core.domain.entities.user import User as DomainUser
from core.domain.use_cases.generic_use_cases import CreateEntityUseCase, GenericCreateRequest

@pytest.fixture
def mock_generic_repository():
    return Mock(spec=GenericRepository)

@pytest.fixture
def sample_user():
    return DomainUser(
        id="1",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )

def test_create_entity_use_case_success(mock_generic_repository, sample_user):
    mock_generic_repository.create.return_value = sample_user
    use_case = CreateEntityUseCase(repository=mock_generic_repository)
    request = GenericCreateRequest(data=sample_user)

    response = use_case.execute(request)

    mock_generic_repository.create.assert_called_once_with(sample_user)
    assert response.data == sample_user
```

## 5. Testes de Integração (Camada de Apresentação - API)

Testes de integração verificam se as diferentes camadas do projeto (API, Casos de Uso, Repositórios, persistência) funcionam bem em conjunto. Eles simulam requisições HTTP para os endpoints da API.

### a. Autenticação e Usuários (`project/core/api/v1/views/auth.py`, `project/core/api/v1/views/user.py`)

Os testes de integração verificam a funcionalidade completa da API, incluindo a interação com os casos de uso e as camadas de infraestrutura (como o banco de dados e o sistema de autenticação). Utilizamos `rest_framework.test.APITestCase` para simular requisições HTTP e verificar as respostas.

#### Exemplo: Login de Usuário (Sucesso)

```python
# project/core/tests/integration/test_auth_api.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class AuthAPITest(APITestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.password = "testpassword123"
        User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name="Test",
            last_name="User",
        )
        self.login_url = "/api/v1/auth/login/"

    def test_login_success(self):
        data = {"email": self.email, "password": self.password}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("access_token", response.data)
```

#### Exemplo: Listar Usuários (como Admin)

```python
# project/core/tests/integration/test_user_api.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class UserAPITest(APITestCase):
    def setUp(self):
        self.admin_email = "admin@example.com"
        self.admin_password = "adminpassword123"
        self.admin_user = User.objects.create_superuser(
            email=self.admin_email,
            password=self.admin_password,
            first_name="Admin",
            last_name="User",
        )
        login_data = {"email": self.admin_email, "password": self.admin_password}
        response = self.client.post("/api/v1/auth/login/", login_data, format="json")
        self.admin_access_token = response.data["access_token"]
        self.user_list_url = "/api/v1/users/"

    def get_auth_headers(self, token):
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_list_users_as_admin_success(self):
        headers = self.get_auth_headers(self.admin_access_token)
        response = self.client.get(self.user_list_url, **headers, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data["items"], list)
        # ... outras asserções
```

## 6. Passos da Implementação

A implementação dos testes automatizados seguiu os seguintes passos:

1.  **Criação de Novo Arquivo de Documentação**: O arquivo `docs/development/automated-testing.md` foi criado para descrever a estratégia de testes.
2.  **Atualização de `config/mkdocs.yml`**: O novo arquivo de documentação foi adicionado à navegação do MkDocs.
3.  **Instalação de Dependências de Teste**: `pytest` e `pytest-mock` foram adicionados ao `project/requirements.txt` e instalados. `pytest-django` já estava presente.
4.  **Estrutura de Diretórios de Testes**: Os diretórios `project/core/tests/unit/` e `project/core/tests/integration/` foram criados para organizar os testes.
5.  **Configuração do `config/pytest.ini`**: Um arquivo `config/pytest.ini` foi criado na raiz do projeto com configurações básicas para o `pytest` (ex: `DJANGO_SETTINGS_MODULE`, `python_files`, `addopts`).
6.  **Implementação de Testes Unitários (Domínio)**: O arquivo `project/core/tests/unit/test_user_entity.py` foi criado com testes para a entidade `User`.
7.  **Implementação de Testes Unitários (Aplicação)**: Os arquivos `project/core/tests/unit/test_user_use_cases.py` e `project/core/tests/unit/test_generic_use_cases.py` foram criados com testes para os casos de uso de `User` e casos de uso genéricos, respectivamente, utilizando mocks.
8.  **Implementação de Testes de Integração (API)**: Os arquivos `project/core/tests/integration/test_auth_api.py` e `project/core/tests/integration/test_user_api.py` foram criados com testes de integração para os _endpoints_ da API de autenticação e gerenciamento de usuários, incluindo a obtenção e uso de tokens de acesso.

Com esses testes implementados, o projeto possui uma base robusta para garantir a qualidade do código e a funcionalidade da aplicação.
