"""Views de autenticação (login) para API v1."""

import logging

from core.api.deps import get_login_user_use_case
from core.api.throttles import LoginRateThrottle
from core.api.v1.serializers.user import LoginRequestSerializer, LoginResponseSerializer
from core.domain.exceptions import AuthenticationError
from core.domain.use_cases.user_use_cases import (
    LoginUserRequest,  # Corrigido o caminho de importação
)
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, Throttled
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class LoginAPIView(APIView):
    """
    Realiza login via email/senha e retorna tokens OAuth2.
    """

    permission_classes = (AllowAny,)
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        """Processa requisição de login."""
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_request = LoginUserRequest(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        login_user_use_case = get_login_user_use_case()
        email = login_request.email
        try:
            logger.info("Tentativa de login para email: %s", email)
            login_response = login_user_use_case.execute(login_request)
            response_serializer = LoginResponseSerializer(instance=login_response)
            logger.info("Login bem-sucedido para email: %s", email)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except (ValueError, AuthenticationError):
            logger.warning("Falha no login para email: %s", email)
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Throttled:
            raise  # Re-raise para DRF tratar
        except AuthenticationFailed as e:
            logger.warning("Falha de autenticação para email: %s", email)
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            logger.warning("Permissão negada para email: %s", email)
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            logger.error(
                "Erro inesperado no login para email: %s", email, exc_info=True
            )
            return Response(
                {"detail": "Erro interno do servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
