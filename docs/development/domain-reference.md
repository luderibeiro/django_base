# 🏗️ Domain Layer Reference

Esta página contém a documentação automática da camada de domínio, incluindo entidades e contratos.

## 📦 Entidades

### User Entity

::: core.domain.entities.user.User
options:
show_source: true
show_root_heading: true

## 🔌 Contratos (Interfaces)

### Generic Repository

::: core.domain.data_access.GenericRepository
options:
show_source: true
show_root_heading: true

### User Repository

::: core.domain.data_access.UserRepository
options:
show_source: true
show_root_heading: true

### Auth Gateway

::: core.domain.gateways.AuthGateway
options:
show_source: true
show_root_heading: true

## 📝 Notas sobre a Arquitetura

A camada de domínio é o coração da aplicação e contém:

-   **Entidades**: Objetos de negócio puros (sem dependências externas)
-   **Contratos**: Interfaces que definem as operações necessárias
-   **Regras de Negócio**: Lógica central da aplicação

### Princípios Seguidos

1. **Independência de Frameworks**: Não depende do Django
2. **Testabilidade**: Pode ser testada sem banco de dados
3. **Reutilização**: Lógica de negócio pode ser reutilizada
4. **Inversão de Dependência**: Depende de abstrações, não implementações
