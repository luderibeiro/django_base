from typing import Optional

from cart.models.cart import Cart
from cart.models.cart_item import CartItem
from django.db import transaction


class CartRepositoryImpl:
    """Implementação simples usando ORM direto. Pode ser substituída por um gateway mais complexo."""

    def get_by_user(self, user_id: int) -> Optional[Cart]:
        """Retorna o carrinho ativo do usuário ou None."""
        return Cart.objects.filter(user_id=user_id, status="active").first()

    def get_by_session(self, session_key: str) -> Optional[Cart]:
        """Retorna o carrinho ativo da sessão ou None."""
        return Cart.objects.filter(session_key=session_key, status="active").first()

    def create(self, **kwargs) -> Cart:
        """Cria e retorna um novo Cart com os kwargs fornecidos."""
        return Cart.objects.create(**kwargs)

    @transaction.atomic
    def add_item(
        self, cart_id: int, product_id: int, quantity: int, price_snapshot
    ) -> CartItem:
        """
        Adiciona um item ao carrinho ou incrementa a quantidade se já existir.
        Retorna sempre a instância de CartItem resultante.
        """
        cart = Cart.objects.select_for_update().get(pk=cart_id)
        item, created = CartItem.objects.select_for_update().get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={"quantity": quantity, "price_snapshot": price_snapshot},
        )
        if not created:
            item.quantity += quantity
            item.price_snapshot = price_snapshot
            item.save(update_fields=["quantity", "price_snapshot"])
            return item

        return item

    @transaction.atomic
    def remove_item(
        self, cart_id: int, product_id: int = None, cart_item_id: int = None
    ) -> None:
        """
        Remove item(s) do carrinho.
        - Se cart_item_id for fornecido, remove o item específico.
        - Senão, se product_id for fornecido, remove itens daquele produto no carrinho.
        - Caso contrário, não faz nada.
        """
        qs = CartItem.objects.filter(cart_id=cart_id)
        if cart_item_id is not None:
            qs = qs.filter(pk=cart_item_id)
            qs.delete()
            return

        if product_id is not None:
            qs = qs.filter(product_id=product_id)
            qs.delete()
            return

        # noop quando nenhum identificador é fornecido
        return
