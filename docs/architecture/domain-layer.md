# Camada de Domínio

Esta é a camada mais interna e contém as regras de negócio essenciais da aplicação (Entidades) e as abstrações para interações com o mundo exterior (Interfaces de Repositório e Gateways). Ela é completamente independente de qualquer framework ou banco de dados.

## Entidades

-   `project/core/domain/entities/user.py`: Criada a entidade `User` para representar um usuário de forma agnóstica a frameworks, contendo apenas os atributos e métodos de domínio (ex: `email`, `first_name`, `is_admin`). Esta entidade não herda de `django.db.models.Model`.

### Interfaces de Acesso a Dados (Repositories)

-   `project/core/domain/data_access.py`: Criada a interface abstrata `UserRepository`, que define os métodos que qualquer repositório de usuário deve implementar (ex: `get_user_by_id`, `create_user`, `get_all_users`).

### Interfaces de Gateways (Auth, etc.)

-   `project/core/domain/gateways.py`: Criada a interface abstrata `AuthGateway`, que define métodos para operações de autenticação como `check_password`, `create_tokens`, e `set_password`.
