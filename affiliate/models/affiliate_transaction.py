from django.db import models 


class AffiliateTransaction(models.Model):
    commissions = models.ManyToManyField('AffiliateCommission', related_name='affiliate_transaction_commissions')
    affiliates = models.ManyToManyField('Affiliate', related_name='affiliate_transaction_affiliates') 
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    order_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    payment_date = models.DateField(null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    discount_applied = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    coupon_code = models.CharField(max_length=255, blank=True)

    class Meta: 
        verbose_name = "Affiliate Transaction"
        verbose_name_plural = "Affiliate Transactions"

"""class AffiliateTransaction(models.Model):
    commission = models.OneToOneField('AffiliateCommission', on_delete=models.CASCADE)
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField()
    order_id = models.CharField(max_length=255)
    product_id = models.IntegerField()
    status = models.CharField(max_length=50, choices=[("completed", "Completed"), ("cancelled", "Cancelled")])
"""