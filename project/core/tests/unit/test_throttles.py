"""Testes unitários para throttles de rate limiting."""

from unittest.mock import Mock, patch

import pytest
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from core.api.throttles import (
    LoginRateThrottle,
    RateLimitThrottle,
    UserCreationRateThrottle,
)

User = get_user_model()


@pytest.fixture
def request_factory():
    """Factory para criar requests de teste."""
    return APIRequestFactory()


@pytest.fixture
def mock_view():
    """Mock de view para testes."""
    return Mock()


class TestRateLimitThrottle:
    """Testes para RateLimitThrottle base."""

    def test_get_cache_key_authenticated_user(self, request_factory, mock_view):
        """Testa geração de chave de cache para usuário autenticado."""
        throttle = RateLimitThrottle()
        user = Mock()
        user.id = "123"
        user.is_authenticated = True
        request = request_factory.get("/")
        request.user = user

        key = throttle.get_cache_key(request, mock_view)

        assert "throttle_user_123" == key

    def test_get_cache_key_unauthenticated_user(self, request_factory, mock_view):
        """Testa geração de chave de cache para usuário não autenticado."""
        throttle = RateLimitThrottle()
        request = request_factory.get("/")
        request.user = Mock()
        request.user.is_authenticated = False
        request.META = {"REMOTE_ADDR": "192.168.1.1"}

        with patch.object(throttle, "get_ident", return_value="192.168.1.1"):
            key = throttle.get_cache_key(request, mock_view)

        assert "throttle_user_192.168.1.1" == key

    def test_allow_request_superuser_bypass(self, request_factory, mock_view):
        """Testa que superusuários são isentos de rate limiting."""
        throttle = RateLimitThrottle()
        user = Mock()
        user.is_superuser = True
        user.is_authenticated = True
        request = request_factory.get("/")
        request.user = user

        result = throttle.allow_request(request, mock_view)

        assert result is True

    def test_allow_request_with_old_requests(self, request_factory, mock_view):
        """Testa remoção de requisições antigas do histórico."""
        throttle = RateLimitThrottle()
        throttle.duration = 3600
        throttle.num_requests = 5

        request = request_factory.get("/")
        request.user = Mock()
        request.user.is_authenticated = False
        request.user.is_superuser = False
        request.META = {"REMOTE_ADDR": "192.168.1.1"}

        with patch.object(throttle, "get_ident", return_value="192.168.1.1"):
            key = throttle.get_cache_key(request, mock_view)

        # Simular histórico com requisições antigas
        # O histórico é ordenado com mais recente primeiro (insert(0, now))
        # Então removemos do final (history[-1]) que é o mais antigo
        import time

        now = time.time()
        old_time = now - 4000  # Mais antiga que duration
        recent_time = now - 100  # Recente
        # Histórico: [recent_time, old_time] - recent_time primeiro (mais recente)
        cache.set(key, [recent_time, old_time], throttle.duration)

        result = throttle.allow_request(request, mock_view)

        # Deve permitir e limpar requisições antigas do final
        assert result is True
        history = cache.get(key, [])
        # old_time removida, recent_time mantida, nova requisição adicionada no início
        assert len(history) == 2
        # Verifica que old_time foi removida (não está mais no histórico)
        assert old_time not in history
        # Verifica que recent_time ainda está
        assert recent_time in history

    def test_allow_request_rate_limit_exceeded(self, request_factory, mock_view):
        """Testa bloqueio quando limite de requisições é excedido."""
        throttle = RateLimitThrottle()
        throttle.num_requests = 2
        throttle.duration = 3600

        request = request_factory.get("/")
        request.user = Mock()
        request.user.is_authenticated = False
        request.user.is_superuser = False
        request.META = {"REMOTE_ADDR": "192.168.1.1"}

        with patch.object(throttle, "get_ident", return_value="192.168.1.1"):
            key = throttle.get_cache_key(request, mock_view)

        # Preencher histórico até o limite
        import time

        cache.set(key, [time.time(), time.time()], throttle.duration)

        result = throttle.allow_request(request, mock_view)

        assert result is False

    def test_wait_returns_none(self):
        """Testa que wait() retorna None."""
        throttle = RateLimitThrottle()
        assert throttle.wait() is None


class TestLoginRateThrottle:
    """Testes para LoginRateThrottle."""

    def test_login_throttle_configuration(self):
        """Testa configuração específica do LoginRateThrottle."""
        throttle = LoginRateThrottle()
        assert throttle.scope == "login"
        assert throttle.num_requests == 5
        assert throttle.duration == 300


class TestUserCreationRateThrottle:
    """Testes para UserCreationRateThrottle."""

    def test_user_creation_throttle_configuration(self):
        """Testa configuração específica do UserCreationRateThrottle."""
        throttle = UserCreationRateThrottle()
        assert throttle.scope == "user_creation"
        assert throttle.num_requests == 3
        assert throttle.duration == 3600
