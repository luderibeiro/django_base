# Casos de Uso CRUD Genéricos

Para promover a reutilização de código e manter a consistência em operações básicas de criação, leitura, atualização e exclusão (CRUD) para diferentes entidades, foram implementados casos de uso genéricos na camada de aplicação.

Esta seção detalha a estrutura e o uso desses casos de uso genéricos.

## Visão Geral

Os casos de uso genéricos permitem realizar operações CRUD sem precisar reescrever a lógica básica para cada nova entidade. Eles operam em cima de interfaces de repositório genéricas e DTOs genéricos.

## Componentes Chave

### 1. DTOs Genéricos (`project/core/domain/use_cases/generic_use_cases.py`)

Os DTOs genéricos são classes de dados (`@dataclass`) usadas para padronizar a entrada e saída dos casos de uso CRUD, garantindo que a comunicação entre as camadas seja desacoplada do framework.

-   `GenericCreateRequest[T]`: Usado para requisições de criação, encapsulando a entidade a ser criada.
-   `GenericReadResponse[T]`: Usado para respostas de leitura, contendo a entidade lida.
-   `GenericListRequest`: Um DTO simples para requisições de listagem (pode ser estendido para incluir filtros e paginação).
-   `GenericListResponse[T]`: Usado para respostas de listagem, contendo uma lista de entidades.
-   `GenericUpdateRequest[T]`: Usado para requisições de atualização, incluindo o ID e os dados da entidade a ser atualizada.
-   `GenericDeleteRequest`: Usado para requisições de exclusão, contendo o ID da entidade.
-   `GenericSuccessResponse`: Uma resposta simples para indicar o sucesso de uma operação (ex: exclusão).

```python
# ... (imports)

T = TypeVar('T') # Representa a entidade de domínio

@dataclass
class GenericCreateRequest(Generic[T]):
    data: T

@dataclass
class GenericReadResponse(Generic[T]):
    data: T

# ... (outros DTOs genéricos)

class UseCase(Generic[T]):
    pass
```

### 2. Interface `GenericRepository[T]` (`project/core/domain/data_access.py`)

A interface `GenericRepository[T]` define o contrato para operações CRUD básicas que qualquer repositório de entidade deve implementar. `T` é um `TypeVar` que representa o tipo da entidade de domínio.

```python
# ... (imports)

T = TypeVar('T')

class GenericRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        pass
```

### 3. Casos de Uso Genéricos (`project/core/domain/use_cases/generic_use_cases.py`)

Esses casos de uso implementam a lógica básica para cada operação CRUD, dependendo da `GenericRepository` para a persistência.

-   `CreateEntityUseCase[T]`: Recebe uma `GenericCreateRequest` e usa `repository.create()`.

    ```python
    class CreateEntityUseCase(UseCase[T]):
        def __init__(self, repository: GenericRepository[T]):
            self.repository = repository

        def execute(self, request: GenericCreateRequest[T]) -> GenericReadResponse[T]:
            created_entity = self.repository.create(request.data)
            return GenericReadResponse(data=created_entity)
    ```

-   `ListEntitiesUseCase[T]`: Recebe uma `GenericListRequest` e usa `repository.get_all()`.

    ```python
    class ListEntitiesUseCase(UseCase[T]):
        def __init__(self, repository: GenericRepository[T]):
            self.repository = repository

        def execute(self, request: GenericListRequest) -> GenericListResponse[T]:
            entities = self.repository.get_all()
            return GenericListResponse(items=entities)
    ```

-   `GetEntityByIdUseCase[T]`: Recebe uma `GenericDeleteRequest` (que contém o ID) e usa `repository.get_by_id()`.

    ```python
    class GetEntityByIdUseCase(UseCase[T]):
        def __init__(self, repository: GenericRepository[T]):
            self.repository = repository

        def execute(self, request: GenericDeleteRequest) -> GenericReadResponse[T]:
            entity = self.repository.get_by_id(request.id)
            if not entity:
                raise ValueError("Entity not found")
            return GenericReadResponse(data=entity)
    ```

-   `UpdateEntityUseCase[T]`: Recebe uma `GenericUpdateRequest` e usa `repository.update()`.

    ```python
    class UpdateEntityUseCase(UseCase[T]):
        def __init__(self, repository: GenericRepository[T]):
            self.repository = repository

        def execute(self, request: GenericUpdateRequest[T]) -> GenericReadResponse[T]:
            existing_entity = self.repository.get_by_id(request.id)
            if not existing_entity:
                raise ValueError("Entity not found")

            updated_entity = request.data
            updated_entity.id = request.id
            saved_entity = self.repository.update(updated_entity)
            return GenericReadResponse(data=saved_entity)
    ```

-   `DeleteEntityUseCase[T]`: Recebe uma `GenericDeleteRequest` e usa `repository.delete()`.

    ```python
    class DeleteEntityUseCase(UseCase[T]):
        def __init__(self, repository: GenericRepository[T]):
            self.repository = repository

        def execute(self, request: GenericDeleteRequest) -> GenericSuccessResponse:
            self.repository.delete(request.id)
            return GenericSuccessResponse(success=True)
    ```

## Adaptação de Casos de Uso Existentes (Ex: Usuário)

Os casos de uso específicos de `User` foram refatorados para utilizar os casos de uso genéricos, promovendo a reutilização de código e mantendo a lógica de negócio específica do usuário onde é necessário.

-   **`UserRepository` (`project/core/domain/data_access.py`)**: Foi modificado para estender `GenericRepository[User]`, implementando seus métodos (`get_by_id`, `get_all`, `create`, `update`, `delete`) e mantendo `get_user_by_email` como um método específico de `User`.

-   **`DjangoUserRepository` (`project/core/repositories/user_repository_impl.py`)**: A implementação concreta do repositório de usuário foi atualizada para implementar os métodos da `GenericRepository`.

-   **`CreateUserUseCase` (`project/core/domain/use_cases/user_use_cases.py`)**: Agora utiliza uma instância de `CreateEntityUseCase[DomainUser]` internamente para a lógica de criação base.

    ```python
    class CreateUserUseCase:
        def __init__(self, user_repository: UserRepository):
            self.user_repository = user_repository
            self.generic_create_use_case = CreateEntityUseCase[DomainUser](repository=user_repository)

        def execute(self, request: CreateUserRequest) -> CreateUserResponse:
            user_domain_to_create = DomainUser(
                # ... atributos do usuário
            )
            generic_request = GenericCreateRequest(data=user_domain_to_create)
            created_user_response = self.generic_create_use_case.execute(generic_request)
            created_user = created_user_response.data
            # ... lógica específica para senha
            return CreateUserResponse(
                # ... resposta
            )
    ```

-   **`ListUsersUseCase` (`project/core/domain/use_cases/user_use_cases.py`)**: Agora utiliza uma instância de `ListEntitiesUseCase[DomainUser]`.

    ```python
    class ListUsersUseCase:
        def __init__(self, user_repository: UserRepository):
            self.user_repository = user_repository
            self.generic_list_use_case = ListEntitiesUseCase[DomainUser](repository=user_repository)

        def execute(self, request: ListUsersRequest) -> ListUsersResponse:
            generic_request = GenericListRequest()
            list_entities_response = self.generic_list_use_case.execute(generic_request)
            users_domain = list_entities_response.items
            # ... mapeamento para CreateUserResponse
            return ListUsersResponse(users=users_response)
    ```

-   **`GetUserByIdUseCase` (`project/core/domain/use_cases/user_use_cases.py`)**: Agora utiliza uma instância de `GetEntityByIdUseCase[DomainUser]`.

    ```python
    class GetUserByIdUseCase:
        def __init__(self, user_repository: UserRepository):
            self.user_repository = user_repository
            self.generic_get_by_id_use_case = GetEntityByIdUseCase[DomainUser](repository=user_repository)

        def execute(self, request: GetUserByIdRequest) -> CreateUserResponse:
            generic_request = GenericDeleteRequest(id=request.user_id)
            get_entity_response = self.generic_get_by_id_use_case.execute(generic_request)
            user = get_entity_response.data
            # ... mapeamento para CreateUserResponse
            return CreateUserResponse(
                # ... resposta
            )
    ```

-   **`ChangeUserPasswordUseCase` (`project/core/domain/use_cases/user_use_cases.py`)**: Foi atualizado para usar `user_repository.get_by_id()` em vez de `get_user_by_id()`.

Com essa estrutura, a criação de novas entidades e suas operações CRUD básicas se torna muito mais rápida e padronizada, exigindo apenas a definição da entidade de domínio, a implementação do repositório e a configuração dos serializadores e views.
