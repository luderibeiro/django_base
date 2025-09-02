# Camada de Aplicação (Casos de Uso)

Esta camada contém a lógica específica da aplicação (use cases ou interatores). Ela orquestra as entidades de domínio e utiliza as interfaces de repositório e gateway para realizar suas operações. Os casos de uso são independentes de qualquer camada externa.

-   `project/core/domain/use_cases/user_use_cases.py`: Este arquivo agora contém:
    -   DTOs (Data Transfer Objects): Classes `CreateUserRequest`, `CreateUserResponse`, `LoginUserRequest`, `LoginUserResponse`, `ChangeUserPasswordRequest`, `ChangeUserPasswordResponse`, `ListUsersRequest`, `ListUsersResponse` e `GetUserByIdRequest` foram definidas para entrada e saída dos casos de uso, garantindo que os casos de uso sejam independentes dos formatos de requisição/resposta da API.
    -   `CreateUserUseCase`: Gerencia a lógica para criar um novo usuário.
    -   `LoginUserUseCase`: Gerencia a lógica para autenticar um usuário e gerar tokens.
    -   `ChangeUserPasswordUseCase`: Gerencia a lógica para alterar a senha de um usuário.
    -   `ListUsersUseCase`: Gerencia a lógica para listar usuários.
    -   `GetUserByIdUseCase`: Gerencia a lógica para obter um usuário por ID.

