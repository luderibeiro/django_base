"""
Views da API para gerenciamento de usuários.

Contém as views para listagem, criação, recuperação e alteração de senha
de usuários, seguindo os padrões de Clean Architecture.
"""
import logging

from core.api.deps import (
    get_change_user_password_use_case,
    get_create_user_use_case,
    get_get_user_by_id_use_case,
    get_list_users_use_case,
)
from core.domain.use_cases.user_use_cases import GetUserByIdRequest, ListUsersRequest
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from ..serializers.user import (
    ListUsersRequestSerializer,
    UserAlterPasswordSerializer,
    UserCreateRequestSerializer,
    UserListResponseSerializer,
    UserReadSerializer,
)

logger = logging.getLogger(__name__)

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    """Lista usuários paginados e filtrados (apenas admins)."""

    serializer_class = UserListResponseSerializer
    permission_classes = (IsAdminUser,)  # Restaurado para IsAdminUser

    def list(self, request, *args, **kwargs):
        request_serializer = ListUsersRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        list_users_request = ListUsersRequest(
            offset=request_serializer.validated_data.get("offset", 0),
            limit=request_serializer.validated_data.get("limit", 10),
            search_query=request_serializer.validated_data.get("search_query", None),
        )

        list_users_use_case = get_list_users_use_case()
        list_users_response = list_users_use_case.execute(list_users_request)

        response_serializer = UserListResponseSerializer(instance=list_users_response)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class UserAlterPasswordAPIView(generics.UpdateAPIView):
    """Atualiza a senha de um usuário. Requer privilégio de admin."""

    queryset = User.objects.all()  # Alterado para permitir superusuários
    serializer_class = UserAlterPasswordSerializer
    permission_classes = (IsAdminUser,)  # Restaurado para IsAdminUser

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_password_request = serializer.validated_data

        change_password_use_case = get_change_user_password_use_case()
        try:
            change_password_response = change_password_use_case.execute(
                change_password_request
            )
            response_serializer = UserAlterPasswordSerializer(
                instance=change_password_response
            )
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Recupera um usuário pelo ID. Acesso restrito a admins."""

    serializer_class = UserReadSerializer
    permission_classes = (IsAdminUser,)  # Restaurado para IsAdminUser
    queryset = User.objects.all()  # Adicionado queryset

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs["pk"]
        get_user_request = GetUserByIdRequest(user_id=str(user_id))

        get_user_use_case = get_get_user_by_id_use_case()
        try:
            user_response = get_user_use_case.execute(get_user_request)
            response_serializer = UserReadSerializer(instance=user_response)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserCreateAPIView(generics.CreateAPIView):
    """Cria um novo usuário (público)."""

    queryset = User.objects.all()
    serializer_class = UserCreateRequestSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user_request = serializer.validated_data

        create_user_use_case = get_create_user_use_case()
        create_user_response = create_user_use_case.execute(create_user_request)
        read_serializer = UserReadSerializer(instance=create_user_response)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
