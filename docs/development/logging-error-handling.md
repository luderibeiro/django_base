# Configuração de Logs e Tratamento Global de Exceções

Esta seção detalha a implementação de uma estratégia robusta de logs e um tratamento global de exceções para a API. Essas funcionalidades são cruciais para a observabilidade, depuração e estabilidade do projeto em produção.

## 1. Contexto e Justificativa

Uma boa estratégia de _logging_ permite monitorar o comportamento da aplicação, identificar problemas e diagnosticar erros em tempo real. O tratamento global de exceções garante que erros inesperados sejam capturados, registrados e apresentados ao cliente de forma consistente e segura, sem expor detalhes internos sensíveis.

## 2. Visão Geral da Implementação

A implementação envolverá as seguintes alterações:

-   **Configuração de Logs**: Definir uma configuração avançada de _logging_ no `settings.py` do Django, com diferentes níveis, _handlers_ (console, arquivo) e formatadores.
-   **Middleware de Tratamento de Exceções**: Criar um _middleware_ personalizado para capturar e registrar exceções não tratadas na camada de apresentação (API), retornando respostas de erro padronizadas.
-   **Integração do Middleware**: Adicionar o novo _middleware_ à configuração do Django.
-   **Uso de Logs**: Exemplos de como utilizar o _logger_ em diferentes camadas para registrar eventos e erros específicos.
-   **Testes de Integração**: Adicionar testes para validar o comportamento do tratamento global de exceções na API.

## 3. Configuração de Logs (`project/project/settings.py`)

Configuramos o sistema de _logging_ do Django para incluir múltiplos _handlers_ (console, arquivo, arquivo de erros), formatadores detalhados e _loggers_ específicos para as aplicações `django`, `core` e `project`. Isso permite um controle granular sobre como e onde as mensagens de log são registradas.

```python
# project/project/settings.py
import os
from pathlib import Path
# ... outras configurações ...

BASE_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "app.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "error.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
        "core": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
        "project": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file", "error_file"],
        "level": "INFO",
    },
}
```

## 4. Criação de Middleware de Tratamento de Exceções (`project/core/middleware.py`)

### a. `custom_exception_middleware.py` (Novo arquivo)

Criamos um _handler_ de exceções customizado que se integra ao Django REST Framework. Ele captura exceções, registra-as usando o sistema de _logging_, e retorna uma resposta padronizada ao cliente, incluindo detalhes do _traceback_ em ambiente de `DEBUG`.

```python
# project/core/middleware/custom_exception_middleware.py
import logging
import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if not response.data.get("status_code"):
            response.data["status_code"] = response.status_code

        if isinstance(exc, ValueError):
            response.data["detail"] = str(exc)
            response.status_code = status.HTTP_400_BAD_REQUEST

        if settings.DEBUG:
            response.data["traceback"] = traceback.format_exc()

        if response.status_code >= 500:
            logger.exception("Erro de servidor interno: %s", exc)
        elif response.status_code >= 400:
            logger.warning("Erro de cliente: %s", exc)

    else:
        logger.exception("Erro inesperado: %s", exc)
        response = Response(
            {"detail": "Ocorreu um erro inesperado.", "status_code": 500},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        if settings.DEBUG:
            response.data["traceback"] = traceback.format_exc()

    return response
```

## 5. Integração do Middleware (`project/project/settings.py`)

Para ativar o _middleware_ e o _handler_ de exceções customizado, fizemos as seguintes alterações no `settings.py`:

-   Adicionamos o `CustomExceptionMiddleware` à lista `MIDDLEWARE`.
-   Configuramos o `REST_FRAMEWORK` para usar o `custom_exception_handler`.

```python
# project/project/settings.py
# ... outras configurações ...

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.custom_exception_middleware.CustomExceptionMiddleware", # Adicionado middleware de exceção customizado
]

# ... outras configurações ...

REST_FRAMEWORK = {
    # ... outras configurações do DRF ...
    "EXCEPTION_HANDLER": "core.middleware.custom_exception_middleware.custom_exception_handler", # Handler de exceção customizado
}

# ... outras configurações ...
```

## 6. Uso de Logs em Casos de Uso e Repositórios

Exemplos de como integrar o _logging_ em diferentes camadas do projeto para registrar eventos importantes, _warnings_ e erros.

### Exemplo: `LoginUserUseCase` (`project/core/domain/use_cases/user_use_cases.py`)

```python
# project/core/domain/use_cases/user_use_cases.py
import logging
# ... outras importações ...

logger = logging.getLogger(__name__)

class LoginUserUseCase:
    # ... __init__ ...

    def execute(self, request: LoginUserRequest) -> LoginUserResponse:
        logger.info("Attempting to log in user with email: %s", request.email)
        user = self.user_repository.get_user_by_email(request.email)
        if not user:
            logger.warning("Login failed: User not found for email %s", request.email)
            raise ValueError("Invalid credentials")

        if not self.auth_gateway.check_password(user.id, request.password):
            logger.warning("Login failed: Invalid password for user ID %s", user.id)
            raise ValueError("Invalid credentials")

        access_token, refresh_token = self.auth_gateway.create_tokens(user.id)
        logger.info("User %s logged in successfully. User ID: %s", request.email, user.id)

        return LoginUserResponse(
            id=user.id,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token,
        )
```

### Exemplo: `DjangoUserRepository` (`project/core/repositories/user_repository_impl.py`)

```python
# project/core/repositories/user_repository_impl.py
import logging
# ... outras importações ...

logger = logging.getLogger(__name__)

class DjangoUserRepository(UserRepository):
    # ... outros métodos ...

    def get_by_id(self, user_id: str) -> Optional[DomainUser]:
        try:
            user = DjangoUser.objects.get(id=user_id)
            logger.debug("User found by ID: %s", user_id)
            return self._to_domain_user(user)
        except DjangoUser.DoesNotExist:
            logger.warning("User not found by ID: %s", user_id)
            return None

    def create(self, user: DomainUser) -> DomainUser:
        logger.info("Attempting to create user with email: %s", user.email)
        django_user = DjangoUser.objects.create_user(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        logger.info("User created successfully with ID: %s", django_user.id)
        return self._to_domain_user(django_user)
```

## 7. Testes de Integração

Adicionamos testes de integração para validar o comportamento do tratamento global de exceções, garantindo que a API retorne respostas padronizadas para diferentes tipos de erros.

### Exemplo: Teste de Login com Credenciais Inválidas (`project/core/tests/integration/test_auth_api.py`)

Este teste verifica se, ao tentar logar com credenciais inválidas, a API retorna um `HTTP 400 Bad Request` com a mensagem de erro esperada, conforme configurado pelo `custom_exception_handler` para `ValueError`.

```python
# project/core/tests/integration/test_auth_api.py
from rest_framework import status
from rest_framework.test import APITestCase
# ... outras importações ...

class AuthAPITest(APITestCase):
    # ... setUp e outros testes ...

    def test_login_failure_invalid_password(self):
        data = {"email": self.email, "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid credentials")

    def test_login_failure_user_not_found(self):
        data = {"email": "nonexistent@example.com", "password": self.password}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid credentials")
```

### Exemplo: Simulação de Erro Interno Inesperado (`project/core/tests/integration/test_user_api.py`)

Este teste simula um erro interno (`RuntimeError`) em um _endpoint_ da API para verificar se o tratamento global de exceções o captura e retorna um `HTTP 500 Internal Server Error` com uma mensagem genérica e o _traceback_ em modo `DEBUG`.

```python
# project/core/tests/integration/test_user_api.py
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings # Necessário para verificar settings.DEBUG
# ... outras importações ...

class UserAPITest(APITestCase):
    # ... setUp e outros testes ...

    def test_global_exception_handler_internal_server_error(self):
        headers = self.get_auth_headers(self.admin_access_token)
        response = self.client.get(
            f"{self.user_list_url}?raise_error=true", **headers, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Ocorreu um erro inesperado.")
        self.assertIn("status_code", response.data)
        self.assertEqual(response.data["status_code"], 500)
        if settings.DEBUG:
            self.assertIn("traceback", response.data)
```

## 8. Passos da Implementação

1.  **Criação do arquivo de documentação**: Criado `docs/development/logging-error-handling.md`.
2.  **Atualização do `config/mkdocs.yml`**: Adicionado o link para o novo documento na navegação.
3.  **Configuração de Logs**: Adicionada a configuração de `LOGGING` em `project/project/settings.py`.
4.  **Criação do Middleware**: Criado `project/core/middleware/custom_exception_middleware.py` com o _handler_ de exceções.
5.  **Integração do Middleware**: Adicionado o `CustomExceptionMiddleware` à lista `MIDDLEWARE` e configurado `REST_FRAMEWORK["EXCEPTION_HANDLER"]` em `project/project/settings.py`.
6.  **Uso de Logs no Código**: Inseridas chamadas de `logger.info`, `logger.warning` e `logger.debug` em `project/core/domain/use_cases/user_use_cases.py` e `project/core/repositories/user_repository_impl.py`.
7.  **Adição de Testes de Integração**: Adicionado `test_global_exception_handler_internal_server_error` em `project/core/tests/integration/test_user_api.py` para validar o comportamento do tratamento de exceções 500.
8.  **Atualização da Documentação**: Este documento foi atualizado com todos os detalhes e exemplos das etapas de implementação.
9.  **Remoção da Lógica Temporária**: A lógica `raise RuntimeError` será removida de `project/core/api/v1/views/user.py` após a finalização da documentação.
