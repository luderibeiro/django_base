from abc import ABC, abstractmethod
from typing import Optional


class CartRepositoryGateway(ABC):
    @abstractmethod
    def get_by_user(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_by_session(self, session_key: str):
        raise NotImplementedError

    @abstractmethod
    def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_item(self, cart_id: int, product_id: int, quantity: int, price_snapshot):
        raise NotImplementedError

    @abstractmethod
    def remove_item(
        self, cart_id: int, product_id: int = None, cart_item_id: int = None
    ):
        raise NotImplementedError
