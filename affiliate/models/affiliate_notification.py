
from django.db import models 

class AffiliateNotification(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name='affiliate_notification_affiliates') 
    message = models.TextField()
    date_sent = models.DateField()
    is_read = models.BooleanField(default=False)
    priority = models.CharField(max_length=50)
    notification_type = models.CharField(max_length=50)

    class Meta:
        ordering = ['-date_sent']
        verbose_name = "Affiliate Notification"
        verbose_name_plural = "Affiliate Notifications"

"""
class AffiliateNotification(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name="notifications")
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
"""