from typing import List, Optional

from core.domain.data_access import UserRepository
from core.domain.entities.user import User as DomainUser
from core.models.user import User as DjangoUser


class DjangoUserRepository(UserRepository):
    def get_by_id(self, user_id: str) -> Optional[DomainUser]:
        try:
            user = DjangoUser.objects.get(id=user_id)
            return self._to_domain_user(user)
        except DjangoUser.DoesNotExist:
            return None

    def get_user_by_email(self, email: str) -> Optional[DomainUser]:
        try:
            user = DjangoUser.objects.get(email=email)
            return self._to_domain_user(user)
        except DjangoUser.DoesNotExist:
            return None

    def create(self, user: DomainUser) -> DomainUser:
        django_user = DjangoUser.objects.create_user(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )  # is_active, is_staff, is_superuser são tratados pelo UserManager
        return self._to_domain_user(django_user)

    def update(self, user: DomainUser) -> DomainUser:
        django_user = DjangoUser.objects.get(id=user.id)
        django_user.email = user.email
        django_user.first_name = user.first_name
        django_user.last_name = user.last_name
        # is_active, is_staff, is_superuser não são mais atributos diretos aqui
        # As permissões são gerenciadas pelo PermissionsMixin
        django_user.save()
        return self._to_domain_user(django_user)

    def delete(self, user_id: str) -> None:
        DjangoUser.objects.filter(id=user_id).delete()

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
