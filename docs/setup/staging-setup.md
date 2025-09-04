# Setup de Homologação

Este guia detalha como configurar o ambiente de homologação (staging) para o Django Base.

## 📋 Pré-requisitos

- Python 3.12+
- PostgreSQL 13+
- Redis (opcional, para cache)
- Nginx (opcional, para proxy reverso)
- Certificado SSL (para HTTPS)

## 🚀 Configuração Rápida com Makefile

```bash
# Clone o repositório
git clone https://github.com/luderibeiro/django_base.git
cd django_base

# Configure o ambiente de homologação
make prod-setup
```

## ⚙️ Configuração Manual

### 1. **Preparar o Ambiente**

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r project/requirements.txt
```

### 2. **Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-segura-aqui
ALLOWED_HOSTS=staging.seudominio.com,localhost,127.0.0.1

# Banco de dados
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=django_base_staging
POSTGRES_USER=django_user
POSTGRES_PASSWORD=senha-super-segura
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis (opcional)
REDIS_URL=redis://localhost:6379/1

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/django_base/staging.log
```

### 3. **Configurar Banco de Dados PostgreSQL**

```bash
# Conectar ao PostgreSQL
sudo -u postgres psql

# Criar banco de dados
CREATE DATABASE django_base_staging;
CREATE USER django_user WITH PASSWORD 'senha-super-segura';
GRANT ALL PRIVILEGES ON DATABASE django_base_staging TO django_user;
\q
```

### 4. **Configurar Settings para Homologação**

Crie o arquivo `project/project/settings_staging.py`:

```python
import os
from .settings import *

# Configurações específicas para homologação
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Banco de dados PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_DB', 'django_base_staging'),
        'USER': os.environ.get('POSTGRES_USER', 'django_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Logging para homologação
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.environ.get('LOG_FILE', '/var/log/django_base/staging.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}

# Configurações de segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Cache com Redis (opcional)
if os.environ.get('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.environ.get('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

# Email (opcional)
if os.environ.get('EMAIL_HOST'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

### 5. **Executar Migrações e Configurações**

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Configurar variáveis de ambiente
export DJANGO_SETTINGS_MODULE=project.settings_staging

# Executar migrações
cd project
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

### 6. **Configurar Nginx (Opcional)**

Crie o arquivo `/etc/nginx/sites-available/django_base_staging`:

```nginx
server {
    listen 80;
    server_name staging.seudominio.com;

    # Redirecionar para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name staging.seudominio.com;

    # Certificados SSL
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Configurações SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Arquivos estáticos
    location /static/ {
        alias /path/to/django_base/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Arquivos de mídia
    location /media/ {
        alias /path/to/django_base/project/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Aplicação Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ativar o site:

```bash
sudo ln -s /etc/nginx/sites-available/django_base_staging /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. **Configurar Systemd Service**

Crie o arquivo `/etc/systemd/system/django-base-staging.service`:

```ini
[Unit]
Description=Django Base Staging
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/django_base
Environment=DJANGO_SETTINGS_MODULE=project.settings_staging
ExecStart=/path/to/django_base/venv/bin/gunicorn project.wsgi:application --bind 127.0.0.1:8000
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable django-base-staging
sudo systemctl start django-base-staging
```

## 🐳 Configuração com Docker

### 1. **Docker Compose para Homologação**

Crie o arquivo `docker-compose.staging.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: django_base_staging
      POSTGRES_USER: django_user
      POSTGRES_PASSWORD: senha-super-segura
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn project.wsgi:application --bind 0.0.0.0:8000
    environment:
      - DJANGO_SETTINGS_MODULE=project.settings_staging
      - DEBUG=False
      - SECRET_KEY=sua-chave-secreta-super-segura
      - ALLOWED_HOSTS=staging.seudominio.com
      - POSTGRES_DB=django_base_staging
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=senha-super-segura
      - POSTGRES_HOST=db
      - REDIS_URL=redis://redis:6379/1
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/staging.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 2. **Executar com Docker**

```bash
# Construir e executar
docker-compose -f docker-compose.staging.yml up --build -d

# Executar migrações
docker-compose -f docker-compose.staging.yml exec web python manage.py migrate

# Criar superusuário
docker-compose -f docker-compose.staging.yml exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose -f docker-compose.staging.yml exec web python manage.py collectstatic --noinput
```

## 🧪 Testes em Homologação

```bash
# Executar testes
make test

# Verificar status
make status

# Verificar logs
tail -f /var/log/django_base/staging.log
```

## 🔧 Comandos Úteis

```bash
# Verificar status do serviço
sudo systemctl status django-base-staging

# Reiniciar serviço
sudo systemctl restart django-base-staging

# Ver logs do serviço
sudo journalctl -u django-base-staging -f

# Backup do banco de dados
pg_dump -h localhost -U django_user django_base_staging > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
psql -h localhost -U django_user django_base_staging < backup_20240101_120000.sql
```

## 🚨 Monitoramento

### 1. **Health Check**

Crie um endpoint de health check em `project/core/views/health.py`:

```python
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    """Endpoint para verificar a saúde da aplicação"""
    try:
        # Verificar banco de dados
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # Verificar cache
        cache.set('health_check', 'ok', 10)
        cache.get('health_check')

        return JsonResponse({
            'status': 'healthy',
            'database': 'ok',
            'cache': 'ok'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

### 2. **Logs de Monitoramento**

```bash
# Monitorar logs em tempo real
tail -f /var/log/django_base/staging.log

# Filtrar erros
grep "ERROR" /var/log/django_base/staging.log

# Estatísticas de acesso
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr
```

## 🔒 Segurança

### 1. **Firewall**

```bash
# Configurar UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. **Backup Automático**

Crie um script de backup em `/usr/local/bin/backup_django_base.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/django_base"
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
pg_dump -h localhost -U django_user django_base_staging > $BACKUP_DIR/db_$DATE.sql

# Backup dos arquivos de mídia
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /path/to/django_base/project/media/

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Agendar no crontab:

```bash
# Executar backup diariamente às 2:00
0 2 * * * /usr/local/bin/backup_django_base.sh
```

## ✅ Checklist de Homologação

- [ ] Ambiente virtual configurado
- [ ] Dependências instaladas
- [ ] Banco de dados PostgreSQL configurado
- [ ] Variáveis de ambiente configuradas
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Arquivos estáticos coletados
- [ ] Nginx configurado (opcional)
- [ ] SSL configurado (opcional)
- [ ] Systemd service configurado
- [ ] Logs configurados
- [ ] Backup automático configurado
- [ ] Monitoramento configurado
- [ ] Testes executados
- [ ] Health check funcionando

## 🆘 Solução de Problemas

### Problema: Erro de conexão com banco de dados
```bash
# Verificar se o PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar logs do PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Problema: Erro de permissão
```bash
# Verificar permissões dos arquivos
ls -la /path/to/django_base/

# Corrigir permissões
sudo chown -R www-data:www-data /path/to/django_base/
sudo chmod -R 755 /path/to/django_base/
```

### Problema: Erro de SSL
```bash
# Verificar certificados
openssl x509 -in /path/to/certificate.crt -text -noout

# Testar SSL
openssl s_client -connect staging.seudominio.com:443
```

---

**🎉 Parabéns! Seu ambiente de homologação está configurado e pronto para uso!**
