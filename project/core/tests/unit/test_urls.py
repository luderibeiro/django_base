"""
Testes unitários para resolução de URLs.
"""

import pytest
from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class TestURLResolution(TestCase):
    """Testes para resolução de URLs."""

    def test_admin_url_resolution(self):
        """Testa resolução da URL do admin."""
        admin_path = f"/{settings.ADMIN_DEFAULT_PATH}/"
        url = reverse("admin:index")
        self.assertEqual(url, admin_path)

    def test_oauth2_urls_resolution(self):
        """Testa resolução das URLs do OAuth2."""
        # Testa URL de autorização
        url = reverse("oauth2_provider:authorize")
        self.assertEqual(url, "/o/authorize/")

        # Testa URL de token
        url = reverse("oauth2_provider:token")
        self.assertEqual(url, "/o/token/")

    def test_api_schema_url_resolution(self):
        """Testa resolução da URL do schema OpenAPI."""
        url = reverse("schema")
        self.assertEqual(url, "/api/schema/")

    def test_api_docs_url_resolution(self):
        """Testa resolução da URL da documentação Swagger."""
        url = reverse("swagger-ui")
        self.assertEqual(url, "/api/docs/")

    def test_api_redoc_url_resolution(self):
        """Testa resolução da URL da documentação ReDoc."""
        url = reverse("redoc")
        self.assertEqual(url, "/api/redoc/")

    def test_core_api_urls_included(self):
        """Testa se as URLs da API core estão incluídas."""
        # Testa se as URLs do OpenAPI estão disponíveis
        schema_url = reverse("schema")
        self.assertEqual(schema_url, "/api/schema/")

    def test_static_files_urls_in_debug(self):
        """Testa se URLs de arquivos estáticos estão disponíveis em DEBUG."""
        if settings.DEBUG:
            # Em modo DEBUG, as URLs estáticas devem estar disponíveis
            self.assertTrue(hasattr(settings, "STATIC_URL"))
            self.assertTrue(hasattr(settings, "MEDIA_URL"))
