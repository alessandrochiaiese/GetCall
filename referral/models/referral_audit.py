from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralAudit(models.Model):
    referral_codes = models.ManyToManyField('ReferralCode', related_name='referral_audit_referral_codes')
    action_taken = models.TextField()
    action_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referral_audit_referral_user')
    ip_address = models.GenericIPAddressField()
    device_info = models.TextField()
    location = models.CharField(max_length=100)


    class Meta:
        ordering = ['-action_date']
        verbose_name = "Referral Audit"
        verbose_name_plural = "Referral Audits"

"""class ReferralAudit(models.Model):
    referral_code = models.OneToOneField('ReferralCode', on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=255)
    action_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField() 
    device_info = models.TextField()

    def __str__(self):
        return f"Audit {self.id} - {self.action_taken} by User {self.user_id}"""