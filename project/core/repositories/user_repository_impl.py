import logging
from typing import List, Optional

from core.domain.data_access import UserRepository
from core.domain.entities.user import User as DomainUser
from core.models.user import User as DjangoUser
from django.db.models import Q

logger = logging.getLogger(__name__)


class DjangoUserRepository(UserRepository):
    """Implementação Django do `UserRepository`.

    Responsável por mapear `core.models.user.User` para a entidade de
    domínio `core.domain.entities.user.User` e oferecer operações de
    persistência e consulta.
    """

    def get_by_id(self, user_id: str) -> Optional[DomainUser]:
        try:
            user = DjangoUser.objects.get(id=user_id)
            logger.debug("User found by ID: %s", user_id)
            return self._to_domain_user(user)
        except DjangoUser.DoesNotExist:
            logger.warning("User not found by ID: %s", user_id)
            return None

    def get_user_by_email(self, email: str) -> Optional[DomainUser]:
        try:
            user = DjangoUser.objects.get(email=email)
            logger.debug("User found by email: %s", email)
            return self._to_domain_user(user)
        except DjangoUser.DoesNotExist:
            logger.warning("User not found by email: %s", email)
            return None

    def create(self, user: DomainUser) -> DomainUser:
        """Cria um usuário Django a partir da entidade de domínio.

        Observação: a senha deve ser tratada em um caso de uso específico
        se for parte do fluxo de criação.
        """
        logger.info("Attempting to create user with email: %s", user.email)
        django_user = DjangoUser.objects.create_user(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )  # is_active, is_staff, is_superuser são tratados pelo UserManager
        logger.info("User created successfully with ID: %s", django_user.id)
        return self._to_domain_user(django_user)

    def update(self, user: DomainUser) -> DomainUser:
        """Atualiza campos básicos de perfil do usuário."""
        logger.info("Attempting to update user with ID: %s", user.id)
        try:
            django_user = DjangoUser.objects.get(id=user.id)
            django_user.email = user.email
            django_user.first_name = user.first_name
            django_user.last_name = user.last_name
            # is_active, is_staff, is_superuser não são mais atributos diretos aqui
            # As permissões são gerenciadas pelo PermissionsMixin
            django_user.save()
            logger.info("User updated successfully with ID: %s", django_user.id)
            return self._to_domain_user(django_user)
        except DjangoUser.DoesNotExist:
            logger.warning("Update failed: User not found with ID: %s", user.id)
            raise ValueError("User not found for update")

    def delete(self, user_id: str) -> None:
        logger.info("Attempting to delete user with ID: %s", user_id)
        deleted_count, _ = DjangoUser.objects.filter(id=user_id).delete()
        if deleted_count == 0:
            logger.warning("Delete failed: User not found with ID: %s", user_id)
            raise ValueError("User not found for deletion")
        logger.info("User deleted successfully with ID: %s", user_id)

    def _to_domain_user(self, django_user: DjangoUser) -> DomainUser:
        return DomainUser(
            id=str(django_user.id),
            email=django_user.email,
            first_name=django_user.first_name,
            last_name=django_user.last_name,
            is_active=django_user.is_active,  # AbstractBaseUser tem is_active por padrão
            is_staff=django_user.is_staff,  # PermissionsMixin tem is_staff
            is_superuser=django_user.is_superuser,  # PermissionsMixin tem is_superuser
        )

    def get_all(self) -> List[DomainUser]:
        # A propriedade is_superuser é acessada diretamente via PermissionsMixin
        django_users = DjangoUser.objects.exclude(
            is_superuser=True
        )  # Excluir superusuários por padrão
        return [self._to_domain_user(user) for user in django_users]

    def get_all_paginated_filtered(
        self, offset: int, limit: int, search_query: Optional[str]
    ) -> tuple[List[DomainUser], int]:
        queryset = DjangoUser.objects.exclude(is_superuser=True)

        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

        total_items = queryset.count()
        django_users = queryset[offset : offset + limit]
        return [self._to_domain_user(user) for user in django_users], total_items
