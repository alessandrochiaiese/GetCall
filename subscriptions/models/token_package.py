from django.db import models

class TokenPackage(models.Model):
    name = models.CharField(max_length=100)
    price_in_cents = models.IntegerField()  # Prezzo in centesimi (per evitare problemi con i decimali)
    tokens = models.IntegerField()  # Numero di token nel pacchetto

    def __str__(self):
        return self.name
