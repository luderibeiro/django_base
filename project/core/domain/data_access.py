from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from core.domain.entities.user import User

T = TypeVar("T")


class GenericRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        pass


class UserRepository(GenericRepository[User]):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def get_all_paginated_filtered(
        self, offset: int, limit: int, search_query: str | None
    ) -> tuple[List[User], int]:
        pass
