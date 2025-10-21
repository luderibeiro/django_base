"""Custom exception classes for the domain layer."""


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class ClientApplicationNotFound(Exception):
    """Raised when the client application is not found."""

    pass
