from decimal import Decimal

from cart.models.cart import Cart
from cart.models.cart_item import CartItem
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_id",
            "quantity",
            "price_snapshot",
            "subtotal",
            "created_at",
            "updated_at",
        ]

    def get_subtotal(self, obj: CartItem) -> Decimal:
        return obj.subtotal()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "session_key",
            "items",
            "total_items",
            "total_value",
            "created_at",
            "updated_at",
        ]

    def get_total_items(self, obj: Cart) -> int:
        return obj.total_items()

    def get_total_value(self, obj: Cart) -> Decimal:
        return obj.total_value()


class AddItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(required=False, default=1)


class RemoveItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(required=False)
