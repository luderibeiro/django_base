"""
Testes unitários para middleware de exceções customizadas.
"""

from unittest.mock import Mock, patch

import pytest
from core.middleware.custom_exception_middleware import custom_exception_handler
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response


class TestCustomExceptionMiddleware:
    """Testes para custom_exception_handler."""

    def test_validation_error_handling(self):
        """Testa tratamento de ValidationError."""
        exc = ValidationError({"field": ["Este campo é obrigatório."]})
        context = {"request": Mock()}

        response = custom_exception_handler(exc, context)

        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "field" in response.data
        assert response.data["field"] == ["Este campo é obrigatório."]

    def test_not_found_error_handling(self):
        """Testa tratamento de NotFound."""
        exc = NotFound("Recurso não encontrado")
        context = {"request": Mock()}

        response = custom_exception_handler(exc, context)

        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.data
        assert response.data["detail"] == "Recurso não encontrado"

    def test_permission_denied_error_handling(self):
        """Testa tratamento de PermissionDenied."""
        exc = PermissionDenied("Acesso negado")
        context = {"request": Mock()}

        response = custom_exception_handler(exc, context)

        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "detail" in response.data
        assert response.data["detail"] == "Acesso negado"

    def test_generic_exception_handling(self):
        """Testa tratamento de exceção genérica."""
        exc = Exception("Erro interno")
        context = {"request": Mock()}

        response = custom_exception_handler(exc, context)

        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "detail" in response.data
        assert response.data["detail"] == "Ocorreu um erro inesperado."

    def test_exception_with_custom_detail(self):
        """Testa exceção com detalhes customizados."""
        exc = ValidationError(
            {"email": ["Email inválido"], "password": ["Senha muito curta"]}
        )
        context = {"request": Mock()}

        response = custom_exception_handler(exc, context)

        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert "password" in response.data
        assert response.data["email"] == ["Email inválido"]
        assert response.data["password"] == ["Senha muito curta"]
