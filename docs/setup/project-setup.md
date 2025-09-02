# Configuração do Projeto

Este guia descreve como configurar e rodar o projeto localmente.

## Requisitos

-   Docker e Docker Compose instalados.
-   Python 3.11 ou superior (se for rodar sem Docker para desenvolvimento local).

## Configuração com Docker Compose (Recomendado)

A maneira mais fácil e recomendada de configurar o projeto é usando Docker Compose.

1.  **Construir e Iniciar os Serviços:**

    Navegue até a raiz do projeto e execute:

    ```bash
    docker-compose up --build
    ```

    Este comando construirá as imagens Docker e iniciará os serviços definidos no `docker-compose.yml` (servidor Django, banco de dados PostgreSQL, etc.).

2.  **Executar Migrações do Banco de Dados:**

    Após os serviços iniciarem, execute as migrações para configurar o banco de dados:

    ```bash
    docker-compose exec web python project/manage.py migrate
    ```

3.  **Criar um Superusuário (Admin):**

    Para acessar o painel de administração do Django, crie um superusuário:

    ```bash
    docker-compose exec web python project/manage.py createsuperuser
    ```

    Siga as instruções no terminal para criar o usuário.

4.  **Acessar a Aplicação:**

    -   A API estará disponível em `http://localhost:8000/v1/`.
    -   O painel de administração do Django estará em `http://localhost:8000/admin/` (o caminho pode variar dependendo da sua configuração em `settings.py`).

## Configuração Local (sem Docker)

Se você preferir rodar o projeto diretamente em sua máquina sem Docker:

1.  **Instalar Dependências:**

    Crie um ambiente virtual e instale as dependências:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r project/requirements.txt
    ```

2.  **Configurar Banco de Dados:**

    Você precisará ter um banco de dados PostgreSQL configurado e atualizar as configurações em `project/project/settings.py` com suas credenciais de banco de dados local.

3.  **Executar Migrações do Banco de Dados:**

    ```bash
    python project/manage.py migrate
    ```

4.  **Criar um Superusuário (Admin):**

    ```bash
    python project/manage.py createsuperuser
    ```

5.  **Rodar o Servidor de Desenvolvimento:**

    ```bash
    python project/manage.py runserver
    ```
