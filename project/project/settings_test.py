from .settings import *

# Override default database to use SQLite in-memory for tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Explicitly define ROOT_URLCONF for tests
ROOT_URLCONF = "project.urls"

# Secret key for tests to enable session signing and similar features
SECRET_KEY = "django-insecure-test-key"

# Explicitly define INSTALLED_APPS for tests to ensure all necessary apps are loaded.
INSTALLED_APPS = [
    "jazzmin",
    "rest_framework",
    "oauth2_provider",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "core",
    "cart",
]

# Explicitly define MIDDLEWARE for tests to ensure all necessary middleware classes are loaded.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configure REST_FRAMEWORK for tests to allow simpler authentication and permissions.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",  # Prioriza OAuth2
    ],
    "EXCEPTION_HANDLER": "core.middleware.custom_exception_middleware.custom_exception_handler",  # Reativa o handler de exceções customizado para testes
}

if DEBUG:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append(
        "rest_framework.authentication.SessionAuthentication"
    )
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append(
        "rest_framework.authentication.BasicAuthentication"
    )

# Ensure DEBUG is True for tests if needed, or adjust as per your testing strategy
DEBUG = True

# Disable logging to console during tests if it clutters output
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "core": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "project": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
