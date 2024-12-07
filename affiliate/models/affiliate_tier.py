from django.db import models

class AffiliateTier(models.Model): 
    programs = models.ManyToManyField('AffiliateProgram', related_name='affiliate_tier_programs')
    tier_name = models.CharField(max_length=50)
    min_sales = models.IntegerField()
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tier_benefits = models.TextField(blank=True)
    access_level = models.IntegerField()
    next_tier_threshold = models.IntegerField()
    tier_expiration = models.DateField(null=True, blank=True)

 
    def __str__(self):
        return f"{self.tier_name} (Program {self.program.id})"

    class Meta: 
        verbose_name = "Affiliate Tier"
        verbose_name_plural = "Affiliate Tiers"
