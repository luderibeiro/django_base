from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from core.models import Product  # pragma: no cover


class Cart(models.Model):
    """
    Carrinho persistido no banco.

    Atributos:
        user: Usuário dono (opcional).
        session_key: Chave de sessão para anônimos.
        status: Estado do carrinho (ex: 'active').
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
    )

    session_key = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    status = models.CharField(max_length=32, default="active", db_index=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["session_key"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        owner = self.user if self.user_id else f"session={self.session_key}"
        return f"Cart(id={self.pk}, owner={owner})"

    def total_items(self) -> int:
        """
        Retorna soma das quantidades dos itens do carrinho.
        """
        return int(self.items.aggregate(total=models.Sum("quantity"))["total"] or 0)

    def total_value(self) -> Decimal:
        """
        Retorna valor total do carrinho como Decimal.
        """
        from django.db.models import F, Sum

        result = self.items.aggregate(total=Sum(F("price_snapshot") * F("quantity")))[
            "total"
        ]
        return Decimal(result or 0)
