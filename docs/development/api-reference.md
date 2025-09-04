# 📚 API Reference - OpenAPI Schema

Esta página contém a documentação completa da API REST do Django Base, gerada automaticamente a partir do código.

## 🔗 Acesso à Documentação Interativa

### Swagger UI

Acesse a documentação interativa da API através do Swagger UI:

-   **URL**: `/api/docs/`
-   **Descrição**: Interface interativa para testar endpoints da API

### ReDoc

Documentação alternativa com visual limpo:

-   **URL**: `/api/redoc/`
-   **Descrição**: Documentação em formato ReDoc

### Schema OpenAPI

Schema JSON da API:

-   **URL**: `/api/schema/`
-   **Descrição**: Schema OpenAPI 3.0 em formato JSON

## 🔐 Autenticação

A API utiliza OAuth2 para autenticação. Para acessar os endpoints protegidos:

1. **Obter token de acesso**:

    ```bash
    curl -X POST http://localhost:8000/o/token/ \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "grant_type=password&username=seu_email&password=sua_senha&client_id=seu_client_id&client_secret=seu_client_secret"
    ```

2. **Usar token nas requisições**:
    ```bash
    curl -H "Authorization: Bearer SEU_TOKEN" \
      http://localhost:8000/api/v1/users/
    ```

## 📋 Endpoints Principais

### Usuários

-   `GET /api/v1/users/` - Listar usuários
-   `POST /api/v1/users/` - Criar usuário
-   `GET /api/v1/users/{id}/` - Obter usuário por ID
-   `PUT /api/v1/users/{id}/password/` - Alterar senha

### Autenticação

-   `POST /api/v1/auth/login/` - Login de usuário

## 🎯 Exemplos de Uso

### Criar Usuário

```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "email": "usuario@exemplo.com",
    "first_name": "João",
    "last_name": "Silva",
    "password": "senha123"
  }'
```

### Listar Usuários com Paginação

```bash
curl -H "Authorization: Bearer SEU_TOKEN" \
  "http://localhost:8000/api/v1/users/?limit=10&offset=0&search=joão"
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@exemplo.com",
    "password": "senha123"
  }'
```

## 📊 Códigos de Status

-   `200` - Sucesso
-   `201` - Criado com sucesso
-   `400` - Dados inválidos
-   `401` - Não autenticado
-   `403` - Sem permissão
-   `404` - Recurso não encontrado
-   `500` - Erro interno do servidor

## 🔧 Configuração

A documentação é gerada automaticamente usando `drf-spectacular` e está configurada em `SPECTACULAR_SETTINGS` no arquivo `settings.py`.

Para regenerar o schema:

```bash
python manage.py spectacular --file schema.yml
```
