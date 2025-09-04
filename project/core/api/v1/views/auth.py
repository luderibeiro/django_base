"""Views de autenticação (login) para API v1."""

from core.api.deps import get_login_user_use_case
from core.api.v1.serializers.user import LoginRequestSerializer, LoginResponseSerializer
from core.domain.use_cases.user_use_cases import (
    LoginUserRequest,  # Corrigido o caminho de importação
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginAPIView(APIView):
    """
    Realiza login via email/senha e retorna tokens OAuth2.
    """

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """Processa requisição de login."""
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_request = LoginUserRequest(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        login_user_use_case = get_login_user_use_case()
        try:
            login_response = login_user_use_case.execute(login_request)
            response_serializer = LoginResponseSerializer(instance=login_response)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
