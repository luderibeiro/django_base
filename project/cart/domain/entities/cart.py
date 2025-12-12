from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CartEntity:
    id: Optional[int]
    user_id: Optional[int]
    session_key: Optional[str]
    status: str
    items: List[dict]
