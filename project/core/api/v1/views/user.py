from django.contrib.auth import get_user_model
from rest_framework import filters, generics
from rest_framework.permissions import IsAdminUser

from ..serializers.user import UserAlterPasswordSerializer, UserSerializer

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filterset_fields = ["first_name", "last_name", "email"]
    search_fields = ["first_name", "last_name", "email"]


class UserAlterPasswordAPIView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserAlterPasswordSerializer
    permission_classes = (IsAdminUser,)
