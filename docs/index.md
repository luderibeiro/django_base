# Bem-vindo ao Template de Projeto Django - Arquitetura Limpa

Este projeto serve como um template robusto para iniciar novas aplicações em Python (versão 3.12) com o framework Django (versão 5.0), seguindo rigorosamente os princípios da Arquitetura Limpa. Nosso objetivo é fornecer uma base sólida que promova a modularidade, a testabilidade e a escalabilidade, tornando o desenvolvimento e a manutenção futuros mais eficientes e menos propensos a erros.

## Por Que Arquitetura Limpa?

A Arquitetura Limpa foca na separação de interesses, garantindo que o código seja independente de *frameworks*, bancos de dados ou interfaces de usuário. Isso resulta em um sistema:

-   **Independente de Frameworks**: A lógica de negócio não está amarrada a nenhum *framework* específico (como Django), permitindo flexibilidade para futuras mudanças.
-   **Testável**: As regras de negócio podem ser testadas sem a necessidade de banco de dados, servidor web ou UI.
-   **Independente de UI**: A UI pode mudar facilmente sem alterar o restante do sistema.
-   **Independente de Banco de Dados**: Você pode trocar o banco de dados sem alterar as regras de negócio.
-   **Independente de Agentes Externos**: A lógica de negócio não sabe nada sobre o mundo externo.

## Início Rápido (Quick Start)

Para começar a usar este template, siga os passos detalhados em nossa seção de [Configuração do Projeto](setup/project-setup.md). Lá você encontrará instruções para configurar o ambiente localmente, tanto com quanto sem Docker.

## Estrutura da Documentação

Nossa documentação está organizada para facilitar o entendimento e a navegação:

-   **[Arquitetura](architecture/overview.md)**: Entenda a estrutura das camadas de Domínio, Aplicação, Infraestrutura e Apresentação, e como elas interagem.
-   **[Desenvolvimento](development/testing.md)**: Guias sobre como desenvolver novas funcionalidades, testes automatizados, paginação, filtragem, implementação OAuth2 e logs.
-   **[Setup](setup/project-setup.md)**: Instruções detalhadas para a configuração do ambiente de desenvolvimento e da própria documentação.
-   **[Changelog](CHANGELOG.md)**: Um registro cronológico de todas as alterações notáveis no projeto, seguindo o Versionamento Semântico.
-   **[Guia de Contribuição](CONTRIBUTING.md)**: Como você pode nos ajudar a melhorar este projeto.
-   **[Código de Conduta](CODE_OF_CONDUCT.md)**: As diretrizes para uma comunidade saudável e respeitosa.

Navegue pelas seções para explorar todos os aspectos deste projeto. Se tiver dúvidas ou sugestões, consulte o [Guia de Contribuição](CONTRIBUTING.md)!
