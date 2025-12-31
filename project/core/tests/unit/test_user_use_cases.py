import uuid
from unittest.mock import Mock

import pytest
from core.domain.data_access import UserRepository
from core.domain.entities.user import User as DomainUser
from core.domain.exceptions import AuthenticationError, EntityNotFoundException
from core.domain.gateways import AuthGateway
from core.domain.use_cases.user_use_cases import (
    ChangeUserPasswordRequest,
    ChangeUserPasswordResponse,
    ChangeUserPasswordUseCase,
    CreateUserRequest,
    CreateUserResponse,
    CreateUserUseCase,
    GetUserByIdRequest,
    GetUserByIdUseCase,
    ListUsersRequest,
    ListUsersResponse,
    ListUsersUseCase,
    LoginUserRequest,
    LoginUserResponse,
    LoginUserUseCase,
)


# Fixtures para mocks de repositório e gateway
@pytest.fixture
def mock_user_repository():
    return Mock(spec=UserRepository)


@pytest.fixture
def mock_auth_gateway():
    return Mock(spec=AuthGateway)


# Testes para CreateUserUseCase
def test_create_user_use_case_success(mock_user_repository):
    # Não precisamos gerar um user_id aqui, pois ele será gerado pelo mock_user_repository
    create_request = CreateUserRequest(
        email="new@example.com",
        first_name="New",
        last_name="User",
        password="newpassword123",
    )
    # Criar um DomainUser de retorno com um ID fixo para o mock
    # O ID real será gerado pelo mock_user_repository
    fixed_user_id = str(uuid.uuid4())
    returned_domain_user = DomainUser(
        id=fixed_user_id,
        email=create_request.email,
        first_name=create_request.first_name,
        last_name=create_request.last_name,
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )
    mock_user_repository.create.return_value = returned_domain_user

    use_case = CreateUserUseCase(user_repository=mock_user_repository)
    response = use_case.execute(create_request)

    # O DomainUser passado para o mock.create não precisa ter um ID,
    # pois o ID é gerado pelo repositório.
    # Apenas precisamos verificar se os outros campos estão corretos.
    expected_domain_user_sent_to_repo = DomainUser(
        email=create_request.email,
        first_name=create_request.first_name,
        last_name=create_request.last_name,
        is_active=True,
        is_staff=False,
        is_superuser=False,
        id=None,  # ID é gerado pelo repositório, não deve ser comparado aqui
    )
    mock_user_repository.create.assert_called_once()  # Apenas verifica que foi chamado
    # Verifique os atributos do objeto passado
    actual_call_arg = mock_user_repository.create.call_args[0][0]
    assert actual_call_arg.email == expected_domain_user_sent_to_repo.email
    assert actual_call_arg.first_name == expected_domain_user_sent_to_repo.first_name
    assert actual_call_arg.last_name == expected_domain_user_sent_to_repo.last_name

    assert response.id == fixed_user_id
    assert response.email == create_request.email


# Testes para LoginUserUseCase
def test_login_user_use_case_success(mock_user_repository, mock_auth_gateway):
    user_id = str(uuid.uuid4())
    login_request = LoginUserRequest(email="test@example.com", password="password123")
    domain_user = DomainUser(
        id=user_id, email=login_request.email, first_name="Test", last_name="User"
    )

    mock_user_repository.get_user_by_email.return_value = domain_user
    mock_auth_gateway.check_password.return_value = True
    mock_auth_gateway.create_tokens.return_value = (
        "access_token_mock",
        "refresh_token_mock",
    )

    use_case = LoginUserUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )
    response = use_case.execute(login_request)

    mock_user_repository.get_user_by_email.assert_called_once_with(login_request.email)
    mock_auth_gateway.check_password.assert_called_once_with(
        user_id, login_request.password
    )
    mock_auth_gateway.create_tokens.assert_called_once_with(user_id)
    assert response == LoginUserResponse(
        id=user_id,
        email=login_request.email,
        access_token="access_token_mock",
        refresh_token="refresh_token_mock",
    )


def test_login_user_use_case_user_not_found(mock_user_repository, mock_auth_gateway):
    login_request = LoginUserRequest(
        email="nonexistent@example.com", password="password123"
    )
    mock_user_repository.get_user_by_email.return_value = None

    use_case = LoginUserUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )

    with pytest.raises(AuthenticationError, match="Invalid credentials"):
        use_case.execute(login_request)

    mock_user_repository.get_user_by_email.assert_called_once_with(login_request.email)
    mock_auth_gateway.check_password.assert_not_called()
    mock_auth_gateway.create_tokens.assert_not_called()


def test_login_user_use_case_invalid_password(mock_user_repository, mock_auth_gateway):
    user_id = str(uuid.uuid4())
    login_request = LoginUserRequest(email="test@example.com", password="wrongpassword")
    domain_user = DomainUser(
        id=user_id, email=login_request.email, first_name="Test", last_name="User"
    )

    mock_user_repository.get_user_by_email.return_value = domain_user
    mock_auth_gateway.check_password.return_value = False

    use_case = LoginUserUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )

    with pytest.raises(AuthenticationError, match="Invalid credentials"):
        use_case.execute(login_request)

    mock_user_repository.get_user_by_email.assert_called_once_with(login_request.email)
    mock_auth_gateway.check_password.assert_called_once_with(
        user_id, login_request.password
    )
    mock_auth_gateway.create_tokens.assert_not_called()


# Testes para ChangeUserPasswordUseCase
def test_change_user_password_use_case_success(mock_user_repository, mock_auth_gateway):
    user_id = str(uuid.uuid4())
    change_request = ChangeUserPasswordRequest(
        user_id=user_id, old_password="oldpass", new_password="newpass"
    )
    domain_user = DomainUser(
        id=user_id, email="test@example.com", first_name="Test", last_name="User"
    )

    mock_auth_gateway.check_password.return_value = True
    mock_user_repository.get_by_id.return_value = domain_user
    mock_auth_gateway.set_password.return_value = None

    use_case = ChangeUserPasswordUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )
    response = use_case.execute(change_request)

    mock_auth_gateway.check_password.assert_called_once_with(user_id, "oldpass")
    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_auth_gateway.set_password.assert_called_once_with(user_id, "newpass")
    assert response == ChangeUserPasswordResponse(success=True)


def test_change_user_password_use_case_incorrect_old_password(
    mock_user_repository, mock_auth_gateway
):
    user_id = str(uuid.uuid4())
    change_request = ChangeUserPasswordRequest(
        user_id=user_id, old_password="wrongpass", new_password="newpass"
    )

    mock_auth_gateway.check_password.return_value = False

    use_case = ChangeUserPasswordUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )

    with pytest.raises(AuthenticationError, match="Old password is incorrect"):
        use_case.execute(change_request)

    mock_auth_gateway.check_password.assert_called_once_with(user_id, "wrongpass")
    mock_user_repository.get_by_id.assert_not_called()
    mock_auth_gateway.set_password.assert_not_called()


def test_change_user_password_use_case_user_not_found(
    mock_user_repository, mock_auth_gateway
):
    user_id = str(uuid.uuid4())
    change_request = ChangeUserPasswordRequest(
        user_id=user_id, old_password="oldpass", new_password="newpass"
    )

    mock_auth_gateway.check_password.return_value = True
    mock_user_repository.get_by_id.return_value = None

    use_case = ChangeUserPasswordUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )

    with pytest.raises(EntityNotFoundException):
        use_case.execute(change_request)

    mock_auth_gateway.check_password.assert_called_once_with(user_id, "oldpass")
    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_auth_gateway.set_password.assert_not_called()


# Testes para ListUsersUseCase
def test_list_users_use_case_success(mock_user_repository):
    domain_users = [
        DomainUser(
            id=str(uuid.uuid4()),
            email="user1@example.com",
            first_name="User1",
            last_name="Last1",
        ),
        DomainUser(
            id=str(uuid.uuid4()),
            email="user2@example.com",
            first_name="User2",
            last_name="Last2",
        ),
    ]
    total_items = len(domain_users)
    list_request = ListUsersRequest(offset=0, limit=10, search_query=None)

    mock_user_repository.get_all_paginated_filtered.return_value = (
        domain_users,
        total_items,
    )

    use_case = ListUsersUseCase(user_repository=mock_user_repository)
    response = use_case.execute(list_request)

    mock_user_repository.get_all_paginated_filtered.assert_called_once_with(
        offset=0, limit=10, search_query=None
    )
    assert len(response.users) == total_items
    assert response.total_items == total_items
    assert response.offset == list_request.offset
    assert response.limit == list_request.limit


def test_list_users_use_case_with_pagination_and_filter(mock_user_repository):
    domain_users = [
        DomainUser(
            id=str(uuid.uuid4()),
            email="filtered@example.com",
            first_name="Filtered",
            last_name="User",
        ),
    ]
    total_items = 1
    list_request = ListUsersRequest(offset=0, limit=1, search_query="Filtered")

    mock_user_repository.get_all_paginated_filtered.return_value = (
        domain_users,
        total_items,
    )

    use_case = ListUsersUseCase(user_repository=mock_user_repository)
    response = use_case.execute(list_request)

    mock_user_repository.get_all_paginated_filtered.assert_called_once_with(
        offset=0, limit=1, search_query="Filtered"
    )
    assert len(response.users) == 1
    assert response.total_items == 1
    assert response.users[0].email == "filtered@example.com"


# Testes para GetUserByIdUseCase
def test_get_user_by_id_use_case_success(mock_user_repository):
    user_id = str(uuid.uuid4())
    get_request = GetUserByIdRequest(user_id=user_id)
    domain_user = DomainUser(
        id=user_id, email="test@example.com", first_name="Test", last_name="User"
    )

    mock_user_repository.get_by_id.return_value = domain_user

    use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
    response = use_case.execute(get_request)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    assert response.id == user_id
    assert response.email == domain_user.email


def test_get_user_by_id_use_case_not_found(mock_user_repository):
    user_id = str(uuid.uuid4())
    get_request = GetUserByIdRequest(user_id=user_id)

    mock_user_repository.get_by_id.return_value = None

    use_case = GetUserByIdUseCase(user_repository=mock_user_repository)

    from core.domain.exceptions import EntityNotFoundException

    with pytest.raises(EntityNotFoundException):
        use_case.execute(get_request)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
