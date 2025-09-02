import uuid

from core.domain.entities.user import User


def test_user_creation():
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id, email="test@example.com", first_name="Test", last_name="User"
    )

    assert user.id == user_id
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


def test_user_is_admin():
    admin_user = User(
        id=str(uuid.uuid4()),
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        is_staff=True,
        is_superuser=True,
    )
    regular_user = User(
        id=str(uuid.uuid4()),
        email="user@example.com",
        first_name="Regular",
        last_name="User",
    )

    assert admin_user.is_admin() is True
    assert regular_user.is_admin() is False


def test_user_default_values():
    user = User(
        id=str(uuid.uuid4()),
        email="default@example.com",
        first_name="Default",
        last_name="User",
    )

    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


def test_user_equality():
    user_id = str(uuid.uuid4())
    user1 = User(
        id=user_id, email="test@example.com", first_name="Test", last_name="User"
    )
    user2 = User(
        id=user_id, email="another@example.com", first_name="Another", last_name="User"
    )
    user3 = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        first_name="Test",
        last_name="User",
    )

    assert user1 == user2
    assert user1 != user3


def test_user_str_representation():
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id, email="test@example.com", first_name="Test", last_name="User"
    )

    assert str(user) == f"User(id={user_id}, email=test@example.com)"
