"""Casos de uso genéricos para operações CRUD no domínio."""

from dataclasses import dataclass
from typing import Generic, List, TypeVar

from core.domain.data_access import GenericRepository
from core.domain.exceptions import EntityNotFoundException

T = TypeVar("T")  # Representa a entidade de domínio


@dataclass
class GenericCreateRequest(Generic[T]):
    """
    Input para criação de entidade de domínio.
    """

    data: T


@dataclass
class GenericReadResponse(Generic[T]):
    """
    Resposta contendo uma entidade de domínio única.
    """

    data: T


@dataclass
class GenericListRequest:
    """Input para listagem (futuras opções de filtro/paginação)."""

    pass


@dataclass
class GenericListResponse(Generic[T]):
    """Resposta contendo uma lista de entidades de domínio."""

    items: List[T]


@dataclass
class GenericUpdateRequest(Generic[T]):
    """Input para atualização de entidade (id + dados)."""

    entity_id: str
    data: T


@dataclass
class GenericDeleteRequest:
    """Input mínimo para remoção/consulta por id."""

    entity_id: str


@dataclass
class GenericSuccessResponse:
    """Resposta padrão para operações bem-sucedidas sem payload."""

    success: bool = True


class UseCase(Generic[T]):
    """Marcador base para casos de uso parametrizados por entidade."""


class CreateEntityUseCase(UseCase[T]):
    """Cria uma entidade via repositório fornecido."""

    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericCreateRequest[T]) -> GenericReadResponse[T]:
        created_entity = self.repository.create(request.data)
        return GenericReadResponse(data=created_entity)


class ListEntitiesUseCase(UseCase[T]):
    """Lista todas as entidades do repositório (sem filtros)."""

    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericListRequest) -> GenericListResponse[T]:
        entities = self.repository.get_all()
        return GenericListResponse(items=entities)


class GetEntityByIdUseCase(UseCase[T]):
    """Busca entidade por id; lança erro se não encontrada."""

    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericGetByIdRequest) -> GenericReadResponse[T]:
        entity = self.repository.get_by_id(request.entity_id)
        if not entity:
            raise EntityNotFoundException("Entity", request.entity_id)
        return GenericReadResponse(data=entity)


class UpdateEntityUseCase(UseCase[T]):
    """Atualiza entidade existente após validar sua existência."""

    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericUpdateRequest[T]) -> GenericReadResponse[T]:
        # Primeiro, verificar se a entidade existe
        existing_entity = self.repository.get_by_id(request.entity_id)
        if not existing_entity:
            raise EntityNotFoundException("Entity", request.entity_id)

        # Assumimos que o request.data já contém a entidade atualizada completa
        # ou apenas os campos a serem atualizados. A lógica de merge pode ser mais complexa.
        # Por simplicidade, substituiremos a entidade com o que vem no request.data
        updated_entity = request.data
        updated_entity.id = (
            request.entity_id
        )  # Garantir que o ID da entidade sendo atualizada é o correto
        saved_entity = self.repository.update(updated_entity)
        return GenericReadResponse(data=saved_entity)


class DeleteEntityUseCase(UseCase[T]):
    """Remove entidade por id via repositório."""

    def __init__(self, repository: GenericRepository[T]):
        self.repository = repository

    def execute(self, request: GenericDeleteRequest) -> GenericSuccessResponse:
        self.repository.delete(request.entity_id)
        return GenericSuccessResponse(success=True)
