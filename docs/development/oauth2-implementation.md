# Implementação Completa de OAuth2

Esta seção detalha a implementação completa do protocolo OAuth2 para autenticação e autorização, utilizando a biblioteca `django-oauth-toolkit`.

## 1. Contexto e Justificativa

Atualmente, a autenticação básica de login retorna tokens simplificados. Para um projeto-base robusto, é essencial ter um sistema de autenticação e autorização baseado em padrões da indústria. O OAuth2, com o `django-oauth-toolkit`, oferece uma solução completa para gerenciamento de tokens de acesso e refresh, permitindo uma integração segura com clientes externos (frontends, aplicativos móveis, outras APIs).

## 2. Abordagem da Implementação

### a. Configuração do `django-oauth-toolkit`

Será necessário configurar o `django-oauth-toolkit` no projeto, incluindo sua adição a `INSTALLED_APPS` e a configuração das URLs de OAuth2.

(Detalhes da configuração em `project/project/settings.py` e `project/project/urls.py` serão adicionados aqui)

### b. `AuthGateway` (`project/core/domain/gateways.py`)

A interface `AuthGateway` já define o método `create_tokens`. Esta interface não será alterada, pois ela já abstrai a necessidade de um gateway de autenticação.

### c. `DjangoAuthGateway` (`project/core/repositories/auth_gateway_impl.py`)

A implementação concreta do `create_tokens` no `DjangoAuthGateway` será modificada para utilizar a API do `django-oauth-toolkit` para gerar tokens OAuth2 padrão (access token e refresh token).

(Detalhes da implementação no arquivo `project/core/repositories/auth_gateway_impl.py` serão adicionados aqui)

### d. Impacto em Casos de Uso e Views

-   **`LoginUserUseCase`**: Este caso de uso chama `auth_gateway.create_tokens()`. Ele receberá os novos tokens OAuth2 sem precisar de alterações na sua lógica.
-   **`LoginAPIView`**: A view de login continuará a usar o `LoginUserUseCase` e o `LoginResponseSerializer` para retornar os tokens ao cliente. O `LoginResponseSerializer` pode precisar de pequenos ajustes se o formato dos tokens mudar significativamente, mas a expectativa é que ele já esteja preparado para receber `access_token` e `refresh_token`.

## 3. Passos da Implementação

(Os passos técnicos detalhados serão adicionados aqui à medida que a implementação for realizada.)
