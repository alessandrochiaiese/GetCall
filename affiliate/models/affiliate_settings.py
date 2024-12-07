from django.db import models 

class AffiliateSettings(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name='affiiate_setting_affiliates') 
    preferred_currency = models.CharField(max_length=10)
    preferred_payment_method = models.CharField(max_length=50)
    payout_schedule = models.CharField(max_length=50)
    notification_preference = models.CharField(max_length=50)
    dashboard_layout = models.CharField(max_length=50)
    
    class Meta: 
        verbose_name = "Affiliate Setting"
        verbose_name_plural = "Affiliate Settings"

"""
class AffiliateSettings(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE)
    preferred_currency = models.CharField(max_length=10)
    preferred_payment_method = models.CharField(max_length=50)
    payout_schedule = models.CharField(max_length=50)
    notification_preference = models.CharField(max_length=50)
"""