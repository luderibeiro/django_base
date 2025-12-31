#!/usr/bin/env python3
"""
Script para configurar OAuth2 application automaticamente.

Este script cria uma aplicação OAuth2 com configurações padrão
para facilitar o setup inicial do projeto.
"""

import os
import sys
import django
from pathlib import Path
import secrets
import string


def setup_django():
    """Configura o ambiente Django."""
    # Adicionar o diretório do projeto ao Python path
    project_dir = Path(__file__).parent.parent / "project"
    sys.path.insert(0, str(project_dir))

    # Configurar Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()


def generate_client_credentials():
    """Gera credenciais seguras para OAuth2."""
    client_id = secrets.token_urlsafe(32)
    client_secret = secrets.token_urlsafe(48)
    return client_id, client_secret


def create_oauth_application():
    """Cria aplicação OAuth2."""
    try:
        from oauth2_provider.models import Application

        # Verificar se já existe uma aplicação
        existing_app = Application.objects.filter(name="Django Base API").first()
        if existing_app:
            print("⚠️  Aplicação OAuth2 já existe:")
            print(f"   Client ID: {existing_app.client_id}")
            print(f"   Client Secret: {existing_app.client_secret}")
            return existing_app

        # Gerar credenciais
        client_id, client_secret = generate_client_credentials()

        # Criar aplicação
        app = Application.objects.create(
            name="Django Base API",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_id=client_id,
            client_secret=client_secret,
        )

        print("✅ Aplicação OAuth2 criada com sucesso!")
        print("   Client ID: " + client_id)
        print("   Client Secret: " + client_secret)
        print("   Grant Type: Password")
        print("   Client Type: Confidential")

        return app

    except Exception as e:
        print(f"❌ Erro ao criar aplicação OAuth2: {e}")
        return None


def update_env_file(client_id, client_secret):
    """Atualiza arquivo .env com as credenciais OAuth2."""
    env_files = [Path(".env"), Path("dotenv_files/.env")]
    found_files = [f for f in env_files if f.exists()]
    
    if not found_files:
        print("⚠️  Arquivo .env não encontrado. Execute 'make generate-env' primeiro.")
        return False

    try:
        for env_file in found_files:
            # Ler conteúdo atual
            content = env_file.read_text()

            # Atualizar credenciais
            lines = content.split("\n")
            updated_lines = []

            for line in lines:
                if line.startswith("OAUTH2_CLIENT_ID="):
                    updated_lines.append(f"OAUTH2_CLIENT_ID={client_id}")
                elif line.startswith("OAUTH2_CLIENT_SECRET="):
                    updated_lines.append(f"OAUTH2_CLIENT_SECRET={client_secret}")
                else:
                    updated_lines.append(line)

            # Adicionar CLIENT_SECRET se não existir
            if not any(line.startswith("OAUTH2_CLIENT_SECRET=") for line in lines):
                updated_lines.append(f"OAUTH2_CLIENT_SECRET={client_secret}")

            # Escrever arquivo atualizado
            env_file.write_text("\n".join(updated_lines))
            print(f"✅ Arquivo {env_file} atualizado com credenciais OAuth2")
        
        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar .env: {e}")
        return False


def create_superuser_if_needed():
    """Cria superusuário se não existir."""
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Criando superusuário...")
            username = input("Digite o username (admin): ").strip() or "admin"
            email = input("Digite o email: ").strip()
            password = input("Digite a senha: ").strip()

            if not password:
                password = "admin123"  # Senha padrão para desenvolvimento
                print("⚠️  Usando senha padrão: admin123")

            user = User.objects.create_superuser(
                username=username, email=email, password=password
            )
            print(f"✅ Superusuário criado: {username}")
            return user
        else:
            print("✅ Superusuário já existe")
            return User.objects.filter(is_superuser=True).first()

    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return None


def show_usage_examples(app):
    """Mostra exemplos de uso da API OAuth2."""
    if not app:
        return

    print("\n" + "=" * 60)
    print("📚 EXEMPLOS DE USO DA API OAUTH2")
    print("=" * 60)

    print("\n1. Obter token de acesso:")
    print("curl -X POST http://127.0.0.1:8000/o/token/ \\")
    print("  -H 'Content-Type: application/x-www-form-urlencoded' \\")
    print("  -d 'grant_type=password' \\")
    print("  -d 'username=admin' \\")
    print("  -d 'password=admin123' \\")
    print(f"  -d 'client_id={app.client_id}' \\")
    print(f"  -d 'client_secret={app.client_secret}'")

    print("\n2. Usar token para acessar API:")
    print("curl -X GET http://127.0.0.1:8000/api/v1/users/ \\")
    print("  -H 'Authorization: Bearer SEU_ACCESS_TOKEN'")

    print("\n3. Documentação da API:")
    print("http://127.0.0.1:8000/api/schema/swagger-ui/")

    print("\n4. Admin do Django:")
    print("http://127.0.0.1:8000/admin/")


def main():
    """Função principal."""
    print("🔐 Configurando OAuth2 application...")
    print("=" * 50)

    # Configurar Django
    setup_django()

    # Executar migrações se necessário
    try:
        from django.core.management import execute_from_command_line

        print("🗄️  Executando migrações...")
        execute_from_command_line(["manage.py", "migrate"])
        print("✅ Migrações executadas")
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        return

    # Criar superusuário se necessário
    create_superuser_if_needed()

    # Criar aplicação OAuth2
    app = create_oauth_application()

    if app:
        # Atualizar .env
        update_env_file(app.client_id, app.client_secret)

        # Mostrar exemplos de uso
        show_usage_examples(app)

        print("\n🎉 Setup OAuth2 concluído com sucesso!")
        print("💡 Execute 'make run' para iniciar o servidor")
    else:
        print("❌ Falha na configuração OAuth2")
        sys.exit(1)


if __name__ == "__main__":
    main()
