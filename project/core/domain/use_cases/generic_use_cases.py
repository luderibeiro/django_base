from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from core.domain.data_access import GenericRepository

T = TypeVar("T")  # Representa a entidade de domínio


@dataclass
class GenericCreateRequest(Generic[T]):
    data: T


@dataclass
class GenericReadResponse(Generic[T]):
    data: T


@dataclass
class GenericListRequest:
    # Adicionar campos para filtragem, paginação, etc.
    pass


@dataclass
class GenericListResponse(Generic[T]):
    items: List[T]


@dataclass
class GenericUpdateRequest(Generic[T]):
    id: str
    data: T


@dataclass
class GenericDeleteRequest:
    id: str


@dataclass
class GenericSuccessResponse:
    success: bool = True


class UseCase(Generic[T]):
    pass


class CreateEntityUseCase(UseCase[T]):
    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericCreateRequest[T]) -> GenericReadResponse[T]:
        created_entity = self.repository.create(request.data)
        return GenericReadResponse(data=created_entity)


class ListEntitiesUseCase(UseCase[T]):
    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericListRequest) -> GenericListResponse[T]:
        entities = self.repository.get_all()
        return GenericListResponse(items=entities)


class GetEntityByIdUseCase(UseCase[T]):
    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(
        self, request: GenericDeleteRequest
    ) -> GenericReadResponse[T]:  # Usando GenericDeleteRequest para ID
        entity = self.repository.get_by_id(request.id)
        if not entity:
            raise ValueError("Entity not found")
        return GenericReadResponse(data=entity)


class UpdateEntityUseCase(UseCase[T]):
    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericUpdateRequest[T]) -> GenericReadResponse[T]:
        # Primeiro, verificar se a entidade existe
        existing_entity = self.repository.get_by_id(request.id)
        if not existing_entity:
            raise ValueError("Entity not found")

        # Assumimos que o request.data já contém a entidade atualizada completa
        # ou apenas os campos a serem atualizados. A lógica de merge pode ser mais complexa.
        # Por simplicidade, substituiremos a entidade com o que vem no request.data
        updated_entity = request.data
        updated_entity.id = (
            request.id
        )  # Garantir que o ID da entidade sendo atualizada é o correto
        saved_entity = self.repository.update(updated_entity)
        return GenericReadResponse(data=saved_entity)


class DeleteEntityUseCase(UseCase[T]):
    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericDeleteRequest) -> GenericSuccessResponse:
        self.repository.delete(request.id)
        return GenericSuccessResponse(success=True)
