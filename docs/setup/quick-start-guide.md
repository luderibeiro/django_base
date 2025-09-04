# 🚀 Guia de Início Rápido

Este guia te levará do zero ao projeto rodando em menos de 5 minutos!

## 📋 Pré-requisitos

### Obrigatórios
- **Python 3.12+** ([Download](https://python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))

### Opcionais (mas recomendados)
- **Docker & Docker Compose** ([Download](https://docker.com/get-started))
- **Make** (geralmente já instalado no Linux/Mac)

## ⚡ Setup em 3 Comandos

### Opção 1: Com Makefile (Recomendado)

```bash
# 1. Clone o template
git clone https://github.com/luderibeiro/django_base.git meu-projeto
cd meu-projeto

# 2. Configure tudo automaticamente
make setup

# 3. Inicie o servidor
make run
```

### Opção 2: Com Docker

```bash
# 1. Clone o template
git clone https://github.com/luderibeiro/django_base.git meu-projeto
cd meu-projeto

# 2. Inicie com Docker
make docker-run
```

## 🎯 Verificando se Funcionou

Após executar os comandos acima, você deve ver:

```
✅ Ambiente configurado com sucesso!
🚀 Servidor iniciado em http://127.0.0.1:8000
```

Acesse http://127.0.0.1:8000 no seu navegador e você verá a página inicial do Django.

## 🔐 Criação de Superusuário

O comando `make setup` solicitará que você crie um superusuário interativamente:

```bash
# Durante o setup, você será solicitado a criar credenciais seguras
make createsuperuser
```

**⚠️ Importante**: Sempre use credenciais seguras em produção!

Acesse http://127.0.0.1:8000/admin para entrar no painel administrativo.

## 🧪 Executando Testes

```bash
# Todos os testes
make test

# Testes com cobertura
make test-coverage

# Testes em modo watch (executa automaticamente quando arquivos mudam)
make test-watch
```

## 🛠️ Comandos Úteis

```bash
make help              # Lista todos os comandos disponíveis
make status            # Mostra status do projeto
make clean             # Limpa arquivos temporários
make lint              # Verifica qualidade do código
make format            # Formata código automaticamente
make docs-serve        # Serve documentação localmente
```

## 🐳 Usando Docker

### Desenvolvimento
```bash
make docker-run        # Inicia containers de desenvolvimento
make docker-stop       # Para os containers
```

### Produção
```bash
make docker-prod       # Inicia em modo produção
```

## 🔧 Personalização Inicial

### 1. Renomeie o Projeto

```bash
# Substitua 'meu-projeto' pelo nome desejado
find . -name "*.py" -exec sed -i 's/django_base/meu_projeto/g' {} \;
```

### 2. Configure Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp dotenv_files/.env-example .env

# Edite com suas configurações
nano .env
```

### 3. Configure o Banco de Dados

Por padrão usa SQLite. Para PostgreSQL:

```bash
# Instale o PostgreSQL
# Ubuntu/Debian: sudo apt install postgresql postgresql-contrib
# macOS: brew install postgresql

# Configure no .env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## 🚨 Problemas Comuns

### Python não encontrado
```bash
# Verifique a versão
python3 --version

# Se não tiver Python 3.12+, instale:
# Ubuntu/Debian: sudo apt install python3.12
# macOS: brew install python@3.12
```

### Make não encontrado
```bash
# Ubuntu/Debian
sudo apt install make

# macOS (com Homebrew)
brew install make
```

### Permissões no Docker
```bash
# Adicione seu usuário ao grupo docker
sudo usermod -aG docker $USER
# Faça logout e login novamente
```

## 🎉 Próximos Passos

Agora que seu projeto está rodando:

1. 📖 Leia a [Documentação da Arquitetura](../architecture/overview.md)
2. 🧪 Explore os [Testes Automatizados](../development/automated-testing.md)
3. 🔐 Configure [Autenticação OAuth2](../development/oauth2-implementation.md)
4. 🚀 Prepare para [Deploy em Produção](production-setup.md)

## 💡 Dicas Pro

- Use `make test-watch` durante desenvolvimento
- Execute `make lint` antes de commits
- Use `make docs-serve` para ver a documentação localmente
- Configure seu IDE para usar o ambiente virtual em `venv/`

---

**🎯 Objetivo alcançado?** Seu projeto Django com Arquitetura Limpa está rodando!

Se encontrou algum problema, [abra uma issue](https://github.com/luderibeiro/django_base/issues) no GitHub.
