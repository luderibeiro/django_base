from unittest.mock import Mock

import pytest

from core.domain.data_access import GenericRepository
from core.domain.entities.user import User as DomainUser
from core.domain.use_cases.generic_use_cases import (
    CreateEntityUseCase,
    DeleteEntityUseCase,
    GenericCreateRequest,
    GenericDeleteRequest,
    GenericListRequest,
    GenericReadResponse,
    GenericUpdateRequest,
    GetEntityByIdUseCase,
    ListEntitiesUseCase,
    UpdateEntityUseCase,
)


@pytest.fixture
def mock_generic_repository():
    return Mock(spec=GenericRepository)


@pytest.fixture
def sample_user():
    return DomainUser(
        id="1",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )


def test_create_entity_use_case_success(mock_generic_repository, sample_user):
    # Given
    mock_generic_repository.create.return_value = sample_user
    use_case = CreateEntityUseCase(repository=mock_generic_repository)
    request = GenericCreateRequest(data=sample_user)

    # When
    response = use_case.execute(request)

    # Then
    mock_generic_repository.create.assert_called_once_with(sample_user)
    assert response.data == sample_user


def test_list_entities_use_case_success(mock_generic_repository, sample_user):
    # Given
    mock_generic_repository.get_all.return_value = [sample_user]
    use_case = ListEntitiesUseCase(repository=mock_generic_repository)
    request = GenericListRequest()

    # When
    response = use_case.execute(request)

    # Then
    mock_generic_repository.get_all.assert_called_once()
    assert len(response.items) == 1
    assert response.items[0] == sample_user


def test_get_entity_by_id_use_case_success(mock_generic_repository, sample_user):
    # Given
    mock_generic_repository.get_by_id.return_value = sample_user
    use_case = GetEntityByIdUseCase(repository=mock_generic_repository)
    request = GenericDeleteRequest(id=sample_user.id)

    # When
    response = use_case.execute(request)

    # Then
    mock_generic_repository.get_by_id.assert_called_once_with(sample_user.id)
    assert response.data == sample_user


def test_get_entity_by_id_use_case_not_found(mock_generic_repository):
    # Given
    mock_generic_repository.get_by_id.return_value = None
    use_case = GetEntityByIdUseCase(repository=mock_generic_repository)
    request = GenericDeleteRequest(id="non-existent-id")

    # When / Then
    with pytest.raises(ValueError, match="Entity not found"):
        use_case.execute(request)

    mock_generic_repository.get_by_id.assert_called_once_with("non-existent-id")


def test_update_entity_use_case_success(mock_generic_repository, sample_user):
    # Given
    updated_user_data = DomainUser(
        id=sample_user.id,
        email="updated@example.com",
        first_name="Updated",
        last_name="User",
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )
    mock_generic_repository.get_by_id.return_value = sample_user
    mock_generic_repository.update.return_value = updated_user_data

    use_case = UpdateEntityUseCase(repository=mock_generic_repository)
    request = GenericUpdateRequest(id=sample_user.id, data=updated_user_data)

    # When
    response = use_case.execute(request)

    # Then
    mock_generic_repository.get_by_id.assert_called_once_with(sample_user.id)
    mock_generic_repository.update.assert_called_once_with(updated_user_data)
    assert response.data == updated_user_data


def test_update_entity_use_case_not_found(mock_generic_repository, sample_user):
    # Given
    mock_generic_repository.get_by_id.return_value = None
    use_case = UpdateEntityUseCase(repository=mock_generic_repository)
    request = GenericUpdateRequest(id="non-existent-id", data=sample_user)

    # When / Then
    with pytest.raises(ValueError, match="Entity not found"):
        use_case.execute(request)

    mock_generic_repository.get_by_id.assert_called_once_with("non-existent-id")
    mock_generic_repository.update.assert_not_called()


def test_delete_entity_use_case_success(mock_generic_repository, sample_user):
    # Given
    mock_generic_repository.get_by_id.return_value = sample_user
    mock_generic_repository.delete.return_value = None
    use_case = DeleteEntityUseCase(repository=mock_generic_repository)
    request = GenericDeleteRequest(id=sample_user.id)

    # When
    response = use_case.execute(request)

    # Then
    mock_generic_repository.delete.assert_called_once_with(sample_user.id)
    assert response.success is True
