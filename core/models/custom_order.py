#pip install django-getpaid
#pip install django-getpaid-payu

from django.urls import reverse
from accounts.models.user import User
from getref import settings
from getpaid.abstracts import AbstractOrder
from django.db import models

class CustomOrder(AbstractOrder):
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    description = models.CharField(max_length=128)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={"pk": self.pk})

    def get_total_amount(self):
        return self.amount

    def get_buyer_info(self):
        return {"email": self.buyer.email}

    def get_currency(self):
        return "EUR"

    def get_description(self):
        return self.description