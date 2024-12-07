
from django.db import models

from accounts.models.country import Country 

class AffiliateProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=10)
    min_payout_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    max_payout_limit = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateField()
    is_active = models.BooleanField(default=True)
    duration = models.IntegerField()  # durata in giorni
    allowed_countries = models.ManyToManyField(Country, related_name='affiliate_program_countries')
    target_industry = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Affiliate Program"
        verbose_name_plural = "Affiliate Programs"

"""
class AffiliateProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=10)
    min_payout_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_payout_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    duration = models.IntegerField(help_text="Duration in days", null=True, blank=True)
    allowed_countries = models.CharField(max_length=255, null=True, blank=True)
    target_industry = models.CharField(max_length=255, null=True, blank=True)
"""
