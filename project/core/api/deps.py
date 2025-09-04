"""
Dependências e factories para casos de uso e gateways.

Fornece funções simples para construir implementações concretas dos
repositórios e casos de uso do domínio, centralizando a composição.
"""

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
    """Retorna implementação Django do `UserRepository`."""
    return DjangoUserRepository()


def get_create_user_use_case() -> CreateUserUseCase:
    """Constrói o caso de uso de criação de usuário."""
    return CreateUserUseCase(user_repository=get_user_repository())


def get_auth_gateway() -> AuthGateway:
    """Retorna o gateway de autenticação baseado no Django."""
    return DjangoAuthGateway()


def get_login_user_use_case() -> LoginUserUseCase:
    """Constrói o caso de uso de login (autenticação com tokens)."""
    return LoginUserUseCase(
        user_repository=get_user_repository(), auth_gateway=get_auth_gateway()
    )


def get_change_user_password_use_case() -> ChangeUserPasswordUseCase:
    """Constrói o caso de uso de troca de senha."""
    return ChangeUserPasswordUseCase(
        user_repository=get_user_repository(), auth_gateway=get_auth_gateway()
    )


def get_list_users_use_case() -> ListUsersUseCase:
    """Constrói o caso de uso de listagem de usuários."""
    return ListUsersUseCase(user_repository=get_user_repository())


def get_get_user_by_id_use_case() -> GetUserByIdUseCase:
    """Constrói o caso de uso de busca de usuário por ID."""
    return GetUserByIdUseCase(user_repository=get_user_repository())
