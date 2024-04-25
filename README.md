# Template para Projetos em Django

Can't read portuguese? Read this README in [english](README-en.md)

Este repositório serve como um template para iniciar projetos em Python (versão 3.12) com o framework Django (versão 5.0).

## Sobre o Projeto

Este projeto em Django está Dockerizado e segue os princípios da arquitetura limpa (Clean Architecture). Ele proporciona uma estrutura sólida para o desenvolvimento de uma variedade de aplicações, desde APIs até aplicações web.

## Como Usar

Siga estes passos para executar o projeto:

1.  **Clonar o Repositório:**

        git clone git@github.com:luderibeiro/django_base.git

2.  **Configurar o Ambiente:**

-   Crie um arquivo `.env` na raiz do projeto e adicione as configurações necessárias, como chaves de API, configurações de banco de dados, etc.

4.  **Executar o Docker Compose:**

        docker-compose up --build

`obs.: a tag --build deve ser executada somente a primeira vez que o projeto for instalado ou quando houverem alterações nos arquivos de build.`

5. **Acessar a Aplicação:**
   A aplicação estará disponível em `http://localhost:8000`.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou novas funcionalidades. Basta seguir estes passos:

1. Faça um fork do repositório.
2. Crie um branch para a sua contribuição: `git checkout -b feature/nova-feature`.
3. Faça suas alterações e faça commit: `git commit -m 'Adiciona nova feature'`.
4. Faça push para o branch: `git push origin feature/nova-feature`.
5. Abra um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
