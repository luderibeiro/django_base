from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the `User` model.

    This serializer serializes user data, including groups the user belongs to.

    Attributes:
    ----------
        groups (SerializerMethodField): Serializer method field for user groups.
    """

    groups = serializers.SerializerMethodField()

    class Meta:
        """Meta class for the `UserSerializer`.

        Specifies the model and fields for serialization.

        Attributes:
        ----------
            model: The model to serialize.
            fields: The fields to include in the serialized output.
            read_only_fields: Fields that are read-only.
            extra_kwargs: Additional keyword arguments for fields.
        """

        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "groups",
        )
        read_only_fields = ("first_name", "last_name", "is_active", "groups")
        extra_kwargs = {
            "email": {"required": False, "validators": []},
            "password": {
                "required": True,
                "write_only": True,
            },
        }

    def get_groups(self, obj):
        """Retrieve groups the user belongs to.

        Args:
        ----
            obj: The user object.

        Returns:
        -------
            list: List of groups the user belongs to.
        """
        return list(obj.groups.all().values_list("name", flat=True))

    def create(self, validated_data):
        """Create a new user.

        Args:
        ----
            validated_data: Validated data for user creation.

        Returns:
        -------
            dict: The created user data.
        """
        return validated_data


class UserAlterPasswordSerializer(serializers.ModelSerializer):
    """Serializer for updating user password.

    This serializer is used for updating user passwords.

    Attributes:
    ----------
        password (CharField): Field for current user password.
        new_password (CharField): Field for new user password.
    """

    password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )
    new_password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )

    class Meta:
        """Meta class for the `UserAlterPasswordSerializer`.

        Specifies the model and fields for serialization.

        Attributes:
        ----------
            fields: The fields to include in the serialized output.
            read_only_fields: Fields that are read-only.
            model: The model to serialize.
        """

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "groups",
            "new_password",
        )
        read_only_fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "groups",
        )
        model = User

    def validate(self, validated_data):
        """Validate user data.

        Args:
        ----
            validated_data: Validated data for user update.

        Returns:
        -------
            dict: The validated user data.

        Raises:
        ------
            ValidationError: If the provided password does not match the user's current password.
        """
        user = User.objects.get(pk=self.context["view"].kwargs["pk"])
        if not user.check_password(validated_data["password"]):
            raise serializers.ValidationError("password does not match")
        return validated_data

    def update(self, instance, validated_data):
        """Update user password.

        Args:
        ----
            instance: The user instance.
            validated_data: Validated data for user update.

        Returns:
        -------
            User: The updated user instance.
        """
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.

    This serializer is used for creating new users.

    Attributes:
    ----------
        email (EmailField): Field for user email.
        password (CharField): Field for user password.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )

    class Meta:
        """
        Meta class for the `UserCreateSerializer`.

        Specifies the model and fields for serialization.

        Attributes:
        ----------
            model: The model to serialize.
            fields: The fields to include in the serialized output.
            read_only_fields: Fields that are read-only.
            extra_kwargs: Additional keyword arguments for fields.
        """

        model = User
        fields = (
            "id",
            "email",
            "password",
            "groups",
        )
        read_only_fields = ("id", "groups")
        extra_kwargs = {
            "password": {
                "required": True,
                "write_only": True,
            },
        }

    def create(self, validated_data):
        """
        Create a new user.

        Args:
        ----
            validated_data: Validated data for user creation.

            define username as the email address without the domain part.

        Returns:
        -------
            User: The created user instance.

        Raises:
        ------
            ValidationError: If the email is already in use.

        """

        username = validated_data.get("email").split("@")[0]
        validated_data["username"] = username
        user = User.objects.create_user(**validated_data)
        return user
