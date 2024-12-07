from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ReferralSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referra_setting_user')
    default_reward_type = models.CharField(max_length=50)
    max_referrals_allowed = models.IntegerField(default=100)
    notification_preference = models.CharField(max_length=50)
    auto_share_setting = models.BooleanField(default=True)
    social_share_message = models.TextField(blank=True)

    class Meta: 
        verbose_name = "Referral Settings"
        verbose_name_plural = "Referral Settings"

"""class ReferralSettings(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    default_reward_type = models.CharField(max_length=50)
    max_referrals_allowed = models.IntegerField(default=0)
    notification_preference = models.CharField(max_length=50)
"""