# Configuração de URLs

Os padrões de URL foram atualizados para refletir a nova estrutura da API.

-   `project/core/api/urls/base_urls.py`: Simplificado para apenas incluir o `v1_urls.py`, removendo as rotas diretas de usuário.
-   `project/core/api/urls/v1_urls.py`: Este arquivo agora centraliza todas as rotas da API versão 1, incluindo:
    -   `path("users/", user.UserCreateAPIView.as_view(), name="create-user")`
    -   `path("users/list/", user.UserListAPIView.as_view(), name="user-list")`
    -   `path("users/alter_password/<uuid:pk>/", user.UserAlterPasswordAPIView.as_view(), name="user-alter-password")`
    -   `path("users/<uuid:pk>/", user.UserRetrieveAPIView.as_view(), name="retrieve-user")`
    -   `path("login/", auth.LoginAPIView.as_view(), name="login")`
