from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)  # Quantità di token disponibili
    last_updated = models.DateTimeField(auto_now=True)  # Quando sono stati aggiornati i token

    def add_tokens(self, amount):
        self.amount += amount
        self.save()

    def deduct_tokens(self, amount):
        if self.amount >= amount:
            self.amount -= amount
            self.save()
            return True
        return False
