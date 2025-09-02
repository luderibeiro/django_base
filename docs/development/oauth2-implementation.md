# Implementação Completa de OAuth2

Esta seção detalha a implementação completa do protocolo OAuth2 para autenticação e autorização, utilizando a biblioteca `django-oauth-toolkit`.

## 1. Contexto e Justificativa

Atualmente, a autenticação básica de login retorna tokens simplificados. Para um projeto-base robusto, é essencial ter um sistema de autenticação e autorização baseado em padrões da indústria. O OAuth2, com o `django-oauth-toolkit`, oferece uma solução completa para gerenciamento de tokens de acesso e refresh, permitindo uma integração segura com clientes externos (frontends, aplicativos móveis, outras APIs).

## 2. Abordagem da Implementação

### a. Configuração do `django-oauth-toolkit`

O `django-oauth-toolkit` já estava configurado no projeto. Os seguintes pontos confirmam isso:

-   **`INSTALLED_APPS`**: `oauth2_provider` já está incluído em `project/project/settings.py`.
-   **URLs**: As URLs do `oauth2_provider` já estão configuradas em `project/project/urls.py` com `path("o/", include("oauth2_provider.urls", namespace="oauth2_provider"))`.

### b. `AuthGateway` (`project/core/domain/gateways.py`)

A interface `AuthGateway` já define o método `create_tokens` e não foi alterada, pois ela já abstrai a necessidade de um gateway de autenticação.

### c. `DjangoAuthGateway` (`project/core/repositories/auth_gateway_impl.py`)

A implementação concreta do `create_tokens` no `DjangoAuthGateway` foi modificada para utilizar a API do `django-oauth-toolkit` para gerar tokens OAuth2 padrão (access token e refresh token). Também foi adicionada uma lógica para criar uma `Application` padrão (`Default Application`) se ela não existir, o que é útil para ambientes de desenvolvimento e teste.

```python
import os
from typing import Tuple

from core.domain.gateways import AuthGateway
from django.contrib.auth import authenticate, get_user_model
from oauth2_provider.models import AccessToken, RefreshToken, Application

User = get_user_model()

class DjangoAuthGateway(AuthGateway):
    # ... (check_password e set_password inalterados)

    def create_tokens(self, user_id: str) -> Tuple[str, str]:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError("User not found")

        try:
            application = Application.objects.get(name="Default Application")
        except Application.DoesNotExist:
            application = Application.objects.create(name="Default Application", client_type="public", authorization_grant_type="password")
        
        AccessToken.objects.filter(user=user, application=application).delete()
        RefreshToken.objects.filter(user=user, application=application).delete()

        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            token="access_token_" + str(user_id) + "_" + os.urandom(30).hex(),
            scope="read write",
            expires=AccessToken.get_expiration_delta(),
        )

        refresh_token = RefreshToken.objects.create(
            user=user,
            application=application,
            token="refresh_token_" + str(user_id) + "_" + os.urandom(30).hex(),
            access_token=access_token,
        )

        return access_token.token, refresh_token.token
```

### d. Impacto em Casos de Uso e Views

Não houve impacto direto no `LoginUserUseCase` nem na `LoginAPIView`. Eles continuam a interagir com a interface `AuthGateway` e seus DTOs, recebendo os tokens OAuth2 gerados pela camada de infraestrutura sem a necessidade de alterações em sua lógica interna. Isso valida a eficácia do desacoplamento da Arquitetura Limpa.

## 3. Passos da Implementação (Concluídos)

1.  **Configuração de `django-oauth-toolkit` verificada**: Confirmado que `oauth2_provider` está em `INSTALLED_APPS` e as URLs estão configuradas.
2.  **`create_tokens` implementado**: O método `create_tokens` em `project/core/repositories/auth_gateway_impl.py` foi atualizado para gerar tokens OAuth2 reais.
3.  **Verificação de Impacto**: Confirmado que `LoginUserUseCase` e `LoginAPIView` não precisaram de alterações diretas.
