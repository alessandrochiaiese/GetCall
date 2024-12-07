from django.db import models 


class AffiliatePayout(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name='affiliate_payout_affiliates') 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    payout_date = models.DateField()
    payout_method = models.CharField(max_length=50)
    payout_status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255)
    processing_fee = models.DecimalField(max_digits=5, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payout_provider = models.CharField(max_length=50)

    class Meta:
        ordering = ['-payout_date']
        verbose_name = "Affiliate Payout"
        verbose_name_plural = "Affiliate Payouts"

"""class AffiliatePayout(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name="payouts")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    payout_date = models.DateTimeField(auto_now_add=True)
    payout_method = models.CharField(max_length=50)
    payout_status = models.CharField(max_length=50, choices=[("processed", "Processed"), ("failed", "Failed")])
"""