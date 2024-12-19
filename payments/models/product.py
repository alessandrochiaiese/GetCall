
from locale import currency
from django.db import models
from django.utils.translation import gettext_lazy as _

from payments.models.product_tag import ProductTag
from payments.models.utils import get_image_filename
"""
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Prezzo con 2 decimali
    quantity_in_stock = models.IntegerField()  # Quantità disponibile in magazzino
    created_at = models.DateTimeField(auto_now=True)  # Data e ora di creazione dell'ordine
    
    def __str__(self):
        return self.name
"""
class Product(models.Model):
    name = models.CharField(max_length=200)
    #tags = models.ManyToManyField(ProductTag, blank=True, related_name="tags")
    description = models.TextField(_("Description"), blank=True)
    thumbnail = models.ImageField(upload_to=get_image_filename, blank=True)
    url = models.URLField()  
    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
