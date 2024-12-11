
from django.db import models

from payments.models.product import Product

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    price = models.DecimalField(decimal_places=2, max_digits=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.product.name} {self.price}"