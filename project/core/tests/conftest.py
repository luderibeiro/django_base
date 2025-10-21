# project/core/tests/conftest.py
import pytest
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application

@pytest.fixture(autouse=True)
def ensure_oauth_application(db):
    """
    Garante que exista uma Application OAuth2 para os testes de integração
    (client_id/test-client-id usado nos testes).
    """
    User = get_user_model()
    # usuário de sistema/owner da aplicação de teste — ajuste email se seu teste exigir outro
    user, _ = User.objects.get_or_create(
        email="admin@example.com",
        defaults={
            "is_superuser": True, 
            "is_staff": True, 
            "first_name": "Admin",
            "last_name": "User"
        },
    )

    # Limpar aplicações existentes para evitar conflitos
    Application.objects.filter(client_id="test-client-id").delete()
    
    Application.objects.create(
        name="Test App",
        client_id="test-client-id",
        client_secret="test-client-secret",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
        user=user,
    )
