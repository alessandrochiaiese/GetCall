from django.db import models
from django.utils.timezone import now

class TokenPrice(models.Model):
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Prezzo per la quantità di token
