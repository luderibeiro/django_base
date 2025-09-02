# Guia de Contribuição

Boas-vindas ao guia de contribuição para o `django_base`!

Estamos muito felizes com o seu interesse em contribuir para tornar este projeto uma base ainda melhor para aplicações Django com Arquitetura Limpa. Sua ajuda é valiosa!

Por favor, reserve um momento para revisar este documento antes de abrir um Pull Request (PR) ou Issue. Isso nos ajuda a manter a comunidade coesa e eficiente, e a garantir um fluxo de trabalho tranquilo para todos.

## 1. Código de Conduta

Por favor, leia nosso [Código de Conduta](https://your-username.github.io/django_base/CODE_OF_CONDUCT/). Esperamos que todos os colaboradores o sigam.

## 2. Como Contribuir

### Reportando Bugs

Se você encontrar um bug, por favor, siga estas etapas:

1.  **Procure por Issues Existentes**: Verifique se o bug já foi reportado. Se sim, adicione seus comentários ou reações.
2.  **Abra uma Nova Issue**: Se não encontrou, abra uma nova issue descrevendo o bug. Inclua:
    -   Um título claro e conciso.
    -   Uma descrição detalhada do problema.
    -   Passos para reproduzir o bug.
    -   Comportamento esperado vs. comportamento real.
    -   Versão do Django, Python e outras dependências relevantes.
    -   Quaisquer mensagens de erro ou logs.

### Sugerindo Novas Funcionalidades ou Melhorias

Se você tiver uma ideia para uma nova funcionalidade ou melhoria, por favor, siga estas etapas:

1.  **Procure por Issues Existentes**: Verifique se a funcionalidade já foi discutida. Se sim, adicione seus comentários ou reações.
2.  **Abra uma Nova Issue**: Se não encontrou, abra uma nova issue descrevendo a funcionalidade. Inclua:
    -   Um título claro e conciso.
    -   Uma descrição detalhada da funcionalidade.
    -   Por que ela seria útil.
    -   Exemplos de como ela funcionaria ou seria usada.

### Contribuindo com Código

Estamos sempre abertos a contribuições de código! Para isso, siga o fluxo de trabalho abaixo:

1.  **Faça Fork do Repositório**: Clique no botão "Fork" no GitHub.
2.  **Clone o seu Fork**: `git clone https://github.com/SEU_USERNAME/django_base.git`
3.  **Crie um Branch**: Crie um novo branch para a sua contribuição. Use um nome descritivo (e.g., `feat/adiciona-autenticacao`, `fix/corrige-bug-de-login`, `docs/melhora-readme`).
    ```bash
    git checkout -b seu-branch-descritivo
    ```
4.  **Desenvolva Suas Alterações**: Implemente suas funcionalidades ou correções.
    -   **Estilo de Código**: Siga o estilo de código existente no projeto (geralmente PEP 8 para Python, com formatação por `black` e `isort`). Usaremos `ruff` para linting.
    -   **Testes**: Adicione testes unitários para o novo código e atualize os testes de integração, se necessário. Certifique-se de que todos os testes existentes continuem passando.
    -   **Documentação**: Atualize a documentação (`docs/`) relevante para suas alterações.
5.  **Faça Commit das Suas Alterações**: Escreva mensagens de commit claras e concisas, usando o **modo imperativo**.
    -   `feat: Adicionar nova funcionalidade de usuário`
    -   `fix: Corrigir erro de validação de email`
    -   `docs: Melhorar guia de contribuição`
6.  **Faça Push para o seu Fork**: `git push origin seu-branch-descritivo`
7.  **Abra um Pull Request (PR)**:
    -   Vá para a página do seu fork no GitHub e clique em "Compare & pull request" ou use o botão "New pull request".
    -   Forneça um título e descrição claros para o seu PR, explicando as mudanças e referenciando as issues relevantes.
    -   Certifique-se de que os testes automatizados (CI) passem.

## 3. Ambiente de Desenvolvimento

Para configurar seu ambiente de desenvolvimento local, por favor, consulte a seção de [Configuração do Projeto na documentação](https://your-username.github.io/django_base/setup/project-setup/).

## 4. Testes

Para informações sobre como executar os testes do projeto, consulte a seção [Como Testar na documentação](https://your-username.github.io/django_base/development/testing/).
