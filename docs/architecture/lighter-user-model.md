# Refatorando o Modelo de Usuário do Django para uma Entidade mais Leve

Esta seção detalha o processo de refatoração do modelo `User` do Django para que ele seja uma entidade de persistência mais leve, com menos acoplamento ao framework Django e mais alinhada com a camada de Domínio da Arquitetura Limpa.

## 1. Contexto e Justificativa

Originalmente, o modelo `User` do Django herda de `AbstractUser`, o que traz consigo muitas funcionalidades e dependências específicas do framework (permissões, grupos, etc.). Embora conveniente, isso pode levar a um forte acoplamento da camada de Domínio à Infraestrutura (Django). O objetivo desta refatoração é isolar a entidade de Domínio `User` e fazer com que o modelo Django atue apenas como um adaptador de persistência.

## 2. Abordagem da Refatoração

### a. Modelo `User` do Django (`project/core/models/user.py`)

O modelo `User` foi simplificado para herdar de `AbstractBaseUser` e `PermissionsMixin`. O campo `username` foi removido, e o `USERNAME_FIELD` foi definido como `email`. Isso o torna mais flexível e menos acoplado às suposições padrão do `AbstractUser`.

```python
from typing import ClassVar
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# ... (UserManager inalterado ou com ajustes internos para AbstractBaseUser)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    objects: ClassVar[UserManager] = UserManager()

    def __str__(self):
        return self.email
```

### b. Entidade de Domínio `User` (`project/core/domain/entities/user.py`)

Esta entidade já foi criada para ser agnóstica a frameworks e não exigiu alterações. Ela contém apenas os atributos e métodos de negócio essenciais, sem qualquer dependência do Django.

### c. Repositório de Usuário (`project/core/repositories/user_repository_impl.py`)

O `DjangoUserRepository` foi atualizado para lidar com as mudanças no modelo Django `User` e para garantir que o mapeamento entre a entidade de Domínio `User` e o modelo de persistência do Django ocorra corretamente.

**Principais alterações:**
- No método `create`, a passagem de `is_active`, `is_staff` e `is_superuser` para `DjangoUser.objects.create_user` foi removida, pois esses campos agora são tratados internamente pelo `UserManager` ao herdar de `AbstractBaseUser`.
- No método `update`, a atualização direta dos campos `is_active`, `is_staff` e `is_superuser` foi removida do modelo Django, pois eles são gerenciados pelo `PermissionsMixin`.
- No método `_to_domain_user`, o acesso aos campos `is_active`, `is_staff` e `is_superuser` foi ajustado para refletir a nova estrutura do modelo Django (`AbstractBaseUser` e `PermissionsMixin`).
- No método `get_all`, a filtragem de `is_superuser=False` foi alterada para `exclude(is_superuser=True)`, que é a forma apropriada de filtrar superusuários com o `PermissionsMixin`.

```python
from typing import List, Optional
from core.domain.data_access import UserRepository
from core.domain.entities.user import User as DomainUser
from core.models.user import User as DjangoUser

class DjangoUserRepository(UserRepository):
    # ... (outros métodos inalterados)

    def create(self, user: DomainUser) -> DomainUser:
        django_user = DjangoUser.objects.create_user(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        ) # is_active, is_staff, is_superuser são tratados pelo UserManager
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

    # ... (delete method inalterado)

    def _to_domain_user(self, django_user: DjangoUser) -> DomainUser:
        return DomainUser(
            id=str(django_user.id),
            email=django_user.email,
            first_name=django_user.first_name,
            last_name=django_user.last_name,
            is_active=django_user.is_active, # AbstractBaseUser tem is_active por padrão
            is_staff=django_user.is_staff, # PermissionsMixin tem is_staff
            is_superuser=django_user.is_superuser, # PermissionsMixin tem is_superuser
        )

    def get_all(self) -> List[DomainUser]:
        # A propriedade is_superuser é acessada diretamente via PermissionsMixin
        django_users = DjangoUser.objects.exclude(is_superuser=True) # Excluir superusuários por padrão
        return [self._to_domain_user(user) for user in django_users]
```

### d. Impacto em Casos de Uso, Serializers e Views

Não houve impacto direto nas camadas de Aplicação (Casos de Uso) e Apresentação (Serializers e Views), pois elas já interagem com a entidade de Domínio `User` e seus DTOs, e não diretamente com o modelo Django. Isso demonstra o sucesso do desacoplamento da Arquitetura Limpa.

## 3. Passos da Implementação (Concluídos)

1.  **Modelo `User` do Django refatorado**: `project/core/models/user.py` foi modificado para herdar de `AbstractBaseUser` e `PermissionsMixin`, removendo o campo `username` e ajustando os campos de identificação.
2.  **Repositório de Usuário atualizado**: `project/core/repositories/user_repository_impl.py` foi ajustado para lidar com as mudanças no modelo Django, garantindo o mapeamento correto e a interação com as propriedades de permissão.
3.  **Verificação de Serializers e Views**: Confirmado que `project/core/api/v1/serializers/user.py` e `project/core/api/v1/views/user.py` não precisaram de alterações diretas, pois já estavam desacoplados do modelo Django.
