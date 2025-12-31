# 🚀 Melhorias Futuras

Este documento lista as possíveis melhorias no projeto, organizadas por componente e priorizadas para facilitar a implementação futura.

## 📊 Priorização

-   **Prioridade Alta:** Melhorias que impactam a segurança, a estabilidade ou o desempenho do projeto.
-   **Prioridade Média:** Melhorias que aprimoram a legibilidade, a manutenibilidade ou a testabilidade do código.
-   **Prioridade Baixa:** Melhorias que adicionam funcionalidades extras ou que aprimoram a experiência do desenvolvedor.

## ⚙️ Configurações (settings.py)

**Prioridade Média**

-   [ ] **Configuração de DEBUG:** Simplificar usando `DEBUG = bool(strtobool(os.getenv("DJANGO_DEBUG", "True")))`.
-   [ ] **ALLOWED_HOSTS:** Simplificar a definição com uma list comprehension mais direta.
-   [ ] **Configuração de banco de dados:** Adicionar suporte para diferentes tipos de bancos de dados através de variáveis de ambiente.
-   [ ] **OAuth Configuration:** Adicionar mais opções de configuração, como tempo de vida dos tokens através de variáveis de ambiente.

## 👤 Modelos (core/models/user.py)

**Prioridade Média**

-   [ ] **Validação de campos:** Adicionar validadores para garantir que os campos `first_name` e `last_name` não excedam os limites definidos.
-   [ ] **Métodos de conveniência:** Adicionar métodos `get_full_name()` e `get_short_name()`.

## 🌐 Views da API

### auth.py

**Prioridade Média**

-   [ ] **Tratamento de exceções:** Adicionar tratamento para outras exceções como `AuthenticationError` ou `PermissionDenied`.
-   [ ] **Logging:** Adicionar logging para registrar tentativas de login (sucesso e falha).

### user.py

**Prioridade Média**

-   [ ] **Tratamento de exceções:** Adicionar tratamento para `ObjectDoesNotExist` ou `ValidationError`.
-   [ ] **Logging:** Adicionar logging para registrar ações nas views (criação, listagem, recuperação, alteração de senha).
-   [ ] **Paginação:** Considerar o uso de `PageNumberPagination` do Django REST Framework.

## 🎯 Camada de Domínio

### data_access.py

**Prioridade Média**

-   [ ] **Duplicação de métodos:** Remover métodos duplicados da interface `UserRepository`.
-   [ ] **Type Hints:** Usar `Optional[str]` para `search_query` em `get_all_paginated_filtered`.

### entities/user.py

**Prioridade Média**

-   [ ] **Congruência com modelo Django:** Criar testes de integração que validem a correspondência entre a entidade de domínio e o modelo Django.
-   [ ] **Métodos de conveniência:** Adicionar métodos `get_full_name()` e `get_short_name()`.

### use_cases/generic_use_cases.py

**Prioridade Média**

-   [ ] **Consistência nos Requests:** Criar um `GenericGetByIdRequest` para manter a semântica correta.
-   [ ] **Lógica de atualização:** Implementar uma lógica de merge mais sofisticada para atualizar apenas os campos modificados.
-   [ ] **Tratamento de erros:** Criar exceções customizadas para representar erros específicos do domínio, como `EntityNotFoundException`.
-   [ ] **GenericListRequest:** Adicionar campos `offset`, `limit` e `search_query` para habilitar filtros e paginação.

### use_cases/user_use_cases.py

**Prioridade Média**

-   [ ] **CreateUserUseCase:** Adicionar lógica para definir a senha do usuário, possivelmente delegando para o `AuthGateway`.
-   [ ] **GetUserByIdUseCase:** Usar `GenericGetByIdRequest` em vez de `GenericDeleteRequest`.
-   [ ] **Duplicação de informações:** Reutilizar a entidade `User` ou criar uma classe base para evitar duplicação nas classes de resposta.
-   [ ] **Logging:** Adicionar logging em pontos estratégicos dos casos de uso.
-   [ ] **ListUsersUseCase:** Evitar a conversão de `user` para `CreateUserResponse` dentro do `ListUsersUseCase`.
-   [ ] **Type Hints:** Usar `Optional[str]` para `search_query` em `ListUsersRequest`.

## 🔄 Repositórios

### auth_gateway_impl.py

**Prioridade Alta**

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

## 🧪 Testes

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

## 🐳 Docker

**Prioridade Média**

-   [ ] **Versões explícitas:** Fixar as versões de pacotes como `wkhtmltopdf`.
-   [ ] **Cache de dependências:** Dividir a instalação de dependências do sistema em várias camadas.
-   [ ] **Segurança:** Avaliar a necessidade de criar um diretório home para o usuário `appuser` e garantir que ele tenha as permissões corretas.
-   [ ] **Limpeza:** Usar ferramentas específicas, como `apt-get clean` e `pip cache purge`, para remover arquivos desnecessários.
-   [ ] **Multi-stage build:** Garantir que apenas os arquivos necessários sejam copiados do builder para a imagem final.
-   [ ] **Healthcheck:** Adicionar um healthcheck para verificar se a aplicação está saudável.

## 📝 Makefile

**Prioridade Baixa**

-   [ ] **Variáveis de ambiente:** Definir as variáveis de ambiente no início do `Makefile`.
-   [ ] **Cores:** Usar uma biblioteca como `tput` para garantir que as cores sejam exibidas corretamente em todos os terminais.
-   [ ] **Comandos Docker:** Usar variáveis para definir os nomes das imagens e dos arquivos de configuração do Docker.
-   [ ] **Comandos Git:** Adicionar uma verificação se o repositório Git foi configurado.
-   [ ] **Linters:** Usar um arquivo de configuração para personalizar o comportamento do `flake8`.

## 📚 Documentação

**Prioridade Média**

-   [ ] **Exemplos práticos:** Adicionar mais exemplos de uso da API
-   [ ] **Tutoriais passo-a-passo:** Criar tutoriais para cenários comuns
-   [ ] **Diagramas:** Adicionar diagramas de arquitetura e fluxo de dados
-   [ ] **Traduções:** Considerar tradução da documentação para outros idiomas

## 🔒 Segurança

**Prioridade Alta**

-   [ ] **Rate limiting:** Implementar rate limiting para endpoints da API
-   [ ] **CORS:** Configurar CORS adequadamente para produção
-   [ ] **HTTPS:** Forçar HTTPS em produção
-   [ ] **Headers de segurança:** Adicionar headers de segurança (HSTS, CSP, etc.)
-   [ ] **Auditoria de segurança:** Implementar auditoria regular de dependências

## ⚡ Performance

**Prioridade Média**

-   [ ] **Cache:** Implementar cache para queries frequentes
-   [ ] **Otimização de queries:** Adicionar `select_related` e `prefetch_related` onde necessário
-   [ ] **Índices de banco:** Adicionar índices para campos frequentemente consultados
-   [ ] **Compressão:** Habilitar compressão de respostas HTTP
-   [ ] **CDN:** Configurar CDN para arquivos estáticos

## 🎨 Organização de Arquivos

**Prioridade Baixa**

-   [ ] **Estrutura de pastas:** Revisar e otimizar estrutura de pastas
-   [ ] **Nomenclatura:** Padronizar nomenclatura de arquivos e diretórios
-   [ ] **Separação de ambientes:** Melhorar separação de configurações por ambiente
-   [ ] **Assets:** Organizar melhor assets e arquivos estáticos

---

**Nota:** Este documento é atualizado regularmente conforme melhorias são implementadas ou novas necessidades são identificadas.

