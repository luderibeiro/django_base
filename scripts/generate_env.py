#!/usr/bin/env python3
"""
Script para gerar arquivo .env com valores seguros.

Este script gera um arquivo .env com valores seguros para desenvolvimento
e produção, incluindo SECRET_KEY único e outras configurações necessárias.
"""

import os
import secrets
import string
from pathlib import Path


def generate_secret_key(length=50):
    """Gera uma SECRET_KEY segura para Django."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_oauth_client_id(project_name="django-base"):
    """Gera um client_id único para OAuth2."""
    return f"{project_name}-{secrets.token_urlsafe(16)}"


def generate_env_content():
    """Gera o conteúdo do arquivo .env."""
    secret_key = generate_secret_key()
    oauth_client_id = generate_oauth_client_id()

    content = f"""# Django Base Template - Environment Variables
# Generated automatically - DO NOT commit to version control

# Django Configuration
DEBUG=True
SECRET_KEY={secret_key}
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration
# For development, leave empty to use SQLite
# For production, use DATABASE_URL or individual settings
DATABASE_URL=
# Or use individual settings:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=postgres
# DB_USER=postgres
# DB_PASSWORD=postgres
# DB_HOST=project_db
# DB_PORT=5432

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0

# OAuth2 Configuration
OAUTH2_CLIENT_ID={oauth_client_id}
OAUTH2_SCOPES=read write
OAUTH2_ACCESS_TOKEN_EXPIRE_SECONDS=86400
OAUTH2_REFRESH_TOKEN_EXPIRE_SECONDS=2592000

# Django REST Framework
DRF_PAGE_SIZE=50

# Logging
LOG_LEVEL=INFO

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Security (Production)
SECURE_SSL_REDIRECT=False
SECURE_PROXY_SSL_HEADER=
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False

# Sentry (optional)
SENTRY_DSN=

# Monitoring (optional)
PROMETHEUS_ENABLED=False
"""
    return content


def main():
    """Função principal."""
    print("🔐 Gerando arquivo .env com valores seguros...")

    # Verificar se já existe um .env
    env_file = Path(".env")
    if env_file.exists():
        response = input("⚠️  Arquivo .env já existe. Deseja sobrescrever? (y/N): ")
        if response.lower() != "y":
            print("❌ Operação cancelada.")
            return

    # Gerar conteúdo
    content = generate_env_content()

    # Escrever arquivo
    env_file.write_text(content)

    print("✅ Arquivo .env gerado com sucesso!")
    print("🔑 SECRET_KEY gerada automaticamente")
    print("🔐 OAuth2 CLIENT_ID gerado automaticamente")
    print("⚠️  Lembre-se de não commitar o arquivo .env para o repositório!")


if __name__ == "__main__":
    main()
