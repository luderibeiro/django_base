from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from cart.models.cart import Cart
from cart.models.cart_item import CartItem
from cart.models.product import Product
from django.db import transaction

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser as User  # type: ignore
else:
    from django.contrib.auth import get_user_model

    User = get_user_model()


class CartService:
    """
    Serviço para operações de carrinho.

    Responsabilidades:
    - criar/obter carrinho
    - adicionar/remover itens com validações de domínio
    - calcular total do carrinho
    """

    def get_or_create_cart(
        self, *, user: Optional["User"] = None, session_key: Optional[str] = None
    ) -> Cart:
        """
        Retorna um carrinho ativo associado a `user` ou `session_key`. Cria se não existir.

        Args:
            user: usuário autenticado ou None.
            session_key: chave de sessão para anônimos.

        Raises:
            ValueError: se nem `user` nem `session_key` forem fornecidos.
        """
        if user is None and not session_key:
            raise ValueError("É necessário fornecer user ou session_key.")

        cart, _created = Cart.objects.get_or_create(
            user=user, session_key=session_key if user is None else None
        )
        return cart

    @transaction.atomic
    def add_item(self, *, cart: Cart, product_id: int, quantity: int = 1) -> CartItem:
        """
        Adiciona `quantity` do `product_id` ao `cart`.

        Regras:
        - quantity > 0 (ValueError)
        - validação de estoque via product.stock (ValueError "Estoque insuficiente")
        - grava price_snapshot com product.price atual
        - se item existir, incrementa quantidade e atualiza snapshot

        Args:
            cart: instância de Cart.
            product_id: id do produto.
            quantity: quantidade a adicionar.

        Returns:
            CartItem atualizado ou criado.

        Raises:
            ValueError: para quantidade inválida ou estoque insuficiente.
            Product.DoesNotExist: se o produto não existir.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        product: Product = Product.objects.get(pk=product_id)
        self._validate_stock(product, quantity)

        current_price: Decimal = product.price

        item, created = CartItem.objects.select_for_update().get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={"quantity": quantity, "price_snapshot": current_price},
        )

        if created:
            return item

        item.quantity += quantity
        # sempre manter snapshot representando o preço atual no momento de alteração
        item.price_snapshot = current_price
        item.save(update_fields=["quantity", "price_snapshot"])
        return item

    @transaction.atomic
    def remove_item(
        self, *, cart: Cart, product_id: int, quantity: Optional[int] = None
    ) -> None:
        """
        Remove `quantity` do item ou remove totalmente se quantity for None ou >= item.quantity.

        Args:
            cart: instância de Cart.
            product_id: id do produto a remover.
            quantity: quantidade a remover (opcional).
        """
        item = self._get_cart_item(cart, product_id)
        if item is None:
            return

        if quantity is None or quantity >= item.quantity:
            item.delete()
            return

        item.quantity -= quantity
        item.save(update_fields=["quantity"])

    def calculate_cart_total(self, cart: Cart) -> Decimal:
        """
        Calcula e retorna o total do carrinho (Decimal).

        Args:
            cart: instância de Cart.

        Returns:
            Decimal: soma de price_snapshot * quantity dos itens.
        """
        total = Decimal("0")
        for item in cart.items.all():
            total += item.subtotal()
        return total

    def _validate_stock(self, product: Product, quantity: int) -> None:
        """
        Verifica se o produto tem estoque suficiente.

        Args:
            product: instância de Product.
            quantity: quantidade desejada.

        Raises:
            ValueError: com mensagem "Estoque insuficiente" se não houver stock.
        """
        stock = getattr(product, "stock", None)
        if stock is None:
            raise ValueError("Product does not have 'stock' field.")
        if stock < quantity:
            raise ValueError("Estoque insuficiente")

    def _get_cart_item(self, cart: Cart, product_id: int) -> Optional[CartItem]:
        """
        Retorna CartItem ou None se não existir.
        """
        try:
            return CartItem.objects.select_for_update().get(
                cart=cart, product_id=product_id
            )
        except CartItem.DoesNotExist:
            return None
