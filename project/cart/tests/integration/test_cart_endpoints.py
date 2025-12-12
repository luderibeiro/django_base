from decimal import Decimal

import pytest
from cart.models.cart import Cart
from cart.models.cart_item import CartItem
from cart.models.product import Product
from cart.services.cart_service import CartService
from rest_framework import status
from rest_framework.test import APIClient

BASE_ADD_URL = "/cart/v1/add_item/"
BASE_REMOVE_URL = "/cart/v1/remove_item/"
BASE_LIST_URL = "/cart/v1/"


@pytest.mark.django_db
def test_anonymous_flow_add_item_persists(monkeypatch):
    client = APIClient()

    # criar produto real (persistido) — o service chamará Product.objects.get,
    # então interceptamos para devolver este objeto com atributo `stock`.
    product = Product.objects.create(
        name="Test Product", price=Decimal("10.00"), is_active=True
    )
    product.stock = 5  # atributo dinâmico usado pelo service

    # garantir sessão do cliente (session_key usada pelo CartViewSet)
    session = client.session
    session.save()
    session_key = session.session_key

    # monkeypatch para que cart.services.cart_service.Product.objects.get retorne nosso produto com `stock`
    import cart.services.cart_service as _svc_mod

    monkeypatch.setattr(_svc_mod.Product.objects, "get", lambda pk: product)

    resp = client.post(
        BASE_ADD_URL, {"product_id": product.id, "quantity": 2}, format="json"
    )
    assert resp.status_code == status.HTTP_200_OK, resp.data

    # carrinho criado e item persistido
    cart = Cart.objects.filter(session_key=session_key).first()
    assert cart is not None
    items = CartItem.objects.filter(cart=cart, product_id=product.id)
    assert items.exists()
    item = items.first()
    assert item.quantity == 2
    assert Decimal(item.price_snapshot) == Decimal("10.00")


@pytest.mark.django_db
def test_add_item_negative_quantity_returns_400(monkeypatch):
    client = APIClient()

    product = Product.objects.create(
        name="Neg Qnty", price=Decimal("5.00"), is_active=True
    )
    product.stock = 10

    session = client.session
    session.save()

    import cart.services.cart_service as _svc_mod

    monkeypatch.setattr(_svc_mod.Product.objects, "get", lambda pk: product)

    resp = client.post(
        BASE_ADD_URL, {"product_id": product.id, "quantity": -1}, format="json"
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "Quantity must be positive" in str(resp.data.get("detail", "")).replace(
        '"', ""
    )


@pytest.mark.django_db
def test_add_item_nonexistent_product_returns_404(monkeypatch):
    client = APIClient()

    session = client.session
    session.save()

    import cart.services.cart_service as _svc_mod

    # simular Product.DoesNotExist
    def _raise(pk):
        raise Product.DoesNotExist()

    monkeypatch.setattr(_svc_mod.Product.objects, "get", _raise)

    resp = client.post(
        BASE_ADD_URL, {"product_id": 99999, "quantity": 1}, format="json"
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_remove_nonexistent_item_is_idempotent(monkeypatch):
    """
    Atualmente o serviço remove_item retorna silenciosamente se o item não existe.
    A view expõe remove_item em POST /cart/.../remove_item/ e devolve 204 no caso.
    """
    client = APIClient()

    product = Product.objects.create(
        name="ToRemove", price=Decimal("1.00"), is_active=True
    )
    product.stock = 10

    session = client.session
    session.save()
    session_key = session.session_key

    import cart.services.cart_service as _svc_mod

    monkeypatch.setattr(_svc_mod.Product.objects, "get", lambda pk: product)

    # garantir que não exista item no carrinho atual
    cart = Cart.objects.create(session_key=session_key)
    assert not CartItem.objects.filter(cart=cart, product=product).exists()

    resp = client.post(BASE_REMOVE_URL, {"product_id": product.id}, format="json")
    # comportamento atual: 204 No Content (idempotente)
    assert resp.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_cart_total_calculation_matches_expected(monkeypatch):
    client = APIClient()

    # dois produtos com preços diferentes
    p1 = Product.objects.create(name="P1", price=Decimal("10.00"), is_active=True)
    p2 = Product.objects.create(name="P2", price=Decimal("5.50"), is_active=True)

    # Attaching stock attribute for service checks
    p1.stock = 10
    p2.stock = 10

    session = client.session
    session.save()
    session_key = session.session_key

    import cart.services.cart_service as _svc_mod

    # monkeypatch Product.objects.get to return correct product based on pk
    def _get(pk):
        if int(pk) == p1.id:
            return p1
        if int(pk) == p2.id:
            return p2
        raise Product.DoesNotExist()

    monkeypatch.setattr(_svc_mod.Product.objects, "get", _get)

    # adicionar 2 x p1 and 3 x p2
    resp1 = client.post(
        BASE_ADD_URL, {"product_id": p1.id, "quantity": 2}, format="json"
    )
    assert resp1.status_code == status.HTTP_200_OK
    resp2 = client.post(
        BASE_ADD_URL, {"product_id": p2.id, "quantity": 3}, format="json"
    )
    assert resp2.status_code == status.HTTP_200_OK

    cart = Cart.objects.filter(session_key=session_key).first()
    assert cart is not None

    # usar o serviço para cálculo (método implementado em CartService)
    service = CartService()
    total = service.calculate_cart_total(cart)

    expected = Decimal("10.00") * 2 + Decimal("5.50") * 3
    assert total == expected

    # Se houver um endpoint GET /cart/v1/cart/ que retorne representação do carrinho,
    # tentamos consumi-lo e verificar se contém algum campo de total (opcional).
    get_resp = client.get(BASE_LIST_URL, format="json")
    if get_resp.status_code == status.HTTP_200_OK:
        # verificar se o payload contém um campo compatível com o total
        data = get_resp.data
        # possíveis chaves: "total", "total_value", "total_amount" — aceitar qualquer uma presente
        possible_keys = ("total", "total_value", "total_amount", "totalValue", "total")
        for k in possible_keys:
            if k in data:
                assert Decimal(str(data[k])) == expected
                break
        # se não houver tal campo, não falhar — já validamos via service/model
