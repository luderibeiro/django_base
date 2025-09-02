from core.domain.data_access import UserRepository
from core.domain.gateways import AuthGateway
from core.domain.use_cases.user_use_cases import (
    ChangeUserPasswordUseCase,
    CreateUserUseCase,
    GetUserByIdUseCase,
    ListUsersUseCase,
    LoginUserUseCase,
)
from core.repositories.auth_gateway_impl import DjangoAuthGateway
from core.repositories.user_repository_impl import DjangoUserRepository


def get_user_repository() -> UserRepository:
    return DjangoUserRepository()


def get_create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase(user_repository=get_user_repository())


def get_auth_gateway() -> AuthGateway:
    return DjangoAuthGateway()


def get_login_user_use_case() -> LoginUserUseCase:
    return LoginUserUseCase(
        user_repository=get_user_repository(), auth_gateway=get_auth_gateway()
    )


def get_change_user_password_use_case() -> ChangeUserPasswordUseCase:
    return ChangeUserPasswordUseCase(
        user_repository=get_user_repository(), auth_gateway=get_auth_gateway()
    )


def get_list_users_use_case() -> ListUsersUseCase:
    return ListUsersUseCase(user_repository=get_user_repository())


def get_get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_repository=get_user_repository())
