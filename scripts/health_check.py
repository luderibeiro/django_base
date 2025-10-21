#!/usr/bin/env python3
"""
Script de health check completo para a aplicação Django.

Este script verifica todos os componentes da aplicação:
- Database connectivity
- Redis connectivity (if configured)
- Static files
- Media files
- OAuth2 configuration
- Django settings
"""

import os
import sys
import django
from pathlib import Path
import requests
import time


def setup_django():
    """Configura o ambiente Django."""
    # Adicionar o diretório do projeto ao Python path
    project_dir = Path(__file__).parent.parent / "project"
    sys.path.insert(0, str(project_dir))
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    django.setup()


def check_database():
    """Verifica conectividade com o banco de dados."""
    print("🗄️  Verificando banco de dados...")
    
    try:
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        # Testar conexão
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        if result:
            print("✅ Banco de dados: OK")
            return True
        else:
            print("❌ Banco de dados: Falha na consulta")
            return False
            
    except Exception as e:
        print(f"❌ Banco de dados: Erro - {e}")
        return False


def check_redis():
    """Verifica conectividade com Redis (se configurado)."""
    print("🔴 Verificando Redis...")
    
    try:
        import redis
        from django.conf import settings
        
        redis_url = getattr(settings, 'REDIS_URL', None)
        if not redis_url:
            print("⚠️  Redis: Não configurado (opcional)")
            return True
            
        r = redis.from_url(redis_url)
        r.ping()
        print("✅ Redis: OK")
        return True
        
    except Exception as e:
        print(f"❌ Redis: Erro - {e}")
        return False


def check_static_files():
    """Verifica arquivos estáticos."""
    print("📁 Verificando arquivos estáticos...")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles import finders
        
        static_dirs = settings.STATICFILES_DIRS
        static_root = settings.STATIC_ROOT
        
        # Verificar se os diretórios existem
        for static_dir in static_dirs:
            if not Path(static_dir).exists():
                print(f"⚠️  Diretório estático não encontrado: {static_dir}")
                return False
                
        if static_root and not Path(static_root).exists():
            print(f"⚠️  STATIC_ROOT não encontrado: {static_root}")
            return False
            
        print("✅ Arquivos estáticos: OK")
        return True
        
    except Exception as e:
        print(f"❌ Arquivos estáticos: Erro - {e}")
        return False


def check_media_files():
    """Verifica arquivos de mídia."""
    print("📷 Verificando arquivos de mídia...")
    
    try:
        from django.conf import settings
        
        media_root = settings.MEDIA_ROOT
        if media_root and not Path(media_root).exists():
            print(f"⚠️  MEDIA_ROOT não encontrado: {media_root}")
            return False
            
        print("✅ Arquivos de mídia: OK")
        return True
        
    except Exception as e:
        print(f"❌ Arquivos de mídia: Erro - {e}")
        return False


def check_oauth2():
    """Verifica configuração OAuth2."""
    print("🔐 Verificando OAuth2...")
    
    try:
        from oauth2_provider.models import Application
        from django.conf import settings
        
        # Verificar se há aplicações OAuth2
        apps = Application.objects.all()
        if not apps.exists():
            print("⚠️  OAuth2: Nenhuma aplicação configurada")
            return False
            
        # Verificar configurações
        oauth_settings = getattr(settings, 'OAUTH2_PROVIDER', {})
        if not oauth_settings:
            print("⚠️  OAuth2: Configurações não encontradas")
            return False
            
        print("✅ OAuth2: OK")
        return True
        
    except Exception as e:
        print(f"❌ OAuth2: Erro - {e}")
        return False


def check_django_settings():
    """Verifica configurações do Django."""
    print("⚙️  Verificando configurações Django...")
    
    try:
        from django.core.management import execute_from_command_line
        
        # Executar check do Django
        execute_from_command_line(['manage.py', 'check'])
        print("✅ Configurações Django: OK")
        return True
        
    except Exception as e:
        print(f"❌ Configurações Django: Erro - {e}")
        return False


def check_server_health():
    """Verifica se o servidor está respondendo."""
    print("🌐 Verificando servidor...")
    
    try:
        # Tentar conectar ao servidor local
        response = requests.get('http://127.0.0.1:8000/health/', timeout=5)
        if response.status_code == 200:
            print("✅ Servidor: OK")
            return True
        else:
            print(f"⚠️  Servidor: Status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Servidor: Não está rodando (normal se não iniciado)")
        return True
    except Exception as e:
        print(f"❌ Servidor: Erro - {e}")
        return False


def main():
    """Função principal do health check."""
    print("🏥 Iniciando health check completo...")
    print("=" * 50)
    
    # Configurar Django
    setup_django()
    
    # Lista de verificações
    checks = [
        check_django_settings,
        check_database,
        check_redis,
        check_static_files,
        check_media_files,
        check_oauth2,
        check_server_health,
    ]
    
    # Executar verificações
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro inesperado em {check.__name__}: {e}")
            results.append(False)
        print()
    
    # Resumo
    print("=" * 50)
    print("📊 RESUMO DO HEALTH CHECK")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 Todos os checks passaram! Aplicação saudável.")
        sys.exit(0)
    else:
        print(f"⚠️  {passed}/{total} checks passaram. Verifique os erros acima.")
        sys.exit(1)


if __name__ == "__main__":
    main()
