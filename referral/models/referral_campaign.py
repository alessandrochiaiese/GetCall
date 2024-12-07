from django.db import models

class ReferralCampaign(models.Model):
    programs = models.ManyToManyField('ReferralProgram', related_name='referral_campaign_programs')
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    goal = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    spending_to_date = models.DecimalField(max_digits=10, decimal_places=2)
    target_audience = models.TextField(blank=True)

    class Meta:
        ordering = ['-end_date']
        verbose_name = "Referral Campaign"
        verbose_name_plural = "Referral Campaigns"
