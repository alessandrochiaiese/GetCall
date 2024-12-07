from django.db import models


class AffiliateAudit(models.Model):
    affiliates = models.ManyToManyField('Affiliate', blank=True, related_name='affiliate_audit_affiliates') #[1,2]
    action_taken = models.TextField()
    action_date = models.DateField()
    ip_address = models.GenericIPAddressField()
    device_info = models.TextField()
    location = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-action_date']
        verbose_name = "Affiliate Audit"
        verbose_name_plural = "Affiliate Audits"
"""
class AffiliateAudit(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=255)
    action_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    device_info = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
"""