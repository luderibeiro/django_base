from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from cart.models.product import Product
from django.db import models
from django.utils import timezone


class CartItem(models.Model):
    """
    Item do carrinho com snapshot de preço.
    """

    cart = models.ForeignKey(
        "cart.Cart",
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(default=1)
    price_snapshot = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        unique_together = ("cart", "product")
        indexes = [models.Index(fields=["cart"]), models.Index(fields=["product"])]

    def __str__(self) -> str:
        return f"CartItem(id={self.pk}, cart={self.cart_id}, product={self.product_id}, qty={self.quantity})"

    def subtotal(self) -> Decimal:
        return Decimal(self.price_snapshot) * self.quantity
