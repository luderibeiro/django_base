from oauth2_provider.oauth2_validators import OAuth2Validator


class GammaBudgetOAuth2Validator(OAuth2Validator):
    def validate_user(self, user):
        return True

    def validate_bearer_token(self, token, scopes, request):
        return True

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return ["read", "write", "delete"]

    def get_available_scopes(self):
        return ["read", "write", "delete", "trust"]
