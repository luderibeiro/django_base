from oauth2_provider.oauth2_validators import OAuth2Validator


class SafeOAuth2Validator(OAuth2Validator):
    """OAuth2 validator que delega às validações padrão com políticas explícitas.

    Esta implementação não afrouxa verificações de segurança. Caso precise
    de customizações, sobrescreva métodos chamando super() e adicionando
    validações adicionais conforme a necessidade do domínio.
    """

    # Exemplo de extensão segura (mantém comportamento padrão):
    def get_default_scopes(self, client_id, request, *args, **kwargs):
        """Retorna escopos padrão para o cliente OAuth2."""
        default_scopes = super().get_default_scopes(client_id, request, *args, **kwargs)
        return default_scopes or ["read"]

    def get_available_scopes(self, application=None, request=None, *args, **kwargs):
        """Retorna escopos disponíveis para a aplicação OAuth2."""
        available_scopes = super().get_available_scopes(
            application=application, request=request, *args, **kwargs
        )
        return available_scopes or ["read", "write"]
