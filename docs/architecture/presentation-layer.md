# Camada de Apresentação (API Django REST Framework)

Esta camada é responsável por apresentar os dados ao usuário e receber entradas. Ela atua como um adaptador, traduzindo as requisições HTTP para os DTOs dos casos de uso e as respostas dos casos de uso para o formato JSON da API.

-   `project/core/api/deps.py`: Criado um simples injetor de dependências para fornecer as instâncias concretas dos repositórios e gateways aos casos de uso. Isso garante que as views e casos de uso não precisem saber sobre as implementações concretas.
    -   Funções como `get_user_repository()`, `get_create_user_use_case()`, `get_auth_gateway()`, `get_login_user_use_case()`, `get_change_user_password_use_case()`, `get_list_users_use_case()` e `get_get_user_by_id_use_case()` foram adicionadas.
-   `project/core/api/v1/serializers/user.py`: Os serializadores foram adaptados para trabalhar com os DTOs dos casos de uso em vez de diretamente com os modelos do Django. Novos serializadores incluem `UserReadSerializer`, `UserCreateRequestSerializer`, `LoginRequestSerializer`, `LoginResponseSerializer`, `UserAlterPasswordSerializer` e `UserListResponseSerializer`.
-   `project/core/api/v1/views/user.py`: As views foram modificadas para:
    -   Injetar os casos de uso relevantes usando as funções do `deps.py`.
    -   Converter os dados da requisição HTTP para os DTOs de entrada do caso de uso.
    -   Chamar o método `execute` do caso de uso.
    -   Converter os DTOs de saída do caso de uso para as respostas HTTP JSON.
    -   **`UserCreateAPIView`**: Usa `CreateUserUseCase`.
    -   **`UserListAPIView`**: Usa `ListUsersUseCase`.
    -   **`UserAlterPasswordAPIView`**: Usa `ChangeUserPasswordUseCase`.
    -   **`UserRetrieveAPIView`**: Usa `GetUserByIdUseCase`.
-   `project/core/api/v1/views/auth.py`: Criada a `LoginAPIView` que utiliza o `LoginUserUseCase` para autenticação.

