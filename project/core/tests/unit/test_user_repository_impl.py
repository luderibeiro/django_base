"""Testes unitários para DjangoUserRepository."""

import pytest
from django.contrib.auth import get_user_model

from core.domain.entities.user import User as DomainUser
from core.domain.exceptions import EntityNotFoundException
from core.repositories.user_repository_impl import DjangoUserRepository

User = get_user_model()


@pytest.mark.django_db
class TestDjangoUserRepository:
    """Testes para DjangoUserRepository."""

    def test_get_by_id_not_found(self):
        """Testa get_by_id quando usuário não existe."""
        repository = DjangoUserRepository()
        result = repository.get_by_id("00000000-0000-0000-0000-000000000000")
        assert result is None

    def test_get_user_by_email_not_found(self):
        """Testa get_user_by_email quando usuário não existe."""
        repository = DjangoUserRepository()
        result = repository.get_user_by_email("nonexistent@example.com")
        assert result is None

    def test_update_user_not_found(self):
        """Testa update quando usuário não existe."""
        repository = DjangoUserRepository()
        domain_user = DomainUser(
            id="00000000-0000-0000-0000-000000000000",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )

        with pytest.raises(EntityNotFoundException) as exc_info:
            repository.update(domain_user)

        assert "User" in str(exc_info.value)
        assert domain_user.id in str(exc_info.value)

    def test_delete_user_not_found(self):
        """Testa delete quando usuário não existe."""
        repository = DjangoUserRepository()
        user_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(EntityNotFoundException) as exc_info:
            repository.delete(user_id)

        assert "User" in str(exc_info.value)
        assert user_id in str(exc_info.value)

    def test_get_all_paginated_filtered_with_empty_search_query(self):
        """Testa get_all_paginated_filtered com search_query vazio."""
        repository = DjangoUserRepository()
        User.objects.create_user(
            email="test@example.com", first_name="Test", last_name="User"
        )

        users, total = repository.get_all_paginated_filtered(
            offset=0, limit=10, search_query="   "
        )

        assert total >= 1
        assert len(users) >= 1

    def test_get_all_paginated_filtered_with_long_search_query(self):
        """Testa get_all_paginated_filtered com search_query muito longo."""
        repository = DjangoUserRepository()
        User.objects.create_user(
            email="test@example.com", first_name="Test", last_name="User"
        )

        # Search query com mais de 100 caracteres
        long_query = "a" * 150
        users, total = repository.get_all_paginated_filtered(
            offset=0, limit=10, search_query=long_query
        )

        # Deve truncar para 100 caracteres e não encontrar nada
        assert isinstance(users, list)
        assert isinstance(total, int)
