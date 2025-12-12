from typing import Optional

from cart.models.cart import Cart
from cart.models.product import Product
from cart.services.cart_service import CartService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import (
    AddItemSerializer,
    CartItemSerializer,
    CartSerializer,
    RemoveItemSerializer,
)


class CartViewSet(viewsets.GenericViewSet):
    """
    API do Carrinho:
    - list: GET /cart/v1/
    - add_item: POST /cart/v1/add_item/
    - remove_item: POST /cart/v1/remove_item/
    """

    permission_classes = [AllowAny]
    service = CartService()
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = (
        None  # desativa paginação para esse recurso (retorna o objeto do carrinho)
    )

    def _ensure_session_key(self, request: Request) -> str:
        """
        Garante e retorna session_key da requisição.
        """
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        return session_key

    def _get_cart_from_request(self, request: Request) -> Cart:
        """
        Obtém ou cria um carrinho para o request (usuário autenticado ou sessão).
        """
        user = request.user if request.user.is_authenticated else None
        session_key = self._ensure_session_key(request)
        return self.service.get_or_create_cart(user=user, session_key=session_key)

    def list(self, request: Request) -> Response:
        """
         Retorna o carrinho atual (instância única) com itens e totais sem paginação.
        GET /cart/v1/
        """
        cart = self._get_cart_from_request(request)
        serializer = self.get_serializer(instance=cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], serializer_class=AddItemSerializer)
    def add_item(self, request: Request) -> Response:
        """
        Adiciona item ao carrinho. Usa AddItemSerializer para documentação.
        """
        cart = self._get_cart_from_request(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            item = self.service.add_item(
                cart=cart, product_id=product_id, quantity=quantity
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            raise NotFound("Produto não encontrado.")

        return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], serializer_class=RemoveItemSerializer)
    def remove_item(self, request: Request) -> Response:
        """
        Remove item (total/parcial) do carrinho. Usa RemoveItemSerializer para documentação.
        """
        cart = self._get_cart_from_request(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data.get("quantity")

        try:
            self.service.remove_item(
                cart=cart, product_id=product_id, quantity=quantity
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
