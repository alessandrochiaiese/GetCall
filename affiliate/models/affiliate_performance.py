

from django.db import models 

class AffiliatePerformance(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name='affiliate_performance_affiliates') 
    period = models.CharField(max_length=50)  # ad esempio "mensile", "annuale"
    total_clicks = models.IntegerField()
    total_conversions = models.IntegerField()
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    refund_rate = models.DecimalField(max_digits=5, decimal_places=2)
    customer_lifetime_value = models.DecimalField(max_digits=10, decimal_places=2)
    top_product = models.CharField(max_length=255)
    
    class Meta: 
        verbose_name = "Affiliate Perfomance"
        verbose_name_plural = "Affiliate Perfomances"

"""
class AffiliatePerformance(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE)
    period = models.CharField(max_length=50)  # e.g., "monthly", "yearly"
    total_clicks = models.IntegerField()
    total_conversions = models.IntegerField()
    conversion_rate = models.FloatField()
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
"""