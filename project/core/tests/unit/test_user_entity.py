from core.domain.entities.user import User

def test_user_creation():
    user = User(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        is_active=True,
        is_staff=False,
        is_superuser=False,
        id="123",
    )
    assert user.id == "123"
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.is_admin is False

def test_user_is_admin_property():
    admin_user = User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        is_superuser=True,
    )
    assert admin_user.is_admin is True

    regular_user = User(
        email="regular@example.com",
        first_name="Regular",
        last_name="User",
        is_superuser=False,
    )
    assert regular_user.is_admin is False
