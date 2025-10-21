import datetime
import uuid
from datetime import timedelta
from unittest.mock import ANY, Mock, patch

import pytest
from core.domain.entities.user import (
    User as DomainUser,  # Para simular o usuário do domínio
)

# Importa o modelo real do Django para usar suas exceções
from core.models.user import User as DjangoUserModel
from core.repositories.auth_gateway_impl import DjangoAuthGateway
from django.conf import settings
from django.utils import timezone
from oauth2_provider.models import Application  # Importar o modelo Application real


# Mock para o modelo de usuário do Django
class MockDjangoUser:
    def __init__(
        self,
        id,
        email,
        password=None,
        is_active=True,
        is_staff=False,
        is_superuser=False,
    ):
        self.id = id
        self.email = email
        self._password = password  # Simula o password hash
        self.is_active = is_active
        self.is_staff = is_staff
        self.is_superuser = is_superuser
        self.save = Mock()  # Mockar o método save

    def check_password(self, raw_password):
        # Simula a verificação de senha. Em um teste real, você usaria um hash.
        return raw_password == self._password

    def set_password(self, new_password):
        self._password = new_password  # Simula a definição de senha

    def save(self):
        pass  # Mock save

    def __str__(self):
        return self.email


# Adiciona um atributo `objects` que se comporta como um manager para o MockDjangoUser
MockDjangoUser.objects = Mock()


# Mock para o modelo Application do oauth2_provider
class MockApplication:
    def __init__(
        self,
        name,
        client_type,
        authorization_grant_type,
        id=1,
        client_id="test-client-id",
        client_secret="test-client-secret",
        user_id=1,
    ):
        self.id = id
        self.name = name
        self.client_type = client_type
        self.authorization_grant_type = authorization_grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id

    def __str__(self):
        return f"<MockApplication {self.client_id}>"


# Mock para AccessToken e RefreshToken
class MockAccessToken:
    def __init__(self, user, application, token, scope, expires):
        self.user = user
        self.application = application
        self.token = token
        self.scope = scope
        self.expires = expires


class MockRefreshToken:
    def __init__(self, user, application, token, access_token):
        self.user = user
        self.application = application
        self.token = token
        self.access_token = access_token


@pytest.fixture
def setup_auth_gateway_mocks():
    mock_user_model = Mock()
    mock_user_model.objects = Mock()
    mock_user_model.DoesNotExist = (
        DjangoUserModel.DoesNotExist
    )  # Usar a exceção real do Django

    # Mock do manager para Application
    mock_application_manager = Mock()
    mock_application_instance_for_get = MockApplication(
        name="Default Application",
        client_type="public",
        authorization_grant_type="password",
        id=1,
        client_id="test-client-id",
        client_secret="test-client-secret",
        user_id=1,
    )
    # Por padrão, retorna a instância — testes individuais podem sobrescrever side_effect quando necessário
    mock_application_manager.get.return_value = mock_application_instance_for_get
    mock_application_manager.create.return_value = mock_application_instance_for_get

    # Mock do manager para AccessToken
    mock_access_token_manager = Mock()
    mock_access_token_manager.filter.return_value = Mock()
    mock_access_token_manager.filter.return_value.delete.return_value = None
    mock_access_token_instance_for_create = MockAccessToken(
        user=None,
        application=None,
        token="mock_access_token",
        scope="read write",
        expires=None,  # Definir expires depois
    )
    mock_access_token_manager.create.return_value = (
        mock_access_token_instance_for_create
    )

    # Mock do manager para RefreshToken
    mock_refresh_token_manager = Mock()
    mock_refresh_token_manager.filter.return_value = Mock()
    mock_refresh_token_manager.filter.return_value.delete.return_value = None
    mock_refresh_token_instance_for_create = MockRefreshToken(
        user=None, application=None, token="mock_refresh_token", access_token=None
    )
    mock_refresh_token_manager.create.return_value = (
        mock_refresh_token_instance_for_create
    )

    with (
        patch("core.repositories.auth_gateway_impl.User", new=mock_user_model),
        patch(
            "oauth2_provider.models.Application.objects", new=mock_application_manager
        ),
        patch(
            "oauth2_provider.models.AccessToken.objects", new=mock_access_token_manager
        ),
        patch(
            "oauth2_provider.models.RefreshToken.objects",
            new=mock_refresh_token_manager,
        ),
        patch(
            "django.conf.settings.OAUTH2_PROVIDER",
            {"ACCESS_TOKEN_EXPIRE_SECONDS": 3600},
        ),
        patch(
            "django.utils.timezone.now",
            return_value=timezone.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc),
        ) as mock_now,
    ):
        # Agora, defina expires com o mock_now para garantir consistência
        mock_access_token_instance_for_create.expires = (
            mock_now.return_value + timedelta(seconds=3600)
        )
        # também "preencha" referências internas para que asserts que comparam objetos funcionem
        mock_access_token_instance_for_create.user = None
        mock_access_token_instance_for_create.application = (
            mock_application_instance_for_get
        )
        mock_refresh_token_instance_for_create.access_token = (
            mock_access_token_instance_for_create
        )
        yield {
            "user_model": mock_user_model,
            "application_manager": mock_application_manager,
            "access_token_manager": mock_access_token_manager,
            "refresh_token_manager": mock_refresh_token_manager,
            "mock_now": mock_now,
            "mock_application_instance_for_get": mock_application_instance_for_get,
            "mock_access_token_instance_for_create": mock_access_token_instance_for_create,
            "mock_refresh_token_instance_for_create": mock_refresh_token_instance_for_create,
        }


# Testes para check_password
def test_check_password_success(setup_auth_gateway_mocks):
    mocks = setup_auth_gateway_mocks
    user_id = str(uuid.uuid4())
    mock_user = MockDjangoUser(
        id=user_id, email="test@example.com", password="correct_password"
    )
    mocks["user_model"].objects.get.return_value = mock_user

    gateway = DjangoAuthGateway()
    result = gateway.check_password(user_id, "correct_password")

    mocks["user_model"].objects.get.assert_called_once_with(id=user_id)
    assert result is True


def test_check_password_failure_wrong_password(setup_auth_gateway_mocks):
    mocks = setup_auth_gateway_mocks
    user_id = str(uuid.uuid4())
    mock_user = MockDjangoUser(
        id=user_id, email="test@example.com", password="correct_password"
    )
    mocks["user_model"].objects.get.return_value = mock_user

    gateway = DjangoAuthGateway()
    result = gateway.check_password(user_id, "wrong_password")

    mocks["user_model"].objects.get.assert_called_once_with(id=user_id)
    assert result is False


def test_check_password_failure_user_not_found(setup_auth_gateway_mocks):
    mocks = setup_auth_gateway_mocks
    user_id = str(uuid.uuid4())
    mocks["user_model"].objects.get.side_effect = mocks["user_model"].DoesNotExist

    gateway = DjangoAuthGateway()
    result = gateway.check_password(user_id, "any_password")

    mocks["user_model"].objects.get.assert_called_once_with(id=user_id)
    assert result is False


# Testes para create_tokens
def test_create_tokens_success_existing_application(setup_auth_gateway_mocks):
    mocks = setup_auth_gateway_mocks
    user_id = str(uuid.uuid4())
    mock_user = MockDjangoUser(id=user_id, email="test@example.com")

    # Por padrão, o manager.get já retorna a instância configurada no fixture
    mocks["user_model"].objects.get.return_value = mock_user

    gateway = DjangoAuthGateway()
    access_token, refresh_token = gateway.create_tokens(user_id)

    mocks["user_model"].objects.get.assert_called_once_with(id=user_id)
    mocks["application_manager"].get.assert_called_once_with(client_id="test-client-id")
    # A aplicação não deve ser criada se já existe
    mocks["application_manager"].create.assert_not_called()

    mocks["access_token_manager"].filter.assert_called_once()
    mocks["refresh_token_manager"].filter.assert_called_once()
    mocks["access_token_manager"].create.assert_called_once_with(
        user=mock_user,
        application=mocks["mock_application_instance_for_get"],
        token=ANY,  # Token é gerado aleatoriamente
        scope="read write",
        expires=ANY,  # Usar ANY para a data de expiração
    )
    mocks["refresh_token_manager"].create.assert_called_once_with(
        user=mock_user,
        application=mocks["mock_application_instance_for_get"],
        token=ANY,  # Token é gerado aleatoriamente
        access_token=mocks["mock_access_token_instance_for_create"],
    )

    assert access_token == "mock_access_token"
    assert refresh_token == "mock_refresh_token"


def test_create_tokens_success_new_application(setup_auth_gateway_mocks):
    """Test que verifica o comportamento quando a aplicação OAuth2 não existe.

    O comportamento esperado é que uma exceção ClientApplicationNotFound seja levantada
    quando a aplicação não é encontrada, pois o gateway não cria aplicações automaticamente.
    """
    mocks = setup_auth_gateway_mocks
    user_id = str(uuid.uuid4())
    mock_user = MockDjangoUser(id=user_id, email="test@example.com")

    # Configura o side_effect para simular que a aplicação NÃO existe -> raise da exceção
    mocks["application_manager"].get.side_effect = Application.DoesNotExist()

    mocks["user_model"].objects.get.return_value = mock_user

    gateway = DjangoAuthGateway()

    from core.domain.exceptions import ClientApplicationNotFound

    with pytest.raises(ClientApplicationNotFound, match="Client application not found"):
        gateway.create_tokens(user_id)

    mocks["user_model"].objects.get.assert_called_once_with(id=user_id)
    mocks["application_manager"].get.assert_called_once_with(client_id="test-client-id")


def test_create_tokens_user_not_found(setup_auth_gateway_mocks):
    mocks = setup_auth_gateway_mocks
    user_id = str(uuid.uuid4())
    mocks["user_model"].objects.get.side_effect = mocks["user_model"].DoesNotExist

    gateway = DjangoAuthGateway()

    from core.domain.exceptions import AuthenticationError

    with pytest.raises(AuthenticationError, match="User not found"):
        gateway.create_tokens(user_id)

    mocks["user_model"].objects.get.assert_called_once_with(id=user_id)
    mocks["application_manager"].get.assert_not_called()


# Testes para set_password
def test_set_password_success(setup_auth_gateway_mocks):
    mocks = setup_auth_gateway_mocks
    user_id = str(uuid.uuid4())
    mock_user = MockDjangoUser(
        id=user_id, email="test@example.com", password="old_password"
    )
    mocks["user_model"].objects.get.return_value = mock_user

    gateway = DjangoAuthGateway()
    gateway.set_password(user_id, "new_password")

    mocks["user_model"].objects.get.assert_called_once_with(id=user_id)
    assert (
        mock_user._password == "new_password"
    )  # Verifica se a senha mockada foi atualizada
    mock_user.save.assert_called_once()  # Verifica se o método save foi chamado


def test_set_password_user_not_found(setup_auth_gateway_mocks):
    mocks = setup_auth_gateway_mocks
    user_id = str(uuid.uuid4())
    mocks["user_model"].objects.get.side_effect = mocks["user_model"].DoesNotExist

    gateway = DjangoAuthGateway()

    from core.domain.exceptions import AuthenticationError

    with pytest.raises(AuthenticationError, match="User not found"):
        gateway.set_password(user_id, "new_password")

    mocks["user_model"].objects.get.assert_called_once_with(id=user_id)
