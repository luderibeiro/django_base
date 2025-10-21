# 🚀 Django Base - Template com Arquitetura Limpa

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://djangoproject.com)
[![Version](https://img.shields.io/badge/Version-2.1.0-orange.svg)](https://github.com/luderibeiro/django_base/releases)
[![Tests](https://img.shields.io/badge/Tests-93%25%20coverage-brightgreen.svg)](https://github.com/luderibeiro/django_base/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=django-base-template&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=django-base-template)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=django-base-template&metric=coverage)](https://sonarcloud.io/summary/new_code?id=django-base-template)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=django-base-template&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=django-base-template)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-MkDocs-blue.svg)](https://luderibeiro.github.io/django_base/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)

**🌟 Template profissional para projetos Django com Arquitetura Limpa**

[📖 Documentação](https://luderibeiro.github.io/django_base/) • [🚀 Início Rápido](#-início-rápido) • [🏗️ Arquitetura](#️-arquitetura) • [🤝 Contribuir](#-contribuição)

</div>

---

## 🎯 Sobre o Projeto

Este template Django oferece uma **base sólida e profissional** para desenvolvimento de aplicações web e APIs, seguindo os princípios da **Clean Architecture**. Ideal para:

-   🔥 **Startups** que precisam de desenvolvimento rápido e escalável
-   🏢 **Empresas** que buscam padronização e qualidade de código
-   👨‍💻 **Desenvolvedores** que querem aprender boas práticas de arquitetura
-   🎓 **Estudantes** interessados em projetos bem estruturados

### ✨ Principais Características

-   🏗️ **Arquitetura Limpa** - Separação clara de responsabilidades
-   📊 **93% Cobertura de Testes** - Suite completa de testes unitários e de integração
-   📖 **OpenAPI/Swagger** - Documentação automática da API
-   🔧 **Pre-commit Hooks** - Qualidade de código automatizada
-   🐍 **MyPy** - Verificação de tipos estática
-   🐳 **Docker Ready** - Containerização completa para desenvolvimento e produção
-   🚀 **GitHub Actions CI/CD** - Pipeline completo de integração contínua
-   📚 **Documentação Rica** - MkDocs com MkDocstrings para documentação automática
-   🔧 **Makefile Poderoso** - 20+ comandos de automação de desenvolvimento
-   🎨 **Interface Admin** - Django Jazzmin para administração elegante
-   🔐 **Autenticação OAuth2** - Sistema de autenticação robusto
-   📊 **API REST** - Django REST Framework configurado

## 🚀 Início Rápido

### Pré-requisitos

-   Python 3.12+
-   Docker & Docker Compose (opcional)
-   Git

### ⚡ Setup em 3 comandos

```bash
# 1. Clone o template
git clone https://github.com/luderibeiro/django_base.git meu_projeto
cd meu_projeto

# 2. Configure o ambiente
make setup

# 3. Inicie o servidor
make run
```

🎉 **Pronto!** Acesse <http://127.0.0.1:8000>

### 🐳 Com Docke

```bash
# Desenvolvimento
make docker-run

# Produção
make docker-prod
```

## 🏗️ Arquitetura

```bash
project/
├── core/                    # Aplicação principal
│   ├── domain/             # Regras de negócio
│   ├── repositories/       # Acesso a dados
│   ├── api/               # Endpoints REST
│   └── admin/             # Interface administrativa
├── project/               # Configurações Django
└── tests/                 # Testes automatizados
```

### 🎯 Camadas da Arquitetura

-   **🎯 Domain**: Entidades e regras de negócio
-   **🔄 Repository**: Abstração de acesso a dados
-   **🌐 API**: Endpoints e serializers
-   **⚙️ Infrastructure**: Configurações e integrações

## 📋 Comandos Disponíveis

```bash
make help              # Lista todos os comandos
make setup             # Configuração inicial completa
make test              # Executa todos os testes
make test-coverage     # Testes com cobertura
make lint              # Análise de código
make format            # Formatação automática
make docs-serve        # Serve documentação local
make clean             # Limpeza de arquivos temporários
```

## 🛠️ Tecnologias

-   **Backend**: Django 5.2+, Django REST Framework
-   **Database**: PostgreSQL (produção), SQLite (desenvolvimento)
-   **Authentication**: Django OAuth Toolkit
-   **Testing**: pytest, pytest-django
-   **Documentation**: MkDocs
-   **Containerization**: Docker, Docker Compose
-   **Code Quality**: Black, Flake8, pip-audit

## 📖 Documentação Completa

Para guias detalhados, exemplos e referências da API, acesse nossa [**documentação completa**](https://luderibeiro.github.io/django_base/).

### 📚 Guias Disponíveis

-   [🚀 Setup do Projeto](https://luderibeiro.github.io/django_base/setup/project-setup/)
-   [🏗️ Arquitetura Detalhada](https://luderibeiro.github.io/django_base/architecture/)
-   [🧪 Testes Automatizados](https://luderibeiro.github.io/django_base/development/automated-testing/)
-   [🚀 Deploy em Produção](https://luderibeiro.github.io/django_base/setup/production-setup/)

## 🤝 Contribuição

Contribuições são muito bem-vindas! Este projeto foi criado para ser um **template comunitário**.

### 💡 Como Contribuir

1. 🍴 Faça um fork do projeto
2. 🌟 Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. ✅ Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push para a branch (`git push origin feature/AmazingFeature`)
5. 🔄 Abra um Pull Request

### 🎯 Ideias para Contribuição

-   📱 Templates específicos (e-commerce, blog, API, etc.)
-   🔧 Melhorias na automação
-   📚 Tradução da documentação
-   🧪 Novos casos de teste
-   🎨 Melhorias na UI/UX

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo LICENSE para detalhes.

## 🌟 Apoie o Projeto

Se este template foi útil para você:

-   ⭐ Dê uma estrela no repositório
-   🍴 Faça um fork para suas customizações
-   📢 Compartilhe com outros desenvolvedores
-   🐛 Reporte bugs ou sugira melhorias

---

<div align="center">

**Desenvolvido com ❤️ para a comunidade Django**

[📖 Documentação](https://luderibeiro.github.io/django_base/) • [🐛 Issues](https://github.com/luderibeiro/django_base/issues) • [💬 Discussões](https://github.com/luderibeiro/django_base/discussions)

</div>
