# affiliate_system/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class AffiliateLink(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name='affiliate_link_affiliates')
    programs = models.ManyToManyField('AffiliateProgram', related_name='affiliate_link_programs')
    url = models.URLField()
    click_count = models.IntegerField(default=0)
    conversion_count = models.IntegerField(default=0)
    date_created = models.DateField()
    last_used = models.DateTimeField(null=True, blank=True)
    link_status = models.CharField(max_length=50)
    landing_page = models.URLField(blank=True)
    custom_tracking_id = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Affiliate Link"
        verbose_name_plural = "Affiliate Links"

"""
class AffiliateLink(models.Model):
    program = models.OneToOneField('AffiliateProgram', on_delete=models.CASCADE)
    affiliates = models.ManyToManyField('Affiliate', related_name="affiliate_links")
    url = models.URLField()
    click_count = models.IntegerField(default=0)
    conversion_count = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    link_status = models.CharField(max_length=50, choices=[("active", "Active"), ("expired", "Expired")])

class AffiliateLink(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE)
    program = models.OneToOneField('AffiliateProgram', on_delete=models.CASCADE)
    url = models.URLField()
    click_count = models.IntegerField(default=0)
    conversion_count = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    link_status = models.CharField(max_length=50, choices=[("active", "Active"), ("expired", "Expired")])

    def __str__(self):
        return f"Link by {self.affiliate.user.username} - {self.url}"

class AffiliateLink(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name="links")
    url = models.URLField()
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Link by {self.affiliate.user.username} - {self.url}"
"""