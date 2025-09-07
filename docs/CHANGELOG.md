# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Adicionado

-   Nenhuma mudança ainda

### Alterado

-   Nenhuma mudança ainda

### Corrigido

-   Nenhuma mudança ainda

### Removido

-   Nenhuma mudança ainda

## [2.1.0] - 2024-12-19

### Adicionado

-   **OpenAPI/Swagger Documentation**: Implementação completa de documentação automática da API usando `drf-spectacular`, incluindo schema OpenAPI 3.0, interface Swagger UI e ReDoc para melhor experiência de desenvolvedor.

-   **Pre-commit Hooks**: Configuração de hooks de pre-commit para garantir qualidade de código, incluindo formatação automática (Black), linting (Flake8), verificação de docstrings (pydocstyle) e verificação de tipos (MyPy).

-   **MyPy Static Type Checking**: Implementação de verificação de tipos estática em modo gradual, com configuração específica para diferentes módulos e integração com Django via `django-stubs`.

-   **MkDocstrings Integration**: Integração do `mkdocstrings` para gerar documentação automática da API Python diretamente dos docstrings, criando referências completas para camadas de domínio, casos de uso e repositórios.

-   **GitHub Actions CI/CD**: Pipeline completo de CI/CD com workflows para testes, documentação, qualidade de código e deploy, incluindo templates para issues e pull requests.

-   **Documentação Abrangente**:

    -   Guias completos de setup (produção, staging, quick-start)
    -   Análise detalhada de arquitetura do projeto
    -   Diretrizes de segurança e melhores práticas
    -   Referências de API e documentação técnica

-   **Ferramentas de Qualidade**: Configuração de `pydocstyle`, `pytest-cov`, `flake8`, `black` e `pip-audit` para garantir padrões de código e segurança.

-   **Assets e Branding**: Logos e assets visuais do projeto em diferentes tamanhos para uso em documentação e interfaces.

### Melhorado

-   **Docstrings Completas**: Adição de docstrings detalhadas em todo o projeto seguindo padrões PEP 257, incluindo módulos, classes, métodos e funções.

-   **Cobertura de Testes**: Aumento da cobertura de testes para 93% com testes unitários adicionais para middleware, URLs e casos de uso.

-   **Configuração de Ambiente**: Melhoria significativa na configuração de variáveis de ambiente com suporte a diferentes ambientes (desenvolvimento, staging, produção).

-   **Makefile**: Expansão do Makefile com mais de 20 comandos de automação para desenvolvimento, testes, documentação e deploy.

-   **Estrutura de Documentação**: Reorganização completa da documentação com navegação melhorada e seções específicas para diferentes aspectos do projeto.

### Corrigido

-   **Exposição de Credenciais**: Correção de problemas de segurança relacionados à exposição de credenciais em configurações e logs.

-   **Configurações de Template**: Correção de configurações de templates e paths para funcionamento correto em diferentes ambientes.

-   **Imports Não Utilizados**: Limpeza de imports desnecessários e otimização da estrutura de código.

### Refatorado

-   **Configurações de Settings**: Refatoração das configurações do Django para melhor organização e segurança, incluindo configuração condicional de banco de dados.

-   **Estrutura de Arquivos**: Reorganização de arquivos estáticos, templates e configurações para melhor manutenibilidade.

## [2.0.0] - 2024-09-03

### Adicionado

-   **Testes de Integração Completos**: Implementação de uma suíte abrangente de testes de integração para todas as funcionalidades da API, incluindo autenticação, gerenciamento de usuários, paginação, filtragem e alteração de senhas. Todos os 48 testes estão passando com 100% de cobertura das funcionalidades principais.

-   **Tratamento Robusto de Exceções**: Melhoria significativa no tratamento de exceções, incluindo captura correta de `IntegrityError` para retornar 400 Bad Request em vez de 500 Internal Server Error, e tratamento adequado de erros de validação e permissões.

-   **Autenticação e Autorização Aprimoradas**: Implementação de autenticação robusta com OAuth2 e suporte a testes usando `force_authenticate` para maior confiabilidade nos testes de integração.

-   **Limpeza e Otimização de Código**: Remoção de imports não utilizados, logs de debug desnecessários e otimização da estrutura de código para melhor manutenibilidade.

### Corrigido

-   **Erro de Serializer de Alteração de Senha**: Corrigido problema onde o serializer tentava chamar `to_internal_value()` em dados já validados, causando `AttributeError`.

-   **Tratamento de IntegrityError**: Corrigido para capturar corretamente `django.db.utils.IntegrityError` e retornar 400 Bad Request para violações de constraint de banco de dados.

-   **Imports Não Utilizados**: Removidos imports desnecessários (`filters`, `ClassVar`, `get_user_repository`) que estavam causando warnings de linting.

-   **Logs de Debug**: Removidos logs de debug temporários dos testes e middleware para produção.

### Melhorado

-   **Qualidade do Código**: Aplicação de "pente fino" em todo o projeto, garantindo que não há problemas de linting, imports não utilizados ou código desnecessário.

-   **Estrutura de Testes**: Reorganização e otimização dos testes para maior clareza e manutenibilidade, com foco em testes de integração robustos.

-   **Documentação**: Atualização da documentação para refletir as mudanças da versão 2.0.0, incluindo README e CHANGELOG.

## [2.0.0] - 2024-07-30

### Adicionado

-   **Atualização de Dependências e Correção de Vulnerabilidades**: Todas as dependências do projeto foram atualizadas para suas versões estáveis mais recentes, e as vulnerabilidades de segurança conhecidas no Django (5.0.14) e setuptools (66.1.1) foram corrigidas. Isso garante um ambiente de desenvolvimento e produção mais seguro e estável.

-   **Configuração de Logs e Tratamento Global de Exceções**: Implementação de uma estratégia robusta de _logging_ com múltiplos _handlers_ (console, arquivo de log, arquivo de erros), formatadores padronizados e _loggers_ específicos. Criação de um _middleware_ customizado para tratamento global de exceções no Django REST Framework, que captura, registra e padroniza respostas de erro da API. Logs foram adicionados a casos de uso (`LoginUserUseCase`, `ListUsersUseCase`) e repositórios (`DjangoUserRepository`) para maior observabilidade.

    -   `project/project/settings.py`: Configuração de `LOGGING` e integração do _middleware_ no `REST_FRAMEWORK`.
    -   `project/core/middleware/custom_exception_middleware.py`: Novo arquivo com o _handler_ de exceções customizado.
    -   `project/core/domain/use_cases/user_use_cases.py`: Adição de logs.
    -   `project/core/repositories/user_repository_impl.py`: Adição de logs e tratamento de exceções específicas.
    -   Documentação detalhada em `docs/development/logging-error-handling.md`.

-   **Otimização e Refatoração de Arquivos Docker**: Reestruturação do `Dockerfile` para um modelo multi-stage (build e execução) com imagem base mais leve (`python:3.12-slim-bookworm`), combinação de comandos `RUN` para reduzir camadas, e otimização na instalação de dependências. Introdução de arquivos `docker-compose.dev.yml` e `docker-compose.prod.yml` para separar as configurações de ambientes de desenvolvimento e produção, com `Dockerfile.dev` para desenvolvimento e `.dockerignore` para exclusão de arquivos desnecessários.

    -   `.dockerignore`: Novo arquivo para exclusão de arquivos irrelevantes no contexto de build.
    -   `Dockerfile`: Refatorado para multi-stage build e otimizado para produção.
    -   `Dockerfile.dev`: Novo arquivo para ambiente de desenvolvimento.
    -   `docker-compose.dev.yml`: Novo arquivo para orquestração de serviços em desenvolvimento.
    -   `docker-compose.prod.yml`: Novo arquivo para orquestração de serviços em produção.
    -   `docker-compose.yml`: Removido.
    -   `dotenv_files/.env.prod`: Novo arquivo para variáveis de ambiente de produção.
    -   `docs/setup/project-setup.md`: Documentação atualizada para refletir a nova estrutura Docker.

-   **Testes Automatizados**: Implementação de uma suíte abrangente de testes unitários para as camadas de Domínio e Aplicação, e testes de integração para a API (autenticação e gerenciamento de usuários).
    -   `project/core/tests/unit/test_user_entity.py`
    -   `project/core/tests/unit/test_user_use_cases.py`
    -   `project/core/tests/unit/test_generic_use_cases.py`
    -   `project/core/tests/integration/test_auth_api.py`
    -   `project/core/tests/integration/test_user_api.py`
    -   Configuração do Pytest (`config/pytest.ini`) e adição de dependências (`pytest`, `pytest-mock`, `pytest-django`).
    -   Documentação detalhada em `docs/development/automated-testing.md`.
-   **Paginação e Filtragem**: Adicionadas capacidades de paginação (`offset`, `limit`) e filtragem (`search_query`) para a API de listagem de usuários. Isso envolveu modificações nos DTOs, interface de repositório, implementação do repositório (`DjangoUserRepository` usando `Q` objects), _serializers_ e _views_ do DRF, e testes de integração abrangentes.
    -   `project/core/domain/use_cases/user_use_cases.py`: DTOs `ListUsersRequest`, `ListUsersResponse` e `ListUsersUseCase` atualizados.
    -   `project/core/domain/data_access.py`: Interface `UserRepository` com `get_all_paginated_filtered`.
    -   `project/core/repositories/user_repository_impl.py`: Implementação de `get_all_paginated_filtered`.
    -   `project/core/api/v1/serializers/user.py`: `ListUsersRequestSerializer` e `UserListResponseSerializer`.
    -   `project/core/api/v1/views/user.py`: `UserListAPIView` atualizada.
    -   `project/core/tests/integration/test_user_api.py`: Novos testes de paginação e filtragem.
    -   Documentação detalhada em `docs/development/pagination-filtering.md`.
-   **Estrutura de Changelog**: Criação deste arquivo `CHANGELOG.md` para rastrear todas as alterações do projeto, substituindo o antigo `SUMMARY_OF_CHANGES.md`.

### Alterado

-   **Links de Documentação**: Corrigidos links absolutos e relativos no `README.md` da raiz e no `docs/CONTRIBUTING.md` para garantir o funcionamento correto no GitHub Pages.
-   **Navegação do MkDocs**: Atualização do `config/mkdocs.yml` para incluir novas entradas de documentação (Testes Automatizados, Paginação e Filtragem, Logs e Tratamento de Exceções) e a nova entrada `Changelog`.

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
