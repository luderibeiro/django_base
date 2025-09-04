# 🚀 _django_base_ - Template Profissional com Arquitetura Limpa

<div align="center">
<a href="https://djangoproject.com/"><img src="https://img.shields.io/badge/Django-5.0+-green?style=for-the-badge&logo=django" alt="Django"></a>
<a href="https://python.org/"><img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" alt="Python"></a>
<a href="https://github.com/luderibeiro/django_base/actions"><img src="https://img.shields.io/badge/Tests-93%25%20coverage-brightgreen?style=for-the-badge" alt="Tests"></a>
<a href="https://github.com/luderibeiro/django_base/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"></a>
<a href="https://github.com/luderibeiro/django_base/releases"><img src="https://img.shields.io/badge/Version-2.1.0-orange?style=for-the-badge" alt="Version"></a>
</div>

**O template Django mais completo e profissional para iniciar seus projetos com Arquitetura Limpa!**

<div align="center">
<a href="https://github.com/luderibeiro/django_base/generate"><img src="https://img.shields.io/badge/Use%20this%20template-2DA44E?style=for-the-badge&logo=github" alt="Use this template"></a>
<a href="https://github.com/luderibeiro/django_base/fork"><img src="https://img.shields.io/badge/Fork%20on%20GitHub-181717?style=for-the-badge&logo=github" alt="Fork on GitHub"></a>
<a href="https://github.com/luderibeiro/django_base"><img src="https://img.shields.io/badge/Star%20on%20GitHub-181717?style=for-the-badge&logo=github" alt="Star on GitHub"></a>
</div>

---

## ✨ Por que escolher o django_base como seu template?

Este não é apenas mais um template Django. É uma **base sólida e profissional** que implementa os melhores padrões de desenvolvimento, seguindo rigorosamente os princípios da **Arquitetura Limpa**.

### 🎯 **Características Principais**

-   ✅ **93% de cobertura de testes** com testes unitários e de integração
-   ✅ **Arquitetura Limpa** implementada corretamente
-   ✅ **OpenAPI/Swagger** documentação automática da API
-   ✅ **Pre-commit hooks** para qualidade de código
-   ✅ **MyPy** verificação de tipos estática
-   ✅ **OAuth2** completo com django-oauth-toolkit
-   ✅ **Paginação e Filtragem** avançadas
-   ✅ **Logging e Tratamento de Exceções** robustos
-   ✅ **Docker** otimizado para dev e produção
-   ✅ **GitHub Actions CI/CD** pipeline completo
-   ✅ **Documentação completa** com MkDocs e MkDocstrings
-   ✅ **Makefile** com 20+ comandos de automação
-   ✅ **Configurações** para local, staging e produção

### 🏗️ **Arquitetura Limpa - Por que é importante?**

A Arquitetura Limpa garante que seu código seja:

-   🔄 **Independente de Frameworks**: Troque Django sem quebrar a lógica de negócio
-   🧪 **Testável**: Teste regras de negócio sem banco de dados ou UI
-   🎨 **Independente de UI**: Mude a interface sem afetar o sistema
-   🗄️ **Independente de Banco**: Troque PostgreSQL por MongoDB facilmente
-   🌐 **Independente de Agentes Externos**: Lógica de negócio isolada

---

## 🚀 Início Rápido

### 1. **Use este template**

```bash
# Clique no botão "Use this template" acima ou:
git clone https://github.com/luderibeiro/django_base.git meu-projeto
cd meu-projeto
```

### 2. **Setup com Makefile (Recomendado)**

```bash
# Instalar dependências e configurar ambiente
make setup

# Executar testes
make test

# Iniciar servidor de desenvolvimento
make run
```

### 3. **Setup Manual**

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r project/requirements.txt

# Configurar banco de dados
cd project
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar testes
pytest

# Iniciar servidor
python manage.py runserver
```

---

## 📚 Documentação Completa

### 🏛️ **Arquitetura**

-   [Visão Geral](architecture/overview.md) - Entenda a estrutura das camadas
-   [Camada de Domínio](architecture/domain-layer.md) - Entidades e regras de negócio
-   [Camada de Aplicação](architecture/application-layer.md) - Casos de uso
-   [Camada de Infraestrutura](architecture/infrastructure-layer.md) - Repositórios e gateways
-   [Camada de Apresentação](architecture/presentation-layer.md) - APIs e interfaces

### 🛠️ **Desenvolvimento**

-   [Testes Automatizados](development/automated-testing.md) - Suíte completa de testes
-   [Paginação e Filtragem](development/pagination-filtering.md) - APIs avançadas
-   [OAuth2 Implementation](development/oauth2-implementation.md) - Autenticação robusta
-   [Logging e Tratamento de Erros](development/logging-error-handling.md) - Observabilidade
-   [Integração Frontend](development/frontend-integration.md) - Guias para React/Vue/Angular

### ⚙️ **Setup e Deploy**

-   [Setup Local](setup/project-setup.md) - Ambiente de desenvolvimento
-   [Setup Homologação](setup/staging-setup.md) - Ambiente de testes
-   [Setup Produção](setup/production-setup.md) - Deploy em produção
-   [Configuração Docker](setup/production-setup.md) - Containers otimizados

---

## 🎯 **Casos de Uso Ideais**

Este template é perfeito para:

-   🏢 **APIs REST** profissionais e escaláveis
-   🛒 **E-commerce** com autenticação robusta
-   📊 **Sistemas de gestão** empresariais
-   🎓 **Plataformas educacionais** com múltiplos usuários
-   📱 **Backend para mobile apps** com autenticação OAuth2
-   🔐 **Sistemas com múltiplos perfis** de usuário

---

## 🤝 **Contribua e Crie Forks**

### **Contribuindo**

-   📖 Leia nosso [Guia de Contribuição](CONTRIBUTING.md)
-   🐛 Reporte bugs ou sugira melhorias
-   💡 Proponha novas funcionalidades
-   📝 Melhore a documentação

### **Criando Forks Especializados**

Este template é perfeito para criar forks especializados:

-   🛒 **django-ecommerce-base** - Template para e-commerce
-   🎓 **django-education-base** - Template para plataformas educacionais
-   🏥 **django-healthcare-base** - Template para sistemas de saúde
-   🏦 **django-finance-base** - Template para sistemas financeiros
-   📊 **django-analytics-base** - Template para dashboards e analytics

---

## 📊 **Estatísticas do Projeto**

-   **93% de cobertura de testes** com testes unitários e de integração
-   **Arquitetura Limpa** implementada corretamente
-   **OpenAPI/Swagger** documentação automática da API
-   **Pre-commit hooks** para qualidade de código
-   **MyPy** verificação de tipos estática
-   **Docker** otimizado para dev e produção
-   **GitHub Actions CI/CD** pipeline completo
-   **Documentação completa** com MkDocs
-   **Makefile** com 20+ comandos de automação

---

## 🏆 **Por que este template é diferente?**

1. **Arquitetura Limpa Real**: Não é apenas uma estrutura de pastas, é uma implementação real dos princípios
2. **Qualidade de Código**: Pre-commit hooks, MyPy, Black, Flake8 e Pydocstyle configurados
3. **Documentação Automática**: OpenAPI/Swagger + MkDocstrings para documentação sempre atualizada
4. **CI/CD Completo**: GitHub Actions com pipeline de testes, qualidade e deploy
5. **93% Cobertura de Testes**: Testes unitários e de integração abrangentes
6. **Automação Avançada**: Makefile com 20+ comandos para desenvolvimento
7. **Configurações Completas**: Local, staging e produção com Docker otimizado
8. **Comunidade Ativa**: Projeto em constante evolução com suporte da comunidade

---

<div align="center">

**🌟 Se este projeto te ajudou, considere dar uma estrela!**

<a href="https://github.com/luderibeiro/django_base"><img src="https://img.shields.io/badge/Star%20on%20GitHub-181717?style=for-the-badge&logo=github" alt="Star on GitHub"></a>
<a href="https://github.com/luderibeiro/django_base/fork"><img src="https://img.shields.io/badge/Fork%20on%20GitHub-181717?style=for-the-badge&logo=github" alt="Fork on GitHub"></a>

-   **Feito com ❤️ pela comunidade Django**

</div>
