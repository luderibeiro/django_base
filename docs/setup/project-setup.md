# Configuração do Projeto

Este guia descreve como configurar e rodar o projeto localmente.

## Requisitos

-   Docker e Docker Compose instalados.
-   Python 3.11 ou superior (se for rodar sem Docker para desenvolvimento local).

## Configuração com Docker Compose (Recomendado)

A maneira mais fácil e recomendada de configurar o projeto é usando Docker Compose, com arquivos de configuração separados para desenvolvimento e produção.

### 1. Ambiente de Desenvolvimento

Utilize o `docker-compose.dev.yml` (localizado em `docker/`) orquestra os serviços em desenvolvimento, e o `Dockerfile.dev` (localizado em `docker/`) contém as instruções para construir a imagem de desenvolvimento.

1.  **Construir e Iniciar os Serviços de Desenvolvimento:**

    Navegue até a raiz do projeto e execute:

    ```bash
    docker compose -f docker-compose.dev.yml up --build
    ```

    Este comando construirá a imagem Docker de desenvolvimento (`Dockerfile.dev`) e iniciará os serviços definidos no `docker-compose.dev.yml` (servidor Django, banco de dados PostgreSQL, etc.).

2.  **Executar Migrações do Banco de Dados:**

    Após os serviços iniciarem, execute as migrações para configurar o banco de dados:

    ```bash
    docker compose -f docker-compose.dev.yml exec project_dev python /app/project/manage.py migrate
    ```

3.  **Criar um Superusuário (Admin):**

    Para acessar o painel de administração do Django, crie um superusuário:

    ```bash
    docker compose -f docker-compose.dev.yml exec project_dev python /app/project/manage.py createsuperuser
    ```

    Siga as instruções no terminal para criar o usuário.

4.  **Acessar a Aplicação:**

    -   A API estará disponível em `http://localhost:8000/v1/`.
    -   O painel de administração do Django estará em `http://localhost:8000/admin/`.

### 2. Ambiente de Produção

Para simular o ambiente de produção localmente ou preparar para o deploy, utilize o `Dockerfile` (localizado em `docker/`) e o `docker-compose.prod.yml` (localizados em `docker/`) são usados para o ambiente de produção, otimizados para performance e escalabilidade.

1.  **Configurar Variáveis de Ambiente de Produção:**

    Crie o arquivo `dotenv_files/.env.prod` e preencha com as variáveis de ambiente necessárias para produção. Um exemplo pode ser encontrado no próprio arquivo comentado.

2.  **Construir e Iniciar os Serviços de Produção:**

    Navegue até a raiz do projeto e execute:

    ```bash
    docker compose -f docker-compose.prod.yml up --build -d
    ```

    Este comando construirá a imagem Docker de produção (`Dockerfile`) e iniciará os serviços em modo _detached_ (`-d`). Em produção, a porta exposta será a 80.

3.  **Executar Migrações do Banco de Dados (Produção):**

    ```bash
    docker compose -f docker-compose.prod.yml exec project_prod python /app/project/manage.py migrate
    ```

4.  **Criar um Superusuário (Admin - Produção):**

    ```bash
    docker compose -f docker-compose.prod.yml exec project_prod python /app/project/manage.py createsuperuser
    ```

5.  **Acessar a Aplicação (Produção Local):**

    -   A API estará disponível em `http://localhost/v1/`.
    -   O painel de administração do Django estará em `http://localhost/admin/`.

## Configuração Local (sem Docker)

Se você preferir rodar o projeto diretamente em sua máquina sem Docker, as instruções permanecem as mesmas:

1.  **Instalar Dependências:**

    Crie um ambiente virtual e instale as dependências:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r project/requirements.txt
    ```

2.  **Configurar Banco de Dados:**

    Você precisará ter um banco de dados PostgreSQL configurado e atualizar as configurações em `project/project/settings.py`
