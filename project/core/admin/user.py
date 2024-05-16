from core.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    """Custom admin panel for the `User` model.

    This admin panel customizes the display and functionality of the `User` model in the admin panel.

    Attributes:
    ----------
        fieldsets (tuple): Sets of fields to display in the admin panel for different sections.
        add_fieldsets (tuple): Sets of fields to display in the admin panel for adding new users.
        list_display (tuple): Fields to display in the list view of users.
        search_fields (tuple): Fields to search for users.
        ordering (tuple): Fields to order users by.
    """

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
