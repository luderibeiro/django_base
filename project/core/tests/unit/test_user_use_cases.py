from unittest.mock import Mock

import pytest

from core.domain.entities.user import User as DomainUser
from core.domain.use_cases.user_use_cases import (
    ChangeUserPasswordRequest,
    ChangeUserPasswordResponse,
    CreateUserRequest,
    CreateUserResponse,
    GetUserByIdRequest,
    ListUsersRequest,
    ListUsersResponse,
    LoginUserRequest,
    LoginUserResponse,
    CreateUserUseCase,
    LoginUserUseCase,
    ChangeUserPasswordUseCase,
    ListUsersUseCase,
    GetUserByIdUseCase,
)


@pytest.fixture
def mock_user_repository():
    return Mock()


@pytest.fixture
def mock_auth_gateway():
    return Mock()


def test_create_user_use_case_success(mock_user_repository):
    # Given
    user_id = "123"
    email = "test@example.com"
    first_name = "Test"
    last_name = "User"
    password = "password123"

    mock_user_repository.create.return_value = DomainUser(
        id=user_id, email=email, first_name=first_name, last_name=last_name
    )

    use_case = CreateUserUseCase(user_repository=mock_user_repository)
    request = CreateUserRequest(
        email=email, first_name=first_name, last_name=last_name, password=password
    )

    # When
    response = use_case.execute(request)

    # Then
    mock_user_repository.create.assert_called_once()
    assert response.id == user_id
    assert response.email == email
    assert response.first_name == first_name
    assert response.last_name == last_name


def test_login_user_use_case_success(mock_user_repository, mock_auth_gateway):
    # Given
    user_id = "456"
    email = "login@example.com"
    password = "loginpassword123"
    access_token = "mock_access_token"
    refresh_token = "mock_refresh_token"

    mock_user = DomainUser(id=user_id, email=email, first_name="Login", last_name="User")
    mock_user_repository.get_user_by_email.return_value = mock_user
    mock_auth_gateway.check_password.return_value = True
    mock_auth_gateway.create_tokens.return_value = (access_token, refresh_token)

    use_case = LoginUserUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )
    request = LoginUserRequest(email=email, password=password)

    # When
    response = use_case.execute(request)

    # Then
    mock_user_repository.get_user_by_email.assert_called_once_with(email)
    mock_auth_gateway.check_password.assert_called_once_with(user_id, password)
    mock_auth_gateway.create_tokens.assert_called_once_with(user_id)
    assert response.id == user_id
    assert response.email == email
    assert response.access_token == access_token
    assert response.refresh_token == refresh_token


def test_login_user_use_case_invalid_credentials(mock_user_repository, mock_auth_gateway):
    # Given
    email = "invalid@example.com"
    password = "wrongpassword"

    mock_user_repository.get_user_by_email.return_value = None  # Usuário não encontrado

    use_case = LoginUserUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )
    request = LoginUserRequest(email=email, password=password)

    # When / Then
    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.execute(request)

    mock_user_repository.get_user_by_email.assert_called_once_with(email)
    mock_auth_gateway.check_password.assert_not_called()  # Não deve chamar se o usuário não for encontrado


def test_change_user_password_use_case_success(mock_user_repository, mock_auth_gateway):
    # Given
    user_id = "789"
    old_password = "oldpass"
    new_password = "newpass"

    mock_user_repository.get_by_id.return_value = DomainUser(id=user_id, email="user@example.com", first_name="A", last_name="B")
    mock_auth_gateway.check_password.return_value = True
    mock_auth_gateway.set_password.return_value = None

    use_case = ChangeUserPasswordUseCase(
        user_repository=mock_user_repository, auth_gateway=mock_auth_gateway
    )
    request = ChangeUserPasswordRequest(user_id=user_id, old_password=old_password, new_password=new_password)

    # When
    response = use_case.execute(request)

    # Then
    mock_auth_gateway.check_password.assert_called_once_with(user_id, old_password)
    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    mock_auth_gateway.set_password.assert_called_once_with(user_id, new_password)
    assert response.success is True


def test_list_users_use_case_success(mock_user_repository):
    # Given
    users_data = [
        DomainUser(id="1", email="user1@example.com", first_name="User", last_name="One"),
        DomainUser(id="2", email="user2@example.com", first_name="User", last_name="Two"),
    ]
    mock_user_repository.get_all.return_value = users_data

    use_case = ListUsersUseCase(user_repository=mock_user_repository)
    request = ListUsersRequest()

    # When
    response = use_case.execute(request)

    # Then
    mock_user_repository.get_all.assert_called_once()
    assert len(response.users) == 2
    assert response.users[0].email == "user1@example.com"


def test_get_user_by_id_use_case_success(mock_user_repository):
    # Given
    user_id = "123"
    mock_user_repository.get_by_id.return_value = DomainUser(
        id=user_id, email="test@example.com", first_name="Test", last_name="User"
    )

    use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
    request = GetUserByIdRequest(user_id=user_id)

    # When
    response = use_case.execute(request)

    # Then
    mock_user_repository.get_by_id.assert_called_once_with(user_id)
    assert response.id == user_id
    assert response.email == "test@example.com"


def test_get_user_by_id_use_case_not_found(mock_user_repository):
    # Given
    user_id = "non_existent_id"
    mock_user_repository.get_by_id.return_value = None

    use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
    request = GetUserByIdRequest(user_id=user_id)

    # When / Then
    with pytest.raises(ValueError, match="User not found"):
        use_case.execute(request)

    mock_user_repository.get_by_id.assert_called_once_with(user_id)
