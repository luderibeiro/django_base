# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o **Django Base**! Este projeto foi criado para ser um **template comunitário** e suas contribuições são muito bem-vindas.

## 🎯 Como Contribuir

### 1. 🍴 Fork e Clone

```bash
# Fork o repositório no GitHub
# Depois clone seu fork
git clone https://github.com/seu-usuario/django_base.git
cd django_base

# Adicione o repositório original como upstream
git remote add upstream https://github.com/luderibeiro/django_base.git
```

### 2. 🔧 Configure o Ambiente

```bash
# Setup completo do ambiente
make full-setup

# Ou manualmente:
make install
make migrate
make test
```

### 3. 🌟 Crie sua Branch

```bash
# Para novas funcionalidades
git checkout -b feature/nome-da-funcionalidade

# Para correções de bugs
git checkout -b fix/nome-do-bug

# Para melhorias na documentação
git checkout -b docs/melhoria-documentacao
```

### 4. ✅ Faça suas Alterações

- Siga os padrões de código existentes
- Adicione testes para novas funcionalidades
- Atualize a documentação quando necessário
- Execute os testes antes de commitar

```bash
# Verificar qualidade do código
make analyze

# Executar todos os testes
make test-coverage
```

### 5. 📝 Commit suas Mudanças

Use mensagens de commit descritivas seguindo o padrão:

```bash
# Exemplos de boas mensagens
git commit -m "✨ feat: adiciona autenticação OAuth2"
git commit -m "🐛 fix: corrige erro na paginação da API"
git commit -m "📚 docs: atualiza guia de instalação"
git commit -m "🧪 test: adiciona testes para UserRepository"
```

#### Prefixos de Commit

- `✨ feat:` - Nova funcionalidade
- `🐛 fix:` - Correção de bug
- `📚 docs:` - Documentação
- `🎨 style:` - Formatação, sem mudança de lógica
- `♻️ refactor:` - Refatoração de código
- `🧪 test:` - Adição ou correção de testes
- `🔧 chore:` - Tarefas de manutenção

### 6. 🚀 Envie seu Pull Request

```bash
# Push para seu fork
git push origin nome-da-sua-branch

# Abra um Pull Request no GitHub
```

## 📋 Diretrizes de Desenvolvimento

### Padrões de Código

- **Python**: Siga PEP 8, use Black para formatação
- **Arquitetura Limpa**: Mantenha a separação de responsabilidades
- **Testes**: Cobertura mínima de 80% para novas funcionalidades
- **Documentação**: Docstrings obrigatórias para funções públicas

### Estrutura de Testes

```python
# Exemplo de teste bem estruturado
def test_user_creation_with_valid_data():
    """
    Testa a criação de usuário com dados válidos.

    Given: Dados válidos de usuário
    When: Criar um novo usuário
    Then: Usuário deve ser criado com sucesso
    """
    # Arrange
    email = "test@example.com"
    name = "Test User"

    # Act
    user = User(email=email, name=name)

    # Assert
    assert user.email == email
    assert user.name == name
```

### Documentação

- Use Markdown para documentação
- Inclua exemplos práticos
- Mantenha a documentação atualizada
- Adicione diagramas quando necessário

## 🎯 Tipos de Contribuição

### 🔥 Funcionalidades Prioritárias

- **Templates Especializados**: E-commerce, Blog, API, etc.
- **Integrações**: Celery, Elasticsearch, S3, etc.
- **Autenticação**: Social auth, 2FA, etc.
- **Monitoramento**: Sentry, Prometheus, etc.

### 📚 Documentação

- Tradução para outros idiomas
- Tutoriais passo-a-passo
- Exemplos de uso real
- Vídeos explicativos

### 🧪 Testes

- Testes de integração
- Testes de performance
- Testes de segurança
- Testes end-to-end

### 🐛 Bugs e Melhorias

- Correção de bugs reportados
- Otimizações de performance
- Melhorias na UX/DX
- Atualizações de dependências

## 🚀 Criando Forks Especializados

Encorajamos a criação de forks especializados! Aqui estão algumas ideias:

### 🛒 Django E-commerce Base
```bash
git clone https://github.com/luderibeiro/django_base.git django-ecommerce-base
cd django-ecommerce-base

# Adicione funcionalidades específicas:
# - Carrinho de compras
# - Sistema de pagamento
# - Gestão de produtos
# - Cupons de desconto
```

### 🎓 Django Education Base
```bash
# Funcionalidades educacionais:
# - Sistema de cursos
# - Avaliações e notas
# - Fóruns de discussão
# - Certificados
```

### 🏥 Django Healthcare Base
```bash
# Funcionalidades de saúde:
# - Prontuários eletrônicos
# - Agendamento de consultas
# - Prescrições médicas
# - Conformidade LGPD/HIPAA
```

## 📊 Processo de Review

### Critérios de Aprovação

- ✅ Testes passando
- ✅ Cobertura de testes adequada
- ✅ Código seguindo padrões
- ✅ Documentação atualizada
- ✅ Sem conflitos de merge

### Timeline

- **Review inicial**: 2-3 dias úteis
- **Feedback**: Resposta em 24-48h
- **Merge**: Após aprovação de 2 maintainers

## 🏆 Reconhecimento

### Contributors

Todos os contribuidores são reconhecidos:

- **README.md**: Lista de contributors
- **CHANGELOG.md**: Créditos por release
- **Documentação**: Página de agradecimentos

### Badges

Contribuidores ativos podem receber badges especiais:

- 🥇 **Core Contributor**: 10+ PRs aceitos
- 📚 **Documentation Hero**: Melhorias significativas na docs
- 🧪 **Testing Champion**: Contribuições em testes
- 🎨 **UX Improver**: Melhorias na experiência do usuário

## 🆘 Precisa de Ajuda?

### Canais de Comunicação

- **Issues**: Para bugs e feature requests
- **Discussions**: Para perguntas e ideias
- **Discord**: Chat em tempo real (em breve)

### Mentoria

Novos contribuidores podem solicitar mentoria:

1. Comente na issue que deseja trabalhar
2. Marque `@luderibeiro` para orientação
3. Participe das sessões de pair programming

## 📜 Código de Conduta

Este projeto segue o [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, você concorda em manter um ambiente respeitoso e inclusivo.

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).

---

**🎉 Obrigado por contribuir!** Juntos estamos construindo o melhor template Django da comunidade.

### Links Úteis

- 📖 [Documentação Completa](https://luderibeiro.github.io/django_base/)
- 🐛 [Reportar Bug](https://github.com/luderibeiro/django_base/issues/new?template=bug_report.md)
- 💡 [Sugerir Funcionalidade](https://github.com/luderibeiro/django_base/issues/new?template=feature_request.md)
- 💬 [Discussões](https://github.com/luderibeiro/django_base/discussions)
