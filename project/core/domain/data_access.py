"""Interfaces de acesso a dados (repositórios) do domínio.

Define contratos genéricos e específicos (UserRepository) que são
implementados na camada de infraestrutura.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from dataclasses import dataclass

from core.domain.entities.user import User

T = TypeVar("T")


@dataclass
class GenericRequest:
    """Base class for all request objects."""

    pass


@dataclass
class GenericGetByIdRequest(GenericRequest):
    """Request object for getting an entity by ID."""

    entity_id: str


@dataclass
class GenericDeleteRequest(GenericRequest):
    """Request object for deleting an entity by ID."""

    entity_id: str


@dataclass
class GenericListRequest(GenericRequest):
    """Request object for listing entities with pagination and filtering."""

    offset: int = 0
    limit: int = 50
    search_query: Optional[str] = None


@dataclass
class GenericCreateRequest(GenericRequest, Generic[T]):
    """Request object for creating an entity."""

    entity: T


@dataclass
class GenericUpdateRequest(GenericRequest, Generic[T]):
    """Request object for updating an entity."""

    entity: T


class GenericRepository(ABC, Generic[T]):
    """Contrato genérico de repositório para entidades de domínio."""

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Busca entidade por ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Lista todas as entidades."""
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        """Cria nova entidade."""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Atualiza entidade existente."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        """Remove entidade por ID."""
        pass


class UserRepository(GenericRepository[User]):
    """Contrato específico para operações com usuários do domínio."""

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuário por ID."""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email."""
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        """Cria novo usuário."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Atualiza usuário existente."""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """Remove usuário por ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        """Lista todos os usuários."""
        pass

    @abstractmethod
    def get_all_paginated_filtered(
        self, offset: int, limit: int, search_query: str | None
    ) -> tuple[List[User], int]:
        """Lista usuários com paginação e filtro."""
        pass
