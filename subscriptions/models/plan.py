from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Plan(models.Model):
    DURATION_CHOICES = [
        ('daily', 'Giornaliero'),
        ('weekly', 'Settimanale'),
        ('monthly', 'Mensile'),
        ('yearly', 'Annuale'),
    ]

    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Prezzo in euro
    tokens_included = models.PositiveIntegerField(default=0)  # Token inclusi

    def get_duration_timedelta(self):
        if self.duration == 'daily':
            return timedelta(days=1)
        elif self.duration == 'weekly':
            return timedelta(weeks=1)
        elif self.duration == 'monthly':
            return timedelta(days=30)
        elif self.duration == 'yearly':
            return timedelta(days=365)
        return timedelta(0)
