from django.db import models


from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralConversion(models.Model):
    referral_codes = models.ManyToManyField('ReferralCode', related_name='referral_conversion_referral_codes')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referral_conversion_user')
    conversion_date = models.DateField()
    conversion_value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    reward_issued = models.BooleanField(default=False)
    conversion_source = models.CharField(max_length=50)
    referral_type = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-conversion_date']
        verbose_name = "Referral Conversation"
        verbose_name_plural = "Referral Conversations"

"""class ReferralConversion(models.Model):
    referral_code_id = models.IntegerField()  # Assuming it's an integer ID from another table
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')  # User ID of the referred user
    conversion_date = models.DateTimeField()
    conversion_value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)  # E.g., 'Completed', 'Pending', etc.
    reward_issued = models.BooleanField(default=False)
    conversion_source = models.CharField(max_length=255)  # E.g., 'Email', 'Social Media', etc.
    referral_type = models.CharField(max_length=255)  # E.g., 'First purchase', 'Sign-up', etc.

    def __str__(self):
        return f"Conversion {self.id} - Referral {self.referral_code_id}"
"""