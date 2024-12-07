# referral_system/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ReferralReward(models.Model):
    referral_codes = models.ManyToManyField('ReferralCode', related_name='referra_reward_referral_codes')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referra_reward_user')
    reward_type = models.CharField(max_length=50)
    reward_value = models.DecimalField(max_digits=10, decimal_places=2)
    date_awarded = models.DateField()
    status = models.CharField(max_length=50)
    expiry_date = models.DateField(null=True, blank=True)
    reward_description = models.TextField(blank=True)
    reward_source = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date_awarded']
        verbose_name = "Referral Reward"
        verbose_name_plural = "Referral Rewards"

"""
class ReferralReward(models.Model):
    referral_code = models.ManyToManyField('ReferralCode', related_name="rewards")
    reward_type = models.CharField(max_length=50)
    reward_value = models.DecimalField(max_digits=10, decimal_places=2)
    date_awarded = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

class ReferralReward(models.Model):
    referral_code = models.OneToOneField('ReferralCode', on_delete=models.CASCADE)
    referred_user = models.OneToOneField('User', on_delete=models.CASCADE)
    reward_type = models.CharField(max_length=50)
    reward_value = models.DecimalField(max_digits=10, decimal_places=2)
    date_awarded = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

class ReferralReward(models.Model):
    referral = models.OneToOneField('Referral', on_delete=models.CASCADE, related_name="reward")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_given = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reward for {self.referral.referrer.username} - {self.amount} EUR"
"""