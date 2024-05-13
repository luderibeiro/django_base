from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "groups",
            "phone",
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
        return list(obj.groups.all().values_list("name", flat=True))


    def create(self, validated_data):
        return validated_data


class UserAlterPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )
    new_password = serializers.CharField(
        write_only=True, required=True, min_length=6, allow_blank=False
    )

    class Meta:
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
        user = User.objects.get(pk=self.context["view"].kwargs["pk"])
        if not user.check_password(validated_data["password"]):
            raise serializers.ValidationError("password does not match")
        return validated_data

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance
