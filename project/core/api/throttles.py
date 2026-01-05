"""Throttle classes para rate limiting da API."""

import time

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle


class RateLimitThrottle(BaseThrottle):
    """Throttle base para rate limiting usando cache do Django."""

    cache_format = "throttle_%(scope)s_%(ident)s"
    scope = "user"
    num_requests = 100
    duration = 3600  # 1 hora em segundos

    def get_cache_key(self, request, view):
        """Gera chave de cache baseada no IP ou usuário."""
        if request.user and request.user.is_authenticated:
            ident = str(request.user.id)
        else:
            ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}

    def allow_request(self, request, view):
        """Verifica se a requisição deve ser permitida."""
        if request.user and request.user.is_superuser:
            return True

        key = self.get_cache_key(request, view)
        history = cache.get(key, [])

        # Remove requisições antigas
        now = time.time()
        while history and history[-1] <= now - self.duration:
            history.pop()

        # Verifica limite
        if len(history) >= self.num_requests:
            return False

        # Adiciona requisição atual
        history.insert(0, now)
        cache.set(key, history, self.duration)
        return True

    def wait(self):
        """Retorna tempo de espera em segundos."""
        return None


class LoginRateThrottle(RateLimitThrottle):
    """Throttle específico para endpoint de login - mais restritivo."""

    scope = "login"
    num_requests = 5  # 5 tentativas
    duration = 300  # 5 minutos


class UserCreationRateThrottle(RateLimitThrottle):
    """Throttle específico para criação de usuários."""

    scope = "user_creation"
    num_requests = 3  # 3 criações
    duration = 3600  # 1 hora
