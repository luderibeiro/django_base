from typing import ClassVar

from django.contrib.auth import get_user_model
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAdminUser

from ..serializers.user import (
    UserAlterPasswordSerializer,
    UserCreateSerializer,
    UserSerializer,
)

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    """List API view for users.

    This view lists non-superuser users.

    Attributes:
    ----------
        queryset: The queryset of users to display.
        serializer_class: The serializer class to use for user serialization.
        filterset_fields (ClassVar[list[str]]): List of fields for filtering users.
        search_fields (ClassVar[list[str]]): List of fields for searching users.
    """

    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filterset_fields: ClassVar[list[str]] = ["first_name", "last_name", "email"]
    search_fields: ClassVar[list[str]] = ["first_name", "last_name", "email"]


class UserAlterPasswordAPIView(generics.UpdateAPIView):
    """API view for altering user passwords.

    This view is used for updating non-superuser user passwords.

    Attributes:
    ----------
        queryset: The queryset of users to update passwords.
        serializer_class: The serializer class to use for password update.
        permission_classes: The permission classes required to access this view.
    """

    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserAlterPasswordSerializer
    permission_classes = (IsAdminUser,)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)
