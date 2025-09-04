# 🗄️ Repositories Reference

Esta página contém a documentação automática das implementações de repositórios.

## 👤 User Repository Implementation

### Django User Repository

::: core.repositories.user_repository_impl.DjangoUserRepository
options:
show_source: true
show_root_heading: true

## 🔐 Auth Gateway Implementation

### Django Auth Gateway

::: core.repositories.auth_gateway_impl.DjangoAuthGateway
options:
show_source: true
show_root_heading: true

## 🔧 Dependency Injection

### API Dependencies

::: core.api.deps
options:
show_source: true
show_root_heading: true

## 📝 Sobre as Implementações

As implementações de repositórios e gateways:

-   **Conectam** a camada de domínio com a infraestrutura
-   **Implementam** os contratos definidos na camada de domínio
-   **Utilizam** Django ORM para persistência
-   **Mapeiam** entre modelos Django e entidades de domínio

### Padrões Utilizados

1. **Repository Pattern**: Abstração de acesso a dados
2. **Gateway Pattern**: Abstração de serviços externos
3. **Dependency Injection**: Inversão de controle
4. **Adapter Pattern**: Adaptação entre camadas

### Mapeamento de Dados

Os repositórios fazem a conversão entre:

-   **Modelos Django** ↔ **Entidades de Domínio**
-   **Querysets** ↔ **Listas de Entidades**
-   **Exceções Django** ↔ **Exceções de Domínio**
