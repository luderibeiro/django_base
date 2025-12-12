from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class CartItemEntity:
    id: Optional[int]
    cart_id: int
    product_id: int
    quantity: int
    price_snapshot: Decimal
