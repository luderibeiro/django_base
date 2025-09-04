"""
Entidades de domínio para usuários.

Contém as entidades de domínio que representam os conceitos centrais
do negócio relacionados a usuários.
"""

import uuid
from dataclasses import dataclass, field


@dataclass
class User:
    """
    Entidade de domínio para usuário.
    """

    email: str = field(compare=True)
    first_name: str = field(compare=False)
    last_name: str = field(compare=False)
    id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=True)
    is_active: bool = field(default=True, compare=False)
    is_staff: bool = field(default=False, compare=False)
    is_superuser: bool = field(default=False, compare=False)

    def is_admin(self) -> bool:
        """Verifica se o usuário é administrador."""
        return self.is_staff and self.is_superuser

    def __eq__(self, other):
        """Compara usuários por ID."""
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        """Hash baseado no ID do usuário."""
        return hash(self.id)

    def __str__(self):
        """Representação string do usuário."""
        return f"User(id={self.id}, email={self.email})"
