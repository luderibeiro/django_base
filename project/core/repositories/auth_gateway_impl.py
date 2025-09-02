from typing import Tuple

from core.domain.gateways import AuthGateway
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class DjangoAuthGateway(AuthGateway):
    def check_password(self, user_id: str, password: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            return user.check_password(password)
        except User.DoesNotExist:
            return False

    def create_tokens(self, user_id: str) -> Tuple[str, str]:
        # Aqui você integraria com django-oauth-toolkit ou outra biblioteca de token.
        # Por enquanto, retorne tokens de exemplo.
        return "dummy_access_token_for_user_" + str(
            user_id
        ), "dummy_refresh_token_for_user_" + str(user_id)

    def set_password(self, user_id: str, new_password: str) -> None:
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            raise ValueError("User not found")
