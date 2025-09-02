import os
from typing import Tuple

from core.domain.gateways import AuthGateway
from django.contrib.auth import authenticate, get_user_model
from oauth2_provider.models import AccessToken, Application, RefreshToken

User = get_user_model()


class DjangoAuthGateway(AuthGateway):
    def check_password(self, user_id: str, password: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            return user.check_password(password)
        except User.DoesNotExist:
            return False

    def create_tokens(self, user_id: str) -> Tuple[str, str]:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError("User not found")

        # Para propósitos de desenvolvimento/exemplo, assumimos uma aplicação cliente padrão.
        # Em um cenário real, você buscaria a aplicação cliente associada à requisição.
        try:
            application = Application.objects.get(name="Default Application")
        except Application.DoesNotExist:
            # Se não existir, crie uma (apenas para ambiente de desenvolvimento/teste)
            application = Application.objects.create(
                name="Default Application",
                client_type="public",
                authorization_grant_type="password",
            )

        # Remove quaisquer tokens existentes para o usuário e aplicação
        AccessToken.objects.filter(user=user, application=application).delete()
        RefreshToken.objects.filter(user=user, application=application).delete()

        # Crie um novo access token
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            token="access_token_"
            + str(user_id)
            + "_"
            + os.urandom(30).hex(),  # Gerar um token real
            scope="read write",
            expires=AccessToken.get_expiration_delta(),
        )

        # Crie um novo refresh token
        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token="refresh_token_"
            + str(user_id)
            + "_"
            + os.urandom(30).hex(),  # Gerar um token real
            access_token=access_token,
        )

        return access_token.token, refresh_token.token

    def set_password(self, user_id: str, new_password: str) -> None:
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            raise ValueError("User not found")
