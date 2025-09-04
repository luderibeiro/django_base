# 🔒 Diretrizes de Segurança

## ⚠️ Credenciais e Dados Sensíveis

### 🚫 NUNCA Commitar

- Senhas em texto plano
- Chaves de API
- Tokens de autenticação
- Certificados SSL
- Arquivos de configuração com dados sensíveis

### ✅ Boas Práticas

#### 1. Variáveis de Ambiente

```bash
# .env (nunca commitado)
SECRET_KEY=sua-chave-super-secreta-aqui
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=sua-api-key-secreta
```

#### 2. GitHub Secrets

Para CI/CD, use GitHub Secrets:

- `SECRET_KEY_FOR_CI`
- `DATABASE_URL_TEST`
- `API_KEYS`

#### 3. Configuração Segura do Superusuário

```bash
# ✅ Correto - Interativo
make createsuperuser

# ❌ Incorreto - Hardcoded
# Nunca faça isso em código público
```

## 🛡️ Configurações de Produção

### Django Settings

```python
# settings/production.py
import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS').split(',')
```

### Banco de Dados

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
    }
}
```

## 🔐 Autenticação e Autorização

### OAuth2 Seguro

```python
# settings.py
OAUTH2_SETTINGS = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400,
}
```

### Middleware de Segurança

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configurações de segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## 📋 Checklist de Segurança

### Antes do Deploy
- [ ] Todas as credenciais estão em variáveis de ambiente
- [ ] `.env` está no `.gitignore`
- [ ] `DEBUG = False` em produção
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] HTTPS habilitado
- [ ] Certificado SSL válido
- [ ] Backup seguro configurado

### Monitoramento
- [ ] Logs de segurança habilitados
- [ ] Alertas de tentativas de acesso não autorizado
- [ ] Auditoria de dependências (pip-audit)
- [ ] Scans de vulnerabilidade regulares

## 🚨 Resposta a Incidentes

### Se Credenciais Foram Expostas

1. **Imediatamente**:
   - Revogar/alterar todas as credenciais expostas
   - Verificar logs de acesso
   - Notificar equipe de segurança

2. **Limpeza do Git**:
   ```bash
   # Remover do histórico (CUIDADO!)
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch arquivo-com-credenciais' \
   --prune-empty --tag-name-filter cat -- --all

   # Force push (coordenar com equipe)
   git push origin --force --all
   ```

3. **Prevenção**:
   - Implementar pre-commit hooks
   - Usar ferramentas como git-secrets
   - Treinamento da equipe

## 🔧 Ferramentas de Segurança

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### Auditoria Automática
```bash
# No Makefile
security-audit:
	pip-audit
	bandit -r project/
	safety check
```

## 📚 Recursos Adicionais

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [12 Factor App](https://12factor.net/)
- [Mozilla Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)

---

**🛡️ Lembre-se**: Segurança é responsabilidade de todos. Sempre revise código em busca de vulnerabilidades antes de fazer commit!
