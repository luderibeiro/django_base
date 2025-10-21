import logging

from core.api.deps import (
    get_change_user_password_use_case,
    get_create_user_use_case,
    get_get_user_by_id_use_case,
    get_list_users_use_case,
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from core.domain.use_cases.user_use_cases import GetUserByIdRequest, ListUsersRequest

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
        logger.info("Listando usuários (admin)")
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
        logger.info(
            f"Listagem de usuários (admin) retornou {len(list_users_response.users)} usuários"
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class UserAlterPasswordAPIView(generics.UpdateAPIView):
    """Atualiza a senha de um usuário. Requer privilégio de admin."""

    queryset = User.objects.all()  # Alterado para permitir superusuários
    serializer_class = UserAlterPasswordSerializer
    permission_classes = (IsAdminUser,)  # Restaurado para IsAdminUser

    def update(self, request, *args, **kwargs):
        logger.info(f"Alterando senha do usuário com ID: {kwargs['pk']} (admin)")
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
            logger.info(
                f"Senha do usuário com ID: {kwargs['pk']} alterada com sucesso (admin)"
            )
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.warning(
                f"Falha ao alterar senha do usuário com ID: {kwargs['pk']} (admin) - {str(e)}"
            )
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Recupera um usuário pelo ID. Acesso restrito a admins."""

    serializer_class = UserReadSerializer
    permission_classes = (IsAdminUser,)  # Restaurado para IsAdminUser
    queryset = User.objects.all()  # Adicionado queryset

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs["pk"]
        logger.info(f"Recuperando usuário com ID: {user_id} (admin)")
        get_user_request = GetUserByIdRequest(user_id=str(user_id))

        get_user_use_case = get_get_user_by_id_use_case()
        try:
            user_response = get_user_use_case.execute(get_user_request)
            response_serializer = UserReadSerializer(instance=user_response)
            logger.info(f"Usuário com ID: {user_id} recuperado com sucesso (admin)")
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            logger.warning(
                f"Falha ao recuperar usuário com ID: {user_id} (admin) - {str(e)}"
            )
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserCreateAPIView(generics.CreateAPIView):
    """Cria um novo usuário (público)."""

    queryset = User.objects.all()
    serializer_class = UserCreateRequestSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        logger.info("Criando novo usuário (público)")
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            create_user_request = serializer.validated_data

            create_user_use_case = get_create_user_use_case()
            create_user_response = create_user_use_case.execute(create_user_request)
            read_serializer = UserReadSerializer(instance=create_user_response)
            logger.info(
                f"Usuário com ID: {create_user_response.id} criado com sucesso (público)"
            )
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning(f"Falha ao criar usuário (público) - {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
