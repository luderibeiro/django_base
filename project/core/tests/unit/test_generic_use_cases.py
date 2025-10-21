import uuid
from unittest.mock import Mock

import pytest
from core.domain.data_access import GenericRepository
from core.domain.entities.user import (
    User as DomainUser,  # Usar DomainUser como entidade de exemplo
)
from core.domain.exceptions import EntityNotFoundException
from core.domain.use_cases.generic_use_cases import (
    CreateEntityUseCase,
    DeleteEntityUseCase,
    GenericCreateRequest,
    GenericDeleteRequest,
    GenericListRequest,
    GenericListResponse,
    GenericReadResponse,
    GenericSuccessResponse,
    GenericUpdateRequest,
    GetEntityByIdUseCase,
    ListEntitiesUseCase,
    UpdateEntityUseCase,
)


# Fixture para um repositório genérico mock
@pytest.fixture
def mock_generic_repository():
    return Mock(spec=GenericRepository)


# Testes para CreateEntityUseCase
def test_create_entity_use_case_success(mock_generic_repository):
    entity_id = str(uuid.uuid4())
    domain_user = DomainUser(
        id=entity_id, email="test@example.com", first_name="Test", last_name="User"
    )
    mock_generic_repository.create.return_value = domain_user

    use_case = CreateEntityUseCase(repository=mock_generic_repository)
    request = GenericCreateRequest(data=domain_user)
    response = use_case.execute(request)

    mock_generic_repository.create.assert_called_once_with(domain_user)
    assert response == GenericReadResponse(data=domain_user)


# Testes para ListEntitiesUseCase
def test_list_entities_use_case_success(mock_generic_repository):
    domain_users = [
        DomainUser(
            id=str(uuid.uuid4()),
            email="user1@example.com",
            first_name="User1",
            last_name="Last1",
        ),
        DomainUser(
            id=str(uuid.uuid4()),
            email="user2@example.com",
            first_name="User2",
            last_name="Last2",
        ),
    ]
    mock_generic_repository.get_all.return_value = domain_users

    use_case = ListEntitiesUseCase(repository=mock_generic_repository)
    request = GenericListRequest()
    response = use_case.execute(request)

    mock_generic_repository.get_all.assert_called_once()
    assert response == GenericListResponse(items=domain_users)


def test_list_entities_use_case_empty(mock_generic_repository):
    mock_generic_repository.get_all.return_value = []

    use_case = ListEntitiesUseCase(repository=mock_generic_repository)
    request = GenericListRequest()
    response = use_case.execute(request)

    mock_generic_repository.get_all.assert_called_once()
    assert response == GenericListResponse(items=[])


# Testes para GetEntityByIdUseCase
def test_get_entity_by_id_use_case_success(mock_generic_repository):
    entity_id = str(uuid.uuid4())
    domain_user = DomainUser(
        id=entity_id, email="test@example.com", first_name="Test", last_name="User"
    )
    mock_generic_repository.get_by_id.return_value = domain_user

    use_case = GetEntityByIdUseCase(repository=mock_generic_repository)
    request = GenericDeleteRequest(
        id=entity_id
    )  # Usando GenericDeleteRequest como um request para ID
    response = use_case.execute(request)

    mock_generic_repository.get_by_id.assert_called_once_with(entity_id)
    assert response == GenericReadResponse(data=domain_user)


def test_get_entity_by_id_use_case_not_found(mock_generic_repository):
    entity_id = str(uuid.uuid4())
    mock_generic_repository.get_by_id.return_value = None

    use_case = GetEntityByIdUseCase(repository=mock_generic_repository)
    request = GenericDeleteRequest(id=entity_id)

    with pytest.raises(EntityNotFoundException):
        use_case.execute(request)

    mock_generic_repository.get_by_id.assert_called_once_with(entity_id)


# Testes para UpdateEntityUseCase
def test_update_entity_use_case_success(mock_generic_repository):
    entity_id = str(uuid.uuid4())
    existing_user = DomainUser(
        id=entity_id, email="old@example.com", first_name="Old", last_name="User"
    )
    updated_user_data = DomainUser(
        id=entity_id, email="new@example.com", first_name="New", last_name="User"
    )

    mock_generic_repository.get_by_id.return_value = existing_user
    mock_generic_repository.update.return_value = updated_user_data

    use_case = UpdateEntityUseCase(repository=mock_generic_repository)
    request = GenericUpdateRequest(id=entity_id, data=updated_user_data)
    response = use_case.execute(request)

    mock_generic_repository.get_by_id.assert_called_once_with(entity_id)
    mock_generic_repository.update.assert_called_once_with(updated_user_data)
    assert response == GenericReadResponse(data=updated_user_data)


def test_update_entity_use_case_not_found(mock_generic_repository):
    entity_id = str(uuid.uuid4())
    updated_user_data = DomainUser(
        id=entity_id, email="new@example.com", first_name="New", last_name="User"
    )

    mock_generic_repository.get_by_id.return_value = None

    use_case = UpdateEntityUseCase(repository=mock_generic_repository)
    request = GenericUpdateRequest(id=entity_id, data=updated_user_data)

    with pytest.raises(EntityNotFoundException):
        use_case.execute(request)

    mock_generic_repository.get_by_id.assert_called_once_with(entity_id)
    mock_generic_repository.update.assert_not_called()


# Testes para DeleteEntityUseCase
def test_delete_entity_use_case_success(mock_generic_repository):
    entity_id = str(uuid.uuid4())
    mock_generic_repository.delete.return_value = (
        None  # delete não precisa retornar valor
    )

    use_case = DeleteEntityUseCase(repository=mock_generic_repository)
    request = GenericDeleteRequest(id=entity_id)
    response = use_case.execute(request)

    mock_generic_repository.delete.assert_called_once_with(entity_id)
    assert response == GenericSuccessResponse(success=True)


def test_delete_entity_use_case_not_found(mock_generic_repository):
    entity_id = str(uuid.uuid4())
    # DeleteEntityUseCase não verifica se a entidade existe, apenas deleta
    # Isso é esperado para operações idempotentes

    use_case = DeleteEntityUseCase(repository=mock_generic_repository)
    request = GenericDeleteRequest(id=entity_id)

    response = use_case.execute(request)

    mock_generic_repository.delete.assert_called_once_with(entity_id)
    assert response == GenericSuccessResponse(success=True)
