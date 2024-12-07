from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referral_code_user')
    programs = models.ManyToManyField('ReferralProgram', related_name='referral_code_programs')
    code = models.CharField(max_length=50, unique=True)
    usage_count = models.IntegerField(default=0)
    date_created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    expiry_date = models.DateField(null=True, blank=True)
    referred_user_count = models.IntegerField(default=0)
    unique_url = models.URLField(blank=True)
    campaign_source = models.CharField(max_length=100, blank=True)
    campaign_medium = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Referral Code"
        verbose_name_plural = "Referral Codes"

"""
class ReferralCode(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    programs = models.ManyToManyField('ReferralProgram', through='ReferralProgramPartecipation', related_name="referral_codes")
    code = models.CharField(max_length=255, unique=True)
    usage_count = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("expired", "Expired")])
    expiry_date = models.DateField(null=True, blank=True)

class ReferralCode(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    program = models.OneToOneField('ReferralProgram', on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)
    usage_count = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("expired", "Expired")])
    expiry_date = models.DateField(null=True, blank=True)
"""