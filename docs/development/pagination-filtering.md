# Adicionando Paginação e Filtragem

Esta seção descreve a implementação de funcionalidades de paginação e filtragem para a listagem de usuários na API, tornando-a mais flexível e eficiente para lidar com grandes volumes de dados.

## 1. Contexto e Justificativa

Para APIs que retornam listas de recursos, é crucial implementar mecanismos de paginação para evitar sobrecarregar o cliente e o servidor com grandes respostas. A filtragem, por sua vez, permite que os clientes solicitem apenas os dados relevantes, melhorando a experiência do usuário e a performance da aplicação.

Na Arquitetura Limpa, esses controles devem ser introduzidos nas camadas de Aplicação (nos casos de uso, que orquestram a lógica) e de Infraestrutura (nos repositórios, que interagem com o mecanismo de persistência), e expostos na camada de Apresentação (API).

## 2. Visão Geral da Implementação

A implementação envolverá as seguintes alterações:

-   **Camada de Aplicação**: Modificar o `ListUsersRequest` e `ListUsersResponse` para incluir parâmetros de paginação (offset, limit) e filtragem (ex: `search_query`). O `ListUsersUseCase` será atualizado para utilizar esses parâmetros.
-   **Camada de Domínio (Interface)**: Atualizar a interface `UserRepository` com um novo método para obter usuários paginados e filtrados.
-   **Camada de Infraestrutura**: Implementar o método de paginação e filtragem no `DjangoUserRepository`, utilizando recursos do ORM do Django.
-   **Camada de Apresentação (API)**: Adaptar a `UserListAPIView` e seus serializers para receber os parâmetros de paginação e filtragem via requisição HTTP e formatar a resposta com metadados de paginação.
-   **Testes de Integração**: Adicionar testes para validar o funcionamento da paginação e filtragem na API.

## 3. Alterações na Camada de Aplicação (Casos de Uso)

### a. `ListUsersRequest` e `ListUsersResponse`

Modificamos os DTOs `ListUsersRequest` e `ListUsersResponse` para incluir os parâmetros de paginação (`offset`, `limit`) e filtragem (`search_query`), além dos metadados de paginação na resposta.

```python
# project/core/domain/use_cases/user_use_cases.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class ListUsersRequest:
    offset: int = 0
    limit: int = 10
    search_query: str | None = None

@dataclass
class ListUsersResponse:
    users: list[CreateUserResponse]
    total_items: int
    offset: int
    limit: int
```

### b. `ListUsersUseCase`

O `ListUsersUseCase` foi modificado para aceitar os novos parâmetros de `ListUsersRequest` e delegar a lógica de paginação e filtragem ao repositório, retornando os metadados de paginação na `ListUsersResponse`.

```python
# project/core/domain/use_cases/user_use_cases.py
from core.domain.data_access import UserRepository
from core.domain.entities.user import User as DomainUser
from core.domain.use_cases.generic_use_cases import CreateUserResponse # Necessário para o ListUsersResponse
from dataclasses import dataclass
from typing import Optional, List # Adicionado List aqui

@dataclass
class ListUsersRequest:
    offset: int = 0
    limit: int = 10
    search_query: str | None = None

@dataclass
class ListUsersResponse:
    users: list[CreateUserResponse]
    total_items: int
    offset: int
    limit: int

class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, request: ListUsersRequest) -> ListUsersResponse:
        users_domain, total_items = self.user_repository.get_all_paginated_filtered(
            offset=request.offset, limit=request.limit, search_query=request.search_query
        )

        users_response = [
            CreateUserResponse(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser,
            )
            for user in users_domain
        ]
        return ListUsersResponse(
            users=users_response,
            total_items=total_items,
            offset=request.offset,
            limit=request.limit,
        )
```

## 4. Alterações na Camada de Domínio (Interface de Repositório)

### a. `UserRepository`

Adicionamos o método `get_all_paginated_filtered` à interface `UserRepository`, que permite obter usuários com base em parâmetros de paginação e filtragem, retornando uma tupla contendo a lista de usuários e o total de itens.

```python
# project/core/domain/data_access.py
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from core.domain.entities.user import User

T = TypeVar("T")

# ... GenericRepository ...

class UserRepository(GenericRepository[User]):
    # ... outros métodos ...

    @abstractmethod
    def get_all_paginated_filtered(
        self, offset: int, limit: int, search_query: str | None
    ) -> tuple[List[User], int]:
        pass
```

## 5. Alterações na Camada de Infraestrutura (Implementação de Repositório)

### a. `DjangoUserRepository`

A implementação do `DjangoUserRepository` agora inclui o método `get_all_paginated_filtered`, que utiliza o ORM do Django para aplicar a filtragem por email, `first_name` e `last_name` (case-insensitive) e a paginação (`offset` e `limit`).

```python
# project/core/repositories/user_repository_impl.py
from typing import List, Optional
from django.db.models import Q

from core.domain.data_access import UserRepository
from core.domain.entities.user import User as DomainUser
from core.models.user import User as DjangoUser

class DjangoUserRepository(UserRepository):
    # ... outros métodos ...

    def get_all_paginated_filtered(
        self, offset: int, limit: int, search_query: str | None
    ) -> tuple[List[DomainUser], int]:
        queryset = DjangoUser.objects.exclude(is_superuser=True)

        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

        total_items = queryset.count()
        django_users = queryset[offset : offset + limit]
        return [self._to_domain_user(user) for user in django_users], total_items
```

## 6. Alterações na Camada de Apresentação (API)

### a. Serializers (`project/core/api/v1/serializers/user.py`)

Criamos um `ListUsersRequestSerializer` para validar os parâmetros de `query` de paginação e filtragem, e atualizamos o `UserListResponseSerializer` para incluir os metadados de paginação na resposta.

```python
# project/core/api/v1/serializers/user.py
from rest_framework import serializers
from core.domain.use_cases.user_use_cases import ListUsersRequest, ListUsersResponse
from .user import UserSerializer

class UserListResponseSerializer(serializers.Serializer):
    items = UserSerializer(many=True)
    total_items = serializers.IntegerField()
    offset = serializers.IntegerField()
    limit = serializers.IntegerField()

    def to_representation(self, instance: ListUsersResponse):
        return {
            "items": [UserSerializer(user).data for user in instance.users],
            "total_items": instance.total_items,
            "offset": instance.offset,
            "limit": instance.limit,
        }

class ListUsersRequestSerializer(serializers.Serializer):
    offset = serializers.IntegerField(default=0, required=False, min_value=0)
    limit = serializers.IntegerField(default=10, required=False, min_value=1)
    search_query = serializers.CharField(required=False, allow_blank=True)

    def to_internal_value(self, data):
        return ListUsersRequest(
            offset=data.get("offset", 0),
            limit=data.get("limit", 10),
            search_query=data.get("search_query", None),
        )
```

### b. Views (`project/core/api/v1/views/user.py`)

A `UserListAPIView` foi adaptada para utilizar o `ListUsersRequestSerializer` para validar os parâmetros de paginação e filtragem da requisição, e passa esses parâmetros para o `ListUsersUseCase`.

```python
# project/core/api/v1/views/user.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from core.domain.use_cases.user_use_cases import get_list_users_use_case
from ..serializers.user import (
    UserAlterPasswordSerializer,
    UserCreateRequestSerializer,
    UserListResponseSerializer,
    UserReadSerializer,
    UserSerializer,
    ListUsersRequestSerializer,
)

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListResponseSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        request_serializer = ListUsersRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        list_users_request = request_serializer.to_internal_value(request_serializer.validated_data)

        list_users_use_case = get_list_users_use_case()
        list_users_response = list_users_use_case.execute(list_users_request)

        response_serializer = UserListResponseSerializer(instance=list_users_response)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
```

## 7. Testes de Integração

Adicionamos testes de integração em `project/core/tests/integration/test_user_api.py` para validar o comportamento da API com as novas funcionalidades de paginação e filtragem.

### Exemplo: Paginação (Limite)

```python
# project/core/tests/integration/test_user_api.py
# ... imports e setUp ...

class UserAPITest(APITestCase):
    # ... setUp e outros testes ...

    def test_list_users_pagination_limit(self):
        headers = self.get_auth_headers(self.admin_access_token)
        response = self.client.get(f"{self.user_list_url}?limit=5", **headers, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 5)
        self.assertEqual(response.data["limit"], 5)
        self.assertEqual(response.data["offset"], 0)
        self.assertGreaterEqual(response.data["total_items"], 15)
```

### Exemplo: Filtragem por Email

```python
# project/core/tests/integration/test_user_api.py
# ... imports e setUp ...

class UserAPITest(APITestCase):
    # ... setUp e outros testes ...

    def test_list_users_filter_by_email(self):
        headers = self.get_auth_headers(self.admin_access_token)
        search_email = self.test_users[0].email

        response = self.client.get(f"{self.user_list_url}?search_query={search_email}", **headers, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["email"], search_email)
```

## 8. Passos da Implementação

A implementação da paginação e filtragem para a listagem de usuários seguiu os seguintes passos:

1.  **Criação de Novo Arquivo de Documentação**: O arquivo `docs/development/pagination-filtering.md` foi criado para descrever a estratégia de paginação e filtragem.
2.  **Atualização de `config/mkdocs.yml`**: O novo arquivo de documentação foi adicionado à navegação do MkDocs.
3.  **Atualização de Casos de Uso (`ListUsersUseCase`)**: `ListUsersRequest` e `ListUsersResponse` foram modificados para incluir parâmetros de paginação (`offset`, `limit`) e filtragem (`search_query`). O `ListUsersUseCase` foi adaptado para utilizar esses parâmetros e delegar a lógica ao repositório.
4.  **Atualização da Interface de Repositório (`UserRepository`)**: O método abstrato `get_all_paginated_filtered` foi adicionado à interface `UserRepository`.
5.  **Atualização da Implementação de Repositório (`DjangoUserRepository`)**: O método `get_all_paginated_filtered` foi implementado, utilizando o ORM do Django (com `Q` para filtragem `icontains`) para aplicar a lógica de paginação e filtragem.
6.  **Atualização de Serializers da API**: Um `ListUsersRequestSerializer` foi criado para validar os parâmetros de `query` de entrada, e o `UserListResponseSerializer` foi atualizado para incluir os metadados de paginação (`total_items`, `offset`, `limit`) na resposta.
7.  **Atualização de Views da API (`UserListAPIView`)**: A `UserListAPIView` foi modificada para utilizar o `ListUsersRequestSerializer` para processar os parâmetros da requisição e passar os dados para o `ListUsersUseCase`.
8.  **Atualização de Testes de Integração**: Novos testes foram adicionados em `project/core/tests/integration/test_user_api.py` para validar o funcionamento da paginação e filtragem nos _endpoints_ da API.

Com a paginação e filtragem implementadas e documentadas, a API de listagem de usuários torna-se mais flexível e eficiente.
