# 🎯 Use Cases Reference

Esta página contém a documentação automática dos casos de uso da aplicação.

## 👤 User Use Cases

### Create User Use Case

::: core.domain.use_cases.user_use_cases.CreateUserUseCase
options:
show_source: true
show_root_heading: true

### Login User Use Case

::: core.domain.use_cases.user_use_cases.LoginUserUseCase
options:
show_source: true
show_root_heading: true

### Change User Password Use Case

::: core.domain.use_cases.user_use_cases.ChangeUserPasswordUseCase
options:
show_source: true
show_root_heading: true

### List Users Use Case

::: core.domain.use_cases.user_use_cases.ListUsersUseCase
options:
show_source: true
show_root_heading: true

### Get User By ID Use Case

::: core.domain.use_cases.user_use_cases.GetUserByIdUseCase
options:
show_source: true
show_root_heading: true

## 🔧 Generic Use Cases

### Create Entity Use Case

::: core.domain.use_cases.generic_use_cases.CreateEntityUseCase
options:
show_source: true
show_root_heading: true

### List Entities Use Case

::: core.domain.use_cases.generic_use_cases.ListEntitiesUseCase
options:
show_source: true
show_root_heading: true

### Get Entity By ID Use Case

::: core.domain.use_cases.generic_use_cases.GetEntityByIdUseCase
options:
show_source: true
show_root_heading: true

### Update Entity Use Case

::: core.domain.use_cases.generic_use_cases.UpdateEntityUseCase
options:
show_source: true
show_root_heading: true

### Delete Entity Use Case

::: core.domain.use_cases.generic_use_cases.DeleteEntityUseCase
options:
show_source: true
show_root_heading: true

## 📋 DTOs (Data Transfer Objects)

### User Use Cases DTOs

::: core.domain.use_cases.user_use_cases.CreateUserRequest
options:
show_source: true
show_root_heading: true

::: core.domain.use_cases.user_use_cases.CreateUserResponse
options:
show_source: true
show_root_heading: true

::: core.domain.use_cases.user_use_cases.LoginUserRequest
options:
show_source: true
show_root_heading: true

::: core.domain.use_cases.user_use_cases.LoginUserResponse
options:
show_source: true
show_root_heading: true

### Generic Use Cases DTOs

::: core.domain.use_cases.generic_use_cases.GenericCreateRequest
options:
show_source: true
show_root_heading: true

::: core.domain.use_cases.generic_use_cases.GenericReadResponse
options:
show_source: true
show_root_heading: true

::: core.domain.use_cases.generic_use_cases.GenericListRequest
options:
show_source: true
show_root_heading: true

::: core.domain.use_cases.generic_use_cases.GenericListResponse
options:
show_source: true
show_root_heading: true

## 🎯 Sobre os Use Cases

Os casos de uso encapsulam a lógica de aplicação e:

-   **Orquestram** operações entre diferentes camadas
-   **Implementam** regras de negócio específicas da aplicação
-   **Coordenam** repositórios e gateways
-   **Retornam** DTOs padronizados

### Padrão de Execução

Todos os use cases seguem o padrão:

1. Recebem um `Request` DTO
2. Executam a lógica de negócio
3. Retornam um `Response` DTO
4. Tratam exceções de forma consistente


