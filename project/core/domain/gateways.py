"""Gateways do domínio para integrações externas (ex.: autenticação)."""

from abc import ABC, abstractmethod
from typing import Tuple


class AuthGateway(ABC):
    """Gateway de autenticação (senha e emissão de tokens)."""

    @abstractmethod
    def check_password(self, user_id: str, password: str) -> bool:
        """Verifica se a senha está correta para o usuário."""
        pass

    @abstractmethod
    def create_tokens(self, user_id: str) -> Tuple[str, str]:
        """Cria tokens de acesso e refresh para o usuário."""
        pass

    @abstractmethod
    def set_password(self, user_id: str, new_password: str) -> None:
        """Define nova senha para o usuário."""
        pass
