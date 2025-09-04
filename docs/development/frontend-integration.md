# Guia de Integração Frontend

Este guia detalha como um aplicativo frontend pode interagir com a API refatorada, focando nos endpoints de usuário e autenticação.

### Formato de Dados (DTOs)

As requisições e respostas da API seguem os DTOs definidos na camada de aplicação. É crucial que o frontend envie e espere dados nesses formatos.

#### Exemplo: Criação de Usuário

**Requisição (Input):**

-   **Endpoint**: `POST /v1/users/`
-   **Body (JSON)**: Corresponde a `CreateUserRequest`
    ```json
    {
        "email": "novo.usuario@example.com",
        "first_name": "Novo",
        "last_name": "Usuario",
        "password": "senhaSegura123",
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    }
    ```

**Resposta (Output):**

-   **Status**: `201 Created` (sucesso), `400 Bad Request` (erro de validação/domínio)
-   **Body (JSON)**: Corresponde a `CreateUserResponse` (e `UserReadSerializer`)
    ```json
    {
        "id": "<uuid-do-usuario>",
        "email": "novo.usuario@example.com",
        "first_name": "Novo",
        "last_name": "Usuario",
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    }
    ```

#### Exemplo: Login de Usuário

**Requisição (Input):**

-   **Endpoint**: `POST /v1/login/`
-   **Body (JSON)**: Corresponde a `LoginUserRequest`
    ```json
    {
        "email": "usuario.existente@example.com",
        "password": "senhaExistente123"
    }
    ```

**Resposta (Output):**

-   **Status**: `200 OK` (sucesso), `400 Bad Request` (credenciais inválidas)
-   **Body (JSON)**: Corresponde a `LoginUserResponse`
    ```json
    {
        "id": "<uuid-do-usuario>",
        "email": "usuario.existente@example.com",
        "access_token": "<token-de-acesso>",
        "refresh_token": "<token-de-refresh>"
    }
    ```

### Autenticação no Frontend

Após o login, o frontend receberá `access_token` e `refresh_token`. O `access_token` deve ser incluído em todas as requisições subsequentes a endpoints protegidos (que exigem autenticação, como listar usuários ou alterar senha) no cabeçalho `Authorization` como um `Bearer Token`.

Exemplo de cabeçalho em uma requisição fetch/axios:

```javascript
headers: {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${accessToken}`
}
```

### Exemplo: Listar Usuários

**Requisição (Input):**

-   **Endpoint**: `GET /v1/users/list/`
-   **Cabeçalhos**: Necessita `Authorization: Bearer <access_token>` de um usuário com permissão (`IsAdminUser`).
-   **Body**: Não aplicável

**Resposta (Output):**

-   **Status**: `200 OK` (sucesso), `401 Unauthorized` (sem token), `403 Forbidden` (sem permissão)
-   **Body (JSON)**: Corresponde a `ListUsersResponse`
    ```json
    {
        "users": [
            {
                "id": "<uuid-do-usuario-1>",
                "email": "user1@example.com",
                "first_name": "User",
                "last_name": "One",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false
            },
            {
                "id": "<uuid-do-usuario-2>",
                "email": "user2@example.com",
                "first_name": "User",
                "last_name": "Two",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false
            }
        ]
    }
    ```

### Exemplo: Obter Detalhes de um Usuário por ID

**Requisição (Input):**

-   **Endpoint**: `GET /v1/users/:id/`
-   **Cabeçalhos**: Necessita `Authorization: Bearer <access_token>` de um usuário com permissão (`IsAdminUser`).
-   **Parâmetros de URL**: `:id` é o ID do usuário (UUID).
-   **Body**: Não aplicável

**Resposta (Output):**

-   **Status**: `200 OK` (sucesso), `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
-   **Body (JSON)**: Corresponde a `CreateUserResponse` (e `UserReadSerializer`)
    ```json
    {
        "id": "<uuid-do-usuario>",
        "email": "usuario.solicitado@example.com",
        "first_name": "Nome",
        "last_name": "Sobrenome",
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    }
    ```

### Exemplo: Alterar Senha de Usuário

**Requisição (Input):**

-   **Endpoint**: `PUT /v1/users/alter_password/:id/`
-   **Cabeçalhos**: Necessita `Authorization: Bearer <access_token>` de um usuário com permissão (`IsAdminUser`).
-   **Parâmetros de URL**: `:id` é o ID do usuário (UUID).
-   **Body (JSON)**: Corresponde a `ChangeUserPasswordRequest`
    ```json
    {
        "old_password": "senhaAntiga123",
        "new_password": "senhaNovaSegura123"
    }
    ```

**Resposta (Output):**

-   **Status**: `200 OK` (sucesso), `400 Bad Request` (senha antiga incorreta), `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
-   **Body (JSON)**: Corresponde a `ChangeUserPasswordResponse`
    ```json
    {
        "success": true
    }
    ```
