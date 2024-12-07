from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referra_user_user')
    total_referrals = models.IntegerField(default=0)
    active_referrals = models.IntegerField(default=0)
    inactive_referrals = models.IntegerField(default=0)
    total_rewards_earned = models.DecimalField(max_digits=10, decimal_places=2)
    total_spent_by_referred_users = models.DecimalField(max_digits=10, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    loyalty_points_earned = models.IntegerField(default=0)

    class Meta: 
        verbose_name = "Referral User"
        verbose_name_plural = "Referral Users"

"""class ReferralUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')  # User reference ID, assuming it's an integer
    total_referrals = models.IntegerField(default=0)
    active_referrals = models.IntegerField(default=0)
    inactive_referrals = models.IntegerField(default=0)
    total_rewards_earned = models.DecimalField(max_digits=10, decimal_places=2)
    total_spent_by_referred_users = models.DecimalField(max_digits=10, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    loyalty_points_earned = models.IntegerField(default=0)

    def __str__(self):
        return f"ReferralUser {self.user_id}"
"""