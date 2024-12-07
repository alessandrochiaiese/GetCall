from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class ReferralEngagement(models.Model):
    referral_codes = models.ManyToManyField('ReferralCode', related_name='referral_engagement_referral_codes')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    email_opened = models.BooleanField(default=False)
    email_clicked = models.BooleanField(default=False)
    social_share_count = models.IntegerField(default=0)
    last_interaction_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-last_interaction_date']
        verbose_name = "Referral Engagement"
        verbose_name_plural = "Referral Engagements"
