# Setup de Produção

Este guia detalha como configurar o ambiente de produção para o Django Base de forma segura e escalável.

## 📋 Pré-requisitos

- Servidor Ubuntu 20.04+ ou CentOS 8+
- Python 3.12+
- PostgreSQL 13+
- Redis 6+
- Nginx
- Certificado SSL válido
- Domínio configurado

## 🚀 Configuração Rápida com Makefile

```bash
# Clone o repositório
git clone https://github.com/luderibeiro/django_base.git
cd django_base

# Configure o ambiente de produção
make prod-setup
```

## ⚙️ Configuração Manual

### 1. **Preparar o Servidor**

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3.12 python3.12-venv python3.12-dev \
    postgresql postgresql-contrib redis-server nginx \
    git curl wget build-essential libpq-dev

# Criar usuário para a aplicação
sudo adduser --system --group --shell /bin/bash django
sudo mkdir -p /opt/django_base
sudo chown django:django /opt/django_base
```

### 2. **Configurar PostgreSQL**

```bash
# Conectar ao PostgreSQL
sudo -u postgres psql

# Criar banco de dados e usuário
CREATE DATABASE django_base_prod;
CREATE USER django_user WITH PASSWORD 'senha-super-segura-e-complexa';
GRANT ALL PRIVILEGES ON DATABASE django_base_prod TO django_user;
ALTER USER django_user CREATEDB;
\q

# Configurar PostgreSQL para produção
sudo nano /etc/postgresql/15/main/postgresql.conf
```

Configurações importantes no `postgresql.conf`:

```conf
# Configurações de performance
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Configurações de conexão
max_connections = 100
listen_addresses = 'localhost'

# Logging
log_destination = 'stderr'
logging_collector = on
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_min_duration_statement = 1000
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
```

```bash
# Reiniciar PostgreSQL
sudo systemctl restart postgresql
sudo systemctl enable postgresql
```

### 3. **Configurar Redis**

```bash
# Configurar Redis
sudo nano /etc/redis/redis.conf
```

Configurações importantes:

```conf
# Configurações de segurança
bind 127.0.0.1
protected-mode yes
requirepass senha-redis-super-segura

# Configurações de performance
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistência
save 900 1
save 300 10
save 60 10000
```

```bash
# Reiniciar Redis
sudo systemctl restart redis-server
sudo systemctl enable redis-server
```

### 4. **Deploy da Aplicação**

```bash
# Clonar repositório
sudo -u django git clone https://github.com/luderibeiro/django_base.git /opt/django_base
cd /opt/django_base

# Criar ambiente virtual
sudo -u django python3.12 -m venv venv
sudo -u django ./venv/bin/pip install --upgrade pip
sudo -u django ./venv/bin/pip install -r project/requirements.txt
sudo -u django ./venv/bin/pip install gunicorn psycopg2-binary
```

### 5. **Configurar Variáveis de Ambiente**

```bash
# Criar arquivo de ambiente
sudo -u django nano /opt/django_base/.env
```

Conteúdo do `.env`:

```bash
# Configurações Django
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-segura-e-complexa-aqui
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Banco de dados
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=django_base_prod
POSTGRES_USER=django_user
POSTGRES_PASSWORD=senha-super-segura-e-complexa
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://:senha-redis-super-segura@localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/django_base/production.log

# Segurança
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY
```

### 6. **Configurar Settings para Produção**

Crie o arquivo `project/project/settings_production.py`:

```python
import os
from .settings import *

# Configurações específicas para produção
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Banco de dados PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_DB', 'django_base_prod'),
        'USER': os.environ.get('POSTGRES_USER', 'django_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Cache com Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Sessões com Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Logging para produção
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.environ.get('LOG_FILE', '/var/log/django_base/production.log'),
            'maxBytes': 15728640,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Configurações de segurança
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() == 'true'
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True').lower() == 'true'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Arquivos estáticos e mídia
STATIC_ROOT = '/opt/django_base/staticfiles'
MEDIA_ROOT = '/opt/django_base/media'

# Configurações de performance
CONN_MAX_AGE = 60
```

### 7. **Executar Configurações Iniciais**

```bash
# Ativar ambiente virtual
sudo -u django bash -c "cd /opt/django_base && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=project.settings_production && cd project && python manage.py migrate"

# Criar superusuário
sudo -u django bash -c "cd /opt/django_base && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=project.settings_production && cd project && python manage.py createsuperuser"

# Coletar arquivos estáticos
sudo -u django bash -c "cd /opt/django_base && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=project.settings_production && cd project && python manage.py collectstatic --noinput"
```

### 8. **Configurar Gunicorn**

Crie o arquivo `/opt/django_base/gunicorn.conf.py`:

```python
# Gunicorn configuration file
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
accesslog = "/var/log/django_base/gunicorn_access.log"
errorlog = "/var/log/django_base/gunicorn_error.log"
loglevel = "warning"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
```

### 9. **Configurar Systemd Service**

Crie o arquivo `/etc/systemd/system/django-base.service`:

```ini
[Unit]
Description=Django Base Production
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=django
Group=django
WorkingDirectory=/opt/django_base
Environment=DJANGO_SETTINGS_MODULE=project.settings_production
ExecStart=/opt/django_base/venv/bin/gunicorn --config gunicorn.conf.py project.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3
KillMode=mixed
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl daemon-reload
sudo systemctl enable django-base
sudo systemctl start django-base
```

### 10. **Configurar Nginx**

Crie o arquivo `/etc/nginx/sites-available/django_base`:

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

# Upstream
upstream django_base {
    server 127.0.0.1:8000;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name seudominio.com www.seudominio.com;
    
    # SSL configuration
    ssl_certificate /etc/ssl/certs/seudominio.com.crt;
    ssl_certificate_key /etc/ssl/private/seudominio.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Static files
    location /static/ {
        alias /opt/django_base/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Media files
    location /media/ {
        alias /opt/django_base/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # API endpoints with rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://django_base;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Login endpoint with stricter rate limiting
    location /api/v1/auth/login/ {
        limit_req zone=login burst=5 nodelay;
        proxy_pass http://django_base;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Main application
    location / {
        proxy_pass http://django_base;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/django_base /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 11. **Configurar SSL com Let's Encrypt**

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Configurar renovação automática
sudo crontab -e
```

Adicionar ao crontab:

```bash
# Renovar certificados automaticamente
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🐳 Configuração com Docker

### 1. **Docker Compose para Produção**

Crie o arquivo `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: django_base_prod
      POSTGRES_USER: django_user
      POSTGRES_PASSWORD: senha-super-segura-e-complexa
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - django_network

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass senha-redis-super-segura
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - django_network

  web:
    build: .
    command: gunicorn project.wsgi:application --config gunicorn.conf.py
    environment:
      - DJANGO_SETTINGS_MODULE=project.settings_production
      - DEBUG=False
      - SECRET_KEY=sua-chave-secreta-super-segura-e-complexa
      - ALLOWED_HOSTS=seudominio.com,www.seudominio.com
      - POSTGRES_DB=django_base_prod
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=senha-super-segura-e-complexa
      - POSTGRES_HOST=db
      - REDIS_URL=redis://:senha-redis-super-segura@redis:6379/0
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - django_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/production.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - django_network

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:

networks:
  django_network:
    driver: bridge
```

### 2. **Executar com Docker**

```bash
# Construir e executar
docker-compose -f docker-compose.prod.yml up --build -d

# Executar migrações
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Criar superusuário
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## 🔒 Segurança

### 1. **Firewall**

```bash
# Configurar UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. **Fail2Ban**

```bash
# Instalar Fail2Ban
sudo apt install -y fail2ban

# Configurar
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
```

### 3. **Backup Automático**

Crie o script `/usr/local/bin/backup_django_base_prod.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/django_base_prod"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
pg_dump -h localhost -U django_user django_base_prod > $BACKUP_DIR/db_$DATE.sql

# Backup dos arquivos de mídia
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /opt/django_base/media/

# Backup dos arquivos estáticos
tar -czf $BACKUP_DIR/static_$DATE.tar.gz /opt/django_base/staticfiles/

# Backup das configurações
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /opt/django_base/.env /opt/django_base/gunicorn.conf.py

# Upload para S3 (opcional)
# aws s3 cp $BACKUP_DIR/db_$DATE.sql s3://seu-bucket/backups/
# aws s3 cp $BACKUP_DIR/media_$DATE.tar.gz s3://seu-bucket/backups/
# aws s3 cp $BACKUP_DIR/static_$DATE.tar.gz s3://seu-bucket/backups/
# aws s3 cp $BACKUP_DIR/config_$DATE.tar.gz s3://seu-bucket/backups/

# Manter apenas os últimos backups
find $BACKUP_DIR -name "*.sql" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup concluído: $DATE"
```

```bash
# Tornar executável
sudo chmod +x /usr/local/bin/backup_django_base_prod.sh

# Agendar no crontab
sudo crontab -e
```

```bash
# Executar backup diariamente às 3:00
0 3 * * * /usr/local/bin/backup_django_base_prod.sh
```

## 📊 Monitoramento

### 1. **Health Check**

Crie o endpoint em `project/core/views/health.py`:

```python
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
import psutil
import os

def health_check(request):
    """Endpoint para verificar a saúde da aplicação"""
    try:
        # Verificar banco de dados
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Verificar cache
        cache.set('health_check', 'ok', 10)
        cache.get('health_check')
        
        # Verificar Redis
        r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
        r.ping()
        
        # Verificar espaço em disco
        disk_usage = psutil.disk_usage('/')
        disk_free_percent = (disk_usage.free / disk_usage.total) * 100
        
        # Verificar memória
        memory = psutil.virtual_memory()
        memory_available_percent = memory.available / memory.total * 100
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'ok',
            'cache': 'ok',
            'redis': 'ok',
            'disk_free_percent': round(disk_free_percent, 2),
            'memory_available_percent': round(memory_available_percent, 2),
            'uptime': os.popen('uptime -p').read().strip()
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
sudo tail -f /var/log/django_base/production.log

# Filtrar erros
sudo grep "ERROR" /var/log/django_base/production.log

# Estatísticas de acesso
sudo awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr

# Monitorar performance
sudo htop
sudo iotop
sudo nethogs
```

### 3. **Alertas Automáticos**

Crie o script `/usr/local/bin/monitor_django_base.sh`:

```bash
#!/bin/bash
LOG_FILE="/var/log/django_base/monitor.log"
ALERT_EMAIL="admin@seudominio.com"

# Verificar se a aplicação está respondendo
if ! curl -f -s http://localhost:8000/health/ > /dev/null; then
    echo "$(date): Aplicação não está respondendo" >> $LOG_FILE
    echo "Aplicação Django Base não está respondendo em $(date)" | mail -s "ALERTA: Django Base Down" $ALERT_EMAIL
fi

# Verificar espaço em disco
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$(date): Espaço em disco baixo: ${DISK_USAGE}%" >> $LOG_FILE
    echo "Espaço em disco baixo: ${DISK_USAGE}% em $(date)" | mail -s "ALERTA: Espaço em Disco Baixo" $ALERT_EMAIL
fi

# Verificar memória
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ $MEMORY_USAGE -gt 90 ]; then
    echo "$(date): Uso de memória alto: ${MEMORY_USAGE}%" >> $LOG_FILE
    echo "Uso de memória alto: ${MEMORY_USAGE}% em $(date)" | mail -s "ALERTA: Uso de Memória Alto" $ALERT_EMAIL
fi
```

```bash
# Tornar executável
sudo chmod +x /usr/local/bin/monitor_django_base.sh

# Agendar no crontab
sudo crontab -e
```

```bash
# Executar monitoramento a cada 5 minutos
*/5 * * * * /usr/local/bin/monitor_django_base.sh
```

## 🔧 Comandos Úteis

```bash
# Verificar status dos serviços
sudo systemctl status django-base
sudo systemctl status postgresql
sudo systemctl status redis-server
sudo systemctl status nginx

# Reiniciar serviços
sudo systemctl restart django-base
sudo systemctl restart postgresql
sudo systemctl restart redis-server
sudo systemctl restart nginx

# Ver logs
sudo journalctl -u django-base -f
sudo tail -f /var/log/django_base/production.log
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Backup manual
sudo /usr/local/bin/backup_django_base_prod.sh

# Restaurar backup
sudo -u postgres psql django_base_prod < /var/backups/django_base_prod/db_20240101_120000.sql

# Verificar certificados SSL
sudo certbot certificates

# Renovar certificados
sudo certbot renew --dry-run
sudo certbot renew
```

## ✅ Checklist de Produção

- [ ] Servidor configurado e atualizado
- [ ] PostgreSQL configurado e otimizado
- [ ] Redis configurado e otimizado
- [ ] Aplicação deployada
- [ ] Variáveis de ambiente configuradas
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Arquivos estáticos coletados
- [ ] Gunicorn configurado
- [ ] Systemd service configurado
- [ ] Nginx configurado e otimizado
- [ ] SSL configurado
- [ ] Firewall configurado
- [ ] Fail2Ban configurado
- [ ] Backup automático configurado
- [ ] Monitoramento configurado
- [ ] Alertas configurados
- [ ] Testes executados
- [ ] Health check funcionando
- [ ] Logs configurados

## 🆘 Solução de Problemas

### Problema: Aplicação não inicia
```bash
# Verificar logs
sudo journalctl -u django-base -f

# Verificar configurações
sudo -u django bash -c "cd /opt/django_base && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=project.settings_production && cd project && python manage.py check"
```

### Problema: Erro de banco de dados
```bash
# Verificar conexão
sudo -u postgres psql -c "SELECT 1"

# Verificar logs do PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Problema: Erro de SSL
```bash
# Verificar certificados
sudo certbot certificates

# Testar SSL
openssl s_client -connect seudominio.com:443
```

### Problema: Performance baixa
```bash
# Verificar recursos
htop
iotop
nethogs

# Verificar logs de acesso
sudo tail -f /var/log/nginx/access.log

# Verificar configurações do Gunicorn
sudo nano /opt/django_base/gunicorn.conf.py
```

---

**🎉 Parabéns! Seu ambiente de produção está configurado e pronto para receber usuários!**
