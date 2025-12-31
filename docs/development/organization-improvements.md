# 📁 Melhorias de Organização do Projeto

Este documento lista melhorias sugeridas para a organização de arquivos, pastas e nomenclatura do projeto Django Base.

## 🎯 Objetivos

- Melhorar a clareza e navegabilidade do projeto
- Facilitar a manutenção e evolução
- Padronizar nomenclatura e estrutura
- Otimizar para diferentes tipos de uso (template, projeto base, etc.)

## 📋 Melhorias Propostas

### 1. Estrutura de Diretórios

#### 1.1 Separação de Configurações por Ambiente

**Problema Atual:**
- Configurações misturadas em `project/project/settings.py`
- Dificuldade em gerenciar diferentes ambientes

**Sugestão:**
```
project/project/
├── settings/
│   ├── __init__.py
│   ├── base.py          # Configurações base
│   ├── development.py   # Configurações de desenvolvimento
│   ├── staging.py       # Configurações de staging
│   ├── production.py    # Configurações de produção
│   └── test.py          # Configurações de teste
```

**Benefícios:**
- Separação clara de responsabilidades
- Facilita manutenção por ambiente
- Reduz risco de expor configurações sensíveis

#### 1.2 Organização de Assets

**Problema Atual:**
- Assets espalhados em diferentes locais
- Falta de estrutura clara para imagens, CSS, JS

**Sugestão:**
```
project/core/
├── static/
│   ├── css/
│   ├── js/
│   ├── img/
│   └── fonts/
├── templates/
│   └── core/
│       ├── base.html
│       └── components/
└── media/  # Apenas em desenvolvimento
```

**Benefícios:**
- Estrutura mais clara e profissional
- Facilita uso de ferramentas de build (webpack, etc.)
- Melhor organização para projetos maiores

### 2. Nomenclatura

#### 2.1 Padronização de Nomes de Arquivos

**Regras Propostas:**
- **Models**: `user.py`, `product.py` (singular, lowercase)
- **Views**: `user_views.py`, `auth_views.py` (plural + `_views`)
- **Serializers**: `user_serializers.py` (plural + `_serializers`)
- **Tests**: `test_user.py`, `test_auth.py` (prefixo `test_`)
- **Use Cases**: `user_use_cases.py` (plural + `_use_cases`)
- **Repositories**: `user_repository.py` (singular + `_repository`)

**Benefícios:**
- Consistência em todo o projeto
- Facilita localização de arquivos
- Melhora experiência do desenvolvedor

#### 2.2 Nomenclatura de Variáveis e Classes

**Regras Propostas:**
- **Classes**: PascalCase (`UserRepository`, `CreateUserUseCase`)
- **Funções/Métodos**: snake_case (`create_user`, `get_all_users`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_RETRY_ATTEMPTS`)
- **Variáveis privadas**: `_private_variable` (prefixo `_`)

### 3. Organização de Documentação

#### 3.1 Estrutura Atual vs. Proposta

**Atual:**
```
docs/
├── architecture/
├── development/
├── setup/
└── security/
```

**Melhorias:**
- Adicionar `docs/guides/` para tutoriais passo-a-passo
- Adicionar `docs/examples/` para exemplos de código
- Adicionar `docs/faq/` para perguntas frequentes
- Adicionar `docs/migration/` para guias de migração

#### 3.2 Documentação de Código

**Sugestão:**
- Adicionar docstrings em todos os módulos públicos
- Usar formato Google ou NumPy para docstrings
- Incluir exemplos de uso nos docstrings
- Manter documentação sincronizada com código

### 4. Configurações e Scripts

#### 4.1 Organização de Scripts

**Problema Atual:**
- Scripts na raiz ou em `scripts/` sem organização clara

**Sugestão:**
```
scripts/
├── setup/          # Scripts de configuração inicial
│   ├── generate_env.py
│   └── setup_oauth.py
├── maintenance/    # Scripts de manutenção
│   ├── backup_db.py
│   └── cleanup.py
├── testing/        # Scripts de teste
│   ├── test_endpoints.sh
│   └── revisao_completa.sh
└── deployment/    # Scripts de deploy
    └── deploy.sh
```

**Benefícios:**
- Organização clara por função
- Facilita manutenção
- Melhora descoberta de scripts

#### 4.2 Configurações de Ferramentas

**Sugestão:**
- Mover todas as configurações para `.config/` ou manter na raiz com prefixo claro
- Agrupar configurações relacionadas

```
.config/
├── python/
│   ├── mypy.ini
│   ├── pytest.ini
│   └── pydocstyle.ini
├── docker/
│   └── docker-compose.override.yml.example
└── ci/
    └── sonar-project.properties
```

**OU manter na raiz com nomenclatura clara:**
- `mypy.ini` → `python-mypy.ini`
- `pytest.ini` → `python-pytest.ini`

### 5. Separação de Template vs. Projeto

#### 5.1 Arquivos Específicos de Template

**Sugestão:**
- Mover arquivos específicos do template para `.template/` ou `template_files/`
- Incluir apenas arquivos essenciais no template final

```
template_files/
├── cookiecutter.json
├── hooks/
│   ├── pre_gen_project.py
│   └── post_gen_project.py
└── examples/
    └── .env.example
```

### 6. Melhorias de Git

#### 6.1 Estrutura de Branches

**Sugestão:**
- `main` - Código estável
- `develop` - Desenvolvimento ativo
- `feature/*` - Novas funcionalidades
- `fix/*` - Correções de bugs
- `docs/*` - Melhorias de documentação

#### 6.2 Arquivos de Configuração Git

**Sugestão:**
- Adicionar `.gitattributes` para normalização de linha
- Melhorar `.gitignore` com mais padrões
- Adicionar `.gitmessage` para template de commits

### 7. CI/CD e Automação

#### 7.1 Organização de Workflows

**Sugestão:**
```
.github/
├── workflows/
│   ├── ci/
│   │   ├── test.yml
│   │   └── lint.yml
│   ├── cd/
│   │   └── deploy.yml
│   └── maintenance/
│       └── dependency-update.yml
├── ISSUE_TEMPLATE/
└── PULL_REQUEST_TEMPLATE.md
```

### 8. Testes

#### 8.1 Organização de Testes

**Sugestão:**
```
project/core/tests/
├── unit/
│   ├── domain/
│   ├── use_cases/
│   └── repositories/
├── integration/
│   ├── api/
│   └── database/
├── e2e/
│   └── scenarios/
└── fixtures/
    └── factories.py
```

**Benefícios:**
- Separação clara por tipo de teste
- Facilita execução seletiva
- Melhora organização

### 9. Dependências

#### 9.1 Separação de Requirements

**Sugestão:**
```
project/
├── requirements/
│   ├── base.txt        # Dependências base
│   ├── development.txt # Dependências de desenvolvimento
│   ├── production.txt  # Dependências de produção
│   └── test.txt        # Dependências de teste
└── requirements.txt    # Aponta para base.txt (compatibilidade)
```

**Benefícios:**
- Instalação seletiva por ambiente
- Reduz tamanho de imagens Docker
- Melhora segurança

### 10. Docker

#### 10.1 Organização de Dockerfiles

**Sugestão:**
```
docker/
├── Dockerfile.base
├── Dockerfile.dev
├── Dockerfile.prod
├── docker-compose.dev.yml
├── docker-compose.prod.yml
└── .dockerignore
```

**Benefícios:**
- Organização clara
- Facilita manutenção
- Melhora reutilização

## 📊 Priorização

### Alta Prioridade
1. Separação de configurações por ambiente
2. Padronização de nomenclatura
3. Organização de scripts
4. Separação de requirements

### Média Prioridade
5. Organização de assets
6. Melhorias de estrutura de testes
7. Organização de documentação
8. Estrutura de branches Git

### Baixa Prioridade
9. Reorganização de Dockerfiles
10. Separação template vs. projeto
11. Configurações de ferramentas

## 🚀 Implementação

### Fase 1: Fundação
- Padronizar nomenclatura
- Organizar scripts
- Separar requirements

### Fase 2: Estrutura
- Separar configurações por ambiente
- Reorganizar testes
- Melhorar organização de assets

### Fase 3: Refinamento
- Otimizar Docker
- Melhorar documentação
- Implementar melhorias de Git

## 📝 Notas

- Todas as mudanças devem ser retrocompatíveis quando possível
- Documentar breaking changes claramente
- Manter referências atualizadas
- Testar em diferentes ambientes antes de aplicar

---

**Última atualização:** 2024-12-31
**Status:** Propostas para discussão e implementação gradual

