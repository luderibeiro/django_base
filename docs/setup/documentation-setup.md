# Configuração da Documentação com MkDocs e GitHub Pages

Este guia descreve como configurar e gerenciar a documentação do projeto usando MkDocs, com o tema Material, e publicá-la no GitHub Pages.

## 1. Instalação do MkDocs

Certifique-se de ter um ambiente virtual Python ativo (e.g., `source venv/bin/activate`). Em seguida, instale o MkDocs e o tema Material:

```bash
pip install mkdocs mkdocs-material
```

## 2. Estrutura da Documentação

A documentação está organizada no diretório `docs/`. O arquivo principal é `docs/index.md` (que substitui o antigo `docs/README.md`). Os demais arquivos Markdown estão distribuídos em subdiretórios lógicos (e.g., `architecture/`, `development/`, `setup/`).

## 3. Configuração do MkDocs (`mkdocs.yml`)

O arquivo `mkdocs.yml` na raiz do projeto configura o site da documentação. Ele define o nome do site, URL do repositório, tema, extensões Markdown e a estrutura de navegação (`nav`).

```yaml
site_name: Django Clean Architecture Base Project
site_url: https://your-username.github.io/django_base/ # Atualize com o seu URL
repo_url: https://github.com/your-username/django_base/ # Atualize com o seu repositório
edit_uri: edit/main/docs/ # Caminho para editar arquivos no GitHub

theme:
  name: material
  features:
    - navigation.expand
    - navigation.tabs
    - navigation.sections
    - search.highlight
    - search.suggest
    - toc.integrate
    - content.tabs.link
    - content.code.annotate
  palette:
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
      primary: teal
      accent: purple
    - scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
      primary: teal
      accent: lime

markdown_extensions:
  # ... (extensões configuradas)

nav:
  # ... (estrutura de navegação)
```

**Pontos importantes:**
- Atualize `site_url` e `repo_url` com as informações do seu próprio repositório e URL de publicação no GitHub Pages.
- A seção `nav` define a hierarquia e os links para todos os seus arquivos Markdown.

## 4. Visualização Local da Documentação

Para visualizar a documentação antes de publicá-la, execute o servidor de desenvolvimento do MkDocs:

```bash
mkdocs serve
```

Isso iniciará um servidor local, geralmente em `http://127.0.0.1:8000`. As alterações nos arquivos Markdown e no `mkdocs.yml` serão automaticamente recarregadas no navegador.

## 5. Publicação no GitHub Pages

Para publicar a documentação no GitHub Pages, o MkDocs usa a ferramenta `ghp-import` (que já foi instalada como dependência).

1.  **Gere e Implante a Documentação:**

    ```bash
    mkdocs gh-deploy
    ```

    Este comando fará o seguinte:
    -   Construirá o site estático da documentação no diretório `site/`.
    -   Criará um branch `gh-pages` no seu repositório Git (ou atualizará um existente).
    -   Fará o push do conteúdo do diretório `site/` para o branch `gh-pages`.

2.  **Configurar GitHub Pages no Repositório:**

    No seu repositório GitHub, vá em `Settings` > `Pages`:
    -   Em `Build and deployment`, selecione `Deploy from a branch`.
    -   Em `Branch`, selecione `gh-pages` e a pasta `/ (root)`. Salve as alterações.

    Sua documentação estará disponível no URL `https://your-username.github.io/your-repository-name/` (ou `https://your-organization.github.io/your-repository-name/`). Pode levar alguns minutos para o GitHub Pages construir e publicar o site pela primeira vez.

## 6. Automatizando a Publicação com GitHub Actions (Recomendado)

Para um fluxo de trabalho de open source eficiente, é altamente recomendável automatizar a publicação da documentação sempre que houver um push para o branch `main` (ou o branch principal que contém seus arquivos de documentação).

Você pode configurar um GitHub Action para isso. Um exemplo de workflow (`.github/workflows/deploy-docs.yml`):

```yaml
name: Deploy Docs

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.11 # Use a versão do seu projeto
      - run: pip install mkdocs mkdocs-material
      - run: mkdocs gh-deploy --force
```

Este workflow garantirá que sua documentação esteja sempre atualizada no GitHub Pages após cada push para o `main`.
