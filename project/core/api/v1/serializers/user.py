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
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def to_representation(self, instance: CreateUserResponse):
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
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def to_representation(self, instance: CreateUserResponse):
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
    users = UserSerializer(many=True)

    def to_representation(self, instance: ListUsersResponse):
        return {"users": [UserSerializer(user).data for user in instance.users]}


class UserAlterPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )
    new_password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )

    def to_internal_value(self, data):
        return ChangeUserPasswordRequest(
            user_id=self.context["view"].kwargs["pk"],
            old_password=data.get("old_password"),
            new_password=data.get("new_password"),
        )

    def to_representation(self, instance: ChangeUserPasswordResponse):
        return {"success": instance.success}


class UserCreateRequestSerializer(serializers.Serializer):
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
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def to_internal_value(self, data):
        return LoginUserRequest(
            email=data.get("email"),
            password=data.get("password"),
        )


class LoginResponseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def to_representation(self, instance: LoginUserResponse):
        return {
            "id": instance.id,
            "email": instance.email,
            "access_token": instance.access_token,
            "refresh_token": instance.refresh_token,
        }
