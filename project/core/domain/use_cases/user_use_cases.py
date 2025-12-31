import logging
from dataclasses import dataclass
from typing import Optional

from core.domain.data_access import UserRepository
from core.domain.entities.user import User as DomainUser
from core.domain.gateways import AuthGateway
from core.domain.use_cases.generic_use_cases import (
    CreateEntityUseCase,
    GenericCreateRequest,
    GenericDeleteRequest,
    GenericReadResponse,
    GetEntityByIdUseCase,
    ListEntitiesUseCase,
)

logger = logging.getLogger(__name__)


@dataclass
class CreateUserRequest:
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False


@dataclass
class CreateUserResponse:
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool


class CreateUserUseCase:
    """Caso de uso para criação de usuários.

    Constrói a entidade de domínio e delega ao caso de uso genérico
    de criação. A definição de senha deve ocorrer por gateway/autenticação.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.generic_create_use_case = CreateEntityUseCase[DomainUser](
            repository=user_repository
        )

    def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        user_domain_to_create = DomainUser(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            is_active=request.is_active,
            is_staff=request.is_staff,
            is_superuser=request.is_superuser,
        )
        generic_request = GenericCreateRequest(data=user_domain_to_create)
        created_user_response = self.generic_create_use_case.execute(generic_request)
        created_user = created_user_response.data

        # Aqui você precisaria adicionar a lógica para definir a senha do usuário
        # Isso é uma operação específica do usuário e não deve ser genérica.
        # Por enquanto, mantemos a simplicidade.

        return CreateUserResponse(
            id=created_user.id,
            email=created_user.email,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            is_active=created_user.is_active,
            is_staff=created_user.is_staff,
            is_superuser=created_user.is_superuser,
        )


@dataclass
class LoginUserRequest:
    email: str
    password: str


@dataclass
class LoginUserResponse:
    id: str
    email: str
    access_token: str
    refresh_token: str


class LoginUserUseCase:
    """Caso de uso para autenticação e geração de tokens."""

    def __init__(self, user_repository: UserRepository, auth_gateway: AuthGateway):
        self.user_repository = user_repository
        self.auth_gateway = auth_gateway

    def execute(self, request: LoginUserRequest) -> LoginUserResponse:
        logger.info("Attempting to log in user with email: %s", request.email)
        user = self.user_repository.get_user_by_email(request.email)
        if not user:
            logger.warning("Login failed: User not found for email %s", request.email)
            raise ValueError("Invalid credentials")

        if not self.auth_gateway.check_password(user.id, request.password):
            logger.warning("Login failed: Invalid password for user ID %s", user.id)
            raise ValueError("Invalid credentials")

        access_token, refresh_token = self.auth_gateway.create_tokens(user.id)
        logger.info(
            "User %s logged in successfully. User ID: %s", request.email, user.id
        )

        return LoginUserResponse(
            id=user.id,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token,
        )


@dataclass
class ChangeUserPasswordRequest:
    user_id: str
    old_password: str
    new_password: str


@dataclass
class ChangeUserPasswordResponse:
    success: bool


class ChangeUserPasswordUseCase:
    """Caso de uso para troca segura de senha de usuário."""

    def __init__(self, user_repository: UserRepository, auth_gateway: AuthGateway):
        self.user_repository = user_repository
        self.auth_gateway = auth_gateway

    def execute(self, request: ChangeUserPasswordRequest) -> ChangeUserPasswordResponse:
        if not self.auth_gateway.check_password(request.user_id, request.old_password):
            raise ValueError("Old password is incorrect")

        user = self.user_repository.get_by_id(request.user_id)
        if not user:
            raise ValueError("User not found")

        self.auth_gateway.set_password(user.id, request.new_password)

        return ChangeUserPasswordResponse(success=True)


@dataclass
class ListUsersRequest:
    offset: int = 0
    limit: int = 10
    search_query: Optional[str] = None


@dataclass
class ListUsersResponse:
    users: list[CreateUserResponse]
    total_items: int
    offset: int
    limit: int


class ListUsersUseCase:
    """Caso de uso para listagem paginada e filtrada de usuários."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        # Não usaremos o generic_list_use_case diretamente aqui,
        # pois precisamos de uma lógica de paginação/filtragem mais específica.

    def execute(self, request: ListUsersRequest) -> ListUsersResponse:
        logger.info(
            "Listing users with offset: %s, limit: %s, search_query: %s",
            request.offset,
            request.limit,
            request.search_query,
        )
        users_domain, total_items = self.user_repository.get_all_paginated_filtered(
            offset=request.offset,
            limit=request.limit,
            search_query=request.search_query,
        )
        logger.debug(
            "Found %s users in total, returning %s users.",
            total_items,
            len(users_domain),
        )

        users_response = [
            CreateUserResponse(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser,
            )
            for user in users_domain
        ]
        return ListUsersResponse(
            users=users_response,
            total_items=total_items,
            offset=request.offset,
            limit=request.limit,
        )


@dataclass
class GetUserByIdRequest:
    user_id: str


class GetUserByIdUseCase:
    """Caso de uso para obter usuário por identificador único."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.generic_get_by_id_use_case = GetEntityByIdUseCase[DomainUser](
            repository=user_repository
        )

    def execute(self, request: GetUserByIdRequest) -> CreateUserResponse:
        generic_request = GenericDeleteRequest(
            id=request.user_id
        )  # Usando GenericDeleteRequest para ID
        get_entity_response = self.generic_get_by_id_use_case.execute(generic_request)
        user = get_entity_response.data

        return CreateUserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
        )
