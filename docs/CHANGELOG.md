# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2024-07-30

### Adicionado

-   **Testes Automatizados**: Implementação de uma suíte abrangente de testes unitários para as camadas de Domínio e Aplicação, e testes de integração para a API (autenticação e gerenciamento de usuários).
    -   `project/core/tests/unit/test_user_entity.py`
    -   `project/core/tests/unit/test_user_use_cases.py`
    -   `project/core/tests/unit/test_generic_use_cases.py`
    -   `project/core/tests/integration/test_auth_api.py`
    -   `project/core/tests/integration/test_user_api.py`
    -   Configuração do Pytest (`pytest.ini`) e adição de dependências (`pytest`, `pytest-mock`, `pytest-django`).
    -   Documentação detalhada em `docs/development/automated-testing.md`.
-   **Estrutura de Changelog**: Criação deste arquivo `CHANGELOG.md` para rastrear todas as alterações do projeto, substituindo o antigo `SUMMARY_OF_CHANGES.md`.

### Alterado

-   **Links de Documentação**: Corrigidos links absolutos e relativos no `README.md` da raiz e no `docs/CONTRIBUTING.md` para garantir o funcionamento correto no GitHub Pages.
-   **Navegação do MkDocs**: Atualização do `mkdocs.yml` para incluir a nova entrada `Changelog`.

### Refatorado

-   **Modelo de Usuário Mais Leve**: O modelo `User` do Django foi refatorado para herdar de `AbstractBaseUser` e `PermissionsMixin`, removendo o campo `username` e definindo `USERNAME_FIELD = "email"` e `REQUIRED_FIELDS` apropriadamente. A lógica em `DjangoUserRepository` e nos casos de uso foi adaptada para o novo modelo.
-   **Implementação OAuth2 Completa**: A `DjangoAuthGateway` foi atualizada para utilizar o `django-oauth-toolkit` para a geração real de tokens de acesso e refresh, substituindo a lógica de tokens fictícios. Configurações OAuth2 confirmadas em `settings.py` e `urls.py`.


## [1.1.0] - Projeto Base de Arquitetura Limpa Inicial

### Adicionado

-   **Estrutura da Arquitetura Limpa**: O projeto foi reestruturado em camadas distintas (Domínio, Aplicação, Infraestrutura, Apresentação), promovendo o desacoplamento e a separação de responsabilidades.
    -   **Domínio**: Entidades de negócio (`User`) e interfaces abstratas (`UserRepository`, `AuthGateway`).
    -   **Aplicação**: Casos de uso (use cases/interactors) para orquestrar a lógica de negócio, dependendo apenas da camada de Domínio. Foram criados casos de uso genéricos CRUD e casos de uso específicos para `User` (criação, login, listagem, obtenção por ID, alteração de senha).
    -   **Infraestrutura**: Implementações concretas das interfaces de repositório e gateway usando tecnologias específicas (ex: `DjangoUserRepository` via ORM do Django, `DjangoAuthGateway` para autenticação Django).
    -   **Apresentação (API)**: Views e serializers do Django REST Framework adaptados para interagir com os casos de uso e seus DTOs.
-   **Injeção de Dependências**: Módulo (`project/core/api/deps.py`) criado para gerenciar e injetar as dependências concretas nos casos de uso.
-   **Documentação Inicial**: Criação de um guia detalhado sobre a Arquitetura Limpa no projeto.
-   **Arquivos Open Source**: Inclusão de `CONTRIBUTING.md` e `CODE_OF_CONDUCT.md`.
-   **Configuração MkDocs**: Setup do MkDocs e GitHub Pages para hospedar a documentação do projeto.

### Alterado

-   **Configuração de URLs**: Rotas da API (`/v1/users/`, `/v1/login/`, etc.) foram centralizadas e atualizadas.
-   **Serializers e Views DRF**: Adaptados para interagir com os casos de uso e seus DTOs, garantindo que a camada de apresentação atue como um adaptador.
-   **Reestruturação da Documentação**: O guia original foi dividido e organizado em um novo diretório `docs/` com subdiretórios (`architecture/`, `development/`, `setup/`), melhorando a navegabilidade.

### Removido

-   Lógica de negócio diretamente de views e serializers do DRF, movida para os casos de uso na camada de Aplicação.
