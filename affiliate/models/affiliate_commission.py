
from django.db import models 

class AffiliateCommission(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name='affiliate_commission_affiliates')
    programs = models.ManyToManyField('AffiliateProgram', related_name='affiliate_commission_programs')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    date_awarded = models.DateField()
    status = models.CharField(max_length=50)
    approved_by = models.CharField(max_length=255)
    commission_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    tier = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['-date_awarded']
        verbose_name = "Affiliate Commission"
        verbose_name_plural = "Affiliate Commissions"

"""
class AffiliateCommission(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE)
    partecipation = models.OneToOneField('AffiliateProgramPartecipation', on_delete=models.CASCADE)
    program = models.OneToOneField('AffiliateProgram', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_awarded = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")])
    approved_by = models.CharField(max_length=255, null=True, blank=True)
"""