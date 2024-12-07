# affiliate_system/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class AffiliateReward(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name="affiliate_reward_affiliates")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reward for {self.affiliate.user.username} - {self.amount} EUR"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Affiliate Reward"
        verbose_name_plural = "Affiliate Rewards"
