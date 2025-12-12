from django.db import models


class Product(models.Model):
    """
    Produto básico utilizado pelo carrinho.
    O carrinho não depende de nenhum app externo.
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)  # <-- adicionado para validação de estoque
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "cart_product"
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.name
