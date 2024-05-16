from typing import ClassVar
from django.contrib.auth.models import AbstractUser, BaseUserManager
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


class User(AbstractUser):
    """A custom user model that extends `AbstractUser`.

    Attributes:
    ----------
        email (str): The unique email address of the user.
        username (str): The unique username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        is_active (bool): Indicates if the user is active.
        is_staff (bool): Indicates if the user is a staff member.
        is_superuser (bool): Indicates if the user is a superuser.

    Attributes:
    ----------
        USERNAME_FIELD (str): The field used as the unique identifier for authentication (email).
        REQUIRED_FIELDS (ClassVar[list[str]]): A list of fields required when creating a user.

    Properties:
        is_admin (bool): Property to check if the user is a superuser (admin).
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser
