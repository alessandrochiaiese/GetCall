from django.db import models

class AffiliateCampaign(models.Model):
    programs = models.ManyToManyField('AffiliateProgram', related_name='affiliate_campaign_programs')
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    goal = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    spending_to_date = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Affiliate Campaign"
        verbose_name_plural = "Affiliate Campaigns"

"""
class AffiliateCampaign(models.Model):
    program = models.OneToOneField('AffiliateProgram', on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    goal = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    spending_to_date = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
"""