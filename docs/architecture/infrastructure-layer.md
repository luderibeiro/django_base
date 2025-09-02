# Camada de Infraestrutura

Esta camada é responsável pela implementação das interfaces definidas na camada de Domínio. Ela lida com os detalhes técnicos, como persistência de dados (Django ORM) ou comunicação com serviços externos.

-   `project/core/repositories/user_repository_impl.py`: Criada a implementação `DjangoUserRepository` que herda de `UserRepository` e utiliza o ORM do Django para interagir com o modelo `User` do Django. Inclui a conversão entre a entidade de domínio `User` e o modelo Django `User`.
-   `project/core/repositories/auth_gateway_impl.py`: Criada a implementação `DjangoAuthGateway` que herda de `AuthGateway` e utiliza o sistema de autenticação do Django para `check_password` e um placeholder para `create_tokens` e a implementação para `set_password`.

