# placeholder - tests for models
from decimal import Decimal

import pytest
from cart.models.cart import Cart
from cart.models.cart_item import CartItem
from cart.models.product import Product
from cart.services.cart_service import CartService


@pytest.mark.django_db
def test_get_or_create_cart_requires_params():
    service = CartService()
    with pytest.raises(ValueError):
        service.get_or_create_cart(user=None, session_key=None)


@pytest.mark.django_db
def test_add_item_negative_quantity_raises():
    service = CartService()
    cart = Cart.objects.create(session_key="s1")
    product = Product.objects.create(
        name="P", price=Decimal("1.00"), stock=10, is_active=True
    )

    with pytest.raises(ValueError) as exc:
        service.add_item(cart=cart, product_id=product.id, quantity=-1)
    assert "Quantity must be positive" in str(exc.value)


@pytest.mark.django_db
def test_add_item_insufficient_stock_raises():
    service = CartService()
    cart = Cart.objects.create(session_key="s2")
    product = Product.objects.create(
        name="LowStock", price=Decimal("2.00"), stock=1, is_active=True
    )

    with pytest.raises(ValueError) as exc:
        service.add_item(cart=cart, product_id=product.id, quantity=2)
    assert "Estoque insuficiente" in str(exc.value)


@pytest.mark.django_db
def test_add_item_creates_and_updates_snapshot_and_quantity():
    service = CartService()
    cart = Cart.objects.create(session_key="s3")
    product = Product.objects.create(
        name="Snap", price=Decimal("10.00"), stock=10, is_active=True
    )

    item = service.add_item(cart=cart, product_id=product.id, quantity=2)
    assert item.quantity == 2
    assert Decimal(item.price_snapshot) == Decimal("10.00")

    # change product price and add more => snapshot must update to current price
    product.price = Decimal("12.50")
    product.save()

    item2 = service.add_item(cart=cart, product_id=product.id, quantity=3)
    assert item.id == item2.id
    assert item2.quantity == 5
    assert Decimal(item2.price_snapshot) == Decimal("12.50")


@pytest.mark.django_db
def test_add_item_product_not_found_propagates(monkeypatch):
    service = CartService()
    cart = Cart.objects.create(session_key="s4")

    import cart.services.cart_service as _svc_mod

    def _raise(pk):
        raise Product.DoesNotExist()

    monkeypatch.setattr(_svc_mod.Product.objects, "get", _raise)

    with pytest.raises(Product.DoesNotExist):
        service.add_item(cart=cart, product_id=9999, quantity=1)


@pytest.mark.django_db
def test_remove_item_partial_and_full():
    service = CartService()
    cart = Cart.objects.create(session_key="s5")
    product = Product.objects.create(
        name="ToRemove", price=Decimal("3.00"), stock=10, is_active=True
    )

    item = CartItem.objects.create(
        cart=cart, product_id=product.id, quantity=5, price_snapshot=Decimal("3.00")
    )

    service.remove_item(cart=cart, product_id=product.id, quantity=2)
    item.refresh_from_db()
    assert item.quantity == 3

    service.remove_item(cart=cart, product_id=product.id, quantity=None)
    assert not CartItem.objects.filter(pk=item.pk).exists()


@pytest.mark.django_db
def test_remove_nonexistent_item_is_noop():
    service = CartService()
    cart = Cart.objects.create(session_key="s6")
    # should not raise
    service.remove_item(cart=cart, product_id=9999, quantity=1)


@pytest.mark.django_db
def test_calculate_cart_total():
    service = CartService()
    cart = Cart.objects.create(session_key="s7")
    p1 = Product.objects.create(
        name="A", price=Decimal("4.00"), stock=10, is_active=True
    )
    p2 = Product.objects.create(
        name="B", price=Decimal("2.50"), stock=10, is_active=True
    )

    CartItem.objects.create(
        cart=cart, product_id=p1.id, quantity=2, price_snapshot=Decimal("4.00")
    )
    CartItem.objects.create(
        cart=cart, product_id=p2.id, quantity=3, price_snapshot=Decimal("2.50")
    )

    total = service.calculate_cart_total(cart)
    expected = Decimal("4.00") * 2 + Decimal("2.50") * 3
    assert total == expected


@pytest.mark.django_db
def test_cart_total_items_and_total_value_and_str():
    cart = Cart.objects.create(session_key="s_mod_1")
    p1 = Product.objects.create(
        name="M1", price=Decimal("7.00"), stock=10, is_active=True
    )
    p2 = Product.objects.create(
        name="M2", price=Decimal("1.50"), stock=10, is_active=True
    )

    CartItem.objects.create(
        cart=cart, product_id=p1.id, quantity=1, price_snapshot=Decimal("7.00")
    )
    CartItem.objects.create(
        cart=cart, product_id=p2.id, quantity=4, price_snapshot=Decimal("1.50")
    )

    assert cart.total_items() == 5
    assert cart.total_value() == Decimal("7.00") * 1 + Decimal("1.50") * 4
    assert "Cart(" in str(cart) or "session=" in str(cart)
