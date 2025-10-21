import os
import secrets
from datetime import timedelta
from typing import Tuple

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application, RefreshToken
import structlog

from core.domain.exceptions import AuthenticationError, ClientApplicationNotFound
from core.domain.gateways import AuthGateway

User = get_user_model()
logger = structlog.get_logger(__name__)


class DjangoAuthGateway(AuthGateway):
    def check_password(self, user_id: str, password: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            result = user.check_password(password)
            return result
        except User.DoesNotExist:
            return False

    def create_tokens(self, user_id: str) -> Tuple[str, str]:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationError("User not found")

        # Look up the client application based on the client_id from the request
        client_id = settings.OAUTH2_CLIENT_ID
        if not client_id:
            logger.error("OAUTH2_CLIENT_ID environment variable not defined")
            raise ValueError("OAUTH2_CLIENT_ID environment variable not defined")

        try:
            application = Application.objects.get(client_id=client_id)
        except Application.DoesNotExist:
            logger.error("Client application not found", client_id=client_id)
            raise ClientApplicationNotFound("Client application not found")

        # Remove any existing tokens for the user and application
        AccessToken.objects.filter(user=user, application=application).delete()
        RefreshToken.objects.filter(user=user, application=application).delete()

        # Create a new access token
        scope = os.getenv("OAUTH2_SCOPES", "read write")
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            token=secrets.token_urlsafe(32),  # Generate a real token
            scope=scope,
            expires=timezone.now()
            + timedelta(
                seconds=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"]
            ),
        )
        
        logger.info("Access token created successfully", user_id=str(user.id), application_id=str(application.id))

        # Create a new refresh token
        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token=secrets.token_urlsafe(32),  # Generate a real token
            access_token=access_token,
        )

        return access_token.token, refresh_token.token

    def set_password(self, user_id: str, new_password: str) -> None:
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            raise AuthenticationError("User not found")
