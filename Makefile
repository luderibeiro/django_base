# Django Base - Makefile para Automação de Tarefas
# Template Django com Arquitetura Limpa

.PHONY: help setup install test run clean docker-build docker-run docker-stop migrate makemigrations createsuperuser lint format security-check docs-serve docs-build type-check check collectstatic shell

# Variáveis
PYTHON := python3
PIP := pip
VENV := venv
PROJECT_DIR := project
REQUIREMENTS := $(PROJECT_DIR)/requirements.txt
PYTEST := pytest
MANAGE := $(PYTHON) manage.py

# Cores para output (usando tput para compatibilidade)
RED := $$(tput setaf 1 2>/dev/null || echo '\033[0;31m')
GREEN := $$(tput setaf 2 2>/dev/null || echo '\033[0;32m')
YELLOW := $$(tput setaf 3 2>/dev/null || echo '\033[1;33m')
BLUE := $$(tput setaf 4 2>/dev/null || echo '\033[0;34m')
NC := $$(tput sgr0 2>/dev/null || echo '\033[0m')

# Help
help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)Django Base - Template com Arquitetura Limpa$(NC)"
	@echo "$(YELLOW)Comandos disponíveis:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ============================================================================
# SETUP E INSTALAÇÃO
# ============================================================================

setup: ## Configura o ambiente de desenvolvimento completo
	@echo "$(BLUE)🚀 Configurando ambiente de desenvolvimento...$(NC)"
	@if [ ! -f ".env" ] && [ ! -f "dotenv_files/.env" ]; then \
		echo "$(YELLOW)📝 Arquivo .env não encontrado. Gerando automaticamente...$(NC)"; \
		$(PYTHON) scripts/generate_env.py || echo "$(YELLOW)⚠️  Não foi possível gerar .env automaticamente. Crie manualmente.$(NC)"; \
	fi
	@$(MAKE) install
	@$(MAKE) migrate
	@echo "$(GREEN)✅ Ambiente configurado com sucesso!$(NC)"
	@echo "$(YELLOW)💡 Execute 'make run' para iniciar o servidor$(NC)"
	@echo "$(YELLOW)💡 Execute 'make createsuperuser' para criar um superusuário$(NC)"

install: ## Instala todas as dependências
	@echo "$(BLUE)📦 Instalando dependências...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(YELLOW)📁 Criando ambiente virtual...$(NC)"; \
		$(PYTHON) -m venv $(VENV); \
	fi
	@echo "$(YELLOW)🔄 Ativando ambiente virtual...$(NC)"
	@. $(VENV)/bin/activate && $(PIP) install --upgrade pip
	@. $(VENV)/bin/activate && $(PIP) install -r $(REQUIREMENTS)
	@echo "$(GREEN)✅ Dependências instaladas com sucesso!$(NC)"

# ============================================================================
# DESENVOLVIMENTO
# ============================================================================

run: ## Inicia o servidor de desenvolvimento
	@echo "$(BLUE)🚀 Iniciando servidor de desenvolvimento...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && $(MANAGE) runserver
	@echo "$(GREEN)✅ Servidor iniciado em http://127.0.0.1:8000$(NC)"

shell: ## Abre o shell do Django
	@echo "$(BLUE)🐍 Abrindo shell do Django...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && $(MANAGE) shell

check: ## Executa verificações do Django
	@echo "$(BLUE)🔍 Executando verificações do Django...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && $(MANAGE) check
	@echo "$(GREEN)✅ Verificações concluídas!$(NC)"

# ============================================================================
# BANCO DE DADOS
# ============================================================================

migrate: ## Executa migrações do banco de dados
	@echo "$(BLUE)🗄️ Executando migrações...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && $(MANAGE) migrate
	@echo "$(GREEN)✅ Migrações executadas com sucesso!$(NC)"

makemigrations: ## Cria novas migrações
	@echo "$(BLUE)📝 Criando migrações...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && $(MANAGE) makemigrations
	@echo "$(GREEN)✅ Migrações criadas com sucesso!$(NC)"

createsuperuser: ## Cria um superusuário
	@echo "$(BLUE)👤 Criando superusuário...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && $(MANAGE) createsuperuser
	@echo "$(GREEN)✅ Superusuário criado com sucesso!$(NC)"

collectstatic: ## Coleta arquivos estáticos
	@echo "$(BLUE)📁 Coletando arquivos estáticos...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && $(MANAGE) collectstatic --noinput
	@echo "$(GREEN)✅ Arquivos estáticos coletados!$(NC)"

# ============================================================================
# TESTES
# ============================================================================

test: ## Executa todos os testes
	@echo "$(BLUE)🧪 Executando testes...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && export PYTHONPATH=$$PWD && $(PYTEST) -v
	@echo "$(GREEN)✅ Testes executados com sucesso!$(NC)"

test-coverage: ## Executa testes com cobertura
	@echo "$(BLUE)🧪 Executando testes com cobertura...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && export PYTHONPATH=$$PWD && $(PYTEST) --cov=. --cov-config=../.coveragerc --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✅ Relatório de cobertura gerado em htmlcov/$(NC)"

# ============================================================================
# QUALIDADE DE CÓDIGO
# ============================================================================

lint: ## Executa linting no código
	@echo "$(BLUE)🔍 Executando linting...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && flake8 . --exclude=migrations,venv,__pycache__
	@echo "$(GREEN)✅ Linting concluído!$(NC)"

format: ## Formata o código com Black
	@echo "$(BLUE)🎨 Formatando código...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && black . --exclude=migrations
	@echo "$(GREEN)✅ Código formatado!$(NC)"

type-check: ## Executa verificação de tipos com mypy
	@echo "$(BLUE)🔍 Verificando tipos (mypy)...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && mypy --config-file=../mypy.ini core/
	@echo "$(GREEN)✅ Verificação de tipos concluída!$(NC)"

security-check: ## Verifica vulnerabilidades de segurança
	@echo "$(BLUE)🔒 Verificando vulnerabilidades...$(NC)"
	@cd $(PROJECT_DIR) && . ../$(VENV)/bin/activate && pip-audit
	@echo "$(GREEN)✅ Verificação de segurança concluída!$(NC)"

analyze: ## Análise completa do código (lint + type-check + security)
	@echo "$(BLUE)🔍 Executando análise completa do código...$(NC)"
	@$(MAKE) lint
	@$(MAKE) type-check
	@$(MAKE) security-check
	@echo "$(GREEN)✅ Análise completa concluída!$(NC)"

# ============================================================================
# DOCUMENTAÇÃO
# ============================================================================

docs-serve: ## Serve a documentação localmente
	@echo "$(BLUE)📚 Servindo documentação...$(NC)"
	@mkdocs serve
	@echo "$(GREEN)✅ Documentação disponível em http://127.0.0.1:8000$(NC)"

docs-build: ## Constrói a documentação
	@echo "$(BLUE)📚 Construindo documentação...$(NC)"
	@mkdocs build
	@echo "$(GREEN)✅ Documentação construída em site/$(NC)"

# ============================================================================
# DOCKER
# ============================================================================

docker-build: ## Constrói a imagem Docker (produção)
	@echo "$(BLUE)🐳 Construindo imagem Docker de produção...$(NC)"
	@docker build -t django-base:latest .
	@echo "$(GREEN)✅ Imagem Docker construída com sucesso!$(NC)"

docker-build-dev: ## Constrói a imagem Docker de desenvolvimento
	@echo "$(BLUE)🐳 Construindo imagem Docker de desenvolvimento...$(NC)"
	@docker build -f Dockerfile.dev -t django-base:dev .
	@echo "$(GREEN)✅ Imagem Docker de desenvolvimento construída!$(NC)"

docker-run: ## Executa o container Docker (desenvolvimento)
	@echo "$(BLUE)🐳 Executando container Docker...$(NC)"
	@docker-compose -f docker-compose.dev.yml up --build
	@echo "$(GREEN)✅ Container Docker executando!$(NC)"

docker-stop: ## Para o container Docker
	@echo "$(BLUE)🐳 Parando container Docker...$(NC)"
	@docker-compose -f docker-compose.dev.yml down
	@echo "$(GREEN)✅ Container Docker parado!$(NC)"

docker-prod: ## Executa em modo produção com Docker
	@echo "$(BLUE)🐳 Executando em modo produção...$(NC)"
	@docker-compose -f docker-compose.prod.yml up --build -d
	@echo "$(GREEN)✅ Aplicação rodando em produção!$(NC)"

# ============================================================================
# LIMPEZA
# ============================================================================

clean: ## Limpa arquivos temporários e cache
	@echo "$(BLUE)🧹 Limpando arquivos temporários...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf htmlcov/ .coverage
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

clean-all: clean ## Limpa tudo incluindo ambiente virtual
	@echo "$(BLUE)🧹 Limpando ambiente virtual...$(NC)"
	@rm -rf $(VENV)
	@echo "$(GREEN)✅ Limpeza completa concluída!$(NC)"

# ============================================================================
# UTILITÁRIOS
# ============================================================================

generate-env: ## Gera arquivo .env com valores seguros
	@echo "$(BLUE)📝 Gerando arquivo .env...$(NC)"
	@$(PYTHON) scripts/generate_env.py
	@echo "$(GREEN)✅ Arquivo .env gerado!$(NC)"

# ============================================================================
# CI/CD
# ============================================================================

ci: ## Pipeline de CI/CD completo
	@echo "$(BLUE)🔄 Executando pipeline CI/CD...$(NC)"
	@$(MAKE) install
	@$(MAKE) lint
	@$(MAKE) type-check
	@$(MAKE) security-check
	@$(MAKE) test-coverage
	@$(MAKE) docs-build
	@echo "$(GREEN)✅ Pipeline CI/CD concluído!$(NC)"

# Default target
.DEFAULT_GOAL := help
