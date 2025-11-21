# Possíveis melhorias no projeto

Este documento lista as possíveis melhorias no projeto, organizadas por arquivo e priorizadas para facilitar a implementação. As melhorias são apresentadas em formato de checklist para facilitar o acompanhamento do progresso.

## Priorização das Melhorias

-   **Prioridade Alta:** Melhorias que impactam a segurança, a estabilidade ou o desempenho do projeto.
-   **Prioridade Média:** Melhorias que aprimoram a legibilidade, a manutenibilidade ou a testabilidade do código.
-   **Prioridade Baixa:** Melhorias que adicionam funcionalidades extras ou que aprimoram a experiência do desenvolvedor.

## project/project/settings.py

**Prioridade Média**

-   [ ] **Variáveis de ambiente:** Utilizar um pacote como `python-decouple` ou `django-environ` para facilitar a gestão das variáveis de ambiente e garantir que todas as variáveis necessárias estejam definidas.
-   [ ] **Configuração de DEBUG:** Simplificar a configuração de DEBUG usando `DEBUG = bool(strtobool(os.getenv("DJANGO_DEBUG", "True")))`.
-   [ ] **ALLOWED_HOSTS:** Simplificar a definição de `ALLOWED_HOSTS` com uma list comprehension mais direta.
-   [ ] **Configuração de banco de dados:** Simplificar a configuração do banco de dados usando um único bloco de código e ajustando as configurações com base na variável `DEBUG`. Adicionar suporte para diferentes tipos de bancos de dados através de variáveis de ambiente.
-   [ ] **Logging:** Aprimorar a configuração de logging com a adição de logs estruturados usando um pacote como `structlog`.
-   [ ] **Oauth Configuration:** Adicionar mais opções de configuração, como a possibilidade de configurar o tempo de vida dos tokens de acesso e refresh tokens através de variáveis de ambiente.

## project/core/models/user.py

**Prioridade Média**

-   [ ] **Validação de campos:** Adicionar validadores para garantir que os campos `first_name` e `last_name` não excedam os limites definidos (`max_length`).
-   [ ] **Métodos de conveniência:** Adicionar métodos de conveniência para obter o nome completo do usuário, como `get_full_name()` e `get_short_name()`.

## project/core/api/v1/views/

### auth.py

**Prioridade Média**

-   [ ] **Tratamento de exceções:** Adicionar tratamento para outras exceções que podem ocorrer, como `AuthenticationError` ou `PermissionDenied`.
-   [ ] **Logging:** Adicionar logging para registrar as tentativas de login, tanto as bem-sucedidas quanto as mal-sucedidas.

### user.py

**Prioridade Média**

-   [ ] **Tratamento de exceções:** Adicionar tratamento para outras exceções que podem ocorrer, como `ObjectDoesNotExist` ou `ValidationError`.
-   [ ] **Logging:** Adicionar logging para registrar as ações realizadas nas views, como criação, listagem, recuperação e alteração de senha de usuários.
-   [ ] **Nomes de variáveis:** Simplificar o código passando `serializer.validated_data` diretamente para o caso de uso.
-   [ ] **Paginação:** Considerar o uso de `PageNumberPagination` do Django REST Framework.

## project/core/domain/

### data_access.py

**Prioridade Média**

-   [ ] **Duplicação de métodos:** Remover os métodos duplicados da interface `UserRepository` e deixar apenas os métodos específicos para usuários.
-   [ ] **Type Hints:** Usar `Optional[str]` para `search_query` em `get_all_paginated_filtered`.

### entities/user.py

**Prioridade Média**

-   [ ] **Congruência com o modelo Django:** Criar testes de integração que validem a correspondência entre a entidade de domínio e o modelo Django.
-   [ ] **Métodos de conveniência:** Adicionar métodos de conveniência para obter o nome completo do usuário, como `get_full_name()` e `get_short_name()`.

### use_cases/generic_use_cases.py

**Prioridade Média**

-   [ ] **Consistência nos Requests:** Criar um `GenericGetByIdRequest` para manter a semântica correta.
-   [ ] **Lógica de atualização:** Implementar uma lógica de merge mais sofisticada para atualizar apenas os campos modificados.
-   [ ] **Tratamento de erros:** Criar exceções customizadas para representar erros específicos do domínio, como `EntityNotFoundException`.
-   [ ] **GenericListRequest:** Adicionar os campos `offset`, `limit` e `search_query` para habilitar filtros e paginação.

### use_cases/user_use_cases.py

**Prioridade Média**

-   [ ] **CreateUserUseCase:** Adicionar a lógica para definir a senha do usuário, possivelmente delegando para o `AuthGateway`.
-   [ ] **GetUserByIdUseCase:** Usar `GenericGetByIdRequest` em vez de `GenericDeleteRequest`.
-   [ ] **Duplicação de informações:** Reutilizar a entidade `User` ou criar uma classe base para evitar duplicação nas classes de resposta.
-   [ ] **Logging:** Adicionar logging em pontos estratégicos dos casos de uso.
-   [ ] **ListUsersUseCase:** Evitar a conversão de `user` para `CreateUserResponse` dentro do `ListUsersUseCase`.
-   [ ] **Type Hints:** Usar `Optional[str]` para `search_query` em `ListUsersRequest`.

## project/core/repositories/

### auth_gateway_impl.py

**Prioridade Alta**

-   [ ] **Geração de tokens:** Usar uma biblioteca específica para geração de tokens, como `secrets` do Python ou uma biblioteca JWT.
-   [ ] **Busca da aplicação cliente:** Buscar a aplicação cliente com base em informações da requisição. A criação da aplicação cliente deve ser feita em um processo separado.
-   [ ] **Tratamento de erros:** Lançar exceções customizadas para representar erros específicos do domínio.
-   [ ] **Hardcoded Scopes:** Permitir a configuração dos scopes.

### user_repository_impl.py

**Prioridade Média**

-   [ ] **Tratamento de erros:** Lançar exceções customizadas para representar erros específicos do domínio.
-   [ ] **Criação de usuários:** A definição da senha deve ser feita em um caso de uso específico e delegada para o `AuthGateway`.
-   [ ] **Mapeamento de objetos:** Garantir que o mapeamento entre o modelo Django e a entidade de domínio seja consistente.
-   [ ] **Exclusão de superusuários:** Adicionar uma opção para incluir ou excluir superusuários na listagem.
-   [ ] **Paginação:** Usar a paginação do Django (`Paginator`) para garantir um comportamento consistente e evitar problemas de desempenho.

## project/core/tests/

### unit/test_user_use_cases.py

**Prioridade Média**

-   [ ] **Verificação de argumentos:** Usar `assert_called_with` para verificar os argumentos passados para o método `create` do repositório.
-   [ ] **Testes de erro:** Adicionar asserções para verificar se a mensagem de erro está correta.
-   [ ] **Testes de limites:** Adicionar testes de limites para os casos de uso.
-   [ ] **Fixtures:** Simplificar a criação de fixtures usando o decorator `@pytest.fixture(spec=...)`.
-   [ ] **Uso de UUIDs:** Deixar o mock gerar o UUID para maior isolamento.

### integration/test_user_api.py

**Prioridade Média**

-   [ ] **Setup:** Simplificar o setup usando fixtures do pytest.
-   [ ] **Autenticação:** Usar a biblioteca `oauth2_provider.test.utils` para criar tokens de acesso.
-   [ ] **Verificação de erros:** Adicionar asserções para verificar se a mensagem de erro está correta.
-   [ ] **Testes de limites:** Adicionar testes de limites para as APIs.
-   [ ] **DRY (Don't Repeat Yourself):** Refatorar os testes para evitar duplicação de código.
-   [ ] **Cobertura:** Adicionar testes para cobrir todos os cenários possíveis.

## Dockerfile

**Prioridade Média**

-   [ ] **Versões explícitas:** Fixar as versões de pacotes como `wkhtmltopdf`.
-   [ ] **Cache de dependências:** Dividir a instalação de dependências do sistema em várias camadas.
-   [ ] **Segurança:** Avaliar a necessidade de criar um diretório home para o usuário `appuser` e garantir que ele tenha as permissões corretas.
-   [ ] **Limpeza:** Usar ferramentas específicas, como `apt-get clean` e `pip cache purge`, para remover arquivos desnecessários.
-   [ ] **Multi-stage build:** Garantir que apenas os arquivos necessários sejam copiados do builder para a imagem final.
-   [ ] **Healthcheck:** Adicionar um healthcheck para verificar se a aplicação está saudável.

## Makefile

**Prioridade Baixa**

-   [ ] **Ativação do ambiente virtual:** Usar `source $(VENV)/bin/activate` em vez de `. $(VENV)/bin/activate`.
-   [ ] **Variáveis de ambiente:** Definir as variáveis de ambiente no início do `Makefile`.
-   [ ] **Cores:** Usar uma biblioteca como `tput` para garantir que as cores sejam exibidas corretamente em todos os terminais.
-   [ ] **Comandos Docker:** Usar variáveis para definir os nomes das imagens e dos arquivos de configuração do Docker.
-   [ ] **Comandos Git:** Adicionar uma verificação se o repositório Git foi configurado.
-   [ ] **Linters:** Usar um arquivo de configuração para personalizar o comportamento do `flake8`.
