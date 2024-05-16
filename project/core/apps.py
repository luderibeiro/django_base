from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core app.

    This AppConfig sets the default auto field and name for the core app.

    Attributes:
    ----------
        default_auto_field (str): The default auto field used by models in the app.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
