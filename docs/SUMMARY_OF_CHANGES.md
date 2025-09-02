# Resumo das Alterações do Projeto Django - Arquitetura Limpa

Este documento apresenta um resumo das principais alterações e refatorações realizadas neste projeto Django para implementar os princípios da Arquitetura Limpa. O objetivo foi transformar o projeto em uma base robusta, modular e facilmente extensível.

## 1. Estrutura da Arquitetura Limpa

O projeto foi reestruturado em camadas distintas, promovendo o desacoplamento e a separação de responsabilidades:

-   **Domínio**: Contém as entidades de negócio (`User`) e interfaces abstratas (`UserRepository`, `AuthGateway`).
-   **Aplicação**: Gerencia os casos de uso (use cases/interactors) que orquestram a lógica de negócio, dependendo apenas da camada de Domínio. Foram criados casos de uso genéricos CRUD e casos de uso específicos para `User` (criação, login, listagem, obtenção por ID, alteração de senha).
-   **Infraestrutura**: Implementa as interfaces de repositório e gateway usando tecnologias específicas (ex: `DjangoUserRepository` para persistência via ORM do Django, `DjangoAuthGateway` para autenticação Django).
-   **Apresentação (API)**: Adapta as requisições HTTP para os DTOs dos casos de uso e formata as respostas (usando Django REST Framework views e serializers).

## 2. Implementação de Casos de Uso CRUD Genéricos

Foram introduzidos casos de uso CRUD genéricos (`CreateEntityUseCase`, `ListEntitiesUseCase`, `GetEntityByIdUseCase`, `UpdateEntityUseCase`, `DeleteEntityUseCase`) junto com DTOs e interfaces de repositório genéricas. Isso permite a reutilização de lógica CRUD para diferentes entidades, reduzindo a duplicação de código. Os casos de uso de `User` existentes foram adaptados para utilizar essa estrutura genérica.

## 3. Refatoração da Autenticação e Gestão de Usuários

As operações de autenticação e gestão de usuários foram completamente refatoradas para se adequarem à Arquitetura Limpa:

-   **Entidade `User`**: Criada como uma entidade de domínio pura, independente do Django.
-   **`UserRepository` e `DjangoUserRepository`**: Interface e implementação para operações de persistência de usuário.
-   **`AuthGateway` e `DjangoAuthGateway`**: Interface e implementação para operações de autenticação (verificação de senha, geração de tokens).
-   **Casos de Uso de Usuário**: `CreateUserUseCase`, `LoginUserUseCase`, `ChangeUserPasswordUseCase`, `ListUsersUseCase`, `GetUserByIdUseCase` foram criados para encapsular a lógica de negócio.
-   **Injeção de Dependências**: Um módulo (`project/core/api/deps.py`) foi criado para gerenciar e injetar as dependências concretas (repositórios e gateways) nos casos de uso.

## 4. Adaptação da API (Django REST Framework)

As views e serializers do DRF foram adaptados para interagir com os casos de uso e seus DTOs, garantindo que a camada de apresentação seja um mero adaptador, sem lógica de negócio:

-   **Serializers**: Criados para mapear dados de requisição/resposta HTTP para os DTOs dos casos de uso (ex: `UserCreateRequestSerializer`, `LoginResponseSerializer`).
-   **Views**: Modificadas para injetar e chamar os casos de uso correspondentes, manipulando erros e formatando respostas HTTP (ex: `LoginAPIView`, `UserCreateAPIView`, `UserListAPIView`).
-   **Configuração de URLs**: Rotas da API (`/v1/users/`, `/v1/login/`, etc.) foram centralizadas e atualizadas para as novas views.

## 5. Reestruturação da Documentação

A documentação original (`CLEAN_ARCHITECTURE_GUIDE.md`) foi dividida e organizada em um novo diretório `docs/` com subdiretórios (`architecture/`, `development/`, `setup/`). Isso melhora a navegabilidade e facilita o acesso a informações específicas sobre a arquitetura, desenvolvimento e configuração do projeto.

Esta reestruturação visa fornecer um projeto-base mais compreensível, fácil de manter e de escalar, seguindo as melhores práticas da Arquitetura Limpa.
