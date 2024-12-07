from django.db import models 

from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralNotification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='engagement_notification_user')
    message = models.TextField()
    date_sent = models.DateField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    action_required = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_sent']
        verbose_name = "Referral Notification"
        verbose_name_plural = "Referral Notifications"


"""class ReferralNotification(models.Model):
    user = models.ManyToManyField('User', related_name="referral_notifications")
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)"""