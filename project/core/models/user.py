import uuid
from typing import ClassVar

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager para o modelo `User` baseado em email.

    Fornece criação consistente de usuários e superusuários com validações
    claras. Normalize email e centraliza atributos do PermissionsMixin.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Cria e persiste um usuário com email e senha.

        Parameters
        ----------
        email: str
            Endereço de email do usuário.
        password: str
            Senha em texto plano (será hasheada).
        **extra_fields:
            Campos adicionais do modelo.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        # Extrair campos de PermissionsMixin e AbstractBaseUser de extra_fields
        is_staff = extra_fields.pop("is_staff", False)
        is_superuser = extra_fields.pop("is_superuser", False)
        is_active = extra_fields.pop("is_active", True)

        user = self.model(email=email, **extra_fields)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Cria um usuário regular.

        Retorna a instância criada.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Cria um superusuário com validações obrigatórias de privilégios."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário autenticado por email.

    Guarda informações básicas de perfil e flags de permissão. Usa UUID
    como chave primária e segue boas práticas de segurança do Django.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    objects: ClassVar[UserManager] = UserManager()

    def __str__(self):
        """Representação string do usuário."""
        return self.email

    def get_full_name(self):
        """Retorna o nome completo do usuário.

        Returns
        -------
        str
            Nome completo (first_name + last_name).
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Retorna o primeiro nome do usuário.

        Returns
        -------
        str
            Primeiro nome do usuário.
        """
        return self.first_name
