from typing import ClassVar
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """A model manager for the `User` model with no username field.

    Methods:
    -------
        _create_user: Internal method to create and save a user with the given email and password.
        create_user: Creates and saves a regular user with the given email and password.
        create_superuser: Creates and saves a superuser with the given email and password.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Creates and saves a user with the given email and password.

        Args:
        ----
            email (str): The email address of the user.
            password (str): The password of the user.
            **extra_fields: Additional fields for the user model.

        Returns:
        -------
            User: The created user object.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a regular user with the given email and password.

        Args:
        ----
            email (str): The email address of the user.
            password (str, optional): The password of the user.
            **extra_fields: Additional fields for the user model.

        Returns:
        -------
            User: The created user object.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a superuser with the given email and password.

        Args:
        ----
            email (str): The email address of the superuser.
            password (str): The password of the superuser.
            **extra_fields: Additional fields for the user model.

        Returns:
        -------
            User: The created superuser object.

        Raises:
        ------
            ValueError: If is_staff or is_superuser is not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """A custom user model that extends `AbstractBaseUser` and `PermissionsMixin`.

    Attributes:
    ----------
        email (str): The unique email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.

    Attributes:
    ----------
        USERNAME_FIELD (str): The field used as the unique identifier for authentication (email).
        REQUIRED_FIELDS (ClassVar[list[str]]): A list of fields required when creating a user.

    Properties:
        is_admin (bool): Property to check if the user is a superuser (admin).
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    objects: ClassVar[UserManager] = UserManager()

    def __str__(self):
        return self.email
