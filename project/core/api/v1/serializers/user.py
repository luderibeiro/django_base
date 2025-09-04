"""Serializers para as operações de usuário na API v1."""

from core.domain.use_cases.user_use_cases import (
    ChangeUserPasswordRequest,
    ChangeUserPasswordResponse,
    CreateUserRequest,
    CreateUserResponse,
    ListUsersResponse,
    LoginUserRequest,
    LoginUserResponse,
)
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserReadSerializer(serializers.Serializer):
    """Representação somente leitura de um usuário (DTO)."""

    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def to_representation(self, instance: CreateUserResponse):
        """Converte instância para representação de dicionário."""
        return {
            "id": instance.id,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "is_active": instance.is_active,
            "is_staff": instance.is_staff,
            "is_superuser": instance.is_superuser,
        }


class UserSerializer(serializers.Serializer):
    """Representação básica de usuário em listagens (DTO)."""

    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def to_representation(self, instance: CreateUserResponse):
        """Converte instância para representação de dicionário."""
        return {
            "id": instance.id,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "is_active": instance.is_active,
            "is_staff": instance.is_staff,
            "is_superuser": instance.is_superuser,
        }


class UserListResponseSerializer(serializers.Serializer):
    """Envelope para resposta de listagem paginada de usuários."""

    users = UserSerializer(many=True)
    total_items = serializers.IntegerField()
    offset = serializers.IntegerField()
    limit = serializers.IntegerField()

    def to_representation(self, instance: ListUsersResponse):
        """Converte instância para representação de dicionário."""
        return {
            "items": [UserSerializer(user).data for user in instance.users],
            "total_items": instance.total_items,
            "offset": instance.offset,
            "limit": instance.limit,
        }


class ListUsersRequestSerializer(serializers.Serializer):
    """Entrada de paginação/consulta para listagem de usuários."""

    offset = serializers.IntegerField(default=0, required=False, min_value=0)
    limit = serializers.IntegerField(default=10, required=False, min_value=1)
    search_query = serializers.CharField(required=False, allow_blank=True)


class UserAlterPasswordSerializer(serializers.Serializer):
    """Entrada/saída para alteração de senha de usuário."""

    old_password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )
    new_password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )

    def to_internal_value(self, data):
        """Converte dados de entrada para DTO."""
        return ChangeUserPasswordRequest(
            user_id=self.context["view"].kwargs["pk"],
            old_password=data.get("old_password"),
            new_password=data.get("new_password"),
        )

    def to_representation(self, instance: ChangeUserPasswordResponse):
        """Converte instância para representação de dicionário."""
        return {"success": instance.success}


class UserCreateRequestSerializer(serializers.Serializer):
    """Entrada para criação de usuário."""

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )
    is_active = serializers.BooleanField(required=False, default=True)
    is_staff = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)

    def to_internal_value(self, data):
        """Converte dados de entrada para DTO."""
        return CreateUserRequest(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            password=data.get("password"),
            is_active=data.get("is_active", True),
            is_staff=data.get("is_staff", False),
            is_superuser=data.get("is_superuser", False),
        )


class LoginRequestSerializer(serializers.Serializer):
    """Entrada para login (email + senha)."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs: LoginUserRequest) -> LoginUserRequest:
        """Valida dados de entrada e retorna DTO."""
        # Simplesmente retorna o DTO, pois a validação de campo já ocorreu
        return attrs


class LoginResponseSerializer(serializers.Serializer):
    """Resposta do login com tokens de acesso/refresh."""

    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def to_representation(self, instance: LoginUserResponse):
        """Converte instância para representação de dicionário."""
        return {
            "id": instance.id,
            "email": instance.email,
            "access_token": instance.access_token,
            "refresh_token": instance.refresh_token,
        }
