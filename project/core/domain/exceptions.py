"""
Custom domain exceptions for the Django Base template.

This module contains all custom exceptions used throughout the domain layer
to provide better error handling and more specific error messages.
"""


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class ClientApplicationNotFound(Exception):
    """Raised when OAuth2 client application is not found."""

    pass


class EntityNotFoundException(Exception):
    """Raised when an entity is not found in the repository."""

    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id '{entity_id}' not found")


class ValidationError(Exception):
    """Raised when domain validation fails."""

    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message)


class BusinessRuleViolationError(Exception):
    """Raised when a business rule is violated."""

    def __init__(self, message: str, rule_name: str = None):
        self.rule_name = rule_name
        super().__init__(message)


class DuplicateEntityError(Exception):
    """Raised when trying to create an entity that already exists."""

    def __init__(self, entity_type: str, field: str, value: str):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"{entity_type} with {field} '{value}' already exists")


class RepositoryError(Exception):
    """Base exception for repository operations."""

    pass


class DatabaseConnectionError(RepositoryError):
    """Raised when database connection fails."""

    pass


class TransactionError(RepositoryError):
    """Raised when a database transaction fails."""

    pass
