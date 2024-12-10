
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Prezzo con 2 decimali
    quantity_in_stock = models.IntegerField()  # Quantità disponibile in magazzino
    created_at = models.DateTimeField(auto_now=True)  # Data e ora di creazione dell'ordine
    
    def __str__(self):
        return self.name
