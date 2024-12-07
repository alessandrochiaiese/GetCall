# referral_system/models.py

from django.db import models
from django.contrib.auth import get_user_model

from accounts.models.region import Region

User = get_user_model()

class ReferralProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    reward_type = models.CharField(max_length=50)
    reward_value = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    min_referral_count = models.IntegerField(default=0)
    max_referrals_per_user = models.IntegerField(default=100)
    date_created = models.DateField()
    is_active = models.BooleanField(default=True)
    program_duration = models.IntegerField()
    allowed_regions = models.ManyToManyField(Region, related_name='engagement_program_regions')
    target_industry = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Referral Program"
        verbose_name_plural = "Referral Program"

"""
class ReferralProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    reward_type = models.CharField(max_length=50)
    reward_value = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    min_referral_count = models.IntegerField(default=1)
    max_referrals_per_user = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class ReferralProgram(models.Model):
    name = models.CharField(max_length=100)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
"""