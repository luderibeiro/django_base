# Diário de Bordo do TCC (Intervenção A) - Projeto Django Base

**Projeto:** django_base (Intervenção A - Carrinho de Compras)
**Funcionalidade:** Módulo de Carrinho de Compras (`cart`)
**Período de Execução:** Novembro/Dezembro 2025

---

### Entrada de Diário: 24/11/2025 a 26/11/2025 - Definição de Arquitetura e Configuração Inicial

| **Item**                       | **Detalhe da Execução**                                                |
| :----------------------------- | :--------------------------------------------------------------------- |
| **Pesquisador**                | Lude Ribeiro                                                           |
| **Requisito(s) Focados**       | Arquitetura do Módulo (Modular Monolith), Infraestrutura Django (Apps) |
| **Ferramenta de IA Utilizada** | ChatGPT 4.0 (Interface Web)                                            |
| **Tempo Gasto na Tarefa**      | ~3 horas                                                               |

#### 1.1. Objetivo da Sessão

**Descrição:** Obter da IA a estrutura de pastas correta para um novo módulo isolado (`cart`) dentro do padrão "Modular Monolith", gerar os scripts de automação (`bash`) para criação dos arquivos e configurar o Django (`INSTALLED_APPS`) para reconhecer o novo módulo.

#### 1.2. Prompts e Interações com a IA

**Prompt de Entrada:**

```text
Atue como um Arquiteto de Software Sênior especialista em Python e Django.
Estou trabalhando no projeto `django_base` (Monolito Modular + Clean Architecture).
Contexto Arquitetural:
- Domínios separados em módulos raiz.
- Estrutura interna: `domain/`, `services/`, `api/`, `tests/`.

Sua Missão:
Preciso criar um NOVO módulo isolado chamado `cart` para gerenciar o Carrinho de Compras.
Requisitos Funcionais:
1. Persistência: O carrinho deve ser salvo no banco.
2. Dono: Suportar usuários autenticados e anônimos.
3. Relacionamento: `CartItem` deve ter FK para `Product` (do módulo `core`).

Entregáveis:
A) Script Bash para criar a árvore de diretórios.
B) Configuração (`apps.py`) e string para `INSTALLED_APPS`.
C) Modelagem de Domínio (`models.py`).
D) Service Skeleton.
```

**Resposta/Sugestão de Código da IA (Trecho Relevante):**

```bash
#!/usr/bin/env bash
# A IA assumiu que a raiz do projeto era a raiz do git
MODULE_DIR="cart"
mkdir -p ${MODULE_DIR}/{domain,services,api,tests}
# ... (script gerado criava pastas na raiz errada, fora de 'project/')
```

#### 1.3. Análise da Sugestão da IA e Decisão do Pesquisador

| **Decisão**               | **Descrição e Justificativa (Conexão com RNFs)**                                                                                                                                                                                                                                                            |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Rejeitado (Parcial)**   | O script bash gerado pela IA estava sintaticamente correto, mas **posicionalmente errado**. A IA assumiu que o comando seria rodado na raiz do repositório, ignorando que o projeto Django real vivia dentro de uma subpasta `project/`. Isso violaria a integridade da arquitetura se executado cegamente. |
| **Modificado**            | O pesquisador interveio manualmente, movendo a execução do script para dentro da pasta `project/` para garantir que o módulo `cart` fosse criado como "irmão" do `core`.                                                                                                                                    |
| **Acatado Integralmente** | A sugestão de configuração do `apps.py` (`CartConfig`) e a string de `INSTALLED_APPS` ("cart.apps.CartConfig") estavam corretas e foram utilizadas.                                                                                                                                                         |

#### 1.4. Observações Críticas (Incidente de Contexto)

-   **Análise de Falha de Contexto:** Durante esta sessão, ocorreu um erro de infraestrutura (Docker/IPv6). A sessão de debugging consumiu dezenas de páginas de contexto. Ao tentar retornar ao código Python após resolver o Docker, a IA "esqueceu" as definições de Clean Architecture estabelecidas no início, exigindo reinjeção manual de contexto.

---

### Entrada de Diário: 26/11/2025 - Implementação da API e Migração de Ferramenta

| **Item**                       | **Detalhe da Execução**                                     |
| :----------------------------- | :---------------------------------------------------------- |
| **Pesquisador**                | Lude Ribeiro                                                |
| **Requisito(s) Focados**       | HU-A1 (Adicionar Item), Integração API-Service              |
| **Ferramenta de IA Utilizada** | ChatGPT 4.0 (Web) -> **Migração para GitHub Copilot Agent** |
| **Tempo Gasto na Tarefa**      | ~45 minutos                                                 |

#### 2.1. Objetivo da Sessão

**Descrição:** Implementar as Views (DRF) e Serializers para o endpoint de adição de itens, conectando a API ao Serviço de Domínio.

#### 2.2. Prompts e Interações com a IA

**Prompt de Entrada (ChatGPT):**

```text
Agora vamos criar a API.
1) Crie `cart/api/serializers.py`.
2) Crie `cart/api/views.py` usando o `CartService`.
3) Registre no router.
```

**Resposta/Sugestão de Código da IA (O Erro):**
A IA sugeriu um código que gerava `400 Bad Request` no endpoint `add_item`. Ao ser questionada sobre o erro, entrou em contradição cíclica:

> _"O endpoint está correto."_ -> _"Ah, desculpe, o serializer está errado."_ -> _"Sugiro mudar para GenericViewSet."_ (Mudança desnecessária).

#### 2.3. Análise da Sugestão da IA e Decisão do Pesquisador

| **Decisão**              | **Descrição e Justificativa**                                                                                                                                                                                |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Rejeitado**            | As sugestões de correção do ChatGPT tornaram-se contraditórias e alucinatórias (sugerindo imports circulares e arquivos que não existiam).                                                                   |
| **Decisão Metodológica** | **Interrupção do uso do ChatGPT Web.** Diagnóstico: A ferramenta perdeu a capacidade de rastrear o estado de 3 arquivos interdependentes (`models`, `views`, `serializers`) sem acesso direto ao filesystem. |
| **Ação (Pivô)**          | Migração imediata para o **GitHub Copilot Agent** no VS Code, utilizando o comando `@workspace` para indexar o projeto real.                                                                                 |

#### 2.4. Conclusão da Sessão

A falha confirmou a hipótese de que LLMs baseados em chat sem acesso ao contexto local são insuficientes para refatoração de múltiplos arquivos simultâneos.

---

### Entrada de Diário: - Implementação de Regras de Negócio (CartService)

| **Item**                       | **Detalhe da Execução**                                 |
| :----------------------------- | :------------------------------------------------------ |
| **Pesquisador**                | Lude Ribeiro                                            |
| **Requisito(s) Focados**       | RNF-A2 (Complexidade), Regra de Negócio (Estoque/Preço) |
| **Ferramenta de IA Utilizada** | GitHub Copilot Agent (`@workspace`)                     |
| **Tempo Gasto na Tarefa**      | ~40 minutos                                             |

#### 3.1. Objetivo da Sessão

**Descrição:** Implementar a lógica robusta de `add_item` no `CartService`, garantindo validação de estoque e integridade de dados (snapshot de preço), e refatorar para reduzir complexidade.

#### 3.2. Prompts e Interações com a IA

**Prompt de Entrada (Copilot):**

```text
@workspace Agora vamos focar na robustez da Lógica de Negócios no `CartService`.
Analise o método `add_item`. Preciso que você implemente:
1. Validação de Estoque: verifique se `product.stock` >= quantidade. Lance ValueError.
2. Snapshot de Preço: Garanta que o `price_snapshot` use o preço atual.
3. Atomicidade.
```

**Resposta/Sugestão de Código da IA (Trecho Relevante):**

```python
@transaction.atomic
def add_item(self, *, cart: Cart, product_id: int, quantity: int = 1) -> CartItem:
    product = Product.objects.get(pk=product_id)

    # A IA extraiu a validação para um método privado (reduzindo complexidade)
    self._validate_stock(product, quantity)

    current_price = product.price
    # Uso correto de select_for_update para evitar Race Condition
    item, created = CartItem.objects.select_for_update().get_or_create(
        cart=cart, product_id=product_id,
        defaults={"quantity": quantity, "price_snapshot": current_price},
    )
    # ...
    return item
```

#### 3.3. Análise da Sugestão da IA e Decisão do Pesquisador

| **Decisão**               | **Descrição e Justificativa**                                                                                                                                                                                                                                                                 |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Acatado Integralmente** | A sugestão do Copilot foi tecnicamente perfeita. Ele implementou a atomicidade de transação (`@transaction.atomic`), o _row locking_ (`select_for_update`) e a extração de método auxiliar (`_validate_stock`) sem alucinações, pois tinha acesso ao código real dos Models via `@workspace`. |

---

### Entrada de Diário: [Inserir Data] - Geração de Testes e Correção de Configuração

| **Item**                       | **Detalhe da Execução**          |
| :----------------------------- | :------------------------------- |
| **Pesquisador**                | Lude Ribeiro                     |
| **Requisito(s) Focados**       | RNF-A1 (Testabilidade/Cobertura) |
| **Ferramenta de IA Utilizada** | GitHub Copilot Agent             |
| **Tempo Gasto na Tarefa**      | ~50 minutos                      |

#### 4.1. Objetivo da Sessão

**Descrição:** Gerar uma suíte de testes de integração para o módulo `cart` e garantir que a cobertura de testes atinja a baseline (>90%).

#### 4.2. Prompts e Interações com a IA

**Prompt de Entrada:**

```text
@workspace Gere testes de integração para `cart/tests/integration/test_cart_endpoints.py` cobrindo:
1. Fluxo Anônimo.
2. Erro de Quantidade Negativa (400).
3. Produto Inexistente (404).
```

**Incidente (Resposta do Terminal ao rodar testes):**

```text
RuntimeError: Model class cart.models.cart.Cart doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
```

**Prompt de Correção (Enviado ao Copilot):**

```text
@workspace Recebi este erro ao rodar os testes. Analise o `settings.py` e `settings_test.py` e me diga o que falta.
```

#### 4.3. Análise da Sugestão da IA e Decisão do Pesquisador

| **Decisão**               | **Descrição e Justificativa (Conexão com RNFs)**                                                                                                                                                                            |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Acatado Integralmente** | O Copilot identificou corretamente que, embora o app `cart` estivesse no `settings.py`, ele estava ausente do `settings_test.py` (usado pelo Pytest). A IA gerou o patch para corrigir o arquivo de configuração de testes. |

#### 4.4. Observações Críticas e Rastreamento Sonar

-   **Problema de Cobertura:** Inicialmente, o relatório de _coverage_ ignorou o módulo `cart` (0%).
-   **Correção:** Foi necessário ajustar manualmente o comando do `Makefile` para incluir `--cov=cart`.
-   **Resultado Final:** Após a correção e adição de testes unitários para o Domínio, a cobertura do módulo `cart` atingiu níveis excelentes:
    -   **CartService:** 98% de Cobertura.
    -   **CartViewSet:** 92% de Cobertura.
    -   **Total do Módulo:** 92%.
-   **Conclusão:** A meta de manter a baseline de qualidade (>90%) foi atingida com sucesso.
